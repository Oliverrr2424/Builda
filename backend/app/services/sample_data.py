from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from app.schemas.build import BuildValidationResult
from app.schemas.chat import (
    AlternativeBuild,
    BuildComponent,
    ChatPlanResponse,
)
from app.schemas.product import PricePoint, Product


def generate_sample_plan() -> ChatPlanResponse:
    components: List[BuildComponent] = [
        BuildComponent(
            category="CPU",
            name="AMD Ryzen 7 7800X3D",
            price=2899.0,
            vendor="jd.com",
            url="https://www.example.com/products/cpu-7800x3d",
        ),
        BuildComponent(
            category="GPU",
            name="NVIDIA GeForce RTX 4070 SUPER",
            price=4599.0,
            vendor="bestbuy",
            url="https://www.example.com/products/gpu-4070-super",
        ),
        BuildComponent(
            category="主板",
            name="ASUS TUF GAMING B650M-PLUS WIFI",
            price=1299.0,
            vendor="amazon",
        ),
        BuildComponent(
            category="内存",
            name="Corsair Vengeance 32GB DDR5-6000",
            price=899.0,
            vendor="amazon",
        ),
        BuildComponent(
            category="固态硬盘",
            name="Samsung 990 PRO 2TB NVMe",
            price=1299.0,
            vendor="amazon",
        ),
        BuildComponent(
            category="电源",
            name="Seasonic Focus GX-750",
            price=899.0,
            vendor="newegg",
        ),
        BuildComponent(
            category="机箱",
            name="Lian Li Lancool 216",
            price=699.0,
            vendor="newegg",
        ),
    ]

    alternative = AlternativeBuild(
        title="性价比升级方案",
        description="将显卡升级为 RTX 4070 Ti SUPER，适合 4K 游戏和创作。",
        total_price=10999.0,
        components=[
            components[0],
            BuildComponent(
                category="GPU",
                name="NVIDIA GeForce RTX 4070 Ti SUPER",
                price=6299.0,
                vendor="bestbuy",
            ),
            *components[2:],
        ],
    )

    return ChatPlanResponse(
        plan_id="demo-plan-001",
        total_price=sum(component.price for component in components),
        currency="CNY",
        components=components,
        alternatives=[alternative],
        summary="针对 2K 高刷新率游戏与内容创作的均衡配置，兼顾性能与静音。",
        notes="价格基于最近 48 小时抓取数据，仅供参考。",
    )


def generate_sample_products() -> List[Product]:
    now = datetime.utcnow()
    return [
        Product(
            sku="cpu-7800x3d",
            name="AMD Ryzen 7 7800X3D",
            category="CPU",
            price=2899.0,
            vendor="jd.com",
            rating=4.9,
            stock_status="in_stock",
            specs={
                "cores": 8,
                "threads": 16,
                "base_clock": "4.2GHz",
                "boost_clock": "5.0GHz",
            },
            updated_at=now,
        ),
        Product(
            sku="gpu-4070s",
            name="NVIDIA RTX 4070 SUPER",
            category="GPU",
            price=4599.0,
            vendor="bestbuy",
            rating=4.7,
            stock_status="low_stock",
            specs={"vram": "12GB GDDR6X", "tdp": "220W"},
            updated_at=now - timedelta(hours=6),
        ),
    ]


def generate_price_history(sku: str) -> List[PricePoint]:
    base_time = datetime.utcnow()
    return [
        PricePoint(
            timestamp=base_time - timedelta(days=offset),
            price=4999.0 - offset * 120,
            vendor="bestbuy",
        )
        for offset in range(5)
    ]


def validate_build() -> BuildValidationResult:
    return BuildValidationResult(
        is_valid=True,
        issues=[],
        recommendations=[
            "建议选择 80PLUS 金牌或更高认证的 750W 电源以应对未来升级",
            "为 NVMe 固态添加散热片以保证长时间性能稳定",
        ],
    )
