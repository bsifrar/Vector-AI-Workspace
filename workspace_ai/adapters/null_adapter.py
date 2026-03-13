from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


class NullAdapter:
    def health(self) -> Dict[str, Any]:
        return {
            "status": "ok",
            "adapter_mode": "null",
            "synapse_connected": False,
        }

    def build_context_preview(
        self,
        *,
        project_id: str,
        prompt: str,
        token_budget: int = 1800,
        top_k: int = 8,
        conversation_id: str | None = None,
    ) -> Dict[str, Any]:
        return {
            "status": "ok",
            "project_id": project_id,
            "prompt": prompt,
            "context_items": [],
            "context_item_count": 0,
            "retrieved_count": 0,
            "knowledge_count": 0,
            "token_budget": token_budget,
            "summary": "",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "adapter_mode": "null",
        }

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
        return {
            "status": "ok",
            "adapter_mode": "null",
            "project_id": project_id,
            "conversation_id": conversation_id,
            "role": role,
        }
