# Vector

Persistent AI Workspace

Goals:
- no direct imports from Synapse runtime modules
- separate storage and settings
- optional HTTP adapter back into Synapse
- safe to iterate without destabilizing the main platform

This runtime now has its own:
- `workspace_standalone/.venv`
- `workspace_standalone/.runtime_logs`
- `workspace_standalone/scripts/*`

Install its environment:

```bash
./workspace_standalone/scripts/install.sh
```

Start it without Synapse:

```bash
export WORKSPACE_ADAPTER_MODE=null
./workspace_standalone/scripts/start.sh
```

Start it with Synapse as an external dependency:

```bash
export WORKSPACE_ADAPTER_MODE=synapse
export WORKSPACE_SYNAPSE_BASE_URL=http://127.0.0.1:8080
./workspace_standalone/scripts/start.sh
```

Stop it:

```bash
./workspace_standalone/scripts/stop.sh
```

Check status:

```bash
./workspace_standalone/scripts/status.sh
```

Terminal client:

```bash
source workspace_standalone/.venv/bin/activate
PYTHONPATH=/Users/briansifrar/SynapseWorkspaceStandalone python -m workspace_standalone.workspace_terminal.app create-session synapse --title "Test"
```
