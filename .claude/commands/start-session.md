---
description: Begin a work session - load context, review progress, identify next steps
---

Start a new work session for this project.

## GUARD: Read Course Manifest First

Before doing anything else, check for `plans/DECISIONS.md`:

```bash
ls plans/DECISIONS.md 2>/dev/null
```

If the file does NOT exist, stop immediately and say:

> `plans/DECISIONS.md` not found. Run `/init-workshop` first to record the workshop decisions. Every command requires this file before proceeding.

If it exists, read the full file and keep its contents in mind throughout this command.

---

## Step 1: Load All Context

Read these files in order:

1. `CLAUDE.md` - full project context, language rule, stack, agenda, workflow
2. `plans/DECISIONS.md` - the workshop manifest

## Step 2: Load LABS.md (Primary Source of Truth)

Read `plans/LABS.md` if it exists - this is the authoritative status tracker.

If it does NOT exist, say:
> `plans/LABS.md` not found. I can create it from the agenda in CLAUDE.md, or you can run `/init-workshop` if the manifest is also missing.

If it does exist, read the Summary table and the Open Issues sections for each lab.

Also check for open items in TODOS.md:
```bash
grep -c "\[OPEN\]" TODOS.md 2>/dev/null || echo "0"
```

## Step 3: Cross-Check Filesystem

Verify LABS.md matches reality:

```bash
ls -la concierge_workshop.ipynb 2>/dev/null
ls plans/lab_*.md diagrams/*.mmd 2>/dev/null
```

Then list the notebook's actual section headers and cell count:

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

Flag anything that:
- Exists in the notebook but is not marked done/in_progress in LABS.md
- Is marked done but has no matching section header in the notebook
- Is a diagram placeholder in the notebook with no `.mmd` file in `diagrams/`

## Step 4: Report Status

Report the Summary table from LABS.md, plus:
- Current cell count (informational, there is no cell budget)
- Unbuilt diagrams (placeholders with no `.mmd` file)
- Any filesystem mismatches found in Step 3

## Step 5: Recommend Next Step

State clearly:
- Next lab to work on (first not_started or in_progress)
- Whether to run `/run-research-lab N` (no plan), `/build-notebook N` (plan exists),
  or `/build-diagrams N` (notebook built, diagrams still placeholders)
- If the solution notebook is out of sync with the exercise, say so and recommend
  rebuilding it before anything else

## Step 6: Ask

Ask the user: "Ready to proceed with [recommended next step]? Or is there something else you want to work on?"

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
