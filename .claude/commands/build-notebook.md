---
description: Build the workshop notebook, 5 cells at a time with approval checkpoints
---

Build the workshop notebook. Optional argument: a lab number to build or rebuild just that
section (e.g. `3`). With no argument, build the whole notebook in agenda order.

$ARGUMENTS

## GUARD: Read Course Manifest First

Before doing anything else, check for `plans/DECISIONS.md`:

```bash
ls plans/DECISIONS.md 2>/dev/null
```

If the file does NOT exist, stop immediately and say:

> `plans/DECISIONS.md` not found. Run `/init-workshop` first to record the workshop decisions. Every command requires this file before proceeding.

If it exists, read the full file. It is the source of truth for the arc, the audience, the tone, the diagrams, and every decision Axel made in the interview.

---

**CRITICAL INSTRUCTIONS - READ CAREFULLY BEFORE STARTING**

## Command Arguments

This command takes an OPTIONAL argument: a lab number (e.g., `3`).

- `/build-notebook` builds the whole notebook in agenda order.
- `/build-notebook 3` builds or rebuilds only the Lab 3 section.

The environment is always **Colab** for this workshop. Do not ask.

There is ONE notebook for the whole workshop: `concierge_workshop.ipynb` at the repo root.
No exercise/solution pair. Mini-exercise solutions live in a section at its end.

---

## Pre-Work: MANDATORY Reading

### Step 1: Read All Context Files (DO THIS FIRST)

**YOU MUST READ THESE FILES BEFORE DOING ANYTHING:**

1. **CLAUDE.md** - Language rule, stack, agenda, notebook conventions, critical rules
2. **plans/DECISIONS.md** - The workshop manifest
3. **plans/lab_<N>_<slug>.md** - The cell-by-cell plan produced by `/run-research-lab`
4. If building lab N > 1: the already-built sections of `concierge_workshop.ipynb` -
   confirm the exact variable names, server file names, and client objects already in scope.
   This is ONE notebook, so every earlier variable is still live. Never redefine a name
   that already exists; bridge to it.

### Step 2: Show Plan Summary Before Building

**IN CHAT, SHOW ME (in English):**
1. Lab title and learning objectives
2. List of concepts (2-4) with their Problem / Diagram / Demo breakdown
3. Total estimated cell count, and the running total for the notebook
4. Which mini exercises this beat adds, and their numbers
5. Any continuity bridges from the prior lab section (exact variable names carried forward)
6. The clock check: can Axel narrate these cells inside the beat's slot?

**DO NOT PROCEED until I approve this summary.**

---

## Core Teaching Principles

### 1. Four-Beat Arc for Every Concept
Every concept in the notebook follows exactly this sequence:

**Beat 1 - Problem intro (Markdown + naive/broken code)**
Show what goes wrong WITHOUT this concept. Attendees feel the pain before the cure.
The naive code cell runs and shows the problem, that is the point.

**Beat 2 - Diagram placeholder (Markdown)**
Insert this exact comment so `/build-diagrams` can find and fill it later:
```
<!-- DIAGRAM: describe what this diagram should show -->
```
Followed by 1-2 sentences explaining what the diagram will illustrate.

**Beat 3 - Full working demo (Code)**
Complete, runnable, heavily commented. Axel narrates from these comments.

**Beat 4 - Mini exercise (optional)**
A comment-only cell, additive. Nothing downstream reads it. See below.

### 2. Demo-Led, and NOTHING BLOCKS

This is the single most important structural rule. See `plans/DECISIONS.md`.

Axel demos and explains the code as he goes. Attendees take the notebook home and run it
there. Some follow along live on laptops, most just watch.

**Therefore every cell runs top to bottom exactly as written.** There are NO
`None  # TU CODIGO` placeholders in the main flow. A blocked cell breaks the notebook for
everyone who is only watching, which is most of the room.

**Mini exercises are additive.** They live in their own clearly marked cells, they never sit
in the path of the next cell, and nothing downstream depends on their output. Anyone can
skip every single one and the notebook still runs end to end.

Mini exercise cell shape:

```python
# EJERCICIO 1 (opcional, para despues)
# Agregale al agente una tool que busque actividades para el finde.
# Pista: es el mismo patron que buscar_vuelos, cambia la query.
# La solucion esta al final del notebook.
```

Note it is a comment block, not an assignment to `None`. Nothing to fill in that anything
else reads.

**Solutions go in a dedicated section at the end of the notebook**, never inline. Someone
stuck at home scrolls down. Nobody is graded.

Because nothing blocks, **safety-net cells are unnecessary and must not be added.** They
existed to rescue a blocked lab. There are no blocked labs.

### 3. Tone - Spanish, First Person, Friendly

**Every markdown cell, code comment and printed string is in Spanish.** Code identifiers
stay in English. Chat with Axel stays in English. See the language rule in CLAUDE.md.

- First person plural throughout: "Vamos a ver...", "Fijate que si no hacemos esto...",
  "Ahora lo rompemos a proposito"
- Fully Rioplatense register with voseo: 'fijate', 'arma', 'vos', 'acordate'
- Encouraging and warm, attendees may be meeting MCP for the first time
- Emojis welcome in markdown cell headers and section titles
- No jargon unless I explain it in the same cell. "Supervisor", "swarm" and "MCP" each get
  one plain-Spanish sentence the first time they appear
- Never half-translate: a cell is fully Spanish, never Spanish headers with English body

### 4. Heavy Comments
- Every non-obvious line has a comment explaining the WHY
- Demo cells are fully commented as live-coding reference
- The comments ARE the script Axel reads from. Thin comments fail the beat

### 5. Self-Contained Data Only
- Flights and hotels come from serper.dev, wrapped so the messy SERP is normalized into a
  clean shape. Axel says on stage: 'esta parte es solo algoritmica'
- Never hardcode API keys. They come from a shared `.env` loaded with `python-dotenv`,
  which Axel distributes at the workshop. NOT `getpass`
- Nothing that needs a cloud account, a Docker daemon, or a local install. Colab only

---

## Notebook Structure

### Header (Cells 0-4), built once for the whole notebook
- **Cell 0 (Markdown)**: Workshop title with emoji, the Bariloche request quoted, what they
  leave with, the agenda table
- **Cell 1 (Markdown)**: "Seccion 0: Preparamos el entorno"
- **Cell 2 (Code)**: `!pip install -q ...` with pinned versions from requirements.txt
- **Cell 3 (Code)**: All imports + `load_dotenv()` reading the shared `.env`
- **Cell 4 (Markdown)**: "Que vamos a construir" - the concierge, with the opening diagram:
  the Bariloche request fanning into 3 unrelated jobs

### Per Concept (repeat 2-4 times, each concept = 5-7 cells)
1. **Markdown**: Concept section header + problem intro paragraph (first person, what breaks without this)
2. **Code**: Naive/broken demo that runs and shows the problem
3. **Markdown**: Diagram reference cell - contains the `<!-- DIAGRAM: ... -->` comment from the plan PLUS a link to the diagram file:
   ```
   <!-- DIAGRAM: description from plan -->
   [Ver diagrama: titulo del diagrama](diagrams/<slug>.mmd)
   > Diagrama pendiente via /build-diagrams.
   ```
   Then 1-2 sentences in Spanish explaining what the diagram shows conceptually.
4. **Code**: Full working demo. Complete, runnable, and **heavily commented**, because Axel
   narrates from these comments live and they carry the notebook for whoever runs it at home
5. **Code** (optional): A mini exercise, as a comment block in its own cell. Additive only,
   nothing downstream reads it. Its solution goes in the end section, not here

**Diagram placeholder rule**: The link path `diagrams/<slug>.mmd` is relative to the repo
root, since the notebook lives at the root. It must match exactly the slug recorded in the
plan's diagram index. The file does not exist yet, that is expected. `/build-diagrams` creates
it. Do not skip the link or use a different path.

### Closing (Section 6, the last 4 minutes)
- **Markdown**: Key takeaways, what we built, how this scales to 100 agents
- **Markdown**: The template to keep going alone, with the repo link
- **Markdown**: Q&A prompt

---

## CRITICAL: 5-Cell Approval Checkpoints - MANDATORY

**YOU MUST NEVER ADD MORE THAN 5 CELLS WITHOUT EXPLICIT USER APPROVAL**

### Process (DO NOT DEVIATE):

1. Add exactly 5 cells (or fewer for the final batch)
2. STOP IMMEDIATELY
3. Run validation: `.venv/bin/python3 validate_notebooks.py concierge_workshop.ipynb --type exercise`
4. **UNCONDITIONAL /save-state rule**: whenever the notebook cell count crosses a multiple of 10
   (reaches 10, 20, 30, ...), invoke the `/save-state` skill immediately. This fires regardless
   of whether the user said "go until the end", "continue", or anything else. It is NOT optional
   and is NOT skipped in continuous mode. Context compaction can happen at any time; save-state
   ensures a new session can resume from exactly where the build was interrupted.
5. Ask user: "I have added cells X-Y. How does it look? Should I continue?"
   If the user previously gave blanket "go until end" approval, skip this question and continue -
   but step 4 still fires unconditionally at every 10-cell boundary.
6. After approval (or under blanket approval): add ONLY the next 5 cells, then return to step 1.

### Forbidden:
- Adding 6+ cells in a single batch without approval (blanket "go" covers subsequent batches)
- Skipping validation between batches
- Skipping /save-state at 10-cell boundaries for any reason, including "go until end" mode

### Notebook Write Pattern (CRITICAL FOR FILE SIZE):

When writing large content (markdown with many lines, long code cells), NEVER write all cells in one tool call. Even within a single 5-cell batch:
- Add cells one at a time if any single cell exceeds ~30 lines
- This prevents JSON truncation in the notebook file

---

## Cell Order: ALWAYS Use cell_id

**After the first cell, ALWAYS pass `cell_id` to NotebookEdit.**

### MANDATORY: Verify Cell ID Before ANY NotebookEdit call

Before EVERY NotebookEdit (replace, insert, OR delete), run this python snippet to confirm
the cell_id is at the expected position. This prevents editing the wrong cell or deleting
unintended content:

```bash
.venv/bin/python3 -c "
import json
with open('PATH_TO_NOTEBOOK') as f:
    nb = json.load(f)
for i, c in enumerate(nb['cells']):
    print(i, c.get('id','?'), c['cell_type'], repr(''.join(c['source'])[:60]))
"
```

Check the output, confirm the target cell_id is where you expect it, THEN make the edit.
Never skip this step - it is the only way to be certain you are not deleting or overwriting
the wrong cell.

Workflow:
1. Create empty notebook with Write tool (minimal JSON skeleton)
2. Add Cell 0 with `edit_mode="insert"` - no `cell_id` needed
3. Before adding Cell 1: run python snippet to confirm Cell 0's id
4. Add Cell 1 with `cell_id="<id-of-cell-0>"` - insert after Cell 0
5. Before each subsequent cell: run python snippet to verify position
6. Continue chaining `cell_id` for every subsequent cell

**Never assume cells append to the end automatically. Always chain cell_id.**

### Empty Notebook JSON Skeleton:
```json
{
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.11.0"
  }
 },
 "cells": []
}
```

---

## Markdown Rendering

Markdown cells use raw strings - no escaping needed:
```python
new_source = """# Lab 3: Que trabajen juntos, modo supervisor

## Que vamos a lograr

Al final de esta seccion vas a poder:
- Coordinar dos agentes MCP bajo un supervisor
- Entender por que el supervisor tambien es un agente

```python
# Bloque de codigo inline de ejemplo
supervisor = create_supervisor(agents=[vuelos, hoteles])
```
"""
```

Never escape markdown characters. Never double-backslash headers.

---

## Mini Exercises and the Solutions Section

There is ONE notebook. No exercise/solution pair.

### Mini exercise cells

A comment block in its own cell. Nothing assigned, nothing downstream depends on it:

```python
# EJERCICIO 2 (opcional, para despues)
# El agente busca vuelos. Agregale una tool que busque actividades para el finde
# usando el mismo wrapper de serper que ya tenemos.
# Pista: mira como definimos buscar_vuelos y cambia la query.
# Solucion al final del notebook.
```

Rules:
- Numbered sequentially across the whole notebook: EJERCICIO 1, 2, 3...
- Always says `(opcional, para despues)`, so nobody watching feels they are falling behind
- Always ends with `Solucion al final del notebook.`
- Never assigns `None` to anything
- Never referenced by a later cell

### The solutions section

The last content section before the close, titled `## Soluciones de los mini ejercicios`.

One subsection per exercise, in order, each with:
- The exercise restated in one line
- A complete, runnable, commented implementation
- One or two sentences on why it works

These cells are runnable but nothing else depends on them, so the notebook is valid whether
or not anyone executes them.

---

## Workflow Summary

1. Read all context files, starting with `plans/DECISIONS.md`
2. Show plan summary - wait for approval
3. The notebook `concierge_workshop.ipynb` already exists with its section skeleton.
   Insert this beat's cells into its section. Never overwrite the file
4. Build the beat:
   - Add 5 cells
   - Run validation
   - After every 10 cells: invoke /save-state before asking for approval
   - Show user and ask for approval
   - Repeat until complete
5. Add any mini-exercise solutions to the `## Soluciones de los mini ejercicios` section
   at the end, matching the exercise numbers used in this beat
6. Final validation:
   - `.venv/bin/python3 validate_notebooks.py concierge_workshop.ipynb --type exercise`
   - The notebook runs top to bottom in Colab without errors, with no cell requiring
     anyone to fill anything in
   - File size reasonable (under 500 KB)

---

## Checklist (complete before marking done)

- [ ] Section title has emoji, learning objectives clear
- [ ] **Everything attendee-facing is in fully Rioplatense Spanish with voseo**: markdown,
      comments, printed strings
- [ ] Code identifiers are in English
- [ ] No half-translated cells
- [ ] **NOTHING BLOCKS**: every cell runs as written, no `None  # TU CODIGO` in the main flow
- [ ] No safety-net cells (they are obsolete, nothing blocks)
- [ ] Mini exercises are comment-only, additive, marked `(opcional, para despues)`, and
      nothing downstream reads them
- [ ] Each mini exercise has a matching entry in the end solutions section
- [ ] Colab setup: pip install + `.env` via python-dotenv, no cloud accounts, no getpass
- [ ] MCP client uses `MCPAdapter` from `langchain.mcp`, NOT `langchain-mcp-adapters`
- [ ] MCP server uses `MCPServer` from `mcp.server.mcpserver`, NOT `FastMCP`
- [ ] Every concept has: problem intro, diagram placeholder, full demo
- [ ] Naive/broken demo cell precedes every full demo
- [ ] Diagram placeholder `<!-- DIAGRAM: ... -->` present for each concept
- [ ] **Demo code is heavily commented**, because Axel narrates from the comments live
- [ ] First person plural tone throughout ("Vamos a ver...")
- [ ] Wrap-up cell connects to the next beat
- [ ] AI-tells scan passed (no em dashes, no en dashes, no `---` separators, no Unicode multiplication)
- [ ] Validation passes

---

## Update plans/LABS.md on Completion

When a beat's cells are fully built and validated:

1. Read `plans/LABS.md`
2. Find the entry for this beat
3. Update status: `- **Status**: in_progress` -> `- **Status**: done`
4. Mark the manifest checkboxes as done (`[ ]` -> `[x]`)

When starting the exercise build (before solution):
- Set status to `in_progress`

Use Edit (not Write) - do not rewrite the whole file, only the targeted lines.

---

## Notebook Edit Protocol (MANDATORY)

This skill edits Jupyter notebook cells. Before any cell edit, insert, or
delete, you MUST follow the canonical procedure in
`~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`. In short:

- Normalize cell ids first (`nbformat.normalize`) so every cell has an id.
- Pick the mechanism by size: `NotebookEdit` only if the notebook fits the
  Read limit (~25k tokens); otherwise a targeted, audited in-place JSON edit.
- Locate every cell by id AND by asserting its current content.
- Control insert position explicitly - never trust append/insert order.
- After every edit: read back from disk and assert the cell content.
- Run the structural gate (`nbformat.validate`) and the static code gate
  (`ast.parse` + `pyflakes` on all code cells concatenated in order).

Blind bulk scripts that rewrite cells by index are forbidden. Read the full
protocol file before editing.
