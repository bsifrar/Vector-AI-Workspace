from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from workspace_standalone.adapters.base import MemoryAdapter
from workspace_standalone.workspace_import.chatgpt_models import ImportedChatConversation, ImportedChatMessage
from workspace_standalone.workspace_memory.session_store import SessionStore


class ChatGPTExportImporter:
    def __init__(self, *, store: SessionStore | None = None, adapter: MemoryAdapter | None = None) -> None:
        self.store = store or SessionStore()
        self.adapter = adapter

    @staticmethod
    def _iso_from_any(value: Any) -> str | None:
        if value is None or value == "":
            return None
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
        if isinstance(value, str):
            return value
        return None

    @staticmethod
    def _extract_content(message: Dict[str, Any]) -> str:
        content = message.get("content")
        if isinstance(content, dict) and isinstance(content.get("parts"), list):
            return "\n\n".join(str(part).strip() for part in content["parts"] if str(part).strip()).strip()
        if isinstance(content, str):
            return content.strip()
        return ""

    @staticmethod
    def _normalize_role(author: Any) -> str:
        if isinstance(author, dict):
            return str(author.get("role") or "assistant")
        if isinstance(author, str) and author:
            return author
        return "assistant"

    def _parse_conversation(self, raw: Dict[str, Any]) -> ImportedChatConversation | None:
        conv_id = str(raw.get("id") or raw.get("conversation_id") or "").strip()
        if not conv_id:
            return None
        messages: List[ImportedChatMessage] = []
        mapping = raw.get("mapping")
        if isinstance(mapping, dict):
            for node_id, node in mapping.items():
                if not isinstance(node, dict) or not isinstance(node.get("message"), dict):
                    continue
                message = node["message"]
                content = self._extract_content(message)
                if not content:
                    continue
                messages.append(
                    ImportedChatMessage(
                        role=self._normalize_role(message.get("author")),
                        content=content,
                        timestamp=self._iso_from_any(message.get("create_time") or node.get("create_time")),
                        external_message_id=str(message.get("id") or node_id),
                        metadata={},
                    )
                )
        messages.sort(key=lambda item: item.timestamp or "")
        if not messages:
            return None
        return ImportedChatConversation(
            external_conversation_id=conv_id,
            title=str(raw.get("title") or f"ChatGPT import {conv_id[:8]}").strip(),
            create_time=self._iso_from_any(raw.get("create_time")),
            update_time=self._iso_from_any(raw.get("update_time")),
            messages=messages,
        )

    def import_export(self, *, export_path: str, project_id: str, conversation_ids: List[str] | None = None, max_conversations: int = 25) -> Dict[str, Any]:
        path = Path(export_path).expanduser()
        if not path.exists():
            return {"status": "not_found", "export_path": str(path)}
        payload = json.loads(path.read_text(encoding="utf-8"))
        return self.import_export_payload(
            payload=payload,
            project_id=project_id,
            conversation_ids=conversation_ids,
            max_conversations=max_conversations,
            export_path=str(path),
        )

    def import_export_payload(
        self,
        *,
        payload: Any,
        project_id: str,
        conversation_ids: List[str] | None = None,
        max_conversations: int = 25,
        export_path: str = "",
    ) -> Dict[str, Any]:
        if not isinstance(payload, list):
            return {"status": "invalid", "reason": "expected conversations array"}
        selected = set(conversation_ids or [])
        max_items = int(max_conversations)
        imported = []
        for raw in payload:
            if not isinstance(raw, dict):
                continue
            conv_id = str(raw.get("id") or raw.get("conversation_id") or "")
            if selected and conv_id not in selected:
                continue
            parsed = self._parse_conversation(raw)
            if parsed is None:
                continue
            imported.append(self._import_conversation(project_id=project_id, conversation=parsed))
            if max_items > 0 and len(imported) >= max_items:
                break
        return {
            "status": "ok",
            "project_id": project_id,
            "export_path": export_path,
            "imported_count": len(imported),
            "conversations": imported,
        }

    def _import_conversation(self, *, project_id: str, conversation: ImportedChatConversation) -> Dict[str, Any]:
        session = self.store.create_session(
            project_id=project_id,
            title=conversation.title,
            mode="chat",
            source="chatgpt_export",
            external_conversation_id=conversation.external_conversation_id,
            external_title=conversation.title,
        )
        session_id = str(session["session_id"])
        for item in conversation.messages:
            metadata = {
                "external_source": "chatgpt_export",
                "external_conversation_id": conversation.external_conversation_id,
                "external_message_id": item.external_message_id,
            }
            self.store.add_message(session_id=session_id, role=item.role, content=item.content, provider="chatgpt_import", metadata=metadata)
            if self.adapter is not None:
                self.adapter.ingest_message(
                    project_id=project_id,
                    conversation_id=conversation.external_conversation_id,
                    role=item.role,
                    content=item.content,
                    timestamp=item.timestamp,
                    title=conversation.title,
                    metadata={"workspace_session_id": session_id, **metadata},
                )
        checkpoint = self.store.create_checkpoint(
            session_id=session_id,
            summary=f"Imported ChatGPT conversation '{conversation.title}' with {len(conversation.messages)} messages.",
            state={"external_conversation_id": conversation.external_conversation_id, "external_title": conversation.title},
        )
        return {"workspace_session_id": session_id, "external_conversation_id": conversation.external_conversation_id, "title": conversation.title, "checkpoint_id": checkpoint["checkpoint_id"], "message_count": len(conversation.messages)}
