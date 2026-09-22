# Technical audit: per-flow checklist

Checks the agent runs for **one specific flow** (by `flowId` + `versionNumber`). This is the default
checklist when the audit is launched on a specific flow.

Each check follows the format: **how NOT to → why it's bad → what to do instead → how to check**.
The "how to check" lines rely on the flow structure (`detail`, `structure`, `depth`) only — no external
lookups. Block-type tags and output names — see `flows-tools.md` ("How to read the skeleton").

> The case numbers below are a **stable reference contract** — `examples.md` and `SKILL.md` refer to
> checks by number internally (never in the user-facing report). Keep the numbering stable when editing.

## Contents

1. [Split block instead of A/B-test block](#1-split-block-instead-of-ab-test-block)
2. [Audience filter after the start instead of in the start block (advisory)](#2-audience-filter-after-the-start-instead-of-in-the-start-block-advisory)
3. [Condition-block granularity: too many small conditions or one giant one (advisory)](#3-condition-block-granularity-too-many-small-conditions-or-one-giant-one-advisory)
4. [Customer-scoped condition instead of session-scoped in "abandoned" mechanics](#4-customer-scoped-condition-instead-of-session-scoped-in-abandoned-mechanics)
5. [No wait before checking "customer didn't do X"](#5-no-wait-before-checking-customer-didnt-do-x)
6. [Subscription check that ignores channel and topic](#6-subscription-check-that-ignores-channel-and-topic)
7. [No contact-validity check for the channel before a communication](#7-no-contact-validity-check-for-the-channel-before-a-communication)
8. [No daytime restriction on the exit from a wait block](#8-no-daytime-restriction-on-the-exit-from-a-wait-block)
9. [Recalculated segment instead of a realtime condition](#9-recalculated-segment-instead-of-a-realtime-condition)
10. [Reference: healthy flow shape](#reference-healthy-flow-shape)

---

## 1. Split block instead of A/B-test block

**How NOT to:** use a split block (`splitBlock`) for A/B tests and settle their results on imports.

**Why it's bad:** an A/B-test block guarantees that on repeat entries the same customer always goes down
the same branch (stays in one variant). A split block sends the customer to a random output on every
pass — which distorts the test results.

**What to do instead:** for A/B tests use an A/B-test block (`abTestBlock`), not a split block.

**How to check:** the structure contains a `splitBlock` whose branches lead to similar sets of steps
(variants with different content), especially with no per-customer limitation block (`limitationBlock`)
above it.

---

## 2. Audience filter after the start instead of in the start block (advisory)

**This is a trade-off, not a hard problem — offer it as an optional suggestion, and only when it's clearly a pure efficiency win.**

Two clashing realities: **efficiency/load** — filters in the start block cut clients *before* they enter, so
less processing load and faster flow processing; vs **analytics/visibility** — keeping filters as
separate steps after the start lets you see the funnel (how many clients drop at each step, whether a
condition wrongly cuts the whole audience). Both are legitimate.

**What to suggest (softly):** if a **purely static** audience filter (segment membership, presence of a
contact, a customer attribute) sits after the start **only to cut** the audience — especially with a wait
before it, so clients idle then get cut — you *may* move it into the start block to save load. But if it
could be intentional (kept separate to watch the funnel, or a scheduled flow where drop-off visibility
matters), leave it and don't call it a problem.

**Never flag** a **dynamic re-check** after a wait (did an order appear, still subscribed / valid, cart
still relevant) — that's the healthy "event → wait → re-check" shape, not an audience filter. And two
occupied branches (`:positive` **and** `:negative` lead onward) = branching, not narrowing — fine.

**How to check:** the first `conditionBlock` after the start (skipping `delayBlock`s) with only one output
occupied, filtering on static audience traits. Raise it as an optional efficiency suggestion, not a problem.

---

## 3. Condition-block granularity: too many small conditions or one giant one (advisory)

**Also a trade-off, not a hard problem — offer as an optional suggestion.** Same tension as case 2: more
separate condition blocks make the funnel easy to read and debug (you see where clients drop), but add
processing load and slow the flow down; fewer, larger blocks mean less load but it's harder to see
where the audience is cut.

Suggest a change only at the **extremes**:

- **Many narrowing conditions in a row (~5–6+)**, each single-output, on the same entity → suggest
  **grouping related checks** into fewer blocks by business meaning — e.g. put "subscribed + valid email"
  together; keep "no order in period" as its own block; keep "no communication in the last X days" as its
  own block. Group sensibly — do **not** collapse everything into one, and keep steps whose drop-off is
  worth watching separate.
- **One condition block checking too many things at once (~6–7+ filters)** → suggest **splitting** it into a
  few smaller blocks, for visibility, easier debugging, and analytics.
- **In between** (a handful of conditions, moderately sized blocks) → say nothing; this is fine.

**How to check:** count consecutive single-output `conditionBlock`s on the same entity (from the skeleton),
and the number of filters inside a block (from full detail); only suggest at the thresholds above.

---

## 4. Customer-scoped condition instead of session-scoped in "abandoned" mechanics

**How NOT to:** in "abandoned" mechanics (cart / view / category / session), describe the mechanic itself
with a condition on the **customer** rather than the **session**. E.g. "did the customer add a product to
cart?" — that could be any cart in any session, not the one belonging to the current run.

**Why it's bad:** a customer condition with no session binding catches the wrong event — the mechanic fires
on actions from other sessions, and the logic becomes wrong.

**What to do instead:** describe the mechanic with a condition on the **session** ("added a product to cart
in THIS session?", "is the product available?"). Meanwhile **general** customer conditions — whether we can
communicate at all (subscription, valid contact) — are fine and allowed.

**How to check:** a flow with an "abandoned" start event has a `conditionBlock` describing the mechanic's
target action (add-to-cart / view) on the "customer" entity rather than "session" (entity and subject come
from full detail). General subscription/validity conditions do not belong to this pattern.

---

## 5. No wait before checking "customer didn't do X"

**How NOT to:** check "the customer did NOT do X" right after the trigger event, with no wait first.

**Why it's bad:** if the event is built on the customer *not* doing something, we can't be sure they aren't
**in the middle** of doing it right now (they left the site, but may return and place the order any moment).
A check with no pause cuts or processes the customer prematurely.

**What to do instead:** add a wait between the event and the check, then re-check the condition. Typical
chain: event "customer left the site/app" → wait "maybe they'll come back and finish the order?" →
condition "did they return and complete the order?".

**How to check:** a `conditionBlock` checking the absence of a recent action ("no order", "didn't return")
sits right after the `inboundEventBlock` with no `delayBlock` in between.

---

## 6. Subscription check that ignores channel and topic

**How NOT to:** check "just a subscription to the brand" without accounting for the channel and the topic of
the message being sent.

**Why it's bad:** subscriptions are multi-level. A customer can be subscribed to the brand but not to a
specific channel. They can be subscribed to the channel but unsubscribed from all topics in it. Delivery rule:
- a message **with topic X** is delivered only if the customer is subscribed to that topic X;
- a message **without a topic** is checked only against the channel subscription.

So "subscribed to the channel, unsubscribed from all topics" → receives any message **without** a topic, but
never one with a topic; "unsubscribed from the channel, subscribed to topic X" → messages without a topic are
ignored, only messages with topic X get through.

**What to do instead:** check the subscription for the specific communication: determine the channel and
whether the message has a topic. If it has a topic — check the subscription to that topic; if not — check the
subscription to the channel.

**How to check:** for a communication step (`operationStepsBlockSettings`), take the channel and whether the
message has a topic (from full detail) and confirm there's a matching subscription check above it in the
branch (to topic X if there's a topic; otherwise to the channel).

---

## 7. No contact-validity check for the channel before a communication

**How NOT to:** send a communication without checking contact validity for the specific channel.

**Why it's bad:** high risk of undelivered messages and degraded channel "health" (for email — deliverability
and domain reputation).

**What to do instead:** before the group of communication steps, check validity for the channel being sent:
- **Email** → a valid email exists;
- **SMS** → a valid phone number exists;
- **MobPush** → the customer has the mobile app and mobile pushes are allowed in **that specific** app for this brand;
- **WebPush** → there's permission to send WebPush on **that specific** site.

**How to check:** for each communication step, determine the channel (from full detail) and confirm there's a
channel-appropriate validity check above it in the branch. No check for the relevant channel — flag.

---

## 8. No daytime restriction on the exit from a wait block

**How NOT to:** leave a wait block before a communication with no daytime restriction on its **exit**, so the
message can leave the wait at any hour.

**Why it's bad:** without it the message can go out at night.

**What to do instead:** add a **daytime restriction on the exit** from the wait block (an allowed window), so
the message never leaves the wait at night.

**When it's OK to skip the window:** only if the customer is likely **still active** at the moment they exit
the wait **and** the wait is short (~30 min). "Active" = they just did the thing that triggered the flow:
- **Event trigger implying recent activity** (e.g. "abandoned session" — they were browsing ~30 min ago)
  **+ a short (~30 min) wait right after it** → sending ~30 min later is expected even at night; a window
  isn't required — don't flag.
- **Schedule trigger** (activity unknown), a **long wait**, or a wait **deep in a cascade** (much time has
  passed, so the customer may no longer be active) → recommend a daytime exit window.
- **Can't tell** whether the customer is active → **fall back to recommending** the window.

**How to check:** a `delayBlock` before a communication whose reschedule strategy doesn't restrict the time of
day (any time allowed / no `timeFrom`–`timeTill`) — from full detail. Then judge activity from the trigger
type and the wait's length and position (right after the trigger vs later in a cascade), per the rule above.

---

## 9. Recalculated segment instead of a realtime condition

**How NOT to:** in an event-triggered flow, make a decision by membership in a **recalculated segment** where
the current state at run time is what matters (subscription, validity, whether an order was placed).

**Why it's bad:** recalculated segments refresh once a day — at run time the data may be stale (the customer
already unsubscribed/subscribed, but the segment is still old).

**What to do instead:** use a direct realtime condition (by subscription / validity / order) rather than
segment membership.

**How to check:** in an event-triggered flow a `conditionBlock` relies on membership in a recalculated segment
where the intent needs current state. Detectability is below average: to tell that the segment is actually
recalculated you need the condition's properties (full detail), and sometimes the segment's metadata too.

---

## Reference: healthy flow shape

A positive baseline, to confirm the audit doesn't flag correct flows:

1. **Precise trigger event** — spam traps and undeliverable customers excluded; audience filters placed
   sensibly (in the start block for efficiency, or kept as separate steps after the start when funnel
   visibility is the goal — both are fine).
2. **Mechanic checks** — relevant conditions (for "abandoned" — session-scoped; when checking "didn't do an
   action" — with a wait first).
3. **Validity + subscription check for the right channel/topic → the group of communication steps**, with a
   daytime exit window on waits where the customer may not be active at send time.

Plus: A/B test via `abTestBlock` (not split), condition blocks at a sensible granularity, minimal duplicate flows.
