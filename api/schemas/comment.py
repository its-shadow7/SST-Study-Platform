from datetime import datetime, timezone
from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class CreateCommentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Comment body (max 1000 characters)")
    parent_id: Optional[str] = Field(None, description="Optional parent comment ID for threaded replies")

class VoteCommentRequest(BaseModel):
    action: Literal["upvote", "downvote"] = Field(..., description="Vote action: upvote or downvote")

class VoteCommentResponse(BaseModel):
    id: str
    score: int
    user_vote: Optional[str] = Field(None, description="'upvote', 'downvote', or None if unvoted")

class CommentDocument(BaseModel):
    id: str = Field(..., description="Stringified MongoDB ObjectId")
    note_id: str = Field(..., description="Identifier of the lecture note")
    user_id: str = Field(..., description="Stringified user ID mapping to Users collection _id")
    content: str = Field(..., max_length=1000, description="Sanitized comment content")
    parent_id: Optional[str] = Field(None, description="Parent comment ID for threaded replies")
    score: int = Field(0, description="Aggregate vote score (upvotes minus downvotes)")
    upvoted_by: List[str] = Field(default_factory=list, description="List of user IDs who upvoted")
    downvoted_by: List[str] = Field(default_factory=list, description="List of user IDs who downvoted")
    status: Literal["published", "quarantined", "reported", "deleted"] = Field("published", description="Moderation status")
    moderation_reasons: List[str] = Field(default_factory=list, description="OpenAI flags or user report reasons")
    reported_by: List[str] = Field(default_factory=list, description="User IDs who reported this comment")
    report_history: List[dict] = Field(default_factory=list, description="Timestamped report events for audit and velocity quarantine")
    created_at: str = Field(..., description="ISO 8601 creation timestamp")
    updated_at: str = Field(..., description="ISO 8601 update timestamp")
    username: Optional[str] = Field(None, description="Author's public handle joined from Users")
    avatar_url: Optional[str] = Field(None, description="Author's avatar URL joined from Users")
    author_role: Optional[Literal["student", "moderator", "admin"]] = Field("student", description="Author's role joined from Users")

class CommentListResponse(BaseModel):
    comments: List[CommentDocument]
    total: int

class DeleteCommentResponse(BaseModel):
    status: str
    id: str

class ReportCommentRequest(BaseModel):
    reason: str = Field(..., min_length=1, max_length=500, description="Reason for reporting this comment")

class ReportCommentResponse(BaseModel):
    message: str
    status: str
    id: str

class ResolveModerationRequest(BaseModel):
    action: Literal["approve", "delete"] = Field(..., description="Action to take: approve or delete")

class ResolveModerationResponse(BaseModel):
    message: str
    status: str
    id: str

class ModerationQueueResponse(BaseModel):
    queue: List[CommentDocument]
    total: int

class ModerationAuditLogItem(BaseModel):
    id: str = Field(..., description="Audit log ID")
    action: Literal["approved", "deleted", "auto_quarantined", "quarantined"] = Field(..., description="Action performed")
    comment_id: str = Field(..., description="Target comment ID")
    note_id: Optional[str] = Field(None, description="Course note ID")
    comment_content: Optional[str] = Field(None, description="Snippet of comment content")
    moderator_id: str = Field(..., description="User ID of moderator or 'system'")
    moderator_name: str = Field(..., description="Name or handle of moderator")
    moderator_role: str = Field(..., description="Role of moderator")
    reason: Optional[str] = Field(None, description="Resolution or auto-quarantine reason")
    created_at: str = Field(..., description="ISO timestamp")

class ModerationAuditLogResponse(BaseModel):
    logs: List[ModerationAuditLogItem]
    total: int

class NotificationItem(BaseModel):
    id: str = Field(..., description="Notification ID")
    user_id: str = Field(..., description="Recipient user ID")
    type: Literal["reply", "report_resolved", "comment_status", "system"] = Field(..., description="Notification category")
    title: str = Field(..., description="Short notification title")
    message: str = Field(..., description="Notification body")
    link: Optional[str] = Field(None, description="Target note URL or link")
    read: bool = Field(False, description="Read status")
    created_at: str = Field(..., description="ISO timestamp")

class NotificationListResponse(BaseModel):
    notifications: List[NotificationItem]
    unread_count: int
