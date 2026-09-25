<!-- locale: ru-RU. Parallel variant of ../en-US/terminology.md. Keep both in step. -->

# Report wording — ru-RU

The exact wording the business audit prints when the user works in Russian. Keys are stable across
locales: the same key in `../en-US/terminology.md` is the English variant of the same string. The
rest of the skill names a key or writes English; this file is the only home of the locale wording.

One concept, one word, for the whole report: the run picks the wording from here once, writes it
into the log, and holds it to the last line.

## Metric names — the platform's own labels

The metric names are the product's own, as its scenario report prints them in this locale. The
left column is this skill's internal word, which never reaches the reader.

| Key | Wording |
|---|---|
| `metric.revenue` | Выручка из доставленных сообщений в выбранном периоде — the scenario report's wording, kept as the printed label; the same money is «Выручка из конверсий» on the mailings report, so the screen is named with it. After first use shortened to «выручка», with the note in the header |
| `metric.revenueByOrderDate` | Выручка — the same money on the order date; not printed, named once to explain why the two do not match |
| `metric.businessRevenue` | Выручка — **a different quantity** carrying the same word: everything the project earned in the period, the denominator of the mailings' share of revenue. Not printed by this audit, and never set beside `metric.revenueByOrderDate` without saying they are two figures |
| `metric.orders` | Заказов / Конверсий |
| `metric.conversionToOrder` | Конверсия в заказ — the platform's own rate, computed over the deliveries its attribution settings admit, never orders over all deliveries (`../rates.md`) |
| `metric.sends` | Отправлено |
| `metric.deliveries` | Доставлено |
| `metric.deliveryRate` | % доставок |
| `metric.opens` | Открытия |
| `metric.openRate` | % открытий |
| `metric.clicks` | Клики |
| `metric.ctr` | % кликов |
| `metric.ctor` | CTOR |
| `metric.unsubscribes` | Отписки |
| `metric.unsubRate` | % отписок |
| `metric.spam` | Жалоб на спам |
| `metric.spamRate` | % жалоб на спам |
| `metric.bounces` | bounce — the one deliberate departure from the product's own label «Отказов», decided by the skill's owner |
| `metric.bounceRate` | Bounce Rate |
| `metric.aov` | Средний чек |
| `metric.revenuePerDelivery` | Доход на сообщение |
| `metric.executions` | прохождения сценария — never «исполнения» |
| `metric.flowRuns` | Вхождений в сценарии |
| `metric.uniqueCustomers` | Уникальных клиентов |
| `metric.customersWithDeliveries` | Клиентов с доставленными рассылками |
| `metric.ownLevel` | собственный уровень сценария — среднее за двенадцать месяцев — said once |

A rate carries its channel where the product does — `% отписок (Email)` — and its denominator
beside it where the denominator is small.

**A label belongs to a screen**, and in this locale two quantities share one word: «Выручка» is both
the attributed money on the order date and the project's whole revenue for the period. Where either
is printed, the screen and the quantity are said with it, and the two are never printed side by side
without that sentence.

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
| `verdict.problem` | есть проблема |
| `verdict.fine` | в порядке |
| `verdict.didNotSend` | не отправлял в этом периоде |
| `verdict.cantJudge` | не берусь судить |
| `verdict.weakSuffix` | в порядке — слабый вывод |

A weak verdict is the same word with a qualifier in the same language, never a second label and
never a hybrid of two languages. The deck carries none of the four.

## Urgency labels — the deck only

A closed set of three, assigned by the rule in `../../SKILL.md` step 8.

| Key | Wording |
|---|---|
| `urgency.now` | Решить сегодня |
| `urgency.fix` | Чинить |
| `urgency.idea` | Идея |

## Report sections

| Key | Wording |
|---|---|
| `report.title` | Разбор сценариев — деньги |
| `report.section.project` | Проект целиком |
| `report.section.flowsThatSent` | Сценарии, отправлявшие в периоде — показаны {n} из {m} |
| `report.section.problemFlows` | Сценарии с проблемой |
| `report.section.silentButLive` | Молчит, но продолжает принимать людей |
| `report.section.whatToDo` | Что сделать |
| `report.section.whatWeDoNotKnow` | Чего мы не знаем |
| `report.group.observed` | Что наблюдаем |
| `report.group.inTheScenario` | Что в сценарии |
| `report.group.whyItMoved` | Почему сдвинулось |
| `report.group.whatToFix` | Что починить |
| `report.group.actions` | Действия |

## Report table headers

| Key | Wording |
|---|---|
| `table.header.metric` | Показатель |
| `table.header.scenario` | Сценарий |
| `table.header.verdict` | Вердикт |
| `table.header.revenue` | Выручка |
| `table.header.orders` | Заказов |
| `table.header.deliveries` | Доставлено |
| `table.header.openRate` | % открытий |
| `table.header.ctr` | % кликов |
| `table.header.unsubRate` | % отписок |
| `table.header.whatTheVerdictRestsOn` | На чём стоит вердикт |
| `table.header.yoy` | Изменение год к году |
| `table.header.project` | Проект целиком |

## Deck

| Key | Wording |
|---|---|
| `deck.title` | Пример: предложения по сценариям |
| `deck.overview.heading` | Предложения по текущим сценариям |
| `deck.overview.more` | Ещё {n} находок — в полном разборе |
| `deck.heading.whereLost` | Где именно теряется |
| `deck.heading.whatChecked` | Что проверено |
| `deck.heading.whatThisDoesNotExplain` | Что это не объясняет |
| `deck.heading.inTheScenario` | Что в сценарии |
| `deck.heading.whatToDo` | Что сделать |
| `deck.nav.prev` | ← Назад |
| `deck.nav.next` | Вперёд → |
| `deck.nav.overview` | Обзор |
| `deck.nav.proposal` | Предложение {n} |

The evidence disclosure is headed by what it shows. Never a self-assessing heading such as
«Почему сравнение честное».

## Presenter notes

| Key | Wording |
|---|---|
| `notes.heading.howToSayIt` | Как это сказать |
| `notes.heading.whatNotToSay` | Чего не говорить |

## Fixed phrases

| Key | Wording |
|---|---|
| `phrase.empty` | — |
| `phrase.notMeasured` | — не измерялось |
| `phrase.noAttributedRevenue` | у сценария нет ничего, атрибутированного цели, за этот период |
| `phrase.forWhoeverRunsTheProject` | Для того, кто ведёт проект в платформе |
| `phrase.whatWillShowItWorked` | Что покажет, что сработало |
| `phrase.whatWouldSettleIt` | Что решит |
| `phrase.supposed` | Предположение |
| `phrase.notEstablished` | Не установлено — это предположение, и оно так и записано |

Numbers are printed the way this locale prints them: `1 185 769,20`, a non-breaking space between
thousands and a decimal comma.
