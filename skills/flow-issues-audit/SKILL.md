---
name: flow-issues-audit
description: >-
  Technically audit a marketing scenario (flow): inspect its structure and flag
  known anti-patterns — processing-load and communication-correctness issues —
  each with a concrete fix and a short why. Use when asked to audit, review,
  health-check, or "find what's wrong / what to fix" in an existing flow, or across
  a whole project's flows. Don't use to summarize what a flow does (use flow-summary)
  or to create, edit, or launch a flow — this skill is read-only.
metadata:
  author: Maestra.io
  upstream: AI tribe
---

# Flow audit

Inspect one flow (or a project's flows) and report where it violates known
best-practices, with a concrete fix and a brief reason for each finding.

**Prefer to run this audit in a subagent** if you're orchestrating other work — delegate the whole
audit and surface only the short report. But you can't rely on it: a host may run this skill inline,
in which case your report goes straight to the user. **Either way the report must be user-ready on its
own** — concise and in plain business language (see `## Writing the report`). You fetch the structure
yourself with the flows tools — do not expect it to be pasted into your prompt.

Decode blocks from their type tag, name, and `detail=Full` properties. What the skill needs
from the flows tools — and how to read their output — is in `references/flows-tools.md`
(the tools themselves are authoritative for exact signatures); this file and the checklists
describe *capabilities*.

The anti-patterns themselves live in two checklist files, bundled with the skill — read the
one(s) you need on demand with `Read`:

- `references/checklist-per-flow.md` — checks for **one flow**. The default.
- `references/checklist-all-flows.md` — checks that only make sense across **all flows** of a project.
- `references/examples.md` — worked examples (clean **and** flawed real flows) calibrating what to flag
  and, crucially, what **not** to flag. Consult it whenever a call is borderline.
- `references/html-report-example.html` — the themed HTML report to reproduce **only when the user asks**
  for an HTML checklist (see `## Output format`).

## CRITICAL — never fabricate a finding

- **Report only anti-patterns you can substantiate from fetched data.** Tie each finding to a
  specific real block/edge in the fetched data (for your own rigor). Never invent a block, an edge, or a problem.
- **A false alarm on a healthy flow is as bad as a miss.** Reference flows must come back
  clean. If a check needs a block property you haven't fetched, fetch `detail=Full` for that
  block before deciding — don't guess, and don't flag on suspicion alone.
- **When structure isn't enough to confirm, say so.** Some checks (e.g. segment-is-recalculated,
  subscription topic/channel) may not be fully decidable from the flow alone. Mark those as
  "requires manual confirmation" rather than asserting a violation.
- **Never audit a flow you couldn't load.** And keep the report free of internals — no block ids,
  no `rowVersion`, no internal field/enum names (`entityType`, `entityDataPartType`,
  `sessionOrdersStatus`, block-type tags, …), no checklist numbers. Speak in user terms
  (see `## Writing the report`). See also `## If something goes wrong`.

## Prerequisites — check the tools first

Before anything else, confirm the flow tools you need are available in this session:
- a per-flow audit needs `flows_lookup`;
- a project-wide audit needs `flows_list`, `flows_get`, and `flows_lookup`.

No separate probe is needed — the first call you'd make anyway is the check: the skeleton fetch for a single
flow, or `flows_list` for a project. **If a required tool isn't available / the project's flow MCP isn't
connected** (distinct from a transient error — for that, retry once), **abort immediately. Do not run a partial
audit.** Tell the user plainly, in their language:
- the audit needs the project's flow tools (list flows / read a flow's structure / read version history) and they aren't connected here;
- they should connect the project's flow MCP (the one that exposes these tools) and re-run the audit;
- if they don't know how, point them to their team's instructions for connecting the flow MCP.

## Inputs

- Per-flow audit (default): `flowId` (int) and `versionNumber` (int). Tenant/project is set on
  the MCP connection.
- Project-wide audit: no specific flow — you enumerate flows yourself with `flows_list`.

If a per-flow audit is asked but `flowId`/`versionNumber` is missing, ask the caller instead of guessing.

## Which checklist

- Called on a **specific flow** → run `references/checklist-per-flow.md`. After reporting, **offer** to also
  run the project-wide checks ("some issues only show up across all flows — want me to run that too?").
- Asked to audit the **project / all flows** → run `references/checklist-all-flows.md`, and run the per-flow
  checklist on each flow you can (or on the ones the caller cares about).

## Procedure — per-flow

**First satisfy `## Prerequisites`** (the flow tools are available) — the step‑1 skeleton fetch below doubles as that check.

1. **Map the graph — cheaply first.** Fetch the skeleton of the whole flow
   (`detail=Skeleton, structure=Full`). Read the entry block, branches, merges, which outputs
   are dead-ends (no outgoing edge), and any orphan branches.

   **Gate:** if the fetch failed or the graph is empty / has no entry block, **stop and report**
   (see below). Do not produce an audit of nothing.

2. **Read `references/checklist-per-flow.md`.** It defines every anti-pattern (how-not / why /
   how-instead / how-to-check). Work through the checks.

3. **Pull `detail=Full` where a check needs block properties** — condition entity & subject,
   delay time-of-day strategy, operation-step channel/topic,
   segment vs realtime condition. Scope it (`structure=Subgraph`/`Neighbours` + `depth`) to the
   relevant blocks so a big flow stays cheap. Several skeleton-only checks (Split-for-A/B,
   only-narrowing condition, consecutive same-entity conditions, missing wait before a
   "not-done" check) need no Full fetch.

4. **(Optional) Corroborate with executions.** Re-fetch with executions when it strengthens a
   finding (a narrowing condition that drops everyone; an overheating flow). Always state the
   window; counts exist only for ~30 days. Never make it the sole basis of a structural finding.

5. **Assemble findings.** For each confirmed violation record: the anti-pattern, the exact
   block(s), why it's bad, and the fix — drawn from the checklist. Then write the report.

> These five steps are short and linear — no separate plan is needed for a normal flow. For a very
> large flow, keep a quick running list of which checklist cases you've applied vs still pending so
> you don't drop the tail.

## Procedure — all-flows

**First satisfy `## Prerequisites`** (the flow tools are available); the `flows_list` call below is that check.

Follow the ordered "how to check" steps inside `references/checklist-all-flows.md` (enumerate with
`flows_list`; read each flow as an entity with `flows_get` for its launch event and version history —
that drives both the merge-by-event and stale-test checks; use `flows_lookup` only for a flow's
longest-delay path).

**Scope by status when asked.** If the user wants only *running* (launched) flows audited, include only
flows whose status is `Execution` (running) — `flows_list` returns the status — and skip stopped/draft ones
(`Paused`, `Indevelopment`, …). Don't audit everything when the ask was "running flows".

**Track coverage — a project sweep must not silently go partial.** A project can have dozens of
flows, more than fit one context comfortably. Keep a running list of every flow from `flows_list`
with a status (audited / pending / skipped-and-why), work through it deliberately, and for very
large projects batch the flows (and respawn/continue if the context fills) rather than dropping
the tail. **Always state coverage in the report** — "audited N of M flows" — and list any flow you
could not reach, so an incomplete sweep never reads as complete.

## Output format

Write the report in **the language the user is working in** (it reaches the user directly), following
`## Writing the report`, and cover **only** what the user should act on.

**Two kinds of finding — keep them distinct:**
- **Problems** (firm): split used instead of an A/B test; customer- vs session-scope in "abandoned" mechanics;
  missing subscription/validity check for the channel; night sends; stale test versions; many flows on one event.
  Present these as "what to fix".
- **Suggestions** (advisory trade-offs): audience-filter placement and condition-block granularity. Present
  these **softly** as optional "could be improved (a load-vs-clarity trade-off)", clearly
  **not** problems. If the only findings are advisory, say the flow is basically fine and list them as optional.

**Per-flow report:**
- **No problems and no suggestions → one short line**, e.g. "No issues found — the flow looks correct."
- **Otherwise** → a short verdict line, then one short block per finding: **what** (plain words); **where** (block
  by its name in quotes, or a plain role/position description — never an id); **fix** (concrete, with a brief note
  of why it matters). Problems first, then any suggestions clearly labelled as optional.
- Only if you couldn't confirm something from the structure: one line on what to check manually.
- Close with a one-line offer to also run the project-wide checks.

**Project-wide report:** lead with the concrete scenarios, ordered by priority — a **table**:

| Flow | Problems | What to do | Priority |
|---|---|---|---|
| [name](link) | short list | short list | High / Med / Low |

Each scenario name is a **link** (see below). Order rows by priority (most impactful first); keep cells short;
state coverage ("audited N of M flows"). Keep advisory suggestions out of the "Problems" column — put them in
"What to do" as optional, or in a lower-priority note. Write the table in English unless the user is working in
another language; then translate the headers with it.

**Scenario links:** build as `<base_project_url>/scenarios/<flowId>` — e.g.
`https://acme.maestra.io/scenarios/269446`. The `<base_project_url>` is the project's admin URL; if you
don't know it, ask the user once (or reuse a scenario URL they gave you) and apply the same base to every link.

**HTML checklist — offer, never auto-build.** At the end, always **offer** to assemble a presentation-ready HTML
version of the report ("want an HTML checklist you can open in a browser and show the client?"). Build it **only on
request**, and reproduce `references/html-report-example.html`: its structure and visual theme are the product's
design — **keep the colors, fonts, radii and layout exactly as they are**, change only the content (project name,
scenarios, ids, links, findings). It's a self-contained `.html` (inline CSS; the product web-font is loaded by URL
with a local fallback) — the prioritized linked table plus a per-scenario card breakdown (problems / optional
suggestions / manual-check), each with a checkbox to tick off.

Most impactful first. No raw JSON, no skeletons, no "everything else is fine" section.

## Writing the report — talk to the user, not the system

The reader is a marketer/CSM who has never seen the flow's internals. Translate everything into their world:

- **No system terms.** Never name internal fields or enum values (`sessionOrdersStatus: Absent`,
  `entityDataPartType: Customer`, `entityType: User`, `filterFactory`, `conditionBlock`, …). Say what it
  *means*: not "set `sessionOrdersStatus: Absent`" but "make the trigger fire only when the session ended
  without an order"; not "the condition is on `entityType: User`" but "the condition looks at the customer
  overall instead of the session that just ended".
- **No block ids.** Refer to a block by its **name in quotes** if it has one (the «Welcome» email step);
  otherwise **describe it** by role/position — "the start (trigger) block", "the 30-minute wait",
  "the third condition in the chain", "the email-send step group".
- **No checklist numbers.** Never write "case 6" or "check №2 — ok". The user never sees the checklist.
- **Only actionable things.** If an aspect is fine, don't mention it — no reassurance, no "and this is
  correct" notes. Say only what to change and, briefly, why it matters (deliverability, wasted processing
  load, distorted test results, night sends, …).
- **Short.** A clean flow is one line. Two issues are two short blocks, not two screens.

## Rules (quick reference)

- Never fabricate; when unsure, say what to check manually — see `## CRITICAL — never fabricate a finding`.
- Report only what the user should act on, in plain user terms — see `## Writing the report`.

## If something goes wrong

Read-only skill, so blast radius is small — but a wrong finding erodes trust in the whole audit.

| Situation | What to do |
|---|---|
| A required flow tool isn't available / the flow MCP isn't connected | Abort per `## Prerequisites` — tell the user to connect the project's flow MCP and re-run; never run a partial audit. |
| `flows_lookup` / `flows_list` errors or times out | Retry once. If it still fails, stop and report the error — don't audit partial data as if complete. |
| Skeleton empty / no entry block / flow or version not found | Stop and report: the flow/version couldn't be loaded (or doesn't exist). Never audit an empty graph. |
| A check needs block properties the Full fetch didn't return | Report that check as "requires manual confirmation", naming what's missing — don't flag or clear it on a guess. |
| Executions requested but no run data in the window (or older than ~30 days) | Skip the run-based corroboration; keep the structural findings without invented figures. |
