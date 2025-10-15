from __future__ import annotations

from typing import List

from .crawlers import CanadaComputersCrawler, NeweggCrawler
from .crawlers.base import CrawlerResult
from .vector_store import SimpleVectorStore, get_vector_store


class DataPipeline:
    """Coordinate crawling and ingestion into the vector store."""

    def __init__(self, store: SimpleVectorStore | None = None) -> None:
        self.store = store or get_vector_store()
        self.crawlers = [NeweggCrawler(), CanadaComputersCrawler()]

    async def refresh_samples(self) -> List[CrawlerResult]:
        results: List[CrawlerResult] = []
        for crawler in self.crawlers:
            results.extend(await crawler.fetch_latest())
        for result in results:
            self.store.upsert(result.to_metadata())
        self.store.persist()
        return results


def get_pipeline() -> DataPipeline:
    return DataPipeline()
