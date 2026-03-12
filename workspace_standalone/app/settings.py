from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StandaloneSettings:
    host: str
    port: int
    storage_path: Path
    synapse_base_url: str
    adapter_mode: str
    openai_api_key: str
    default_model: str


def get_settings() -> StandaloneSettings:
    root = Path(__file__).resolve().parents[1]
    return StandaloneSettings(
        host=os.getenv("WORKSPACE_HOST", "127.0.0.1"),
        port=int(os.getenv("WORKSPACE_PORT", "8091")),
        storage_path=Path(
            os.getenv("WORKSPACE_STORAGE_PATH", str(root / "storage" / "workspace.db"))
        ).expanduser().resolve(),
        synapse_base_url=os.getenv("WORKSPACE_SYNAPSE_BASE_URL", "http://127.0.0.1:8080"),
        adapter_mode=os.getenv("WORKSPACE_ADAPTER_MODE", "null").strip().lower(),
        openai_api_key=os.getenv("WORKSPACE_OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", "")),
        default_model=os.getenv("WORKSPACE_MODEL", os.getenv("SYNAPSE_WORKSPACE_OPENAI_MODEL", os.getenv("OPENAI_MODEL", "gpt-5.4"))),
    )
