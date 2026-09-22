# Structural causes — reading the scenario's construction behind a figure

**Reporting data gives the size of a movement. The scenario's construction gives the mechanism.
A cause is established when the run holds both.** This file is the procedure that turns "go and
look at the construction" into a bounded reading, and the catalogue that says, for each symptom
the reporting data can show, where in the construction to look, what is usually found there, and
what a fix sounds like when it is written for the reader.

It is read at `SKILL.md` step 6b, for every finding about a scenario. `SKILL.md § From "what" to
"why"` fixes what a reading may conclude — established cause, hypothesis with a probe, or nothing —
and this file does not restate that. What is here is *how* the reading is taken and *where* it
looks.

**The catalogue is not a list of diagnoses.** It says where to look and what is usually there; the
report may state only what the run saw in this scenario's construction. A symptom whose row names
three usual findings and a construction that shows none of them is a finding with an open cause,
printed as such.

## Contents

1. [The reading protocol — three levels, cheapest first](#the-reading-protocol--three-levels-cheapest-first)
2. [Budget](#budget)
3. [What the wiki adds, and what it never carries](#what-the-wiki-adds-and-what-it-never-carries)
4. [The catalogue: symptom → where to look → what is usually there → the shape of the fix](#the-catalogue-symptom--where-to-look--what-is-usually-there--the-shape-of-the-fix)
5. [Form F, the burnt attempt — checked on every scenario that reaches level 2](#form-f-the-burnt-attempt--checked-on-every-scenario-that-reaches-level-2)
6. [Documented mechanics: a source of hypotheses, not a standard](#documented-mechanics-a-source-of-hypotheses-not-a-standard)
7. [What this reading must not do](#what-this-reading-must-not-do)

---

## The reading protocol — three levels, cheapest first

The order matters: a full graph at full detail costs thousands of tokens, a skeleton hundreds.
Each level answers a question the previous one cannot; stop at the level that answers the finding's.

**Level 1 — the scenario card. `flows_get` by id. Mandatory for every finding about a scenario.**
Gives: the `launch:` line (the start event with its system name, or a schedule), the folder, the
brand, the version list with statuses and creation dates, the `issues` block.
Answers: what starts the scenario; whether it is running now (`calling-the-tools.md`, the status
table); whether a version was published near the movement — which is a *place to look*, never a
cause (`SKILL.md § From "what" to "why"`, the change block).

**Level 2 — the skeleton with executions. `flows_lookup(detail=Skeleton, structure=Full,
includeExecutions=true)`. Mandatory for every finding about a scenario.**
Gives: every edge of the graph, the count on every output, the stop lines with their reasons, the
window the counters cover.
Answers: where executions are lost; which outputs lead nowhere; whether a second attempt exists
downstream of a failed check. This is the same call `calling-the-tools.md`, "Reading the per-block
funnel" already describes — what is new is that it is **owed**, not taken when there is time.

**Level 3 — the properties of a neighbourhood. `flows_lookup(detail=Full,
structure=Subgraph|Neighbours, startBlockId=<block>, depth=1..2)`. As the finding needs.**
Gives: the body of a condition's filter; the trigger event with its filter; the send steps with each
mailing's profile (`mailing.isTransactional`); the wait strategy with its exit window and time zone;
and the flow-level `settings` — `repeatSettings` (`"$type": "defaultRepeatStrategy"` means no limit)
and `launchSettings` — which come with **every** `detail=Full` answer whatever `structure`,
`startBlockId` or `depth` say, and never at `detail=Skeleton` `[service source, 2026-09-17]`.
Answers: what exactly the condition people stop at checks; whether a wait has a window; whether the
once-per-customer limit is on.

> **`detail=Full, structure=Full` is not called without a reason.** On a ten-block scenario it is
> around seven thousand tokens; the neighbourhood of the block where executions stop usually gives
> the same answer an order of magnitude cheaper. The full graph is justified only when the losses
> are spread over several places. **When the only question is the repeat limit or the working period, the
> cheap read is `flows_lookup(detail=Full, structure=Subgraph, depth=0)` from any block** — it
> returns `settings` with almost no graph. `depth` is ignored at `structure=Full`, so
> `structure=Full, depth=0` is the whole graph, not a cheap read. The values are not in the start
> block's properties; they belong to the version.

**Which version.** The version to read is decided the way `calling-the-tools.md`, "Call arguments"
decides it for `flows_lookup`, fallback included: the version whose run overlaps the audited window,
else the active one from the list, with which one was used said in the log. A finding about a
period the current version did not cover reads the current construction and says so — the
construction it describes is today's.

## Budget

- **Up to seven problem scenarios and up to three top performers** receive levels 1 and 2 — the
  problem scenarios in the order step 5 produced (money at stake, then volume or reach), the top
  performers read for what to copy rather than what to fix (`SKILL.md` step 6b).
- **Up to four of those** receive level 3.
- **The construction is read only for scenarios the figures singled out** — never for the whole
  list. On a project with hundreds of scenarios most never sent in the period and are not opened.
- What did not fit is a line in `## What we do not know`, naming the scenario and what was left
  unread — and a problem scenario beyond the budget keeps its verdict by the figures and goes to the
  hypothesis table marked «construction not read» (`SKILL.md`, CRITICAL rule 4).
- **Whether the scenario's mailings are transactional is read before the money ranking, not here** —
  `SKILL.md` step 4, the T1t paragraph — because a scenario that should never have entered the money
  ranking must not spend this budget confirming a finding that does not exist.

This adds twelve to twenty-four calls to the run. It is comparable with what the reach probes of
step 5 already cost, and it buys the one thing those probes do not: a mechanism, where they give a
count.

## What the wiki adds, and what it never carries

The `wiki` tool (domain `flows`) explains what the construction means; it is read, and nothing in the
report stands on it alone. The size comes from the reporting data, the mechanism from the scenario;
the wiki says what a setting seen at level 3 does. **A statement that rests only on the wiki is not a
finding.** Which documents, and when — the table is in `SKILL.md § Prerequisites`.

Three documents matter most to this reading:

- `overview` — what an execution is, what "a run counts" means for the repeat limit, and the
  warning that **the absence of a limit is never inferred from the skeleton** — which is why form F
  below is not asserted without level 3;
- `flow_types` — the mailing profile (`isTransactional`) and what it waives; and the attribution
  paragraph that turns attributed revenue on a transactional mailing into a project finding
  (`SKILL.md` step 4);
- `mechanics.<mechanic>.overview` / `.structure` and `mechanics.best_practices` — what a recognised
  mechanic is for and by what means it usually gets there; a source of hypotheses about what is
  missing (section 6 below), not a standard.

## The catalogue: symptom → where to look → what is usually there → the shape of the fix

Every row starts from something the reporting data of steps 4–6 already shows. The second column is
what level 2 or 3 reads; the third is what that reading has turned up on live projects; the fourth
is how a step in «What to do» sounds when it is written for the reader — a place by its name and a
verb that can be carried out (`writing-the-report.md`, "Per problem flow", part 5).

| # | Symptom in the reporting data | Where to look in the construction | What is usually there | The shape of the fix |
|---|---|---|---|---|
| **A** | Revenue and volume fell together | The start block: the event and its filter, or the schedule and its condition. The conditions before the first send, with their counts. Versions near the date of the break | The entry condition narrowed; the event's source dried up; a condition on the path started cutting almost everyone | «Condition ⟨block name⟩ passes N of M; reconsider ⟨what in it⟩», or «the source of event ⟨name⟩ stopped filling — check what writes it» |
| **B** | Volume holds, conversion or revenue fell | The send steps: the set of mailings, their channels, their profile. The conditions immediately before the send | A channel was replaced (SMS → email); a branch was added that takes part of the audience; the set of mailings changed | «Return ⟨channel⟩ to step ⟨name⟩» / «separate ⟨the two branches⟩» |
| **C** | Running, and sending nothing or almost nothing | The skeleton with counts: where it breaks off. Negative outputs leading nowhere. Condition bodies against the entry condition. **The state of the mailing on the send step** (section 7, "accepted is not sent") | **An impassable condition**: the entry takes «no order in 14 days», a condition inside passes «with an order». Or the send step is not wired. Or the mailing is unfinished, so the step renders instead of sending | «Invert condition ⟨name⟩: it requires ⟨X⟩ now, and the entry takes ⟨not-X⟩» / «finish mailing ⟨name⟩ on step ⟨name⟩ — the step renders it instead of sending» |
| **D** | Bounce share above the threshold | The send steps and every address check before them. The per-message bounce split (T3f) | No validity check; a check on the invalidity flag — that is, on history, which a fresh bad address passes; the first touch collects every bounce | «Between ⟨the address source⟩ and ⟨the first message⟩ put a check ⟨which⟩» |
| **E** | Unsubscribe share high, open share low | The entry condition: a cut-off by recency of the last reaction. `repeatSettings`. Frequency control on the mailings | The audience is taken with no activity limit; frequency is unbounded | «Add to the entry condition of ⟨block⟩ a cut-off by recency of the last open» |
| **F** | Many enter, few receive | `repeatSettings.maxRepeatCount` against where the contact and subscription checks stand | **The burnt attempt** (section 5) | «Move the checks ⟨list⟩ from blocks ⟨names⟩ into the launch conditions» |
| **G** | Revenue implausibly high for the mechanic | `mailing.isTransactional` on the send steps | A transactional mailing: attribution follows the order, not the message | Not a fix to the scenario but the withdrawal of the finding — and, where revenue is attributed to it at all, a project finding about attribution (`SKILL.md` step 4) |
| **H** | Opens below neighbouring mechanics with normal delivery | The `delayBlock`: exit window, time zone, `useCustomerTimeZone` | No window at all; a window in the wrong time zone; the first message goes out at night | «Put a window ⟨hours⟩ in time zone ⟨which⟩ on wait ⟨name⟩» |
| **I** | Two scenarios on one event, the customer receives both | `launch:` on both. Frequency control on both mailings | A migration not finished: the old scenario relaunched beside the new one | «Stop ⟨which one, and why that one⟩» |
| **J** | Executions stop with a reason | The `stops` lines in the answer with counts | Relevance expired; entity not found; the send failed | «Look into ⟨N⟩ stops with reason ⟨which⟩ in block ⟨name⟩» |
| **K** | Volume up, opens and clicks flat or down, unsubscribes up | `repeatSettings`; the number of send steps on one path; waits between them | Frequency grew on the same base — reach did not: the same people are written to more often (`business-rules.md`, "Reach × frequency") | «Lengthen the wait ⟨name⟩ from ⟨X⟩ to ⟨Y⟩» / «set the repeat limit to ⟨one entry per N days⟩» |

**Row C carries the one case that is not in the graph at all.** A mailing nobody has finished
writing is accepted by the send step, passes validation, and the platform silently switches the step
to a mode where the message is rendered instead of sent (`steps.send_mailing`,
`mechanics.best_practices` §6). Every signal that means "this worked" reports success, and nothing
is delivered. It explains «running, sending nothing» better than any guess about conditions, and it
is checked on the state of the mailing, not on the structure.

**Rows D and H are the `flow-issues-audit` skill's cases 7 and 8** (that skill's own
`references/checklist-per-flow.md` — a sibling skill in this plugin, not a file of this one), and a missing subscription or validity check found under row C is its cases 6 and 7. That checklist describes the anti-pattern from
the construction alone; this catalogue arrives at the same block from a figure. **When one of those
rows fires, the fix is worded the way that checklist words it**, so the two skills do not hand a
client two different instructions for one block.

## Form F, the burnt attempt — checked on every scenario that reaches level 2

The sign is read mechanically: **`repeatSettings` limits the number of entries per customer AND the
contact or subscription checks stand as blocks inside the graph rather than in the launch
condition.** A customer who fails the check has spent their only entry and will not come back — not
when they subscribe, not when the address becomes valid. The platform's own documentation states it
in so many words: a frequency limit counts the customer's previous execution whatever that execution
did (`overview`, "a run counts").

It costs one level-3 call at `structure=Subgraph, depth=0` — `repeatSettings` are in `settings`,
and `settings` come only at `detail=Full` — and it is **never asserted from the skeleton**: the
skeleton shows the checks, not the limit, and a limit the run did not read is a limit the run does
not know about.

**The fix is one sentence and it names two places**: the checks to move (by block name) and where
they go (the launch conditions of the start block). Then a customer who fails simply does not enter,
and keeps the attempt.

## Documented mechanics: a source of hypotheses, not a standard

The `mechanics` section of the wiki holds, per mechanic, `.overview` (what the mechanic is for),
`.decisions`, `.structure` (the usual shape) and `.blocks`, plus `mechanics.best_practices` across
them: the re-check after a deliberate wait, where an A/B test goes, why branches cascade, how a
frequency cap binds a branch that counts entries. **These are templates for building new
scenarios.** A live scenario that departs from them is not thereby defective, and the audit does not
grade it against them.

What they are for here: **when a scenario is recognisable as a documented mechanic** — by its start
event and shape, not by its name (`business-rules.md`, "Recognising a scenario's type") — read the
`.overview` and `.structure` for **what the mechanic is meant to achieve and by what means**, and
match: is that means present in this construction, and what is missing. A gap is worth naming when it
connects to the figure the finding started from — a missing re-check after the wait where
unsubscribes are high, no wait before the first message where bounces sit on it, no gate where the
entry takes everyone. It is printed as a hypothesis with the block named, never as «departs from
the standard». **What the scenario does right is named too**, in its «What is in the scenario» part —
a report made only of complaints is not a report on the scenario.

## What this reading must not do

The limits below already stand elsewhere in this skill; the construction reading loads them, so they
are repeated beside it.

- **Read only.** `flows_get` and `flows_lookup` read. Never `flows_apply_operations`,
  `flows_set_testing_mode`, `flows_create`. The audit describes a fix; it does not make it.
- **No diagnosis of content.** Subject, body, layout, images are outside the skill. «Rewrite the
  subject» is not a step of this audit, whatever the open share says.
- **No cause from a version date.** Measured on a live project: versions are published regularly on
  a scenario that is merely maintained. Version dates are a place to look, printed as a hypothesis
  with its probe — `SKILL.md § From "what" to "why"`, the change block, which nothing here relaxes.
- **No branch named where the answer does not name one.** The counts do not say which branch the
  difference left by. Name the volume and the block by its name — yes; invent a branch — no
  (`calling-the-tools.md`, "Reading the per-block funnel").
- **Not everything becomes «problem».** The provability floors are not lifted: the construction
  explains a mechanism, and the size still has to clear the floor. A scenario on 200 deliveries with
  a perfectly readable construction defect stays «can't judge» — with the difference that its line
  now names what is visible in it.
- **The budget is not widened in silence.** Section 2's limits are part of the requirement; what did
  not fit is named.
- **Settings are not inferred from the skeleton.** `repeatSettings` and `launchSettings` live in
  `settings` and arrive only at `detail=Full`. Form F is not asserted without level 3.
- **"Accepted" is not "sent".** A mailing in draft state passes validation, the write applies, a read
  returns what was written — and the step renders instead of sending (row C). Checked on the state of
  the mailing, not on the graph.
- **No grading against the wiki's mechanics.** They are templates for new scenarios; a gap they
  suggest is a hypothesis with a block named, and only where it connects to the figure.
