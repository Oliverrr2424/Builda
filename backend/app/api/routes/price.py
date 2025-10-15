from typing import List

from fastapi import APIRouter, Path

from app.schemas.product import PricePoint
from app.services.sample_data import generate_price_history

router = APIRouter(prefix="/price", tags=["price"])


@router.get("/history/{sku}", response_model=List[PricePoint])
async def price_history(sku: str = Path(..., description="Product SKU")) -> List[PricePoint]:
    """Return price history data for the requested product."""

    return generate_price_history(sku)
