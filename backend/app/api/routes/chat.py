from fastapi import APIRouter

from app.schemas.chat import ChatPlanRequest, ChatPlanResponse
from app.services.sample_data import generate_sample_plan

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/plan", response_model=ChatPlanResponse)
async def generate_plan(payload: ChatPlanRequest) -> ChatPlanResponse:
    """返回一份示例装机方案，后续可替换为真实 RAG 调用。"""

    # TODO: 将 payload 传递给 LLM/RAG 管道生成真实方案
    return generate_sample_plan()
