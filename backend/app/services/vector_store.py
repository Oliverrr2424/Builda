from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

LOGGER = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
_STORE_PATH = _DATA_DIR / "vector_store.json"
_SAMPLE_PATH = _DATA_DIR / "sample_products.json"


@dataclass
class VectorRecord:
    identifier: str
    embedding: List[float]
    metadata: Dict[str, Any]


class HashingVectorizer:
    def __init__(self, dimensions: int = 256) -> None:
        self.dimensions = dimensions

    def embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        tokens = re.findall(r"[\w-]+", text.lower())
        for token in tokens:
            index = hash(token) % self.dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]
        return vector


class SimpleVectorStore:
    def __init__(self, path: Path = _STORE_PATH, dimensions: int = 256) -> None:
        self.path = path
        self.vectorizer = HashingVectorizer(dimensions=dimensions)
        self.records: List[VectorRecord] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.records = []
            return
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive
            LOGGER.error("Failed to load vector store: %s", exc)
            payload = []
        self.records = [
            VectorRecord(
                identifier=item["identifier"],
                embedding=item["embedding"],
                metadata=item["metadata"],
            )
            for item in payload
        ]

    def persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            json.dump(
                [
                    {
                        "identifier": record.identifier,
                        "embedding": record.embedding,
                        "metadata": record.metadata,
                    }
                    for record in self.records
                ],
                handle,
                ensure_ascii=False,
                indent=2,
            )

    def is_empty(self) -> bool:
        return not self.records

    def upsert(self, metadata: Dict[str, Any]) -> None:
        identifier = metadata["sku"]
        embedding = self.vectorizer.embed(self._build_corpus(metadata))
        payload = VectorRecord(identifier=identifier, embedding=embedding, metadata=metadata)

        for index, record in enumerate(self.records):
            if record.identifier == identifier:
                self.records[index] = payload
                break
        else:
            self.records.append(payload)

    def _build_corpus(self, metadata: Dict[str, Any]) -> str:
        specs = metadata.get("specs", {})
        specs_parts: Iterable[str] = []
        if isinstance(specs, dict):
            specs_parts = [f"{key} {value}" for key, value in specs.items()]
        elif isinstance(specs, list):
            specs_parts = [str(item) for item in specs]
        return " ".join(
            [
                metadata.get("name", ""),
                metadata.get("category", ""),
                " ".join(specs_parts),
            ]
        )

    def search(
        self,
        query: Optional[str],
        *,
        top_k: int = 10,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        if not self.records:
            return []

        if query:
            query_vector = self.vectorizer.embed(query)
        else:
            uniform_value = 1.0 / math.sqrt(self.vectorizer.dimensions)
            query_vector = [uniform_value] * self.vectorizer.dimensions

        scored: List[tuple[float, VectorRecord]] = []
        for record in self.records:
            score = sum(q * v for q, v in zip(query_vector, record.embedding))
            scored.append((float(score), record))
        scored.sort(key=lambda item: item[0], reverse=True)

        results: List[Dict[str, Any]] = []
        requested_tags = set(tag.lower() for tag in (tags or []))

        for score, record in scored:
            if len(results) >= top_k:
                break
            metadata = record.metadata
            if category and metadata.get("category", "").lower() != category.lower():
                continue
            price = float(metadata.get("price", 0))
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            if requested_tags:
                product_tags = set(
                    str(tag).lower()
                    for tag in metadata.get("specs", {}).get("scene_tags", [])
                )
                if not requested_tags.issubset(product_tags):
                    continue
            enriched = metadata.copy()
            enriched["similarity"] = score
            results.append(enriched)

        return results

    def all(self) -> List[Dict[str, Any]]:
        return [record.metadata.copy() for record in self.records]


def _load_samples() -> List[Dict[str, Any]]:
    if not _SAMPLE_PATH.exists():
        return []
    with _SAMPLE_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


_store_instance: Optional[SimpleVectorStore] = None


def get_vector_store() -> SimpleVectorStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = SimpleVectorStore(path=_STORE_PATH)
        if _store_instance.is_empty():
            for item in _load_samples():
                _store_instance.upsert(item)
            _store_instance.persist()
    return _store_instance
