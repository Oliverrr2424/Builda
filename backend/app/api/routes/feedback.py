from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.feedback import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
async def submit_feedback(payload: FeedbackRequest) -> FeedbackResponse:
    """接收用户反馈并返回模拟的反馈编号。"""

    return FeedbackResponse(feedback_id=str(uuid4()), submitted_at=datetime.utcnow())
