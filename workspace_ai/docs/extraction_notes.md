# Extraction Notes

This scaffold is intentionally isolated from the main external runtime.

Key rules:
- no direct imports from any external application codebase
- integration with an external memory service happens only through `adapters/external_adapter.py`
- storage is separate at `workspace_ai/storage/workspace.db`
- disabling or deleting this scaffold does not change any external runtime behavior

Safe extraction sequence:
1. copy the scaffold out
2. replace direct integrations with adapters
3. verify local-only mode
4. validate HTTP integration without changing external internals
