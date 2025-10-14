from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductFilter(BaseModel):
    keyword: Optional[str] = Field(default=None, description="Keyword search")
    category: Optional[str] = Field(default=None, description="Product category")
    min_price: Optional[float] = Field(default=None, description="Minimum price")
    max_price: Optional[float] = Field(default=None, description="Maximum price")
    tags: List[str] = Field(default_factory=list, description="Scenario tags")


class Product(BaseModel):
    sku: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Current price")
    currency: str = Field(default="CNY", description="Currency of price")
    vendor: str = Field(..., description="Data source platform")
    rating: Optional[float] = Field(default=None, description="Rating")
    stock_status: Optional[str] = Field(default=None, description="Stock status")
    specs: dict = Field(default_factory=dict, description="Specification JSON")
    updated_at: datetime = Field(..., description="Last updated time")


class PricePoint(BaseModel):
    timestamp: datetime = Field(..., description="Price timestamp")
    price: float = Field(..., description="Price")
    currency: str = Field(default="CNY", description="Currency unit")
    vendor: str = Field(..., description="Price source platform")
