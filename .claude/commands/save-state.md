---
description: Snapshot workshop state to progress.txt so a new session can resume exactly where the build stopped
---

# /save-state

Snapshot the current session into `progress.txt` so a brand-new conversation can resume
with zero context loss.

---

## What This Produces

A single file: `progress.txt` (repo root, gitignored).

The file is written so that `/resume` can read it and immediately understand:
- What was built, in what order, and what state each artifact is in
- What was decided (locked decisions)
- Exactly what to do next, with the specific command to run
- Which files to read for full detail

---

## Process

### Step 1: Read all state sources (one at a time, never batched)

Read these files:
- `plans/LABS.md` - lab status and manifest checkboxes
- `TODOS.md` - open issues (if exists)
- `plans/DECISIONS.md` - locked decisions

Also run:
```bash
ls -la concierge_workshop.ipynb 2>/dev/null
ls plans/lab_*.md diagrams/*.mmd 2>/dev/null
```

And capture the notebook's section map and cell count:
```bash
.venv/bin/python3 -c "
import json
nb = json.load(open('concierge_workshop.ipynb'))
print('total cells:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    if c['cell_type'] == 'markdown' and src.lstrip().startswith('#'):
        print(i, src.splitlines()[0][:70])
" 2>/dev/null
```

### Step 2: Derive status for every lab

For each lab 0-5, determine:

| Signal | Status label |
|--------|-------------|
| No plan, no cells in the notebook | `not_started` |
| Plan exists, no cells built | `plan_only` |
| Both built, pair check passes | `done` |
| Both built, pair check fails or open TODOS | `needs_fix` |

Run validation on the one notebook:
```bash
.venv/bin/python3 validate_notebooks.py concierge_workshop.ipynb --type exercise
```

### Step 3: Identify the single next action

Scan the lab list in order (0 -> 5). The first lab that is not `done` determines
the next action. Map it:

| Status | Next action |
|--------|-------------|
| `not_started` | `/run-research-lab N` |
| `plan_only` | `/build-notebook N` |
| `needs_fix` | Describe the specific issue and fix it |

If all labs are `done`: next action is `/build-diagrams` for any diagram still a
placeholder, then a full run-through of the notebook in Colab.

### Step 4: Write progress.txt

Write to `progress.txt` in the repo root. Use this exact structure:

```
WORKSHOP: Concierge de Viajes Multiagente - Nerdearla
SAVED: <YYYY-MM-DD HH:MM>
REPO: /Users/axelsirota/repos/nerdearla_concierge_agent

==============================================================================
NOTEBOOK
==============================================================================

concierge_workshop.ipynb            <N> cells

==============================================================================
LAB STATUS
==============================================================================

[done]         Lab 0 - El caso: por que un agente no alcanza
               cells:    0-8 in concierge_workshop.ipynb
               plan:     plans/lab_0_el-caso.md
               diagrams: un-agente-ahogado.mmd

[plan_only]    Lab 2 - AgenteHoteles en otro framework
               plan:     plans/lab_2_agente-hoteles.md
               next:     /build-notebook 2

[not_started]  Lab 3 - Modo supervisor
               next:     /run-research-lab 3

... (one line per lab, 0-5)

==============================================================================
KNOWN ISSUES / OPEN TODOS
==============================================================================

<contents of TODOS.md open entries, or "none" if all resolved>

==============================================================================
LOCKED DECISIONS (do not re-litigate without Axel)
==============================================================================

- Notebook content in Spanish. Code identifiers in English. Chat with Axel in English.
- ONE notebook for the whole workshop, not one per lab.
- MCP client: MCPAdapter from langchain.mcp. NOT langchain-mcp-adapters, NOT
  MultiServerMCPClient. That package is unmaintained.
- MCP server: MCPServer from mcp.server.mcpserver (NOT FastMCP, renamed in mcp 2.x),
  stdio, via %%writefile plus subprocess.
- MCPAdapter takes a Path for a local server, never a plain string.
- Lab 1 agent is plain Python. Lab 2 agent is LangGraph. Same client call for both.
- Supervisor: langgraph-supervisor. Swarm: langgraph-swarm.
- Race condition: CUT from the workshop. See plans/DECISIONS.md.
- Environment is Colab only. No cloud accounts, no Docker, no local installs.
- No safety-net cells. They are obsolete because nothing blocks.
- API keys from a shared .env via python-dotenv, distributed at the workshop. NOT getpass.
- Demo-led. NOTHING BLOCKS: every cell runs as written, no fill-in placeholders.
- Always verify cell_id with python snippet before every NotebookEdit.

==============================================================================
KEY FILES
==============================================================================

CLAUDE.md                                 - language rule, stack, agenda
plans/DECISIONS.md  - all workshop decisions
plans/LABS.md                             - lab status manifest
TODOS.md                                  - open issues
.claude/commands/                         - all slash commands
concierge_workshop.ipynb                  - the workshop notebook
solutions/                                - completed notebook
plans/lab_N_slug.md                       - cell-by-cell plan for each lab
diagrams/*.mmd                      - Mermaid diagram sources

==============================================================================
NEXT ACTION
==============================================================================

<ONE specific command or action to run next>
Reason: <one sentence why this is the next step>

==============================================================================
HOW TO RESUME
==============================================================================

1. Open this repo: /Users/axelsirota/repos/nerdearla_concierge_agent
2. Run: /resume
   The /resume command reads this file and tells you exactly where to pick up.
3. If /resume is not available, read this file directly and run the NEXT ACTION above.
```

### Step 5: Add progress.txt to .gitignore if not already there

```bash
grep -q "progress.txt" .gitignore 2>/dev/null || echo "progress.txt" >> .gitignore
```

### Step 6: Confirm

Print to chat:

```
progress.txt written.

Quick summary:
  notebook:     <N> cells
  done:         labs 0-1
  plan_only:    lab 2
  not_started:  labs 3-5

Next action: /build-notebook 2

Run /resume in any future session to reload this context.
```

---

## Non-Negotiables

- Write actual file paths, not placeholders - every path in progress.txt must be real
- NEXT ACTION must be a single runnable command, not a vague description
- Do not omit any lab from the status table, even if not_started
- Always record the current cell count
- progress.txt is human-readable plain text, no markdown formatting, no emoji

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
