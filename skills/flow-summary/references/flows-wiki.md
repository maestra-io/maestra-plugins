# Flows wiki — where to look, what to look for

Block/event/step semantics are **not bundled in this skill**. They live in the product wiki,
which is served by the **`wiki` tool** on the same MCP server as the flow tools. This file says
where to look and what to look for — it does **not** copy wiki content (the wiki is the source
of truth; it changes).

## How the wiki is reached

**One route: the `wiki` tool.** Call it once per document — the flows domain, named as the
tool's own schema names it, plus the document `id`. Take the tool's name from your tool
listing. There is no other copy of the reference to read: no tree in the workspace, no files to
open, no path to ask the caller for.

**Do not decide from the tool's schema whether it can serve you — make the call.** Its
advertised argument list has understated what it answers, so a schema read is not a capability
check.

**If no `wiki` tool is connected**, fall back to decoding blocks from the flow itself (the
bracket tag, the block name, and `detail=Full` properties) and **flag anything you can't
confirm** rather than guessing (per the skill's never-fabricate rule). That is the only
fallback there is.

**One thing the tool cannot tell you:** different contours serve different revisions of the
wiki and no answer carries a version marker. Read what it answers as the reference anyway.

## Navigate index-first (never guess an id)

Retrieval is **navigate-only** — there is no search, no full-text lookup, and no call that
lists a domain's documents. So the indexes are the only entry points there are.

1. **Start at the flows domain index.** It lists the sections and, crucially, carries the
   **UI-wording → technical term map** (what a user's UI label maps to in `flows_lookup`
   terms). Turn the caller's wording into a term there *first*.
2. **Read `overview`** for how a flow runs end-to-end before the per-block docs.
3. **Open the leaf you need**, then **follow the `` `id` `` cross-links** inside it. Every doc
   ends with a `# References` section listing its outgoing ids — that is the navigation graph.
   **Never invent an id**; if unsure, read the relevant section index (`blocks`, `events`,
   `steps`) and take the id from there.

An index answers in a single locale and there is nothing to pick — read it as it comes. Leaf
docs are **English-only** and speak the **technical vocabulary `flows_lookup` returns** (block
tags, output names, property names).

## Ids

Domain-relative, lowercase snake_case; ids carry no `flows.` prefix. A prefix names a section
and the leaf names the document — `overview`, `blocks`, `blocks.<...>`, `events` /
`events.<type>`, `steps` / `steps.<type>`. **Take every id from the index you are standing
on**, never by assembling one from a block tag.

## What to look up for a summary

- **A block's meaning** → the **blocks index** maps each `flows_lookup` bracket tag
  (`conditionBlock`, `delayBlock`, `operationStepsBlockSettings`, …) to its `blocks.<...>` doc;
  open that doc. Don't guess the id from the tag — let the index map it.
- **A trigger event** on a start block → the **events index**, then the `events.<type>` doc.
- **An operation step** inside a steps group (e.g. a send and its channel) → the **steps
  index**, then the `steps.<type>` doc.
- **A user's UI wording** ("limit", "wait until", "control group") → the domain-index **term
  map** translates it to the technical tag/property, then open that doc.

Only read what you need to explain this flow — don't walk the whole wiki.
