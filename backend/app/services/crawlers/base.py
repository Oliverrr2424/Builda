from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class CrawlerResult(BaseModel):
    sku: str = Field(..., description="Unique SKU from the data source")
    name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Current price")
    currency: str = Field(default="USD", description="Currency code")
    vendor: str = Field(..., description="Vendor identifier")
    rating: Optional[float] = Field(default=None, description="Average rating")
    stock_status: Optional[str] = Field(default=None, description="Inventory status")
    specs: Dict[str, Any] = Field(default_factory=dict, description="Normalized specs")
    url: Optional[str] = Field(default=None, description="Product URL")
    updated_at: datetime = Field(..., description="Timestamp of the capture")

    def to_metadata(self) -> Dict[str, Any]:
        data = self.model_dump()
        data["updated_at"] = self.updated_at.isoformat()
        return data
