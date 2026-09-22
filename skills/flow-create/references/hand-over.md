# Writing the hand-over

Read this when you reach step 8. The rules behind it — what "done" means and how to rank a
shortfall — are in `SKILL.md`.

- [The link](#the-link)
- [The three parts](#the-three-parts)
- [Reporting a stop under CRITICAL 6](#reporting-a-stop-under-critical-6)
- [What never goes in](#what-never-goes-in)
- [A filled example](#a-filled-example)

The reader is a marketer who has never seen the flow's internals. **Same meaning, fewer words** is
the whole editorial rule: every sentence that is neither a fact they need nor an action they can take
comes out.

## The link

Hand over a link to **the draft version you built** — the project's admin base URL, the flow's
scenario path, and the marker that names the version you built rather than whichever one the
platform would pick. **A link without an explicit version marker is not guaranteed to open the
version you built**, so it is not a hand-over on its own.

**The path shape is a platform value, so take it from the reference — never assemble one.** A URL
built from a pattern you have seen sends the user to a page that is not their flow, or to none.
**The `flows` domain has a document of its own for the address of a flow version** — the path, the
mode and the version markers, with what each one opens; navigate to it from the domain index, whose
term map lists it under the user's own words for a link (its id is `urls` in today's index — take the
id from the index, not from here). Read it before you build the address. If the reference does not
print it — a document can go missing again — treat it as the
documentation gap it is (`SKILL.md` → `## CRITICAL` 2): say you cannot produce a link, name the flow
and the version number you built so they can open it, and carry the gap into the shortfall list as a
limitation on your side.

**Check which kind of marker your link carries — then say almost nothing about it.** The reference
distinguishes a marker that selects a version **by state** from one that names a version **by
identity**, and the difference is worth one clause of text, never a paragraph:

- **It names the version by identity** — say nothing at all. The link works; how it is built is not
  something the user can act on.
- **It selects by state** — one clause: the link opens the draft *now*. That much is actionable,
  because re-opened after the flow is launched the same address can show the running version with
  nothing saying it switched.

Put the version number in the same line as the link, and stop there.

You cannot derive the admin base URL from any tool. **Ask for it in the step-3 batch**, with the
rest of your questions — never at hand-over, where a question is a broken promise (or reuse one
the user has already given you in this session).

## The three parts

Exactly three, in this order, and nothing else.

### 1. What was built

**Reuse the `maestra:flow-summary` skill's own output format** — its three sections, in the language the
user is working in, dash bullets, never a wall of text. Take the section names and the rules from that
skill rather than from here; if it is not available in your session, keep to the same three parts (what
starts the flow, what it does step by step, what it is for). Keep it compact, and expand only if the
user asks for more.

Refer to a block by its name in quotes or by its role ("the 3-day wait", "the email step"). No block
ids, no type tags, no row versions, no field or value names.

### 2. Actions

**A checklist, and every item something the user can do.** Two kinds belong here and nothing else:

- what they must **check or fill themselves**, and
- what they must **tell you** so that you can do it — the name of a mailing to attach, which of two
  candidates they meant, an audience you could not build without their words.

Rules for the items:

- **Each item is an instruction, not a statement.** *"Check that the filters use the right product
  lists — Cart and Favourites"* is an action. The same thing prefaced with an account of how the
  platform stores those lists is a statement with an action buried in it: delete the preface.
- **Where an item is a shortfall, its consequence goes in the same line**, in the user's terms —
  *"until a mailing is chosen the flow will not run"*, or *"this needs a small follow-up from you and
  the rest is built"*. `SKILL.md` says the two kinds are not comparable, so **put the headline ones
  first**: a severe item listed beside three routine ones reads as routine.
- **What did not land is stated as a limitation on your side, not as a chore you are handing over** —
  and say what the flow does *instead* right now, so they can judge the risk ("the condition passes
  everyone").
- **Choose the checklist form the client supports** — a markdown file, an artifact, a checklist in the
  message. Any of them is right; picking the one that suits where you are running is yours to do, and
  nothing here prescribes it.
- **If there is nothing to do, say so in one line.** Do not pad the section.

### 3. Suggestions

**How the flow could go further — as offers, and only as offers.** *"If you want, I can: add an A/B
test between the branch condition and the send; …"*. Never half statement and half offer: *"I didn't
do an A/B test — you didn't ask. Its place would be …"* is a note about your own reasoning, and there
is nothing in it to act on. Drop the note, keep the offer. If you have nothing to offer, omit the
section.

## Reporting a stop under CRITICAL 6

A run that stopped short is handed over in the same three parts, not as an apology. **Say plainly
what is not built and what the flow will therefore not do**, in business terms, in *what was built*;
put the choice in **Actions** as something they decide, never as work they perform.

Three things belong in it and nowhere else:

- **The objection verbatim**, where there was one. This is the same exception the tool-behaviour
  bullet below carries for an incomplete validation: a message the procedure tells you to pass on
  goes through unedited, platform vocabulary included.
- **What you tried**, in one line — enough that nobody repeats it, not a log of calls.
- **The choices you can see**, as choices. "This needs a value no write of mine can set — do you
  want it set another way, or the flow handed over without it?" is an Action. "Please open the editor
  and fill it in" is not: that is handing them the job, which CRITICAL 6 does not license
  (`SKILL.md` step 1b, step 2).

**Do not report the budget, the count, or the rule's name.** That it stopped at six calls is our
business; that the branch is unfinished and why is theirs.

## What never goes in

Cut it, whatever else is true of it, if the user cannot act on it:

- **System names, ids, type tags, row versions, field names, discriminators** — anything from the
  platform's own vocabulary.
- **Tool behaviour.** How a write answered, that a call reported nothing applied and applied
  everything, that a listing had to be re-queried. If it is worth reporting it is worth reporting **to
  us, not to them** — where the session has a feedback capability connected, that is where it goes;
  otherwise it goes nowhere.
  > **One exception: a message the procedure tells you to pass on verbatim.** Where step 7 could not
  > complete a validation, CRITICAL 5 requires saying plainly that the flow is unvalidated **and
  > giving the message as it came** — platform vocabulary included. That outranks this bullet: never
  > tidy such a message out of the hand-over, and never paraphrase it into something acceptable.
- **A platform quirk with no user-side move.** A value the read path regenerates and nothing can
  confirm (`SKILL.md` step 6) is the standing example: naming it buys them nothing.
- **Explanations of how the link is built**, of why a rule is what it is, or of a constraint that no
  longer bears on a decision. Folder reachability is the case to watch: it belongs in the **question**,
  before the choice is made (`references/questions.md`) — after the fact it is an essay nobody reads.
- **Your own reasoning about what you did not do**, unless it turns into an offer in *Suggestions*.

## A filled example

One shape that satisfies the three parts. The link stands in as `‹link›` here **only** because this
file must not carry a path shape — build the real one from `## The link`. Write yours in the language
the user is working in, with the section names in that language; this one is English. The first part
is shortened to a line per section; the real one follows the `maestra:flow-summary` format.

> Draft of the "Abandoned cart reminder" scenario, version 3: ‹link›
>
> **Trigger** — the customer left a cart behind.
> **Flow logic** — wait 3 hours → check "still hasn't bought" → email "Come back to your cart";
> everyone else leaves the flow. At most once a week per customer.
> **Goal** — bring the customer back to an unfinished order.
>
> **What to do**
> - Name the mailing for the send step: I couldn't pick one, and without it the flow won't run.
> - Activate the "Come back to your cart" mailing in the interface — until you do, the flow prepares
>   the message and sends nothing, and there is no way for me to activate it.
> - Check that the filters use the right product lists — Cart and Favourites.
> - Tell me whether an order in any status counts as a purchase, or only a paid one: for now the
>   condition passes everyone.
>
> **If you want, I can**
> - add an A/B test between the condition and the send;
> - add an SMS to anyone who hasn't opened the email within a day.

Note what the example does **not** do: no ids, no field names, no explanation of the link, no account
of how the tools behaved, no paragraph about folders. The blocking item comes first and says what
happens without it, and every line under *What to do* starts with something to do.

# References

- `SKILL.md` → CRITICAL 6 — when a run stops short, and what the exit is

- `SKILL.md` → step 8 — the rule this file serves
- `SKILL.md`, top — the two kinds of shortfall, and why the ranking carries the message
- `references/questions.md` — what belongs in the question rather than in the hand-over
- `maestra:flow-summary` → `## Output format` — the format part 1 reuses
