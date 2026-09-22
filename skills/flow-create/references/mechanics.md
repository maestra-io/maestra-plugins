# Following a documented mechanic

Read this when a request looks like a **mechanic** — the person naming a marketing job and expecting
a shape for it, rather than describing the blocks they want. `SKILL.md` carries the rule; this file
is how to run it.

## What the reference owns, and what you own

The wiki's mechanics sub-folder owns **the assembly**: which mechanics are documented, what each one
is for, what has to be settled before it can be built, what shape it takes, and what goes in its
blocks. None of it is restated here or in `SKILL.md`, and none of it is yours to recall: both files
only send you there.

You own the **behaviour**: deciding whether a request is one of them, asking what the mechanic says
must be asked before anything is built, building it under the write path's rules, and reporting
honestly what you followed and where you left it.

## Deciding whether one matches

1. **Read the sub-folder's index first.** It is the only thing that says which mechanics exist. A
   mechanic you remember and cannot find there does not exist for this purpose.
2. **Read a candidate's documents in the order the folder states**, and stop at the one that answers
   the question you currently have. The document written for recognition is what decides a match —
   never the mechanic's name, and never a later document skimmed for its shape.
3. **Match on what the mechanic says it is for, against what the person actually asked for.** A word
   in common is not a match. Where it plainly covers the request, it — not your own arrangement of
   blocks — is the design.
4. **A partial match is not a licence to stretch it.** Take only what it covers, tell the user which
   part of their request it covers and which it does not, and treat the remainder as an ordinary
   request: described by them, built from their description.
5. **If nothing matches, say so plainly** and fall back to what the skill already does — ask them to
   describe the flow they want and build only what they describe (step 3). That path is unchanged,
   and taking it is not a failure.

**A preset named after a mechanic is not that mechanic.** A preset is a prepared graph and nothing
else — no trigger settings, no filter, no mailing, no entity of any kind — so its name tells you
nothing about what the mechanic is and saves you none of the work. The folder remains the only source
of the assembly, and every block still has to be filled and verified (`references/creation.md`).

**Never improvise a mechanic the folder does not carry, and never fill a hole in one that it does.**
A mechanic the request needs and the folder lacks is a **documentation gap**: name it, say what you
asked the user instead, and carry it to step 8 (CRITICAL 2). A folder you can read, with theirs not
in it, is a fact about the reference — not a licence to supply one from memory.

## The decisions come before the first write

A documented mechanic states what must be settled before anything is built, and the folder is where
that list lives. **Read it at that point — before your first write — and ask it in the step-3
batch.** Not after the first block, and not discovered while filling one: what those answers settle
is not what a later write can revise, so an answer arriving late costs a rebuild.

Ask them the way the folder phrases them, in the marketer's words, never as a field name and never
as an id (step 2). They go in the **same batch** as everything else you have to ask — one asking
moment per flow, not two — alongside the ambiguous entities and everything you have already
established you cannot write.

Where the folder states what to do with a question that goes unanswered, follow it — and **say at
hand-over that you did**. An assumption the reference licenses is still an assumption the user has
not seen.

## Building it

- The mechanic decides **the shape**: which blocks, in what order, and what each one is about. The
  write path decides **how a block is written**: fields, values, bodies, verification. They do not
  compete — where a mechanic's wording reads like an instruction about writing, the write-path
  sub-folder and the `## CRITICAL` rules win (`SKILL.md` → `## Where to look`).
- **Filters are still not yours.** A mechanic saying what a condition is *about* is not a filter
  body; delegate it like any other (`references/filter-delegation.md`).
- **Entities are still resolved from names, by you** (step 2). A mechanic naming the *kind* of thing
  a block points at never supplies an id, and no mechanic makes one guessable.
- **Verify every block regardless** (step 6). A mechanic that matched perfectly is no reason to
  trust a write.

## The rules that hold across mechanics

The sub-folder also carries the rules that belong to no single mechanic. **They apply to every flow
you build, matched mechanic or not** — a flow assembled from a plain description can break them just
as easily, and nothing in the tools reports it. Read them while you are in the folder and design
against them; where the user's request forces you to break one, say so and why at hand-over rather
than quietly.

## At hand-over

Name the mechanic you followed, and **every place your build departs from it** — a branch left out,
a question that went unanswered and what you assumed instead, a part of the request it did not
cover. Ranked with the rest of what is missing (step 8, `references/hand-over.md`). A design the
user cannot compare against its reference is one they have to re-derive from the graph.
