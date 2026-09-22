---
description: Reload saved workshop state from progress.txt and orient the session to continue the build
---

# /resume

Load the saved session state from `progress.txt` and orient the current conversation
so work can continue immediately. Ask at most one clarifying question.

---

## Process

### Step 1: Check for progress.txt

```bash
ls progress.txt 2>/dev/null
```

If not found:

> `progress.txt` not found. Run `/save-state` first to snapshot session state, or
> run `/start-session` to load context from scratch.

Stop here if not found.

### Step 2: Read progress.txt

Read the full file. Extract:
- All lab statuses from the LAB STATUS section
- All open issues from KNOWN ISSUES
- All locked decisions from LOCKED DECISIONS
- The NEXT ACTION line

### Step 3: Read supporting files to verify state is current

The progress.txt snapshot may be hours or days old. Verify it is still accurate:

```bash
ls -la concierge_workshop.ipynb 2>/dev/null
ls plans/lab_*.md diagrams/*.mmd 2>/dev/null
```

Cross-check: does the filesystem match what progress.txt says?
- If a notebook exists that progress.txt says is missing -> update your understanding
- If progress.txt says done but the notebook is missing -> flag it

Do NOT re-run full validation. Trust progress.txt unless filesystem contradicts it.

### Step 4: Print orientation summary

Print this exact format to chat (no preamble, no "let me tell you what I found"):

```
=== RESUMED SESSION ===

Saved: <date from progress.txt>

NOTEBOOK
  concierge_workshop.ipynb - <N> cells

DONE
  Lab 0 - El caso (cells 0-8)
  Lab 1 - AgenteVuelos (cells 9-22)

IN PROGRESS / NEXT
  Lab 2 - AgenteHoteles  [plan exists, no cells built yet]

NOT STARTED
  Labs 3-5

DIAGRAMS
  Built: <list>    Placeholders pending: <list>

OPEN ISSUES
  <list or "none">

NEXT ACTION
  /build-notebook 2
  Reason: plan exists at plans/lab_2_agente-hoteles.md, no cells built yet.

KEY DECISIONS (active)
  - Notebook in Spanish, code identifiers English, chat in English
  - ONE notebook for the whole workshop, not one per lab
  - MCPAdapter from langchain.mcp, NOT langchain-mcp-adapters
  - Mini exercises are additive and optional; solutions live at the end
  - Verify cell_id with python snippet before every NotebookEdit
  - Demo-led, nothing blocks, solutions at the end

=== READY ===
```

### Step 5: Ask at most one clarifying question

After printing the summary, ask ONE question only if the intent is genuinely ambiguous:

- If NEXT ACTION is obvious from progress.txt -> do not ask, just confirm ready
- If multiple labs are in_progress simultaneously -> ask "Which lab do you want to
  continue with first?"
- If progress.txt NEXT ACTION conflicts with filesystem state -> describe the conflict
  and ask which is correct

Never ask more than one question. Never ask for information already in progress.txt or
the filesystem.

---

## Non-Negotiables

- Read progress.txt first, verify against filesystem second
- Print the orientation summary before asking anything
- One question max - if you have to ask more than one, you have not read the files carefully enough
- Do not start building or fixing anything unless the user says "go" or "continue"

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
