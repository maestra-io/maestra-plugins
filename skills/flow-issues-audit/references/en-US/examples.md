<!-- locale: en-US. Parallel variant of ../ru-RU/examples.md. Keep both in step. -->

# Audit examples — calibration

Real captures of flow structure, the internal reasoning, and the **user-facing report**. These calibrate
recall (find real problems), precision (don't flag healthy or merely-debatable patterns), **and the report style**.

Each example carries the internal reasoning and then the report as the user would see it —
shown in English here; in practice write it in the user's language.

Block names inside the skeletons are rendered in English here; real flows are often named in the project's language.

---

## Example 1 — abandoned cart (clean)

Skeleton:

```
B_4c2df28 [inboundEventBlock] B_4c2df28:default --> B_e054f9c [delayBlock "Wait 30 minutes"]
B_e054f9c [delayBlock "Wait 30 minutes"] B_e054f9c:default --> B_1de3b56 [conditionBlock "No orders, no mailings. Email subscription present"]
B_1de3b56 [conditionBlock "…"] B_1de3b56:positive --> B_00b9338 [operationStepsBlockSettings "Email - abandoned cart"]
```

**Reasoning (internal):** session-scoped trigger (case 4 ok); the post-wait condition is a dynamic re-check, not a
static audience filter (case 2 n/a); valid-email + Email-channel subscription present (cases 6, 7 ok); a send window
08:00–21:00 is set (case 8 ok — and even without it, a 30-min wait right after an abandoned-session trigger wouldn't
be flagged: the customer was just browsing, so likely still active); single realtime condition, no split (cases 1, 3, 9
n/a). Nothing to flag.

**Report to the user:**

> No issues found — the flow looks correct.

Same flow merged with the favourites / view / category variants stays clean too: its mechanic
conditions branch (both outputs used), so it is priority routing, not a long single-output
narrowing chain — case 3 does not apply.

---

## Example 2 — scheduled reactivation (restraint on advisory items)

Skeleton:

```
B_2f45b64 [scheduleBlock] --> B_329bd04 [conditionBlock] :positive --> B_896e2e9 [conditionBlock] :positive --> B_543cfd8 [conditionBlock] :positive --> B_9095162 [operationStepsBlockSettings "Steps 6"]
```

**Reasoning (internal):** daily schedule; three single-output Customer conditions — orders (>180d), Email
subscription, valid email; then an Email send. Case 3 is **advisory** and only triggers at ~5–6+ conditions — three is
below that, so **no merge suggestion**. Case 2 is **advisory**: these filters sit after the start, but this is a
scheduled flow where keeping steps separate for funnel visibility is legitimate, so at most an *optional* efficiency
note, not a problem. Subscription/validity checks are correct (6, 7 ok). No delay block → case 8 n/a. No firm problems.

**Report to the user:**

> **Scheduled reactivation flow — no real problems.**
>
> _Optional (a load-vs-clarity trade-off):_ the checks "subscription + valid email" and "no order for a long time" are
> separate condition steps after the start. To cut load you could move some into the schedule's launch conditions — but
> if they're kept separate on purpose to see where the audience drops off, that's fine; leave them.

---

## Example 3 — welcome with a split block (problems + one suggestion)

Skeleton:

```
B_a486b20 [inboundEventBlock] --> B_b78e8b4 [delayBlock] --> B_eb48fe1 [conditionBlock] :positive --> B_b81d911 [splitBlock]
B_b81d911 :1(50%) --> B_2c5b5fd [operationStepsBlockSettings "Steps 2"]   (SMS)
B_b81d911 :2(50%) --> B_ab3b00f [conditionBlock] :positive --> B_0d8f573 [operationStepsBlockSettings "Copy of Steps 2"]   (Email)
```

**Reasoning (internal):** split 50/50 across SMS vs Email variants, so a returning customer is re-randomised → **problem** (case 1; the version's own re-entry setting, not a limit block, is what says whether they can return); Email
gated only by brand-level subscription and SMS by none → **problem** (case 6); no valid-email/valid-phone checks →
**problem** (case 7). Delay has a 10:00–20:00 window → case 8 ok. Segment-membership filter after start + 1-day wait,
single-output → **advisory suggestion** (case 2), not a firm problem.

**Report to the user:**

> **Welcome flow — 3 problems to fix (+ 1 optional).**
>
> - **A random split is used instead of an A/B test.** The 50/50 split (SMS vs email) sends a returning customer to a
>   random branch each time, which distorts any comparison between the two. Use the A/B-test block — it keeps each
>   customer in one variant.
> - **Subscription isn't checked for the channel being sent.** Before the email, only a brand-level subscription is
>   checked (not the email channel); before the SMS there's no subscription check at all. Check the subscription for the
>   actual channel — email before the email, SMS before the SMS.
> - **Contact validity isn't checked before sending.** Add a "valid email" check before the email and a "valid phone"
>   check before the SMS. Without it, customers with no usable contact still enter the send step, so the
>   branch's numbers overstate reach — and on a transactional mailing the message really goes to an invalid
>   contact and costs the channel's reputation.
>
> _Optional (load vs clarity):_ the segment filter sits after the start and past a 1-day wait, so customers who don't
> match wait a day only to be cut. Moving it into the launch conditions would save load — but if it's kept separate for
> funnel visibility, that's your call.
