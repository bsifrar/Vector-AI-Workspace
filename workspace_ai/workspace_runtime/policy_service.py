from __future__ import annotations

from typing import Any, Dict

from workspace_ai.workspace_memory.session_store import SessionStore
from workspace_ai.workspace_runtime.settings_service import SettingsService


class PolicyService:
    def __init__(self, store: SessionStore | None = None, settings_service: SettingsService | None = None) -> None:
        self.store = store or SessionStore()
        self.settings_service = settings_service or SettingsService(store=self.store)

    def allow_live_call(self) -> Dict[str, Any]:
        settings = self.settings_service.get()
        if not bool(settings.get("api_enabled")):
            return {"allowed": False, "reason": "api_disabled", "settings": settings}
        if not bool(settings.get("api_key_configured")):
            return {"allowed": False, "reason": "api_key_missing", "settings": settings}
        if int(settings["usage"]["calls_this_hour"]) >= int(settings["hourly_call_cap"]):
            return {"allowed": False, "reason": "hourly_call_cap_exceeded", "settings": settings}
        if float(settings["usage"]["spent_today_usd"]) >= float(settings["daily_spend_cap_usd"]):
            return {"allowed": False, "reason": "daily_spend_cap_exceeded", "settings": settings}
        return {"allowed": True, "reason": "ok", "settings": settings}

    def estimate_cost_usd(self, *, input_tokens: int, output_tokens: int, settings: Dict[str, Any]) -> float:
        return round(
            ((int(input_tokens) / 1_000_000.0) * float(settings.get("price_input_per_1m_usd", 0.0)))
            + ((int(output_tokens) / 1_000_000.0) * float(settings.get("price_output_per_1m_usd", 0.0))),
            8,
        )

    def record_live_call(self, *, session_id: str, provider: str, model: str, mode: str, usage: Dict[str, Any]) -> Dict[str, Any]:
        settings = self.settings_service.get()
        input_tokens = int(usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0)
        output_tokens = int(usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0)
        return self.store.record_api_call(
            session_id=session_id,
            provider=provider,
            model=model,
            mode=mode,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost_usd=self.estimate_cost_usd(input_tokens=input_tokens, output_tokens=output_tokens, settings=settings),
        )
