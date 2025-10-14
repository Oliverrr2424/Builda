from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    plan_id: Optional[str] = Field(default=None, description="Associated plan ID")
    rating: int = Field(..., ge=1, le=5, description="User rating")
    comment: Optional[str] = Field(default=None, description="User feedback content")
    purchased: bool = Field(default=False, description="Whether the user purchased")


class FeedbackResponse(BaseModel):
    feedback_id: str = Field(..., description="Feedback identifier")
    submitted_at: datetime = Field(..., description="Feedback submission time")
