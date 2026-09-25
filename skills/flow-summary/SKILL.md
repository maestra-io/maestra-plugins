---
name: flow-summary
description: >-
  Produce a concise, structured business summary of a marketing
  scenario (flow) from its structure. Use when you need to understand or
  explain what an existing flow does — before adapting it, editing it, auditing
  it, or reporting to a user, and on requests like "what does this flow do",
  "summarize the scenario" or "explain this flow". Reads the flow with the
  project's flow tools and looks up block / event / step meanings in the flows
  wiki. Don't use to audit a flow for problems (use flow-issues-audit) or to
  create, edit, or launch a flow (use flow-create); this skill is read-only.
metadata:
  author: Maestra.io
  upstream: AI tribe
  version: 1.0.0
---

# Flow summary

Turn one flow's structure into a short summary a marketer can grasp in seconds.

This skill is meant to run in a **subagent**: the calling agent hands you a flow
reference, you fetch and read the structure yourself, and you return **only** the
finished summary (markdown), or the short error contract in `## Inputs` when you
cannot produce one.

Reading the tools' output: `references/flows-tools.md`. Decoding block / event / step
meanings: `references/flows-wiki.md`. Refer to tools by name (`flows_lookup`, `wiki`),
never by a project-prefixed id.

## CRITICAL — never fabricate

- **Describe only what the structure shows.** Never invent steps, channels, delays,
  or conditions that aren't in the fetched flow.
- **Never summarize a flow you couldn't load.** Empty graph or failed fetch → stop and
  report (`## If something goes wrong`).
- **Never surface internals** — block ids, the optimistic-lock token, or raw internal
  properties and their technical names.

## Inputs

The caller gives you:

- `flowId` — the scenario id
- `versionNumber` — the scenario version to summarize
- (the project is fixed by the MCP connection)
- optionally, whether to include flow-run counts (see the optional step below)

Missing input → return the error block below, don't ask: as a sub-agent you have no one
to ask.

```
Cannot summarize.
Missing: <the input, or the thing that would not load>
Tried: <the calls you made before stopping, and how they ended>
```

Use the same three lines whenever the procedure stops early (see `## If something goes wrong`).

## Procedure

Only `flows_lookup` returns the graph — the flow listing and the read of a flow as an
entity carry none.

1. **Get the shape of the graph — cheaply first.**
   Start with the skeleton of the whole flow: the entry block, the branches, the merges,
   and the orphan branches the response lists separately.

   **Gate:** if the fetch failed or the graph is empty / has no entry block, **stop
   and report** (see below). Do not continue to a summary.

2. **Decode block / event / step meanings — from the flows wiki, not from memory.**
   Call `wiki` with the flows domain and no id for the index, then read the documents it
   names. Details in `references/flows-wiki.md`.

3. **Pull detail where it matters.**
   Fetch full properties for the blocks that carry the meaning — trigger, sends, key
   conditions, delays — where the real names, event types and channels live.

4. **(Optional) Add flow-run counts — only if the caller wants a run-informed summary.**
   Re-read with execution counts. Report branches that never fired, blocks that lost
   executions, and executions still waiting — always with the counting window, in a note
   kept separate from the structural description.

5. **Check you have enough, then write.**
   Before writing, confirm you can name the trigger, the main sends and the branching from
   fetched data. Flag any block you could not resolve. Then write the summary below —
   nothing else.

## Output format

Always exactly these three sections, as markdown headings, in this order:

### Trigger
What launches the flow — the event or condition, plus any pre-launch checks
(subscriptions, recent communications, customer conditions) and trigger specifics.

### Flow logic
The sequence of actions — which communications go out and on the channel the step names
(email, SMS, push, messenger and so on, as the reference lists them), the branching and
conditions, delays between steps, fallback channels, and any re-triggers.

### Goal
The business goal in 1–2 sentences — what it's trying to achieve, which problem it
solves, which metric it moves (conversion, retention, engagement).

Write in the user's language; headings and labels from `references/<locale>/terminology.md`
(en-US, ru-RU — otherwise en-US, translated). Examples: `references/<locale>/examples.md`.

## Rules

- **Structured**: use dash bullet lists for enumerations; never one wall of text.
- **Plain language**: avoid jargon where a plain word works.
- **Business tone**: professional but not dry.
- **Confident**: no "probably" / "most likely" — state what the structure shows.
- **Orphans**: if the flow has orphan (disconnected) branches, say so plainly — it's
  usually a signal something is unfinished.

## If something goes wrong

Where a row says **stop**, return the three-line error from `## Inputs` as your whole
answer.

| Situation | What to do |
|---|---|
| `flows_lookup` errors or times out | Retry once. If it still fails, stop — do not summarize. |
| Skeleton is empty / no entry block / flow or version not found | Stop: the flow/version couldn't be loaded (or doesn't exist). Never emit a summary of an empty graph. |
| Skeleton loaded but full detail for some blocks fails | Summarize what did load; explicitly note which part couldn't be read instead of inventing it. |
| A block type can't be resolved from the wiki or the flow | Describe the block by its type tag / name / position and state that its exact behaviour couldn't be confirmed — don't guess its semantics. |
| Run counts requested but there were no runs in the window, or the period predates the counters | Say there's no run data for the period and give the structural summary, without invented figures. |
| Only orphan branches, no reachable flow from entry | Report that the flow appears unfinished/disconnected rather than forcing a three-section narrative. |
