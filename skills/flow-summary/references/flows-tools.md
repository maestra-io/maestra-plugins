# Flows tools — what a summary needs from the read

The live tool schema is authoritative: it owns the arguments, the response shape and the
skeleton's line format. This file says only what a *summary* needs from `flows_lookup`.

- Start with the skeleton of the whole flow. It is cheap and it is the navigation map:
  one line per edge, each block printed with its type tag and, where it has one, its name.
- Fetch full properties only for the blocks that carry the meaning — the trigger, the
  sends (the channel and the message live there), the key conditions, the delays — and for
  the flow-level settings a skeleton cannot show.
- Execution counts are a second, optional read: corroborating colour rather than the point
  of a summary, and never quoted without the window they were counted over.
