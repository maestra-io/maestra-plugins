# Business rules — how a scenario is judged, and what may be recommended

The rules of marketing judgement this audit applies once the figures are in hand.

**Where a rule here and a flows-wiki document disagree, the wiki is the domain's statement and this
file is corrected.**

---

## The five kinds of scenario, and the metric each is judged by

**Five kinds, and no others.** A scenario is filed under one of these, or its kind is said to be
unclear — never under a label of the run's own making ("high-engaging", "cold", "hot"): the product
has no such categories and a reader cannot check what rule sorted the scenarios into them.

| Kind | Examples | Judged by | Not judged by, and why |
|---|---|---|---|
| **Trigger on behaviour** | abandoned cart / view / session, price drop, back in stock | revenue per send, click share, unsubscribe share | **volume** — it follows the site's traffic and the event's source. A fall in sends is not a technical defect of the scenario by itself, and "send more" is not a recommendation (`structural-causes.md`, row A for where a fall does come from) |
| **Engagement** | welcome, birthday, loyalty, content chains | open share, click share, unsubscribe share | **revenue alone** — a low return is a reason to modify, never to stop |
| **Reactivation of buyers** | "no order for N days", win-back | **unsubscribe share only** (≥ 1 % is high and expected); the growth of the active base over 60–90 days where the project measures it | revenue per send — it is expected to be low, and a reactivation is not stopped for it |
| **Reactivation of readers** | "did not open for 60+ days", "inactive email" | open share, unsubscribe share | revenue — the job is base hygiene, not sales |
| **Post-purchase** | thank-you, review request, second-order incentive | conversion to the second order, revenue per send | — ; a weak one is modified, not stopped; its absence on a project is a critical gap |

Two more classes stand outside the five and outside the marketing metrics altogether — the
transactional and the opt-in mailings ("What is never judged on money"). **The report says which job
it assigned a mechanic and on what basis**, and the basis is the construction — the start event and
the entry filter — never the name alone and never the figures.

## Recognising a scenario's type

**From the construction, not from the metrics and not from the name.** The level-1 and level-2
reading of `structural-causes.md` gives the start event and the entry filter, and those decide:

- starts on the session ending, a product list changing, a price change → trigger on behaviour;
- starts on a customer appearing, a subscription being confirmed, a birthday date → engagement;
- starts on a schedule with a filter on days since the last order → reactivation of buyers;
- starts on a schedule with a filter on days since the last open or click → reactivation of readers;
- starts on an order being paid, delivered, or its status changing, and sends a marketing mailing →
  post-purchase; sends a transactional mailing → order status, outside the five.

**The name is a hint, not the basis**: a scenario called "Welcome" that starts on an order event is
not the welcome mechanic. **The figures are never the basis**: a conversion pattern never identifies
a kind. Where the construction leaves the kind unclear, the report says so and judges the scenario
by the metrics that need no kind — unsubscribe share, bounce share.

**One scenario can hold several mechanics** — an "abandoned session" chain commonly carries the
cart, the view and the category branches — and the coverage of a mechanic on a project is read
from what the scenarios send, not from their names. "This project has no abandoned-cart mechanic"
is a claim about every scenario's branches, not about the list of names. And **a specialised
scenario is not compared head-on with a multi-purpose one**: "Abandoned cart" against "Abandoned
session" compares two audiences and two logics, and a lower revenue per send on the wider one after
a narrower one was launched is the expected shape, not cannibalisation.

## What is never judged on money

- **Transactional mailings** — order confirmations, status changes, authorisation codes, subscription
  confirmations sent with a transactional profile. Attribution follows the order the customer was
  already placing, so revenue attributed to them is not the scenario's doing. A scenario whose
  mailings are all transactional (read off its send steps' mailing profile — T1t, `SKILL.md` step 4)
  **gets no money verdict and is not in the money ranking**; its row stays, with its revenue printed and the words
  "revenue on a confirmation message follows the order, not the message" beside it. A mixed scenario
  is ranked with that caveat on its line.
- **Opt-in mailings** (the confirmation request itself) carry a profile of their own, distinct
  from transactional (`flow_types`), so the T1t reading may not show them — they are recognised at
  level 3 by the send step's mailing, or by the scenario's start on a subscription-status event.
  They are judged by what they produce — confirmation requests sent, confirmations obtained where
  the project measures them — never by revenue.
- **A/B-test variants** are read as a test, not as a mechanic: their conversion and revenue are not
  the scenario's figures until the test has settled.
- **A scenario aimed at a segment that does not buy by construction** — a pre-churn or churn
  reactivation, a welcome chain before the first order — has a structural zero on attributed
  revenue whenever the customer who does buy leaves the segment first. It is judged by the metrics
  of its kind (section 1) and, where the project measures it, by the movement of the active base.
- **A channel with no sends is "not used", never "ineffective".**

## Health: thresholds and the benchmark rule

**Every "good" and every "bad" names what it was measured against.** The comparisons, in the order
they are reached for: the project's own rate over the same window; the scenario's own year-ago
value; the industry median that `email_health_report` carries for email; the thresholds below.

**Where `email_health_report` is available, its own calibrated ranges govern the verdict on
deliverability** — it says, for instance, to keep spam under 0,2 % of deliveries. The thresholds in
the table below are this skill's, stricter, and are used when the tool is not there; where both are
printed, the tool's range is the one the verdict rests on and this skill's figure is quoted as the
platform's own guidance beside it.

| Figure | Threshold | Reading |
|---|---|---|
| Bounce share | above 2 % of sends | base hygiene, and a domain-reputation matter that comes **before** revenue — a steadily high bounce or a rising spam share is looked into first (`structural-causes.md`, row D) |
| Spam-complaint share | above 0,05 % of deliveries | the same |
| Unsubscribe share | more than twice the project's own over the same window, or above 0,5 % on a marketing mailing | fatigue or a wrong audience (row E) — with one exception: on a buyer reactivation 1 % is expected |
| Open share, pre-churn audience | below 10 % | the audience is not reading; a reactivation on it by email has a ceiling under 1 % once a year has passed without interaction |
| Conversion to order | below 0,05 % on more than 500 000 deliveries | a "noisy" scenario: informational ones are the norm and are not stopped; a selling one is rebuilt |
| Conversion to order | above 1 % | an effective selling scenario — a candidate to scale, said as a strength |

**Both conversion rows are read on the product's own rate** — `flow_report`'s `ConversionRate`,
which the platform computes over the deliveries its attribution settings admit — never
`Orders ÷ Deliveries` from the counters beside it (`rates.md`, "What the denominators are, and what
that forbids"). A conversion computed over all deliveries is a different, lower number, and a
threshold applied to it fires on scenarios that are fine. Where the rate comes back empty the line
says the volume is not attributable rather than that nobody converted.

**Thresholds are not verdicts.** What turns a gap into "problem" is still the provability floor and
the traps of `findings-and-failures.md`; a threshold is the comparison the verdict names.

**A falling series beats a level.** A scenario whose click share went 2,3 → 1,1 inside the window
on unchanged volume is a degradation even when its average sits above the project's; print the
direction, not the mean (`findings-and-failures.md`, "against an unexamined base").

Beside every share stands its absolute count; the provability floors themselves are
`findings-and-failures.md`, "Materiality before signal".

## Decomposing a change in revenue

`revenue ≈ deliveries × conversion to order × average order value` — an approximation, not an
identity, because the platform's conversion rate is computed over the deliveries its attribution
admits and revenue is earned over all of them (`rates.md`, "What the denominators are, and what that
forbids"); where the two denominators are far apart the decomposition is read for direction and not
for a product of exact factors. **Name the dominant
factor by its multiple** — the one that moved most — and show the funnel for both periods side by side:
sends → deliveries → open share → click share → conversion → average order → revenue → unsubscribe
share. The reading per factor:

| What moved | Where the cause usually is |
|---|---|
| sends fell, the rest holds | the input: the entry, the event's source, a stopped or cut chain (`structural-causes.md`, row A) |
| sends hold, deliveries fell | deliverability — the address source, a channel gone bad (row D) |
| deliveries hold, opens or clicks fell | the audience first, the content second (section "audience before content" below); the send time (row H) |
| clicks hold, conversion fell | the landing, the assortment, the price — **or the attribution lag on a fresh window** (`findings-and-failures.md`, "Compare like for like") |
| conversion holds, volume fell | not a defect of the mechanic: it is fed less. Volume is the finding, and its cause is upstream of the send (row A) |

**Channel first.** Before a scenario is blamed, the change is split by channel: a fall in every
channel is a common factor (base, season, traffic); a fall in one channel is that channel's; the
channels in order and one scenario down is the scenario's. On a single-channel project the step
collapses, and that is itself the statement "the channel is not the reason".

**Before "the mechanic was lost", check for a replacement**: a new scenario with the same start
event and the same job that took the audience is a move, not a loss (`findings-and-failures.md`,
"check for a replacement").

**Audience before content.** Opens and clicks are first a function of whom the message reached,
and only then of what it said. A low open share on a wide entry filter is not "bad content"; it is
a wide filter. This audit never reads content, so the content half is never its finding — the
audience half is read off the entry condition at level 3.

## Reach × frequency — the two halves of "volume moved"

"Sends rose" is ambiguous, and the two readings call for opposite fixes. **Reach** is how many
distinct people the scenario wrote to; **frequency** is how many times each. More people is growth
of the base or of the entry — healthy, and the fix if any is upstream (the subscription form, the
opt-in). More times per person on the same base is re-sending — opens and clicks fall, unsubscribes
rise — and the fix is inside the scenario: the wait between steps, the repeat limit
(`structural-causes.md`, row K).

What this audit reads: the reporting data's sends and deliveries (volume), the start block's
execution count (reach into the scenario, ~30-day window, `flows_lookup`) — and, **only where the
platform populates it**, `flow_report`'s per-customer family: `ScenarioClientCount` (distinct
customers who entered), `ScenarioClientDeliveries` and `ScenarioClientAvgDeliveries` (customers
reached and messages per customer), which settle reach against frequency directly. That family is
measured empty on live projects (`invariants.md`, 5): where it is zero beside non-zero executions,
**frequency is a hypothesis here, never an established cause**, and the probe is those very figures
on a project that populates them, or an export of messages per customer for the month.

## What a recommendation has to contain

Five things, and a recommendation missing one is a question, not a step
(`writing-the-report.md`, "Per problem flow", part 5):

1. **the scenario or the mailing**, by name;
2. **the place** — a block, a setting, a condition or a data source, by its name in the scenario;
3. **the action** — a verb that can be carried out: move, invert, add, lengthen, stop, finish. Not
   "improve", not "reconsider", not "look into" (a probe is written as a probe, in part 4);
4. **the reader who does it** — the project's marketer, whoever runs the project in the platform,
   whoever owns the address source (`writing-the-report.md`, "Written for both readers");
5. **the metric that will show it worked, and over what window** — "bounce share of the first
   message, next full month".

**Specific down to the setting.** Not "improve the abandoned cart" but "lengthen the wait ‹two
hours› to a day; add a second message after 24 hours to those with no order; set the repeat limit to
one entry in three days". A marketer has to be able to build it in the platform from the sentence,
without guessing. Where a mechanic is missing altogether, the wiki's `mechanics.<mechanic>.structure`
is the shape to describe.

**Before "add channel X"** — the construction already says whether the scenario sends on X (level 3,
the send steps). A channel present is not "launched"; the recommendation is then about its timing or
its condition. Before mobile push or in-app, the project has a mobile app or the recommendation is
not made.

**An expected effect is a formula with sourced inputs**, or it is not printed: the share comes from
this project's own analogous mechanic (the second message's conversion where the first is being
added to), the volume from the run's own figures, and a benchmark is a ceiling, never the forecast.
"+15–20 %" with no source is a number no call returned (`SKILL.md`, CRITICAL rule 1).

## What is never recommended

- **Stopping an engagement scenario** (welcome, birthday, loyalty) for low revenue — it is judged by
  open, click and unsubscribe shares, and modified.
- **Stopping a reactivation** for low revenue per send — it is judged by unsubscribe share.
- **Sending more from a trigger on behaviour** — volume follows traffic.
- **Merging welcome chains from different subscription forms** — each form has its own context and
  incentive.
- **Merging different price-drop scenarios** — they start on different system events.
- **Changing the site** — buttons, forms, interface.
- **Changing a message's text or design** — this audit never reads content.
- **"Keep monitoring"** — not an action.
- **Closing a channel** whose automatic scenarios bring most of its revenue at a healthy unsubscribe
  share, because its bulk mailings look weak — a channel is judged by its best mechanics.
- **Adding a paid channel** (SMS, messengers) to a project that does not use it, without a stated
  economic reason; **adding web push** as anything but a low-priority idea — its reach is weak.
- **Restarting a scenario that has not sent for three months or more** on the strength of its old
  figures alone — its state is established from the version statuses, and the recommendation stands
  on that state, on what it earned while it ran, **and on an established cause for why it stopped**
  (`SKILL.md § From "what" to "why"`, the restart paragraph).

## Ranking findings and recommendations

**Money first, where the finding has a figure; volume or reach where it has none**
(`SKILL.md § From "what" to "why"`, the ranking paragraph) — and the report says which key ranked
the list. Within that order two ladders apply:

- **higher**: a critical gap in the funnel (no welcome chain, no post-purchase chain), a base
  mechanic missing altogether, a key metric down more than ten per cent, a hygiene threshold
  breached (section 4);
- **lower**: tuning a mechanic that works, a timing change, a content idea.

Among steps whose money is within noise of each other, first the one that can be done without
anyone's help. How many scenarios are taken through in full, and what happens to the rest, is
`writing-the-report.md`, the frame.

## A/B ideas

A test is proposed where a step can be settled by one, and it is written with five things: the
scenario, the variable (one), the criterion, the audience size the scenario reaches, and the
duration.

- **The criterion is money or conversion, not opens or clicks.** The variant that wins on opens
  often loses on revenue; open share is a vanity criterion, click share an intermediate one.
- **The test goes at the end of the branch, on the message**, with the trigger, the waits and the
  gate shared — and it is the A/B block, never a random split (why: `mechanics.best_practices` §2,
  `blocks.ab_test`).
- **Enough volume.** A test is not proposed on a scenario whose monthly conversions are in the tens:
  it will not settle. The audit's own provability floors are the first estimate — under 50 orders a
  month, no money criterion is testable in a month.
- **Duration one to two full weeks at least**, no stopping at the first significant reading, and
  "no significant difference" is not "the variants are equal" — it is often too little volume.

## Attribution, in the reader's words

- The model is **attribution by the last non-direct touch**: an order goes to the last marketing
  message before it that was not a direct visit. Never "last click".
- Every revenue figure is **"by attribution"** — an upper bound on the scenario's contribution, not a
  measured increment. An increment is measured by a control group, and this audit does not have one.
- **One goal per figure** (`SKILL.md` step 2); revenue across goals or across channels is never
  summed — the same order is attributed in each.
- A **service message right before an order takes the order's revenue** from the marketing message
  that brought the customer — which is why transactional mailings are excluded from attribution by
  design, and why revenue attributed to one on this project is a finding (`SKILL.md` step 4).
- A **fresh window is understated** while attribution keeps arriving — up to thirty days
  (`findings-and-failures.md`, "Compare like for like").
