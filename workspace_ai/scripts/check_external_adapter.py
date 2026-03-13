from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workspace_ai.adapters.external_adapter import ExternalAdapter
from workspace_ai.app.settings import get_settings


def main() -> int:
    settings = get_settings()
    adapter = ExternalAdapter(settings.external_base_url)
    payload = {
        "health": adapter.health(),
        "context_preview_sample": adapter.build_context_preview(
            project_id="external",
            prompt="Summarize current project context.",
            token_budget=512,
            top_k=4,
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
