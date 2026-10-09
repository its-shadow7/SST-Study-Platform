from typing import List, Optional
from pydantic import BaseModel, Field

class GoogleLoginRequest(BaseModel):
    id_token: str = Field(..., description="Google ID Token issued by GIS")
    nonce: Optional[str] = Field(None, description="One-time login nonce")

class UserResponse(BaseModel):
    user_id: str
    email: str
    display_name: str
    status: str
    csrf_token: Optional[str] = None

class AuthResponse(BaseModel):
    user: UserResponse
    csrf_token: str

class BookmarkItem(BaseModel):
    note_id: str
    created_at: str

class BookmarkListResponse(BaseModel):
    bookmarks: List[BookmarkItem]

class BookmarkActionResponse(BaseModel):
    note_id: str
    status: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: str
