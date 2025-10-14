from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductFilter(BaseModel):
    keyword: Optional[str] = Field(default=None, description="关键词搜索")
    category: Optional[str] = Field(default=None, description="产品类别")
    min_price: Optional[float] = Field(default=None, description="最低价格")
    max_price: Optional[float] = Field(default=None, description="最高价格")
    tags: List[str] = Field(default_factory=list, description="场景标签")


class Product(BaseModel):
    sku: str = Field(..., description="产品唯一标识")
    name: str = Field(..., description="产品名称")
    category: str = Field(..., description="产品类别")
    price: float = Field(..., description="当前价格")
    currency: str = Field(default="CNY", description="价格货币单位")
    vendor: str = Field(..., description="数据来源平台")
    rating: Optional[float] = Field(default=None, description="评分")
    stock_status: Optional[str] = Field(default=None, description="库存状态")
    specs: dict = Field(default_factory=dict, description="规格参数 JSON")
    updated_at: datetime = Field(..., description="最后更新时间")


class PricePoint(BaseModel):
    timestamp: datetime = Field(..., description="价格时间点")
    price: float = Field(..., description="价格")
    currency: str = Field(default="CNY", description="货币单位")
    vendor: str = Field(..., description="价格来源平台")
