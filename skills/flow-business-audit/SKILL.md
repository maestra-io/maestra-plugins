---
name: flow-business-audit
description: >-
  Business audit of a project's marketing scenarios (flows), ending in fixes to them. First
  the figures: revenue, orders, funnel and rates per flow, over the period and against the
  month before and the year-earlier month, to find the flows with a problem and the ones that
  work best. Then, only for those, the construction: start block, conditions, sends, repeat
  settings, to name the block and the action that would fix it, or what to copy. Up to seven
  scenarios go through in full, the rest become hypotheses. Two report forms, chosen at the
  start: the full report, or a proposal deck with separate presenter notes. Use when the
  question is about business results, in any language: which flows earn and which do not,
  what the scenarios brought in for the month, one flow's money. Answers in the language
  asked. Read-only: don't use to audit one flow's structure with no figures
  (flow-issues-audit), to summarize what a flow does (flow-summary), or to create or edit
  anything.
metadata:
  author: Maestra.io
  upstream: AI tribe
  version: 8.0.0
---

# Flow business audit

Answer, for a project, **which scenarios earn and which do not, and what in each would fix it**.
Every number carries its window and its origin; everything uncomputable is said.

Figures first, construction only for the flows the figures single out (`structural-causes.md`).

**If you are orchestrating other work, run this in a subagent**: name `maestra:flow-business-audit`
in the brief, tell it to read `SKILL.md` and the reference files itself, and give it the project,
the period and the goal. Running inline is allowed; either way you fetch every figure yourself and
the report must be user-ready on its own (`writing-the-report.md`).

## Where to look

Three sources rank above anything written here, and they answer different questions.

- **The live tool schema wins on signatures.** This skill names capabilities, never their
  arguments, defaults or allowed values; read the schema before you build a call
  (`calling-the-tools.md`, "Call arguments").
- **`flow_report` wins on the figures** — every number in this audit is computed by the platform,
  the same computation behind the project's Scenarios screen, so a figure printed here and a figure
  the reader opens in the admin UI are the same figure. There is no SQL in this skill and no
  datamart to query (`## Where a figure comes from`).
- **The wiki wins on meanings** — what a block type does, what a status means, what the flow-level
  settings hold. The `wiki` tool on the same server as the flow tools is the only route to it; take
  every id from an index or from a document's `# References` list.

Nothing in the report stands on the wiki alone (`structural-causes.md`, "What the wiki adds"). The
documents this audit opens:

| Document | When | What it settles |
|---|---|---|
| `flow_types` | before the money ranking (step 4) | the mailing profile — which sends are transactional and what that does to attribution |
| `overview` | before the first construction reading | what an execution is; what the flow-level settings hold and what the repeat limit counts |
| `urls` | when a status has to be read | the priority order between statuses; the running / not-running vocabulary itself is the `flows_list` schema's |
| `blocks`, then `blocks.<block>` | while reading a specific block | what a block type is, and what a setting seen in its properties means |
| `mechanics.<mechanic>.overview` / `.structure`, `mechanics.best_practices` | when a scenario is recognisable as a known mechanic | what the mechanic is for and how that is usually achieved — a source of hypotheses about what is missing, **not a standard the scenario is validated against** |

**Where the live contract and this skill disagree, the live contract wins**: act on it, say so in the
run log, and report the divergence.

## Reference map

Read with `Read` at the step that names the file — not all of them up front.

| File | Read when |
|---|---|
| `references/calling-the-tools.md` — the transport, the version and status readings | before the first call |
| `references/invariants.md` — what an answer is not | before the first call |
| `references/metrics-map.md` — question → call, the metric vocabulary, the arguments verbatim | steps 2 and 4 |
| `references/rates.md` — which rate decides what, the floors, the one benchmark | step 4 |
| `references/beyond-the-overview.md` — the year-ago call, its continuity guard, the per-flow calls | step 4 (year cut), step 6 |
| `references/business-rules.md` — marketing judgement | steps 5 and 6b, and before `## From "what" to "why"` |
| `references/structural-causes.md` — the construction reading | step 6b |
| `references/findings-and-failures.md` — traps, floors, triage, handover check | step 5, on the first refusal, when writing the report |
| `references/writing-the-report.md` — language, frame, surfaces | once, when the report is begun |
| `references/<locale>/terminology.md` — the printed wording | when writing the report |
| `references/<locale>/html-report-example.html` — the themed full page | only if the page is asked for |
| `references/<locale>/html-proposal-deck-example.html` — the themed deck | only on the deck form |

`<locale>` is `en-US` or `ru-RU`, chosen by the user's language; a language with no variant takes
`en-US` and translates it. Copy every call's arguments from the reference; never invent a metric name.

## CRITICAL — four rules that outrank everything below

1. **Never print a number without its passport — in the reader's words.** Every figure carries,
   where it is printed, the window it covers and what measured it, in words the reader has — never a
   template handle, a tool name or a metric name. Which call produced it stays in the run log. A
   number no call of this run returned does not go in the report, not as an estimate.
2. **Never invent a finding.** A false alarm on a healthy flow is as bad as a miss. A finding names
   the observation, the window and the comparison it rests on; where the data supports two readings,
   "can't judge, and here is what would settle it" is a legitimate verdict. What this forbids is a
   finding with no figure behind it — not a supposition that says it is one and names its probe
   (`## From "what" to "why"`).
3. **Never run a partial audit silently, and never write.** Either the audit is complete for what it
   claims to cover, or the gap is named — in the header for a stop, in `## What we do not know` for
   anything that failed along the way. Read-only: never `flows_apply_operations`, `flows_create`,
   `flows_create_draft`, `flows_set_testing_mode` or any other writing tool.
4. **A scenario is not taken through in full until it has been read, and no fix names a place the
   run did not see.** Three obligations. Every scenario with a full block in the report and every
   scenario on a deck slide has had its construction read (`structural-causes.md`, levels 1 and 2 at
   least). **Every step in "What to do" names a place and an action** — a block, a setting, a
   condition or a data source by name, and a verb that can be carried out; a step naming only an
   area to search is a question, and questions live in the cause part as probes. **The construction
   budget is never widened in silence** (`structural-causes.md`, "Budget"): a flagged scenario the
   budget did not reach keeps its verdict by the figures, goes to the hypothesis table with the
   words "construction not read" on its row, and gets no full block and no slide. Project-level
   findings have no single construction and are outside this rule.

## Prerequisites — the tools, checked by using them

**Required**: `flow_report`, `flows_list`, `flows_get`, `flows_lookup` — the first is where every
figure comes from, the last because rule 4 cannot be kept without it. **A `flows_lookup` that
answers but returns no counters for the window is not a missing tool**: it is the triage row of that
name in `findings-and-failures.md`, "If something goes wrong", and the audit continues without
block-level figures. One missing → name which capability is missing, in plain words, print no figure,
and stop that part; enabling it is done by whoever administers the project's platform account, not
by you.

**Optional enrichment** — absence never stops the audit and is named in `## What we do not know`:
`wiki` (domain `Flows` — what a construction means), `campaign_report` (what each mailing inside a
flow contributed), `email_health_report` (the industry benchmark), `entities_list`, `tenants_list`
(on a connection serving several projects, to resolve the project name).

**Not used by this edition.** `analytics_execute_query` / `analytics_get_schema` are the freehand
datamart tools; earlier editions of this skill ran on them. The scenario marts they served are not
part of this platform's catalogue, so **this skill writes no SQL**. If a project's catalogue does
expose scenario-grain marts, that is a reason to extend this skill deliberately, not to improvise a
query mid-audit: a hand-written figure beside a platform-computed one is the thing invariant 13
forbids.

No probe call: the first real calls of the procedure are the check. A refusal arrives wrapped in the
same prefix as a transport error — read the text after the colon; it decides between a retry and a
stop. **Stop only on a refusal returned to your own call to a required tool**
(`findings-and-failures.md`, "If something goes wrong"); a notice about another MCP server, a tool
that has to be loaded before it can be called, a subagent's silence and your own failure to compose
a call are none of them. A missing required tool reads three ways and they are fixed differently
(`invariants.md`, 12).

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

Ask, in one message, before the first call, and do not press on any of them. **A second question is
asked only for a gap that blocks the run** — a project that cannot be resolved, a version that
neither the flow list nor its fallback answers for — and never to refine an answer already given or
one deliberately left unanswered.

- **Project** — **read from the tool listing whether the connection serves one project or several.**
  Where `tenants_list` is absent the connection already fixes the project: nothing is resolved and
  nothing is asked, and the header names the project the run covers. Where it is present, the
  project comes from the user's words — resolve them with it to the exact system name and confirm
  the match, never guessing a spelling, and ask only when the user named no project. So this is a
  question on some connections and not on others; the rest of the list is asked either way.
- **Goal** — which goal the project counts its money by. No answer → step 2's mechanical rule, and
  the report says so.
- **Basis of the verdicts** — the month before, or the same month a year earlier, in those words. No
  answer → the year-earlier basis (the month-on-month cut has a measured false finding on mechanics
  that send in bursts; the year cut has a measured catch of a fall the month cut showed as growth).
  Both cuts are made and printed whatever the answer; the basis decides which one a verdict rests on
  when they disagree.
- **Report form** — the **full report** (default) or the **proposal deck** with its presenter notes.
  **The form changes nothing in the analysis** — same steps, same calls, same thresholds, same log;
  the deck is a presentation of the full run, not a shorter audit, and the full report still exists
  as the chat answer.

**Period** is not asked: no period given → the last closed calendar month, said in the header.

The report names which of these were chosen and which defaulted. If the user named one flow, run
the same procedure narrowed to it.

## Procedure

**Keep a task list** — one item per step, one per scenario taken into steps 6–6b. The report owes
coverage ("classified N of M"), which is not reconstructable from memory on a project with hundreds
of scenarios. Do not begin the report while an item is open: close it, or carry it into
`## What we do not know`.

**The run has two outputs: the report and the log.** The log exists before the first call and is
appended as the run goes, in a file beside the report — every call with its answer, the decisions of
the cause step, the handover counts. A report whose figures cannot be found in the log is not
finished (`findings-and-failures.md`, "The handover check").

Budget: the overview is **one call per window**, so steps 1–5 cost about five — the audited period,
the month before, the year ago, the twelve-month level, plus paging where `topN` capped a breakdown —
then up to five month-by-month series (T1m) and five reach probes; the T1t construction reads, one
skeleton and one restricted full-detail read per flow with rows, as a line of their own; at step 6
one T3f call per compared window, since it returns every automatic mailing at once; at step 6b
twelve to twenty-four calls (up to ten scenarios at levels
1–2, up to four at level 3) plus up to ten single-block settings reads for form F
(`structural-causes.md`, "Budget"). **The `flows_list` pages are a line of their own and are not
inside any of those numbers** — how many there are is the size of the project, not the depth of the
audit, and on a large project they can outnumber every analytical call. `flows_get` name resolutions
are counted apart too. Past that you are re-querying what you already hold.

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
name beside the money, every time; the report names it by its **display name**, never a system
name. `goalName` picks a different one; omitted means the project's default.

**There is no goal catalogue**: no tool lists the project's goals with their revenue, and
`entities_list` has no goal kind. So the report cannot print every goal with its revenue the way
earlier editions did — it names the goal it counted by and says once, in `## What we do not know`,
that the alternatives were not enumerable. **One goal per figure**, never two goals in one call or
one sum (`invariants.md`, 6).

**A goal name the project does not have returns an opaque error, not a fallback** (`invariants.md`,
6). When the user names a goal and the first call fails, re-run it once with `goalName` omitted
before spending a retry on the transport; if that succeeds, the name was wrong — say so, and never
let it pass as a project with no data.

### 3. The scenario list, read to exhaustion

Page `flows_list` to the end (`calling-the-tools.md`, "Call arguments"); the count is what this
account sees, and is reported with the tool beside it. **Paging to the end is required for two
things only — M and the set of statuses**; nothing later reads the content of the later pages. There
is no page cap: M has to be exact. Where the listing runs past a few pages, say so where the count
is printed and record the number of pages in the log as its own cost. Names clipped to `..` are
resolved with `flows_get` for every scenario named in prose and for every row of the overview table.

### 4. Overview — the scenarios that were active

**Only scenarios with rows in the reporting data for the period are analysed further.** On a
project with 500 scenarios that is usually a few dozen; the rest are "did not send in the period"
and collapse into one counter (step 5). Nothing beyond `flows_list` is read for them, with one
exception in step 5.

**One call over the period** (`metrics-map.md`, "the overview, in one call"). Its `## Flows`
breakdown is **T1** (money, volume, raw counters), **T2** (Open Rate / Click Rate / Unsubscribe
Rate) and **T8** (Bounce Rate, Spam Rate) — the same rows, different columns. Its `## Summary` is
**T1p** and **T2p**, the project's own line, which every per-flow figure is stated against, at no
extra call. Conversion to order is the platform's own `ConversionRate`, computed over the deliveries
its attribution admits — never `Orders ÷ Deliveries` (`rates.md`).

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
  ranking** — its row stays, revenue printed, with the words "revenue on a confirmation message
  follows the order, not the message"; a mixed one is ranked with that caveat on its line
  (`business-rules.md`, "What is never judged on money");
- **meaningful attributed revenue on transactional scenarios is a project finding** about the
  attribution set-up (why: `flow_types`; the reader-facing wording: `business-rules.md`,
  "Attribution, in the reader's words"). Print it in "the project as a whole" with the sum and the
  share **computed from those flows' own rows**, as a supposition whose probe is the project's
  attribution-exclusion list, with the step it implies and the caveat that until then every money
  figure in the report is shifted by an unknown share. Opt-in mailings (the confirmation request)
  carry a profile of their own: they are recognised at level 3 by the send step's mailing, and
  judged the same way. **Say once in `## What we do not know` what this share does not cover** —
  transactional sends inside flows the construction budget did not open, and transactional mailings
  sent outside any flow.

**Month before** — the same one overview call on the previous closed period; the delta is
arithmetic. A period closed less than the attribution window ago is a lower bound; a fall against a
settled period is "at most this much" (`findings-and-failures.md`, "Compare like for like"). On the
month-before basis, no verdict on a burst-sending mechanic until its daily shape has been seen (same
section).

**Year earlier** — **T10**: the same overview call on the year-ago window, paired to the audited one
**by flow id**, the delta arithmetic and recorded with both raw sides in the log. Its rates and its
project line are that same answer's columns and `## Summary`. It is guarded by **T11** — is this the
same mechanic in both windows — which is assembled cheapest-first from `flows_get` versions, then the
mailings, then the construction (`beyond-the-overview.md`); **anything short of "the same mechanic"
prints the delta with a warning, never as a result**, and where the guard could not be reached the
delta is "can't judge". **The year-on-year section is in every report** — figures where there are
pairs, and where there are none the counts of how many flows are in both windows / only now / only a
year ago, and what follows for the verdicts.

**A delta is never printed alone** — beside it goes the flow's own level: the overview call over the
twelve closed months. Audited month at or above the level → a year-on-year fall is "can't judge",
both printed. Year-ago month above the level → the fall is measured from a peak; rest the verdict on
the level. Where a verdict would rest on the level, run **T1m** — that flow's twelve months one row
per month, one call with `timelineBucket="Month"` (up to five flows, largest money at stake first) —
and read the shape, not the average (`findings-and-failures.md`, "against an unexamined base").

**Attach names** — ids in the list → the list's name; ids in a report and not in the list →
`flows_get` by id, which returns the name with the deletion marked. Never drop such a row: it is
real money. Names clipped with `..` are resolved before they are printed or matched
(`invariants.md`, 8).

### 5. Classify every active scenario

| Verdict | Means |
|---|---|
| **problem** | a named observation, in a window, against a named comparison, on volume that clears the floor |
| **fine** | nothing the data supports flagging — and it says what it was compared with, or that it is a weak verdict |
| **did not send in the period** | no rows for the period; a counter, not a row |
| **can't judge** | two defensible readings, or volume under the floor — say which, and the probe that would settle it |

The four names are this file's; the report prints the reader's language from
`references/<locale>/terminology.md`. **The provability floors are numbers and they live in one
place**: `findings-and-failures.md`, "Materiality before signal". A flow under them keeps its row
and its figures and takes "can't judge"; when the whole project is under them, the money verdict is
stated at project level (T1p) and the per-flow one declared unavailable once, in the header.

**Which metric decides depends on the kind of scenario** — read `business-rules.md`, "The five
kinds", before this step. **An all-transactional or opt-in scenario is judged on bounce and spam
share only**, the two metrics that need no kind: "problem" or "fine" on those, "can't judge" under
the floor, and its money cell carries the confirmation-message caveat.

**Two lists come out of this step, and both go to step 6:** the scenarios with a problem, ordered by
the money at stake (volume or reach where there is none), and **the top performers** — the two or
three scenarios with the highest conversion to order (the platform's own rate) or revenue per
delivery on volume that clears the floor. A scenario whose conversion rate comes back empty has no
conversion to compare and is chosen, if at all, on revenue per delivery, with that said. The second
list is read for what to copy, not for what to fix.

**Silent but still taking people in.** Before the did-not-send scenarios collapse into a counter,
probe the running ones with `flows_lookup(includeExecutions=true)` — **at most five**, ordered by the
price of the silence (stopped earners by twelve-month revenue first, then never-sent ones by the reach
their mechanic implies; `findings-and-failures.md`, "A flow that delivered nothing"). A scenario at or
above the floor with people entering and nothing delivered keeps a row: "can't judge", the count with
its window, and the probe.

State coverage explicitly, and name any scenario you could not reach.

### 6. Deep dive on the figures — problem scenarios and top performers

- **T3f** — the scenario's mailings, money joined to funnel, matched to that flow's send steps by
  name (`beyond-the-overview.md`). It shows which send inside the flow carries the flow's result —
  the ranking, never a total to reconcile against the flow's own row, since the two reports overlap
  by construction; a shape that contradicts the flow's row is a finding about the matching, not
  about the flow.
- **Decompose the movement** — `business-rules.md`, "Decomposing a change in revenue": which
  message moved (T3f against the compared window), when it turned (T1m), which channels sent (T2,
  T8), and whether it is volume, deliverability, engagement or conversion that moved. Channel first.
- **What this step fetched is what the cause step reads.** Do not write the finding from here; go
  through 6b and `## From "what" to "why"` with it.

### 6b. Read the construction — only for the scenarios step 5 singled out

Read `structural-causes.md` and apply its protocol and its budget, in the order step 5 produced:
**level 1** (`flows_get` — the start, the versions, the state) and **level 2** (`flows_lookup`,
skeleton with execution counts) for every problem scenario and every top performer within the
budget; **level 3** (one block's neighbourhood at full detail) where the finding needs it. **Before
the report is begun, write the outcome back**: which scenarios were read, which were not, and any
verdict this step changed — the overview rows, the confidence split and the coverage line are
rewritten from that.

Take the symptom the figures showed to the catalogue in that file and look where it says; **assert
only what this scenario's construction shows.** Check form F (the burnt attempt) on every scenario
that reaches level 2: it has a read allowance of its own — one full-detail call restricted to a
single block, separate from the four full readings (`structural-causes.md`, "Budget"). A scenario
whose allowance went unspent carries **"form F not checked"**; it is never asserted from the
skeleton.

**For a top performer the reading is the same and the question is inverted**: what in this
construction — the gate, the wait, the re-check, the cascade, the timing — is absent from the
problem scenarios of the same kind. That difference is a hypothesis for them, printed as one, with
the block it names.

Where the scenario is a recognisable mechanic, the wiki's `mechanics` documents are a source of
hypotheses about what is missing (`structural-causes.md`, "Documented mechanics: a source of
hypotheses, not a standard").

### 7. Enrichment, if the optional tools are there

`campaign_report`, `email_health_report` — routinely off per project. **Never sum or compare across
tools**: each describes its own population (`invariants.md`, "Numbers from two different tools are
not added together"). From `email_health_report` only the thresholds and the industry median travel
here; its brand values do not. **Entries into a scenario over the period are `flow_report`'s own
`ScenarioExecutionsCount`**, printed under its own name (`metrics-map.md`, "The map"); the
per-customer family beside it is printed only where the platform populates it (`invariants.md`, 5)
and otherwise goes to `## What we do not know`. Per-flow parity with the platform's screen goes
there whatever tools are present.

### 8. Select for the deck — only when the report form is the proposal deck

The full run is done; this step computes nothing. Choose from findings taken through in full —
construction read — plus at most one project finding, and build the slides by the rule in
`writing-the-report.md`, "The proposal deck", urgency labels included: **one overview plus up to
seven proposals — as many as were taken through in full**, never padded and never cut to a round
number, and a deck of two proposals is a correct deck on a project with two such findings. The
hypothesis table's scenarios are not slides and are named on the overview slide with the
`deck.overview.more` line of the locale. **Urgency labels are assigned by rule**: a breached hygiene
threshold or the attribution finding → "Decide today"; an established cause with a fix → "Fix"; a
hypothesis with a probe → "Idea" — the wording per locale is `references/<locale>/terminology.md`.

## From "what" to "why" — a cause, or a hypothesis with a probe

Runs after steps 6, 6b and 7, on the findings they produced, before a line of the report is written;
one task-list item per finding. **Every finding goes one step further than "what moved"**: the cause
is established in this run's own data, or it is a supposition with the one thing that would settle
it. "An open question for the project owner" with nothing beside it is what this step replaces.
Three shapes, told apart by the sentence and not by how sure it sounds:

- **An established cause.** The run holds a figure of its own about this scenario that accounts for
  the movement, **and something names the mechanism between the two** — coincidence in time is not
  a mechanism. The call that produced it and its answer are in the log. It does not rest only on a
  quantity in the register of unreliable figures (`invariants.md`, 14 — today, the run-close date).
  Its window is said and placed against the finding's: an execution count over the structure's own
  ~30-day window set beside a monthly finding is honest with the window named and a hypothesis
  without it.
- **A hypothesis.** What is supposed, and beside it **the probe** — what someone would look at and
  what result would confirm or refute it, named by the thing looked at, never by the tool. A
  supposition whose probe cannot be named is dropped; the observation and its cost stay.
- **An invented finding** — the thing rule 2 forbids: a cause as fact with no figure behind it, a
  hypothesis worded as a diagnosis, "probably" carrying the weight of a missing figure.

**Six sources of causes, spent in this order before supposing anything.** The first four cost no new
call: (1) which message inside the scenario moved (T3f); (2) when it turned (T1m); (3) which
channels sent and whether that set moved (T2, T8); (4) where inside the graph executions stopped
(`flows_lookup`, over the counters' own window). (5) **The construction** (6b) is the only one that
gives a mechanism: an impassable condition, a burnt attempt, a missing check, a wait without a
window (`structural-causes.md`). (6) The version history never becomes an established cause about a
change — versions are published regularly on scenarios that are merely maintained, and a mailing's
content is edited outside the version — so a version change near a movement is printed as a
hypothesis with the changed message set as its evidence (`structural-causes.md`, "Comparing two
versions of a scenario").

**Whether a scenario is running is established from its version statuses** (`calling-the-tools.md`,
"Call arguments"), never from the `active version` line and never from send dates; **when it
stopped** is bounded by the last month with sends in the reporting data and printed as bounds;
**the run-close date is quotable for nothing** (`invariants.md`, 14). Every running-state decision
leaves a line in the log — scenario, the status strings as returned, the call, the reading — and a
run that decided none says so.

**Recommendations to start or restart a scenario stand only on an established cause**; on a
hypothesis they are printed as the hypothesis with its probe. What every recommendation must
contain, and what is never recommended: `business-rules.md`. **The steps come ranked** by the money
the finding has put a figure on, then by volume or reach where there is none, and the report says
which key ranked them.

## What is a finding and what only looks like one

Read `findings-and-failures.md`, "What is a finding and what only looks like one", before writing any
finding. Every trap in it has produced a wrong verdict on a real project.

## Writing the report

**Stop here and read `writing-the-report.md` before writing anything.** It fixes the language and the
vocabulary, the frame of sections, the five parts of a problem scenario's block, the hypothesis table
for the rest, the strengths, the three surfaces (chat, full page, proposal deck with its presenter
notes) and the handover check that has to be in the log before anything is handed over.

## If something goes wrong

The triage table is `findings-and-failures.md`, "If something goes wrong": situation → what to do,
for every failure this audit has met.
