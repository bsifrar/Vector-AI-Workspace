from __future__ import annotations

from typing import Any, Dict

from workspace_ai.adapters.base import MemoryAdapter
from workspace_ai.workspace_memory.session_store import SessionStore


class ContextService:
    def __init__(self, *, adapter: MemoryAdapter, store: SessionStore | None = None) -> None:
        self.adapter = adapter
        self.store = store or SessionStore()

    def build_context(self, *, project_id: str, prompt: str, session_id: str | None = None, token_budget: int = 1800, top_k: int = 8) -> Dict[str, Any]:
        recent_messages = self.store.list_messages(session_id=session_id, limit=12) if session_id else []
        checkpoints = self.store.list_checkpoints(session_id=session_id, limit=3) if session_id else []
        preview = self.adapter.build_context_preview(project_id=project_id, prompt=prompt, token_budget=token_budget, top_k=top_k)
        return {
            "status": "ok",
            "project_id": project_id,
            "session_id": session_id,
            "prompt": prompt,
            "recent_messages": recent_messages,
            "checkpoints": checkpoints,
            "memory_context": preview,
        }

    def adapter_health(self) -> Dict[str, Any]:
        return self.adapter.health()
