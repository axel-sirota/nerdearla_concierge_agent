---
description: Initialize plans/DECISIONS.md by asking questions one at a time about the workshop
---

Initialize the workshop manifest: $ARGUMENTS

This command creates `plans/DECISIONS.md` - the single source of truth
that every other command reads before doing any work. Run this once at the start, or when
workshop details change.

Read `CLAUDE.md` first. It already locks the language rule, the stack, and the agenda, so do
not re-ask anything it answers. This interview fills only what CLAUDE.md leaves open.

---

## Guard

If `plans/DECISIONS.md` already exists, read it first and show the user
the current contents, then ask: "Do you want to update specific sections, or start fresh?"
If updating: only re-ask questions for sections the user wants to change.
If starting fresh: proceed with the full interview below.

---

## Process: One Question at a Time

Ask each question individually. Wait for the answer before asking the next one.
Do NOT dump all questions at once.
After each answer, confirm you understood it before moving on.

Keep a running draft in memory as answers come in.
After the final question, show the complete draft and ask for approval before writing the file.

---

## Questions (ask in this order)

**Block 1 - The Audience**

Q1: "Who shows up to a Nerdearla talk like this? Backend devs, data people, students, a mix? And roughly how many?"

Q2: "How much agent experience do you assume? Have they built with LangGraph or MCP before, or is this their first contact?"

Q3: "Any misconception about multi-agent systems you specifically want to kill in this hour?"

**Block 2 - The Case**

Q4: "The running example is the Bariloche request: flights, a hotel near the centre, what to do on the weekend. Do we keep Bariloche throughout, or does the destination change per lab?"

Q5: "Are the flight and hotel APIs faked with hardcoded data, stubbed with a fixture file, or hitting something real?"

Q6: "Lab 4 breaks a race condition on purpose. Do you want the break to happen live and fail loudly in the output, or a pre-captured traceback shown in markdown?"

**Block 3 - The Environment**

Q7: "Colab free tier, or do you expect attendees on Colab Pro? Affects how heavy we can go."

Q8: "Whose API keys? Attendees bring their own, or do you hand out a shared workshop key?"

Q9: "Which model for the agents? And is there a cheap fallback if the room is bigger than expected and rate limits bite?"

Q10: "If someone's MCP stdio subprocess does not start in Colab, what is the fallback you want baked into the notebook?"

**Block 4 - The Delivery**

Q11: "Live coding with the room following along, or do you demo while they watch and they run labs after?"

Q12: "Each lab is 12 minutes. In practice, do you want the lab cell solvable in 12 minutes by a median attendee, or is it fine if only the fast ones finish and the rest use the safety net?"

Q13: "Do you project the notebook itself, slides, or both? Affects how much lives in markdown vs a separate deck."

**Block 5 - Tone and Constraints**

Q14: "Spanish register: fully Rioplatense with voseo, or neutral Latin American Spanish for a wider room?"

Q15: "Anything else about how you want to run this hour that is not captured above - pacing, what makes this land vs fall flat, the one thing they must leave with?"

---

## After All Answers: Write the File

Show the complete draft in chat and ask for approval.

Once approved, write `plans/DECISIONS.md` with this structure:

```markdown
# Workshop Manifest: Concierge de Viajes Multiagente
# Nerdearla - 60 minutes, live
# Last updated: <YYYY-MM-DD>
#
# This file is read by every command before any work begins.
# Update it by running /init-workshop.

## The Audience

- **Who attends**: <answer>
- **Expected headcount**: <answer>
- **Agent / LangGraph / MCP experience assumed**: <answer>
- **Misconception to kill**: <answer>

## The Case

- **Destination**: <Bariloche throughout / varies per lab>
- **Flight and hotel data**: <hardcoded / fixture file / real API>
- **Lab 4 race condition**: <live failure / pre-captured traceback>

## Environment

- **Colab tier**: <free / Pro>
- **API keys**: <attendees bring own / shared workshop key>
- **Model**: <answer>
- **Cheap fallback model**: <answer>
- **MCP stdio fallback in Colab**: <answer>

## Delivery

- **Teaching style**: <live coding / demo then labs>
- **Lab difficulty target**: <median attendee finishes / fast ones finish, rest use safety net>
- **Projection**: <notebook / slides / both>

## Constraints and Tone

- **Spanish register**: <Rioplatense voseo / neutral Latin American>
- **Teaching philosophy notes**: <answer>

## Key Decisions (locked by CLAUDE.md)

- Notebook content in Spanish, code identifiers in English, chat with Axel in English
- One notebook for the whole workshop: concierge_workshop.ipynb.
  No exercise/solution pair; mini-exercise solutions live in a section at the end
- Environment: Google Colab, pip install in-notebook, shared .env via python-dotenv
- MCP server side: MCPServer from mcp.server.mcpserver (NOT FastMCP, renamed in mcp 2.x)
- MCP client side: MCPAdapter from the langchain.mcp namespace (beta, needs the fastmcp
  package). NOT langchain-mcp-adapters / MultiServerMCPClient, that package is unmaintained
- MCPAdapter takes a Path for a local stdio server, never a plain string
- Lab 1 agent: plain Python, no framework. Lab 2 agent: LangGraph
- Supervisor mode: langgraph-supervisor. Swarm mode: langgraph-swarm
- Race condition fix: reducer, Annotated[list[...], operator.add]
- MCP transport: stdio servers via %%writefile, launched as subprocesses
- No blocking placeholders. Mini exercises are comment-only and optional
- NOTHING BLOCKS: every cell runs as written. No safety-net cells
- No cell budget. Timing is checked by reading the notebook aloud
- No em dashes, no en dashes, no bare --- separators in notebook cells
- Emojis in section headers and first-person voice are encouraged
```

---

## Confirm

After writing, say:

> `plans/DECISIONS.md` written.
>
> Every command will now read this file before starting work. Run `/start-session` to see your current progress, or `/run-research-lab 1` to begin Lab 1.

---

## Notebook Edit Protocol (awareness)

If this skill ends up editing notebook cells (not just reading them), follow
the canonical procedure in `~/.claude/NOTEBOOK_EDIT_PROTOCOL.md`: normalize
cell ids, size-gate the mechanism, locate cells by id + content, read back and
assert after every edit, and run the structural + static code gates. Blind
bulk index-based rewrites are forbidden.
