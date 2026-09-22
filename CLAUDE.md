# CLAUDE.md

Guidance for Claude Code working in this repository.

## Project Overview

Live workshop by Axel Sirota (Data Trainers LLC) for Nerdearla: **a multi-agent travel
concierge**. 60 minutes, demoed live, step by step, in front of an audience.

The deliverable is **one Jupyter notebook**, which is the whole artifact. No separate
exercise/solution notebook pair.

**`plans/DECISIONS.md` is the source of truth.** It holds Axel's decisions from the
interview. Read it before any work. Where this file and that file disagree, that file wins.

**Central thesis**, two things to kill in this order:

1. **"You need a framework to build an agent."** Killed by writing one in plain Python
   first: a class with a `while` loop, methods as tools, dispatching `tool_calls` by hand.
   Only then migrate to LangGraph, so the framework's value is felt, not asserted.
2. **"Just give one agent all the tools."** Killed by watching a 6-tool agent misroute
   live, then splitting it into one core capability per agent.

The organizing principle that replaces them: **API-led connectivity for agents.** One core
functionality, one agent, with its own tools.

**MCP is deliberately demoted.** It is not the spine. It arrives late, as a protocol for
reaching someone else's agent, and gets debunked as "just a tool protocol" by rebuilding
with MCP something we already built with plain tools.

## Language Rule (CRITICAL)

- **Notebook content is in fully Rioplatense Spanish with voseo** ("fijate", "armá", "vos",
  "acordate"), as Axel speaks. This covers every markdown cell, every code comment, every
  printed string, every exercise instruction.
- **Code identifiers stay in English** (`flight_agent`, `search_hotels`, `state`). Standard
  practice, and it keeps library calls readable.
- **Conversation with Axel is in English.** Plans, chat summaries, approval questions,
  commit messages: English.
- Never mix: a markdown cell is fully Spanish, never half-translated.

## Workshop Structure

The arc, 60 minutes total. Full detail in `plans/DECISIONS.md`.

| # | Beat | Format |
|---|---|---|
| 1 | Agent as a plain Python class: `while` loop, tools as methods, dispatch `tool_calls` by hand | Demo + mini exercise |
| 2 | The same agent migrated to LangGraph | Demo + mini exercise |
| 3 | `AgenteVuelosMuchasTools`: one agent, 6 tools, misroutes live | Demo |
| 4 | Split into two agents: flights, hotels. One capability each | Demo + mini exercise |
| 5 | Who owns the presentation to the user? Add a third agent: the supervisor | Demo + mini exercise |
| 6 | MCP: a partner's agent as a tool, then we build our own Serper MCP | Demo + diagram |
| 7 | "Maybe agents can figure out themselves what to do" → swarm, working | Demo + diagram |
| 8 | Solutions to all mini exercises | Section |

**Race condition: CUT.** See `plans/DECISIONS.md` for why.

Timing is tight, but **there is no cell budget**. Cell count is a poor proxy for a demo-led
notebook. The real constraint is minutes of narration: check it by reading the notebook aloud.

## Stack (installed and verified end to end 2026-09-21)

Exact versions are pinned in `requirements.txt`. Every import below was run locally, not
recalled from memory.

- **MCP server side**: `from mcp.server.mcpserver import MCPServer` (mcp 2.2.0).
  **NOT `FastMCP`.** In mcp 2.x `FastMCP` was renamed to `MCPServer` and moved out of
  `mcp.server.fastmcp`, which no longer exists. Importing the old path raises
  `ModuleNotFoundError` with a migration hint. Usage is otherwise familiar:
  `mcp = MCPServer("agente-vuelos")`, then `@mcp.tool()`, then `mcp.run()`.
- **MCP client side**: `from langchain.mcp import MCPAdapter` (langchain 1.4.2).
  **Do NOT use `langchain-mcp-adapters` or `MultiServerMCPClient`.** That standalone package
  is unmaintained; MCP support moved into LangChain under `langchain.mcp` and
  `MultiServerMCPClient` collapsed into the single `MCPAdapter` class.
  - `langchain.mcp` is in **beta** and emits `LangChainBetaWarning`. The API may shift before
    Wednesday, so re-verify imports the morning of the talk.
  - It requires the separate `fastmcp` package, which it uses for protocol negotiation.
  - **`MCPAdapter` takes a `Path`, not a string, for a local stdio server.** A plain string
    is rejected unless it is an http(s) URL, deliberately, so a model-supplied string cannot
    trigger local execution. Pass `Path("agente_vuelos.py")`. This is the single easiest
    thing to get wrong live.
  - `await adapter.list_tools()` returns async LangChain tools. Invoking one returns a list
    of content blocks: `[{'type': 'text', 'text': ..., 'id': ...}]`, not a bare string.
- **Supervisor mode**: `from langgraph_supervisor import create_supervisor` (0.0.31).
- **Swarm mode**: `from langgraph_swarm import create_swarm` (0.1.0). Both ship as separate
  maintained libraries, so the workshop picks each one deliberately.
- **Async**: the adapter is async throughout, so notebook cells calling it use `await`
  directly (Jupyter runs a live event loop) or `asyncio.run()` in a plain script.
- **Model**: `gpt-4o-mini`. Chosen because it is cheap enough to absorb a large room on
  Axel's key. NOTE: it is **not** a weak tool selector (AppSelectBench 0.603 vs gpt-4o's
  0.633), so Beat 3's failure comes from colliding tool descriptions, not model weakness.
- **OpenAI SDK**: `openai` 3.16.2. Beat 1 hand-rolls the tool loop against
  `chat.completions.create`, reading `tool_calls` off the response and dispatching manually.
- **Search**: serper.dev `/search` for both flights and hotels. Same wrapper both times.

## Environment

- **Colab.** Attendees run in Google Colab, so every dependency is `!pip install -q` in the
  notebook itself. No local setup, no Docker, no cloud accounts.
- **Keys via `getpass`** in the setup cell. REVERSED 2026-09-22: the `.env` approach needed
  attendees to upload a file, which is friction in Colab. `getpass` masks the input, so
  nothing shows on Axel's screen share or in the saved notebook.
  `client = OpenAI(api_key=OPENAI_API_KEY)` is explicit; the key also goes into
  `os.environ` because LangChain and LangGraph look there.
- **The MCP subprocess gets its key explicitly**, via
  `PythonStdioTransport(path, env={"SERPER_API_KEY": ...})`. It inherits only a short
  safe-list, so this is the only way in without a `.env` file. Verified working.
- **All keys are Axel's, cost absorbed**: OpenAI for the agents, serper.dev for search.
- **Data source**: serper.dev `/search` with `gl=ar, hl=es` for both flights and hotels.
  Returns `organic[]` with `title` + `snippet`. We wrap it to normalize the messy SERP into
  a clean shape. Verified working on Axel's key 2026-09-21.
  There is no Google Flights API; Google shut it down in 2018.
- **MCP transport**: stdio servers written to disk with `%%writefile`, then launched as
  subprocesses. This is the only pattern that works cleanly inside Colab.

## Notebook Conventions

- **One notebook**: `concierge_workshop.ipynb` at the repo root. It is the whole artifact.
- **Demo-led, not lab-led.** Axel demos and explains as he goes. Attendees take it home.
- **Therefore: heavy, high-quality comments.** Axel narrates from them live, and they carry
  the notebook for whoever runs it later without him.
- **CRITICAL: nothing blocks.** Every cell runs top to bottom as written. There are no
  `None  # TU CODIGO` placeholders in the main flow, because a blocked cell breaks the
  notebook for everyone who is only watching.
- **Mini exercises are additive**, in their own clearly marked cells, never in the path of
  the next cell.
- **Solutions collected at the end**, in their own section. Not inline.
- Built with the four-beat arc per concept: problem intro, diagram, full demo, then an
  optional mini exercise.
- Diagram placeholders use `<!-- DIAGRAM: ... -->` and link to `diagrams/<slug>.mmd`.
  11 diagrams are approved; placement and rules are in `plans/DECISIONS.md`.

## Editing Notebooks

Follow `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md` before any cell edit, insert, or delete.
Normalize cell ids, locate cells by id AND asserted content, read back after every edit,
run the structural and static gates. Blind index-based bulk rewrites are forbidden.

## Python

All Python runs through the virtualenv: `.venv/bin/python3`. All pip through
`.venv/bin/python3 -m pip`. Every installed package goes into `requirements.txt`.
The venv here is only for tooling (validators, nbformat); the notebook itself targets Colab.

## No AI Tells

Notebook markdown is student-facing copy. No em dashes, no en dashes, no bare `---`
separators inside cells, no Unicode multiplication sign. Short declarative sentences,
concrete nouns. Emojis in section headers are welcome; emoji bullets in body copy are not.

## Commands

`/init-workshop` has already been run. Its output is `plans/DECISIONS.md`, the source of
truth every other command reads first.

1. `/run-research-lab <N>` researches one beat and writes its cell-by-cell plan.
2. `/build-notebook <N>` builds that beat's cells, 5 at a time.
3. `/build-diagrams <N>` fills the diagram placeholders.
4. `/validate-notebooks` gates the result.

`/save-state`, `/start-session`, and `/resume` exist so a compacted context can pick the
build back up exactly where it stopped.
