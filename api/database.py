"""
Backward compatibility shim for api.database.
Canonical location is now api.core.database.
"""
from api.core.database import (
    get_mongo_db,
    in_memory_store,
    InMemoryStore,
    seed_initial_notes,
)

__all__ = [
    "get_mongo_db",
    "in_memory_store",
    "InMemoryStore",
    "seed_initial_notes",
]
