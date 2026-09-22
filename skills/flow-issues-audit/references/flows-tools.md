# Flows tools — what this skill needs

This skill reads scenarios through the project's flow tools (MCP tools in a session).
**The tools themselves (their MCP schema) are the source of truth for exact signatures.** This
file describes only what the audit needs from them: the capabilities it uses, the fields it reads,
and how to parse the output. If a parameter or response shape changes, defer to the tool's current
schema, not to this file.

> **Naming / portability:** the short names used throughout this skill — `flows_list`, `flows_get`,
> `flows_lookup` — are stable *capability handles*. What varies per project is the **full tool id** (the
> connected MCP prefixes it, e.g. `mcp__<project>__flows_lookup`) and the **exact parameter signatures**,
> which defer to the live tool schema. Refer to the connected tools by capability; don't hardcode a
> full, project-specific id or a frozen signature.

## List a project's flows

The audit needs to enumerate a project's flows (paginated). The list returns, per flow: numeric id, name,
current version number, and **status**. Status `Execution` means the flow is currently **running (launched)**;
other statuses (`Paused`, `Indevelopment`, …) mean it is not. Use the status when the user asks to audit only
the running flows, so you don't audit stopped or draft ones.

## Read a flow as an entity (version history + launch condition)

For the project-wide checks the audit needs to read a flow *as an entity* by its id: its brand/folder,
its current active version, its **launch condition** (which trigger event, or a schedule), a **flag for
platform-detected issues**, and — key — the **full list of versions**, each with its status (draft / ready /
testing / …), who created it and when, and an **activity timeline** (when that version actually ran, or that
it never ran). This is one call per flow and is the efficient way to get the launch event and the testing
history without walking the graph — it drives both the "many flows on one event" and "stale test version"
checks in `checklist-all-flows.md`.

## Read one flow's structure

The audit needs to read a flow's structure by id and version number — in two levels of detail, and
with a way to bound the traversal:

- **Skeleton** — blocks as arrow-strings, no properties: the navigation map of the graph (start here).
- **Full block properties** — filter/condition bodies (including the condition's **entity** and
  **subject**), trigger events, operation steps (**channel** and message **topic**), delay strategies
  (including the **send-time-of-day window**), split / A-B test data, schedules.
- **Bounded traversal** — whole graph / subtree downstream from a block / neighbours (down and up) to a
  given depth, so a large flow isn't pulled in full (full properties for the whole graph are expensive).
- **Optional execution counts** for a period (available for roughly the last month): how many runs took
  each output, how many stopped in a block and why. For the audit this is only corroborating signal
  (e.g. a condition that drops everyone), never the sole basis for a structural finding.

The response also carries a row-version token (never surface it) and — for the whole graph — the list of
orphan branches (blocks with no incoming edge other than the start block).

> **Not in the structure:** the start block's "runs-per-customer / trigger limit" settings are not
> returned — you cannot tell from the structure whether an entry-frequency limit is set. Do not infer
> its absence (this is why that check is not performed).

## How to read the skeleton

Current shape of skeleton lines:

```
B_f0a98df [inboundEventBlock "Customer subscribed to mailings"] B_f0a98df:default --> B_1c80f93 [operationStepsBlockSettings "Welcome"]
B_5519993 [limitationBlock] B_5519993:beforeLimit --> B_147bb5f [operationStepsBlockSettings "…"]
```

- The block's short stable id is `B_xxxxxxx`.
- The block type is the bracket tag: `inboundEventBlock`, `scheduleBlock`, `operationStepsBlockSettings`,
  `delayBlock`, `conditionBlock`, `limitationBlock`, `abTestBlock`, `splitBlock`, … An optional human
  name follows in quotes.
- Output names are used verbatim: `:default`, `:positive`, `:negative`, `:beforeLimit`, `:afterLimit`,
  `:1(75%)` (A-B variant + share). **An output with no outgoing edge means clients on that output leave
  the flow** — key for the "condition only narrows" check.
