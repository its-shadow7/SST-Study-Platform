"""
Backward compatibility shim for api.models.
Canonical location is now api.schemas.
"""
from api.schemas.auth import (
    GoogleLoginRequest,
    UserResponse,
    UpdateProfileRequest,
    PublicUserProfileResponse,
    AuthResponse,
    BookmarkItem,
    BookmarkListResponse,
    BookmarkActionResponse,
    ErrorResponse,
)
from api.schemas.comment import (
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

__all__ = [
    "GoogleLoginRequest",
    "UserResponse",
    "UpdateProfileRequest",
    "PublicUserProfileResponse",
    "AuthResponse",
    "BookmarkItem",
    "BookmarkListResponse",
    "BookmarkActionResponse",
    "ErrorResponse",
    "CommentDocument",
    "CreateCommentRequest",
    "CommentListResponse",
    "DeleteCommentResponse",
    "VoteCommentRequest",
    "VoteCommentResponse",
    "ReportCommentRequest",
    "ReportCommentResponse",
    "ResolveModerationRequest",
    "ResolveModerationResponse",
    "ModerationQueueResponse",
    "ModerationAuditLogItem",
    "ModerationAuditLogResponse",
    "NotificationItem",
    "NotificationListResponse",
]
