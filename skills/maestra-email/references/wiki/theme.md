---
description: "The email's letter styles: what they cover on which node, how a node follows or leaves them, themeVariant, the <Theme> tags with their exact props, moving styles from nodes into <Theme>, an email without its own styles, what the preview shows without a format"
---

# Letter styles — `themeVariant` and `<Theme>`

An email has its own set of styles — what a heading looks like, what the primary button looks like, what
background a block has. In the editor this is the "Design" tab.

The letter-styles read returns the current values as a ready `<Theme>` fragment in exactly the form below. Reading an email never returns `<Theme>`: the document carries the tag only when it
changes something.

## What the letter styles cover

Only these props, and only on these nodes:

| node | covered |
|---|---|
| `Block`, `FlexRow` | `background`, `innerSpacing` — one variant, not written |
| `Text`, `BulletItem` | inside `style`: `font`, `fallbackFontFamily`, `fontSize`, `lineHeight`, `letterSpacing`, `inscription`, `color`, `link`, `mobile.fontSize` — not the words, not `align`, not the other `mobile` fields |
| `Button` | `background`, `border`, `borderRadius`, `buttonSize`, `simpleTextStyles` |
| `Label` | `background`, `border`, `borderRadius`, `contentSpacing`, `simpleTextStyles` |

The same name is covered on one node and not on another: a `<Text>` with its own `background` still takes its
typography from the letter styles, because the text background is not in the set.

## A node follows the styles or has its own look

Nothing declares it; the converter **infers** it from what the node writes:

```jsx
<Text themeVariant="h1">Summer sale</Text>
<Button url="https://shop.example">Buy</Button>
<Text themeVariant="h1" style={{ align: "center" }}>Summer sale</Text>
```

The first two say nothing about their look and follow the styles. The third names only `align`, which the styles
do not set, so it stays under them and is centred at the same time. Name a value the styles do set, and the node is
detached: from then on edits to the styles no longer reach it.

**What the node did not name is filled in from the styles at the moment the document is read, and frozen** —
field by field inside every covered prop. `<Text style={{ fontSize: 20 }}>` carries the font and colour over from
the styles; `<Button borderRadius={{ topLeft: 4 }}>` keeps the other corners. So write only the fields the request
names; the carried-over ones are the same values either way. A document read before and after the styles are edited
yields nodes with a different look.

**The phone side is filled in the same way:** a phone field the node leaves out comes from the styles, not from the
node's own desktop value. A button with a size of its own writes `widthMobile` and `heightMobile` next to `width` and
`height`; a text whose phone size must differ from the variant writes `mobile.fontSize`.

When nothing was said about an element's look, it stays without style attributes and follows the styles.

## `themeVariant`

Which variant the node is assigned to: `h1`, `h2`, `h3`, `text` for a text or a bullet line, `primary` or
`secondary` for a button or a label. Blocks and rows have one variant and it is not written. Only a variant
different from the default (`text`, `primary`) is written. Having a variant says nothing about whether the node
follows the styles: these are read from different places.

The names are not interchangeable: on a node the attribute is `themeVariant`, inside `<Theme>` it is `variant`.
The converter refuses both mix-ups, with different messages: `variant` on a node is `Unknown attribute`;
`themeVariant` inside `<Theme>` is «The text styles come in 4 variants, so one has to be named». Neither means a
node cannot be assigned to a variant — the wrong name was used.

## `<Theme>` — editing the letter styles

Written once, directly inside `<Template>`, before the blocks, one tag per style kind, only on a request to change
the styling of the whole email ("make the buttons orange throughout", not "make this button orange"): editing a
shared style changes every node that follows it, including those the document did not touch.

```jsx
<Template>
  <Theme>
    <TextStyle variant="h1" simpleTextStyles={{ fontSize: 32, mobile: { fontSize: 26 } }} />
    <ButtonStyle variant="primary" background={{ type: "color", value: "#ff6600" }} />
  </Theme>
  <Block><FlexRow><Column size={12}><Text>Body</Text></Column></FlexRow></Block>
</Template>
```

| tag | `variant` | props |
|---|---|---|
| `BlockStyle`, `RowStyle` | none, not written | `background`, `innerSpacing` |
| `TextStyle` | `h1`, `h2`, `h3`, `text` | `simpleTextStyles` |
| `ButtonStyle` | `primary`, `secondary` | `background`, `border`, `borderRadius`, `buttonSize`, `simpleTextStyles` |
| `LabelStyle` | `primary`, `secondary` | as `ButtonStyle`, with `contentSpacing` instead of `buttonSize` |

The typography inside `<TextStyle>` is called `simpleTextStyles`, on `<Text>` itself the same set is `style`; the
fields are the same ([typography.md](typography.md)). The name in the style set and the name on the node do not
always match; the two tables above give the mapping.

**A field outside a style's set is refused**, with the list of what the style covers; most often this is an attempt
to set alignment, which lives on the node:

```jsx
<Theme><TextStyle variant="h2" simpleTextStyles={{ fontSize: 14 }} /></Theme>
<Text themeVariant="h2" style={{ align: "right" }}>Gmail</Text>
```

**`<Theme>` is a patch, down to the fields: what it does not name stays as the email had it** —
`<ButtonStyle variant="primary" background={{ … }} />` alone keeps the email's `buttonSize`, `border` and typography,
and `<TextStyle variant="h1" simpleTextStyles={{ fontSize: 34 }} />` changes only the size. Write only what the
request changes. The letter-styles fragment is for moving a look into the styles and for checking the values after the move.

## Moving styles from nodes into `<Theme>`

A request to "move the styles into the letter styles" is three actions in one document:

1. write the values into `<Theme>`;
2. **remove** these styles from the nodes that move under them;
3. add `themeVariant` where the variant is not the default.

Skipping the second is the most common mistake, and it is invisible: the look does not shift, the preview shows
nothing, and the letter styles end up applied to nothing. The person finds out at their first edit of them.

**The look after the move matches the previous one pixel for pixel.** Hence:

- **the number of variants is finite** — text `h1`/`h2`/`h3`/`text`, button and label `primary`/`secondary`,
  block and row one each. Different values are not merged into one variant;
- **values are not adjusted**: 12px stays 12px, no rounding, no "almost the same";
- **a different mobile size is a different look**, even if the desktop one matches;
- **more looks than variants** — state it as a number and leave the extra ones unique: "I found six text sizes,
  there are four variants; I'll move the four most common, and leave two unique — they are in the footer".
  Pulling a look toward the nearest variant is not allowed;
- **alignment stays on the node** — it is not part of the set and is not removed from the node during the move.

**The mobile side moves together with the rest.** The set holds it in two forms: nested
(`simpleTextStyles.mobile.fontSize`) and as a flat sibling field (`buttonSize.heightMobile`, `widthMobile`). Both
are written inside `<ButtonStyle>` / `<TextStyle>` on par with the desktop value: "the letter styles do not store
a separate mobile button height" is an unwritten field, not a limitation — look at what the fragment defines and
move everything the node had.

**Mobile values live in the variant, not on the node:** all buttons on `primary` have the same mobile height. A
node that needs on mobile something other than the variant cannot keep it under the styles, since a phone field it
does not name comes from the variant; for a text the styles set only `mobile.fontSize`, the rest of the mobile values
stay on the node. Moved, such a node loses its mobile difference; left unique, it keeps it. Rewriting a variant for
one node is not allowed: all nodes of the variant would change.

**A look that drifted after the move is always an incomplete set, not a platform limit.** Either the missing side is added, or the node stays unique.

After the move, for each node the styles were removed from, the variant's set matches what was removed, field by
field — before the move the values are in the document, after it in the letter-styles fragment.

## An email without its own letter styles

Every email has effective styles; not every email has its own. One that has not configured them takes the
platform default styles and stays that way: reading and saving do not turn them into its own, frozen at today's
values. The tool says this directly — do not present platform default values as the styling of the person's
email.

A preview without the template the email takes its settings from draws the document under the platform defaults,
`<Theme>` included — [canvas.md](canvas.md).
