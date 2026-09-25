# Flows wiki — where to look, what to look for

Block, event and step semantics live in the product wiki, served by the `wiki` tool on the
same server as the flow tools. Its schema owns the call shape — which domains it accepts,
and how many document ids one call takes. This file says how to navigate it.

**Do not decide from the tool's schema whether it can serve you — make the call.** A schema
read is not a capability check, in either direction.

**If no `wiki` tool is connected**, decode blocks from the flow itself — the bracket tag,
the block name, and the block's full properties — and flag anything you can't confirm
rather than guessing. That is the only fallback there is.

## Navigate index-first

There is no search; the domain index lists the domain's documents, so the indexes are the
entry points. Start at the flows domain index: it carries the UI-wording → technical term
map, the map from each block tag to its document, and the table of output names.

- `overview` — how a flow runs end to end, plus the flow-level settings a skeleton cannot
  show: how often one customer may re-enter, when the version starts and stops.
- A block → the `blocks` index; a trigger event on a start block → `events`; an operation
  step, such as a send and its channel → `steps`. Take the id from the index you are
  standing on.
- Whether a send is subject to subscription and contact checks, and what makes a flow
  transactional → `flow_types`.

An index answers in a single locale; leaf documents are English-only and speak the
technical vocabulary the flow tools return (block tags, output names, property names).

Only read what you need to explain this flow — don't walk the whole wiki.
