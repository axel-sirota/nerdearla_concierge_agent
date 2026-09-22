---
description: Read all project context files before starting any work
---

Read the following files to load full project context:

1. `CLAUDE.md` - language rule, stack, agenda, notebook conventions, critical rules
2. `plans/DECISIONS.md` - the workshop manifest
3. `plans/LABS.md` - status tracker, if it exists

Then report back:
- Which labs have plans in `plans/lab_*.md`
- Which lab sections are already built in `concierge_workshop.ipynb` (list the cell ranges)
- Which diagrams exist in `diagrams/` vs which are still placeholders
- What is the next lab to work on

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
