# If something goes wrong

One row per situation you can actually hit. Read it when something does. The rules these rows
apply are in `SKILL.md`; nothing here overrides it, and nothing here is a substitute for the
reference — where a row says "the reference", go and read it.

- [When a documented recovery outranks this file](#when-a-documented-recovery-outranks-this-file)
- [Getting started: session, wiki, draft](#getting-started-session-wiki-draft)
- [Writes](#writes)
- [Entities](#entities)
- [Reading back](#reading-back)
- [Validation](#validation)
- [Filters and delegation](#filters-and-delegation)
- [Out of scope requests](#out-of-scope-requests)

## When a documented recovery outranks this file

`SKILL.md` step 5 states the precedence: where the symptom matches one in the `flows` domain's
known-issues sub-folder, the recovery written there **replaces the per-body retry budget and every
generic ladder** — here and in `SKILL.md` — for as long as it runs, and it decides the order of what
you try next. **It does not decide when the session stops.** Four limits keep it from swallowing
everything else. Read them before you follow a recovery.

- **A recovery is spent once you have run its steps.** Matching the same one again is not running it,
  it is improvising, so the budget governs from there — in step 6 that means going on to route 2
  rather than round the same recovery again.
- **The precedence is over the per-body budget only, never over the session budget.** CRITICAL 6
  counts every write call that did not move you forward, a recovery's calls included, and nothing
  suspends it. A recovery cannot license an unbounded run of calls; where its own steps outlast the
  session budget, the budget stops you and the rest is reported, not attempted.
- **A recovery whose step is an unbounded search is not run at all.** Where a documented recovery
  says to harvest a value by paging a catalogue, or by reading flow after flow until one carries it,
  **that step is not taken**: the value is declared unfillable and ranked in the hand-over instead
  (`SKILL.md` step 2). The rest of that recovery still applies where it does not depend on the sweep.
- **The precedence never runs over a `## CRITICAL` rule.** Where a
  recovery's wording would have you break one, the rule stands and you meet the recovery's intent the
  way the rule prescribes: a recovery that says to re-send a block's whole body is satisfied by
  reading the block to *learn* its values and then **building** the body, never by echoing what you
  read (CRITICAL 3) — **with CRITICAL 3's whole-set exception intact**, so a whole-set field you must
  keep goes back **unchanged**, because rebuilding that one is exactly what would lose it.

## Getting started: session, wiki, draft

| Situation | What to do |
|---|---|
| The project's flow tools aren't connected in this session | Stop and tell the user to connect the project's flow MCP first. Do not attempt to build anything. |
| The `wiki` tool answers nothing for a domain, or you cannot see one in the session | **A schema is not the check — make the call, naming the domain** (`SKILL.md` → `## Where to look`). If there is genuinely no `wiki` tool at all you have no reference: **stop and report it as a missing capability**, naming the tools you do have. **Do not proceed from memory of field names** — that is fabrication — and do not go looking for the documents somewhere else. |
| **No flow-creating tool exists in this session**, and you were not given a draft | Stop and report a **missing capability** in plain words, naming the tools you do have (step 1b). Do not substitute another tool, do not build into an unrelated flow, and do not ask the user to make one by hand. |
| `flows_create` errors, or the draft it should return never arrives | Stop and report it as a tool failure, naming the call and the error. Before any retry, check whether the flow now exists — a repeat under the same name is refused, which is what makes that check cheap (`references/creation.md`). Do not build into a flow you were not given. |
| The user wants a flow that **does not exist yet** | Create it — that is the normal path (step 1b). Ask your batch **first**: the folder, the brand and the name are settled at creation and cannot be written later. `references/creation.md` before your first create. |
| The user names **no folder** with the mailings the flow will send, and **nothing in this session creates a folder** | **That branch ends there.** Say plainly that you cannot create a folder and that this is a limitation on your side. **Do not pick a folder nobody named**, do not reuse one from another flow, and do not ask the user to make one in the UI (`references/creation.md` → *Asking about the folder*, step 1b). |
| A create is refused because the **name is already in use** | Nothing was created, so there is nothing to clean up. Ask whether they meant the flow that already has that name; if not, ask for a different name. **Never make the name unique yourself.** |
| A create is refused naming the **folder** or the **brand** | The id did not resolve. Go back to the listing and re-resolve it from the name the user gave, and check you passed the id the reference asks for rather than the entity's other one (step 2). **Never take one from another flow, whatever the message suggests.** |
| A create is refused for **permission** | Report it plainly as a permission you do not have, naming the project. Do not retry, and do not build into some other flow instead. |

## Writes

| Situation | What to do |
|---|---|
| A write is refused as not editable for this version | Only some version statuses accept writes; **which ones is the write-path sub-folder's to say** — read it rather than assuming. Get the version list with statuses, use one that accepts writes, and re-read the flow for a current row version first. If none does, stop and report it. |
| A write is refused as a version conflict | Nothing was applied, **and the token you hold is stale**. Re-read the flow for a current row version, then re-send the same batch. |
| A write is refused for any other reason | **First, is it a refusal at all?** A batch that comes back carrying validation entries was *not* refused — it applied, and those entries are the progress meter (`SKILL.md` step 4). A refusal applied nothing and your row version is still current. **Before you act on the message, match it in the known-issues sub-folder** — a refusal that names nothing, and a refusal naming something you never sent, are both documented symptoms, and the recovery there **replaces this row** and decides when to stop (`SKILL.md` step 5); a message that names a thing you did not send is not a cause you can fix by editing that thing out. Otherwise: fix the cause named in the error and re-send the corrected batch **once**. Never re-send an unchanged body, and never loop on an opaque error — stop and report which block and what you tried. |
| A validation entry or a refusal names **something no write of yours can send** | **The body is not the cause, and no re-send closes it.** Check the write-path sub-folder once, for that thing, by name; if it is on no body you can build and no operation sets it, say which it is, say that no write reaches it, stop that block and rank it (`SKILL.md` CRITICAL 6). **Do not re-send the body in any shape, do not delete and recreate the block, and do not re-delegate to hear the same answer again.** |
| You are about to **delete a block** | **Read it at full detail first and keep that read** — a delete has no undo, and that read is the only copy and the source for any recreate (`SKILL.md` step 5). This binds a delete the design asked for as much as a repair delete; only the repair delete counts against the session budget. A **second** delete of the same block, or a delete of a block you never read, is a guess: stop (`SKILL.md` CRITICAL 6). |
| **A write never answered** — a timeout, a dropped connection, a cancelled call | **This is not a refusal, and you do not know that nothing was applied.** **Read the flow back before doing anything else**: the batch may have applied in full. A blind retry duplicates what it created and applies what it changed twice. Decide from the read whether to retry. |

## Entities

| Situation | What to do |
|---|---|
| `entities_list` isn't available (it ships behind its own toggle) | Say so plainly: with no listing there is nothing that turns a name into an id, so those entities cannot be resolved and the fields that need them will be left unset — say what the flow will not do as a result. **Do not ask the user for ids**, never invent one, and never pass a name where an id is wanted. |
| An entity resolves to nothing, or to several candidates | Ask for the **name** again, or for which candidate they meant (step 3). Never pick for them, never guess an id, and never ask them to supply one. |
| The reference says no listing covers the kind of entity you need | **First check the listing's own schema** — its coverage moves and the reference can lag it; if the kind is in the live schema, call it (`SKILL.md` → `## Where to look` — the live schema wins). If it genuinely is not there, tell the user which entity cannot be resolved right now, name what is therefore left unset and what the flow will not do because of it, and **stop — do not look for another way in** (step 2). Do not ask for an id, do not borrow a value from another flow, do not write a placeholder, **and do not sweep** — paging a catalogue or reading flow after flow because one might carry the value is not a resolution route, whatever a recovery suggests as a place to harvest one from. Rank it in the hand-over. |
| You need a field or a value the wiki doesn't document | **Report a documentation gap** — the field, the document that should print it, what you meant to express — and **stop that one write**, then build the rest (CRITICAL 2). Never guess it, never ask the user for a platform value, never borrow one from a similar field elsewhere. Rank it in the hand-over. |

## Reading back

| Situation | What to do |
|---|---|
| A read-back carries keys you never sent | **Normal, not a failure.** A read-back is a superset of the body you sent; judge only the fields you sent (step 6). Never report a correct block as broken over an extra key. |
| A read-back disagrees with what you sent | **Match the symptom before you repair anything.** Whether it came back **unchanged**, or **different** from what you sent, or refuses to change at all, these are documented symptoms with recoveries of their own: go to the `flows` domain's known-issues sub-folder, match what you observed, and **follow that recovery to its own end — it replaces the repair routes and decides when to stop** (`SKILL.md` step 5). Only if nothing there matches: **a block that reads back wrong is recoverable, not a write-off** — run the two ordered routes in `references/graph-and-verify.md` → *Repairing a block that reads back wrong*, in that order and including its instruction to **match the symptom again before route 2**, and stop only after both. Then report which block and which field. Do not describe the block as built until a read-back agrees. |
| **Something the block held before is gone, and your body never mentioned it** | **First: could a write of yours have sent that member at all?** Where the reference puts it on no body you can build, it is the platform's projection of the block and not its state — nothing was lost, nothing is restored, and sending it back is the write the reference forbids (`SKILL.md` CRITICAL 4(b), CRITICAL 6). Where it **is** writable, treat it as a **failed write**, not noise (`SKILL.md` CRITICAL 4(b), step 6.5): restore it from your pre-write read **unchanged** — that is CRITICAL 3's whole-set exception — inside a body that also carries everything else the block needs, then verify again from step 6.1. **Do not** re-send the destroying body and hope. **And if a `flows_validate` fell between your pre-write read and this one, you have no baseline** — take a fresh read and do not diff across the call (`SKILL.md` step 7). |
| The value is gone and you have **no pre-write read** of the block | You cannot verify that write and you cannot restore from the flow. Say so plainly: name what is missing, name what the flow does **instead** right now (a lost audience filter means *everyone*), and rank it in the hand-over. Then rebuild it only the way it was built the first time — ask the user what the audience should be and delegate again (`references/filter-delegation.md`). **Never reconstruct it from what you infer it must have been**, and never report the block as verified. |
| A read-back doesn't contain a block you wrote | It is **unverified**, not fine. Re-read it scoped to that block alone (step 6); if you still cannot read it, report it as unverified. |

## Validation

| Situation | What to do |
|---|---|
| **The user asks for another change *after* a validation that passed** | Start again from step 1(c): re-read the flow, its versions with their statuses, and its current row version, or the write is refused as a conflict and applies nothing. **Then take a fresh full-detail read of every block you are about to write** — the validate re-shaped them, so any read you kept from before it is no baseline for CRITICAL 4(b) (`SKILL.md` step 7). **Validating does not, by itself, put the version out of reach** — which statuses accept writes is the write-path sub-folder's to state, so read it rather than assuming. If a write *is* refused as not editable, say plainly that the change could not be applied to this version and stop. If it goes through, **verify it in step 6 and validate again** — the edit reopened validation, so this change is checked like everything before it, and the summary must not rest on the earlier pass. |
| Validation reports something you already knew you could not author | **Expected.** Do not retry and do not invent it away. Put it in the hand-over as what the flow still needs (step 7). |
| A validation problem doesn't say which block it is about | Match it yourself from what you wrote. If more than one block could be the subject, report it verbatim, name the candidates, and leave it to the user (step 7). |
| Any of the validation rows below, in more detail | `references/validation.md` — the call's failure modes, the three kinds, and the after-validation path. **Calling it again on a version that is *still* passing is never the recovery**; after a fix, or after any later write, validating again is the step (kind 2 there). |
| The validate call itself is refused | Do not loop on it. Read the flow back once and check your writes are as you left them; then report the message verbatim as a validation you could not complete, naming the blocks it could concern. Do not start rewriting blocks that verified. |
| Validation says your row version is stale and hands back **the token you already hold** | The token has not moved, so there is nothing to re-read and re-reading changes nothing. Treat it as a failed validation, not as a conflict: read the rest of the message for the real problems, and do not loop. |
| Validation fails with a message naming nothing at all | Validation did not run, so it is telling you nothing about the flow — asking again changes nothing. **Go to the `flows` domain's known-issues sub-folder, match the symptom there, and follow the recovery it gives** (`SKILL.md` → `## Where to look`): a blind validation has documented causes with a stated order to check them in, and the cheap one is not the one you would guess from your own writes. Work through that order before you suspect anything of your own, and **do not delete a block on suspicion** — a deletion made on a guess costs you a block that was fine and leaves the real cause in place. If the sub-folder's causes are all ruled out, report the flow as unvalidated, naming what you verified in step 6 and what you checked here. |

## Filters and delegation

| Situation | What to do |
|---|---|
| **No filter-building tools on this server**, or the filters skill is not available | The two toolsets are gated independently, so this can happen on a server whose flow tools work. Stop the conditions that need a filter and report it as a **missing capability**. Never compose a body yourself, and never leave a condition unfiltered and call it built — no filter means *everyone*. |
| More than one project's server is connected | Ask the user which project **before the research pass** — not in the step-3 batch, so it is settled before you survey, delegate or write (`references/questions.md` → *Before the pass: which project, in their words*). A filter built on the wrong project does not error; it describes a different audience — and a survey run against the wrong one does not error either. |
| The sub-agent reports a different project or environment than the flow's server | **Discard that filter** and re-delegate, naming the server explicitly. Do not "fix" it and do not write it. |
| The answer looks right but does not evidence **which skill built it** | You cannot settle this from the payload — an agent with the same tools returns the same shape. **Ask once more for the provenance specifically — as a fresh delegation, never a message to a sub-agent already launched** (`references/filter-delegation.md` → *The answer is a return value, not a conversation*): the answer template that skill follows does not carry it by default, so a first answer without it is not yet proof of improvisation. **How many delegations that leaves you is `references/filter-delegation.md` → *What to check in the answer, before you write anything* to state — take the budget from there, not from this row**, because asking again and re-launching are the same act and counting them twice buys a delegation you do not have. Once it is spent and the body is still unprovenanced, stop that condition and report it. Do not write it, and do not check the body yourself in place of provenance. |
| The filter-building skill is not in your skill listing under any name | This is the missing-capability branch, even if the filter tools are present. Stop the conditions that need a filter and report it. **Do not build one in a sub-agent that has the tools but not the skill** — that is the silent failure this rule exists for. |
| The sub-agent answers with a link and no filter body | Delegate once more — a fresh sub-agent, the whole message again — restating that the payload is the deliverable and why (`references/filter-delegation.md`). If a body still does not come, stop and report that condition. Never reconstruct one from the link, from the readable draft, or from memory. |
| **The sub-agent never answers** — the launch reports it unreachable, it returns nothing, or nothing comes back | **The channel failed, not the filter**, and the work may be finished and undeliverable — so this tells you nothing about whether the audience can be expressed. **Launch a fresh sub-agent with the same message**; never re-message the silent one, and never expect a follow-up exchange with a sub-agent — the answer is its return value (`references/filter-delegation.md` → *The answer is a return value, not a conversation*). One fresh launch is the budget: after a second silence, stop that condition and report **a delegation you could not get an answer out of**. **Do not report the branch as unbuildable** — that hands the user a smaller flow than was achievable, over a broken channel. |
| The reference says the flow's scope set cannot express what was asked | **Stop that condition and report it** (`SKILL.md` → `## Filters and entity scope`). Do not substitute a scope, do not ask for a filter on another root, do not approximate the audience. |
| The rendered read-back of a filter reads differently from what the sub-agent reported | The rendering **normalises** — different wording is expected. Judge the meaning; only a difference in meaning is a failure (step 6). |
| The rendering's value for something the clause **names** does not read like the name in the draft | **Not a failure, not a defect, and not yours to fix — the comparison does not exist there.** The building side stores what the filters side minted for that name, the rendering side prints that and never resolves it back, so a *correct* filter always looks wrong at that spot. Judge the clause around it; leave the value alone; record it for yourself as **verified by field, not by meaning**, and at hand-over turn it into one *Actions* item in their words — check the condition uses the thing they meant — with none of the reasoning attached (`references/filter-delegation.md` → *Verifying it after the write*, `references/hand-over.md`). Do not discard the filter, re-send the block or ask for a rebuild — and do not read a numeric-looking value as either proof or suspicion: catalogue names can look numeric too, which is why this spot cannot carry the check. |

## Out of scope requests

| Situation | What to do |
|---|---|
| The request names a marketing mechanic instead of describing a flow | Check the wiki's mechanics sub-folder before designing anything (`references/mechanics.md`). If one matches, it is the design, and what it says must be settled first is asked in the step-3 batch, before your first write. If none matches, say so plainly, ask them to describe the flow they want, and build only what they describe. Never improvise a mechanic that folder does not carry. |
| The user asks you to launch / test / stop / delete the flow | Say what you can't do: launching, stopping and deleting are outside this skill and no tool of yours may be used for them. Hand over the draft instead. |
