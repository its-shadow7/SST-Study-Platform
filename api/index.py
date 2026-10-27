import logging
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.core.config import settings
from api.core.database import get_mongo_db, in_memory_store, seed_initial_notes
from api.core.dependencies import get_current_student, get_db_or_fail
from api.core.rate_limiter import check_rate_limit
from api.routes import (
    auth_router,
    notes_router,
    comments_router,
    quizzes_router,
    scratchpad_router,
    moderation_router,
    notifications_router,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager:
    Initializes database indexes and runs startup catalogue seeding
    from content/fixtures/ into MongoDB and InMemoryStore.
    """
    try:
        db = get_mongo_db()
        seed_initial_notes(db)
        logger.info("Startup notes catalogue seeding completed successfully.")
    except Exception as exc:
        logger.warning("Startup catalogue seeding encountered a warning: %s", exc)
    yield


app = FastAPI(
    title="SST Study Platform API",
    version="1.1",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# CORS configuration
if settings.APP_ORIGIN:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            settings.APP_ORIGIN,
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )


# --- Common JSON Error Response Handlers ---
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = str(uuid.uuid4())
    error_code = (
        "UNAUTHORIZED"
        if exc.status_code == 401
        else (
            "FORBIDDEN"
            if exc.status_code == 403
            else (
                "NOT_FOUND"
                if exc.status_code == 404
                else (
                    "UNPROCESSABLE_ENTITY"
                    if exc.status_code == 422
                    else (
                        "TOO_MANY_REQUESTS"
                        if exc.status_code == 429
                        else (
                            "SERVICE_UNAVAILABLE"
                            if exc.status_code == 503
                            else "BAD_REQUEST"
                        )
                    )
                )
            )
        )
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_code,
            "message": str(exc.detail),
            "request_id": request_id,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = str(uuid.uuid4())
    logger.warning("Validation error [req_id=%s]: %s", request_id, exc.errors())
    err_msgs = [
        f"{'.'.join(str(loc) for loc in err.get('loc', []))}: {err.get('msg')}"
        for err in exc.errors()
    ]
    summary_msg = "; ".join(err_msgs) if err_msgs else "The request payload failed validation."
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": summary_msg,
            "request_id": request_id,
            "details": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = str(uuid.uuid4())
    logger.error("Unhandled server exception [req_id=%s]: %s", request_id, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred. Please try again later.",
            "request_id": request_id,
        },
    )


# ==============================================================================
# Health Check Endpoint
# ==============================================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "service": "sst-study-platform",
        "time": datetime.now(timezone.utc).isoformat(),
    }


# ==============================================================================
# Backward-compatibility routes for /data/ paths
# ==============================================================================

@app.get("/data/notes-index.json")
async def get_legacy_notes_index(user: dict = Depends(get_current_student)):
    """
    Backward-compatibility shim for legacy clients and tests.
    Queries the database / in_memory_store for all published notes.
    """
    db = get_db_or_fail()
    if db is not None:
        notes = list(db.notes.find({"status": "published"}))
    else:
        notes = in_memory_store.list_notes(include_drafts=False)
    
    # Strip MongoDB _id
    for n in notes:
        n.pop("_id", None)
    return notes


@app.get("/data/notes/{note_id}.json")
async def get_legacy_note_content(note_id: str, user: dict = Depends(get_current_student)):
    """
    Backward-compatibility shim for legacy clients and tests.
    """
    clean_id = note_id.lower().strip()
    db = get_db_or_fail()
    if db is not None:
        note = db.notes.find_one({"note_id": clean_id})
    else:
        note = in_memory_store.get_note(clean_id)

    if not note:
        raise HTTPException(status_code=404, detail=f"Note '{clean_id}' not found.")
    
    note.pop("_id", None)
    return note


# Mount domain routers
app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(comments_router)
app.include_router(quizzes_router)
app.include_router(scratchpad_router)
app.include_router(moderation_router)
app.include_router(notifications_router)
