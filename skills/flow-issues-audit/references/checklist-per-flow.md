# Technical audit: per-flow checklist

The default checklist, run on **one specific flow** (`flowId` + `versionNumber`).

Each check follows the format: **how NOT to → why it's bad → what to do instead → how to check**.
The blocks are named here by what they do — trigger, wait, condition, limit, split, A/B test, step
group — and each maps to one type tag in the wiki's flows domain index.

> The case numbers below are a **stable reference contract** — `<locale>/examples.md`, `SKILL.md` and
> the wiki (`mechanics.best_practices` cites cases 1, 2, 5 and 9 by number) refer to checks by number
> internally, never in the user-facing report. Keep the numbering stable when editing.

---

## 1. Split block instead of A/B-test block

**How NOT to:** use a split block for A/B tests and settle their results on imports.

**Why it's bad:** the A/B block is sticky per customer; the split re-randomises on every entry, so a
returning customer sees both variants and the comparison stops meaning anything
(`mechanics.best_practices` §2).

**What to do instead:** use the A/B-test block.

**How to check:** the structure contains a split block whose branches lead to similar sets of steps
(variants with different content). Whether a customer can enter twice at all is the flow version's
own `repeatSettings`, not a block — it is absent from the skeleton and from the start block, and
comes back in the flow-level settings of the full-properties view (`overview` § Flow-level settings).

---

## 2. Audience filter after the start instead of in the start block (advisory)

**This is a trade-off, not a hard problem — offer it as an optional suggestion, and only when it's clearly a pure efficiency win.**

Filters in the start block cut load; filters kept as separate steps after it show the funnel. Both
are legitimate.

**What to suggest (softly):** if a **purely static** audience filter (segment membership, presence of a
contact, a customer attribute) sits after the start **only to cut** the audience — especially with a wait
before it, so clients idle then get cut — you *may* move it into the start block to save load. But if it
could be intentional (kept separate to watch the funnel, or a scheduled flow where drop-off visibility
matters), leave it and don't call it a problem.

**Never flag** a **dynamic re-check** after a wait (did an order appear, still subscribed / valid, cart
still relevant) — that's the healthy "event → wait → re-check" shape, not an audience filter. And a
condition with **both** of its branches leading onward is branching, not narrowing — fine.

**How to check:** the first condition block after the start (skipping waits) with only one output
occupied, filtering on static audience traits. In the skeleton, an output with no outgoing edge is a
dead end — executions routed there leave the flow, which is what "only narrows" means here. Raise it
as an optional efficiency suggestion, not a problem.

---

## 3. Condition-block granularity: too many small conditions or one giant one (advisory)

**Same trade-off as case 2 — an optional suggestion, and only at the extremes:**

- **Many narrowing conditions in a row (~5–6+)**, each single-output, on the same entity → suggest
  **grouping related checks** into fewer blocks by business meaning — e.g. put "subscribed + valid email"
  together; keep "no order in period" as its own block; keep "no communication in the last X days" as its
  own block. Where the whole cascade sits on **one context**, the condition block's **multibranch**
  mode is the product's own remedy — fewer blocks, fewer repeated lookups, and branch order = priority
  (`blocks.condition` § Settings). Group sensibly — do **not** collapse everything into one, and keep
  steps whose drop-off is worth watching separate.
- **One condition block checking too many things at once (~6–7+ filters)** → suggest **splitting** it into a
  few smaller blocks, for visibility, easier debugging, and analytics.
- **In between** (a handful of conditions, moderately sized blocks) → say nothing; this is fine.

**How to check:** count consecutive single-output condition blocks on the same entity (from the skeleton),
and the number of filters inside a block (from its full properties); only suggest at the thresholds above.

---

## 4. Customer-scoped condition instead of session-scoped in "abandoned" mechanics

**How NOT to:** in "abandoned" mechanics (cart / view / category / session), describe the mechanic itself
with a condition on the **customer** rather than the **session**. E.g. "did the customer add a product to
cart?" — that could be any cart in any session, not the one belonging to the current run, so the
mechanic fires on actions from other sessions and the logic becomes wrong.

**What to do instead:** describe the mechanic with a condition on the **session** ("added a product to cart
in THIS session?", "is the product available?"). Meanwhile **general** customer conditions — whether we can
communicate at all (subscription, valid contact) — are fine and allowed.

**How to check:** a flow with an "abandoned" start event has a condition describing the mechanic's
target action (add-to-cart / view) scoped to the customer rather than to the session — the condition's
entity context and subject come from its full properties, and the wiki's condition-block document says
how that context is expressed. General subscription/validity conditions do not belong to this pattern.

---

## 5. No wait before checking "customer didn't do X"

**How NOT to:** check "the customer did NOT do X" right after the trigger event, with no wait first.

**Why it's bad:** the customer may be in the middle of doing it right now, so a check with no pause
cuts or processes them prematurely (`mechanics.best_practices` §1).

**What to do instead:** put a wait between the event and the check, then re-check the condition.
Typical chain: event "customer left the site/app" → wait → condition "did they return and complete
the order?".

**How to check:** a condition checking the absence of a recent action ("no order", "didn't return")
sits right after the event trigger with no wait block in between.

---

## 6. Subscription check that ignores channel and topic

**How NOT to:** check "just a subscription to the brand" without accounting for the channel and the topic of
the message being sent.

**Why it's bad:** subscriptions are multi-level. A customer can be subscribed to the brand but not to a
specific channel. They can be subscribed to the channel but unsubscribed from all topics in it. Delivery rule:
- a message **with topic X** is delivered only if the customer is subscribed to that topic X;
- a message **without a topic** is checked only against the channel subscription.

**What to do instead:** check the subscription for the specific communication: determine the channel and
whether the message has a topic. If it has a topic — check the subscription to that topic; if not — check the
subscription to the channel.

**How to check:** for a step group that communicates, take the channel and whether the message has a topic
(from the block's full properties) and confirm there's a matching subscription check above it in the branch
(to topic X if there's a topic; otherwise to the channel). A flow pre-filters nothing: whether the message
actually goes out is the mailing profile's decision (`flow_types` § Recipient checks in a flow). Without the
in-flow check, ineligible customers still enter the send step and the branch's numbers stop meaning
anything — and under a transactional profile, or where the mailing waives the check, the message goes out
regardless.

---

## 7. No contact-validity check for the channel before a communication

**How NOT to:** send a communication without checking contact validity for the specific channel.

**Why it's bad:** ineligible customers still enter the send step, so the branch's numbers overstate
reach — and where the mailing waives the check or is transactional, the message really does go to an
invalid contact and costs the channel's reputation.

**What to do instead:** before the group of communication steps, check validity for the channel being sent:
- **Email** → a valid email exists;
- **SMS** → a valid phone number exists;
- **MobPush** → the customer has the mobile app and mobile pushes are allowed in **that specific** app for this brand;
- **WebPush** → there's permission to send WebPush on **that specific** site.

**How to check:** for each communication step, determine the channel (from the block's full properties) and
confirm there's a channel-appropriate validity check above it in the branch. No check for the relevant
channel — flag. As with case 6, the flow itself pre-filters nothing and the outcome at the send is the
mailing profile's (`flow_types` § Recipient checks in a flow).

---

## 8. No daytime restriction on the exit from a wait block

**How NOT to:** leave a wait block before a communication with no daytime restriction on its **exit**, so the
message can leave the wait at any hour.

**Why it's bad:** without it the message can go out at night.

**What to do instead:** set the wait's exit window.

**When it's OK to skip the window:** only if the customer is likely **still active** at the moment they exit
the wait **and** the wait is short (~30 min). "Active" = they just did the thing that triggered the flow:
- **Event trigger implying recent activity** (e.g. "abandoned session" — they were browsing ~30 min ago)
  **+ a short (~30 min) wait right after it** → sending ~30 min later is expected even at night; a window
  isn't required — don't flag.
- **Schedule trigger** (activity unknown), a **long wait**, or a wait **deep in a cascade** (much time has
  passed, so the customer may no longer be active) → recommend a daytime exit window.
- **Can't tell** whether the customer is active → **fall back to recommending** the window.

**How to check:** a wait block before a communication whose exit is not restricted to an allowed time window
— from the block's full properties, where `blocks.delay` § Exit-time window names the setting that carries
the window and the switch that turns it off. Then judge activity from the trigger type and the wait's length
and position (right after the trigger vs later in a cascade), per the rule above.

---

## 9. Recalculated segment instead of a realtime condition

**How NOT to:** in an event-triggered flow, make a decision by membership in a **recalculated segment** where
the current state at run time is what matters (subscription, validity, whether an order was placed).

**Why it's bad:** a recalculated segment answers as of its last recalculation, which may be older than the
decision needs (`mechanics.best_practices` §5).

**What to do instead:** use a direct realtime condition (by subscription / validity / order) rather than
segment membership.

**How to check:** in an event-triggered flow a condition relies on membership in a recalculated segment
where the intent needs current state. Detectability is below average: to tell that the segment is actually
recalculated you need the condition's full properties, and sometimes the segment's own metadata — which is
resolved in the `entities` domain, not in the flow.
