# Findings and failures — what counts as a finding, and what to do when a call fails

Four catalogues, read at the moments the audit judges: the traps that turn a successful answer into a
wrong verdict; the triage table for a tool that refuses, fails or answers with something that is not
data; the handover check; and the reader's vocabulary — what an empty value is printed as, and what
each word of ours becomes on the surface.

## Contents

1. [What is a finding and what only looks like one](#what-is-a-finding-and-what-only-looks-like-one)
2. [If something goes wrong](#if-something-goes-wrong)
3. [The handover check](#the-handover-check)
4. [How an empty value is printed](#how-an-empty-value-is-printed)
5. [Our words and the reader's](#our-words-and-the-readers)

---

## What is a finding and what only looks like one

- **«Fine» owes a comparison exactly as much as «problem» does.** Every judgement names what it was
  measured against — the project's own rate over the same window (T2p, T8's rollup row), the same
  window a year earlier, the industry median `email_health_report` carries for email — or says
  there is no benchmark, which makes the verdict weak and printed as weak. An unsupported «fine» is
  repeated to the client as readily as an unsupported «problem», and it is the one that stops anyone
  looking again.
- **A class is not a benchmark.** «Normal for a reactivation» names a category, not a measurement.
  If a comparison for that category is in the run's hands, it is applied and its number printed; if
  none exists, the verdict is weak or «can't judge». A figure below a benchmark is not thereby a
  finding either — the floor and the traps below still decide.
- **An unresolved channel does not give a low rate — it gives an enormous one.** T2's
  `unresolvedChannels` is read on every row: anything in it, the flow's rates are `—` with the
  channel named (`rates.md`, T2, property 1).
- **A rate on a multi-channel aggregate is not a rate.** Opens near zero on a flow that sends mostly
  push is the channel mix. Use T2's narrowed denominators; an aggregate rate, if quoted at all, is
  said to be one.
- **One effect across every flow is one project-level finding**, not N degradations — named once,
  with the cause marked unestablished after the readings the run holds have been spent.
- **Compare like for like.** Closed, comparable periods. The fresh side of any pair is understated
  while attribution keeps arriving (up to 30 days), so a fall against a settled month is «at most
  this much, partly an artefact of the window»; a rise is the safe direction. Opens and clicks on
  the newest two to three days are still arriving too, so a rate whose window ends inside that tail
  is qualified the same way. **A month is the wrong unit for a mechanic that sends in bursts**:
  before a month-on-month verdict, look at the daily shape of that scenario's sends (T1m at day
  grain); concentrated in a handful of days, the comparison is not a measurement and the verdict is
  «can't judge» with that probe. Where seasonality is plausible, the year-ago cut decides.
- **A year-on-year fall against an unexamined base is not a finding.** Two points make a delta,
  never a level. Every delta is stated beside the flow's own twelve-month level (T1, T2 over the
  twelve closed months); where the verdict would rest on the level, see the thirteen months one by
  one (T1m) — an average of a series that fell through the year describes no month the flow has had.
  Count the months with sends off T1m's rows, never with an aggregate over the unbucketed T1 (a
  flow has several rows per month). A series that no month resembles is printed as its shape with
  the first-to-last ratio, and the average is not printed as the level. Year down while the flow
  sits at its level → both printed, verdict a step down, handed over as a question with both
  comparisons.
- **A flow id outlives the mechanic it names.** T11's message-set overlap guards T10: clean, the
  delta is plain; above zero, the delta carries the warning naming which side has the extra
  mailings, and it goes to the CSM as a question — never dropped, never stated as a result.
- **Before «the mechanic was lost», check for a replacement** — a successor scenario with the same
  job that took the audience is a move, not a loss (`business-rules.md`).
- **Running or not is read from the version statuses; never from send dates and never from the
  `active version` line** (`calling-the-tools.md`, the status table). When it stopped is bounded by
  the last month with sends and printed as bounds. Presence in the reporting data and status are
  independent facts in both directions.
- **Materiality before signal, and the floor is a number written down here.** Below 1 000
  deliveries in the window no rate is provable; below 50 goal-attributed orders no money verdict is.
  The floors are about provability, not importance: a flow under them keeps its row and its figures,
  takes «can't judge» with its count, and the probe is a longer window. **A floor with no exit is a
  refusal to work**: when no flow clears it the audit answers at the coarsest level that does (the
  project, T1p) and says once that the finer level is not provable. The report states the split as a
  number — how many confident, how many «can't judge», which floor.
- **A rate that falls on unchanged volume is a finding in its own right**, and the year-ago window
  shows it: the volume on both sides clears the floor, the movement is relative to the flow's own
  year-ago value, the project's other flows on the same channel did not move the same way, and where
  both are present clicks and orders moved together (which rules out «only the attribution broke»).
  T11 clean is required first.
- **Do not rank flows whose figures differ within noise.** Say the spread is inside noise.
- **Judge a mechanic by the metric its job implies**, and name which job you assigned and on what
  basis — the construction, never the name alone and never the figures
  (`business-rules.md`, "The five kinds").
- **Conversion holds, volume fell — the mechanic is not broken, it is fed less.** The finding is the
  volume; its cause is upstream of the send — the entry, the event's source
  (`structural-causes.md`, row A).
- **Stay inside what you can see.** No recommendations about subject lines, copy or layout. No
  «activate the channel, the base is collected» for a channel with no sends.
- **A reporting artefact is not an achievement.** Sends equal to deliveries with non-zero bounces
  means deliverability is not measured on that project — never 100 %.
- **A material anomaly whose cause you did not establish is a hypothesis, worked on before it is
  handed over.** Spend the six sources of `SKILL.md § From "what" to "why"` first; what they do not
  settle is a supposition with its probe. A supposition whose probe cannot be named is dropped — the
  supposition, not the observation.
- **A flow that delivered nothing is not thereby harmless.** The reporting data holds no arrivals; the one
  reach figure is `flows_lookup`'s start-block count over ~30 days. Which five flows get the probe:
  stopped earners by twelve-month revenue first, then never-sent ones by the reach their mechanic
  implies (abandoned cart, view, session, welcome admit orders of magnitude more than a narrow
  mechanic), at most one per repeated name stem. The verdict stays «can't judge» with a probe — a
  diagnosis here is a false finding on every paused flow of the project.

## If something goes wrong

Read-only skill, so blast radius is small — but a number quoted to a client is not retractable.

| Situation | What to do |
|---|---|
| A required tool is missing / not enabled / access denied | Stop per `SKILL.md § Prerequisites`, print no figure, name **which** of the three kinds it is and the toggle that gates it (`invariants.md`, "A tool that is not available reads three different ways"). |
| **The answer is a bare sentence where the JSON array should be** (`An error occurred. Please try again or ask support.`) | A failure, not data — the tool emits no failure marker, so check the shape of every answer before computing on it. Treat as a failed query. |
| The overview call fails opaquely | If a `goalName` was passed, re-run once without it — a wrong goal returns the same opaque text (`invariants.md`, 6). Otherwise retry on the transport budget below and spend all of it; **then stop with no figure**, naming the window. |
| `Unable to connect. Is the computer able to access the url?`, or the protocol prefix with nothing after the tool name | The transport dropped — nothing about the call caused it. Retry the same call unchanged, **never immediately**: these stalls run one to three minutes and take the whole connection, so keep retrying while the attempts span less than about three minutes, at most three retries, putting the next useful call between attempts. If that call fails the same way, the connection is down — spend the budget once, resume when anything answers. Past the budget, stop for that call; what the loss costs is decided by which call it was. |
| A query failed | Retry delayed; narrow it (shorter period, fewer columns) **only when the text names something about the query**. Budget spent → the loss is one figure: name the metric in `## What we do not know` and move on. Never substitute a neighbouring figure. |
| A protocol-level error (`An error occurred invoking '…': …`) | Read the text after the colon. `Tool 'X' is not enabled` or `Access denied` is a gate: do not retry; required tool → stop, optional → continue and name the loss. No text → the transport row. |
| A call fails with an empty error while a neighbouring form of the same call succeeds | An argument shape, not the transport: re-read the tool's schema and remake the call (`calling-the-tools.md`, "Call arguments"). No retry budget spent. |
| A missing table, a division by zero and a refused table name | Byte-identical text; the cause is not recoverable from the answer. Do not diagnose it. |
| The answer is far larger than expected, or the host spills it to a file | Add the missing pin (most often `mailingSourceId` on T3f), never a blind `LIMIT`. |
| The breakdown header says `top N of M` with M above N | Not a stop, and not optional to fix. Raise `topN` to 200 and page with `excludeFlowIds`; a project classified from a capped breakdown is a wrong report, not a partial one (`invariants.md`, 2). |
| A flow's T1 row and its T3f sum disagree | That flow's figures are not quotable: print both, name the mismatch, report it up as a finding about the marts. |
| `ScenarioClientCount` is 0 beside non-zero executions | Not a stop and not a finding. The per-customer metric family is unpopulated on this project — declare it unavailable once in `## What we do not know` and judge on the populated metrics (`invariants.md`, 5). |
| `flows_lookup` returns no counters for the window | Counters live ~30 days. Keep the reporting findings; do not invent block-level figures. Read levels 1–3 as usual — the skeleton without counts still says which outputs lead nowhere and whether a second attempt exists — and part 3 says the counts were not available. |
| `flows_lookup` on the version could not be resolved to the audited window | Read the active version, say in part 3 that the construction described is today's, not necessarily the period's. |
| A figure of yours disagrees with the platform screen or another tool | Print both with the tool and window beside each. Never average, never pick silently. |

## The handover check

Written rules hold on some runs; counted rules hold on every run. **The counts go in the run log
and nowhere else** — no form of the report carries a section about this check, its counts or its
words. Where the counts cannot be recorded, the report says in one line that they were taken and
could not be written down. When a count comes out wrong, the fix is the report, not the count.

Count what must be there, not what must not; each count is taken over the forms that exist.

1. **Chat answer ↔ full page, paired.** Verdicts by scenario, section headings in order, table
   cells row by row: **N paired, M differing — M = 0**. The page's shorter table (its rule 6) is the
   one allowed difference.
2. **Promises against the half that makes them.** «shown below», «ordered by», «full list» — each
   checked against its own form: **K found, K met.**
3. **Verdict words.** The four English names on any surface: **0**. Distinct words per outcome: **1**.
4. **Machinery on the surface**, per form: tool names, template handles, column names, the goal's
   system name, a metric in this file's English where the product has its own word, names ending
   `..`, block identifiers, version numbers, bare scenario identifiers. **Each count recorded, zeros
   included.** Identifiers: chat **0** always; page **0** unless the user explicitly asked for a
   shown page; deck **0** unless asked. Count positionally — drop everything between `<` and `>`,
   count the runs of five or six digits left.
5. **Links.** Rows in the scenario table vs rows whose name is a link: equal, or the difference is
   exactly the scenarios with no base, said in the report.
6. **Every printed number is in the log.** **P printed, F found verbatim, D derived with the
   derivation on its line, U unaccounted — U = 0.** Build the list from the report's figure slots,
   not by sweeping for digits.
7. **Safe to forward.** Every «What to do» item and every probe: **N items, K needing platform
   access, A of those naming an addressee — K − A = 0**; statements about the reader's own settings
   with the verdict left open: **0**.
8. **Construction read.** For every scenario taken through in full (a full block, or a slide): which
   levels were read (card / skeleton / properties), and whether its part 3 names at least one block.
   **Full blocks F, with a construction read C — F − C = 0.** And every row of the hypothesis table
   carries «construction not read»: **rows R, marked M — R − M = 0.**
9. **Steps name a place.** Every step in «What to do»: does it name a block, a setting, a condition
   or a data source. **K steps, L naming a place — K − L = 0.**
10. **Money ranking clean of transactional scenarios.** Scenarios with all-transactional mailings in
    the money ranking: **0**. And the share of project revenue on transactional mailings, as T1t
    returned it, recorded.
11. **Deck inclusion** (deck form only). Every figure and claim on the slides looked up in the full
    report: **S on slides, F found, U not found — U = 0.**
12. **CSM note complete** (deck form only). **Proposal slides N, sections in the note M — N − M = 0**;
    per section, the spoken paragraph's word count (60–120) and figure count (≤ 3), and the number of
    skill terms, tool names or identifiers in it: **0**.
13. **Nothing addressed to the CSM inside the deck.** Occurrences of «how to say it», «not to say»,
    «for the CSM» — or their equivalents in the report's language, written into the log with the
    verdict words — or any second-person note to the presenter in the deck file: **0**.

## How an empty value is printed

**A figure that is not empty is printed for a human**: thousands separated, currency named,
percentages to the precision the rate deserves (unsubscribe rates need more decimals than open
rates), the separator and the decimal mark of the report's language (a Russian report writes
`1 185 769,20`).

| Case | Print |
|---|---|
| Money `NULL` (no goal-attributed rows for the flow and period) | `—`, and say the flow has no attributed revenue in the period — never `0,00` |
| A rate `NULL` (the flow's channels cannot report the event) | `—` **with the reason beside it** |
| A flow whose rate columns are empty while its money columns are filled | `—` for every rate, reason «the reporting data holds no rate for this flow in the period» — a property of the data, not a verdict on the channel mix |
| Funnel `NULL` while money is not | `—` for the funnel; the money is attributed but the sends are not in the data. **Not** «did not send» |
| No rows at all | the verdict «did not send in the period», not a row of zeros |
| A counter never measured on this project | omit the column and name it in `## What we do not know` |
| A sentence promises a list and the list is empty or was not assembled | the list, or the count and why there is none — never a colon with nothing after it |
| A construction that could not be read | part 3 says what was not read and why; the verdict is «can't judge» |

## Our words and the reader's

None of our vocabulary reaches a reader in any form; one concept, one word, for the whole report.
**The metric names are the product's own — the scenario report's labels — in the report's locale.**
The run writes the words it will use into the log before the report is begun.

### Metrics — the product's labels

| This skill's / the platform's word | Russian report | English report |
|---|---|---|
| revenue (`Revenue`) | Выручка из доставленных сообщений в выбранном периоде — shortened after first use to «выручка» with the header's note | Total Revenue (First touch within data range) |
| revenue by order date (not printed; named once to explain the mismatch) | Выручка за период | Total Revenue |
| orders (`Orders`) | Заказов / Конверсий | Orders |
| conversion to order | Конверсия в заказ | Conversions rate — say «conversion to order» |
| sends (`Sends`) | Отправлено | Sent |
| deliveries (`Deliveries`) | Доставлено | Delivered |
| delivery rate (`DeliveryRate`) | % доставок | Delivery Rate |
| opens / Open Rate (`Opens` / `OpenRate`) | Открытия / % открытий | Opens / Open Rate |
| clicks / CTR (`Clicks` / `ClickRate`) | Клики / % кликов | Clicks / Click Rate |
| CTOR | CTOR | CTOR |
| unsubscribes / Unsub Rate (`Unsubscribes` / `UnsubscribeRate`) | Отписки / % отписок | Unsubscribes / Unsubscribe Rate |
| spam / Spam Rate (`SpamCount` / `SpamRate`) | Жалоб на спам / % жалоб на спам | Spam Complaints / Spam Rate |
| bounces / Bounce Rate | bounce / Bounce Rate — the one deliberate departure from the product's label «Отказов», decided by the skill's owner | Bounces / Bounce Rate |
| average order value (`AverageOrderValue`) | Средний чек | Average order value |
| revenue per delivery | Доход на сообщение | Revenue per message |
| executions (`flows_lookup`, the structure's own counter) | прохождения сценария — never «исполнения» | executions of the scenario |
| entries into the scenario (`ScenarioExecutionsCount`) | Вхождений в сценарии | Flow runs |
| unique customers / customers with deliveries (`ScenarioClientCount` / `ScenarioClientDeliveries` — often unpopulated, `invariants.md` 5) | Уникальных клиентов / Клиентов с доставленными рассылками | Unique customers / Customers received campaigns |

The rates carry their channel where the product does — «% отписок (Email)» — and their denominator
beside them where the denominator is small.

### Terms of this skill

| Not this | This |
|---|---|
| rollup, grain, floor, datamart, breakdown, metric handle | the scenario's own total; its mailings one by one; the provability threshold, in words; the project's reporting data |
| a template handle, a tool name, a column name | the period, the slice and what measured it, in words |
| a bare identifier, a block identifier, a version number, a block type tag | the scenario's name as a link; the block by its own name in quotes; the date a version took over; the message by name |
| the goal's system name (`Default`) | the goal's display name, alone |
| level (twelve-month average) | «собственный уровень сценария — среднее за двенадцать месяцев» / «the scenario's own level, its twelve-month average», said once |
| the literal text of a failed call | what could not be got, and what to ask for |
| «Почему сравнение честное» and similar self-assessing headings | a heading that says what the section shows: «Что проверено», «Где именно теряется», «Что это не объясняет» |
| verdicts in English on any surface | the fixed words below |

### The four verdicts, fixed

| Outcome | Russian | English |
|---|---|---|
| problem | **есть проблема** | **problem** |
| fine | **в порядке** | **fine** |
| did not send in the period | **не отправлял в этом периоде** | **did not send in the period** |
| can't judge | **не берусь судить** | **can't judge** |

A weak verdict is the same word with a qualifier in the same language («в порядке — слабый вывод»),
never a second label and never a hybrid of two languages. In another language the run picks the
four words once and writes them into the log. **The deck carries none of them**: its labels are the
three urgency labels of `writing-the-report.md`, "The client deck".

**What must not be flattened while translating**: a scenario's own total and its mailings added up
are two quantities, and a check of this audit is that they are equal; where the report says they
disagree, both are named in their own words.
