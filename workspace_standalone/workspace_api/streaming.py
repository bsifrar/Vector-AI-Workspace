from __future__ import annotations

import json
from typing import Dict, Iterable


def encode_sse_stream(events: Iterable[Dict[str, object]]) -> Iterable[str]:
    for event in events:
        yield f"data: {json.dumps(event, sort_keys=True)}\n\n"
