from typing import List

from fastapi import APIRouter, Path

from app.schemas.product import PricePoint
from app.services.sample_data import generate_price_history

router = APIRouter(prefix="/price", tags=["price"])


@router.get("/history/{sku}", response_model=List[PricePoint])
async def price_history(sku: str = Path(..., description="产品 SKU")) -> List[PricePoint]:
    """返回指定产品的价格历史数据。"""

    return generate_price_history(sku)
