# One research pass, then one question batch

`SKILL.md` states the rule in two halves: **survey first** (step 2), **ask once** (step 3). Read this
in step 2 — the survey exists to feed the batch, so you need to know what the batch will want before
you go looking.

- [Before the pass: which project, in their words](#before-the-pass-which-project-in-their-words)
- [Before you ask: the one research pass](#before-you-ask-the-one-research-pass)
- [What the survey may not sweep](#what-the-survey-may-not-sweep)
- [Several flows in one request, and material you were handed](#several-flows-in-one-request-and-material-you-were-handed)
- [What to ask](#what-to-ask)

The list is not exhaustive and cannot be. **The reference is what says which fields a block cannot
be written without** (step 1a), so walk those required fields against what the request actually
said, and ask about every one that is a business decision rather than a platform value
(CRITICAL 2).

## Before the pass: which project, in their words

**Which project the flow is built on comes before everything else here**, because nothing below can
be looked up until it is fixed: the listings, the survey and the filter delegation all run against
one project. It is therefore **not part of the batch** — it is the precondition for the batch
existing, and asking it first does not break "ask once": the batch is the round the survey feeds, and
the survey cannot start until this one answer is in.

- **If only one project is reachable, do not ask at all.** Build there, and name that project at
  hand-over so a wrong assumption is visible while the flow is still a draft.
- **If more than one is, ask this one question on its own, immediately, and then run the pass.**
  Keep it to that single question — do not use the opening to ask half the batch blind.
- **Ask it in their world, and never in ours.** They do not have connected projects, servers,
  tenants, environments or contours — those are our plumbing, and naming one to a marketer is at best
  noise and at worst a word they will repeat back to us as if it meant something to them. So **do not
  print an internal label**, however convenient: not a deployment or environment name, not a
  connection or server name, not a tenant code. Name each project by its **human name** where you
  have one, and where the only labels you hold are internal, ask by what tells them apart in their
  terms instead — *"is this for the account you send real customer mailings from, or one you try
  things out in?"*
- **Their answer decides it; a mismatch is a stop, not a pick.** If what they name matches nothing
  you can reach, say so and ask again — never quietly build on whichever one you could reach.

## Before you ask: the one research pass

**One round of questions is the target, and a question asked blind is what costs you the second and
the third.** So before the batch goes out, establish everything you can establish without them, and
put what you found **inside the question**: not *"which folder?"* but *"three folders match what you
described — this one holds four automatic email mailings, the other two hold none; which is it?"*.
That is answerable from recognition, in one go, and a recommendation backed by what is actually in
each candidate is worth more than the question it replaces.

What the pass establishes, in this order:

1. **What the design needs at all** — from the reference, and where the request named a mechanic from
   that mechanic's own documents, including its list of decisions to settle first
   (`references/mechanics.md`). Until you know which fields a block cannot be written without, you do
   not know what to survey or what to ask.
2. **Everything the request already names** — resolved in the project's entity listing (step 2).
3. **The containers and the brands the flow will need.** Two listings, and what you need from each
   is different — see below.
   - **The brand catalogue is short** — the `entities` domain says so on the brand entity — so
     **read it whole here, before the questions.** That is what lets the brand question offer names
     they recognise instead of the bare word *brand*, and the brand is asked in the same section as
     the folder (below), so it has to be in your hands by now.
   - **Find the folder yourself before you ask about it.** Start from what the user described —
     their own words, and what the mechanic and the sends imply — and look it up by that. Where that
     matches nothing, **read the catalogue and judge it by meaning**: a folder's name often says
     nothing about what it holds, and the name a marketer would use is frequently not the name it was
     given. How that listing is searched and read is the `entities` domain's folder document — read
     it there, and take the live schema's word for how it is spelled today (`SKILL.md` →
     `## Where to look`). Then **open the plausible ones and see what is in them**: a folder you have
     not looked inside is a guess, not a recommendation. What goes into the question is what you read
     and judged — never rows that scrolled past while you were looking for something else, and never
     a folder recommended on its name alone. **Where you have read and judged and still have nothing,
     a question with no list is a legitimate outcome**, not a failure to research.

   Do this **before** asking about the folder, about the brand, or about which mailings a step will
   send.
4. **What is inside the plausible containers** — bounded; see the next section.
5. **What is already in the draft**, if you were given one (step 1c), and anything in it that
   conflicts with the design.
6. **What you have already established you cannot do** — an entity nothing resolves, a value the
   reference does not print, a setting no operation reaches — in business terms, with what it blocks.

**Then ask, once.** A second round is legitimate only for a **gap that blocks the build**: an answer
that resolves to nothing or to several candidates, a thing they named that no listing reaches, an
answer that skipped something a block cannot be written without. Never for something the survey could
have settled before you asked, and never for a detail the reference marks optional.

## What the survey may not sweep

**"Research everything first" cannot mean "list every catalogue".** One of them does not fit: on a
real project the **mailing catalogue runs to many thousands of rows** — the `entities` domain says so
on the mailing entity itself, and says which narrowings exist. Reading it whole is not research, it is
a stall, and it buries the four rows that mattered.

So the mailing half of the survey is **bounded, and the boundary is the folder**:

- **Never list mailings unnarrowed.** Narrow by the container, and by whatever the reference says
  distinguishes a mailing a flow can actually be told to send from one it cannot — read that on the
  entity first, and take the narrowing keys from the live tool schema, never from here.
- **Survey only the folders you picked out as plausible**, plus the neighbours the reference says are
  reachable from them. A handful of folders, not the tree. Where the request narrows it to one, that
  is one call and you have your recommendation.
- **If nothing in the request narrows the folders at all, read the catalogue and pick the plausible
  ones by meaning — but do not then open every folder to see what is inside.** Reading the folder
  catalogue is cheap; surveying the contents of each one is the sweep this section forbids. Take the
  few that could be it, look inside those, then **ask the folder question with what you found — a
  list, or nothing** — and survey the rest afterwards, once they have named one. That is not a second
  round of questions; it is research finishing after the one question it needed answered.
- **Report what you read, and only what you read.** "No automatic mailing in this folder" is a finding
  worth putting in the batch; a count you did not read is not.

## Several flows in one request, and material you were handed

**A batch of flows is one question round, not one per flow.** Whether it is several mechanics, a set
of flows migrating from another project, or logic being moved off another platform: do the reference
pass and the survey for **all** of them first, then ask everything in **one** batch, grouped so the
user can see which flow each answer belongs to. Build them **one at a time** afterwards, each to a
verified draft. Asking per flow turns one round into N, and it invites a mechanic to be designed
before its own questions are answered.

**Whatever you were handed comes first, in whatever form it arrived** — a written description, a
screenshot, a meeting transcript, an export from another platform in a format nobody documented, or
anything else. Read it, take every decision it already settles, and **treat only what is left as a
question**. Two things follow: it **reduces** this batch rather than replacing it, since it will not
settle the project's own entities or the permanent choices at creation; and **no format is promised
to be readable** — where you cannot make sense of what you were given, say which part and ask about
that, rather than inferring a design from it.

**A migration is a build, not a copy.** A flow read out of another project is context: its ids
resolve nothing in the target, and the decisions it encodes are still asked (`SKILL.md` CRITICAL 2).

## What to ask

- **The name or description of every thing the blocks point at** — never an id (step 2), with the
  candidates you found for anything ambiguous.
- **If you are creating the flow — which folder it belongs in.** Ask whether a folder holding the
  mailings this flow will send **already exists** — and **where your survey found candidates, ask it
  with them and with what each one holds**, not as a bare "which folder", and never as an id.
  **Where you read the catalogue, judged it, and nothing in it fits, the question still goes out; it
  just carries no list.** Say what you looked through and found nothing relevant under (so they know
  what has been ruled out and can correct you in one line), and ask what the folder is **called** —
  the one the mailings this flow will send live in. A name you can then look up; an id they do not
  hold. An empty survey is never a reason to settle on a folder yourself, and never a reason to read
  rows out as though they were their options.
  **A new folder changes what the flow can ever send, and that consequence has to arrive inside this
  question rather than in the hand-over — so read `references/creation.md` → *Asking about the folder*
  before you word it.** That section owns the consequence, the reachability boundary to read first,
  and the branch where nothing in this session creates a folder.
- **If you are creating the flow — the brand, always, in this same section as the folder.** **Do not
  derive it** from the folder, from a mailing, or from anything else: it is permanent, and a folder
  may permit many brands anyway. Ask about the shop, site or product line **by its name**, from the
  brand catalogue you read in the pass above (its item 3), not the bare word *brand*. Say in the
  question itself that this one cannot be changed afterwards. **Then, after the answers and before
  you create, check that the chosen folder permits the chosen brand** — and if the brand answer never
  came, **ask again for it**; do not infer one. `references/creation.md` has the wording, the check
  and the traps.
- **If you are creating the flow — what to call it.** Required, and theirs. Do not default it, do
  not compose one from the request, do not append anything to make it unique — the name is also what
  makes a create safe to repeat (step 1b), and that only holds while it is a name they chose.
- **The project's admin URL** — the address they open the platform at. You need it to hand over a
  link (step 8) and **no tool of yours returns it**, so it belongs here, not at hand-over. Skip it
  only if they have already given you one in this session.
- **Every place the request is underdetermined** — which trigger, how long a wait, what a limit
  should be, which branch does what, where a branch should end.
- **Where more than one kind of message is in play — how the sends are arranged, not only which
  ones there are.** Learning that they want an email and a push does not tell you whether two or
  three messages chase each other inside one mechanic, whether each mechanic sends its own single
  kind, or whether it is a third arrangement again — so **ask without presuming which**. Ask it in
  what they send, never as a channel and never as a field: *"does one message go out and then
  another if nobody reacts, or does each part of this send its own?"* **Leave the answer room to be
  per mechanic** — one arrangement for everything is an answer, a different one per mechanic is
  equally an answer, and a question about a single send cannot hold the second, so the person never
  gives it. Where a matched mechanic asks this question itself, its wording wins
  (`references/mechanics.md`).
  **The answer shapes the graph, so it belongs in this batch and not after the first write**:
  messages chasing each other are one path with a wait and a check between the sends, while separate
  mechanics are separate branches. Arriving late, it costs a rebuild — the same reason a mechanic's
  own decisions are asked here.
- **Every value a block *requires* that is the user's to choose and the request never gave.** A
  required field is exactly where the pressure to invent comes from — you cannot leave it out — and
  **an invented business value is stored looking precisely like a chosen one**: the read-back in
  step 6 cannot tell them apart, and neither can the user at hand-over.
- **Everything a matched mechanic says must be settled first.** Where the request matched a
  documented mechanic, that list is part of this batch — read it from the wiki now and ask it in the
  mechanic's own words, because no later write revises what those answers decide
  (`references/mechanics.md`).
- **Anything in the existing draft** (step 1c) that conflicts with the design.
- **Anything you have already established you cannot write** — an entity nothing resolves, a value
  the reference does not print, a setting no operation reaches. Say it now, in business terms, with
  what it blocks: it may change what they ask for, and a headline requirement they learn about at
  the end reads as a broken promise. Do **not** ask them for a way around it (step 2).
- **What every condition and every start-block entry filter should select, in business terms** — the
  audience in their own words is exactly what the filter agent needs, so ask for it here rather than
  guessing at it later. Say what a missing condition would mean (no filter means *everyone*); if the
  reference says this flow's scope set cannot express what they asked, say that now too.
- **Not the project.** That one is asked and answered *before* the pass, in the reader's own words —
  see *Before the pass* above. By the time this batch goes out it is already settled.

# References

- `SKILL.md` → step 2 — the research pass this file is read during
- `SKILL.md` → step 3 — the rule this list serves
- `references/creation.md` — the folder and name questions in full, and why they cannot wait
- `references/filter-delegation.md` — what the filter agent needs from the audience answer
- `references/mechanics.md` — following a documented mechanic, and when its decisions are asked
