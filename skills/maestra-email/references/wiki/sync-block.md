---
description: "A block shared between emails, <SyncBlock>: the tag is a reference with one attribute, its content is not in the JSX and is edited only in the editor, what is carried over, the library path, the unsubscribe caption inside it, the refusals"
---

# A block shared between emails — `<SyncBlock>`

A sync block is one block that stands in several emails at once. In the editor it is the “Universal block”. The email holds only a reference to it, so the tag
is self-closing and has a single attribute:

```jsx
<Template>
  <Block><FlexRow><Column size={12}><Text>Header</Text></Column></FlexRow></Block>
  <SyncBlock savedBlockInternalId="7c9e6679-7425-40de-944d-e07fc1f90ae7" />
</Template>
```

| | |
|---|---|
| where it stands | directly in `<Template>`, where a `<Block>` stands; a template may consist of sync blocks and editor-template blocks alone |
| attributes | `savedBlockInternalId` only; no children |
| letter styles | does not follow them ([theme.md](theme.md)): its look is fixed, as with any library block |

**Where it comes from.** Only from an email that was read, or from the library: in the library list
a row of `kind` `sync` is a sync block, and reading it returns this tag. An identifier
the project does not have is rejected on preview and on save, so **`savedBlockInternalId` is never invented.**

**The content is not in the JSX and cannot be changed through it.** It is edited only in the editor.
Asked to change text that is not in the JSX while the email has `<SyncBlock>` tags, find the text in the preview:
where a `<SyncBlock>` stands — it is inside a sync block; inside a `<QuokkaBlock>` — it is a setting of the editor-template
block ([quokka-block.md](quokka-block.md)).

**Carry the tag over as it came and where it stood, unless asked to move it.** Do not expand it into a `<Block>`
and do not build a similar block in its place: the block stops being shared, and the other emails no longer get
its changes. **Removing the tag is allowed** when asked: the email loses the block, while the library and the other
emails keep it.

**The preview draws its content**, links included, though the JSX hides it; an unsubscribe caption inside it —
[unsubscribe-link.md](unsubscribe-link.md).
