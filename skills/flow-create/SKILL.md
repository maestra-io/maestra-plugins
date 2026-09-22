---
name: flow-create
description: >-
  Build a correct draft marketing scenario (flow) from a plain-language request: read the
  flows reference, resolve the entities the design needs to real ids, create and fill the
  blocks, wire the outputs, verify every block by reading it back, and hand over a link.
  Use when asked to create, build, assemble or set up a new flow, or to add blocks to an
  existing draft; when asked to move, transfer or migrate a mechanic or a flow from one project
  to another, whether one or a batch of them; when asked for several flows in one go; and when
  asked to rebuild here the logic a client is moving off an external marketing-automation
  platform — in whatever language the request comes in, and whatever the reader calls
  the thing: a flow is also a scenario or a journey, a send step is a mailing or a campaign,
  an entry filter is an audience or a segment. Don't use to audit a flow (use
  maestra:flow-issues-audit), or to launch, stop or delete anything.
metadata:
  author: Maestra.io
  upstream: AI tribe
  version: 16.3.0
---

# Flow create

Turn a plain-language request into a **correct draft flow**. The hard part is not the graph — it is
getting every block's properties, field names and entity ids right, and *knowing* you did. **This file
deliberately carries no field names, no property values and no per-block procedure:** those change, and a
copy of this file cannot. They live in the wiki, which can — read them at the right moment
(`## Where to look`).

You fetch and write everything yourself with the flow tools. Two things are **not** yours to invent:

- **Filter conditions.** The predicate inside a condition block, and the entry filter on a start
  block, are authored by the **filter-building skill, which you run in a sub-agent** (it is
  `maestra:filter-build` in today's skill listing — take the name from the listing, not from here);
  you write back what it returns, unchanged, and verify it landed. Never compose, edit or retype a
  filter body, and never resolve the entities inside one — that agent does both. **A body is only
  usable if the answer shows that skill produced it** (`## Filters and entity scope`).
- **Marketing mechanics.** A request may name a *mechanic* — a marketing job people expect a known
  shape for — rather than describe the flow block by block. **That shape is never yours to recall.**
  The `flows` domain's **mechanics sub-folder** says which are documented and how each is read: **go
  there before you design anything.** If one matches, **it is the design**, and what it says must be
  settled first is asked in the step-3 batch, **before your first write**. If none matches, say so and
  ask the user to describe the flow they want; build **only** what they describe. **Never improvise a
  mechanic that folder does not carry**, and never read one out of a preset's *name*. Its
  cross-mechanic rules bind every flow, matched or not. **Read `references/mechanics.md`.**

**Never launch, test-launch, pause, stop or delete a flow, and never call a tool that does** —
including anything that sets a testing or test mode, whatever it is named. Creating a flow, reading,
applying operations and validating are yours; nothing else is, and you must not claim to have started one.

**What "done" means for you.** A **verified draft**, plus an **honest, ranked account of what is
missing**. That is success, not failure — and so is stopping short of a verified draft when you are
stuck, which has its own rule (CRITICAL 6). Expect some part of a routine request to be out of your
reach — a condition the flow's entity scope cannot express, an id no listing tool covers, a setting
no write operation exists for — and **find out which while you are still planning writes**, not at
hand-over: validation reminds you of some of it and not the rest, so it is not your checklist.

**Rank what is missing; do not just list it.** Two kinds, and they are not comparable: **a small
human follow-up**, and **a shortfall in the user's headline requirement** — where the flow will not
do what they asked, or will not run at all. **Write each one down with its kind the moment you hit
it**, from step 2 onward: it is the one thing step 8 needs that step 8 cannot reconstruct
(`references/hand-over.md`).

## Where to look

The reference is the **wiki**: linked documents grouped into domains. Two domains matter here.

- **`flows`** — the domain overview, a document per block type, and a **write-path sub-folder**
  carrying the write contract: how a flow is created and what its arguments take, which fields a
  block takes, what values they accept and mean, what must travel together, what the server assigns,
  what a read includes that a write must not send. **Read the write-path sub-folder before your first
  write, every time.** Block documents say what a block *does*; the write-path sub-folder says how to
  *write* one — read both, per block type.
  The same domain also carries a **known-issues sub-folder**: the ways the write path currently
  misbehaves, indexed by the **symptom you observed**, each with the recovery for it. Go there the
  moment something is inexplicable — its index is the symptom table — **and take the recovery from it
  instead of reasoning one out.** A guessed recovery on this branch is usually a deletion, and
  deleting a block that was fine leaves the real cause where it was. **A recovery you take from there
  outranks the generic ladders in this file and in `references/troubleshooting.md`** — see step 5,
  which also says what it does **not** outrank.

  > **One class of it cannot wait for a symptom.** Some of what goes wrong there is **silent and has
  > no undo**: something the block already held, that your body never mentioned, destroyed at success,
  > with no message and nothing on a later read. It never becomes inexplicable, so "go when something
  > surprises you" never fires and the recovery is a **rule to follow before writing**. **So read the
  > sub-folder's index before your first write** — and **open every leaf whose symptom is something
  > you did not send going missing, or that says the loss cannot be undone.** Take its pre-write rule
  > into the body you build and into the check in step 6; the rest still waits for a symptom.
- **`entities`** — which identifier a given place wants. Several ids travel side by side under
  different names and one does not substitute for another.

**Reaching it: call the `wiki` tool**, one document per call, naming the domain explicitly.
Take the tool's name from your tool listing, not from memory. It serves these domains whole, and it
is the **only** route to them: there is no second copy of the reference for you to read, so a field
name or a value you cannot get out of a call is one you do not have (CRITICAL 1, CRITICAL 2). **Do
not decide from its schema whether it can serve you: call it** (the tie-breaker below). An index
answers in a single locale and there is nothing to pick — read it as it comes.

**With no `wiki` tool in the session you have no reference, and that is a stop.** Say so plainly as a
missing capability, naming the tools you do have, and **do not write from memory of field names** —
that is fabrication (CRITICAL 1, CRITICAL 5). Do not go looking for the documents somewhere else.

**Navigate, never guess — and there is no search.** Retrieval is walking the tree and nothing else:
root index → the domain index → a sub-section index → a leaf, taking every id from the `# References`
list of the index you are standing on. **Never construct an id**, and if you do not have one, go back
to the nearest index and take it from there — that is what keeps you off invented documents. **There
is no grep, no full-text search and no call that lists a domain's documents**, so the indexes are the
only entry points there are: the domain index carries a **term map** from the user's own wording to
technical ids, and the known-issues index a **symptom table**. Turn the user's words into a term
there *first*, then walk down. Where neither table carries your term, **read the indexes one level
down rather than guessing a document id**; if it is genuinely not there, that is a documentation gap
to report (CRITICAL 2), not something to reason out.

**One limit, and it is not a reason to distrust what it answers.** Different contours serve different
revisions and **no answer carries a version marker**, so you can never promise the user the reference
is current. Read it as the reference anyway: it is the contract you have, and CRITICAL 1 is about
reading it rather than recalling it.

**The tools are authoritative for their own signatures.** This file names capabilities —
`flows_create`, `flows_lookup`, `flows_get`, `flows_apply_operations`, `flows_validate`,
`entities_list` — and never their argument shapes. Where the live tool schema disagrees with anything
you remember, **the live schema wins**; read the operation vocabulary you need off it before you build
a call. **The same tie-breaker settles what a tool can *reach*:** a listing tool's schema moves faster
than any document about it, so **before reporting an entity as unresolvable because the reference says
nothing covers it, look at the live schema and try it** — one call, not a sweep (CRITICAL 6).
The reference wins on meaning; the tool wins on its own coverage.
**But a schema read is not a capability check, in either direction.** A schema can advertise what the
service refuses, and it can hide what the service serves — both have happened here: a listing that
offered kinds it would not accept, and the `wiki` tool, whose argument list still names one domain of
the three it answers. So a schema is never grounds for concluding a call would fail. **The only
capability check is the call** — one call, and read the answer (CRITICAL 6). That is what "the tool
wins on its own coverage" means in practice: the *running* tool, not its description.

**Every write carries the iteration it belongs to** — the one argument this file does name, because
no schema and no reference can supply it. `flows_create` and `flows_apply_operations` take a
`metadata` object with an `iteration` number that nothing in the product reads: it exists so the
adoption measurement can count the rounds a flow took before launch, and you are the only one who
knows the count. Start at **1** and hold it across everything you write — **raise it only when a
person has seen a result and asked for a change.** A retry after a refusal, the next batch of the
same plan, a block you fill on step 5: all the same iteration. Omitting the field loses the
measurement with no trace; counting your own retries as iterations fakes it.

## Filters and entity scope

**Where a filter shares a block with that block's other settings, it travels — complete — in *every*
write to that block, however unrelated the change.** The start block's entry filter is the case that
matters: a body that sets its timing and omits the filter can **destroy the filter**, at success,
silently — nothing in the answer says so, and no later read reports it. The flow becomes *everyone*,
with no undo, and the *later* write is the dangerous one, so no order of writes is safe. So: **the
filter goes in the body, every time**, whether or not the reference lists your write among those that
reach past what they name (`## Where to look`). **Read the block before you write it** and re-send the
filter it holds unchanged — neither composing a filter nor editing one (CRITICAL 3).

**Everything else about filters is `references/filter-delegation.md`'s, and it is mandatory before
your first delegation**: the flow's **entity scope set** — fixed by the start block, the same at every
block, obtainable only from the reference, and to be checked against what the user asked *before* you
ask for a filter — how to launch the sub-agent onto that skill, the provenance check that is the one
failing *silently*, and how to verify the body after the write. **One condition block per call.** Flow
tools do not imply filter tools — the two toolsets are gated independently.

## CRITICAL

**1. Read the reference before you write. Every time.**
Not from memory, not from a previous session, not by analogy with another block type. The
write-path sub-folder before your first write; the block document for every type you touch. A
field name or a value you recall is a guess wearing a fact's clothes.

**2. Never guess a value.**
If the reference does not give it, you do not have it. Distinguish two cases:

- **Something only the user could know** — a time zone, how long a wait, **what a thing they want
  the flow to point at is called**: **ask** (step 3). A name is always theirs to give; an id never
  is (step 2).
- **A platform value** — a field name, an accepted value, a discriminator, a code: a marketer
  cannot know it, so do not ask, do not guess, and **do not derive it from a similar field
  elsewhere**. Report a **documentation gap**: name the field, name the document that should
  print it, and say what you were trying to express. Then **stop that one write** and build the
  rest of the flow. Carry the gap into step 8 as a ranked shortfall.

**Some values are both** — the user knows the *thing*, the platform owns the exact **form** it is
written in. Take that form from the reference, or from a block in this project that already carries
one; **never assemble it yourself** from something you calculated or from another value's pattern.
And check the reference whether the field is needed at all first: **one it marks optional is
omitted, not chased** — asking about it costs the user a question for nothing.

**An existing flow is context, never an answer.** What you read in one — a wait, a limit, the thing a
block points at — records what somebody once decided, not what this person wants now, so it **never**
retires a question step 3 would have asked. **That holds for a flow you were asked to *move* to
another project too:** the ids in it resolve nothing in the target, so a migration is a build from
the source's *design*, resolved fresh there (step 2) — never a body carried across. Harvesting a value is legitimate only where the paragraph
above sanctions it, and the **decision** it encodes is still asked (step 1c, step 3).

**3. Send what you mean.**
Build each body from the reference and your own intent. **Never echo an object you read back as a
write body** — a read carries members the server owns and members belonging to a shape other than
the one you are writing, and copying an identifier you did not mean to set can change something you
were not asked to touch. Read a block to *learn* its values; then build the body.

> **One exception, narrow and load-bearing: a value you must send back to keep.** Some fields are
> stored as a **whole set** — the list you send replaces the stored one entire, and a body that leaves
> it out or empties it destroys it. The **only** way to preserve one is to send back exactly what you
> read, **unchanged**. That is not the act this rule forbids: the ban exists to stop you **composing
> or mutating** a value you do not understand, and handing one back untouched does neither. The
> exception holds only under all of these — the same field, on the same block, from a read you took in
> this session; passed through **byte for byte**, not one member, order or character altered, and not
> retyped; and done to **preserve**, never to author or change. The moment you would edit any part of
> it you are outside the exception. Which fields are whole sets, and which writes destroy them, is the
> reference's to say (`## Where to look`) — never your inference from a field looking list-shaped.

**An object goes whole.** When a body carries a nested object, send **every** member of it — not
only the member you want to change. Whether a half-sent object is completed from the block, from its
own defaults, or refused outright is the **reference's** to state, and it has changed before; a body
carrying every member is correct under all three, and it is the habit the write-path sub-folder asks
for. So treat it as settled: there is no such thing as changing one member of an object — to change
one, send them all, with the member list taken from the reference (CRITICAL 1), never from what you
happen to remember of the object's shape. **And what your body does not name is not thereby safe:**
see CRITICAL 4.

**4. Verify every write by reading it back and diffing what you sent.**
The spine of the skill, not a safety net. A success response acknowledges **receipt, not effect**:
it says the graph is as you asked and nothing about whether the properties landed, and an advancing
version token is not a success signal either. So after every write, read the block back and compare.

> **The test has two halves, and a write that passes only the first is not verified.**
>
> **(a) Every field you sent is present and equal.** A read-back is a **superset** of what you sent
> — the server fills in members you never wrote — so **an extra key is never a mismatch**, and
> equality of the two whole objects is not the test.
>
> **(b) Nothing you did *not* send has gone missing or changed.** A field your body never mentioned
> is not thereby safe: a write can empty or overwrite something it never names, at success, with
> nothing in the answer saying so and nothing reported on a later read. Half (a) is blind to it by
> construction — the field that was destroyed is the one you were not going to look at. So the diff
> needs a second thing to compare against: **the read you took of that block before you wrote it.**
> Keep it. Anything the block held before, that you did not send, and that came back changed or
> gone, is a real loss — treat it as a failed write, not as noise, and restore it (step 6).
>
> A read after a write can print different members from a later read: right after a write you may
> see the values you sent, while the platform's own projection of the block — resolved entity
> objects, server-assigned ids — appears on a later read. The block is intact; nothing was lost. Do
> not send those members back: they are not writable. Members you *can* write — a filter, a wait, a
> set of conditions, a name — are still yours to check, and their loss is still a failed write.
>
> **Which member is which is the write contract's to say, not yours** (`## Where to look`,
> CRITICAL 6): a member the reference puts on no body you can build is not restorable, so its
> absence is never a failed write to repair.
>
> **And a `flows_validate` between the two reads makes them incomparable.** That call re-shapes the
> blocks of the version it runs on, so a pre-write read taken before it is no baseline for a write
> made after it: half (b) has **not** been run, a fresh read is owed before that write, and you do
> not diff across the call or repair what such a diff shows (step 7).
>
> This is why half (b) is stated as a rule and not as a list of the writes it applies to: **which
> writes reach past what they name is the reference's** (`## Where to look`), it moves, and a copy of
> it here would go stale exactly where it costs a filter.
>
> **Predict a server-computed value before you write, and check it afterwards** — the reference says
> which values those are. One that matches is the strongest evidence your fields were interpreted,
> and one absent where it should exist means the configuration did not take. The arithmetic is only
> cheap while you are still designing.

**5. Never fabricate, and never report a flow as built on the strength of a success response.**
No invented field, value, discriminator, id or filter body. If a read-back shows a block unfilled, or
missing from the response, or a tool errored, or an entity could not be resolved: say exactly that. A
half-built flow honestly reported is a good outcome; a "done!" over constructor defaults is the worst.

**Nor on the strength of a read-back.** For a step body and for a filter, a clean read-back proves
only that what you sent was **stored** — the subsystem that has to accept it does not see it until
step 7, so it can refuse a block that verified in full. A flow handed over **without a
`flows_validate` that came back clean has not been accepted**, and calling it built is the same
fabrication as inventing a field. Where the call reported problems, or could not be completed, or was
never made: say plainly that the flow is unvalidated and give the message as it came
(step 7, `references/hand-over.md`).

**6. Stop when you are stuck. Stopping is an outcome, not a failure.**
Every other "stop" in this file ends **one branch** and the flow goes on. This one ends **your
writing**. It outranks every budget, ladder and documented recovery in the procedure, because the
loop it catches is invisible from inside: a body that is already correct, re-sent against an
objection no body can close.

- **A session budget, and nothing suspends it.** Count the write calls that did **not** move you
  forward — a re-send after a read-back that still disagrees, a repair, a delete-and-recreate — across
  the **whole session and all blocks**, not per block. **At six, stop writing.** A documented recovery
  runs *inside* this count (step 5): it can fix the order of your next calls, never that there is no
  limit, and rephrasing the same objection does not restart the count.
- **Some objections are not yours to close, and the test is the write contract, not your judgement.**
  Where a validation entry or a refusal names **something no write of yours can send** — the
  write-path sub-folder puts it on no body you can build, and no operation sets it — **the body is not
  the cause**, and re-sending it in any shape closes nothing. Check the sub-folder once, for that
  thing, by name; if it is not writable there, say which it is, say that no write reaches it, and stop
  that block. The flow will not run until somebody with another surface sets it: that is a shortfall
  to rank (step 8), not a bug to grind at.
- **A diagnosis is not a failed attempt.** Where an answer — a tool's, a sub-agent's, or your own
  reading of the reference — puts the cause **outside the body you are sending**, that branch's budget
  is spent at that answer. Do not spend the rest of it re-sending, and **do not re-delegate the same
  request to hear the same thing again**: a second agent reaching the same conclusion is one answer
  paid for twice, not a second attempt.
- **Genuinely stuck means say so directly, at once.** An entity that cannot be resolved, a tool or
  API that does not work: **grinding on one spends the user's tokens on nothing.** Name it in plain
  words and stop that branch. **The exit is a decision you put to the user, never work you hand them**
  — everything about never asking a human to perform a step by hand stands (step 1b, step 2), and
  putting a *decision* to them is a different act that is open to you, as is a question after the
  batch (step 3). What goes in it is step 8's (`references/hand-over.md`).

## Inputs

- The request, plus whatever else you were handed; the project, where several are reachable (step 2).
- If a flow already exists to build into: its id and the number of a version whose status accepts
  writes, which the write-path sub-folder tells you. If it does not exist yet, **step 1(b) creates
  it** — and what that needs is the user's: the folder, the brand, and what to call it (step 3).

## Procedure

### 1. Read the reference, get the flow you will build into, and read what is already in it

**(a) Read the reference first**, per `## Where to look`: the `flows` overview, the mechanics
sub-folder when relevant, the write-path sub-folder with its pre-write known issues, every block doc.

**(b) Get the draft — create one when there is none.** Handed a flow id and a draft version, you have
the draft: skip to (c). Otherwise create it with `flows_create`, which hands back the flow and the
draft version number for everything that follows.

**A create needs answers you do not have yet.** The folder, the brand and the name are settled **at
creation** and no block operation writes them, so for a new flow the order is 1(a) → **step 2** →
**step 3** → **check the folder permits the brand** → create → read the new flow back → then (c) and
step 4 onward. A create is a write, so CRITICAL 4 applies. **Never guess the folder:** it fixes for
the flow's whole life which mailings the flow can ever send, and a wrong one is **accepted at
creation in silence**, surfacing much later at a send step as an unrelated-looking scope error.
**Resolve it from what the user named (step 3), or stop** — never copy one from another flow,
whatever a message may advise. **Read `references/creation.md` before your first create**: the folder
trap, the brand-new-folder consequence that has to reach the user *inside* the step-3 question, and
what to confirm on the read-back are all there.

**If nothing in this session creates a flow**, and you were not given a draft: stop and report a
**missing capability** in plain words, naming the tools you do have. Do not hunt for a substitute, do
not build into another flow, and **do not hand the user the job of making one** — a step you ask a human to perform by hand is how a defect becomes the design.

**(c) Read the draft before writing into it — always.** Whether you just created it or the user
handed you one, read its structure at skeleton detail over the whole flow, and record **the current
row version** (this read is where you get it) and **an inventory of what is already there** — blocks,
their types and names, and the edges. A draft is often *not* empty, and a design made without looking
can be refused by a block you never saw. **Read it as context, never as an answer** — nothing in it
retires a question step 3 asks, however settled it looks (CRITICAL 2).

**If the design does not want an existing block, delete it, in the same batch as the rest of your
writes** — after reading it (step 5) — **and never leave a block unwired.** An orphan fails
validation, and the write path reports only *that* a block is unwired, never where its edge belongs.
**So decide the wiring here**, from `references/graph-and-verify.md` → *Orphans and wiring*.

### 2. Resolve the entities the design needs — before you build any block

Blocks reference entities by **id**, never by name — so **the person supplies the name, the listing
supplies the id.** Read the `entities` domain for which identifier a given place wants, and pass on
exactly what was asked for, as printed. **Never ask a marketer for an id, in any form**: it is not
something they hold, so asking turns a lookup you should be doing into their failure to answer, and a
value they dig up elsewhere is often one the platform refuses. Ask what the thing is *called*.

**A flow you are creating has two entities of its own, resolved here before it exists** — the
**folder** it lives in and its **brand**. Both come from names, **both are asked in the same section
of the one batch** (step 3), and both are said to be permanent as you ask. **Never derive the brand**
— not from the folder, which may permit many, nor from a mailing: it is a guess at a decision nothing
repairs. **Before you create, check the chosen folder permits the chosen brand**
(`references/creation.md`). Take from the reference **which** of an entity's ids each argument wants,
keyed on the argument's **type**, never on its name — on one of these two the decisive-looking word
names ids of both types.

**Steps 2 and 3 interleave once, in this order — so this pass is where everything the questions need
comes from.** **Start from everything you were handed, in whatever form it came** — a description, a
screenshot, a transcript, an export from another platform in a format nobody documented: read it, take
every design decision it already settles, and treat what it does not settle as a question (step 3).
It **reduces** the batch; it never replaces it, and no format is promised to be parseable. Then
resolve what the request already names with the project's entity listing (`entities_list`) — an empty
answer means *nothing of that kind matched*, not a partial search, so re-query with a different name
fragment. **Then survey what the request does *not* name,
before you ask about it**, so every question offers candidates instead of asking blind: answered from
a list it costs one round, answered blind it costs three. **Read `references/questions.md` before you
start this pass** — what to establish, what **bounds** the survey (not every catalogue may be swept,
and turning up no candidate is a legitimate outcome), and **which project to build on: asked on its
own, first, where more than one is reachable** — the whole pass runs against one project and a survey
run against the wrong one does not error. Take everything left into the batch (step 3): ambiguous
matches with their candidates, names that matched nothing, the things never named. **A second round is
only for a gap that blocks the build.** **If the design points at nothing by id, the resolving half is
legitimately empty** — the survey half is not.

**The listing does not cover every kind of entity yet, and its coverage moves.** Which lookup applies
to which kind is the `entities` domain's to say — but **where the reference says nothing covers a
kind, check the live listing schema before you believe it** (`## Where to look`). For an entity
genuinely out of reach the whole procedure is to **say so and stop**: name what is left unset and what
the flow will not do because of it, in business terms, in the step-3 batch, and carry it to step 8 as
a ranked shortfall. **Do not look for another way in** — no id from the user, no value borrowed from
another flow, no placeholder — and do not hand them the work. **And no sweep: paging a catalogue, or
reading flow after flow because one might carry the value, is not a resolution route**, whatever a
recovery you found suggests as a place to harvest one from. **A value you cannot resolve is declared
unfillable, and that is the outcome** — not the start of a search (CRITICAL 6).

### 3. Ask your clarifying questions — once, in a batch, before writing anything

Collect and ask together, in one round: step 2's pass has put the ambiguous matches, the empty ones
and everything you surveyed in your hands, so **every question carries what you found beside it** —
the candidates, and what each one holds — never a blind *"which folder?"*. Where a listing produced no
candidates at all, the question carries no list and says what you looked through instead — never rows
that scrolled past dressed up as the options. `references/questions.md` is the list of what goes in, and **a
matched mechanic's own pre-write decisions go in this batch too**, since no later write revises them
(`references/mechanics.md`).

**That list is not exhaustive and cannot be**: the reference says which fields a block cannot be
written without (step 1a), so walk those against what the request said and ask about each one that is
a business decision rather than a platform value (CRITICAL 2).

**Several flows in one request are still one round.** Whether it is a batch of mechanics, a set of
flows to migrate from another project, or logic being moved off another platform, do step 1(a) and
step 2 for **all** of them first, then ask the questions for **all** of them together in this one
batch, grouped so the user can see which flow each answer belongs to. Then build them **one at a
time**, each through steps 4–7 to a verified draft, and hand over once (step 8). Asking per flow
turns one round into N and invites a mechanic to be designed before its questions are answered.

**Do not start writing until they answer** — one batched round is cheap; a flow built on a guess is
not.

**Say which phase you are in, every time it changes — this is the promise the batch is worth.** Two
states, and the user needs to know which one they are in: **still researching**, so a few more
questions may follow shortly and they should stay; or **everything needed is in hand and the build
has started**, so they can walk away. **Say it in those terms**, at the top of the question round and
again the moment you begin writing. A question asked after you have declared you have everything is a
broken promise, and it is the expensive kind; a question asked while you have said you are still
researching costs nothing. So the ordering rule is: **check first what you can check cheaply, ask
what is left, and only then declare you have everything** — and if something genuinely unforeseeable
turns up later, say plainly that the earlier declaration was wrong before you ask.

### 4. Design the graph, then create blocks

Choose the start block from the user's answer — exactly one per flow — and take its fields from
the reference. Where a request could be served by more than one kind of trigger, prefer the one
you can author completely, and say so.

**Then settle the filters, before you build a single operation.** The start block is chosen, so the
flow's scope set is settled — and a filter is written with the block that carries it, so the bodies
have to be in hand before the first write. For every block that needs one: pick the scope from that
set, stopping and reporting the condition if the set cannot express what was asked
(`## Filters and entity scope`); **delegate to the filter-building skill in a sub-agent**, one filter
per delegation, **launching the sub-agent onto that skill** and checking the answer as
`references/filter-delegation.md` says; then **write the body and the scope together** in the same
condition, never one without the other. Never repair, reformat, retype or assemble a body.

Then build the operations — **which block is filled at creation and which is deferred to step 5, how
the edges are wired, why a dead end is a decision, and how a version-level setting is written are
`references/graph-and-verify.md` → *Building the operations*, together with carrying the row version
forward and what a refusal does and does not tell you.** Read it before the first batch.

**A send step with no mailing to name: create one, and mind the one-way doors.** One mailing per
send step, created by you — not through the mailing skills, because you need the identifier the
create hands back to bind the step to. **The kind is the loudest thing on that call:** a flow may
only ever send an automated mailing (`flows` → the send-step document), the create does **not**
default to one, and neither the kind nor the folder can be changed afterwards — a mailing made with
the wrong one is unusable and has to be created again, so both are settled before the first create
(step 3). Give the mailing a **name and a short description** of its business purpose and the
interaction it is meant to get, so it can be filled in later without reconstructing the intent:
**no content, and no state changes.**

**Every answer carries a validation list** — each unfilled and each unwired block, **by id**; it is
**not** a refusal, so a batch returning entries was applied. **Read it after every write** as your
progress meter — and for what it cannot tell you, `references/graph-and-verify.md` → *Orphans and
wiring*.

### 5. Fill deferred blocks one at a time

Each gets its **own follow-up update call**, one block per call. Worth the round-trips: a body accepted
that leaves the block **partly filled, or on its defaults**, is reported nowhere, and one block per
call is what makes that silent case attributable when you read it back (step 6). **A condition block
carrying a filter is always one of these** — one condition per call, no exceptions.

**Read a block at full detail immediately before you send a body to it, and keep that read.** It is
your only baseline for CRITICAL 4(b), and for anything a write destroys without naming it, the only
copy that will ever exist. If the block carries a filter, that read is also what you send the filter
back from (`## Filters and entity scope`, CRITICAL 3's exception).

**A delete takes that same read first, because it is the write with no undo at all.** Deleting a
block destroys everything it held and nothing brings it back, so **read the block at full detail
immediately before you delete it, and keep that read** — it is the only copy that will ever exist,
and it is what a recreate is built from. This binds **every** delete, the design's and the repair's
alike: a block the design does not want (step 1c) is deleted because it was decided, not because
something failed, so it does not count against the repair budget — **but it is not exempt from the
read.** A repair delete does count (CRITICAL 6). And a **second** delete of the same block, or a
delete of a block whose contents you never read, is a guess: stop instead of taking it.

**Retries are bounded.** One re-send of a *corrected* body is the budget — never the same body
after the same failure, and never a loop on an opaque error: stop and report which block and what
you tried. For a body that was accepted but read back wrong, step 6 says what "corrected" means.

**Transient and unsolvable are different, and only one is worth a retry.** A timeout, an
unavailability, a dropped connection may be worth up to two further tries; **anything the answer
*explains* is worth none** — that is a diagnosis, and CRITICAL 6 spends the budget at it. **A retry
must not be immediate**, and this harness gives you no reliable way to wait: unless you have other
work to put between the two tries, **you do not have a retry** — report it as a failure you could not
clear rather than looping on it.

**A documented recovery replaces this per-body budget — never the session budget.** When the symptom
matches one in the known-issues sub-folder, the procedure written there **replaces** this budget and
the generic ladders for as long as it runs: it is a diagnosis with a stated order, not blind
retrying, so follow its order rather than your own. But it runs **inside** CRITICAL 6, which nothing
suspends, and a recovery whose step would have you search an unbounded set — page a catalogue, read
flow after flow — is **not run at all**: the value is declared unfillable instead (step 2). Read the
recovery's two limits first — `references/troubleshooting.md` → *When a documented recovery outranks
this file*.

### 6. Verify by reading back — mandatory

**The write-path sub-folder has a verification page of its own — read it, and follow it.** Below is
the shape of the step; the per-block checklist of *which* field carries the most information is the
reference's, and it is worth more than a generic diff.

For **every** block you created or updated:

1. **Read it** — at full detail, either scoped to that block or in one whole-flow read. **Do not
   scope a read from the start block:** an unwired block is unreachable from it, its absence is not
   an error, and you would report an unverified block as built.
2. **Reconcile the sets.** Compare what came back against the list of blocks you wrote. A block
   missing from the response is **unverified** — never "fine".
3. **Check the block's properties are there at all**, and carry the shape discriminator you wrote.
   An empty or absent properties object is the whole failure this step exists to catch, and it is
   cheaper to see than any field-level diff.
4. **Compare against the body you sent** — every field you sent is present and equal, CRITICAL 4(a).
   Include the block's name, but **read it from where the reference says a read carries it, which is
   not where you sent it** — comparing it in the wrong place is a guaranteed false mismatch. Judge
   only the keys you sent; an extra one is normal.
5. **Then compare against the block as it was before you wrote it** — CRITICAL 4(b), the half step
   6.4 cannot do. Take the pre-write read you kept (step 5) and look at what your body **did not**
   mention: anything the block held then and does not hold now was destroyed by a write that named it
   nowhere and reported nothing. **This is the check that saves an audience filter.** A loss found
   here is a **failed write** — restore what was lost from that same pre-write read, **unchanged**
   (CRITICAL 3's exception), then verify again from 6.1.
   **But ask first whether it is a loss at all.** A member the reference puts on no body you can
   write is the platform's projection, not the block's state: it is neither restored nor repaired
   (CRITICAL 4(b), CRITICAL 6), and repairing one spends a forbidden write and a slot of the session
   budget on a block that is correct. **And if a `flows_validate` fell between your pre-write read
   and this one you have no baseline** — take a fresh full-detail read, write from there, and do not
   diff across the call (step 7).
   **The *create* write has no half (b) to run**: the block held nothing before it, and half (a)
   verifies a simple block filled at creation in full (step 4). **Every *later* write to that block
   owes half (b)** against the pre-write read from step 5, **whether or not you created the block** —
   the start block whose entry filter went in at creation and whose timing you set afterwards is
   exactly that, and it is the dangerous write (`## Filters and entity scope`). **With no pre-write
   read you cannot run this half**: never report such a write verified on half (a) alone. Both
   branches are in `references/troubleshooting.md` → *Reading back*.
6. **Check any value the server computes from what you sent.** The reference names which ones: one
   that matches proves the fields were *interpreted*, and one that is **absent where it should
   exist** means the configuration did not take even though every field came back. Work the expected
   value out while designing the write — afterwards it is expensive.
7. **Re-read a block's output tokens before wiring anything onto it if you have just changed its
   branches, cases or variants** — they are derived from its contents, so a token remembered from
   before the change can address a different branch, and the edge lands silently in the wrong
   place. This is not only about freshly created blocks.

**A field can match and still be unconfirmed, and the only fix is *before* the write.** The
verification page names the values the read path **regenerates** rather than echoing back what was
stored: a wrong one comes back looking exactly right, uncaught by the write and by validation alike.
Take each from the reference as you build the body, **do not report one verified** — and do not put it
in the hand-over either (step 8): a value only the reference can settle is nothing the user can act on.

**A stored filter gets one further check, in addition to the diff — not instead of it.** The body goes
in verbatim, so step 6.4 applies to it like any other field and is the cheaper of the two: do it
first. Then read the filter back, have it rendered into readable form, and compare the **meaning**
against the draft the sub-agent reported in that same language. That settles **structure only** — a
clause naming something out of the project's catalogue cannot be compared at that spot at all, and a
*correct* filter always looks wrong there, so it comes **out** of the comparison.
`references/filter-delegation.md` → *Verifying it after the write* has the rendering, what counts as a
genuine mismatch, and what to report.

**A block that reads back wrong is recoverable, not a write-off — but match the symptom before you
repair it.** Several ways a read-back can disagree are documented, each with a recovery of its own
that ends somewhere a generic ladder does not. **Go to the known-issues sub-folder, match what you
observed, and if it is there take that recovery** — it replaces every ladder and decides when to stop
(`## Where to look`, step 5). **Only if nothing there matches**, run the two ordered routes in
`references/graph-and-verify.md` → *Repairing a block that reads back wrong* — repair in place with a
complete body, then delete and recreate — and stop only after both, reporting which block and which
field.

**Check the edges too, on the read that actually carries them** — a narrower read answers the wiring
question without knowing the answer, and the response does not say which you got
(`references/graph-and-verify.md`, step 1c). Confirm the edges land where you designed, and **resolve
every orphan here, not later.**

### 7. Validate — after everything else is written and verified

**This step is not the last check — it is the first.** For a step body and for a filter, nothing
before it has been seen by the subsystem that owns them: the write stores what you sent, the
read-back prints what you sent, and **step 6 can pass in full on a block the platform will refuse.**
So the objections this call returns are the **normal case**, not the call misbehaving — never a
reason to treat a first-call refusal as terminal, or to hand over on step 6 alone (CRITICAL 5).

**Order still matters: validate after your last write, not in the middle of them.** Verify all of it
in step 6, then call `flows_validate` for the flow version. **A second call on a version that is
*still* passing tells you nothing:** it answers the same way without validating anything, and a run
of them is the loop CRITICAL 6 counts. **But an ordinary edit to a block reopens validation** — so a
later change is not a change that goes unchecked: verify it in step 6 and validate again. What you
must never do is hand over on the strength of a pass taken *before* your last write (CRITICAL 5).

**A version that came back with problems is the same shape.** Fix what is yours to fix, verify it in
step 6, validate again: that loop is `references/validation.md`'s, and it runs inside CRITICAL 6 like
everything else — what means stop is the *same* objection returning unchanged, not the fact of a
second call.

**The call also re-shapes the version's blocks, whatever its verdict, so it invalidates every read
you took before it.** Any write after a `flows_validate` needs a **fresh** pre-write read of that
block; the read you kept from step 5 is not a baseline across this call (CRITICAL 4(b), step 6.5).

**Never offer a passing validation as evidence the flow is correct** — a run that lists nothing is not
a warranty on anything you built, so report the problems it lists and nothing else: not the call, not
a status, not the fact that it passed. **Where the validation could not be completed the opposite
holds, and CRITICAL 5 governs:** a refusal, an answer naming nothing, a write you never validated
after making it — say plainly that the flow is unvalidated, and give the message verbatim. **A failed
validation can arrive looking like an ordinary answer** — read the text rather than skimming it, and
never infer success from a response merely not looking like an error.

**Read `references/validation.md` at this step.** It carries the call's own failure modes — which are
not the flow's problems and none of which is a licence to loop or to guess which block caused one —
how to sort what it reports into the three kinds, and the path for a change the user asks for after
you validated. Do not improvise any of them.
### 7b. Then the mailings, with the user — one at a time

Every mailing you created in step 4 is still a name and a description. **Fill them by handing off to
the mailing skills** — take their names from your skill listing — **one mailing at a time, and never
unattended:** each one has several points where only the person can choose or confirm, and what they
are shown depends on the host. Then verify the blocks you touched (step 6) and **validate again**
(step 7), which the mailing edits have reopened.

**Nothing sends until a person activates each mailing, in the interface** — no tool of yours does it,
and until they do, the flow renders instead of sending (`flows` → the send-step document). That is
the one thing standing between the flow you built and its first message, so it goes in the hand-over
per mailing, alongside the flow's own launch.

### 8. Hand over

A link to the draft version you built, then three parts and nothing else: **what was built** — reuse
the `maestra:flow-summary` skill's own output format rather than inventing one; **Actions** — a checklist
of what the user must check or fill, or must tell you so you can do it, every item something they can
*do*; and **Suggestions** — how the flow could go further, phrased as an offer. **Cut everything they
cannot act on**: no system names, no tool behaviour, no platform quirk. **Read
`references/hand-over.md` first** — the link rules, the three parts, what never goes in, and how a
stop under CRITICAL 6 is reported.

## If something goes wrong

`references/troubleshooting.md` has one row per situation you can hit — a refused write, a call that
never answered, an entity out of reach, a read-back that disagrees, a validation that names nothing, a
delegation that comes back wrong. **Read it when something goes wrong**; it does not lift CRITICAL 6.
