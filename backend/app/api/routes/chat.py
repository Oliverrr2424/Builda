import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import Settings, get_settings
from app.schemas.chat import ChatPlanRequest, ChatPlanResponse
from app.services import GeminiPlannerError, get_gemini_planner
from app.services.sample_data import generate_sample_plan

router = APIRouter(prefix="/chat", tags=["chat"])

LOGGER = logging.getLogger(__name__)


@router.post("/plan", response_model=ChatPlanResponse)
async def generate_plan(
    payload: ChatPlanRequest,
    settings: Settings = Depends(get_settings),
) -> ChatPlanResponse:
    """调用 Gemini 生成方案，若不可用则回退示例方案。"""

    planner = get_gemini_planner(settings.gemini_api_key)
    if planner.available:
        try:
            return await planner.generate_plan(payload)
        except GeminiPlannerError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Gemini planner failed, falling back to sample plan: %s", exc)

    return generate_sample_plan()
