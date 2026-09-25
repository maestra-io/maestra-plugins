---
name: flow-issues-audit
description: >-
  Technically audit a marketing scenario (flow): inspect its structure and flag
  known anti-patterns — processing-load and communication-correctness issues —
  each with a concrete fix and a short why. Use when asked to audit, review,
  health-check, or "find what's wrong / what to fix" in an existing flow, or across
  a whole project's flows. Don't use to summarize what a flow does (use flow-summary)
  or to create, edit, or launch a flow (use flow-create) — this skill is read-only.
metadata:
  author: Maestra.io
  upstream: AI tribe
  version: 1.0.0
---

# Flow audit

If you delegate this audit, hand the sub-agent: this file's path, the flow reference
(`flowId` + `versionNumber`, or "project-wide"), the project's admin base URL, the language to
write in, and the report shape from `## Output format`.

The report may go straight to the user — always write it per `## Writing the report`. Fetch the
structure yourself with the flows tools; do not expect it to be pasted into your prompt.

Read on demand, with `Read`:

- `references/checklist-per-flow.md` — the anti-patterns for **one flow**. The default.
- `references/checklist-all-flows.md` — checks that only make sense across **all flows** of a project.
- `references/<locale>/examples.md` — worked examples (clean **and** flawed real flows) calibrating what to flag
  and, crucially, what **not** to flag. Consult it whenever a call is borderline.
- `references/<locale>/terminology.md` — the table headers, priority labels and fixed phrases the report prints.
- `references/<locale>/html-report-example.html` — the themed HTML report, reproduced only on request.

`<locale>` is `en-US` or `ru-RU` — pick the one matching the user's language; if their language has
no variant, use `en-US` and translate the wording yourself.

## Where to look

- **Read the connected tool's schema before building a call; it wins over anything written here.**
- **The wiki wins on meanings** — what a block type does, what a status means, what an output name
  denotes, what a trigger event fires on. It is served by the **`wiki` tool** on the same MCP server
  as the flow tools and is the only route to it. Take every id from the index you are standing on or
  from a document's `# References` list; never assemble one yourself.

For an audit the documents worth opening are `overview` (how a flow runs, dead ends, what counts as
a run, ordering and load, and the flow-level settings), the domain index and `blocks` (block types
and their outputs), `events` and `steps` (the trigger and operation-step catalogues), `flow_types`
(which recipient checks a flow applies by itself and which have to be written into it) and `urls`
(the address of a flow version, and the flow status vocabulary). The `entities` domain resolves a
name you may need to print — a segment, a mailing — into the identifier that names it. Read only
what this audit needs.

**A missing `wiki` tool is not a stop** — this skill is read-only and its checks work off the
structure. Decode from the tag, the block name and the full properties instead, and mark whatever
you cannot confirm as needing manual confirmation.

## CRITICAL — never fabricate a finding

- **Report only anti-patterns you can substantiate from fetched data.** Tie each finding to a
  specific real block/edge in the fetched data (for your own rigor). Never invent a block, an edge, or a problem.
- **A false alarm on a healthy flow is as bad as a miss.** Reference flows must come back
  clean. If a check needs a block property you haven't fetched, fetch that block's full properties
  before deciding — don't guess, and don't flag on suspicion alone.
- **A check you can't decide from the fetched data is "requires manual confirmation"** — never a
  violation, and never a clean bill either.
- **Never audit a flow you couldn't load.** See also `## If something goes wrong`.

## Prerequisites — check the tools first

- a per-flow audit needs `flows_lookup`;
- a project-wide audit needs `flows_list`, `flows_get`, and `flows_lookup`.

Your first call doubles as the check. If a required tool is missing (as opposed to erroring — for
that, retry once), abort; never run a partial audit. Tell the user, in their language, that the
project's flow MCP isn't connected here, and to connect it and re-run the audit.

## Inputs

- Per-flow audit (default): `flowId` (int) and `versionNumber` (int). The project is fixed by the
  MCP connection.

If a per-flow audit is asked but `flowId`/`versionNumber` is missing, ask the caller instead of guessing.

## Which checklist

- Called on a **specific flow** → run `references/checklist-per-flow.md`. After reporting, **offer** to also
  run the project-wide checks (`terminology.md` → `offer.allFlows`).
- Asked to audit the **project / all flows** → run `references/checklist-all-flows.md`, and run the per-flow
  checklist on each flow you can (or on the ones the caller cares about).

## Procedure — per-flow

1. **Map the graph — cheaply first.** Fetch the skeleton view of the whole flow, the cheap
   properties-free one. Read the entry block, branches, merges, which outputs are dead-ends (no
   outgoing edge), and any orphan branches.

2. **Read `references/checklist-per-flow.md`.** It defines every anti-pattern (how-not / why /
   how-instead / how-to-check). Work through the checks.

3. **Pull full properties where a check needs them** — condition entity & subject, delay
   time-of-day strategy, operation-step channel/topic, segment vs realtime condition, and the
   flow-level `repeatSettings`. Bound the traversal to the relevant blocks (a subtree or a
   neighbourhood at a small depth) so a big flow stays cheap. Several skeleton-only checks
   (Split-for-A/B, only-narrowing condition, consecutive same-entity conditions, missing wait before
   a "not-done" check) need no full fetch.

4. **(Optional) Corroborate with executions.** Re-fetch with execution counts when they strengthen
   a finding (a narrowing condition that drops everyone; an overheating flow), and state the window
   you counted. Never make counts the sole basis of a structural finding.

5. **Assemble findings.** For each confirmed violation record: the anti-pattern, the exact
   block(s), why it's bad, and the fix — drawn from the checklist. Then write the report.

> On a very large flow, track which cases you've applied and which are still pending.

## Procedure — all-flows

Follow the ordered steps in `references/checklist-all-flows.md`.

**Scope by status when asked.** If the user wants only *running* (launched) flows audited, keep the
flows the listing reports as running and skip the stopped and draft ones. The listing tool has no
status parameter, so filter its rows yourself; take the exact status spelling from the listing tool's
own description or from the wiki document `urls` — a status you invent silently matches nothing.

**Batch the sweep and keep the findings on disk** — a project can have dozens of flows, more than fit
one context.

1. From `flows_list`, write a findings file in the working directory (or another path the host
   allows) holding every flow in scope with its state: audited / pending / skipped-and-why, and
   update it after every batch, before starting the next one.
2. Audit the flows in batches. Where the host offers sub-agents, run one sub-agent per batch, briefed
   as at the top of this file, each returning its per-flow findings in the shape `## Output format`
   defines. Merge the returned findings yourself.
3. Read the file back before writing the report, and build the report from it rather than from
   memory.

**Always state coverage in the report** — `terminology.md` → `coverage` — and list any flow you could
not reach, so an incomplete sweep never reads as complete.

## Output format

Take table headers, priority labels and fixed phrases from `references/<locale>/terminology.md`.
Sample outputs: `references/<locale>/examples.md`.

**Two kinds of finding — keep them distinct:**
- **Problems** (firm): split used instead of an A/B test; customer- vs session-scope in "abandoned" mechanics;
  missing subscription/validity check for the channel; night sends; stale test versions; many flows on one event.
  Present these as "what to fix".
- **Suggestions** (advisory trade-offs): audience-filter placement and condition-block granularity. Present
  these **softly** as optional "could be improved (a load-vs-clarity trade-off)", clearly
  **not** problems. If the only findings are advisory, say the flow is basically fine and list them as optional.

**Per-flow report:**
- **No problems and no suggestions → one short line** (`terminology.md` → `verdict.clean`).
- **Otherwise** → a short verdict line, then one short block per finding: **what** (plain words); **where** (block
  by its name in quotes, or a plain role/position description — never an id); **fix** (concrete, with a brief note
  of why it matters). Problems first, then any suggestions clearly labelled as optional. Two issues
  are two short blocks, not two screens.

**Project-wide report:** lead with the concrete scenarios, ordered by priority — a **table**:

| Scenario | Problems | What to do | Priority |
|---|---|---|---|
| [name](link) | short list | short list | High / Med / Low |

Order rows by priority (most impactful first), keep cells short, and keep advisory items out of the
"Problems" column — put them in "What to do" as optional.

**Scenario links:** a flow's address is the project's admin base URL plus the path the wiki document
`urls` prints — build the link from that document, which also says which version each form of the
link opens. No flow tool returns the base URL, but on this platform it is
`https://<system name>.maestra.io`, the system name being the `tenant` every tool takes as
`tenants_list` prints it: build the base from that, say so in the report, and ask the user once only
when the project answers on another address (or reuse a scenario URL they gave you). Apply the same
base to every link.

**HTML checklist.** Offer an HTML version at the end (`terminology.md` → `offer.html`); build it only
on request. Reproduce `references/<locale>/html-report-example.html`, replacing only the data — keep
its structure and visual theme exactly as they are.

## Writing the report — talk to the user, not the system

The reader is a marketer who has never seen the flow's internals — translate everything into their world.

- **No system terms.** Never print a field name, an enum value or a block type tag — none of the
  vocabulary the flow tools and the wiki speak. Say what it *means* instead: not the name of the
  trigger's order-state setting and the value to put in it, but "make the trigger fire only when the
  session ended without an order"; not the technical name of the condition's entity context, but "the
  condition looks at the customer overall instead of the session that just ended".
- **No block ids.** Refer to a block by its **name in quotes** if it has one (the "Welcome" email step);
  otherwise **describe it** by role/position — "the start (trigger) block", "the 30-minute wait",
  "the third condition in the chain", "the email-send step group".
- **No checklist numbers.** Never write "case 6" or "check №2 — ok". The user never sees the checklist.
- **No internals.** No block ids, no optimistic-lock token, no raw JSON, no skeletons, no
  "everything else is fine" section. If an aspect is fine, don't mention it.

## If something goes wrong

| Situation | What to do |
|---|---|
| A required flow tool isn't available / the flow MCP isn't connected | Abort per `## Prerequisites` — tell the user to connect the project's flow MCP and re-run; never run a partial audit. |
| `flows_lookup` / `flows_list` errors or times out | Retry once. If it still fails, stop and report the error — don't audit partial data as if complete. |
| Skeleton empty / no entry block / flow or version not found | Stop and report: the flow/version couldn't be loaded (or doesn't exist). Never audit an empty graph. |
| A check needs block properties the Full fetch didn't return | Report that check as "requires manual confirmation", naming what's missing — don't flag or clear it on a guess. |
| Executions requested but no run data in the window (or the period predates what the counters retain) | Skip the run-based corroboration; keep the structural findings without invented figures. |
