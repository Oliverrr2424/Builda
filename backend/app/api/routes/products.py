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
        currency=metadata.get("currency", "CNY"),
        vendor=metadata.get("vendor", "unknown"),
        rating=metadata.get("rating"),
        stock_status=metadata.get("stock_status"),
        specs=metadata.get("specs", {}),
        updated_at=updated_at or datetime.utcnow(),
    )


@router.get("/search", response_model=List[Product])
async def search_products(
    keyword: Optional[str] = Query(default=None, description="关键词"),
    category: Optional[str] = Query(default=None, description="产品类别"),
    min_price: Optional[float] = Query(default=None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(default=None, ge=0, description="最高价格"),
    tags: Optional[List[str]] = Query(default=None, description="场景标签"),
    store: SimpleVectorStore = Depends(get_vector_store),
) -> List[Product]:
    """使用向量索引检索产品信息。"""

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
    """运行示例爬虫并刷新向量索引。"""

    results = await pipeline.refresh_samples()
    return {"ingested": len(results)}
