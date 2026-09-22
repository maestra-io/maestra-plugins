# Orphans, wiring, and repairing a block that reads back wrong

The mechanism behind two rules `SKILL.md` states and does not explain: **resolve every orphan
while you are still planning writes** (step 1c, step 6), and **a block that reads back wrong is
recoverable** (step 6). The rules are in `SKILL.md`; nothing here overrides it, and where a
sentence here and a `## CRITICAL` rule disagree, the rule wins.

- [Orphans and wiring](#orphans-and-wiring)
- [Building the operations](#building-the-operations)
- [Repairing a block that reads back wrong](#repairing-a-block-that-reads-back-wrong)

## Orphans and wiring

**An orphan is a block with no incoming edge** — which is *not* the same as a block you cannot
reach from the start block. It is not a harmless leftover: it **fails validation**.

**The write path does tell you — but only that it happened.** Every write answer carries a
validation list naming each unwired and each unfilled block, **by block id**. It is not a refusal: a
batch that comes back carrying entries was applied, and an empty list is how you see the last of them
cleared — so it is a progress meter across a run of batches, and worth reading after every one.

What it cannot give you is the wiring. It says a block has no incoming edge, never where that edge
belongs, and it goes quiet the moment *any* edge arrives — so an orphan cleared by wiring it to
whatever was nearest passes the list and still never runs (first bullet below). That is why the
wiring is decided before the batch, not after it: deciding it there is also what keeps a deletion in
the same batch as the rest. The flow's own orphan list is worked out by the same rule the validator
uses, which makes it the authoritative pre-check for that rule.

Three things about that list, each of which has produced a wrong answer:

- **It counts incoming edges only.** A detached *pair* of blocks passes it, because the second
  one's edge comes from the first. So a clean list is not evidence that every block runs, and
  resolving an orphan means wiring it **into the graph the start block feeds** — not merely giving
  it an incoming edge.
- **Only a read over the whole flow carries it.** A read scoped to one block prints the same field,
  **empty, whether or not that is the truth** — so an orphan check made on the wrong read is a
  false negative that reads like a clean bill of health, and nothing in the response tells you
  which of the two you got. **The write-path verification page says which read carries wiring and
  orphans: check there before you trust an answer**, rather than trusting whatever came back from
  the read you happened to make. The same applies to the edges themselves.
- **Deleting the edge is not deleting the block.** And some block types cannot legally sit at the
  end of a flow, so "re-wire it somewhere" is not always available.

**A block you were never asked about is still yours to resolve** — wire it into the graph the start
block feeds if the design wants it, delete it if not. Leaving it is not neutral.

## Building the operations

`SKILL.md` step 4 decides the graph and points here for how the operations are shaped. **A simple
block is filled at creation time**, its properties in the same create operation; **a block whose
settings are many interdependent fields is deferred to step 5** and filled in a call of its own.
**Wire the edges from the output vocabulary the reference gives**, not from a read-back — a block you
just created has nothing to read there yet. **Check your dead ends are intended:** an output with no
outgoing edge means executions on that branch leave the flow, each one a decision the user made
rather than an oversight. **Anything belonging to the flow *version* rather than to a block** is
written by its own operation if one exists — check the live operation vocabulary before you promise
it, and **never smuggle a version-level setting into a block body**, where it will not be written and
a read-back can appear to confirm it.

**Carry the row version forward:** the one from `SKILL.md` step 1(c) for the first write, the one each
write returns for the next. **A *refused* call applied nothing** — your token is still current, so fix
the cause and re-send the corrected batch rather than re-reading. Two exceptions have rows of their
own in `references/troubleshooting.md` → *Writes*: a refusal that is a **version conflict** (the token
*is* stale), and a call that **never answered at all** — not a refusal, and **not** a licence to
retry, because you do not know that nothing was applied.

## Repairing a block that reads back wrong

**Match the symptom first.** Several ways a read-back can disagree are documented in the `flows`
domain's known-issues sub-folder, each with a recovery of its own that ends somewhere the two
routes below do not: a block that came back **unchanged**, a value that came back **different**
from the one you sent, a value that will not change however you send it, something you never sent
that has **gone missing**. Match what you observed there and take that recovery — it replaces the
routes below and decides when to stop (`SKILL.md` → `## Where to look`, step 5). Guess here and the
likely guess is a deletion, which costs you a block that was fine.

Only if nothing there matches: two routes, both of which work. **Take them in order, and stop only
after both.**

**1. Repair in place.** Re-send that block alone with a **complete** body, every nested part of it
complete as well. *That* is what makes this a corrected re-send rather than the same body twice
(`SKILL.md` step 5). Two reasons, neither of which depends on how a body is applied:

- **A partial body cannot correct or complete what is stored where the platform parses that part
  fresh — it replaces it.** The members it leaves out are then not carried over from the block;
  they are simply not there (CRITICAL 3).
- **A partial repair repairs only what it carries, and answers successfully either way.** There is
  no per-operation status in a success response, so a body naming one field returns the same
  success whether the rest of the block is right or not — and every *other* wrong field stays
  exactly as it was, with nothing saying so.

Then read it back again. If it still disagrees, **match the symptom again** as above before going
on to route 2 — a repair that leaves the block **unchanged** is itself a documented symptom.

**2. Delete the block and create it again**, then read back once more. Deleting does not depend on
the block's contents being readable, so this route stays open when the first one fails. Mind the
graph: a start block's delete and its replacement's create go in **one** batch.

**Take the pre-delete read first, and keep it.** A delete is the write with no undo at all, so it
carries the same obligation as an overwrite: read the block at full detail immediately before, and
build the recreate from that read (`SKILL.md` step 5, *A delete takes that same read first*). Without
it this route cannot restore what the block held, and you are recreating from memory.

**This route is available once per block.** A second delete-and-recreate of the same block is not a
further step in the ladder; it is the loop `SKILL.md` CRITICAL 6 stops, and each of these calls counts
against that session budget.

**And the ladder can be cut short from above.** `SKILL.md` step 6 says to stop **only after both**
routes: that bounds when *you* may give up on a block, not when CRITICAL 6 may stop the session. Where
the session budget is spent, or where the objection names something no write of yours can send, you
stop **without** finishing the routes — and report the block as unverified, which is what step 6 asks
for either way.

**Only if the block still reads back wrong after that: stop.** Report exactly which block, which
field, and what you tried. Do not move on, and do not describe that block as built. **If the
disagreement is an objection naming something no write of yours can send, neither route applies at
all** — the body is not the cause, and CRITICAL 6 says what to do instead.

# References

- `SKILL.md` → step 1(c) — the pre-write read this page's orphan check belongs to
- `SKILL.md` → step 6 — the verification step, and the two halves of the diff
- `SKILL.md` → CRITICAL 6 — the session budget, and objections a rewrite cannot close
- `references/troubleshooting.md` — one row per situation, including the read-back rows
