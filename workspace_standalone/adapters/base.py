from __future__ import annotations

from typing import Any, Dict, Protocol


class MemoryAdapter(Protocol):
    def health(self) -> Dict[str, Any]:
        ...

    def build_context_preview(
        self,
        *,
        project_id: str,
        prompt: str,
        token_budget: int = 1800,
        top_k: int = 8,
        conversation_id: str | None = None,
    ) -> Dict[str, Any]:
        ...

    def ingest_message(
        self,
        *,
        project_id: str,
        conversation_id: str,
        role: str,
        content: str,
        timestamp: str | None = None,
        title: str = "",
        metadata: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        ...
