# Concierge de Viajes Multiagente

Workshop materials for Nerdearla. One Jupyter notebook, 60 minutes, demoed live.

We build a travel concierge starting from an agent written in plain Python: a class with a
`while` loop and methods as tools. Then we migrate it to LangGraph, watch a single agent
with too many tools pick the wrong one, split it into one agent per capability, and add a
supervisor to own the answer. MCP shows up at the end, as what it actually is: a tool protocol.

## Contents

| Path | What |
|---|---|
| `concierge_workshop.ipynb` | The workshop notebook. Runs top to bottom, nothing to fill in. Mini-exercise solutions are in a section at the end |
| `plans/DECISIONS.md` | Source of truth: audience, arc, tone, diagrams (gitignored) |
| `plans/` | Research plans and Mermaid diagram sources (gitignored) |
| `reference/` | Verified working snippets for each lab's core mechanism |
| `validate_notebooks.py` | Notebook gates: syntax, placeholders, pair parity, deprecated imports |
| `.claude/commands/` | Slash commands that research, build and validate the notebook |

## Attendees

Open the notebook in Google Colab. Everything installs from the first cell. Axel shares a
`.env` file at the workshop with the keys already in it: drop it next to the notebook and
run. Every cell runs as written, so you can follow along or just watch.

Mini exercises are marked optional and never block anything. Their solutions are in a
section at the end, for whenever you go deeper at home.

## Local setup (for building the workshop, not for attendees)

```bash
python -m venv .venv
.venv/bin/python3 -m pip install -r requirements.txt
```

Python 3.12.12 via asdf, pinned in `.tool-versions`.

## Build workflow

```
/init-workshop        # one-time: writes plans/DECISIONS.md
/run-research-lab N   # 5-cycle research, writes plans/lab_N_<slug>.md
/build-notebook N     # adds that lab's cells, 5 at a time, with approval
/build-diagrams N     # fills the diagram placeholders
/validate-notebooks   # gates before the talk
```

## Stack

Verified end to end on 2026-09-21. Exact versions in `requirements.txt`.

| Piece | Import |
|---|---|
| MCP server | `from mcp.server.mcpserver import MCPServer` |
| MCP client | `from langchain.mcp import MCPAdapter` |
| Supervisor | `from langgraph_supervisor import create_supervisor` |
| Swarm | `from langgraph_swarm import create_swarm` |

Two traps worth knowing, both verified by running them:

- `mcp` 2.x renamed `FastMCP` to `MCPServer`. `mcp.server.fastmcp` no longer exists.
- `MCPAdapter` rejects a plain string for a local server. Pass a `Path`. A string is only
  accepted when it is an http(s) URL, so that a model-supplied string cannot trigger local
  execution.

`langchain.mcp` is in beta and emits `LangChainBetaWarning`. Re-verify imports before the talk.
