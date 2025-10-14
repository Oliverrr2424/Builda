from typing import List

from pydantic import BaseModel, Field

from .chat import BuildComponent


class BuildValidationItem(BaseModel):
    component: BuildComponent
    quantity: int = Field(default=1, ge=1, description="组件数量")


class BuildValidationRequest(BaseModel):
    items: List[BuildValidationItem] = Field(..., description="待校验的组件列表")


class BuildValidationResult(BaseModel):
    is_valid: bool = Field(..., description="兼容性是否通过")
    issues: List[str] = Field(default_factory=list, description="发现的问题列表")
    recommendations: List[str] = Field(
        default_factory=list, description="改进建议，例如升级电源"
    )
