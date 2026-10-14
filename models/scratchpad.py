from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field


class UpdateScratchpadRequest(BaseModel):
    content: str = Field(
        ...,
        max_length=30000,
        description="Scratchpad markdown content (max 30,000 characters)"
    )


class PrivateNoteDocument(BaseModel):
    id: Optional[str] = Field(None, description="Stringified MongoDB ObjectId")
    user_id: str = Field(..., description="Stringified student user ID")
    note_id: str = Field(..., description="Unique identifier of the lecture note")
    content: str = Field(..., max_length=30000, description="Scratchpad markdown content")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ScratchpadResponse(BaseModel):
    id: Optional[str] = Field(None, description="Stringified MongoDB ObjectId")
    user_id: Optional[str] = Field(None, description="Stringified user ID")
    note_id: str = Field(..., description="Unique identifier of the lecture note")
    content: str = Field("", description="Scratchpad markdown content")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp in ISO format")


class ScratchpadSummaryResponse(BaseModel):
    note_ids: List[str] = Field(
        default_factory=list,
        description="List of note_ids where student has non-empty scratchpad content"
    )
