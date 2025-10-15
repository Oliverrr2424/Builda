from datetime import datetime
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.schemas.product import Product
from app.services import DataPipeline, SimpleVectorStore, get_pipeline, get_vector_store

router = APIRouter(prefix="/products", tags=["products"])


def _to_product(metadata: dict) -> Product:
    updated_at = metadata.get("updated_at")
    if isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
    return Product(
        sku=metadata["sku"],
        name=metadata["name"],
        category=metadata.get("category", ""),
        price=float(metadata.get("price", 0.0)),
        currency=metadata.get("currency", "USD"),
        vendor=metadata.get("vendor", "unknown"),
        rating=metadata.get("rating"),
        stock_status=metadata.get("stock_status"),
        specs=metadata.get("specs", {}),
        updated_at=updated_at or datetime.utcnow(),
    )


@router.get("/search", response_model=List[Product])
async def search_products(
    keyword: Optional[str] = Query(default=None, description="Keyword to search for"),
    category: Optional[str] = Query(default=None, description="Product category"),
    min_price: Optional[float] = Query(default=None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(default=None, ge=0, description="Maximum price filter"),
    tags: Optional[List[str]] = Query(default=None, description="Optional scenario tags"),
    store: SimpleVectorStore = Depends(get_vector_store),
) -> List[Product]:
    """Retrieve product details via the vector index."""

    results = store.search(
        keyword,
        category=category,
        min_price=min_price,
        max_price=max_price,
        tags=tags,
    )
    return [_to_product(item) for item in results]


@router.post("/refresh", response_model=dict)
async def refresh_products(pipeline: DataPipeline = Depends(get_pipeline)) -> dict:
    """Run the sample crawler and refresh the vector index."""

    results = await pipeline.refresh_samples()
    return {"ingested": len(results)}
