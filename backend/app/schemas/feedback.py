from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    plan_id: Optional[str] = Field(default=None, description="关联的方案 ID")
    rating: int = Field(..., ge=1, le=5, description="用户评分")
    comment: Optional[str] = Field(default=None, description="用户反馈内容")
    purchased: bool = Field(default=False, description="用户是否购买")


class FeedbackResponse(BaseModel):
    feedback_id: str = Field(..., description="反馈标识")
    submitted_at: datetime = Field(..., description="反馈提交时间")
