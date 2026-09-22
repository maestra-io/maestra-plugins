---
name: flow-business-audit
description: >-
  Business audit of a project's marketing flows that ends in fixes to the flows
  themselves. First the figures — revenue, orders, funnel and rates per flow over
  the period, against the month before and the same month a year earlier — to find
  the flows with a problem and the ones that work best; then, only for those, the
  construction (start block, conditions, sends, repeat settings) to name the
  block, setting or action that would fix it, or the approach worth copying. Two
  report forms, chosen at the start: the full report, or a client-ready deck of
  proposals with a note for the CSM. Use when the question is about business
  results, in any language: "which flows earn and which don't", "audit the
  project's flows on money", "what did the flows bring in for the month", or one
  named flow's money. Answers in the language asked. Don't use to check one flow's
  structure with no figures (flow-issues-audit), to summarize what a flow does
  (flow-summary), or to create or edit anything — read-only.
metadata:
  author: Maestra.io
  upstream: AI tribe
  version: 7.0.0
---

# Flow business audit

Answer, for a project, **which scenarios work on money and which do not — and what in the scenario
would fix the ones that do not**. Every number carries the window and the origin that produced it,
every fix names a block or a setting by its name, and everything that could not be computed or read
is said out loud.

**Reporting data gives the size of a movement; the scenario's construction gives its mechanism. A
cause is established when the run holds both.** The order is fixed: the figures find the scenarios
worth opening, the construction says why they move and what to change. On a project with hundreds
of scenarios the construction is read for a handful — the ones the figures single out — never for
all of them.

**Prefer to run this audit in a subagent** if you're orchestrating other work. A subagent does not
inherit this skill: name it in the brief (`maestra:flow-business-audit`), tell it to read `SKILL.md` and
the reference files itself, and give it the project, the period and the goal. A host may also run
this skill inline. Either way the report must be user-ready on its own (`writing-the-report.md`),
and you fetch every figure yourself.

**Read with `Read` before the first call:**

- `references/metrics-map.md` — which audit question is answered by which call, the metric
  vocabulary, and the **call arguments verbatim**. Copy the arguments; never invent a metric name.
- `references/rates.md` — which rate decides what, the denominators behind them, the floors, and the
  one industry benchmark the platform brings.
- `references/beyond-the-overview.md` — the year-ago calls and the per-flow ones.
- `references/invariants.md` — what the tools return *successfully* that is not what it looks
  like.
- `references/findings-and-failures.md` — the interpretation traps, the triage table for a failing
  call, the handover check, how an empty value is printed, and the reader's vocabulary.
- `references/calling-the-tools.md` — what each call takes, and what a failure dressed as a success
  looks like.
- `references/business-rules.md` — the rules of marketing judgement: which metric a scenario of a
  given kind is judged by, what is never judged on money, thresholds, decomposition, what a
  recommendation must contain and what is never recommended.
- `references/structural-causes.md` — how a scenario's construction is read behind a figure (three
  levels, cheapest first, and the budget), and the catalogue symptom → where to look → what is
  usually there → the shape of the fix.

**Read later, at the step that names them:** `references/writing-the-report.md` once, when the
report is begun; `references/html-report-example.html` only if the full page is asked for;
`references/html-client-deck-example.html` only when the report form is the client deck.

Tools are named by **capability handle** (`flow_report`, `flows_list`, `wiki`, …). The
connected MCP prefixes them, a multi-tenant endpoint also takes `tenant` on every call, and **the
live tool schema is authoritative for signatures** — never a call form remembered from a document
or an earlier run.

## CRITICAL — four rules that outrank everything below

1. **Never print a number without its passport — in the reader's words.** Every figure carries,
   where it is printed, the window it covers and what measured it, said in words the reader has —
   never a template handle, a tool name or a column name. Which call produced it stays in the run
   log. A number no call of this run returned does not go in the report, not as an estimate.
2. **Never invent a finding.** A false alarm on a healthy flow is as bad as a miss. A finding names
   the observation, the window and the comparison it rests on; where the data supports two
   readings, «can't judge, and here is what would settle it» is a legitimate verdict. What this
   forbids is a finding with no figure behind it — never a supposition that says it is one and names
   its probe (`## From "what" to "why"`).
3. **Never run a partial audit silently, and never write.** Either the audit is complete for what it
   claims to cover, or the gap is named — in the header for a stop, in `## What we do not know` for
   anything that failed along the way. Read-only: never `flows_apply_operations`, `flows_create`,
   `flows_set_testing_mode` or any other writing tool.
4. **A scenario is not taken through in full until it has been read, and no fix names a place the
   run did not see.** Every scenario that gets a full block in the report, and every scenario on a
   deck slide, has had its construction read — the start block, the conditions on the way to a
   send, the send steps, the repeat settings (`structural-causes.md`, levels 1 and 2 at least) — and
   its block's «What is in the scenario» part names at least one block. **Every step in «What to
   do» names a place and an action** — a block, a setting, a condition or a data source by name,
   and a verb that can be carried out; a step naming only an area to search is a question, and
   questions live in the cause part as probes. A scenario the figures flagged as «problem» whose
   construction the budget did not reach **keeps its verdict by the figures**, goes to the hypothesis
   table with the words «construction not read» on its row, gets no full block, no step inside the
   scenario and no slide (`writing-the-report.md`, the frame, item 5). Project-level findings have
   no single construction and are outside this rule.

## Prerequisites — the tools, checked by using them

**Required** — without any one of these the audit does not start: `flow_report`, `flows_list`,
`flows_get`, `flows_lookup`. `flow_report` is where every figure in the report comes from; the last
is required because rule 4 cannot be kept without it.

**Optional enrichment** — absence never stops the audit and is named in `## What we do not know`:
`wiki` (domain `Flows` — what a construction means), `campaign_report` (what each mailing inside a
flow contributed), `email_health_report` (the industry benchmark), `entities_list`, `tenants_list`
(multi-tenant connections, to resolve the project name).

**Not used by this edition.** `analytics_execute_query` / `analytics_get_schema` are the freehand
datamart tools; earlier editions of this skill ran on them. The marts they served are not part of
this platform's catalogue, so **this skill writes no SQL**. If a project's catalogue does expose
scenario-grain marts, that is a reason to extend this skill deliberately, not to improvise a query
mid-audit: a hand-written figure beside a platform-computed one is the thing invariant 13 forbids.

**What `wiki` is for, and when.** It explains what the run sees in a construction; nothing in the
report stands on it alone (`structural-causes.md`, "What the wiki adds").

| Document | When | What it settles |
|---|---|---|
| `flow_types` | before the money ranking (step 4) | the mailing profile — which sends are transactional and what that does to attribution |
| `overview` | before the first construction reading | what an execution is; what the repeat limit counts |
| `blocks.<block>` (the id from the index's term map, e.g. `blocks.condition`) | while reading a specific block | what a setting seen in its properties means |
| `mechanics.<mechanic>.overview` / `.structure`, `mechanics.best_practices` | when a scenario is recognisable as a known mechanic | what the mechanic is for and how that is usually achieved — a source of hypotheses about what is missing, **not a standard the scenario is validated against** |

No separate probe: the first calls of the procedure are the check. A refusal arrives wrapped in
the same prefix as a transport error — read the text after the colon; it decides between a retry and
a stop (`findings-and-failures.md`, "If something goes wrong"). **Stop only on a refusal returned to
a call you made yourself** to a required tool: a notice about another MCP server, a tool that has to
be loaded before it can be called, a subagent's silence and your own failure to compose a call are
none of them. A missing required tool reads three ways and they are fixed differently
(`invariants.md`, "A tool that is not available reads three different ways"); on a required tool stop
and print no figure; on an optional one continue and record the loss.

## Where a figure comes from

Every number in this report is **computed by the platform**, not by this skill: `flow_report` is the
same computation behind the project's Scenarios screen, so a figure printed here and a figure the
reader opens in the admin UI are the same figure. That is the one real advantage of this edition over
the hand-written queries it replaces, and it is worth saying to the reader once.

What that costs is freehand: there is no column to reach past a metric the tool does not expose. When
a question has no metric behind it, the honest answer is that it could not be measured — never a
figure assembled from two others. The metric vocabulary is in `metrics-map.md`, the boundaries of
what each tool measures in `invariants.md`, and **the live tool schema outranks both**.

## Inputs — one question, asked once

Ask, in one message, before the first call, and do not press on any of them:

- **Project** — as the user names it. On a multi-tenant connection resolve it with `tenants_list`
  to the exact system name and confirm the match; never guess a spelling. No project named → ask.
- **Goal** — which goal the project counts its money by. No answer → step 2's mechanical rule, and
  the report says so.
- **Basis of the verdicts** — the month before, or the same month a year earlier, in those words. No
  answer → the year-earlier basis (the month-on-month cut has a measured false finding on mechanics
  that send in bursts; the year cut has a measured catch of a fall the month cut showed as growth).
  Both cuts are made and printed whatever the answer; the basis decides which one a verdict rests on
  when they disagree.
- **Report form** — the **full report** (every scenario, tables, coverage, `## What we do not know`)
  or the **client deck** (three to seven proposals, ready to send, with a separate note for the CSM).
  No answer → the full report. **The form changes nothing in the analysis** — same steps, same
  templates, same thresholds, same log; the deck is a presentation of the full run, not a shorter
  audit, and the full report still exists as the chat answer.

**Period** is not asked: no period given → the last closed calendar month, said in the header.

The report names which of these were chosen and which defaulted. If the user named one flow, run
the same procedure narrowed to it.

## Procedure

**Keep a task list from here to the report** — one item per step, then one per scenario taken into
steps 6–6b. The report owes coverage («classified N of M»), which is not reconstructable from memory
on a project with hundreds of scenarios. **The list is a gate: do not begin the report while an
item is open** — close it as done or as deliberately not done with the reason, and carry every open
item into `## What we do not know`.

**The run has two outputs: the report and the log.** The log exists before the first call and is
appended as the run goes, in a file beside the report — every call with its answer, the decisions of
the cause step, the handover counts. A report whose figures cannot be found in the log is not
finished (`findings-and-failures.md`, "The handover check").

Budget: the overview is **one call per window** now, so steps 1–5 cost about five — the audited
period, the month before, the year ago, the twelve-month level, plus paging where `topN` capped a
breakdown — then up to five month-by-month series (T1m) and five reach probes; at step 6 one
T3f per scenario the construction budget will read; at step 6b twelve to twenty-four calls (up to ten
scenarios at levels 1–2, up to four at level 3). `flows_get` name resolutions — clipped names and ids
a report returned that the list did not — are counted apart and are a property of the project.
Past that you are re-querying instead of reading what you hold.

### 1. Header facts

The header carries the project, the period, the goal and the basis — and **one sentence saying that
the freshness of the reporting data could not be measured**, because no call reports it
(`metrics-map.md`, "Retired handles"). Audit a closed period and the sentence is a caveat, not a
hole.

The cheap consistency check runs once, at step 4, and is recorded in the log: **the overview's
`## Summary` against the sum of its `## Flows` rows.** They come from one tool over one window, so a
disagreement means the breakdown is capped or a filter narrowed one side — not that the data is
wrong.

### 2. The goal (T4)

**The goal is named by the report's own header** — `Period: … | Goal: …` — and the audit prints that
name beside the money, every time. `goalName` picks a different one; omitted means the project's
default.

**There is no goal catalogue**: no tool lists the project's goals with their revenue, and
`entities_list` has no goal kind. So the report cannot print every goal with its revenue the way
earlier editions did — it names the goal it counted by and says once, in `## What we do not know`,
that the alternatives were not enumerable.

**A goal name the project does not have returns an opaque error, not a fallback** (`invariants.md`,
6). When the user names a goal and the first call fails, re-run it once with `goalName` omitted
before spending a retry on the transport; if that succeeds, the name was wrong — say so, and never
let it pass as a project with no data.

### 3. The scenario list, read to exhaustion

`flows_list` to the last page (`calling-the-tools.md`, "Call arguments"). The count is what this
account sees; report it with the tool beside it. Names clipped to `..` are resolved with `flows_get`
for every scenario named in prose and for every row of the overview table.

### 4. Overview — the scenarios that were active

**Only scenarios with rows in the reporting data for the period are analysed further.** On a
project with 500 scenarios that is usually a few dozen; the rest are «did not send in the period»
and collapse into one counter (step 5). Nothing beyond `flows_list` is read for them, with one
exception in step 5.

**One call over the period** (`metrics-map.md`, "the overview, in one call"). Its `## Flows`
breakdown is **T1** (money, volume, raw counters), **T2** (Open Rate / Click Rate / Unsubscribe
Rate) and **T8** (Bounce Rate, Spam Rate) — the same rows, different columns. Its `## Summary` is
**T1p** and **T2p**, the project's own line, which every per-flow figure is stated against, at no
extra call.

**Two things to check on that answer before anything is read off it.** `top N of M` in the breakdown
header — a capped breakdown looks exactly like a complete one, and "top 20 of 92" is not the project
(`invariants.md`, 2); raise `topN` to 200 and page with `excludeFlowIds` past that. And
`ScenarioClientCount` against `ScenarioExecutionsCount` — a zero beside non-zero executions means the
per-customer family is unpopulated on this project, not that the flows reached nobody
(`invariants.md`, 5); declare it unavailable once and judge on what is populated.

**No rate is derivable from the counters beside it** — ask for the rate you intend to print
(`rates.md`).

**T1t — before anything is ranked by money.** Which scenarios send on a transactional profile. This
platform exposes no revenue-by-mailing-type split, so it is read from construction instead of from a
column — `flows_lookup` on the send steps plus the wiki's `flow_types`
(`metrics-map.md`, T1t) — and the report says which it was. Then:

- a scenario whose sends are all transactional **gets no money verdict and is not in the money
  ranking** — its row stays, revenue printed, with the words «revenue on a confirmation message
  follows the order, not the message»; a mixed one is ranked with that caveat on its line
  (`business-rules.md`, "What is never judged on money");
- **meaningful attributed revenue on transactional scenarios is a project finding**: the platform
  excludes such mailings from attribution because a service message before an order intercepts the order from
  the marketing message that earned it (`flow_types`). Print it in «the project as a whole» with
  the sum and the share, as a supposition with its probe — «supposed: the exclusion from attribution
  is not configured for these mailings; what would settle it: the project's attribution-exclusion
  list» — and the step it implies («add the transactional mailings to the exclusion, by mailing or
  by a filter on type so new ones fall under it; a recalculation moves the revenue back»), with the
  caveat that until then every money figure in the report is shifted by an unknown share. Opt-in
  mailings (the confirmation request) carry a profile of their own: they are recognised at level 3
  by the send step's mailing, and judged the same way (`business-rules.md`, "What is never judged on
  money"). **Say once in `## What we do not know` what this share does not cover** — transactional
  sends inside flows the construction budget did not open, and transactional mailings sent outside
  any flow.

**Month before** — the same one overview call on the previous closed period; the delta is arithmetic. A period
closed less than the attribution window ago is a lower bound; a fall against a settled period is
«at most this much» (`findings-and-failures.md`, "Compare like for like"). On the month-before
basis, no verdict on a burst-sending mechanic until its daily shape has been seen (same section).

**Year earlier** — **T10**: the same overview call on the year-ago window, paired to the audited one
**by flow id**, the delta arithmetic and recorded with both raw sides in the log. Its rates and its
project line are that same answer's columns and `## Summary`. It is guarded by **T11** — is this the
same mechanic in both windows — which is assembled cheapest-first from `flows_get` versions, then the
mailings, then the construction (`beyond-the-overview.md`); **anything short of "the same mechanic"
prints the delta with a warning, never as a result**, and where the guard could not be reached the
delta is «can't judge». **The year-on-year section is in every report** — figures where there are
pairs, and where there are none the counts of how many flows are in both windows / only now / only a
year ago, and what follows for the verdicts.

**A delta is never printed alone** — beside it goes the flow's own level: the overview call over the
twelve closed months. Audited month at or above the level → a year-on-year fall is «can't judge»,
both printed. Year-ago month above the level → the fall is measured from a peak; rest the verdict on
the level. Where a verdict would rest on the level, run **T1m** — that flow's twelve months one row
per month, one call with `timelineBucket="Month"` (up to five flows, largest money at stake first) —
and read the shape, not the average (`findings-and-failures.md`, "against an unexamined base").

Then attach names: ids in the list → the list's name; ids in a report and not in the list →
`flows_get` by id, which returns the name with the deletion marked — never drop such a row, it is
real money. Names clipped with `..` are resolved before they are printed or matched
(`invariants.md`, 8).

### 5. Classify every active scenario

| Verdict | Means |
|---|---|
| **problem** | a named observation, in a window, against a named comparison, on volume that clears the floor |
| **fine** | nothing the data supports flagging — and it says what it was compared with, or that it is a weak verdict |
| **did not send in the period** | no rows for the period; a counter, not a row |
| **can't judge** | two defensible readings, or volume under the floor — say which, and the probe that would settle it |

The four names are this file's; the report carries the fixed words of the reader's language
(`findings-and-failures.md`, "Our words and the reader's"). **The floors are numbers:** below
1 000 deliveries no rate is provable, below 50 goal-attributed orders no money verdict is. A flow
under them keeps its row and its figures and takes «can't judge»; when the whole project is under
them, the money verdict is stated at project level (T1p) and the per-flow one declared unavailable
once, in the header.

**Which metric decides depends on the kind of scenario** — `business-rules.md`, "The five kinds":
a reactivation is judged on unsubscribes, an engagement chain on opens and clicks, a trigger on
behaviour on revenue per send and never on volume. Read that file before this step. **An
all-transactional or opt-in scenario is judged on bounce and spam share only** — the two metrics that
need no kind: «problem» or «fine» on those, «can't judge» under the floor, and its money cell
carries the confirmation-message caveat.

**Two lists come out of this step, and both go to step 6:** the scenarios with a problem, ordered by
the money at stake (volume or reach where there is none), and **the top performers** — the two or
three scenarios with the highest conversion to order or revenue per delivery on volume that clears
the floor. The second list is read for what to copy, not for what to fix.

**Silent but still taking people in.** Before the did-not-send scenarios collapse into a counter,
probe the running ones with `flows_lookup(includeExecutions=true)` — at most five, ordered by the
price of the silence (stopped earners by twelve-month revenue first, then never-sent ones by the reach
their mechanic implies; `findings-and-failures.md`, "A flow that delivered nothing"). A scenario at or
above the floor with people entering and nothing delivered keeps a row: «can't judge», the count with
its window, and the probe.

State coverage explicitly, and name any scenario you could not reach.

### 6. Deep dive on the figures — problem scenarios and top performers

- **T3f** — the scenario's mailings, money joined to funnel, pinned to that flow. Its sum is
  expected to equal the flow's T1 row; a difference makes that flow's figures unquotable and is a
  finding about the marts, not about the flow.
- **Decompose the movement** — `business-rules.md`, "Decomposing a change in revenue": which
  message moved (T3f against the compared window), when it turned (T1m), which channels sent (T2,
  T8), and whether it is volume, deliverability, engagement or conversion that moved. Channel first.
- **What this step fetched is what the cause step reads.** Do not write the finding from here; go
  through 6b and `## From "what" to "why"` with it.

### 6b. Read the construction — only for the scenarios step 5 singled out

Read `structural-causes.md` and apply its protocol: **level 1** (`flows_get` — the start, the
versions, the state) and **level 2** (`flows_lookup`, skeleton with execution counts — where
executions are lost, which outputs lead nowhere, whether a second attempt exists) for every problem
scenario and every top performer within the budget; **level 3** (one block's neighbourhood at full
detail — a condition's body, a send step's mailing profile, a wait's window, the scenario's repeat
settings) where the finding needs it. **Up to seven problem scenarios and up to three top performers
at levels 1–2, up to four scenarios at level 3**, in the order step 5 produced (money at stake, then
volume or reach). What did not fit is a line in `## What we do not know`; the problem scenarios
beyond the budget keep their verdict and go to the hypothesis table marked «construction not read»
(rule 4). **Before the report is begun, write the outcome back**: which scenarios were read, which
were not, and any verdict this step changed — the overview rows, the confidence split and the
coverage line are rewritten from that.

Take the symptom the figures showed to the catalogue in that file and look where it says; **assert
only what this scenario's construction shows.** Check form F (the burnt attempt) on every scenario
that reaches level 2 — it has been the most expensive finding on two projects.

**For a top performer, the reading is the same and the question is inverted**: what in this
construction — the gate, the wait, the re-check, the cascade, the timing — is absent from the
problem scenarios of the same kind. That difference is a hypothesis for them, printed as one, with
the block it names.

**Where the scenario is a recognisable mechanic** — welcome, abandoned session, reactivation,
birthday, order status — read the wiki's `mechanics.<mechanic>.overview` and `.structure` for what
the mechanic is meant to do and by what means, and match: is that means present here, and what is
missing. **This is a source of hypotheses, not a standard**: the documented assembly is a template
for building new scenarios, and a scenario that departs from it is not thereby defective. A gap
worth naming is one that connects to the figure — a missing re-check where unsubscribes are high, a
missing wait where bounces sit on the first message.

### 7. Enrichment, if the optional tools are there

`flow_report`, `campaign_report`, `email_health_report` — routinely off per project. **Never sum
or compare across tools**: each describes its own population (`invariants.md`, "Numbers from two
different tools are not added together"). From `email_health_report` only the thresholds and the
industry median travel to this audit; its brand values do not. Two things nothing here substitutes,
so they go to `## What we do not know` when asked for: per-customer entries into a scenario over the
period, and per-flow parity with the platform's screen.

### 8. Select for the deck — only when the report form is the client deck

The full run is done. This step computes nothing; it chooses what goes on the slides
(`writing-the-report.md`, "The client deck"): only findings taken through in full — construction
read — plus at most one project finding; **three to seven slides, as many as there are such
findings**, never padded and never cut to a round number; several scenarios with one cause on one
slide; each slide carrying one main figure; the scenarios of the hypothesis table are not slides and
are named on the overview slide as «N more scenarios flagged by the figures — in the full report».
**Urgency labels are assigned by rule**: a breached hygiene threshold or the attribution finding →
"Decide today"; an established cause with a fix → "Fix"; a hypothesis with a probe → "Idea" (in a
report written in another language, their equivalents, fixed once in the log — Russian:
«Решить сегодня» / «Чинить» / «Идея»).

## From "what" to "why" — a cause, or a hypothesis with a probe

Runs after steps 6, 6b and 7, on the findings they produced, before a line of the report is written;
one task-list item per finding. **Every finding goes one step further than «what moved»**: the cause
is established in this run's own data, or it is a supposition with the one thing that would settle
it. «A question for the CSM» with nothing beside it is what this step replaces.

Three shapes, told apart by the sentence and not by how sure it sounds:

- **An established cause.** The run holds a figure of its own about this scenario that accounts for
  the movement, **and something names the mechanism between the two** — coincidence in time is not
  a mechanism. The call that produced it and its answer are in the log. It does not rest only on a
  quantity in the register of unreliable figures (`invariants.md` — today, the run-close date). Its
  window is said and placed against the finding's: a ~30-day execution count set beside a monthly
  finding is honest with the window named and a hypothesis without it.
- **A hypothesis.** What is supposed, and beside it **the probe** — what someone would look at and
  what result would confirm or refute it, named by the thing looked at, never by the tool. A
  supposition whose probe cannot be named is dropped; the observation and its cost stay.
- **An invented finding** — the thing rule 2 forbids: a cause as fact with no figure behind it, a
  hypothesis worded as a diagnosis, «probably» carrying the weight of a missing figure.

**Six sources of causes, spent in this order before supposing anything.** The first four cost no new
call: which message inside the scenario moved (T3f); when it turned (T1m); which channels sent and
whether that set moved (T2, T8); where inside the graph executions stopped (`flows_lookup`, its own
~30-day window). The fifth is **the construction** (6b) — the strongest, because it is the only one
that gives a mechanism: an impassable condition, a burnt attempt, a missing check, a wait without a
window (`structural-causes.md`). The sixth is the version history, which never becomes an
established cause about a change: versions are published regularly on scenarios that are merely
maintained, and a mailing's content is edited outside the version — a version change near a
movement is printed as a hypothesis with the changed message set as its evidence
(`calling-the-tools.md`, "Comparing two versions").

**Whether a scenario is running is established from its version statuses** (`calling-the-tools.md`,
the status table), never from the `active version` line and never from send dates; **when it
stopped** is bounded by the last month with sends in the reporting data and printed as bounds;
**the run-close date is quotable for nothing** (`invariants.md`, the register). Every running-state
decision leaves a line in the log — scenario, the status strings as returned, the call, the reading —
and a run that decided none says so.

**Recommendations to start or restart a scenario stand only on an established cause**; on a
hypothesis they are printed as the hypothesis with its probe. What every recommendation must
contain, and what is never recommended: `business-rules.md`. **The steps come ranked** by the money
the finding has put a figure on, then by volume or reach where there is none, and the report says
which key ranked them.

## What is a finding and what only looks like one

Read `findings-and-failures.md`, "What is a finding and what only looks like one", before writing any
finding. Every trap in it has produced a wrong verdict on a real project.

## Writing the report

**Stop here and read `writing-the-report.md`.** It fixes the language and the vocabulary, the frame
of sections, the five parts of a problem scenario's block, the hypothesis table for the rest, the
strengths, the three surfaces (chat, full page, client deck with its CSM note) and the handover check
that has to be in the log before anything is handed over.

## If something goes wrong

The triage table is `findings-and-failures.md`, "If something goes wrong": situation → what to do,
for every failure this audit has met.
