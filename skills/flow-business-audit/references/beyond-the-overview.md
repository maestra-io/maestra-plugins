# Beyond the overview — a second window, and one flow at a time

The overview in `metrics-map.md` answers one window for every flow. This file answers what needs
something else: **the same period a year earlier** — T10, with T11 guarding it against a flow that
kept its id and changed its mechanic — and **one flow at a time**, T3f for what that flow's mailings
contributed and T5 for whether the flow is in the reporting data at all.

All four are `flow_report` or `campaign_report` calls with particular arguments. The metric
vocabulary, the `topN` rule and the clipping caveat are in `metrics-map.md` and
`calling-the-tools.md`; they apply here unchanged.

## Contents

1. [T10 — the same period a year earlier](#t10--the-same-period-a-year-earlier) — adds to the period-over-period comparison, never replaces it
2. [T11 — is the flow still the same mechanic?](#t11--is-the-flow-still-the-same-mechanic) — the reused-id trap
3. [T3f — what each mailing inside one flow contributed](#t3f--what-each-mailing-inside-one-flow-contributed)
4. [T5 — is this flow in the reporting data at all](#t5--is-this-flow-in-the-reporting-data-at-all)

---

## T10 — the same period a year earlier

The year-on-year overview: the T1 call run a second time over the same calendar period twelve months
back. **It adds to the period-over-period comparison and never replaces it** — month against the
previous month answers "what changed recently", month against the same month a year earlier answers
"is this month normal for this season", and a project with a season answers those two questions
differently. A report carrying only one of them is answering half the question it was asked.

```
flow_report(
  tenant    = <project>,
  startDate = <audited period start minus one year>,
  endDate   = <audited period end minus one year>,
  metrics   = <the same list, in the same order, as the T1 call>,
  topN      = 200,
  mode      = "Full"
)
```

**Three properties of running it as a second call, all of which must reach the report.**

**The two windows are two answers, and the pairing is yours.** Nothing returns both windows on one
row any more. You match the audited window's rows to the year-ago window's **by flow id**, and every
delta is arithmetic you do and record. Keep both raw figures in the log beside the delta; a delta
whose two sides cannot be found in the log is not finished (`findings-and-failures.md`, "The handover
check").

**Three populations, not one.** A flow may have rows in both windows, in the audited window only, or
in the year-ago window only. **Only the first group gets a delta.** The other two are counts, and
the year-on-year section carries them in words: how many flows are in both windows, how many are new
since, how many stopped. **The year-on-year section is in every report** — the figures where there
are pairs, and those counts where there are none.

**A flow absent a year ago has no delta, and "new" is not a verdict.** It means this flow did not
send in that window; whether it existed, was paused, or was built since is a question for
`flows_list` and `flows_get`, not an inference from its absence.

Rates year on year are the same call's rate columns (`rates.md`); the project's own year-ago line is
that answer's `## Summary`.

**A delta is never printed alone** — beside it goes the flow's own level, T1m over the twelve closed
months (`metrics-map.md`). Audited month at or above the level → a year-on-year fall is «can't
judge», both printed. Year-ago month above the level → the fall is measured from a peak; rest the
verdict on the level.

---

## T11 — is the flow still the same mechanic?

A flow id outlives the flow's content. The same id can carry a welcome series this year and a
win-back last year, and a year-on-year delta across that change compares two different mechanics
while looking exactly like a performance movement. **T11 is the guard, and its result gates whether
T10's delta may be printed as a result at all.**

There is no single call that scores the overlap. The guard is assembled, cheapest first, and **the
report says which level answered it**:

1. **The flow's versions.** `flows_get` by id returns the flow's versions with their statuses.
   A version created between the two windows is the signal that something changed; the same version
   running across both is the strongest available evidence that nothing did.
2. **The mailings it sends.** T3f (below) run over each window returns the automatic mailings active
   in it. A flow whose send steps carry the same mailing names in both windows is the same mechanic
   for this purpose; a disjoint set is a different one.
3. **The construction.** Only for a flow whose delta is about to carry a verdict and whose first two
   levels disagree: read the start block and the send steps (`structural-causes.md`) and say what the
   flow does now.

**Anything short of "the same mechanic in both windows" prints the delta with a warning, never as a
result** — the same rule as in earlier editions. Where none of the three levels could be reached
inside the budget, the delta is printed as «can't judge», with the continuity unverified, and the
row says so.

---

## T3f — what each mailing inside one flow contributed

`flow_report` stops at the flow. To see which send inside it earned and which did not, the grain
comes from the other report:

```
campaign_report(
  tenant         = <project>,
  startDate      = <period start>,
  endDate        = <period end>,
  activationType = "Automatic",
  mode           = "Detailed"
)
```

One row per mailing — `Revenue`, `Orders`, `Sent`, and the `Open% / Click% / Conv% / Unsub% / Spam% /
Bounce%` rates — for every automatic mailing in the window, ordered by revenue. `Manual` is the
regular-campaign half and is not this skill's subject; omitting `activationType` mixes both.

**Matching rows to a flow is by name, and the match is yours to make and to state.** The breakdown
carries mailing names, not flow ids. Read the flow's send steps with `flows_lookup(detail="Full")`,
take the mailing each step sends, and match those names to the rows. **Say in the report that the
attribution of mailings to this flow was made by name**, and name any send step whose mailing did not
appear in the breakdown (it sent nothing in the window) and any mailing you could not confidently
place.

**Two traps the matching walks into:**

- **Names are clipped with `..` in the breakdown** (`calling-the-tools.md`). A truncated name can
  match two send steps. Where it does, resolve the full name through `entities_list(entityType:
  "Mailing")` before deciding, or leave the row unplaced and say so.
- **A mailing can be sent by more than one flow.** Nothing in the row says which flow sent it. A
  mailing whose name appears on send steps of two flows is not evidence for either; exclude it from
  the per-flow sum and name it.

**T3f's sum is not checked against that flow's T1 row by equality.** The two come from reports that
overlap by construction and are computed over different grains (`metrics-map.md`, "Two reports that
must never be added together"). Use T3f to see **which send inside the flow carries the flow's
result** — the ranking, not the total. Where the shape it shows contradicts the flow's own row, that
is a finding about the matching, not about the flow.

---

## T5 — is this flow in the reporting data at all

The cheap probe behind "this flow has no rows — is it silent, or is it absent?"

```
flow_report(
  tenant         = <project>,
  startDate      = <a wide window: two years back, or the project's whole life>,
  endDate        = <today>,
  metrics        = "Sends,Revenue",
  includeFlowIds = [<flowId>],
  mode           = "Full"
)
```

Rows in the wide window and none in the audited one → **the flow has run and is silent now**: a
finding, with the last window it did send named. No rows in the wide window either → **the flow has
never sent**, which is a fact about the flow, not a data gap.

Neither answer says *why*, and the difference matters to the reader. Pair it with
`flows_lookup(includeExecutions=true)` — its ≈30-day counters say whether people are still entering
the flow and where they stop (`SKILL.md` step 5, "Silent but still taking people in"). **A flow
taking people in and delivering nothing is the expensive case** and keeps a row: «can't judge», the
execution count with its window, and the probe.
