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
            price=429.0,
            vendor="amazon",
            url="https://www.example.com/products/cpu-7800x3d",
            image_url="https://images.builda.dev/amd-ryzen-7-7800x3d.jpg",
        ),
        BuildComponent(
            category="GPU",
            name="NVIDIA GeForce RTX 4070 SUPER",
            price=599.0,
            vendor="bestbuy",
            url="https://www.example.com/products/gpu-4070-super",
            image_url="https://images.builda.dev/nvidia-rtx-4070-super.jpg",
        ),
        BuildComponent(
            category="Motherboard",
            name="ASUS TUF GAMING B650M-PLUS WIFI",
            price=229.0,
            vendor="amazon",
            image_url="https://images.builda.dev/asus-b650m-plus.jpg",
        ),
        BuildComponent(
            category="Memory",
            name="Corsair Vengeance 32GB DDR5-6000",
            price=124.0,
            vendor="amazon",
            image_url="https://images.builda.dev/corsair-vengeance-ddr5-6000.jpg",
        ),
        BuildComponent(
            category="SSD",
            name="Samsung 990 PRO 2TB NVMe",
            price=169.0,
            vendor="amazon",
            image_url="https://images.builda.dev/samsung-990-pro-2tb.jpg",
        ),
        BuildComponent(
            category="Power Supply",
            name="Seasonic Focus GX-750",
            price=129.0,
            vendor="newegg",
            image_url="https://images.builda.dev/seasonic-focus-gx-750.jpg",
        ),
        BuildComponent(
            category="Case",
            name="Lian Li Lancool 216",
            price=109.0,
            vendor="newegg",
            image_url="https://images.builda.dev/lian-li-lancool-216.jpg",
        ),
    ]

    alternative = AlternativeBuild(
        title="Value Upgrade Plan",
        description="Upgrade the GPU to RTX 4070 Ti SUPER, suitable for 4K gaming and creation.",
        total_price=1988.0,
        components=[
            components[0],
            BuildComponent(
                category="GPU",
                name="NVIDIA GeForce RTX 4070 Ti SUPER",
                price=799.0,
                vendor="bestbuy",
                image_url="https://images.builda.dev/nvidia-rtx-4070-ti-super.jpg",
            ),
            *components[2:],
        ],
    )

    return ChatPlanResponse(
        plan_id="demo-plan-001",
        total_price=sum(component.price for component in components),
        currency="USD",
        components=components,
        alternatives=[alternative],
        summary="A balanced configuration for 2K high-refresh gaming and content creation, balancing performance and acoustics.",
        notes="Prices are based on recent sample data and should be validated against live retailer listings.",
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
            "Choose an 80PLUS Gold or higher 750W PSU to handle future upgrades",
            "Add a heatsink for the NVMe SSD to ensure sustained performance",
        ],
    )
