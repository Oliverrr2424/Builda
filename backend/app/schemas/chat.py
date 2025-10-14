from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="消息角色，例如 user、assistant 或 system")
    content: str = Field(..., description="消息内容")


class ChatPlanRequest(BaseModel):
    messages: List[ChatMessage] = Field(
        ..., description="对话上下文，按时间顺序从最早到最新排列"
    )
    budget: Optional[float] = Field(
        default=None, description="用户预算上限，单位 USD 或 CNY"
    )
    currency: str = Field(default="CNY", description="预算使用的货币单位")
    locale: str = Field(default="zh-CN", description="用户偏好的区域信息")


class BuildComponent(BaseModel):
    category: str = Field(..., description="组件类别，例如 CPU、GPU")
    name: str = Field(..., description="组件名称")
    price: float = Field(..., description="组件价格")
    vendor: str = Field(..., description="数据来源")
    url: Optional[str] = Field(default=None, description="商品详情链接")


class AlternativeBuild(BaseModel):
    title: str = Field(..., description="备选方案标题")
    description: str = Field(..., description="方案简要说明")
    total_price: float = Field(..., description="方案总价")
    components: List[BuildComponent] = Field(..., description="方案包含的组件列表")


class ChatPlanResponse(BaseModel):
    plan_id: str = Field(..., description="方案标识")
    generated_at: datetime = Field(
        default_factory=datetime.utcnow, description="方案生成时间"
    )
    total_price: float = Field(..., description="主方案总价")
    currency: str = Field(..., description="总价货币单位")
    components: List[BuildComponent] = Field(..., description="主方案组件列表")
    alternatives: List[AlternativeBuild] = Field(
        default_factory=list, description="备选方案列表"
    )
    summary: str = Field(..., description="方案概要说明")
    notes: Optional[str] = Field(default=None, description="额外提示或注意事项")
