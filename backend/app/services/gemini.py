from __future__ import annotations

import asyncio
import json
import logging
import re
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import ValidationError

try:  # pragma: no cover - optional dependency during local development
    import google.generativeai as genai
    from google.api_core.exceptions import GoogleAPIError
except ModuleNotFoundError:  # pragma: no cover - fallback when SDK is absent
    genai = None  # type: ignore[assignment]

    class GoogleAPIError(Exception):  # type: ignore[override]
        pass

from app.schemas.chat import (
    AlternativeBuild,
    BuildComponent,
    ChatPlanRequest,
    ChatPlanResponse,
)

LOGGER = logging.getLogger(__name__)


class GeminiPlannerError(Exception):
    """Raised when Gemini plan generation fails."""


class GeminiPlanner:
    """Generate build plans by orchestrating a Gemini model."""

    def __init__(self, api_key: Optional[str], model: str = "gemini-1.5-pro-latest") -> None:
        self._api_key = api_key
        self._model_name = model
        self._model: Optional[Any] = None

        if api_key and genai is not None:
            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(model)
        elif api_key:
            LOGGER.warning("Gemini API key provided but google-generativeai is not installed.")

    @property
    def available(self) -> bool:
        return self._model is not None

    async def generate_plan(self, request: ChatPlanRequest) -> ChatPlanResponse:
        if not self.available:
            raise GeminiPlannerError("Gemini API key is not configured.")

        prompt = self._build_prompt(request)
        try:
            response = await asyncio.to_thread(self._model.generate_content, prompt)  # type: ignore[arg-type]
        except GoogleAPIError as exc:  # pragma: no cover - network errors handled at runtime
            LOGGER.error("Gemini API error: %s", exc)
            raise GeminiPlannerError("Gemini API call failed.") from exc

        text = self._extract_text(response)
        plan_dict = self._extract_json(text)
        return self._parse_plan(plan_dict, request.currency)

    def _build_prompt(self, request: ChatPlanRequest) -> str:
        conversation = []
        for message in request.messages:
            speaker = "User" if message.role == "user" else "Assistant"
            conversation.append(f"{speaker}: {message.content.strip()}")
        conversation_text = "\n".join(conversation)

        instructions = (
            "You are Builda, a senior PC build consultant."
            " Produce a balanced configuration that matches the intent, budget, and scenario"
            " described by the user. Use only publicly available component data."
            " Respond strictly in JSON without code fences."
        )

        schema = {
            "plan_id": "string",
            "currency": request.currency,
            "total_price": "number",
            "summary": "string",
            "notes": "string",
            "components": [
                {
                    "category": "string",
                    "name": "string",
                    "price": "number",
                    "vendor": "string",
                    "url": "string",
                }
            ],
            "alternatives": [
                {
                    "title": "string",
                    "description": "string",
                    "total_price": "number",
                    "components": "same schema as components",
                }
            ],
        }

        return (
            f"{instructions}\n\n"
            f"Conversation history:\n{conversation_text}\n\n"
            f"Output JSON schema (fill with actual data, omit unused optional fields):\n{json.dumps(schema)}"
        )

    def _extract_text(self, response: Any) -> str:
        if hasattr(response, "text"):
            return response.text  # type: ignore[return-value]
        if hasattr(response, "candidates"):
            texts = []
            for candidate in response.candidates:  # pragma: no cover - depends on library internals
                for part in getattr(candidate, "content", []) or []:
                    texts.append(getattr(part, "text", ""))
            return "\n".join(texts)
        raise GeminiPlannerError("Gemini response did not contain text output.")

    def _extract_json(self, text: str) -> Dict[str, Any]:
        candidate = text.strip()
        if not candidate:
            raise GeminiPlannerError("Gemini returned an empty response.")

        if candidate.startswith("```"):
            candidate = candidate.strip("`").strip()

        match = re.search(r"\{.*\}", candidate, re.DOTALL)
        if not match:
            raise GeminiPlannerError("Could not locate JSON payload in Gemini response.")

        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as exc:
            LOGGER.error("Failed to decode Gemini JSON: %s", candidate)
            raise GeminiPlannerError("Gemini returned malformed JSON.") from exc

    def _parse_plan(self, payload: Dict[str, Any], currency: str) -> ChatPlanResponse:
        try:
            components = [self._parse_component(item) for item in payload.get("components", [])]
            alternatives = [self._parse_alternative(item) for item in payload.get("alternatives", [])]

            plan_id = payload.get("plan_id") or f"gemini-plan-{uuid4().hex[:8]}"
            total_price = float(payload.get("total_price", 0.0))
            summary = payload.get("summary") or "Gemini plan summary"
            notes = payload.get("notes")
        except (TypeError, ValueError) as exc:
            raise GeminiPlannerError("Gemini response missing required fields.") from exc

        try:
            return ChatPlanResponse(
                plan_id=plan_id,
                total_price=total_price,
                currency=payload.get("currency", currency),
                components=components,
                alternatives=alternatives,
                summary=summary,
                notes=notes,
            )
        except ValidationError as exc:
            raise GeminiPlannerError("Gemini response failed validation.") from exc

    def _parse_component(self, raw: Dict[str, Any]) -> BuildComponent:
        return BuildComponent(
            category=raw.get("category", "Unknown"),
            name=raw.get("name", "Unnamed Component"),
            price=float(raw.get("price", 0.0)),
            vendor=raw.get("vendor", "unknown"),
            url=raw.get("url"),
        )

    def _parse_alternative(self, raw: Dict[str, Any]) -> AlternativeBuild:
        components = [self._parse_component(item) for item in raw.get("components", [])]
        return AlternativeBuild(
            title=raw.get("title", "Alternative Option"),
            description=raw.get("description", "Alternative configuration"),
            total_price=float(raw.get("total_price", 0.0)),
            components=components,
        )


def get_gemini_planner(api_key: Optional[str]) -> GeminiPlanner:
    return GeminiPlanner(api_key=api_key)
