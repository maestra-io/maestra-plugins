# Creating the flow

Read this before your first create. The rules behind it are in `SKILL.md`; nothing here overrides
it, and nothing here is a substitute for the reference — where a row says "the reference", go and
read it. The **live tool schema** owns the argument shapes; this file owns the order you do things
in and the decisions you must not make for the user.

- [What a create needs, and where each part comes from](#what-a-create-needs-and-where-each-part-comes-from)
- [Why the questions come first](#why-the-questions-come-first)
- [The folder is the decision you cannot take back](#the-folder-is-the-decision-you-cannot-take-back)
- [Asking about the folder](#asking-about-the-folder)
- [The brand: asked, never derived](#the-brand-asked-never-derived)
- [Before you create: does the folder permit the brand?](#before-you-create-does-the-folder-permit-the-brand)
- [The name, and why a repeat is safe](#the-name-and-why-a-repeat-is-safe)
- [Starting from a preset](#starting-from-a-preset)
- [Verify the create like any other write](#verify-the-create-like-any-other-write)
- [When a create is refused](#when-a-create-is-refused)

## What a create needs, and where each part comes from

Four things, and none of them is yours to invent:

| What | Where it comes from |
|---|---|
| The **folder** the flow lives in | the user names it; the entity listing turns that name into the id (step 2) |
| The **brand** the flow belongs to | the user picks, in words they recognise, **in the same questions section as the folder** (step 3) — **never derived** — see below |
| The flow's **name** | the user, always — see below |
| A **preset**, optionally | the **live tool schema** says which presets exist; **nothing says what one contains** — see below |

Two notes on the ids, both of which the reference settles and neither of which you may settle
yourself. **Which of an entity's ids a given argument wants is stated in the reference** — the
write-path sub-folder for the argument, the `entities` domain for the entity — and an entity can
carry several ids under different names. **Do not choose one by how the argument is named:** the
reference keys the choice on the argument's **type**, and on one of these entities the word that
looks decisive appears in the names of ids of both types. Read it, take the column it names.

## Why the questions come first

A flow's folder and its brand are settled **when it is created** and are not what the block
operations write. So the order for a new flow is: read the reference (step 1a) → resolve what the
request already names (step 2) → **ask your batch** (step 3) → **check the folder permits the brand**
→ create → read the new flow back → then design and write blocks (step 4 onward). Creating first and
asking afterwards is not a shortcut, it is the mistake: you would be choosing the one thing that
cannot be changed later before asking the one person who knows it.

## The folder is the decision you cannot take back

**The folder fixes, for the flow's whole life, which mailings it can ever send.** The reference
states the boundary exactly; what matters here is the shape of the failure. A folder that does not
suit the flow is **accepted at creation without complaint**. Nothing is wrong until, much later, a
send step is written — and then the refusal reads like an unrelated scope error about a mailing, at
the point furthest from its cause, on a flow that cannot be repaired by editing that step.

So: **resolve the folder from what the user named, or stop.** Never copy a folder from another
flow, never take a loose match because it was the only row that came back, never carry one over
from a previous session, and never proceed on a folder nobody named. If a refusal message — or
anything else — suggests taking a folder id from an existing flow, that is advice to make exactly
this mistake: do not follow it.

## Asking about the folder

In the step-3 batch, in the user's own words:

1. **Ask whether a folder with the mailings this flow will send already exists — with the candidates
   your survey found and what each one holds**, or, **where it found none, with no list and what you
   looked through** (`references/questions.md`: a folder's name often says nothing about what it
   holds, so a survey that turns up nothing relevant is a normal outcome). Either way it is a question about
   what the folder is *called* — never "which folder id", which is not a thing they hold.
2. **They name one:** resolve it in the listing, by name. Several matches, or none, is a second short
   question naming what came back — not a guess.
3. **They say there is none, or they want a new one:** a flow can still be created in a new folder,
   and this is where the choice is won or lost, so **the consequence goes in the question, not in the
   hand-over.** A folder created from scratch **holds no mailings and sits under nothing**, so the
   only mailings that flow will ever send are the ones you create in it yourself (`SKILL.md` step 4):
   **nothing they already have becomes reachable**, and not later either, because the folder never
   changes. Where the mailings they want live in a folder that already exists, a **subfolder of that
   folder** keeps those reachable as well; a new top-level folder does not. Offer both, in that order, and
   let them choose knowingly. **Read the reachability boundary in the reference before you word
   this** — which neighbouring folders a flow can send from is the reference's to state, and it is
   exactly what makes the subfolder answer work, so do not paraphrase it from memory. If they still
   choose a bare new folder, that is theirs to choose: say that its send steps will carry only
   mailings created there from nothing, and carry that into the hand-over as a named shortfall.
4. **If nothing in this session creates a folder**, that branch ends there. Say plainly that you
   cannot create a folder, that this is a limitation on your side, and stop. Do **not** pick a
   folder that nobody named, do not fall back to one you saw on another flow, and **do not hand the
   user the job of making one by hand** — a step performed by hand around a missing capability is
   how the gap stops looking like a defect.

Either way this goes in the hand-over as what it is: with a prepared folder, nothing to say; with a
new folder, a named shortfall — ranked by whether sending was the user's headline requirement, which
it usually is.

## The brand: asked, never derived

The brand is settled at creation and **cannot be changed afterwards** — a brand you got wrong is a
flow that has to be created again. So **it is asked, every time, and it is asked of them.**

**Do not derive it.** Not from the folder they chose, not from a mailing they named, not from
anything else on a row you happen to hold. A derived brand is a guess at a permanent, unrepairable
decision — and the premise it rests on is false anyway: a folder need not narrow the brand at all. It
can be open to every brand, tied to none, or name several. **What a folder's brand column can hold,
and which column it is, is the reference's folder document to state** — read it there, and read it
for the check below, not to save yourself the question.

**Ask it in the same questions section as the folder** (step 3), with the brand catalogue already
read in the research pass, so the question can offer names instead of the word *brand*:

- **Ask about the thing, not the term.** "Which of your shops/sites is this flow for?" with those
  names — never a system name, never an id (step 2), and not the bare word *brand* if their request
  never used it. They may not know what a brand is; they do know their shop, their site, their
  product line **by name**, and the listing prints a human name beside the ids for exactly that
  reason. The catalogue is short enough to read whole (the `entities` domain says so on the brand
  entity), so there is no excuse for asking this one blind.
- **Say it is permanent in the same breath.** "This one can't be changed afterwards — a different
  brand would mean building the flow again." Said afterwards it is no longer a choice they could
  have made, it is a repair.
- **Never break the tie on how a name looks.** A brand that reads like a default, a test brand, the
  first row, the only active one — none of that is evidence. It is memory dressed as a fact, and the
  price of being wrong is the whole flow.

**If the answer does not come** — they skip it, or say "whatever the usual one is" — **ask again**,
once, with the shortest recognisable list. Do not fill it from the folder, and do not pick one to keep
moving. If they still cannot choose, **stop and report it** as the one thing blocking the create: a
decision you cannot make for them and they cannot undo.

## Before you create: does the folder permit the brand?

Their answers are in, nothing is created yet: **this is the one moment the two can be checked against
each other.** After the create the pairing is fixed for the flow's life, and the failure surfaces
somewhere else entirely.

Read the chosen folder's row and check it permits the chosen brand. **The column that carries a
folder's brands, and what each of its values means, is the reference's folder document to state** —
read it there and judge from what it says, because the values are not all lists of brands and the one
that permits everything does not look like a brand name.

- **It permits the brand** → create.
- **It does not** → that is a **question**, not a guess and not a repair. Put the conflict to them
  plainly — this folder and this brand do not go together — and let them change one of the two.
  Never silently switch the brand to one the folder allows, and never switch the folder to one that
  allows the brand: both are permanent decisions, and you would be taking whichever one they cared
  about more.
- **You could not check** — the row does not resolve, or the reference does not print what its value
  means → say so and stop before the create. An unverified pairing reported honestly costs a
  question; created, it costs the flow.

## The name, and why a repeat is safe

**The name is required and it is the user's.** Do not default it, do not compose one from the
request, do not append a date to make it unique.

It is also what makes the call safe to repeat: a name already used in this project is **refused**
rather than duplicated, so a create you are unsure about does not leave two flows behind. That
property only holds while the name is a real one the user chose — so a name is not a detail to fill
in for them, and it is worth naming back to them at hand-over.

## Starting from a preset

A preset is a **prepared graph**, and that is all of it: **it fills no entities**. A flow created
from one has blocks that are still empty of the entry event or schedule, the conditions' filters and
the steps' mailings — so it **cannot pass validation as created**, and everything from step 1(c)
onward applies to it exactly as it would to a flow you had built block by block.

**The reference deliberately does not describe what any preset contains** — the flow a preset
produced is the only authority on that, so a copy of its innards could go stale without anything
saying so. So you cannot choose a preset by matching its contents, and you must not choose one from
what its **name** suggests either: that is memory dressed as a fact, and a preset named after a
marketing mechanic is still a bare graph. Where the mechanic itself is documented, it is documented
in the wiki's mechanics sub-folder and no preset substitutes for it (`references/mechanics.md`).

What is left is what actually decides it. Take the set of presets that exist **from the live tool
schema**, not from here and not from memory. Unless the user described something a preset is plainly
*for*, create the empty one and build the graph yourself — that is the cheaper default, because
whatever a preset gives you, you still have to read back and fill in. If you do use one, **the
read-back at step 1(c) is how you learn what it built**, and everything from there on applies to
those blocks exactly as to blocks you created yourself.

## Verify the create like any other write

A create is a write, so CRITICAL 4 applies to it: **read the new flow back and check it landed
where you meant.** Confirm the folder and the brand are the ones you resolved, and the name is the
one the user gave. This is the only moment where the folder is cheap to check — the next chance is
the send step, and by then it is not a check but a diagnosis.

Then go on to step 1(c) and read the flow's structure: created from a preset it is **not empty**,
and a design made without looking at what is already there can be refused by a block you never saw.

## When a create is refused

**A refusal applied nothing** — no flow exists, so there is nothing to clean up and nothing to
report as half-built.

| The refusal | What to do |
|---|---|
| The **name is already in use** | Not a failure to work around. Ask whether they meant the flow that already has that name — and if not, ask for another name. Never make the name unique yourself. |
| It names the **folder** | The id you passed did not resolve. Go back to the listing and re-resolve from the name the user gave. Never substitute one from another flow, whatever the message suggests. |
| It names the **brand** | Same, and check first that you passed the id the reference asks for rather than the entity's other one. |
| **Permission** to create is denied | Report it plainly as a permission you do not have, naming the project. Do not retry, and do not build into some other flow instead. |
| Anything opaque, or no answer at all | Report it as a tool failure, naming the call and the message. **Do not retry blind more than once**, and before you do, check whether the flow now exists — a repeat under the same name is refused, which is what makes that check cheap. |
