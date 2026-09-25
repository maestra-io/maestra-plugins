<!-- locale: en-US. Parallel variant of ../ru-RU/examples.md. Keep both in step. -->

# Flow summary — worked examples (en-US)

Two worked examples, to calibrate tone and length. Headings and labels: `terminology.md`
in this folder.

> These are captures from a test project with scrambled ids: don't open them, and don't
> reuse the call that produced one.

## Contents

- [Example 1 — Welcome flow (structure only)](#example-1--welcome-flow-structure-only)
- [Example 2 — Reading flow-run counts](#example-2--reading-flow-run-counts)

---

## Example 1 — Welcome flow (structure only)

Skeleton of a whole flow version, no run counts.

**Skeleton**

```
flow 266741 v1 rowVersion psA4AA==
B_f0a98df [inboundEventBlock "Customer subscribed to Email newsletters"] B_f0a98df:default --> B_1c80f93 [operationStepsBlockSettings "Welcome - welcome email"]
B_1c80f93 [operationStepsBlockSettings "Welcome - welcome email"] B_1c80f93:default --> B_44fb444 [delayBlock]
B_44fb444 [delayBlock] B_44fb444:default --> B_34c0d51 [conditionBlock "No orders and subscribed"]
B_34c0d51 [conditionBlock "No orders and subscribed"] B_34c0d51:positive --> B_cc8e2ad [operationStepsBlockSettings "Welcome - promo code offer"]
B_cc8e2ad [operationStepsBlockSettings "Welcome - promo code offer"] B_cc8e2ad:default --> B_b227fd9 [delayBlock]
B_b227fd9 [delayBlock] B_b227fd9:default --> B_e05c738 [conditionBlock]
B_e05c738 [conditionBlock] B_e05c738:positive --> B_5519993 [limitationBlock]
B_5519993 [limitationBlock] B_5519993:beforeLimit --> B_147bb5f [operationStepsBlockSettings "Welcome sms - promo code still valid"]
B_5519993 [limitationBlock] B_5519993:afterLimit --> B_627f6f4 [operationStepsBlockSettings "Welcome email - promo code still valid"]
```

Channel per step-group block and the exact delay durations come from the full-properties
view; the block names here already indicate Email vs SMS.

**Summary**

### Trigger

Starts on the event "customer subscribed to Email newsletters".

### Flow logic

- A welcome email "Welcome — welcome email" goes out immediately.
- Then a pause, after which the condition "no orders and subscribed" is checked: on the
  positive outcome the email "Welcome — promo code offer" goes out.
- After another pause and a condition check, a frequency-limitation block fires:
  - customers still within the frequency limit get the SMS "Welcome sms — promo code still valid";
  - customers already over the limit get the email "Welcome email — promo code still valid".

Exact pause durations are in the wait blocks' properties (the full-properties view).

### Goal

Activate a new subscriber, bring them to a first purchase and remind them of the active
promo code, while keeping SMS frequency within the configured limit.

---

## Example 2 — Reading flow-run counts

Real capture: the same skeleton view of a whole flow version, this time asking for run counts over a
three-day window in August 2026.

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

> Between 8 and 10 August 2026, 89 customers entered the flow (this version has been
> running since 6 August; counters cover roughly the last month). All 89 reached the
> condition, but nobody took the positive branch — the "Steps 2" block received no
> customers in this window. Signal: the condition currently filters everyone out, so the
> branch is worth checking.
