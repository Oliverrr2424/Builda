from typing import List

from pydantic import BaseModel, Field

from .chat import BuildComponent


class BuildValidationItem(BaseModel):
    component: BuildComponent
    quantity: int = Field(default=1, ge=1, description="Component quantity")


class BuildValidationRequest(BaseModel):
    items: List[BuildValidationItem] = Field(..., description="List of components to validate")


class BuildValidationResult(BaseModel):
    is_valid: bool = Field(..., description="Whether compatibility checks passed")
    issues: List[str] = Field(default_factory=list, description="List of discovered issues")
    recommendations: List[str] = Field(
        default_factory=list, description="Improvement recommendations, e.g., upgrade the PSU"
    )
