<!-- locale: ru-RU. Parallel variant of ../en-US/terminology.md. Keep both in step. -->

# Report wording — ru-RU

The exact wording the audit report prints when the user works in Russian. Keys are stable across
locales: the same key in `../en-US/terminology.md` is the English variant of the same string.

## Project-wide report table

| Key | Wording |
|---|---|
| `table.header.check` | ✓ |
| `table.header.scenario` | Сценарий |
| `table.header.problems` | Проблемы |
| `table.header.whatToDo` | Что сделать |
| `table.header.priority` | Приоритет |

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
| `offer.html` | Собрать HTML-чеклист, чтобы открыть в браузере и поделиться? |
| `offer.allFlows` | Часть проблем видна только на всех сценариях сразу — запустить и такую проверку? |
| `verdict.clean` | Проблем не найдено — сценарий выглядит корректно. |
| `verdict.cleanCell` | Проблем не найдено |
| `verdict.noSeriousProblems` | Серьёзных проблем не найдено. |
| `verdict.counts` | {name} — {n} проблемы исправить (+ {m} опционально) |
| `label.problems` | Проблемы |
| `label.suggestions` | Рекомендации (необязательно) |
| `label.manualCheck` | Проверить вручную |
| `label.optionalInline` | Опционально (компромисс нагрузка/наглядность): |
| `coverage` | проверено {n} из {m} сценариев |

## HTML page chrome

Used in `html-report-example.html` in this folder.

| Key | Wording |
|---|---|
| `html.title` | Аудит сценариев |
| `html.h1` | Технический аудит сценариев |
| `html.sub` | Проект {name} · проверено {n} из {m} сценариев · чек-лист нагрузки и корректности коммуникаций |
| `html.stat.scenarios` | Сценариев |
| `html.stat.clean` | Без проблем |
| `html.stat.withProblems` | С проблемами |
| `html.stat.problemsTotal` | Проблем всего |
| `html.section.summary` | Сводка по приоритету |
| `html.section.details` | Подробно по каждому сценарию |
| `html.note.problems` | «Проблемы» — то, что стоит починить. |
| `html.note.suggestions` | «Рекомендации» — необязательные улучшения (компромисс нагрузка/наглядность), не дефекты. |
| `html.note.manual` | «Проверить вручную» — то, что нельзя однозначно определить по структуре сценария. |
| `html.note.checkboxes` | Отметки-галочки сохраняются только в открытой вкладке. |
| `html.foot.coverage` | Покрытие: проверено {n} из {m} сценариев. |
