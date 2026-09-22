# Flows tools — what this skill needs

This skill reads a scenario through the project's flow tools (MCP tools in a session).
**The tools themselves (their MCP schema) are the source of truth for exact signatures.**
This file describes only what the summary needs from them: the capability it uses, the
fields it reads, and how to parse the output. If a parameter or response shape changes,
defer to the tool's current schema, not to this file.

> **Naming / portability:** the short name `flows_lookup` used throughout this skill is a
> stable *capability handle*. What varies per project is the **full tool id** (the connected
> MCP prefixes it, e.g. `mcp__<project>__flows_lookup`) and the **exact parameter
> signatures**, which defer to the live tool schema. Refer to the connected tool by
> capability; don't hardcode a full, project-specific id or a frozen signature.

## Read one flow's structure

The summary reads a flow's structure by its id and version number. The tool exposes it on
two independent axes plus a way to bound the traversal:

- **Skeleton** — blocks as arrow-strings, no properties: the navigation map of the graph.
  **Start here.**
- **Full block properties** — resolved per block: filter/condition bodies, trigger event,
  operation steps (**channel** and message), delay strategy, split / A-B data, schedule.
  Full properties for the whole graph are expensive.
- **Bounded traversal** — whole graph / subtree downstream from a block / neighbours (down
  and up) to a given depth — so a large flow isn't pulled in full. Use it to fetch full
  detail only for the blocks that carry the meaning.
- **Optional execution counts** for a period (see below).

The response also carries a row-version token (**never surface it**) and — for the whole
graph — the list of **orphan branches** (blocks with no incoming edge other than the start
block).

## How to read the skeleton

Current shape of skeleton lines (real capture; flow id scrambled):

```
B_f0a98df [inboundEventBlock "Customer subscribed to Email"] B_f0a98df:default --> B_1c80f93 [operationStepsBlockSettings "Welcome - greeting email"]
B_5519993 [limitationBlock] B_5519993:beforeLimit --> B_147bb5f [operationStepsBlockSettings "Welcome sms - promo code still valid"]
B_5519993 [limitationBlock] B_5519993:afterLimit --> B_627f6f4 [operationStepsBlockSettings "Welcome email - promo code still valid"]
```

- The block's short stable id is `B_xxxxxxx`.
- The block type is the **bracket tag**: `inboundEventBlock`, `scheduleBlock`,
  `operationStepsBlockSettings`, `delayBlock`, `conditionBlock`, `limitationBlock`,
  `abTestBlock`, `splitBlock`, … An optional human name follows in quotes. To decode a tag
  into plain language, see `references/flows-wiki.md`.
- Output names are used verbatim: `:default`, `:positive`, `:negative`, `:beforeLimit`,
  `:afterLimit`, `:1(75%)` (A-B variant + share). **An output with no outgoing edge means
  executions on that output leave the flow.**

## Execution counts (optional, last ~30 days only)

Counters are kept for roughly the **last month** and then dropped — longer periods aren't
persisted. Asking for an earlier start is not an error; the window is clamped to what exists
and the response says so. It's a second upstream request — only meaningful for a flow that
actually ran. When requested, the response adds:

- A **header** with the counted window and when this version actually ran, e.g.
  `executions counted 2026-08-08 - 2026-08-10 | version 1 ran: 2026-08-06 - now` — so counts
  are never quoted without their window.
- A **count per output** as a trailing `(N)` on the edge. **An edge with no number means zero
  executions took it in the window** (real capture; flow id scrambled):
  ```
  B_3fd3570 [inboundEventBlock] B_3fd3570:default --> B_f2dd430 [conditionBlock]  (89)
  B_f2dd430 [conditionBlock] B_f2dd430:positive --> B_bbe315c [operationStepsBlockSettings "Steps 2"]
  ```
  (89 entered and passed to the condition; the `:positive` edge has no number → 0 reached
  "Steps 2" in the window.)
- A **funnel line for any block that lost executions between in and out** — **always a finding**
  (a block that passed everything through gets no such line):
  ```
  B_107f0df [scheduleBlock]: 785475 in, 292650 out — 492825 stopped (AncientMessageThresholdViolation 492824, 492824 unique; EntityIsNotFound 1, 1 unique)
  ```
  plus, where present, executions still waiting in a block and executions currently processing.

For a **summary**, execution counts are corroborating colour, not the point — fold them in
only when the caller asks for a run-informed summary, and always state the window.
