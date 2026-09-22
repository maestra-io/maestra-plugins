# Delegating a filter to the filter-building skill

Read this **before your first delegation** in a session. It is the wording and the checks; the rules
behind it are in `SKILL.md` → `## Filters and entity scope`, and the flow's entity scope set is the
wiki's to state. Nothing here overrides either.

One delegation per filter. Never two filters in one sub-agent.

- [Entity scope — where the set comes from](#entity-scope--where-the-set-comes-from)
- [Before you delegate](#before-you-delegate)
- [Launching the sub-agent](#launching-the-sub-agent--settle-this-before-you-send-anything)
- [The message](#the-message)
- [The answer is a return value, not a conversation](#the-answer-is-a-return-value-not-a-conversation)
- [What to check in the answer](#what-to-check-in-the-answer-before-you-write-anything)
- [Writing it](#writing-it)
- [Verifying it after the write](#verifying-it-after-the-write)

## Entity scope — where the set comes from

**You cannot work the flow's scope set out from a block, and no read returns it.** The set is
**decided by the flow's start block and is the same set at every block in the flow** — whatever branch
or output it sits on, however deep — so it is one lookup for the whole flow, not one per block. The
only route to it is the reference: the `flows` domain's write-path sub-folder, keyed on this flow's
**start event**. Never infer a scope from another block, from the filter, or from what the
request sounds like. Check that what the user asked for is expressible in that set **before** you ask
for a filter — and if it is not, stop and report that condition rather than substituting a scope,
asking for a filter on a different root, or improvising something adjacent (`SKILL.md` →
`## Filters and entity scope`).

**Nothing cross-checks the two afterwards.** Omitting the scope on a write does not fail — a default
is assumed, and it will not be the one you meant — and a filter that does not match its scope is
accepted without complaint. So the pair is written together, in one call, or it is wrong silently.

## Before you delegate

You need three things in hand, and none of them is a filter's internals:

1. **The server** you are building the flow on — name it, not just the project. The filter tools and
   the flow tools live together per project, so naming the server is what makes the sub-agent work on
   the same project as the flow.
2. **The root entity** for the scope you already chose, in the **filters** vocabulary — as the
   reference gives it. The two sides do not always use the same word for the same thing, so a scope
   name is not a root name; take the translation from the wiki, never by echoing one side into the
   other.
3. **The request in business terms** — the audience as the marketer described it (step 3). Do not
   resolve any of the things it names; that is the sub-agent's job and it is better equipped for it.

## Launching the sub-agent — settle this before you send anything

**The message is only half of the delegation. The sub-agent has to be running the filter-building
skill.** A sub-agent is launched by agent *type*, and **no agent type corresponds to a skill** — so a
sub-agent handed only the message below runs as an ordinary agent. It has the project's filter tools
in its own list, so it will improvise a filter and hand back a payload of **exactly the shape you
asked for** — a plausible filter with the wrong provenance, and nothing about the answer's shape
gives it away. Every other guard in this skill fails loudly; this one fails silently. **The only
route is that the receiving sub-agent invokes the skill itself, because you told it to.** So:

1. **Find the filter-building skill in your own skill listing and use the name printed there.** It
   is the skill whose job is building a CDP filter — a selection of customers, products or actions —
   from a request in words. Do not use a name remembered from anywhere, this file included: the
   listing wins, and the skill may be renamed or re-homed. **If no such skill is in the listing,
   stop** — that is the missing-capability branch in `references/troubleshooting.md` → *Filters and
   delegation*, and having the filter *tools* is not a substitute for it.
2. **Make loading it clause zero of the message** — one sentence instructing the sub-agent to use
   that skill, by the name from the listing, for this task. This is *the* mechanism, not a fallback:
   there is nothing else that puts the skill in front of the receiving agent. Treat that sentence as
   load-bearing exactly like the rest of the message.
3. **Make the answer evidence it** — the provenance clause below — and check it before you write.
   You cannot verify provenance from the payload, only from what the answer says about how it was
   produced.

## The message

Clause zero is the "use the skill" sentence from
`## Launching the sub-agent — settle this before you send anything`.
After it, keep every clause. Each one is load-bearing: without the "store it programmatically"
framing you get a link and no payload, without the "verbatim" clause you get something retyped, and
without the provenance clause you cannot tell a filter the skill built from one an agent improvised.

> Build a filter on the project served by MCP server `<server>` that selects: **\<the request in
> plain words\>**. The filter must be rooted on **\<root entity\>** — a filter on any other root is
> unusable for me, so if that root cannot express the request, say so instead of switching roots.
>
> **Return the filter payload itself, verbatim, exactly as your build step returned it, in a fenced
> code block** — I am going to store it programmatically in a marketing-flow block, so the machine
> payload is the deliverable, not the link. Include a link as well if you have one, but the payload
> is what I need. Do not reformat, re-indent, abbreviate or retype it, and do not hand me the
> readable draft in its place.
>
> **Also give me the query draft itself, by name** — the filter query text your build step compiled,
> in its own query language, in a second fenced code block. I need it in the *same* language a stored
> filter renders back into, because that is what I compare the stored filter against; a prose
> sentence cannot be compared with a rendering. So: the prose sentence **and** the query draft, not
> one instead of the other.
>
> Also tell me, in one line each: the root entity, the project and environment you built on, and any
> assumption you made.
>
> And tell me how the filter was produced: **which skill you followed**, **which of its reference
> documents you read** to choose the root and the predicates (give their ids as the reference prints
> them), **confirm the payload is the output of your build step — the assembled filter the platform
> confirmed — and not one you composed, patched or edited by hand**, and **state explicitly that you
> validated it with the root entity above passed to the validation itself** (a validation run without
> the root passed does not check the root at all, so "it validated" is not enough on its own).
>
> If your build step returned no payload, say so and stop — do not substitute a draft, an earlier
> filter, or one written by hand.

## The answer is a return value, not a conversation

**The delegation's answer is the value the sub-agent returns when it finishes.** Do not build the
delegation around a follow-up exchange: the reply path back to you can fail **one-directionally** —
your messages arrive, its answers do not, and nothing on your side says so. A sub-agent that has
already finished may also be gone. So every *"ask once more"* below means a **fresh delegation**: a
new sub-agent, the whole message again including clause zero, plus one sentence naming what was
missing last time. It never means messaging a sub-agent that is already running, and never means
messaging one that has not answered.

**A delegation that produced no answer is not a delegation that produced a bad one.** They look
alike from where you sit and they need opposite moves:

| What you are holding | What it tells you | What to do |
|---|---|---|
| An answer that fails a check below | The delegation worked and gave you something you cannot use | That row's move, including discarding the body where the row says discard |
| **No answer at all** — the launch reports the sub-agent unreachable, it returns nothing, or nothing comes back and you are waiting | **The channel failed. This says nothing about the filter** — the work may be finished and undeliverable | **Launch a fresh sub-agent with the same message.** Do not re-message the silent one: an answer that could not reach you once will not reach you by asking again |

**Budget: one fresh launch per condition on silence, then stop.** Two silences on the same condition
is a capability you cannot use in this session — and **what you report is a delegation you could not
get an answer out of**, in those words. **Never report, or imply, that the audience could not be
expressed or that the branch could not be built:** you have no evidence of either, and saying it
hands the user a smaller flow than was achievable on the strength of a broken channel. Rank it at
hand-over as a shortfall in your reach, name the block, and say what the flow does not do while that
condition is missing. Do not write the condition unfiltered to fill the hole — no filter means
*everyone*.

## What to check in the answer, before you write anything

| Check | If it fails |
|---|---|
| A filter payload is present, in a code block | Ask once more, restating why the payload is the deliverable. Still nothing: stop that condition and report it. Never reconstruct one. |
| The **query draft** is present too, in the language a stored filter renders back into | Ask once more, by name. Without it you have nothing to compare the stored filter against in *Verifying it after the write*, and a prose sentence is not a substitute. Still nothing: you may proceed, but the condition then needs their eyes — put it in *Actions* as an instruction in their words, asking them to check that condition does what they meant, not as a note about how far your own verification got (`references/hand-over.md`). |
| The answer **evidences its provenance**: it names the skill it followed, cites reference documents it read, and states the payload is the confirmed output of its build step | **Ask once more, for the provenance specifically**, before concluding anything — that skill's default answer shape carries neither the skill name nor the documents it read, so a first answer without them is as likely to be the template as improvisation. **If the second answer still does not evidence it, discard the body as unprovenanced**, however well-formed it is: an agent improvising with the same tools returns the same shape, so the payload itself can never settle this. Then re-launch onto the skill (`## Launching the sub-agent — settle this before you send anything`) and ask again — **once. One re-launch is the budget**, the same way one corrected re-send is the budget for a write (`SKILL.md` → step 5). Since asking again *is* a fresh launch (`## The answer is a return value, not a conversation`), that re-ask and that re-launch are one and the same act: **two delegations on this condition in total, not three.** If that answer does not evidence provenance either, **stop that condition and report it** as a capability you could not use: an agent type that does not load the skill returns the same shape every time, so a third attempt spends another sub-agent on the same answer. Never write an unprovenanced body, and do not substitute your own inspection of it for provenance. A vague "I built a filter" is a fail; so is a claim to have followed the skill with nothing it read to show for it. |
| The answer states it **validated with your root passed explicitly** | Ask once more for that statement. The root check only fires when the root is passed to the validation, so without the statement you do not know the root was checked at all — and then it is yours to corroborate: have the payload rendered and see that it is about the entity you asked for. Corroborate or discard; do not write it on the strength of a bare "it validated". |
| The root is the one you asked for | Discard it. Do not re-root it yourself and do not adjust the scope to match — the scope came from the graph, not from the filter. |
| The project and environment match the server the flow is on | Discard it and re-delegate naming the server. A wrong-project filter does not error; it silently describes a different audience. |
| It reports having built something, not having saved something | That skill saves nothing. If it claims to have saved or applied a filter, treat the answer as unreliable and report it. |
| Its stated assumptions are ones the user would accept | If an assumption is a business decision the marketer should make, take it back to the user rather than writing it. |

That skill's own procedure compiles the filter and checks its values against the project catalogue,
and it refuses a root that does not match the one you named **when the root was passed to the check
explicitly** — which is exactly why both provenance and the root statement matter: those checks come
with the skill and with how it was run, not with the tools. With them in hand the payload is already
platform-checked — **do not re-run that checking**, and do not treat their absence as something you
can work around.

## Writing it

The payload goes into the block's condition **as it stands**, together with the entity scope, in the
same call — never the body alone, and never the scope alone. Which field takes which, and the shape
around them, is the write-path sub-folder's to say. One condition block per call.

Keep the query draft the sub-agent reported, and its prose sentence. You need the draft in the next
step, and the sentence for the hand-over.

## Verifying it after the write

Read the block back, take the stored filter, and get it **rendered back into readable query form**,
then compare that rendering with the **query draft** the sub-agent reported building — the two are in
the same language, which is the whole point of having asked for the draft. Compare **meaning**:

- The rendering **normalises** — a condition can come back phrased differently, or inverted into an
  equivalent form, with nothing wrong. A textual diff of the two will raise false alarms; do not
  report one as a mismatch.
- A **genuine** mismatch is a difference in what the filter would select: a different attribute, a
  missing or extra condition, a negation that is not equivalent, a quantity or period other than the
  one the marketer stated, or anything the rendering says it could not read. Judge clause by clause —
  those are what this check is for.

**This check settles structure, and it cannot settle a value that names a thing.** Structure is what
it is good for: which conditions are present, what each is about, how they combine, whether a
negation survived, that nothing was dropped or added on the way to storage, and that a quantity or
period the marketer themselves stated came through. **Where a clause names something out of the
project's catalogue, the comparison is not available at all** — by design on both sides, not a defect
waiting to be fixed: the building side stores whatever the filters side minted for the name, which can
be a small number with no relation to it, and the rendering side prints that stored value where the
draft printed the name and never resolves it back. A *correct* filter therefore always looks like a
mismatch at that spot.

**So take that spot out of the comparison, rather than reading anything into it.** A value that looks
like a number, or otherwise unlike a name, is the ordinary result of a correct build: on that alone do
not discard the filter, do not re-send the block, do not ask for a rebuild, and do not report the
condition as mismatched. **Do not read it the other way either** — a number is no proof that a name
was resolved, since catalogue names can themselves be digits, dates or version-like strings, and
neither the rendering nor you can tell which of the two you are looking at. And **do not go looking
for another comparison** at this surface; there is none these tools support.

What you have instead, and it is enough to proceed on: the resolution itself was the build step's
work, asserted in the sub-agent's answer, and your field-by-field diff already confirms that what is
stored is byte-for-byte the payload it returned. So leave the value in place and record it, for
yourself, as **verified by field, not by meaning** — never as unverified, and never as verified by
meaning. **At hand-over it becomes one item in *Actions* and nothing more**: an instruction in their
own words, naming the condition and what to look at ("check the filter uses the right product lists —
Cart and Favourites"). None of the reasoning above travels with it (`references/hand-over.md` →
*What never goes in*).

To get the rendering, use the project's filter tooling — there is a read-only capability that turns a
stored filter back into readable text; find it in your tool list. If you cannot find one, ask a
sub-agent to render it and compare what it reports; do not read the stored payload by eye and call
that verified, and do not skip the step.

On a genuine mismatch: re-send that condition once, alone, then re-verify. If it still disagrees,
stop, and report which block and how the stored filter differs in meaning from what was asked for.
Do not describe that condition as built.
