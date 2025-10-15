from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role, e.g., user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatPlanRequest(BaseModel):
    messages: List[ChatMessage] = Field(
        ..., description="Conversation context in chronological order from oldest to latest"
    )
    budget: Optional[float] = Field(
        default=None, description="User budget cap, in USD or CNY"
    )
    currency: str = Field(default="USD", description="Currency unit for the budget")
    locale: str = Field(default="en-US", description="User preferred locale information")


class BuildComponent(BaseModel):
    category: str = Field(..., description="Component category, e.g., CPU, GPU")
    name: str = Field(..., description="Component name")
    price: float = Field(..., description="Component price")
    vendor: str = Field(..., description="Data source")
    url: Optional[str] = Field(default=None, description="Product detail URL")
    image_url: Optional[str] = Field(default=None, description="Product thumbnail URL")


class AlternativeBuild(BaseModel):
    title: str = Field(..., description="Alternative plan title")
    description: str = Field(..., description="Brief description of the plan")
    total_price: float = Field(..., description="Total price of the plan")
    components: List[BuildComponent] = Field(..., description="Components included in the plan")


class ChatPlanResponse(BaseModel):
    plan_id: str = Field(..., description="Plan identifier")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Time when the plan was generated"
    )
    total_price: float = Field(..., description="Total price of the primary plan")
    currency: str = Field(..., description="Currency unit for the total price")
    components: List[BuildComponent] = Field(..., description="Components of the primary plan")
    alternatives: List[AlternativeBuild] = Field(
        default_factory=list, description="List of alternative plans"
    )
    summary: str = Field(..., description="Plan summary")
    notes: Optional[str] = Field(default=None, description="Additional tips or notes")
