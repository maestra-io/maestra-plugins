# Flow summary — worked examples

These calibrate tone, length, and structure. Each example shows a **real skeleton**
(captured from the live flow tools) and the summary to aim for. See `flows-tools.md`
for the line format and `flows-wiki.md` for decoding block meanings.

> **Every summary describes only what its shown structure contains** — no invented
> channels, delays, or fallbacks. That is the point of the skill; the examples must
> model it. What the skeleton doesn't show (exact delay durations, filter bodies) is
> named as "needs the Full view" rather than guessed.
>
> These are real staging captures with **flow ids scrambled** — don't try to open them.

## Contents

- [Example 1 — Welcome flow (structure only)](#example-1--welcome-flow-structure-only)
- [Example 2 — Reading flow-run counts (includeExecutions)](#example-2--reading-flow-run-counts-includeexecutions)

---

## Example 1 — Welcome flow (structure only)

Real capture: `flows_lookup(flowId=266741, versionNumber=1, detail="Skeleton", structure="Full")`.

**Skeleton**

```
flow 266741 v1 rowVersion psA4AA==
B_f0a98df [inboundEventBlock "Customer subscribed to Email"] B_f0a98df:default --> B_1c80f93 [operationStepsBlockSettings "Welcome - greeting email"]
B_1c80f93 [operationStepsBlockSettings "Welcome - greeting email"] B_1c80f93:default --> B_44fb444 [delayBlock]
B_44fb444 [delayBlock] B_44fb444:default --> B_34c0d51 [conditionBlock "No orders and subscribed"]
B_34c0d51 [conditionBlock "No orders and subscribed"] B_34c0d51:positive --> B_cc8e2ad [operationStepsBlockSettings "Welcome - promo code offer"]
B_cc8e2ad [operationStepsBlockSettings "Welcome - promo code offer"] B_cc8e2ad:default --> B_b227fd9 [delayBlock]
B_b227fd9 [delayBlock] B_b227fd9:default --> B_e05c738 [conditionBlock]
B_e05c738 [conditionBlock] B_e05c738:positive --> B_5519993 [limitationBlock]
B_5519993 [limitationBlock] B_5519993:beforeLimit --> B_147bb5f [operationStepsBlockSettings "Welcome sms - promo code still valid"]
B_5519993 [limitationBlock] B_5519993:afterLimit --> B_627f6f4 [operationStepsBlockSettings "Welcome email - promo code still valid"]
```

Channel per operation-steps block and the exact delay durations come from the Full
view; the block names here already indicate Email vs SMS.

**Summary**

### Trigger

Starts on the event "customer subscribed to Email".

### Flow logic

- A greeting email goes out immediately — "Welcome - greeting email".
- Then a pause, after which the condition "no orders and subscribed" is checked: on the
  positive branch the email "Welcome - promo code offer" goes out.
- After another pause and another condition, a frequency-limit block decides the channel:
  - within the limit (beforeLimit) an SMS goes out — "Welcome sms - promo code still valid";
  - over the limit (afterLimit) an email goes out instead — "Welcome email - promo code still valid".

The exact pause durations are in the delay blocks' properties (Full view).

### Goal

Activate a new subscriber, carry them to a first purchase, and remind them the promo code
is still live — while keeping SMS frequency inside the set limit.

---

## Example 2 — Reading flow-run counts (includeExecutions)

Real capture: `flows_lookup(flowId=296412, versionNumber=1, detail="Skeleton",
structure="Full", includeExecutions=true, executionsSince="2026-08-08",
executionsTill="2026-08-10")`.

**Skeleton with executions**

```
flow 296412 v1 rowVersion rMm6Bg==
executions counted 2026-08-08 - 2026-08-10 | version 1 ran: 2026-08-06 - now
B_f2dd430 [conditionBlock] B_f2dd430:positive --> B_bbe315c [operationStepsBlockSettings "Steps 2"]
B_3fd3570 [inboundEventBlock] B_3fd3570:default --> B_f2dd430 [conditionBlock]  (89)
B_3fd3570 [inboundEventBlock]: 89 in, 89 out
```

How to read it: 89 executions entered on the inbound event and all 89 passed to the
condition. The condition's `:positive` edge carries **no number**, so **0** of those 89
took the positive branch in this window — nobody reached "Steps 2". The inbound line
(`89 in, 89 out`) is a clean pass-through, not a drop.

**Run-informed note to fold into the summary (only when the caller asks for one):**

> Over 8–10 August 2026, 89 customers entered the flow (this version has been running since
> 6 August; counters exist for roughly the last month). All 89 reached the condition, but not
> one took the positive branch — the "Steps 2" block received nobody in that window. Signal:
> the condition is currently filtering everyone out; the branch is worth checking.

Keep run figures separate from the structural description, and always state the
counting window — counts older than ~30 days aren't persisted.
