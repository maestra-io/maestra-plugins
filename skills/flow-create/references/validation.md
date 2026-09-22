# Validating the flow version

**Read this when you reach `SKILL.md` step 7** — the last step before hand-over, hours into a
session. `SKILL.md` keeps the ordering rule and the ban on offering a pass as evidence, because both
constrain writes made long before this step; everything below is what the step itself needs. The
rules are in `SKILL.md`; nothing here overrides it, and nothing here suspends CRITICAL 6.

- [The call's own failure modes](#the-calls-own-failure-modes)
- [Sorting what it reports](#sorting-what-it-reports)
- [A change asked for after a validation that passed](#a-change-asked-for-after-a-validation-that-passed)

## The call's own failure modes

**These are not the flow's problems, and none of them is a licence to loop.** A refusal; an answer
that **names nothing at all** (validation did not run, so it says nothing about your flow); a
stale-token claim handing back the token you already hold. Each has a row in
`references/troubleshooting.md` → *Validation*. **Do not guess which of your blocks caused one** —
and in particular do not delete a block on suspicion: a deletion made on a guess costs you a block
that was fine and leaves the real cause in place (`SKILL.md` step 5, *A delete takes that same read
first*).

**Calling it again is not a recovery — and the call is not read-only.** A version that is **still**
passing answers the same way without validating anything, so a second call *on such a version* tells
you nothing a first did not, and a run of them is the loop `SKILL.md` → CRITICAL 6 counts. **That is
the only case.** An ordinary edit to a block reopens validation, so after any further write — one
made long after a pass included — validating again is the step and not a repeat of a no-op; likewise
on a version that came back with **problems** (*Sorting what it reports*, kind 2). **And do not
generalise the no-op into "the call has no effects."** Every call re-shapes the version's blocks
before it validates anything, pass or fail, so it invalidates every pre-write read you are
holding (`SKILL.md` step 7).

## Sorting what it reports

Three kinds, and the difference decides whether you write anything at all.

1. **Expected gaps** — what you already knew you could not author: an id no tool reaches, a
   condition the flow's scope set cannot express. **Do not retry and do not invent them away.** Carry
   them to step 8 as what the flow still needs.
2. **Problems that are yours to fix** — a malformed block, a missing required member, a dead end you
   did not intend, an unconnected block. Fix it, verify the fix in step 6, and **validate again**:
   the version did not pass, so the call is not the no-op above, and this is the only way to see the
   fix accepted. **Take a fresh pre-write read before the fixing write** — the call you already made
   re-shaped the blocks (`SKILL.md` step 7, CRITICAL 4(b)). This loop runs inside CRITICAL 6 and
   nothing suspends it: what means stop is the *same* objection returning unchanged.
3. **A problem that is yours and that you could not write** — a value you had to stop on under
   CRITICAL 2, or an objection naming a member no write reaches (`SKILL.md` → CRITICAL 6). Do
   not retry it and do not invent a value to silence it. Carry it to step 8 **ranked**: if it is the
   user's headline requirement, say plainly that the flow will not run until it is set, as a gap on
   your side.

**If you cannot tell which kind a message is, report it verbatim rather than guessing.** And **do not
assume a problem tells you where it is:** if it names no block, match it yourself from what you
wrote — but if **more than one** could be the subject, do not pick one. Report it verbatim, name the
candidates, and leave it to the user. Guessing is how you rewrite a block that was fine.

## A change asked for after a validation that passed

Start again from `SKILL.md` step 1(c): re-read the flow, its versions with their statuses, and its
current row version, or the write is refused as a conflict and applies nothing. **That re-read gets
you the row version; it is not the baseline for the write.** Take a fresh full-detail read of every
block you are about to touch as well — the call you made re-shaped them, so the pre-write read you
kept from step 5 cannot be diffed against what comes back (`SKILL.md` step 7, CRITICAL 4(b)). **Validating does
not, by itself, put the version out of reach** — which statuses accept writes is the write-path
sub-folder's to state, so read it rather than assuming. If a write *is* refused as not editable, say
plainly that the change could not be applied to this version, and stop.

If it goes through, **verify it in step 6 and then validate again** — the edit reopened validation,
so this change gets the same check as everything before it. Do not let a summary rest on the earlier
pass: what stands behind the flow is the validation that came after your last write.

# References

- `SKILL.md` → step 7 — the ordering rule and the ban on offering a pass as evidence
- `SKILL.md` → CRITICAL 6 — the session budget these failure modes run inside
- `references/troubleshooting.md` → *Validation* — one row per situation
- `references/hand-over.md` — where the three kinds end up
