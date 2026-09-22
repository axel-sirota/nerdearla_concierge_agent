---
description: Research one workshop demo and produce a cell-by-cell plan at plans/subagents/<N>_agentdemo.md that /build-notebook can consume directly
---

Research and plan demo: $ARGUMENTS

(Argument is a beat number, 1 to 7. See the table below.)

## GUARD: Read Workshop Manifest First

Before doing anything else, check for the workshop manifest:

```bash
ls plans/DECISIONS.md 2>/dev/null
```

If it does NOT exist, stop immediately and say:

> `plans/DECISIONS.md` not found. Run `/init-workshop` first. Every research-demos run requires it before proceeding.

If it exists, read it fully along with `CLAUDE.md` and keep both in mind throughout.

---

This command is the **natural precursor to `/build-notebook`**. Its only job is to produce a
plan file at `plans/subagents/<N>_agentdemo.md` so that `/build-notebook <N>` can build that beat's
section of the notebook cell by cell from it.

**This command does NOT create any `.ipynb` notebooks.** It produces markdown only.

**Web research is MANDATORY.**

Run the research DISCIPLINE, not a particular tool. Per cycle: state a hypothesis, gather
evidence, attack it with an antithesis, then refine. What is graded is the evidence trail,
not which tool produced it.

**Evidence ranking, strongest first:**
1. **Running the code** in `.venv/bin/python3` against the installed packages. Signatures,
   defaults and failure modes verified empirically beat any document.
2. Official docs and source for the exact installed version.
3. Current third-party writing, treated as a lead to verify rather than as fact.
4. Recall. **Never sufficient on its own.**

The `Skill` tool may be unavailable in a subagent context. If so, execute the discipline
directly. That is not a deviation and needs no apology; it is the intended fallback. Log each
cycle's hypothesis, evidence operations with URLs or executed snippets, antithesis and
refinement into the plan's `# RESEARCH VALIDATED` block.

## FAILURE DEFINITION

Exactly two outcomes: COMPLETE SUCCESS or COMPLETE FAILURE. No partial credit.

**COMPLETE SUCCESS** = all true:
- All 5 research cycles completed and visible in chat
- Each cycle shows a hypothesis, logged evidence, an antithesis and a refinement
- PRE-WRITE SELF-CHECK printed in chat with all YES answers
- Plan file written to `plans/subagents/<N>_agentdemo.md` with all required sections
- Every cell's Spanish content is drafted in the plan, not left as "write something here"

**COMPLETE FAILURE** = any of:
- Fewer than 5 research cycles
- Any cycle lacks logged evidence, or rests on recall alone where code could have been run
- PRE-WRITE SELF-CHECK not printed, or any field NO at Write time
- Plan file not written, or written with stub/placeholder content
- Any API surface asserted from memory instead of verified against current docs

If COMPLETE FAILURE: report what failed and restart from the beginning. Do not patch a partial result.

---

## Command Arguments

```
/research-demos <beat_number>
```

Example: `/research-demos 2`

The beat number maps to the arc in `plans/DECISIONS.md`:

| N | Beat | Slug |
|---|---|---|
| 1 | Agente en Python puro: la clase con el loop | agente-python |
| 2 | El mismo agente migrado a LangGraph | langgraph |
| 3 | Un agente con 6 tools que se equivoca | muchas-tools |
| 4 | Lo partimos: un agente por capacidad | especialistas |
| 5 | Quien le contesta al usuario: supervisor | supervisor |
| 6 | MCP: la agencia de al lado, y el nuestro | mcp |
| 7 | Y si se organizan solos: swarm | swarm |

---

## Output Contract (NON-NEGOTIABLE)

1. **One file only**: `plans/subagents/<N>_agentdemo.md`. Never write anywhere else.
2. **No `.ipynb` files.** No Write calls except to that one plan file.
3. **Plan must be directly executable by `/build-notebook`** - every cell has enough detail
   that the builder does not need to invent content. Spanish cell content is drafted here,
   not deferred to the builder.
4. **Structure** (every section required):
   - `# Beat <N> - <Title> - Cell-by-Cell Plan`
   - `## Context` (what attendees arrive with, by exact variable name, since this is ONE
     notebook and every earlier variable is still in scope; the key insight they leave with)
   - `## Through-Line` (how this beat advances the two things we are killing: "you need a framework" and "one agent, all the tools")
   - `## STAR Story` (Situation / Task / Action / Result for this beat's scenario)
   - `## Deliverables` (the cells added to the notebook, plus the mini exercises proposed)
   - `## Session Timing (<N> min)` table, matching the agenda slot exactly
   - `# CELL-BY-CELL CONTENT (Target: <N> cells)`
   - Each cell: `## Cell N - Markdown/Code: Description` with full Spanish content in a
     fenced block
   - `## Diagram Index` (slug, path `diagrams/<slug>.mmd`, description per diagram)
   - `# VERIFICATION CHECKLIST`
   - `# RESEARCH VALIDATED (Month Year)`

### Contract rule (MANDATORY, read plans/CONTRACT.md FIRST)

`plans/CONTRACT.md` is FROZEN. Every class name, function signature, variable name and
return shape is fixed there. You are running in parallel with other research subagents who
cannot see your output, so you MUST conform to it verbatim. Never invent a name the
contract already fixes. If a plan genuinely cannot be written within the contract, add a
`## CONTRACT CONFLICT` section describing the conflict, then continue with the contract as
written. Do not edit the contract.

### Continuity rule (this is ONE notebook)

Consult `plans/CONTRACT.md` Layer 3 for what this beat creates vs reuses. Also open any already-built sections of `concierge_workshop.ipynb`
and list the exact variables, server files, and client objects already in scope. For every
planned cell that reuses one, add a line:

- `Reuses: <exact variable name> from Cell <M>`

Never redefine a name that already exists. Never re-teach a concept already covered. If a
beat needs a variable that does not exist yet, say which earlier cell must create it.

### Writing the Plan File in Batches

If the plan will exceed ~150 lines, write the header + timing first, then append
cell-by-cell content in ~50-line chunks with Edit, then append the checklist + research block.

---

## Pre-Work: MANDATORY Reading

Before any research, read:

1. `CLAUDE.md` - language rule, MCP/LangGraph stack, agenda, notebook conventions, tone
2. `plans/OUTLINE.md` - the session running order. Find YOUR beat and see what comes
   immediately before and after it, so your plan bridges cleanly
3. `plans/CONTRACT.md` - FROZEN code contract. Conform verbatim
3. `plans/DECISIONS.md` - workshop decisions: audience, arc, tone, diagrams
3. `.claude/commands/build-notebook.md` - the consumer of your plan (structure it expects)
4. `plans/subagents/<N-1>_agentdemo.md` - the previous lab's plan, for the bridge into this one
5. For lab N > 0: open the already-built sections of `concierge_workshop.ipynb` and list the
   exact variables, server files, and client objects in scope. This is ONE notebook

---

## MANDATORY CYCLE TRACKER

Post this at the start of research and update after each cycle. Do NOT write the plan file
until all 5 boxes are `[x]` AND all show `evidence logged: YES`.

```
CYCLE TRACKER
[_] Cycle 1 - Agenda Alignment and Notebook Continuity        evidence logged: NO
[_] Cycle 2 - API Surface and Dependencies (Colab)            evidence logged: NO
[_] Cycle 3 - Pedagogical Structure (Problem -> Diagram -> Demo) evidence logged: NO
[_] Cycle 4 - Comment Quality and the Clock                   evidence logged: NO
[_] Cycle 5 - Through-Line, Timing, Take-Homes                evidence logged: NO
```

A cycle is NOT complete until its evidence is logged. No exceptions.

---

## Process: 5 TDD-Style Research Cycles

**All cycles visible in chat.** Every cycle needs logged evidence. "I already know this" does
NOT count. Where a claim is checkable by running code against the installed packages, run it:
that is the strongest evidence available and it has already caught several errors that docs
and recall both got wrong.

### Cycle 1 - Arc Alignment and Prior-Notebook Continuity
- Confirm this beat's scope against the arc in `plans/DECISIONS.md`.
- Read `plans/CONTRACT.md` Layer 3: what this beat creates, what it reuses.
- **Invoke `/research`**: current best practices for this beat's core concept (MCP server
  design, supervisor vs swarm, state reducers) as of 2026.
- **Refutation**: any variable-name collision with earlier sections? Re-teaching something
  already covered? Does this beat actually need its full slot, or is it padded?

### Cycle 2 - API Surface and Dependencies (Colab + MCP)
- Lock the full `!pip install -q` line, pinned to current stable.
- **Verify every import path and signature against current docs. APIs here drift fast.**
  Specifically confirm:
  - `MCPServer` constructor and the `@mcp.tool()` decorator signature. NOT `FastMCP`,
    which mcp 2.x renamed and moved out of `mcp.server.fastmcp`
  - `MCPAdapter` from `langchain.mcp`. **Confirm it is still the current path and that
    `langchain-mcp-adapters` / `MultiServerMCPClient` is still the deprecated one.**
    That package moved into the `langchain.mcp` namespace and is unmaintained
  - `create_supervisor` from `langgraph-supervisor`
  - `create_swarm` / handoff tools from `langgraph-swarm`
  - stdio transport config: how the client launches a `%%writefile` server as a subprocess
- **Invoke `/research`**: current stable versions + exact import paths for the above.
- **Refutation**: deprecated import path? Version conflict between the langgraph packages?
  Does the stdio subprocess pattern actually work in Colab, or does it need a shim?

### Cycle 3 - Pedagogical Structure (Problem -> Diagram -> Demo)
- For EACH concept (2-4 per beat), plan cells following the four-beat arc:
  - **Problem** markdown + naive code: what breaks WITHOUT this. It runs and shows the
    problem, that is the point. Attendees feel the pain before the cure
  - **Diagram** placeholder: `<!-- DIAGRAM: ... -->` plus the `diagrams/<slug>.mmd` link
  - **Demo** code: complete, runnable, **heavily commented** in Rioplatense Spanish, because
    Axel narrates from these comments live
  - **Mini exercise** (optional): a comment-only cell, additive, nothing downstream reads it
- **NOTHING BLOCKS.** No `None  # TU CODIGO` in the main flow. See `plans/DECISIONS.md`.
- Never chain more than 3 markdown cells without a code cell.
- **Invoke `/research`**: common gotchas when doing this demo with the chosen library.
- **Refutation**: would any cell fail for someone who skipped every mini exercise? Is the
  demo runnable in Colab as written? Is the naive cell genuinely broken, or theatrically so?

### Cycle 4 - Comment Quality and the Clock
- **The comments are the script.** Axel explains the code from them live, and they carry the
  notebook for whoever runs it at home without him. Thin comments fail this beat.
- Every non-obvious line gets a comment saying WHY, not what.
- Check the beat fits its slot when demoed and narrated, not when silently executed.
  Reading 40 lines of code aloud takes longer than running them.
- Plan the mini exercises: additive, clearly optional, each with a solution for the end
  section. Number them continuing from the previous beat.
- **Invoke `/research`**: the edge cases that most often eat workshop time for this topic.
- **Refutation**: could Axel talk through this cell for its allotted time without running
  out of things to say, or running long? What is the single most likely thing to go wrong
  live, and does the plan handle it?

### Cycle 5 - MCP Through-Line, Timing, Take-Homes
- State how this beat advances the workshop thesis: every agent is a tool, one adapter, no
  lock-in. Name the one-line bridge into the next lab.
- Verify the timing table sums to this beat's agenda slot.
- Produce RESEARCH VALIDATED block: every source URL + the specific fact extracted.
- Produce the VERIFICATION CHECKLIST.
- **Invoke `/research`**: production concerns worth naming in the take-home extension.
- **Refutation**: any unsourced claim? Any API signature asserted from memory rather than
  verified against docs in Cycle 2?

---

## HARD GATE: Pre-Write Self-Check (MANDATORY before any Write call)

Print this in chat and verify every line passes. Any NO = do not write; fix it first.

```
PRE-WRITE SELF-CHECK
--------------------
Cycle tracker all 5 checked [x]:               YES / NO
All 5 cycles have logged evidence:           YES / NO
Plan path is plans/subagents/<N>_agentdemo.md:          YES / NO
No .ipynb files created:                       YES / NO
STAR story section present:                    YES / NO
MCP through-line section present:              YES / NO
Continuity: reused variables named per cell:   YES / NO / N-A
Diagram index present with slugs and paths:    YES / NO
Every cell's Spanish content drafted in full:  YES / NO
MCPAdapter path verified against current docs: YES / NO
Beat fits its slot when narrated aloud:        YES / NO / N-A
Nothing blocks; mini exercises are additive:   YES / NO
RESEARCH VALIDATED block has URLs:             YES / NO
VERIFICATION CHECKLIST present:                YES / NO
All cells have full content (not stubs):       YES / NO
AI-tells scan passed (no em/en dashes):        YES / NO
```

---

## Non-Negotiables (Violating Any = Complete Failure, Start Over)

1. Path is always `plans/subagents/<N>_agentdemo.md` - never anywhere else.
2. No `.ipynb` files created.
3. All notebook-facing content drafted in Spanish; code identifiers in English.
4. NOTHING BLOCKS: no `None  # TU CODIGO` in the main flow. Mini exercises are additive.
5. Every concept has a Problem cell, a Demo cell AND a Lab cell; max 3 markdown cells
   without a code cell.
6. Every lab has a stretch for fast finishers and a take-home extension.
7. Every import path and signature verified against current docs, not memory.
8. `MCPAdapter` from `langchain.mcp` confirmed current; `langchain-mcp-adapters` /
   `MultiServerMCPClient` confirmed still deprecated.
9. Continuity confirmed by opening the actual built notebook sections. This is ONE notebook.
10. STAR story + MCP through-line sections both present.
11. All 5 cycles visible, all `[x]`, all `evidence logged: YES` before any Write.
12. Every cycle logs real evidence. Any claim checkable by running code against the
    installed packages MUST be checked that way, not asserted.
13. PRE-WRITE SELF-CHECK printed with all YES (or N-A where noted) before Write.
14. The lab fits its agenda slot. Cut scope rather than extend the slot.
15. ZERO AI-TELLS in the plan file: no em dashes, no en dashes, no Unicode multiplication.
    Final pass before Write.

---

## Workshop Stack Defaults (this repo)

See CLAUDE.md for the authoritative list. Summary:

- **MCP server**: `from mcp.server.mcpserver import MCPServer`, stdio transport, written to
  disk with `%%writefile` and launched as a subprocess. NOT `FastMCP`.
- **MCP client**: `MCPAdapter` from the `langchain.mcp` namespace. NOT
  `langchain-mcp-adapters`, NOT `MultiServerMCPClient`. That package is unmaintained.
- **Lab 1 agent**: plain Python, no framework. **Lab 2 agent**: LangGraph. Same client call
  for both, which is the entire point of the workshop.
- **Supervisor**: `langgraph-supervisor`. **Swarm**: `langgraph-swarm`.
- **Race condition**: parallel nodes writing one state key raise `InvalidUpdateError`
  (`INVALID_CONCURRENT_GRAPH_UPDATE`). Fix: `Annotated[list[...], operator.add]`.
- **Environment**: Google Colab, pip install in-notebook, shared `.env` via python-dotenv.
- **Data**: hardcoded or fixture-based flights and hotels. No live travel API.
- **Placeholders**: `None  # TU CODIGO` (exercise); full code + Spanish explanation (solution).

---

## Handoff

Once the plan file is written, end with:

> Plan written to `plans/subagents/<N>_agentdemo.md`.
>
> Next step: run `/build-notebook <N>` to add this beat's section to the notebook,
> 5 cells at a time with approval between batches.

Do not offer to run `/build-notebook` yourself.

---

## Notebook Edit Protocol (awareness)

If this command edits notebook cells (it should not - it writes markdown only), follow the
canonical procedure: normalize cell ids, locate cells by id + content, read back and assert
after each edit. Blind bulk index-based rewrites are forbidden.
