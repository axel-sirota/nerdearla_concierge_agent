---
description: Validate the workshop exercise and solution notebooks (syntax, placeholders, pair parity, Spanish, AI-tells)
---

# Validate Notebooks

Run comprehensive validation on the exercise and/or solution notebook.

## What This Command Checks

There is ONE notebook. No exercise/solution pair.

### Nothing blocks (the most important check)
- **No `= None  # TU CODIGO` anywhere in the main flow.** Every cell runs as written
- No safety-net cells. They are obsolete because nothing blocks
- Mini exercises are comment-only cells, marked `(opcional, para despues)`
- No later cell reads a variable that a mini exercise was supposed to define
- Every mini exercise number has a matching entry in the end solutions section

### Structure
- Four-beat arc per concept: problem intro + naive code, diagram placeholder, full demo,
  optional mini exercise
- `<!-- DIAGRAM: -->` placeholders present in markdown cells
- A `## Soluciones de los mini ejercicios` section exists near the end
- Cell order is correct (cell IDs chain correctly)

### Language and tone
- **All markdown, comments and printed strings in fully Rioplatense Spanish with voseo**
- Code identifiers in English
- No half-translated cells
- **Demo code is heavily commented**, since Axel narrates from the comments live
- No AI-tells (em dash, en dash, Unicode x, bare --- in markdown)

### Stack and environment
- API keys from a shared `.env` via `python-dotenv`. **Never `getpass`, never hardcoded**
- MCP client uses `MCPAdapter` from `langchain.mcp`. Flag any use of
  `langchain_mcp_adapters` or `MultiServerMCPClient`, both are deprecated
- MCP server uses `MCPServer` from `mcp.server.mcpserver`. Flag `FastMCP`, renamed in mcp 2.x
- Nothing requiring a cloud account, Docker, or a local install. Colab only

## CRITICAL: Cell Order Verification

Before running the script, also verify cell ordering manually by reading the notebook JSON and
confirming each cell's `id` field matches the sequence expected. When using NotebookEdit to
edit an existing cell, ALWAYS fetch the current cell `id` from the notebook first - never assume
an id. Steps:

1. Read the notebook file
2. Print each cell's `id` and its first line of source to confirm order
3. Only then call NotebookEdit with the verified `cell_id`

If cell order looks wrong after an edit, re-read the notebook to confirm actual order before
making further edits.

## Instructions

Run the notebook validation script to verify:
- Python syntax correctness in all code cells
- No deprecated MCP imports
- No hardcoded API keys
- No blocking placeholders in the main flow

## Usage Patterns

### After each 5-cell batch (during /build-notebook)
```bash
.venv/bin/python3 validate_notebooks.py concierge_workshop.ipynb --type exercise
```

### Generate requirements.txt
```bash
.venv/bin/python3 validate_notebooks.py concierge_workshop.ipynb --requirements
```

## AI-Tells Scan (MANDATORY before marking any notebook done)

Run this grep on every completed notebook to catch forbidden typography in cell source:

```bash
# Em dash (—), en dash (–), Unicode multiplication (×), horizontal rule as separator
python3 -c "
import json, sys
path = sys.argv[1]
with open(path) as f:
    nb = json.load(f)
hits = []
banned = [('—', 'em dash'), ('–', 'en dash'), ('×', 'unicode multiplication')]
for i, cell in enumerate(nb['cells']):
    src = ''.join(cell.get('source', []))
    for char, name in banned:
        if char in src:
            line = next((l for l in src.splitlines() if char in l), '')
            hits.append(f'Cell {i} ({cell[\"cell_type\"]}): {name} found -> {line.strip()[:80]}')
    # Check for --- as a markdown horizontal rule (only flag in markdown cells)
    if cell['cell_type'] == 'markdown':
        for j, line in enumerate(src.splitlines()):
            if line.strip() == '---':
                hits.append(f'Cell {i} (markdown): bare --- separator on line {j}')
if hits:
    print('AI-TELLS FOUND:')
    for h in hits: print(' ', h)
    sys.exit(1)
else:
    print('AI-tells scan: clean')
" <notebook_path>
```

Replace `<notebook_path>` with the actual path.

**If hits are found**: correct them before marking the beat done.

Note: emojis are allowed and will NOT be flagged. Only the banned characters above are checked.
Spanish accented characters are fine and are NOT AI-tells.

## Pass Criteria

- No syntax errors in code cells
- **Nothing blocks**: no `= None  # TU CODIGO` in the main flow
- Every mini exercise has a matching entry in the end solutions section
- AI-tells scan: clean (no em dashes, en dashes, Unicode multiplication, bare `---` separators)
- No deprecated MCP imports (`langchain_mcp_adapters`, `MultiServerMCPClient`, `FastMCP`)
- No hardcoded API keys

## When to Run

- After every 5-cell batch during /build-notebook (mandatory)
- After completing each beat
- Before the workshop, after a full top-to-bottom run in Colab

## See Also

- `validate_notebooks.py` - The validation script in repo root

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
