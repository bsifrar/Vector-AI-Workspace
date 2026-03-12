from __future__ import annotations

import json
from typing import Any, Dict
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class SynapseAdapter:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str) -> Dict[str, Any]:
        request = Request(f"{self.base_url}{path}", method="GET")
        try:
            with urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return {"status": "error", "code": exc.code, "detail": exc.read().decode("utf-8", errors="replace")}
        except URLError as exc:
            return {"status": "error", "detail": str(exc)}

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        request = Request(
            f"{self.base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return {"status": "error", "code": exc.code, "detail": exc.read().decode("utf-8", errors="replace")}
        except URLError as exc:
            return {"status": "error", "detail": str(exc)}

    def health(self) -> Dict[str, Any]:
        root = self._get("/")
        smb = self._get("/smb/status")
        return {
            "status": "ok" if root.get("SynapseLabPro") and smb.get("status") == "ok" else "degraded",
            "adapter_mode": "synapse",
            "synapse_base_url": self.base_url,
            "root": root,
            "smb": smb,
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
        return self._post(
            "/smb/context/preview",
            {
                "project_id": project_id,
                "prompt": prompt,
                "token_budget": token_budget,
                "top_k": top_k,
                "conversation_id": conversation_id,
            },
        )

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
        return self._post(
            "/smb/conversations/ingest",
            {
                "project_id": project_id,
                "conversation_id": conversation_id,
                "platform": "workspace_standalone",
                "role": role,
                "content": content,
                "timestamp": timestamp,
                "capture_source": "workspace_standalone",
                "title": title,
                "metadata": metadata or {},
            },
        )
