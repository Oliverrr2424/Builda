from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List

from .base import CrawlerResult

_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "sample_products.json"


class CanadaComputersCrawler:
    """Load a deterministic sample payload for Canada Computers products."""

    vendor = "canadacomputers"

    async def fetch_latest(self) -> List[CrawlerResult]:
        payloads = self._load_sample()
        return [self._to_result(item) for item in payloads if item.get("vendor") == self.vendor]

    def _load_sample(self) -> List[dict]:
        if not _DATA_PATH.exists():
            return []
        import json

        with _DATA_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _to_result(self, item: dict) -> CrawlerResult:
        updated_at = item.get("updated_at", datetime.utcnow().isoformat())
        return CrawlerResult(
            sku=item["sku"],
            name=item["name"],
            category=item["category"],
            price=float(item["price"]),
            currency=item.get("currency", "CAD"),
            vendor=item.get("vendor", self.vendor),
            rating=item.get("rating"),
            stock_status=item.get("stock_status"),
            specs=item.get("specs", {}),
            url=item.get("url"),
            updated_at=datetime.fromisoformat(updated_at.replace("Z", "+00:00")),
        )
