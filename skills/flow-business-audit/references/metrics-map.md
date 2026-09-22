# Metrics map — which audit question is answered by which call

Every number in a business audit comes from the project's **reporting tools** — `flow_report` for
the scenarios, `campaign_report` for the mailings inside them, `email_health_report` for the
deliverability benchmark. There is no SQL in this skill and no datamart to query: the platform
computes these figures the same way the Scenarios screen does, so a figure printed here and a figure
the reader sees in the admin UI are the same figure.

That is the whole shape of the change from earlier editions, and it collapses most of the old work.
**One `flow_report` call answers money, volume, funnel and every rate, for every flow and for the
project, over one window.** The handles below are still numbered the way the rest of this skill
refers to them (T1, T1m, T2 …), but a handle is now a *call with particular arguments*, not a query
to copy. Copy the arguments; never invent a metric name.

**The live tool schema is authoritative.** The metric list, the argument names and the defaults
below were captured against a working project, but a tool can gain a metric or change a default.
Read the schema in your tool listing; where it disagrees with this file, the schema wins and the
disagreement goes in the run log.

## Contents

1. [The map](#the-map) — which audit question is answered by which call
2. [The metric vocabulary](#the-metric-vocabulary) — every metric name the report accepts
3. [T1 / T1p / T2 / T2p / T8 — the overview, in one call](#t1--t1p--t2--t2p--t8--the-overview-in-one-call)
4. [T1m — one flow's twelve months, one row per month](#t1m--one-flows-twelve-months-one-row-per-month)
5. [T1t — the transactional share](#t1t--the-transactional-share) — what replaced the by-mailing-type row
6. [T4 — which goal is being counted](#t4--which-goal-is-being-counted)
7. [Retired handles](#retired-handles) — T6, T7, T9, and why nothing replaces them

The other two files beside this one:

- `rates.md` — which rate decides what, the denominators behind them, the floors, and the one
  benchmark the platform brings (`email_health_report`).
- `beyond-the-overview.md` — **T10** (the same period a year earlier) with its continuity guard
  **T11**, and the one-flow templates **T3f** and **T5**.
- `calling-the-tools.md` — the transport: arguments, paging, clipping, and what a failure looks
  like when it arrives dressed as a success.

---

## The map

| Audit question | What answers it | Which call |
|---|---|---|
| Which flows exist, what are they called, what is their status | flow list, paginated | `flows_list` |
| A single id the flow list does not contain, or a name clipped with `..` | flow entity, name included | `flows_get` by id |
| How much did each flow bring in, how much did it send, and at what rates | one row per flow: money, volume, funnel counters and every rate | `flow_report`, **T1 / T2 / T8** — the same call |
| How much did the project's scenarios bring in as a whole, at what rates | the `## Summary` section of that same answer | `flow_report`, **T1p / T2p** — no extra call |
| Whether the audited month is normal for this flow | that flow's closed months, one row per month | `flow_report` + `timelineBucket="Month"`, **T1m** |
| What share of the project's scenario revenue stands on transactional sends | the flows whose sends are transactional, identified from their construction | `flows_lookup` + wiki `flow_types`, **T1t** |
| Which mailing inside a flow contributed what | the per-campaign breakdown of automatic mailings, matched to the flow's send steps | `campaign_report`, **T3f** (`beyond-the-overview.md`) |
| Which goal is being counted | the report header names it | `flow_report` header, **T4** |
| Is this flow in the reporting data at all, ever | presence probe over a wide window | `flow_report` + `includeFlowIds`, **T5** (`beyond-the-overview.md`) |
| Period over period | the overview run twice, over two comparable closed periods | `flow_report` once per period; the delta is arithmetic, no tool computes it |
| The same period a year earlier | the same, with the year-ago dates | **T10** (`beyond-the-overview.md`) |
| Whether a year-on-year row compares one mechanic or two | whether the flow sent the same set of mailings in both windows | **T11** (`beyond-the-overview.md`) |
| Where inside the graph people are lost | branch outputs, stops with reasons, waits | `flows_lookup(includeExecutions=true)` — **window ≈ 30 days** |
| Email thresholds and the industry benchmark | one brand's **non-transactional Email over its own window** — a different population from every handle above | `email_health_report` (`rates.md`) |
| Resolving a brand or a folder from a name | id lookup | `entities_list` |

**Two reports that must never be added together.** `flow_report` and `campaign_report` are two views
of partly the same sends: a mailing sent by a flow is counted in both. Their tool descriptions say so
outright. Use one per question — flow-grain from `flow_report`, mailing-grain from `campaign_report`
— and never sum revenue, orders or sends across them. A total that mixes them is wrong by an amount
nothing in the run can measure.

---

## The metric vocabulary

`metrics` is a comma-separated list; **the first metric is the sort key** of the breakdown. Asking
for a name that is not on this list is an error, not a silently dropped column.

**Money and volume** — `Revenue`, `Orders`, `AverageOrderValue`, `ConversionsRevenue`,
`ConversionRevenuePerRecipient`, `Sends`, `InQueue`, `Deliveries`, `Opens`, `Clicks`, `Conversions`.

**Rates** — `DeliveryRate`, `OpenRate`, `ClickRate`, `ConversionRate`, `CTOR`, `UnsubscribeRate`,
`Unsubscribes`, `SpamRate`, `SpamCount`, `BounceRate`, `BouncesCount`.

**Per-execution and per-customer** — `ScenarioExecutionsCount`, `ScenarioClientCount`,
`ScenarioClientDeliveries`, `ScenarioClientOrderRate`, `ScenarioClientOrders`,
`ScenarioClientRevenue`, `ScenarioClientAvgDeliveries`.

> **The `ScenarioClient*` family can come back as zeros on a project where the rest of the report is
> full.** It was measured at `ScenarioClientCount: 0` against a live project with 92 flows and
> 253,800 executions in the window. **A zero there is not a finding** — it is a metric this project
> does not populate. Check it against `ScenarioExecutionsCount` before any sentence rests on it; if
> executions are non-zero and clients are zero, the per-customer figures are unavailable for this
> project and that goes in `## What we do not know`, not into a verdict.

---

## T1 / T1p / T2 / T2p / T8 — the overview, in one call

Everything the overview step needs, for every flow and for the project, over one window.

```
flow_report(
  tenant     = <project system name>,
  startDate  = <period start, ISO>,
  endDate    = <period end, ISO>,
  metrics    = "Revenue,Orders,Sends,Deliveries,Opens,Clicks,Conversions,
                OpenRate,ClickRate,ConversionRate,UnsubscribeRate,SpamRate,BounceRate,
                AverageOrderValue,ScenarioExecutionsCount",
  topN       = 200,
  mode       = "Full"
)
```

The answer has two sections and they are two different handles:

- **`## Summary`** — one figure per metric over every flow in the window. This is **T1p** for the
  money and volume lines and **T2p** for the rate lines. It costs no extra call and it is the level
  a verdict falls back to when no single flow clears the materiality floor (`SKILL.md` step 5).
- **`## Flows (top N of M by <sort metric>)`** — one row per flow. Money and volume columns are
  **T1**; `OpenRate` / `ClickRate` / `UnsubscribeRate` are **T2**; `BounceRate` / `SpamRate` are
  **T8**. There is no join to get wrong and no grain to choose: the platform has already decided
  what a flow's row means.

**`topN` decides your coverage, and the default hides it.** The default is 20 and the maximum is
200. The header prints `top N of M` — **read M every time**. If M is above the rows you were given,
the audit has not seen the project: raise `topN`, and if M is above 200, run again with
`excludeFlowIds` carrying the ids already covered, or narrow by `folders` or `brands`, until every
flow with rows has been seen. **Never classify a project from a capped breakdown**, and never let
"top 20 of 92" become "the project has 20 active flows".

**Only flows with rows in the window appear.** A flow that sent nothing is absent from the
breakdown, not present with zeros. That absence is what step 4 means by "did not send in the period";
it is established by subtracting this breakdown from `flows_list`, never by reading a zero.

**Useful narrowings**, all optional and all named in the answer's `Filters:` line when used:
`brands`, `channels` (exact point-of-contact system names, case-sensitive — an unknown one returns
an empty report rather than an error), `folders`, `includeFlowIds` / `excludeFlowIds`,
`flowNameContains`, `activeOnly`, `startedInPeriodOnly`.

**`activeOnly=true` is not the audit's default.** A flow paused mid-period still earned what it
earned, and dropping it silently rewrites the period's money. Leave it off; read status from
`flows_list` instead and say in the row that the flow is paused.

---

## T1m — one flow's twelve months, one row per month

The level a year-on-year delta is stated beside: is the audited month normal *for this flow*, or is
one end of the comparison the outlier?

```
flow_report(
  tenant         = <project>,
  startDate      = <first day of the month twelve months back>,
  endDate        = <last day of the last closed month>,
  metrics        = "Revenue,Orders,Sends,Deliveries,ConversionRate",
  includeFlowIds = [<flowId>],
  timelineBucket = "Month",
  mode           = "Full"
)
```

The `## Timeline (month)` section is the series, one row per month, `startDate` naming the bucket.
`## Summary` is the twelve-month total for that flow, and the one-row `## Flows` section confirms the
pin landed on the flow you meant.

**Pin by id, not by name.** `includeFlowIds` names one flow exactly; `flowNameContains` is a
substring match that will happily return three flows and a total across them. Use the name filter
only when the id is not yet known, and check the `## Flows` section says `top 1 of 1`.

**Read the shape, not the average.** Twelve months exist so a fall can be told from a season, a
launch or a single burst month. A series with one month carrying most of the year is not a level to
compare against — say so and rest the verdict elsewhere (`findings-and-failures.md`, "against an
unexamined base").

---

## T1t — the transactional share

Earlier editions read the project's revenue split by mailing type straight from a datamart column.
**`flow_report` has no mailing-type dimension, and nothing else exposes that split**, so the question
is answered from construction instead of from a column, and the answer is coarser. Say which it was.

Per flow, at level 1 of the construction reading (`structural-causes.md`): read the send steps with
`flows_lookup(detail="Full")` and the wiki's `flow_types` document, which is what settles whether a
flow's sends run on a transactional mailing profile. A flow whose sends are all transactional
**gets no money verdict and is not in the money ranking** — its row keeps its revenue with the words
«revenue on a confirmation message follows the order, not the message» (`business-rules.md`, "What is
never judged on money"). A mixed flow is ranked with that caveat on its line.

**The project-level finding survives, as a supposition.** If transactional flows carry meaningful
attributed revenue, that is still the sign that a service message is intercepting the order from the
marketing message that earned it. Print it in «the project as a whole» with the sum and the share
**computed from those flows' own rows**, marked as a supposition with its probe — «supposed: the
exclusion from attribution is not configured for these mailings; what would settle it: the project's
attribution-exclusion list» — and the step it implies, with the caveat that until then every money
figure in the report is shifted by an unknown share.

**What is lost, and must be said once in `## What we do not know`:** the share is computed over the
flows whose construction the run read, not over every mailing in the project. Transactional sends
inside flows the budget did not open, and transactional mailings sent outside any flow, are not in
it.

---

## T4 — which goal is being counted

The report counts money against one goal, and **every answer's header names the one it used** —
`Period: … | Goal: Default`. That header line is T4: print the goal by that name in the report, every
time, beside the money.

`goalName` picks a different goal (case-insensitive, e.g. `"Orders"`); omitted or empty means the
project's default goal, which prints as `Goal: Default`.

**A goal name the project does not have returns an error, not a fallback.** Measured: a
`flow_report` call identical but for `goalName="NoSuchGoalXYZ"` came back `An error occurred. Please
try again or ask support.` — the same opaque text a transport failure uses. So when a call fails
immediately after a goal name was introduced, **suspect the goal before suspecting the transport**:
re-run the identical call with `goalName` omitted, and if that succeeds the name was wrong. Say so to
the user, name the goal that was actually counted, and never let a wrong goal name pass as a project
with no data.

**There is no goal catalogue.** `entities_list` has no goal kind in its `entityType` enumeration, and
no tool lists the project's goals with their revenue. Earlier editions printed every goal with its
revenue; this one cannot. When the user names no goal, the default goal is used, the header's name
for it is printed, and the report says in one line that the alternatives were not enumerable —
a fact for `## What we do not know`, not a stop.

---

## Retired handles

Three handles from earlier editions have no counterpart here and **nothing replaces them**. They are
listed so a reader who knows the older skill is not left looking.

- **T6 — do money and funnel cover the same flows.** It existed because money and funnel lived in
  two tables that could disagree. One tool now returns both on the same row, so the gap it measured
  cannot occur. Do not print a coverage figure for it.
- **T7 — how far the datamart has been recalculated.** There is no datamart and no recalculation
  history to read. What survives is the underlying caution, and it belongs in the header: **the
  newest days of any window are a realtime tail**, and **attributed revenue keeps arriving after the
  period closes**, so a period that closed less than the attribution window ago is a lower bound and
  a fall measured against it is «at most this much» (`findings-and-failures.md`, "Compare like for
  like"). Audit closed periods; say in the header which period was audited and that the freshness of
  the reporting data could not be measured.
- **T9 — the shadow check against the wide mart.** Retired upstream with the mart itself.

The self-consistency check earlier editions opened with is likewise gone, and what replaces it is
cheap and worth doing: **the `## Summary` of the overview call and the sum of its `## Flows` rows
should agree** when the breakdown is not capped. They are computed by the same tool over the same
window, so a disagreement means the breakdown is capped (check `top N of M`) or a filter is narrowing
one and not the other. Record the check in the log either way.
