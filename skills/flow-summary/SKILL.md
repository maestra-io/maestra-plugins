---
name: flow-summary
description: >-
  Produce a concise, structured business summary of a marketing
  scenario (flow) from its structure. Use when you need to understand or
  explain what an existing flow does — before adapting it, editing it, auditing
  it, or reporting to a user. Reads the flow with the project's flow tools and
  looks up block / event / step meanings in the flows wiki. Don't use to audit a
  flow for problems (use flow-issues-audit) or to create, edit, or launch a flow
  (use flow-create); this skill is read-only.
metadata:
  author: Maestra.io
  upstream: AI tribe
---

# Flow summary

Turn the structure of one marketing scenario ("flow") into a short, human-readable
summary a marketer can grasp in seconds.

This skill is meant to run in a **subagent**: the calling agent hands you a flow
reference, you fetch and read the structure yourself, and you return **only** the
finished summary (markdown). You are the one who calls `flows_lookup` — do not
expect the structure to be pasted into your prompt.

How to read the flow tools' output is in `references/flows-tools.md`; where to look up what
a block / event / step means is in `references/flows-wiki.md`. Both describe *capabilities and
navigation* — the connected tools' live MCP schema is authoritative for exact signatures.
Refer to the flow tool by its capability handle (`flows_lookup`), not a project-specific id.

## CRITICAL — never fabricate

- **Describe only what the structure shows.** Never invent steps, channels, delays,
  or conditions that aren't in the fetched flow.
- **Never summarize a flow you couldn't load.** If the graph is empty or the fetch
  failed, stop and report it — a confident summary of nothing is the worst outcome
  for a skill whose whole value is trustworthy description. See `## If something goes wrong`.
- **Never surface internals** — block ids, `rowVersion`, or raw internal properties.

## Inputs

The caller gives you:

- `flowId` — the scenario id
- `versionNumber` — the scenario version to summarize
- (tenant/project is already set on the MCP connection)
- optionally, whether to include flow-run counts (see the optional step below)

If any of these is missing, ask the caller for it instead of guessing.

## Procedure

1. **Get the shape of the graph — cheaply first.**
   Fetch the *skeleton* view of the whole flow (cheap, structure-only). You get
   edge-strings like
   `B_f0a98df [conditionBlock "…"] B_f0a98df:positive --> B_9abcdef [delayBlock]`
   — the bracket tag is the block type, the quoted part its name, and the output name
   (`:positive`, `:beforeLimit`, `:1(75%)`, …) is used verbatim. Read the whole graph:
   the entry block, the branches, the merge points, and any **orphan branches** the
   FlowView reports separately.

   **Gate:** if the fetch failed or the graph is empty / has no entry block, **stop
   and report** (see below). Do not continue to a summary.

2. **Decode block / event / step meanings — from the flows wiki, not from memory.**
   The glossary is not bundled here; it lives in the flows wiki, **served by the `wiki` tool
   on the same MCP server as the flow tools** — that is the only route to it. Navigate it per
   `references/flows-wiki.md`: start at the domain index (the UI→technical term map), map each
   `flows_lookup` bracket tag to its `blocks` doc, and read `events` / `steps` docs as needed.
   Retrieval is navigate-only — there is no search — so take every id from the index you are
   standing on. If no `wiki` tool is connected, decode from the tag, the block name, and
   Full-view properties (step 3), and flag anything you genuinely cannot confirm (per the
   never-fabricate rule). Only look up what you need for this flow.

3. **Pull detail where it matters.**
   For the blocks that carry the meaning (triggers, communications, key conditions,
   delays), fetch *full* properties for those blocks and their neighbourhood (or the
   whole flow if it's small). You need actual names, event types, and channels — not
   internal ids.

4. **(Optional) Add flow-run counts — only if the caller wants a run-informed summary.**
   Re-fetch with executions included (see `references/flows-tools.md`). Use it to
   surface signals, not to pad: branches that never fired (an edge with no number),
   funnel-drop lines (`N in, M out — … stopped …`, always a finding), and executions
   stuck waiting. **Always state the counting window**, and note that counts only exist
   for roughly the **last 30 days** — older periods aren't persisted. Keep run figures
   in a separate note, distinct from the structural description.

5. **Check you have enough, then write.**
   Before writing, confirm you can name the trigger, the main communications, and the
   branching from real fetched data. If a meaningful block never resolved (neither the
   wiki nor Full-view properties explained it), say so in the summary rather than
   guessing. Then write the summary in the format below and return it.
   Nothing else.

## Output format

Always exactly these three sections, as markdown headings. **English is the
default**; write them in another language only when the user is working in one, and
then translate the headings too — the three sections and their order stay the same.

### Trigger
What launches the flow — the event or condition, plus any pre-launch checks
(subscriptions, recent communications, customer conditions) and trigger specifics.

### Flow logic
The sequence of actions — which communications go out (Email / SMS / Push), the
branching and conditions, delays between steps, fallback channels, and any
re-triggers.

### Goal
The business goal in 1–2 sentences — what it's trying to achieve, which problem it
solves, which metric it moves (conversion, retention, engagement).

## Rules

- **Structured**: use dash bullet lists for enumerations; never one wall of text.
- **Plain language**: avoid jargon where a plain word works.
- **Concrete**: rely on facts from the structure — real block names, event types,
  channels.
- **Business tone**: professional but not dry.
- **Confident**: no "probably" / "most likely" — state what the structure shows.
- **Orphans**: if the flow has orphan (disconnected) branches, say so plainly — it's
  usually a signal something is unfinished.

(The non-negotiable "never fabricate / never expose internals" rules are at the top
of this file.)

## If something goes wrong

Read-only skill, so blast radius is small — but a silent failure produces a
confident-but-wrong summary, which is worse than an error. Handle these:

| Situation | What to do |
|---|---|
| `flows_lookup` errors or times out | Retry once. If it still fails, stop and report the error to the caller — do not summarize. |
| Skeleton is empty / no entry block / flow or version not found | Stop and report: the flow/version couldn't be loaded (or doesn't exist). Never emit a summary of an empty graph. |
| Skeleton loaded but full detail for some blocks fails | Summarize what did load; explicitly note which part couldn't be read instead of inventing it. |
| A block type can't be resolved from the wiki or the flow | Describe the block by its type tag / name / position and state that its exact behaviour couldn't be confirmed — don't guess its semantics. |
| Run counts requested but the version didn't run in the window (`no recorded runs`, or all older than ~30 days) | Report there's no run data for the period; give the structural summary without invented figures. |
| Only orphan branches, no reachable flow from entry | Report that the flow appears unfinished/disconnected rather than forcing a three-section narrative. |

Worked examples of good summaries are in `references/examples.md`. Read it if you
need to calibrate tone and length.
