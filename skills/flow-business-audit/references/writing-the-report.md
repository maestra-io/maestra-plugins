# Writing the report

Read **once, at the moment the report is begun**, and no report is written without it. It is the one
home of what the report may say, in what words, what each section owes, and which forms it takes.

## One reader, and the proof is the log

Write in **the language the user is working in** — headings, section titles and verdict words
included. The reader is a CSM who repeats these numbers to a client, or the client themselves, so
every figure has to survive being quoted, and **nothing of ours reaches the surface**: no template
handle, no tool name, no column name, no file name of this skill, no «datamart», no block identifier,
no version number. Which call produced a figure is answered from the run log, on request.

**Every figure carries its passport in the reader's words**: the period, the slice, and the origin
plainly said — «from the project's own reporting data», «counted over the mailings inside the
scenario», «the executions counted by the scenario over the last thirty days». Two figures from two
sources never read as one series. A figure whose origin cannot be put into the reader's words is not
printed; what it would have said goes to `## What we do not know`.

**Translate each term once and hold it to the last line.** The fixed vocabulary — the four verdict
words, the product's own metric names, the terms of this skill and what each becomes — is
`findings-and-failures.md`, "Our words and the reader's". One concept, one word, for the whole
report.

## Money: one pair, said in the product's words

Every money figure is aggregated **by the date the message was sent** — the metric the product's
scenario report calls **Total Revenue (First touch within data range)** (Russian locale:
«Выручка из доставленных сообщений в выбранном периоде»). Name it that way once, in the header, and
say that it will not match the report's **Total Revenue** («Выручка за период»), which counts money
on the date of the order — the same order lands in a different month. Never print both to settle it.

## A scenario is a name; the identifier lives inside the link

The scenario is printed by its name, and the name is the link — `[name](<base>/scenarios/<id>)` in
the chat, `<a href>` on a page. The base: a link the user pasted → its base; otherwise
`https://<systemName>.maestra.io`, and the report says once which base the links are built from;
the user names another → rebuild every link. **No bare identifier on any surface**, in any form —
not in a cell, not in prose, not beside a name. Two exceptions, both said in the report: no base
could be built; or the user explicitly said the page will be **shown on a screen** rather than
opened (asked once when the page is offered — silence, «I don't know» and «decide yourself» all mean
no identifiers). The chat answer never carries one whatever the answer.

## Written for both readers

The report is forwarded to the client as it stands. Every step and every probe is worded so both
readers can act on it, or names its addressee in the sentence («this one is for whoever runs the
project in the platform»). Never a statement about the reader's own settings with the verdict left
open — either it is a finding with its figure, or a supposition written as one with its probe.
Neither is a reason to say less: a probe worn down to politeness is the worse defect.

## The frame — the same sections, the same names, in every full report

1. **Header** — project; period; the goal by display name; the basis of the verdicts and whether it
   was chosen or defaulted; the report form and whether it was chosen or defaulted; the
   recalculation date and any lag; what could not be reached, as a capability («the platform's own
   scenario report was not available»); coverage («classified N of M scenarios from the list, plus
   K in the reporting data and not in the list»); the confidence split (how many confident
   verdicts, how many «can't judge», and the two thresholds); the money-and-deliveries match with
   its three counts; the one-sentence note that this edition opens with no self-consistency check;
   the money sentence above.
2. **The project as a whole** — the project's own figures, period columns in the fixed order
   (closed period, the one before, the same period a year earlier, then the change), its own
   year-on-year line, and the project-level findings — the transactional-attribution finding among
   them when T1t showed one.
3. **Overview** — one table of the scenarios active in the period, ordered by revenue: name as a
   link, verdict, revenue, deliveries, the rates that apply, and one line saying **what the verdict
   rests on** — the comparison and the number — for every «problem», every «can't judge» and every
   weak «fine». Did-not-send scenarios are one counter under the table, names on request. A flow
   under the floor keeps its row.
4. **The scenarios with a problem — in full.** One block each, **three to seven of them, as many as
   have a figure and a construction reading behind them** — never padded to seven, never cut to a
   round number. Ordered by the money at stake; volume or reach where there is none. Five parts,
   below.
5. **The rest of the problem scenarios — a table of hypotheses.** For every «problem» scenario not
   taken in full: name as a link, the observation in one line with its figure and window, the
   hypothesis in one line, the kind of step it implies («A/B on the message timing», «check the
   entry condition», «move the validity check into the launch conditions»), the addressee — and the
   words **«construction not read»**, because that is what separates these rows from the full blocks
   (`SKILL.md`, rule 4): their hypotheses were not checked against the scenario. No detail, no
   probes spelled out. A reader who wants one of these in full asks, and the run has the figures.
6. **What works — the top performers.** Two or three scenarios by conversion or revenue per
   delivery on volume above the floor, each with its figure, its comparison, and **what in its
   construction the problem scenarios of the same kind lack** — printed as a hypothesis for them,
   with the block named. A report made only of complaints is not a report on the project.
7. **Silent, but still taking people in** — where step 5 found any; otherwise the line with its
   count.
8. **Where people are lost inside a scenario** — for every construction read: how many entered, the
   block where the largest number stopped going on, by its own name and with both figures, the
   stops with reasons where the answer carried them — each with the counters' own window beside it
   and said not to be the audited month; never the name of the branch the difference left by.
9. **Year on year** — the per-scenario comparison, present in every report; the named reason with
   its counts where there are no pairs.
10. **What to do** — every step of every finding in one ranked list, each naming its scenario, its
    place, its action and its addressee, with the line saying which key ranked the list. The chat
    answer owes this section exactly as the page does.
11. **`## What we do not know`** — always present, translated with the rest; when empty, one line
    saying everything asked for was computed. Otherwise what could not be retrieved and what it
    would have told the reader, questions whose data does not exist, comparisons not run,
    constructions not read (with the scenario named), and anything deliberately not judged. Never
    the literal text of a failed call.

**Sections 7 and 8 are conditional and never disappear in silence**; the rest are owed by every
report. Period columns everywhere in the fixed order above.

## Per problem flow — five parts, in this order

1. **What is observed** — the observation, its window, what it was compared with.
2. **What it costs** — in money, or in base (unsubscribes, bounces) where money is not the metric of
   this kind of scenario.
3. **What is in the scenario.** The blocks by their names as the tool returned them, in quotes; the
   execution counts with their own window, said not to be the period; the settings as they are set
   («limit: one execution per customer»), never as an assessment («the limit is wrong» is part 4).
   Nothing about content. **What could not be read is said here** — a block level 3 did not reach,
   a document that did not open — not left silent. This part is where the run shows it opened the
   scenario; a «problem» block without it is unfinished (`SKILL.md`, rule 4).
4. **Why one explains the other** — the established cause, or the supposition with its probe, told
   apart by the wording (`SKILL.md § From "what" to "why"`). Where a version changed near the
   movement, it is here as a hypothesis, never in part 3 as a fact about the cause.
5. **What to fix** — the steps, each naming **a place and an action**: the block, the setting, the
   condition or the data source by name, and a verb that can be carried out, plus the addressee and
   the metric that will show it worked (`business-rules.md`, "What a recommendation has to
   contain").

| Not this | This |
|---|---|
| «Check whether the address is validated» | «Between the site form and the block “Send Welcome 1” put a validity check that acts before the first send; the only check in the scenario today is “email exists and is invalid = no”, and it fires only on an address that has already bounced» |
| «Look at what changed at the entry» | «The condition “no confirmation mailings” passes 930 of 8 000 executions over the last thirty days; check whether a confirmation mailing was added to its list at the end of January» |
| «Work out why the scenario does not send» | «Invert the condition before the follow-up SMS: it requires an order in the last 14 days, and the entry takes customers with no order in the same 14 days — the branch is impassable» |
| «The audience seems inactive» | «Add to the entry condition of block “…” a cut-off by recency of the last open; there is no activity limit in it today» |

## Three surfaces of one run

- **The chat answer** — always. The full report lives here whatever else is built; nothing is lost
  when no page is built.
- **The full page** — offered at the end, built only on request from `html-report-example.html`.
  Same verdicts, same figures, same scenarios, same sections as the chat answer; the only allowed
  difference is the shorter table (rule 6 of that file) and the identifiers on an explicit yes.
- **The client deck and its CSM note** — built when the report form chosen at `SKILL.md § Inputs`
  is the deck, from `html-client-deck-example.html`. The deck carries a **subset** of the full
  report, chosen by `SKILL.md` step 8; what is checked is not equality but **inclusion**: every
  figure, every claim and every step on a slide is found verbatim in the full report.

## The client deck

**The deck is the report taken apart into proposals, and it is ready to send to the client as it
stands.** Nothing on it is addressed to the CSM. It has two readers, the CSM who runs the meeting
and the client who receives the file afterwards, and one voice — the proposal.

**Slides: one overview plus three to seven proposals.** The overview lists the proposals with their
one-line figure and, when the selection left findings out, the line «N more in the full report».

**The frame of a proposal slide, in this order:**

1. **Context line** — the proposal number, the scenario(s) by name as links, and an urgency label on
   the right from a closed set of three: "Decide today" / "Fix" / "Idea" (their equivalents in
   another language, fixed once in the log — Russian: «Решить сегодня» / «Чинить» / «Идея»).
   **Assigned by rule** (`SKILL.md` step 8): a breached hygiene threshold or the attribution finding
   → "Decide today"; an established cause with a fix → "Fix"; a hypothesis with a probe → "Idea".
   Labels are not verdicts: verdicts stay in the full
   report; a label says how soon, not what state.
2. **Heading — a business statement, not a metric.** «The second-earning mechanic of the year lost
   almost all its volume», not «Fall in sends of scenario X». No identifiers, no metric names, up to
   nineteen words.
3. **One large figure**, with its caption and **its window under it**.
4. **One paragraph** — the mechanism in the reader's words: what is happening, since when, what it
   costs.
5. **A table — only when the slide is about several scenarios.** Up to five rows, the last the
   project's own line as the point of reference; the worst row highlighted.
6. **Three disclosures, in this order:**
   - **the evidence** — headed by what it shows: «Where exactly it is lost», «What is checked»,
     «What this is not». The per-block funnel with its window, the month-by-month series, the
     per-message split, the year-ago comparison go here;
   - **«What is in the scenario»** — part 3 of the full block, shortened: the blocks by name, the
     settings as set, the counts with their window;
   - **«What to do»** — the steps, verbatim from the full report's «What to do», with their
     addressees.

**A small chart is welcome where a series carries the slide** — the twelve months of a fall, the
bounce share per message — drawn inline (an SVG or a CSS bar strip in the deck's own colours, no
external library), with the same window and origin under it that a figure carries, and only from
figures already in the full report. It is an aid, never a requirement: a slide without one is
complete.

**Identifiers in the deck**: never, in any position, unless the user asked — the deck is shown from
a screen by definition, and the name in the context line identifies the scenario. The question
about showing versus opening is not asked for the deck.

**What the deck does not carry**: the overview table, the four verdict words, the did-not-send
counter, the provability thresholds and their numbers, the coverage counts, the money-and-deliveries
match, `## What we do not know` as a section, weak verdicts, below-floor scenarios, anything of our
machinery. `## What we do not know` becomes one footnote line under the navigation: the data
windows, the goal, the money sentence.

### The CSM note — a separate file, never in the deck

Everything the CSM needs and the client must not read goes to **a separate Markdown file beside the
deck**, one section per proposal slide, named for the deck with a `-notes` suffix. It carries, per slide:

- **how to say it** — one paragraph of 60–120 words the CSM can read aloud in under a minute, first
  person plural, at most three figures each rounded to something sayable, ending in the proposal, a
  hypothesis sounding like a hypothesis («it looks as if», «the first place to look»);
- **what not to say** — where a wording would outrun the data (a coincidence in time worded as a
  cause; an upper-bound estimate worded as lost revenue; «the base is burning out» for «the share
  fell while volume grew»); which window differs from the period and what to answer if asked «and
  for the month itself?»; which figure from another population must not be set beside the slide's;
  where the client is right if they object, and what to answer then.

Every proposal slide has its section in the note; a slide without one is a slide where a hypothesis
will be spoken as a fact. **The note is handed over with one sentence**: that it is for the CSM and is
not part of what goes to the client.

## Handover

**Before anything is handed over, run the handover check and put its counts in the log** —
`findings-and-failures.md`, "The handover check". No form of the report carries a section about the
check; a report whose counts are not in the log is not finished. How an empty value is printed, and
how a figure is formatted for a human, are in the same file.

**Offer the full page, never auto-build it**, in the user's language, and in the same sentence ask
whether it will be shown rather than opened. On the deck form, the deck is built without asking;
the page is still offered.
