# Extraction Notes

This scaffold is intentionally isolated from the main Synapse runtime.

Rules:
- no imports from `engine/`, `synapse_memory_browser/`, `event_stream/`, or `mentor_bridge/`
- integration with Synapse happens only through `adapters/synapse_adapter.py`
- storage is separate at `workspace_standalone/storage/workspace.db`
- disabling or deleting this scaffold does not change Synapse behavior

Validation order:
1. run in `WORKSPACE_ADAPTER_MODE=null`
2. validate sessions, imports, streaming, settings
3. switch to `WORKSPACE_ADAPTER_MODE=synapse`
4. validate HTTP integration without changing Synapse internals
