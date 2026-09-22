# Rates — which one decides what, and what stands behind it

Every rate the audit prints comes back as a named metric on the **same `flow_report` call** as the
money and the volume (`metrics-map.md`, "the overview, in one call"). There is nothing to compute and
no denominator to assemble: `OpenRate`, `ClickRate`, `CTOR`, `ConversionRate`, `DeliveryRate`,
`UnsubscribeRate`, `SpamRate` and `BounceRate` are asked for by name, per flow in the breakdown and
for the project in `## Summary`.

That makes this file short, and moves its weight to the part that was never mechanical: **which rate
is allowed to decide what, when a rate is quotable at all, and which rate belongs to a different
population than the rest of the report.**

## Contents

1. [The handles](#the-handles) — T2, T2p, T8
2. [What the denominators are, and what that forbids](#what-the-denominators-are-and-what-that-forbids)
3. [The floors — when a rate is not quotable](#the-floors--when-a-rate-is-not-quotable)
4. [Reading a rate against a channel mix](#reading-a-rate-against-a-channel-mix)
5. [The one benchmark the platform brings — `email_health_report`](#the-one-benchmark-the-platform-brings--email_health_report)

---

## The handles

- **T2** — `OpenRate`, `ClickRate`, `CTOR`, `UnsubscribeRate` **per flow**: the rate columns of the
  overview call's `## Flows` breakdown.
- **T2p** — the same four **for the project**: the same lines in that answer's `## Summary`.
- **T8** — `BounceRate` and `SpamRate`, per flow and for the project, from the same two sections.

One call, three handles. When the audit needs rates for a second window — the month before, the same
month a year earlier — it is the same call with different dates (`beyond-the-overview.md`), and the
delta between them is arithmetic you do yourself.

---

## What the denominators are, and what that forbids

The platform computes each rate over the sends that can report the event it counts. Two consequences
carry into the report:

**A rate is not derivable from the counters beside it.** `Opens / Sends` from the same row is not
`OpenRate`: the rate's denominator is narrowed to the channels that report opens, the counter's is
not. **Ask for the rate you intend to print.** Never divide two counters and call the result a rate,
and never reconstruct a rate the call did not return.

**A rate over a mixed-channel flow is a blend.** A flow that sends both email and SMS has one
`OpenRate` row, and SMS reports no opens. The number is real and it is not comparable to a
single-channel flow's. Where a rate decides a verdict on a mixed flow, re-run the overview with
`channels` pinned to the one channel the verdict is about, and say in the row which channel the rate
covers. Channel names are exact point-of-contact system names and **case-sensitive**; an unrecognised
one returns an empty report rather than an error, so an empty answer after adding `channels` means
the name is wrong, not that the flow is silent (`calling-the-tools.md`).

**Opens are not what they were.** Inflated and suppressed open rates are both ordinary now — mail
privacy protection opens on the customer's behalf, and some clients never report. An open-rate
movement is a signal to look, never a finding on its own; a verdict that rests on opens says so and
names what would settle it (`business-rules.md`).

---

## The floors — when a rate is not quotable

The floors are the same numbers the rest of the audit uses (`SKILL.md` step 5), and they apply to
every rate in this file:

- **Below 1,000 deliveries in the window, no rate is provable.** The flow keeps its row and its
  figures; the verdict is «can't judge», with the delivery count beside it so the reader sees why.
- **Below 50 goal-attributed orders, no money verdict is.** A conversion rate over four orders is a
  number, not evidence.

Real projects produce rate values that look like defects and are arithmetic: a campaign with 1
delivery prints `100.00%` open, a flow with 11 sends prints `9.09%` unsubscribe. **A rate on a
denominator under the floor is never a finding, never a top-performer, and never goes on a deck
slide.**

The floors bite hardest where they matter most. When *no* flow clears them, the money verdict is
stated at project level from `## Summary` (T1p/T2p) and the per-flow verdict is declared unavailable
once, in the header — not repeated on every row.

---

## Reading a rate against a channel mix

Bounce and spam are the two rates that need no knowledge of what kind of scenario a flow is, which is
why an all-transactional or opt-in scenario is judged on them alone (`business-rules.md`). Two things
to hold while reading them:

**A bounce rate in the tens of percent is a real reading and a real problem.** Measured on a live
project: a welcome flow at `BounceRate 17.37%` while the project sat at `1.71%`, and one welcome
mailing inside it at `41.45%`. That is the signature of a list being sent to before it is validated —
name the flow, name the send step, and route it to the deliverability question rather than to a
content one.

**Spam rate is the rate with the smallest tolerable band.** It is usually `0.00%` and any sustained
non-zero figure on volume above the floor outranks every other rate finding in the report.

---

## The one benchmark the platform brings — `email_health_report`

The audit has no industry medians of its own. `email_health_report` has them, and it is the only
place a "good / excellent" band in this report may come from: per metric it returns the brand's
current value, the 7-day change, the industry median for the brand's own industry, the target bands
and a plain recommendation, with an optional per-inbox-provider breakdown.

```
email_health_report(tenant = <project>, brand = <brand name or system name>, windowDays = 30)
```

**It measures a different population from every other handle in this skill**, and that is the whole
care it needs:

- **one brand**, not the project (it is required, and an unknown name comes back with the list of
  brands);
- **Email only**, and **non-transactional Email only**;
- **its own window** — `windowDays`, default 30, counted back from today — which is almost never the
  audited period;
- **every mailing of that brand**, flow-sent and manual alike, not the flows.

So its figures are **never added to, substituted for, or compared row-by-row with** a `flow_report`
rate. What it is legitimately for: the **band** — whether the project's email deliverability sits
inside, near or outside its industry's normal range — and the per-provider breakdown when a bounce
or spam finding needs to be pinned to one receiving domain. Print it as its own line with its own
window and its own scope said in words, exactly as a figure from a different measurement must be
(`SKILL.md`, rule 1), or leave it out.

Its optional status is real: the audit never stops for its absence, and a project whose brand is not
resolvable simply carries no benchmark line, named once in `## What we do not know`.
