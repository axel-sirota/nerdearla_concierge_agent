---
description: Build Mermaid diagram files one by one from a lab's research plan into diagrams/
---

Build diagrams for lab: $ARGUMENTS

(Argument is a lab number. With no argument, build every unbuilt diagram in the notebook.)

## GUARD: Read Course Manifest First

Before doing anything else, check for `plans/DECISIONS.md`:

```bash
ls plans/DECISIONS.md 2>/dev/null
```

If the file does NOT exist, stop immediately and say:

> `plans/DECISIONS.md` not found. Run `/init-workshop` first to record the workshop decisions. Every command requires this file before proceeding.

If it exists, read the full file and keep its contents in mind throughout this command.

---

This command runs AFTER `/run-research-lab N` has produced the plan and AFTER `/build-notebook N` has built the notebook section with diagram link placeholders.

It reads the diagram index from the plan file, builds each Mermaid diagram one at a time into `diagrams/<slug>.mmd`, and asks for approval between each one.

---

## Step 1: Read Context

1. Read `plans/lab_<N>_<slug>.md` - find the diagram index section (all entries with "Diagram slug:", "Diagram path:", "Description:")
2. Read the relevant notebook cells that reference each diagram to understand the exact context each diagram needs to serve

---

## Step 2: List All Diagrams

Print the full list of diagrams to build from the plan index:

```
Diagrams to build for Topic N:
1. <slug>.mmd - <description>
2. <slug>.mmd - <description>
...

I'll build them one at a time and ask for your approval before moving to the next.
```

**Ask**: "Ready to start with diagram 1? Or any specific order you want?"

---

## Step 3: Build Each Diagram (One at a Time, Approval Between Each)

For each diagram:

### 3a. Design the diagram in chat first

Before writing the file, show the Mermaid source in chat:

```
Diagram <N>: <slug>
Description: <from plan>
Context: <which cell this appears in, what concept it illustrates>

Proposed Mermaid source:

```mermaid
<source here>
```

Does this look right? I'll write the file once you approve.
```

**Wait for approval before writing the file.**

### 3b. Write the file

Once approved, create the directory if needed and write the file:

```bash
mkdir -p diagrams
```

File path: `diagrams/<slug>.mmd`

File contents - just the raw Mermaid source, no fences, no extra text:
```
graph TD
    A[...] --> B[...]
    ...
```

The file is plain Mermaid source so it can be rendered by any Mermaid-aware viewer (GitHub, JupyterLab extensions, VS Code).

### 3c. Confirm the notebook link resolves

Check that the notebook cell referencing this diagram has the correct relative path:
`diagrams/<slug>.mmd` (relative to the repo root, where the notebook lives)

If the path in the notebook cell is wrong, fix it with NotebookEdit (read the notebook first to get the cell_id).

### 3d. Ask before the next diagram

"Diagram `<slug>.mmd` written. Ready for diagram <N+1> (`<next-slug>`)?"

**Do not proceed until the user says yes.**

---

## Diagram Design Rules

- Keep diagrams focused: one concept per diagram, not a full system overview
- Use `graph TD` (top-down) for flow and pipeline diagrams
- Use `sequenceDiagram` for API call sequences (request/response flows)
- Use `flowchart LR` for decision trees (routing logic, guardrail checks)
- Node labels: short phrases, no em dashes, no special Unicode
- Max ~10 nodes per diagram - if it needs more, split into two diagrams
- Every node and edge label uses plain ASCII text only

### Node labels are in Spanish

The diagrams are shown to a Spanish-speaking audience, so node and edge labels are in
Spanish, plain ASCII, no accents that break Mermaid rendering. Keep them short.

### Good diagram types by concept:
- One agent drowning in the Bariloche request -> `graph TD`, one node fanning to too many
  responsibilities. This is the opening "why one agent is not enough" diagram
- Agent exposed as MCP server -> `graph LR` showing agent, adapter, MCP server, client
- Same client, two frameworks -> `graph TD` with two different agent boxes converging on one
  identical client call. This is the no-lock-in diagram, the most important one
- Supervisor mode -> `graph TD` with the supervisor routing to specialist agents and back
- Swarm mode -> `graph LR` with peer agents handing off directly to each other
- Race condition -> `sequenceDiagram` with two agents writing the same state key in one
  superstep, then a second diagram showing the reducer accumulating instead of overwriting

---

## Step 4: Summary

After all diagrams are built:

> All N diagrams written to `diagrams/`.
>
> Files:
> - `<slug1>.mmd`
> - `<slug2>.mmd`
>
> Notebook links verified: yes / no (if no, list which cells still need fixing)
>
> Next step: open the notebooks in JupyterLab and confirm the diagram links resolve, or run `/validate-notebooks` to check overall notebook health.

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
