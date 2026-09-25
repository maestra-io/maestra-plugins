<!-- locale: en-US. Parallel variant of ../ru-RU/terminology.md. Keep both in step. -->

# Report wording — en-US

The exact wording the audit report prints when the user works in English. Keys are stable across
locales: the same key in `../ru-RU/terminology.md` is the Russian variant of the same string.

## Project-wide report table

| Key | Wording |
|---|---|
| `table.header.check` | ✓ |
| `table.header.scenario` | Scenario |
| `table.header.problems` | Problems |
| `table.header.whatToDo` | What to do |
| `table.header.priority` | Priority |

## Priority labels

| Key | Wording |
|---|---|
| `priority.high` | High |
| `priority.medium` | Med |
| `priority.low` | Low |
| `priority.ok` | OK |

## Fixed phrases

| Key | Wording |
|---|---|
| `offer.html` | Shall I build an HTML checklist to open in a browser and share? |
| `offer.allFlows` | Some issues only show up across all flows — want me to run that too? |
| `verdict.clean` | No issues found — the flow looks correct. |
| `verdict.cleanCell` | No problems found |
| `verdict.noSeriousProblems` | No serious problems found. |
| `verdict.counts` | {name} — {n} problems to fix (+ {m} optional) |
| `label.problems` | Problems |
| `label.suggestions` | Suggestions (optional) |
| `label.manualCheck` | Check manually |
| `label.optionalInline` | Optional (a load-vs-clarity trade-off): |
| `coverage` | audited {n} of {m} flows |

## HTML page chrome

Used in `html-report-example.html` in this folder.

| Key | Wording |
|---|---|
| `html.title` | Scenario audit |
| `html.h1` | Technical audit of scenarios |
| `html.sub` | Project {name} · {n} of {m} scenarios checked · load and communication-correctness checklist |
| `html.stat.scenarios` | Scenarios |
| `html.stat.clean` | No problems |
| `html.stat.withProblems` | With problems |
| `html.stat.problemsTotal` | Problems in total |
| `html.section.summary` | Summary by priority |
| `html.section.details` | Scenario by scenario |
| `html.note.problems` | "Problems" are what is worth fixing. |
| `html.note.suggestions` | "Suggestions" are optional improvements (a load-vs-clarity trade-off), not defects. |
| `html.note.manual` | "Check manually" is what cannot be decided from the scenario structure alone. |
| `html.note.checkboxes` | Checkbox ticks are kept only in the open tab. |
| `html.foot.coverage` | Coverage: {n} of {m} scenarios checked. |
