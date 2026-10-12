from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class GoogleLoginRequest(BaseModel):
    id_token: str = Field(..., description="Google ID Token issued by GIS")
    nonce: Optional[str] = Field(None, description="One-time login nonce")

class UserResponse(BaseModel):
    user_id: str
    email: str
    display_name: str
    status: str
    role: Literal["student", "moderator", "admin"] = "student"
    username: str
    active_term: int = 1
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    csrf_token: Optional[str] = None
    batch_year: Optional[int] = None
    year_of_study: Optional[int] = None
    max_allowed_term: Optional[int] = None
    is_special: Optional[bool] = False
    needs_profile_setup: Optional[bool] = False

class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Full display name")
    username: Optional[str] = Field(None, min_length=3, max_length=30, pattern=r'^[a-zA-Z0-9_]+$', description="Unique public handle")
    active_term: Optional[int] = Field(None, ge=1, le=12, description="Active curriculum term (1 to 12)")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar image URL")
    bio: Optional[str] = Field(None, max_length=300, description="Short student bio")
    needs_profile_setup: Optional[bool] = Field(None, description="One-time onboarding setup status")

class PublicUserProfileResponse(BaseModel):
    user_id: str
    username: str
    display_name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: str = "student"
    active_term: int = 1
    batch_year: Optional[int] = None
    total_comments: int = 0
    total_upvotes: int = 0
    badges: List[str] = []
    recent_comments: List[dict] = []

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

from models.comment import (
    CommentDocument,
    CreateCommentRequest,
    CommentListResponse,
    DeleteCommentResponse,
    VoteCommentRequest,
    VoteCommentResponse,
    ReportCommentRequest,
    ReportCommentResponse,
    ResolveModerationRequest,
    ResolveModerationResponse,
    ModerationQueueResponse,
    ModerationAuditLogItem,
    ModerationAuditLogResponse,
    NotificationItem,
    NotificationListResponse,
)
