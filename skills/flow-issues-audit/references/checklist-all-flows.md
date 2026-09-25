# Technical audit: project-wide checklist

Checks that only make sense across the **whole set of a project's flows**, not a single flow.

Each check follows the format: **how NOT to → why it's bad → what to do instead → how to check**.
Both read each flow *as an entity* — its launch condition and version history.

---

## 1. Many flows on the same event

**How NOT to:** create a large number of flows that trigger on one and the same event.

**Why it's bad:** they all fire at once and generate load proportional to their count — which can hurt the
processing speed of every other flow in the project.

**What to do instead:** where possible, minimize the number of same-type flows and "collapse" them into one
(e.g. a single flow for abandoned cart / favorites / product view / category / session instead of separate ones).
Where many flows hang off the same event, suggest merging them where possible.

**How to check (steps):**
1. Get the list of all flows (`flows_list`). If the ask is "running flows", filter the rows by status
   yourself — see `SKILL.md` § Procedure — all-flows.
2. For each flow in scope, read it as an entity (`flows_get`) and take its launch condition.
3. If it launches on a schedule (not an event), skip it for this check.
4. Group the event-triggered flows by event type and compare the groups.

---

## 2. Test versions left in testing long after testing is done

**How NOT to:** leave a flow's version in a testing state long after testing is effectively finished, with no
live version launched.

**Why it's bad:** a version left in testing keeps firing on its event/schedule and generates useless load,
which can hurt the processing speed of live flows.

**What to do instead:** if testing is done and no live version was launched, stop the test version (or launch the live one).

**How to check (steps):**
1. Read the flow as an entity (`flows_get`): from the version list, find a version in a **testing** state, how
   long it's been there (its created date and activity timeline), and whether any version is currently the
   **active/live** one. `urls` prints the full status vocabulary and the priority order among the statuses.
2. Estimate the flow's **longest path** — the sum of all wait durations along its longest branch, in days (from
   the flow structure via `flows_lookup`, `detail=Full` — wait durations are not in the skeleton).
3. If a version has been in testing longer than `MAX(2, longest-path-in-days + 1)` days and no live version is
   active, suggest stopping the test version or launching the live one.
