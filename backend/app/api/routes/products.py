from typing import List, Optional

from fastapi import APIRouter, Query

from app.schemas.product import Product
from app.services.sample_data import generate_sample_products

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/search", response_model=List[Product])
async def search_products(
    keyword: Optional[str] = Query(default=None, description="关键词"),
    category: Optional[str] = Query(default=None, description="产品类别"),
    min_price: Optional[float] = Query(default=None, ge=0, description="最低价格"),
    max_price: Optional[float] = Query(default=None, ge=0, description="最高价格"),
    tags: Optional[List[str]] = Query(default=None, description="场景标签"),
) -> List[Product]:
    """返回示例产品列表，后续可接入数据库与检索服务。"""

    products = generate_sample_products()
    filtered = []
    for product in products:
        if keyword and keyword.lower() not in product.name.lower():
            continue
        if category and product.category.lower() != category.lower():
            continue
        if min_price and product.price < min_price:
            continue
        if max_price and product.price > max_price:
            continue
        if tags and not set(tags).issubset(set(product.specs.get("scene_tags", []))):
            continue
        filtered.append(product)

    return filtered
