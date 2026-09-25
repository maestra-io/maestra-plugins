<!-- locale: en-US. Parallel variant of ../ru-RU/terminology.md. Keep both in step. -->

# Report wording — en-US

The exact wording the business audit prints when the user works in English. Keys are stable across
locales: the same key in `../ru-RU/terminology.md` is the Russian variant of the same string. The
rest of the skill names a key or writes English; this file is the only home of the locale wording.

One concept, one word, for the whole report: the run picks the wording from here once, writes it
into the log, and holds it to the last line.

## Metric names — the platform's own labels

The metric names are the product's own, as its scenario report prints them in this locale. The
left column is this skill's internal word, which never reaches the reader.

| Key | Wording |
|---|---|
| `metric.revenue` | Total Revenue (First touch within data range) — the scenario report's own label for money on the send date; shortened after first use to "revenue", with the note in the header |
| `metric.revenueByOrderDate` | Total revenue — the same money on the order date; not printed, named once to explain why the two do not match |
| `metric.businessRevenue` | Total Revenue — **a different quantity**: everything the project earned in the period, the denominator of "share of revenue from mailings". Not printed by this audit, and never set beside `metric.revenueByOrderDate` without saying they are two figures |
| `metric.orders` | Orders |
| `metric.conversionToOrder` | Conversion rate — say "conversion to order"; the platform's own rate, computed over the deliveries its attribution settings admit, and never orders over all deliveries (`../rates.md`) |
| `metric.sends` | Sent |
| `metric.deliveries` | Delivered |
| `metric.deliveryRate` | Delivery Rate |
| `metric.opens` | Opens |
| `metric.openRate` | Open Rate |
| `metric.clicks` | Clicks |
| `metric.ctr` | Click Rate |
| `metric.ctor` | CTOR |
| `metric.unsubscribes` | Unsubscribes |
| `metric.unsubRate` | Unsubscribe Rate |
| `metric.spam` | Spam Complaints |
| `metric.spamRate` | Spam Rate |
| `metric.bounces` | Bounces |
| `metric.bounceRate` | Bounce Rate |
| `metric.aov` | Average order value |
| `metric.revenuePerDelivery` | Revenue per message |
| `metric.executions` | executions of the scenario |
| `metric.flowRuns` | Flow runs |
| `metric.uniqueCustomers` | Unique customers |
| `metric.customersWithDeliveries` | Customers received campaigns |
| `metric.ownLevel` | the scenario's own level, its twelve-month average — said once |

A rate carries its channel where the product does — `Unsubscribe Rate (Email)` — and its
denominator beside it where the denominator is small.

**A label belongs to a screen.** The wordings above are the product's scenario report's; the
mailings report words some of the same quantities differently. Where a label is printed, the screen
it comes from is said with it, and the same label carried by two different quantities —
`metric.revenueByOrderDate` and `metric.businessRevenue` — is never printed for both without that
sentence.

## The `flow_report` handles behind the metric names

The left column is the key above; the right column is the name `flow_report` accepts in `metrics`
(`../metrics-map.md`, "The metric vocabulary"). Handles never reach the reader.

| Key | `flow_report` metric |
|---|---|
| `metric.revenue` | `Revenue` |
| `metric.orders` | `Orders` (`Conversions` counts the same events) |
| `metric.conversionToOrder` | `ConversionRate` — asked for by name, never `Orders ÷ Deliveries` (`../rates.md`) |
| `metric.sends` / `metric.deliveries` / `metric.deliveryRate` | `Sends` / `Deliveries` / `DeliveryRate` |
| `metric.opens` / `metric.openRate` | `Opens` / `OpenRate` |
| `metric.clicks` / `metric.ctr` / `metric.ctor` | `Clicks` / `ClickRate` / `CTOR` |
| `metric.unsubscribes` / `metric.unsubRate` | `Unsubscribes` / `UnsubscribeRate` |
| `metric.spam` / `metric.spamRate` | `SpamCount` / `SpamRate` |
| `metric.bounces` / `metric.bounceRate` | `BouncesCount` / `BounceRate` |
| `metric.aov` | `AverageOrderValue` |
| `metric.revenuePerDelivery` | derived — `Revenue ÷ Deliveries` on the same row, recorded as a derivation in the log; `ConversionRevenuePerRecipient` is a different definition, read its schema line before printing it under this label |
| `metric.executions` | `flows_lookup`'s counters — the structure's own, over their own ~30-day window, not a `flow_report` metric |
| `metric.flowRuns` | `ScenarioExecutionsCount` |
| `metric.uniqueCustomers` / `metric.customersWithDeliveries` | `ScenarioClientCount` / `ScenarioClientDeliveries` — measured empty on live projects (`../invariants.md`, 5); print only where populated |
| `metric.revenueByOrderDate`, `metric.businessRevenue`, `metric.ownLevel` | not `flow_report` metrics — named to explain, never fetched |

## The four verdicts, fixed

| Key | Wording |
|---|---|
| `verdict.problem` | problem |
| `verdict.fine` | fine |
| `verdict.didNotSend` | did not send in the period |
| `verdict.cantJudge` | can't judge |
| `verdict.weakSuffix` | fine — a weak verdict |

A weak verdict is the same word with a qualifier in the same language, never a second label and
never a hybrid of two languages. The deck carries none of the four.

## Urgency labels — the deck only

A closed set of three, assigned by the rule in `../../SKILL.md` step 8.

| Key | Wording |
|---|---|
| `urgency.now` | Decide today |
| `urgency.fix` | Fix |
| `urgency.idea` | Idea |

## Report sections

| Key | Wording |
|---|---|
| `report.title` | Scenario audit — money |
| `report.section.project` | The project as a whole |
| `report.section.flowsThatSent` | Scenarios that sent in the period — {n} of {m} shown |
| `report.section.problemFlows` | The scenarios with a problem |
| `report.section.silentButLive` | Silent, but still taking people in |
| `report.section.whatToDo` | What to do |
| `report.section.whatWeDoNotKnow` | What we do not know |
| `report.group.observed` | What is observed |
| `report.group.inTheScenario` | What is in the scenario |
| `report.group.whyItMoved` | Why it moved |
| `report.group.whatToFix` | What to fix |
| `report.group.actions` | Actions |

## Report table headers

| Key | Wording |
|---|---|
| `table.header.metric` | Metric |
| `table.header.scenario` | Scenario |
| `table.header.verdict` | Verdict |
| `table.header.revenue` | Revenue |
| `table.header.orders` | Orders |
| `table.header.deliveries` | Deliveries |
| `table.header.openRate` | Open |
| `table.header.ctr` | CTR |
| `table.header.unsubRate` | Unsub |
| `table.header.whatTheVerdictRestsOn` | What the verdict rests on |
| `table.header.yoy` | Year-on-year change |
| `table.header.project` | The project as a whole |

## Deck

| Key | Wording |
|---|---|
| `deck.title` | Example: proposals for the scenarios |
| `deck.overview.heading` | Proposals for the scenarios as they stand |
| `deck.overview.more` | {n} more findings — in the full report |
| `deck.heading.whereLost` | Where exactly it is lost |
| `deck.heading.whatChecked` | What is checked |
| `deck.heading.whatThisDoesNotExplain` | What this does not explain |
| `deck.heading.inTheScenario` | What is in the scenario |
| `deck.heading.whatToDo` | What to do |
| `deck.nav.prev` | ← Back |
| `deck.nav.next` | Next → |
| `deck.nav.overview` | Overview |
| `deck.nav.proposal` | Proposal {n} |

The evidence disclosure is headed by what it shows. Never a self-assessing heading such as "Why
the comparison is fair".

## Presenter notes

| Key | Wording |
|---|---|
| `notes.heading.howToSayIt` | How to say it |
| `notes.heading.whatNotToSay` | What not to say |

## Fixed phrases

| Key | Wording |
|---|---|
| `phrase.empty` | — |
| `phrase.notMeasured` | — not measured |
| `phrase.noAttributedRevenue` | the scenario has nothing attributed to the goal in the period |
| `phrase.forWhoeverRunsTheProject` | For whoever runs the project in the platform |
| `phrase.whatWillShowItWorked` | What will show it worked |
| `phrase.whatWouldSettleIt` | What would settle it |
| `phrase.supposed` | Supposed |
| `phrase.notEstablished` | Not established — this is a supposition, and it is written as one |

Numbers are printed the way this locale prints them: `1,185,769.20`, a thousands separator and a
decimal point.
