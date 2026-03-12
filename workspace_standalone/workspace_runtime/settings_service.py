from __future__ import annotations

from typing import Any, Dict

from workspace_standalone.app.settings import get_settings
from workspace_standalone.workspace_memory.session_store import SessionStore


class SettingsService:
    def __init__(self, store: SessionStore | None = None) -> None:
        self.store = store or SessionStore()

    def defaults(self) -> Dict[str, Any]:
        settings = get_settings()
        return {
            "api_enabled": bool(settings.openai_api_key),
            "selected_model": settings.default_model,
            "daily_spend_cap_usd": 5.0,
            "hourly_call_cap": 50,
            "price_input_per_1m_usd": 0.0,
            "price_output_per_1m_usd": 0.0,
        }

    def api_key(self) -> str:
        stored = self.store.list_settings().get("api_key", "")
        if isinstance(stored, str) and stored.strip():
            return stored.strip()
        return get_settings().openai_api_key

    def get(self) -> Dict[str, Any]:
        payload = self.defaults()
        payload.update(self.store.list_settings())
        payload.pop("api_key", None)
        payload["api_key_configured"] = bool(self.api_key())
        payload["usage"] = self.store.api_usage_summary()
        payload["remaining_daily_budget_usd"] = max(0.0, round(float(payload["daily_spend_cap_usd"]) - float(payload["usage"]["spent_today_usd"]), 6))
        payload["remaining_hourly_calls"] = max(0, int(payload["hourly_call_cap"]) - int(payload["usage"]["calls_this_hour"]))
        return payload

    def update(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in updates.items():
            if value is not None:
                self.store.set_setting(key=key, value=value)
        return self.get()
