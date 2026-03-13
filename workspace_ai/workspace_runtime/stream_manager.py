from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List


class StreamManager:
    def __init__(self, max_events: int = 500) -> None:
        self.events: Deque[Dict[str, Any]] = deque(maxlen=max(50, int(max_events)))

    def publish(self, *, event_type: str, session_id: str | None = None, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
        event = {"event_type": event_type, "session_id": session_id, "payload": payload or {}}
        self.events.append(event)
        return event

    def list_events(self, *, session_id: str | None = None, limit: int = 100) -> Dict[str, Any]:
        rows: List[Dict[str, Any]] = list(self.events)
        if session_id:
            rows = [row for row in rows if row.get("session_id") == session_id]
        rows = rows[-max(1, min(len(rows) or 1, int(limit))):]
        return {"session_id": session_id, "count": len(rows), "events": rows}
