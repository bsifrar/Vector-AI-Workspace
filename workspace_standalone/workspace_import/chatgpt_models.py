from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ImportedChatMessage:
    role: str
    content: str
    timestamp: str | None
    external_message_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImportedChatConversation:
    external_conversation_id: str
    title: str
    create_time: str | None
    update_time: str | None
    messages: List[ImportedChatMessage]
    metadata: Dict[str, Any] = field(default_factory=dict)
