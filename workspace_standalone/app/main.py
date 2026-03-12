from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

from workspace_standalone.adapters.null_adapter import NullAdapter
from workspace_standalone.adapters.synapse_adapter import SynapseAdapter
from workspace_standalone.app.settings import get_settings
from workspace_standalone.workspace_api.router import build_router
from workspace_standalone.workspace_runtime.session_manager import SessionManager


def build_app() -> FastAPI:
    settings = get_settings()
    adapter = SynapseAdapter(settings.synapse_base_url) if settings.adapter_mode == "synapse" else NullAdapter()
    manager = SessionManager(adapter=adapter)
    app = FastAPI(title="Vector", version="0.1.0")
    app.include_router(build_router(manager))

    @app.get("/", response_class=HTMLResponse)
    def root() -> str:
        return (Path(__file__).resolve().parents[1] / "ui" / "index.html").read_text(encoding="utf-8")

    @app.get("/health")
    def health() -> dict:
        return {"service": "vector", "tagline": "Persistent AI Workspace", "adapter_mode": settings.adapter_mode}

    @app.get("/ui", response_class=HTMLResponse)
    def ui() -> str:
        return (Path(__file__).resolve().parents[1] / "ui" / "index.html").read_text(encoding="utf-8")

    return app


app = build_app()


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("workspace_standalone.app.main:app", host=settings.host, port=settings.port, reload=False)
