# Calling the tools — arguments, answers, and failures dressed as successes

What each call takes, how much of an answer arrives, and how to tell a call that worked from a call
that returned something.

**The live tool schema is authoritative for every signature here.** This file records the arguments
the audit uses and the behaviours worth knowing before the first call; where it disagrees with the
schema in your tool listing, the schema wins and the disagreement goes in the run log.

**Tools are named by capability handle** — `flow_report`, `flows_list`, `flows_lookup`, `flows_get`,
`campaign_report`, `email_health_report`, `entities_list`, `tenants_list`, `wiki`. The connected MCP
prefixes them, and a multi-tenant connection takes `tenant` on **every** call. Never carry a full
tool id or a frozen signature from this document into a call.

## Contents

1. [`tenant` — the argument every call takes](#tenant--the-argument-every-call-takes)
2. [`flow_report` — call arguments](#flow_report--call-arguments)
3. [`campaign_report` — call arguments](#campaign_report--call-arguments)
4. [Call arguments: `flows_list`, `flows_get`, `flows_lookup`](#call-arguments-flows_list-flows_get-flows_lookup)
5. [`email_health_report`, `entities_list`, `wiki`](#email_health_report-entities_list-wiki)
6. [Failures dressed as successes](#failures-dressed-as-successes)
7. [The retry budget](#the-retry-budget)
8. [Version run timelines — observed behaviour](#version-run-timelines--observed-behaviour)

---

## `tenant` — the argument every call takes

On a multi-tenant connection, every tool requires the project's exact **system name**, spelled as
`tenants_list` prints it. It is never guessed and never derived from the name the user used: run
`tenants_list` once, match, and confirm the match with the user before the first figure is fetched
(`SKILL.md`, "Inputs"). A wrong-but-existing tenant produces a complete, plausible audit of the
wrong project — the worst failure this skill can have.

On a single-project connection there is nothing to resolve and nothing to ask.

## `flow_report` — call arguments

| Argument | What it does | What the audit passes |
|---|---|---|
| `tenant` | project system name | always |
| `startDate` / `endDate` | window, ISO 8601 | always, explicitly — the defaults (3 months back to today) are never what an audit means |
| `metrics` | comma-separated metric names; **the first is the sort key** | the overview list (`metrics-map.md`); never a name not on the vocabulary list |
| `topN` | rows in the breakdown, default 20, **max 200** | `200` on the overview; see invariant 2 |
| `mode` | `Overview` (summary only) / `Detailed` (breakdown only) / `Full` | `Full` — the audit needs both sections |
| `timelineBucket` | `Day` / `Week` / `Month` — adds a timeline section | `Month` for T1m; omitted otherwise |
| `goalName` | which goal money is counted against | only when the user named one; see invariant 6 |
| `includeFlowIds` / `excludeFlowIds` | pin to, or exclude, flow ids | `includeFlowIds` for T1m and T5; `excludeFlowIds` to page past 200 |
| `flowNameContains` | substring match on the name | only when the id is not yet known — it can match several flows |
| `brands`, `channels`, `folders` | narrow the population | only when a verdict needs one channel or one brand; named in the report when used |
| `activeOnly` | drop flows not currently running | **off** — a flow paused mid-period still earned what it earned |
| `startedInPeriodOnly` | only flows that first ran in the window | off, unless the question is about newly launched flows |
| `reason` | free-form note on why this call | fill it — it is what makes the run log readable |

The answer's first line echoes the window and the goal (`Period: … | Goal: …`) and a `Filters:` line
appears when any narrowing was used. **Both lines go in the log with the figures** — they are the
passport every number is printed with.

## `campaign_report` — call arguments

Same window, mode, goal, brand and channel arguments. Its own two:

- `activationType` — `Automatic` (triggered, i.e. sent by flows) or `Manual` (regular campaigns);
  omitted mixes both. The audit passes `Automatic` for T3f.
- `groupByFolder` — folder-grain instead of per-campaign.

The breakdown **paginates up to 200 items** and its header reports the total and whether the list is
capped, exactly as `flow_report`'s does.

## Call arguments: `flows_list`, `flows_get`, `flows_lookup`

**`flows_list`** — id, name, active version number and status, sorted by id, paginated (`page`,
`pageSize`, default 50, max 200). **Read it to the last page**; the count is what this account can
see, and folder-level access control is applied server-side, so report the number with the tool
beside it. There is no search by name or description. Upstream measured a page size above the
ceiling as **clamped, not refused** — the answer comes back short inside a successful reply — so
the page header, not the row count, says whether the list is finished. **The pages are a cost line
of their own** in the log: how many there are is the size of the project, not the depth of the audit.

**`flows_get`** — one flow by id, with its versions and their statuses. Three uses: resolving a name
the breakdown clipped, resolving an id that appears in a report and not in the list, and reading
**whether a scenario is running**. That last reading is made from the **set of version statuses** in
the versions block — a scenario is running when **any** of its versions carries a running status —
never from the `active version` line (it is not necessarily the newest version, and it can be empty
without the scenario having stopped) and never from send dates. Which values mean running is the
live `flows_list` schema's (`Execution` and `Testing` today; `Paused`, `InDevelopment`,
`ReadyForExecution` and the like are not running); what each status means is the wiki's (`urls`).
Two readings the audit adds: **match a status ignoring case** — the same value reaches you as the
wire string or as a flattened enum name depending on the call; and **an unrecognised status value is
*not established*, never "not running"**. When a scenario stopped is bounded by the last month with
sends in the reporting data, not by the version timeline ("Version run timelines" below).

**`flows_lookup`** — the structure of one flow version. The arguments that matter to this audit:

- `flowId` + `versionNumber` — both required, and **the version number has no default. This is the
  one home of that choice**; every step that needs a version points here. Its source is the active
  version column of `flows_list`. For a paused flow, or a window in which an older version was live,
  the source is `flows_get`: the version whose run overlaps the audited window. That overlap is read
  off the run-close date, which is a lower bound ("Version run timelines" below), so it can find no
  overlapping version for a scenario that demonstrably ran; the fallback is then the active version
  from `flows_list`, **with which one was used said out loud**, and it is never presented as the
  version that was live in the window. Ask the user only when neither answers.
- `detail` — `Skeleton` (arrow lines, the navigation map — **start here**) or `Full` (JSON with each
  block's resolved properties, plus the flow's own `settings`: `repeatSettings` and
  `launchSettings`).
- `structure` — `Full` (whole graph), `Subgraph` (downstream from a block), `Neighbours` (both
  directions), with `depth` in hops. **`detail="Full"` over a large graph is heavy** — prefer a
  subgraph around the blocks the figure pointed at.
- `includeExecutions` + `executionsSince` / `executionsTill` — per-output execution counters, stops
  with reasons, and executions still waiting. **Counters exist for roughly the last 30 days only**
  (invariant 10). It costs a second upstream call and means nothing for a flow that has not run.

The `rowVersion` token in the answer is an optimistic-concurrency marker for writes. This skill never
writes, and **the token is never surfaced to the reader**.

## `email_health_report`, `entities_list`, `wiki`

**`email_health_report`** — `brand` is **required** (name or system name, case-insensitive; an
unknown one comes back with the list of brands). `windowDays` 1–60, default 30 —
leave it at 30, which is what the bands are calibrated against. `includeInboxProviders=true` adds
the per-receiving-domain breakdown. Population caveats: invariant 11.

**`entities_list`** — one entity kind per call (`entityType`), `query` to search or omitted for the
whole catalogue, paginated by a `cursor` printed at the end of an answer while rows remain. The audit
uses it for `Brand`, `Folder` and `Mailing`. The answer is a tab-separated table whose header names
its columns — read the column you need off the answer rather than assuming it. **There is no goal
kind in its enumeration** (`metrics-map.md`, T4).

**`wiki`** — `domain="Flows"`, `id` as a list of up to 5 document ids. Ids come from the domain index
or from the links inside a document already read; **never assemble one from a block tag**. What the
audit reads, and when, is the table in `SKILL.md`.

## Failures dressed as successes

The ones that return a well-formed answer and mislead:

| What arrived | What it usually means | What to do |
|---|---|---|
| A breakdown that looks complete | `top N of M` with M above N — capped | Raise `topN`, or page with `excludeFlowIds` (invariant 2) |
| An empty report after a `channels` filter | the channel name is wrong or wrongly cased | Drop the filter, read the channels in use, re-pin (invariant 7) |
| A flow missing from the breakdown | it sent nothing in the window | Subtract from `flows_list`; do not read it as zero (invariant 3) |
| `ScenarioClientCount: 0` beside non-zero executions | the project does not populate the family | Declare it unavailable; do not report "reached nobody" (invariant 5) |
| A name ending in `..` | clipped, and possibly ambiguous | Resolve before printing or matching (invariant 8) |
| A rate that looks impossible (100%, 0%) | a denominator under the floor | «can't judge» — never a finding (`rates.md`) |
| A `## Summary` that disagrees with the sum of the rows | the breakdown is capped, or a filter narrowed one side | Check the header and the `Filters:` line before suspecting the data |

And the one that returns an error and is not a transport problem: **`An error occurred. Please try
again or ask support.` right after a `goalName` was introduced is the goal** (invariant 6). Re-run
once without it before spending a retry.

## The retry budget

**Two retries on an opaque failure, then stop for that figure.** A third attempt at an identical call
is spending the run, not recovering it. On a required tool that means stopping the audit with no
figure printed and the reason in the header; on an optional one it means a line in
`## What we do not know` and the audit goes on.

Before either retry, **change something or confirm nothing needs changing**: the goal check above,
the `channels` spelling, a narrower window, a smaller `topN`. A retry of a call known to be malformed
is not a retry.

**Every call goes in the log — the ones that failed too**, with the arguments, the answer or the
error text, and what was concluded. The log exists before the first call and is appended as the run
goes (`SKILL.md`, "The run has two outputs").

## Version run timelines — observed behaviour

> Observed upstream on the same version-history mechanism, kept because it is expected to be fixed.
> **Expiry, checkable from inside this skill:** take a flow whose status is the running one and
> which has rows in the reporting data this month, and call `flows_get` on it. If its last run entry
> is still open (`ran: <date> - now`), this entry is stale for that flow; if the entry below still
> reproduces on a flow like it, it is current. Measured on this platform 2026-09-24: running
> versions with no later history entry printed open-ended runs (`ran: <date> - now`), which is
> consistent with the entry; the closed-range case was not reproduced, so re-check it on a flow
> with several versions before resting anything on it.

Each version line carries the period it ran, open-ended for a run that is still open. **A printed
closing edge — the run-close date — is a lower bound on when the version stopped, not the date it
stopped.** A run is closed by the next history entry of any version, and an entry that is not a stop
closes it just the same, so a version that is still executing can print a closed range ending on the
day it started. The run-close date is therefore in the register of unreliable figures
(`invariants.md`, 14) and is quotable for nothing.

**The opening edge is sound**: a run opens on the history entry that puts *that* version into
execution, so the start of the run is the date this version took over — the date to use when the
question is when a scenario changed. The creation date is not: upstream measured a version created
two months before it first ran, so the creation date is a last-resort fallback and the gap is said
out loud. Where the history is empty or does not come back, the change cannot be dated at all: that
is a line in `## What we do not know`, not a silent substitution of the creation date.
