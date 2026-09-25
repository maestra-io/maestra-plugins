# Structural causes — reading the scenario's construction behind a figure

**Reporting data gives the size of a movement. The scenario's construction gives the mechanism.
A cause is established when the run holds both.** This file is the procedure that turns "go and
look at the construction" into a bounded reading, and the catalogue that says, for each symptom
the reporting data can show, where in the construction to look, what is usually found there, and
what a fix sounds like when it is written for the reader.

Read at `SKILL.md` step 6b. What a reading may conclude is `SKILL.md § From "what" to "why"`; what
is here is *how* the reading is taken and *where* it looks.

**The catalogue is not a list of diagnoses.** It says where to look and what is usually there; the
report may state only what the run saw in this scenario's construction. A symptom whose row names
three usual findings and a construction that shows none of them is a finding with an open cause,
printed as such.

---

## The reading protocol — three levels, cheapest first

The order matters: a full graph at full detail costs thousands of tokens, a skeleton hundreds.
Each level answers a question the previous one cannot; stop at the level that answers the finding's.

**Level 1 — the scenario card, `flows_get` by id. Owed for every scenario the budget admits.** The
launch line, the versions with statuses, the platform's own problems-and-warnings flag. Answers what
starts the scenario, and whether it is running (`calling-the-tools.md`, "Call arguments"). A version
published near the movement is a *place to look*, never a cause.

**Level 2 — the skeleton with executions, `flows_lookup` at the cheap detail with the counters asked
for. Owed for every scenario the budget admits.** Every edge, the count on every output, the stop
lines with their reasons, the window the counters cover. Answers where executions are lost, which
outputs lead nowhere, whether a second attempt exists downstream of a failed check — read as
"Reading the per-block funnel" below.

**Level 3 — one neighbourhood at full detail. As the finding needs.** A condition's body, the
trigger's filter, the send steps with each mailing's profile, the wait strategy — **and the
flow-level settings, which arrive at no other detail level**, whatever part of the graph was asked
for. What those settings hold is the wiki's `overview`.

> **Full detail over the whole graph is not called without a reason** — on a ten-block scenario it is
> thousands of tokens. **When the only question is the repeat limit or the working period, the cheap
> read is full detail restricted to a single block**: it returns the settings with almost no graph.

**Which version to read is `calling-the-tools.md`, "Call arguments", fallback included.** A finding
about a period the current version did not cover reads the current construction and says so.

## Budget

- **Up to seven problem scenarios and up to three top performers** receive levels 1 and 2 — the
  problem scenarios in the order step 5 produced (money at stake, then volume or reach), the top
  performers read for what to copy rather than what to fix (`SKILL.md` step 6b).
- **Up to four of those** receive level 3 — a full-detail reading of a neighbourhood, as the finding
  needs it.
- **Form F has an allowance of its own, and it is separate from those four.** The flow-level settings
  arrive only at full detail, so checking form F costs a full-detail call — but restricted to a
  single block it returns the settings with almost no graph, which is why it is budgeted apart:
  **one such single-block settings read for each scenario that reached level 2, up to ten**. It is
  not one of the four neighbourhood readings and does not consume one; a scenario that gets both
  spends one of each. Where even that read was not made, **form F is reported as "not checked" on
  that scenario** and is never asserted from the skeleton — the two honest outcomes are a checked
  form F and a named gap, and silently narrowing "every scenario that reaches level 2" to the four
  is the widening-in-silence CRITICAL rule 4 forbids.
- What did not fit is a line in `## What we do not know`, naming the scenario and what was left
  unread (`SKILL.md`, CRITICAL rule 4).
- **Whether the scenario's mailings are transactional is read before the money ranking, not here** —
  `SKILL.md` step 4, the T1t paragraph — because a scenario that should never have entered the money
  ranking must not spend this budget confirming a finding that does not exist.

This adds twelve to twenty-four calls to the run, plus up to ten single-block settings reads for
form F.

## Reading the per-block funnel — where inside a scenario people are lost

One call answers this and no other call does: the whole graph at the cheap detail with the execution
counters attached.

**The drop at a block is the arrow in, minus the arrows out.** The number in brackets on each arrow
is how many executions took that output. Where every output is wired, the outgoing numbers sum
exactly to the incoming one — measured twice on live scenarios, 447 + 1 520 = 1 967 and
6 + 54 924 = 54 930. So where they do **not** sum, the difference left through an output that the
scenario does not continue from, and that difference is the drop.

**The arithmetic has been checked against the platform's own screen** `[tool]`: the difference
computed this way is exactly what the admin panel prints at the port that leads nowhere.

**The block's own line is honest and is not a funnel — this is the trap.** A line like
`28507 in, 28506 out — 1 stopped` adds up: `out` counts **every** output, the unwired one included.
It is therefore true and useless as a measure of loss, and it reads as "one person lost" on a block
where thirteen thousand went nowhere. **Never take `in − out` as the drop.** And the line is
printed only when the block stopped someone, held someone, failed a send or is the start block — so
**a block with no line at all can be the biggest drop in the scenario**, which is how the largest
losses on three live scenarios went unremarked.

**What the answer will not tell you, and what must therefore not be written:**

- **the name of the branch the difference left by, or that it leads nowhere.** Name **the volume and
  the block, by the block's own name as the answer gives it** — "286 534 came into the check and 923
  went on" — and never invent a branch name or claim which condition sent them there;
- **people.** These are executions; the per-branch unique-customer figure came back empty in every
  observation. Say executions, or say "entries", never "customers";
- **why an execution that reached a sending block produced no send.** The gap is unexplained and
  goes to `## What we do not know` rather than into a guess.

**Three edge cases that are not findings**: neighbouring blocks disagreeing by single digits, where
the window cut a run in half; an answer with the window header and no numbers at all, which is
either a quiet month or counters that did not arrive and is indistinguishable either way; and a
version chronology saying a version ran for one day years ago while tens of thousands entered last
month — an upstream defect, not a reason to discard the counters.

**The window is the counters' own, and by default it is not the audit's period** — the header states
which window came back. Two things move it, one deliberately and one not:

- **The tool takes its own since/till arguments** (the live schema names them), so where the audited
  month falls inside the counters' retention — roughly the last thirty days — the window **can** be
  pointed at that month, and doing so is worth one attempt before an extra caveat is printed instead
  of a figure. A month that closed longer ago than the retention cannot be reached at all: the
  counters are deleted, not merely unasked for.
- **It silently shrinks to the day the version started running** when that is later, which on a fresh
  version can leave eleven days instead of thirty; asking for an earlier start is not an error — the
  window is pulled to the boundary and the answer says so.

Whatever window came back, figures from this reading carry it wherever they
are printed, and are never added to, compared with, or subtracted from figures of the audited month
unless the two windows are the same.

## Comparing two versions of a scenario — how the reading is taken

The mechanics of one optional, capped reading. What it may conclude is
`SKILL.md § From "what" to "why"`; which of the version dates may be used is
`calling-the-tools.md`, "Version run timelines — observed behaviour".

- **A scenario that starts on a schedule is outside what this reading was probed on**, so there it
  yields a supposition at best and says so. `flows_get`'s launch line shows which kind it is.
- **The fallback taken on both sides gives the same version twice, and then there is no comparison
  to report** — say the two windows could not be resolved to two versions and stop there. A run that
  reports "nothing was changed" off that is reporting its own fallback as a finding.
- **The difference between two versions is assembled here; no call computes it.** Read each version
  with `flows_lookup` by its number at the cheap detail — old versions come back — and compare the
  two answers yourself: which message blocks are named in one and not the other, which condition
  branches appeared or went. That reading does **not** establish whether an entry condition itself
  was changed: at this detail the entry block is visible and the body of its condition is not, so
  "was the entry condition rewritten" stays a question with its own probe.
- **Why it was changed is nowhere in the data.** No version carries a note of intent. "They added
  push to rescue the basket" is an invented finding wearing a plausible sentence.
- **Cost and cap: one call for the list, plus one per version read — on at most three scenarios per
  audit**, largest money at stake first. What the cap left unexamined is a line in
  `## What we do not know`, like every other cap here.

## What the wiki adds, and what it never carries

The `wiki` tool (domain `flows`) explains what the construction means; it is read, and nothing in the
report stands on it alone. The size comes from the reporting data, the mechanism from the scenario;
the wiki says what a setting seen at level 3 does. **A statement that rests only on the wiki is not a
finding.** Which documents, and when — the table is in `SKILL.md § Where to look`.

Two documents matter most to this reading:

- `overview` — what an execution is, what "a run counts" means for the repeat limit, what the
  flow-level settings hold, and the warning that **the absence of a limit is never inferred from the
  skeleton** — which is why form F below is not asserted without level 3;
- `flow_types` — the mailing profile (`isTransactional`) and what it waives; and the attribution
  paragraph that turns attributed revenue on a transactional mailing into a project finding
  (`SKILL.md` step 4).

## The catalogue: symptom → where to look → what is usually there → the shape of the fix

Every row starts from something the reporting data already shows; the last column is how a step in
"What to do" sounds when it is written for the reader (`writing-the-report.md`, "Per problem flow",
part 5).

| # | Symptom in the reporting data | Where to look in the construction | What is usually there | The shape of the fix |
|---|---|---|---|---|
| **A** | Revenue and volume fell together | The start block: the event and its filter, or the schedule and its condition. The conditions before the first send, with their counts. Versions near the date of the break | The entry condition narrowed; the event's source dried up; a condition on the path started cutting almost everyone | "Condition ⟨block name⟩ passes N of M; reconsider ⟨what in it⟩", or "the source of event ⟨name⟩ stopped filling — check what writes it" |
| **B** | Volume holds, conversion or revenue fell | The send steps: the set of mailings, their channels, their profile. The conditions immediately before the send | A channel was replaced (SMS → email); a branch was added that takes part of the audience; the set of mailings changed | "Return ⟨channel⟩ to step ⟨name⟩" / "separate ⟨the two branches⟩" |
| **C** | Running, and sending nothing or almost nothing | The skeleton with counts: where it breaks off. Negative outputs leading nowhere. Condition bodies against the entry condition. **The state of the mailing on the send step** (`mechanics.best_practices` §6 — accepted is not sent) | **An impassable condition**: the entry takes "no order in 14 days", a condition inside passes "with an order". Or the send step is not wired. Or the mailing is unfinished, so the step renders instead of sending | "Invert condition ⟨name⟩: it requires ⟨X⟩ now, and the entry takes ⟨not-X⟩" / "finish mailing ⟨name⟩ on step ⟨name⟩ — the step renders it instead of sending" |
| **D** | Bounce share above the threshold | The send steps and every address check before them. The per-message bounce split (T3f) | No validity check; a check on the invalidity flag — that is, on history, which a fresh bad address passes; the first touch collects every bounce | "Between ⟨the address source⟩ and ⟨the first message⟩ put a check ⟨which⟩" |
| **E** | Unsubscribe share high, open share low | The entry condition: a cut-off by recency of the last reaction. The repeat limit. Frequency control on the mailings | The audience is taken with no activity limit; frequency is unbounded | "Add to the entry condition of ⟨block⟩ a cut-off by recency of the last open" |
| **F** | Many enter, few receive | The repeat limit against where the contact and subscription checks stand | **The burnt attempt** (section 7) | "Move the checks ⟨list⟩ from blocks ⟨names⟩ into the launch conditions" |
| **G** | Revenue implausibly high for the mechanic | `mailing.isTransactional` on the send steps | A transactional mailing: attribution follows the order, not the message | Not a fix to the scenario but the withdrawal of the finding — and, where revenue is attributed to it at all, a project finding about attribution (`SKILL.md` step 4) |
| **H** | Opens below neighbouring mechanics with normal delivery | The `delayBlock`: exit window, time zone, `useCustomerTimeZone` | No window at all; a window in the wrong time zone; the first message goes out at night | "Put a window ⟨hours⟩ in time zone ⟨which⟩ on wait ⟨name⟩" |
| **I** | Two scenarios on one event, the customer receives both | `launch:` on both. Frequency control on both mailings | A migration not finished: the old scenario relaunched beside the new one | "Stop ⟨which one, and why that one⟩" |
| **J** | Executions stop with a reason | The `stops` lines in the answer with counts | Relevance expired; entity not found; the send failed | "Look into ⟨N⟩ stops with reason ⟨which⟩ in block ⟨name⟩" |
| **K** | Volume up, opens and clicks flat or down, unsubscribes up | The repeat limit; the number of send steps on one path; waits between them | Frequency grew on the same base — reach did not: the same people are written to more often (`business-rules.md`, "Reach × frequency") | "Lengthen the wait ⟨name⟩ from ⟨X⟩ to ⟨Y⟩" / "set the repeat limit to ⟨one entry per N days⟩" |

**Row C carries the one case that is not in the graph at all**: an unfinished mailing renders
instead of sending, and every signal that means "this worked" reports success (`steps.send_mailing`,
`mechanics.best_practices` §6). It is checked on the state of the mailing, not on the structure.

**Rows C, D and H name blocks that are also structural anti-patterns the `maestra:flow-issues-audit`
skill checks** — that skill arrives at them from the construction alone, this catalogue from a figure. Run
that skill for a technical audit of the same scenario; a fix worded here should read as one
instruction with what it would say, not as a second one.

## Form F, the burnt attempt — checked on every scenario that reaches level 2

The sign is read mechanically: **the flow's settings limit the number of entries per customer AND the
contact or subscription checks stand as blocks inside the graph rather than in the launch
condition.** A customer who fails the check has spent their only entry and will not come back — not
when they subscribe, not when the address becomes valid. The platform's own documentation states it
in so many words: a frequency limit counts the customer's previous execution whatever that execution
did (`overview`, "a run counts").

It costs one full-detail call restricted to a single block — the settings come only at full detail,
and so restricted the call returns them with almost no graph. **That call is the form-F allowance of
the "Budget" section above, one per scenario that reached level 2 and separate from the four
neighbourhood readings**, so the check does not compete with them. It is
**never asserted from the skeleton**: the
skeleton shows the checks, not the limit, and a limit the run did not read is a limit the run does
not know about — a scenario whose allowance went unspent carries "form F not checked" and no
verdict on it.

**The fix names two places**: the checks to move, by block name, and the launch conditions of the
start block they go into — then a customer who fails does not enter and keeps the attempt.

## Documented mechanics: a source of hypotheses, not a standard

The wiki's `mechanics` documents are **templates for building new scenarios**. A live scenario that
departs from them is not thereby defective, and the audit does not grade it against them.

**When a scenario is recognisable as a documented mechanic** — by its start event and shape, not by
its name (`business-rules.md`, "Recognising a scenario's type") — read the `.overview` and
`.structure` for **what the mechanic is meant to achieve and by what means**, and ask whether that
means is present here. Name a gap only where it connects to the figure the finding started from — a
missing re-check where unsubscribes are high, no wait before the first message where bounces sit on
it — and print it as a hypothesis with the block named, never as "departs from the standard".
**What the scenario does right is named too**, in its "What is in the scenario" part.

## What this reading must not do

**Not everything becomes "problem".** The provability floors are not lifted: the construction
explains a mechanism, and the size still has to clear the floor. A scenario on 200 deliveries with a
perfectly readable construction defect stays "can't judge" — with the difference that its line now
names what is visible in it.
