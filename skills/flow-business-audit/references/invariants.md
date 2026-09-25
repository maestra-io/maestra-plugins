# Invariants — what the tools return *successfully* that is not what it looks like

Every item here is a way a call succeeds and the reader is misled. None of them raises an error; each
one produces a number that is real, printable and wrong for the sentence it is about to appear in.
This is the file to re-read when a figure surprises you.

**Evidence markers.** `[measured]` — observed against a live project during this port, with what was
observed. `[schema]` — stated by the tool's own description in the connected MCP. `[structural]` —
follows from how the two reports are built, not from a single observation. `[upstream]` — observed
by the upstream team on the same mechanism and carried over with its expiry check, not re-measured
here.

## Contents

1. [The two reports overlap and cannot be summed](#1-the-two-reports-overlap-and-cannot-be-summed)
2. [`topN` silently caps the breakdown](#2-topn-silently-caps-the-breakdown)
3. [Absence is not zero](#3-absence-is-not-zero)
4. [A rate is not its counters divided](#4-a-rate-is-not-its-counters-divided)
5. [The `ScenarioClient*` metrics can be empty on a live project](#5-the-scenarioclient-metrics-can-be-empty-on-a-live-project)
6. [A wrong goal name errors; it does not fall back](#6-a-wrong-goal-name-errors-it-does-not-fall-back)
7. [An unknown channel returns an empty report, not an error](#7-an-unknown-channel-returns-an-empty-report-not-an-error)
8. [Names arrive clipped](#8-names-arrive-clipped)
9. [The newest days are a realtime tail, and attribution keeps arriving](#9-the-newest-days-are-a-realtime-tail-and-attribution-keeps-arriving)
10. [`flows_lookup` counters are a different window from every money figure](#10-flows_lookup-counters-are-a-different-window-from-every-money-figure)
11. [`email_health_report` measures a different population](#11-email_health_report-measures-a-different-population)
12. [A tool that is not available reads three different ways](#12-a-tool-that-is-not-available-reads-three-different-ways)
13. [Numbers from two different tools are not added together](#13-numbers-from-two-different-tools-are-not-added-together)
14. [The run-close date is a lower bound — the register of unreliable figures](#14-the-run-close-date-is-a-lower-bound--the-register-of-unreliable-figures)

---

## 1. The two reports overlap and cannot be summed

`[schema]` Both tool descriptions carry the same warning: a campaign sent by a flow is counted in
`flow_report` **and** in `campaign_report`. They are two views of partly shared data.

So: never add revenue, orders or sends across them; never present "flows earned X, campaigns earned
Y, together Z"; never reconcile one against the other by equality and treat a difference as an error.
Use flow grain for flow questions and mailing grain for mailing questions, and say which tool a
figure came from in the log.

## 2. `topN` silently caps the breakdown

`[schema]` `topN` defaults to **20** and maxes at **200**. `[measured]` A project returned
`## Flows (top 10 of 92 by Revenue)` — the header says M, and M was nine times the rows given.

A capped breakdown looks exactly like a complete one except for that header. **Read `top N of M`
every time**, and never let a capped answer become a statement about the project: "20 of 92" is not
"the project's flows". Above 200, cover the rest with `excludeFlowIds` or narrow by `folders` /
`brands` until every flow with rows has been seen, and record the coverage in the log.

The `## Summary` section is **not** capped — it covers every flow in the window. That is why a
Summary that disagrees with the sum of the visible rows is the cheapest cap detector there is.

## 3. Absence is not zero

`[structural]` A flow that sent nothing in the window has no row in the breakdown. It is not present
with zeros.

"Did not send in the period" is therefore established by **subtracting the breakdown from
`flows_list`**, never by reading a zero, and a flow missing from the breakdown is not missing from
the project. The inverse also holds: a row the flow list has no name for is a real flow with real
money — resolve it with `flows_get` rather than dropping it.

## 4. A rate is not its counters divided

`[structural]` Each rate's denominator is narrowed to the sends that can report its event; the
counters beside it on the same row are not narrowed.

`Opens / Sends` is not `OpenRate`. Ask for the rate you intend to print, and never reconstruct one
the call did not return. On a mixed-channel flow the returned rate is a blend across channels that
report the event and channels that cannot (`rates.md`).

## 5. The `ScenarioClient*` metrics can be empty on a live project

`[measured]` On a project with 92 flows and `ScenarioExecutionsCount: 253,800` in the window,
`ScenarioClientCount` came back **0** — in the same answer where revenue, orders, sends and every
rate were populated.

A zero there is a metric this project does not populate, **not a flow that reached nobody**. Check
`ScenarioClientCount` against `ScenarioExecutionsCount` before any sentence rests on the
per-customer family (`ScenarioClientRevenue`, `ScenarioClientOrders`, `ScenarioClientOrderRate`,
`ScenarioClientDeliveries`, `ScenarioClientAvgDeliveries`); when executions are non-zero and clients
are zero, declare the family unavailable once in `## What we do not know` and judge on the metrics
that are populated.

## 6. A wrong goal name errors; it does not fall back

`[measured]` A `flow_report` call identical to a working one except for `goalName="NoSuchGoalXYZ"`
returned `An error occurred. Please try again or ask support.` — the same opaque text a transport
failure produces. The identical call with `goalName` omitted succeeded.

So an opaque failure immediately after a goal name is introduced is **the goal, until proved
otherwise**. Re-run the call once with `goalName` omitted before spending a retry on the transport.
And because there is no goal catalogue to check a name against (`metrics-map.md`, T4), a name the
user supplies can only be tested by using it.

**One goal per figure.** A call counts money against exactly one goal, and two goals are never added
or set side by side as one series: the same order is attributed under each. A report that needs two
goals prints two figures, each with its goal named.

## 7. An unknown channel returns an empty report, not an error

`[schema]` Channel values are exact point-of-contact **system names, case-sensitive**; an
unrecognised one "returns an empty report rather than an error". The same is true of
`campaign_report`.

An empty answer after adding `channels` means the name is wrong far more often than it means the
flow is silent. Drop the filter, read the breakdown to see which channels the project actually uses,
and pin the correct spelling. Never report "no sends on SMS" from an empty filtered answer.

## 8. Names arrive clipped

`[measured]` Long names come back truncated with a trailing `..` — `[New] Abandoned Checkout, Email
#1 for RETURNING..`, `✅Monthly Impact Report | HAVEN'T pulled anything..` — in both reports.

A clipped name can match two different objects, which is how a mailing gets attributed to the wrong
flow (`beyond-the-overview.md`, T3f). Resolve every name that will appear in prose or in an overview
row: flows through `flows_list` / `flows_get`, mailings through `entities_list(entityType:
"Mailing")`. Never print a clipped name as if it were the name, and never match on one without
saying you did.

## 9. The newest days are a realtime tail, and attribution keeps arriving

`[structural]` Attributed revenue lands against a communication after the fact, so the last days of
any window are still filling, and a period that closed recently is still gaining money.

Two rules follow. **Audit closed periods** — the default period is the last closed calendar month.
And **a comparison against a period that closed less than the attribution window ago is a lower
bound**: a fall measured against it is «at most this much», said in those words
(`findings-and-failures.md`, "Compare like for like").

There is no call that reports how fresh the reporting data is — the recalculation-history handle of
earlier editions has no counterpart here (`metrics-map.md`, "Retired handles"). Say in the header
which period was audited and that its freshness could not be measured.

## 10. `flows_lookup` counters are a different window from every money figure

`[schema]` Execution counters exist for **roughly the last 30 days** and are then dropped. An earlier
`executionsSince` is not an error — the window is pulled forward to the boundary and the answer says
so.

So a flow's execution counts and its revenue in the audited month are two windows, and they are never
put in one sentence without both windows named. A month-long audit of a period more than 30 days back
gets **no** execution counters at all; that is a gap to name, not a zero to print.

## 11. `email_health_report` measures a different population

`[schema]` One brand, Email only, **non-transactional** Email only, over its own `windowDays` window
(default 30, counted back from today), across every mailing of that brand — flow-sent and manual
alike.

None of those four boundaries matches the audit's population. Its figures are never added to,
substituted for, or compared row-by-row with a `flow_report` rate. What it is for is the **band** —
the industry median and the target range — and the per-provider breakdown behind a bounce or spam
finding (`rates.md`).

## 12. A tool that is not available reads three different ways

They are fixed differently, and only one of them is a stop:

- **Not in your tool listing at all** — the connected server does not expose it. For a required tool
  this is the stop; for an optional one it is a line in `## What we do not know`.
- **In the listing but not yet loaded** — the schema has to be fetched before the tool can be called.
  This is **not** unavailability: load it and call it. A message about loading a tool is never a
  reason to stop.
- **Called and refused** — the call reached the server and came back with a refusal. Read the text
  after the colon: it decides between a retry and a stop
  (`findings-and-failures.md`, "If something goes wrong").

**Stop only on a refusal returned to a call you made yourself** to a required tool. A notice about
another MCP server, a subagent's silence, and your own failure to compose a call are none of them.

## 13. Numbers from two different tools are not added together

The general form of items 1 and 11, and the invariant this whole file exists to protect: **a figure
carries the population, the window and the tool that produced it, and only figures that share all
three may be combined.** A sum, a share, a delta or a ratio across two different measurements is not
a figure the audit may print — not even when both numbers are right.

Where the reader needs the two side by side, print them side by side, each with its own window and
scope in the reader's words (`SKILL.md`, rule 1), and say what the comparison can and cannot settle.

## 14. The run-close date is a lower bound — the register of unreliable figures

`[upstream]` The closing edge of a version's run in `flows_get` is set by the next history entry of
any version, whether or not that entry is a stop — so a version still executing can print a closed
range, and a printed close is a lower bound on when the version stopped, not the date it stopped
(`calling-the-tools.md`, "Version run timelines — observed behaviour", with the expiry check).

That date is the one figure in this audit's reach that is **quotable for nothing**: an established
cause never rests on it, when a scenario stopped is bounded by the last month with sends in the
reporting data instead, and whether it is running is read from the version statuses. The opening
edge of a run is sound and dates a change of version.
