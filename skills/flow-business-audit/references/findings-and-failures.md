# Findings and failures — what counts as a finding, and what to do when a call fails

Four catalogues, read at the moments the audit judges: the interpretation traps, the triage table,
the handover check, and how an empty value and each word of ours reach the reader.

---

## What is a finding and what only looks like one

- **"Fine" owes a comparison exactly as much as "problem" does.** Every judgement names what it was
  measured against — the project's own rate over the same window (T2p, T8's rollup row), the same
  window a year earlier, the industry median `email_health_report` carries for email — or says
  there is no benchmark, which makes the verdict weak and printed as weak. An unsupported "fine" is
  repeated to the stakeholders as readily as an unsupported "problem", and it is the one that stops
  anyone looking again.
- **A class is not a benchmark.** "Normal for a reactivation" names a category, not a measurement.
  If a comparison for that category is in the run's hands, it is applied and its number printed; if
  none exists, the verdict is weak or "can't judge". A figure below a benchmark is not thereby a
  finding either — the floor and the traps below still decide.
- **A rate on a multi-channel flow is a blend, not a rate.** Opens near zero on a flow that sends
  mostly push or SMS is the channel mix: `flow_report` returns one `OpenRate` per flow, over the
  channels that report the event. Where a rate decides a verdict on such a flow, re-run with
  `channels` pinned and say which channel the rate covers (`rates.md`, "What the denominators are,
  and what that forbids"); an aggregate rate, if quoted at all, is said to be one.
- **One effect across every flow is one project-level finding**, not N degradations — named once,
  with the cause marked unestablished after the readings the run holds have been spent.
- **Compare like for like.** Closed, comparable periods. The fresh side of any pair is understated
  while attribution keeps arriving (up to 30 days), so a fall against a settled month is "at most
  this much, partly an artefact of the window"; a rise is the safe direction. Opens and clicks on
  the newest two to three days are still arriving too, so a rate whose window ends inside that tail
  is qualified the same way. **A month is the wrong unit for a mechanic that sends in bursts**:
  before a month-on-month verdict, look at the daily shape of that scenario's sends (T1m at day
  grain); concentrated in a handful of days, the comparison is not a measurement and the verdict is
  "can't judge" with that probe. Where seasonality is plausible, the year-ago cut decides.
- **A year-on-year fall against an unexamined base is not a finding.** Two points make a delta,
  never a level. Every delta is stated beside the flow's own twelve-month level (T1, T2 over the
  twelve closed months); where the verdict would rest on the level, see the thirteen months one by
  one (T1m) — an average of a series that fell through the year describes no month the flow has had.
  Count the months with sends off T1m's rows, never off the unbucketed overview — one row per flow
  says nothing about which months sent. A series that no month resembles is printed as its shape with
  the first-to-last ratio, and the average is not printed as the level. Year down while the flow
  sits at its level → both printed, verdict a step down, handed over as a question with both
  comparisons.
- **A flow id outlives the mechanic it names.** T11 guards T10 (`beyond-the-overview.md`): with
  the guard satisfied the delta is plain; where the mailings differ, or the guard could not be
  reached, the delta carries the warning — naming which side has the extra mailings, or that
  continuity is unverified — and it goes to the project owner as an open question, never dropped
  and never stated as a result.
- **Before "the mechanic was lost", check for a replacement** — a successor scenario with the same
  job that took the audience is a move, not a loss (`business-rules.md`).
- **Running or not is read from the version statuses; never from send dates and never from the
  `active version` line** (`calling-the-tools.md`, "Call arguments"). When it stopped is bounded by
  the last month with sends and printed as bounds. Presence in the reporting data and status are
  independent facts in both directions.
- **Materiality before signal, and the floor is a number written down here.** Below 1 000
  deliveries in the window no rate is provable; below 50 goal-attributed orders no money verdict is.
  The floors are about provability, not importance: a flow under them keeps its row and its figures,
  takes "can't judge" with its count, and the probe is a longer window. **A floor with no exit is a
  refusal to work**: when no flow clears it the audit answers at the coarsest level that does (the
  project, T1p) and says once that the finer level is not provable. The report states the split as a
  number — how many confident, how many "can't judge", which floor.
- **A rate that falls on unchanged volume is a finding in its own right**, and the year-ago window
  shows it: the volume on both sides clears the floor, the movement is relative to the flow's own
  year-ago value, the project's other flows on the same channel did not move the same way, and where
  both are present clicks and orders moved together (which rules out "only the attribution broke").
  T11 clean is required first.
- **Do not rank flows whose figures differ within noise.** Say the spread is inside noise.
- **Judge a mechanic by the metric its job implies**, and name which job you assigned and on what
  basis — the construction, never the name alone and never the figures
  (`business-rules.md`, "The five kinds").
- **Conversion holds, volume fell — the mechanic is not broken, it is fed less.** The finding is the
  volume; its cause is upstream of the send — the entry, the event's source
  (`structural-causes.md`, row A).
- **Stay inside what you can see.** No recommendations about subject lines, copy or layout. No
  "activate the channel, the base is collected" for a channel with no sends.
- **A reporting artefact is not an achievement.** Sends equal to deliveries with non-zero bounces
  means deliverability is not measured on that project — never 100 %.
- **A flow that delivered nothing is not thereby harmless.** The reporting data holds no arrivals; the one
  reach figure is `flows_lookup`'s start-block count over ~30 days. Which five flows get the probe:
  stopped earners by twelve-month revenue first, then never-sent ones by the reach their mechanic
  implies (abandoned cart, view, session, welcome admit orders of magnitude more than a narrow
  mechanic), at most one per repeated name stem. The verdict stays "can't judge" with a probe — a
  diagnosis here is a false finding on every paused flow of the project.

## If something goes wrong

Read-only skill, so blast radius is small — but a number quoted to stakeholders is not retractable.

| Situation | What to do |
|---|---|
| A required tool is missing / not enabled / access denied | Stop per `SKILL.md § Prerequisites`, print no figure, name **which** of the three kinds it is and **which capability is missing**, in plain words (`invariants.md`, "A tool that is not available reads three different ways"). |
| **The answer is the bare sentence `An error occurred. Please try again or ask support.`** | A failure, not data — and the same text for a transport failure and a wrong `goalName` (`invariants.md`, 6): if a goal name was passed, re-run once without it before spending a retry on the transport. |
| The overview call fails opaquely with no goal name in play | Retry on the transport budget below and spend all of it; **then stop with no figure**, naming the window. Never fill the gap from a neighbouring window or an earlier run. |
| `Unable to connect. Is the computer able to access the url?`, or the protocol prefix with nothing after the tool name | The transport dropped — nothing about the call caused it. Retry the same call unchanged, **never immediately**: these stalls run one to three minutes and take the whole connection, so keep retrying while the attempts span less than about three minutes, at most three retries, putting the next useful call between attempts. If that call fails the same way, the connection is down — spend the budget once, resume when anything answers. Past the budget, stop for that call; what the loss costs is decided by which call it was. |
| A call failed | Retry delayed; narrow it (a shorter window, fewer metrics, a smaller `topN`) **only when the text names something about the call**. Budget spent → the loss is one figure: name the metric in `## What we do not know` and move on. Never substitute a neighbouring figure. |
| A protocol-level error (`An error occurred invoking '…': …`) | Read the text after the colon. `Tool 'X' is not enabled` or `Access denied` is a gate: do not retry; required tool → stop, optional → continue and name the loss. No text → the transport row. |
| A call fails with an empty error while a neighbouring form of the same call succeeds | An argument shape, not the transport: re-read the tool's schema and remake the call (`calling-the-tools.md`, "Call arguments"). No retry budget spent. |
| The answer is far larger than expected, or the host spills it to a file | Narrow the call — `includeFlowIds`, `folders`, a smaller `topN`, `mode="Detailed"` — never a blind cut of the answer. |
| The breakdown header says `top N of M` with M above N | Not a stop, and not optional to fix. Raise `topN` to 200 and page with `excludeFlowIds`; a project classified from a capped breakdown is a wrong report, not a partial one (`invariants.md`, 2). |
| `ScenarioClientCount` is 0 beside non-zero executions | Not a stop and not a finding. The per-customer metric family is unpopulated on this project — declare it unavailable once in `## What we do not know` and judge on the populated metrics (`invariants.md`, 5). |
| A flow's own row and its T3f rows disagree in shape — the mailings' ranking contradicts the flow's figures | Not a defect of the flow, and not a mismatch to reconcile: the two reports overlap by construction and are never compared by equality (`beyond-the-overview.md`, T3f). A finding about the matching by name — say so, and rest the flow's figures on its own row. |
| `flows_lookup` returns no counters for the window | Counters live ~30 days. Keep the reporting findings; do not invent block-level figures. Read levels 1–3 as usual — the skeleton without counts still says which outputs lead nowhere and whether a second attempt exists — and part 3 says the counts were not available. |
| `flows_lookup` on the version could not be resolved to the audited window | Read the active version, say in part 3 that the construction described is today's, not necessarily the period's. |
| A figure of yours disagrees with the platform screen or another tool | Print both with the tool and window beside each. Never average, never pick silently. |

## The handover check

Written rules hold on some runs; counted rules hold on every run. **The counts go in the run log and
nowhere else**, and when a count comes out wrong the fix is the report, not the count.

Count what must be there, not what must not; each count is taken over the forms that exist.

1. **Chat answer ↔ full page, paired.** Verdicts by scenario, section headings in order, table
   cells row by row: **N paired, M differing — M = 0**. The page's shorter table (its rule 6) is the
   one allowed difference.
2. **Promises against the half that makes them.** "shown below", "ordered by", "full list" — each
   checked against its own form: **K found, K met.**
3. **Verdict words.** Printed verdicts that do not match the chosen locale's wording in
   `<locale>/terminology.md` — a word in another language, this file's English on a non-English
   surface, a second label for one outcome: **0**. Distinct **labels** per outcome: **1** — the
   weak form is that same label with its qualifier (`verdict.weakSuffix`), which is the one label
   and not a second.
4. **Machinery on the surface**, per form: tool names, template handles, column names, the goal's
   system name, a metric in this file's English where the product has its own word, names ending
   `..`, block identifiers, version numbers, bare scenario identifiers. **Each count recorded, zeros
   included.** Identifiers: chat **0** always; page **0** unless the user explicitly asked for a
   shown page; deck **0** unless asked.
5. **Links.** Rows in the scenario table vs rows whose name is a link: equal, or the difference is
   exactly the scenarios with no base, said in the report.
6. **Every printed number is in the log.** **P printed, F found verbatim, D derived with the
   derivation on its line, U unaccounted — U = 0.** Build the list from the report's figure slots,
   not by sweeping for digits. Count U only over figures that claim to describe the project: a
   figure that comes from this skill's own rules rather than from a call — the provability floors,
   the budget caps — is not unaccounted and is not counted at all.
7. **Safe to forward.** Every "What to do" item and every probe: **N items, K needing platform
   access, A of those naming an addressee — K − A = 0**; statements about the reader's own settings
   with the verdict left open: **0**.
8. **Construction read.** For every scenario taken through in full (a full block, or a slide): which
   levels were read (card / skeleton / properties), whether form F was checked or carries "form F
   not checked", and whether its part 3 names at least one block.
   **Full blocks F, with a construction read C — F − C = 0.** And every row of the hypothesis table
   carries "construction not read": **rows R, marked M — R − M = 0.**
9. **Steps name a place.** Every step in "What to do": does it name a block, a setting, a condition
   or a data source. **K steps, L naming a place — K − L = 0.**
10. **Money ranking clean of transactional scenarios.** Scenarios with all-transactional mailings in
    the money ranking: **0**. And the share of project revenue on transactional mailings, as T1t
    returned it, recorded.
11. **Deck inclusion** (deck form only). Every figure and claim on the slides looked up in the full
    report: **S on slides, F found, U not found — U = 0.**
12. **Presenter notes complete** (deck form only). **Proposal slides N, sections in the notes M —
    N − M = 0**, each section within the limits `writing-the-report.md` sets for it.
13. **Nothing addressed to the presenter inside the deck**, in any language and in any
    second-person form: **0**.

## How an empty value is printed

**A figure that is not empty is printed for a human**: thousands separated, currency named,
percentages to the precision the rate deserves (unsubscribe rates need more decimals than open
rates), the separator and the decimal mark of the report's language (a Russian report writes
`1 185 769,20`).

| Case | Print |
|---|---|
| Money `NULL` (no goal-attributed rows for the flow and period) | `—`, and say the flow has no attributed revenue in the period — never `0,00` |
| A rate `NULL` (the flow's channels cannot report the event) | `—` **with the reason beside it** |
| A flow whose rate columns are empty while its money columns are filled | `—` for every rate, reason "the reporting data holds no rate for this flow in the period" — a property of the data, not a verdict on the channel mix |
| No rows at all | the verdict "did not send in the period", not a row of zeros |
| A counter never measured on this project | omit the column and name it in `## What we do not know` |
| A construction that could not be read | part 3 says what was not read and why; the verdict is "can't judge" |

## Our words and the reader's

None of our vocabulary reaches a reader in any form; one concept, one word, for the whole report.
**The metric names are the product's own — the scenario report's labels — in the report's locale.**
The run writes the words it will use into the log before the report is begun.

**The wording itself lives in one place: `<locale>/terminology.md`** (`en-US`, `ru-RU`), where every
metric name, verdict, urgency label, section heading and fixed phrase stands under a stable key. If
the report's language has no variant of its own, take `en-US`, translate it, and write the chosen
words into the log.

### Terms of this skill

| Not this | This |
|---|---|
| rollup, grain, floor, datamart, breakdown, metric handle | the scenario's own total; its mailings one by one; the provability threshold, in words; the project's reporting data |
| a template handle, a tool name, a column name | the period, the slice and what measured it, in words |
| a bare identifier, a block identifier, a version number, a block type tag | the scenario's name as a link; the block by its own name in quotes; the date a version took over; the message by name |
| the goal's system name (`Default`) | the goal's display name, alone |
| level (twelve-month average) | the scenario's own level, its twelve-month average (`metric.ownLevel`), said once |
| the literal text of a failed call | what could not be got, and what to ask for |
| a self-assessing heading — "Why the comparison is fair" | a heading that says what the section shows: "What is checked", "Where exactly it is lost", "What this does not explain" (`deck.heading.*`) |
| a verdict in a language other than the report's, on any surface | the four words below, in the report's locale |

The four verdicts and their weak form are `<locale>/terminology.md`. **The deck carries none of
them**: its labels are the three urgency labels (`writing-the-report.md`, "The proposal deck").

**What must not be flattened while translating**: a scenario's own total and its mailings added up
are two quantities from two reports that overlap by construction; this audit never adds them and
never presents them as one, and where both are printed each carries its own origin in its own words.
