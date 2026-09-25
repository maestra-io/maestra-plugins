<!-- locale: ru-RU. Parallel variant of ../en-US/examples.md. Keep both in step. -->

# Flow summary — worked examples (ru-RU)

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
B_f0a98df [inboundEventBlock "Клиент подписался на Email рассылки"] B_f0a98df:default --> B_1c80f93 [operationStepsBlockSettings "Welcome - приветственное письмо"]
B_1c80f93 [operationStepsBlockSettings "Welcome - приветственное письмо"] B_1c80f93:default --> B_44fb444 [delayBlock]
B_44fb444 [delayBlock] B_44fb444:default --> B_34c0d51 [conditionBlock "Нет заказов и подписан"]
B_34c0d51 [conditionBlock "Нет заказов и подписан"] B_34c0d51:positive --> B_cc8e2ad [operationStepsBlockSettings "Welcome - предложение промокода"]
B_cc8e2ad [operationStepsBlockSettings "Welcome - предложение промокода"] B_cc8e2ad:default --> B_b227fd9 [delayBlock]
B_b227fd9 [delayBlock] B_b227fd9:default --> B_e05c738 [conditionBlock]
B_e05c738 [conditionBlock] B_e05c738:positive --> B_5519993 [limitationBlock]
B_5519993 [limitationBlock] B_5519993:beforeLimit --> B_147bb5f [operationStepsBlockSettings "Welcome sms - промокод еще действует"]
B_5519993 [limitationBlock] B_5519993:afterLimit --> B_627f6f4 [operationStepsBlockSettings "Welcome email - промокод еще действует"]
```

Channel per step-group block and the exact delay durations come from the full-properties
view; the block names here already indicate Email vs SMS.

**Summary**

### Стартовое событие

Запускается по событию «клиент подписался на Email-рассылки».

### Логика сценария

- Сразу отправляется приветственное письмо «Welcome — приветственное письмо».
- Затем — пауза, после которой проверяется условие «нет заказов и подписан»: при
  положительном исходе отправляется письмо «Welcome — предложение промокода».
- После ещё одной паузы и проверки условия срабатывает блок ограничения частоты:
  - клиентам, которые остаются в пределах частоты, уходит SMS «Welcome sms — промокод ещё действует»;
  - тем, кто лимит уже превысил, уходит письмо «Welcome email — промокод ещё действует».

Точные длительности пауз — в свойствах блоков ожидания (полное представление свойств).

### Цель сценария

Активировать нового подписчика, довести до первой покупки и напомнить о действующем
промокоде, удерживая частоту SMS в заданном лимите.

---

## Example 2 — Reading flow-run counts

Real capture: the same skeleton view of a whole flow version, this time asking for run counts over a
three-day window in August 2026.

**Skeleton with executions**

```
flow 296412 v1 rowVersion rMm6Bg==
executions counted 2026-08-08 - 2026-08-10 | version 1 ran: 2026-08-06 - now
B_f2dd430 [conditionBlock] B_f2dd430:positive --> B_bbe315c [operationStepsBlockSettings "Шаги 2"]
B_3fd3570 [inboundEventBlock] B_3fd3570:default --> B_f2dd430 [conditionBlock]  (89)
B_3fd3570 [inboundEventBlock]: 89 in, 89 out
```

How to read it: 89 executions entered on the inbound event and all 89 passed to the
condition. The condition's `:positive` edge carries **no number**, so **0** of those 89
took the positive branch in this window — nobody reached «Шаги 2». The inbound line
(`89 in, 89 out`) is a clean pass-through, not a drop.

**Run-informed note to fold into the summary (only when the caller asks for one):**

> За период 8–10 августа 2026 в сценарий вошло 89 клиентов (версия работает с 6 августа;
> счётчики доступны примерно за последний месяц). Все 89 дошли до условия, но по
> положительной ветке не прошёл никто — блок «Шаги 2» за это окно не получил ни одного
> клиента. Сигнал: условие сейчас отсекает всех, ветку стоит проверить.
