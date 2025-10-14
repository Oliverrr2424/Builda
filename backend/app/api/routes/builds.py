from fastapi import APIRouter

from app.schemas.build import BuildValidationRequest, BuildValidationResult
from app.services.sample_data import validate_build

router = APIRouter(prefix="/builds", tags=["builds"])


@router.post("/validate", response_model=BuildValidationResult)
async def validate(payload: BuildValidationRequest) -> BuildValidationResult:
    """执行基础的兼容性校验示例。"""

    # TODO: 根据 payload.items 实现真实的兼容性检测逻辑
    return validate_build()
