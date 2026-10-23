---
description: "The containers Template, Block, FlexRow, Column and Split: attributes with defaults, what the letter styles cover, the twelfths grid, what spacing adds up from, mobile stacking and column order"
---

# Containers — `<Template>`, `<Block>`, `<FlexRow>`, `<Column>`, `<Split>`

```
Template  →  Block  →  FlexRow  →  Column  →  elements
```

A `<Block>` is a section of the email: its background runs edge to edge. A `<FlexRow>` is a row of columns inside
it; a `<Column>` holds the elements. A `<Split>` is an element: a row of columns inside a column, for an icon
beside a line of text. A block may hold a `<CollectionRow>` instead, the product row
([product-rows.md](product-rows.md)), and a `<QuokkaBlock>` ([quokka-block.md](quokka-block.md)) or a `<SyncBlock>` ([sync-block.md](sync-block.md)) stands where a block stands.

A wrong root, an element straight in a row, an empty template, block, row or group, a column without `size`,
sizes that do not sum to 12, a fractional `size`, an unknown tag or attribute — the converter refuses each with a
message naming the tag; fix by the message. What it does not refuse: a label or a group where the editor has none
([label.md](label.md), [groups.md](groups.md)).

## `<Template>`

| attribute | value | default |
|---|---|---|
| `containerWidth` | number, px | 600 |
| `background` | as for `Block`; an image — [image.md](image.md) | transparent |

Unlike a node's attributes, these are **carried over on save** from the email's previous version: its width and
background, the "Global (CSS) styles", the Gmail annotation and the letter styles. What
the document does not name stays as it was: width and background are named here, the letter styles with `<Theme>`
([theme.md](theme.md)), the CSS and the annotation only in the editor.

## `<Block>`

```jsx
<Block background={{ type: "color", value: "#F5F5F5" }} innerSpacing={{ top: 24, bottom: 24, left: 24, right: 24 }}>
```

| attribute | value | default |
|---|---|---|
| `background` | `{ type: "color", value: "#RRGGBB" }` \| `{ type: "transparent" }` | letter styles (the platform's: `#FFFFFF`) |
| `innerSpacing` | `{ top, bottom, left, right, mobile: { … } }`, px | letter styles (the platform's: 0) |
| `border` | `{ type: "none" \| "solid" \| "dashed" \| "dotted", color, size: { top, right, bottom, left } }` | none |
| `borderRadius` | `{ topLeft, topRight, bottomLeft, bottomRight, mobile: { … } }` | 0 |
| `gapAfterBlock` | `{ desktop: N, mobile: N }` — a strip **outside** the block, below it; it shows `externalBackground` when that is set, otherwise `Template.background` | 0 |
| `externalBackground` | as `background` — what fills the page beside the block when the client's window is wider than the email | transparent |
| `visibilityOnDevices` | `"all"` \| `"desktop"` \| `"mobile"` — on the canvas the hidden block is drawn blurred, in the email a media query hides it ([canvas.md](canvas.md)) | `"all"` |
| `targeting` | printed by a read email on `Block`, `FlexRow` and `QuokkaBlock`; carried over unchanged, never written anew — a segment is chosen in the editor, and losing the attribute sends the block to everyone | — |

"letter styles": `background` and `innerSpacing` are what the email's `BlockStyle` covers; a block that writes either
is detached from it and the other is frozen at the styles of that moment ([theme.md](theme.md)). A partial
`innerSpacing` or `background` is completed from the styles. Spacing and backgrounds on blocks and rows are the normal
way to lay out a section and are not a reason for Workflow step 5.

Vertical rhythm inside a section is `innerSpacing` of the block, the row or the column, so the section's background
continues under it; a visible strip of the page between sections is `gapAfterBlock`, written only when the user asks
for one or the mockup shows it — an existing one outside the part being edited stays. Two blocks with no gap and the
same `background` read as one card.

## `<FlexRow>`

| attribute | value | default |
|---|---|---|
| `background` | as for `Block` | letter styles (the platform's: transparent) |
| `innerSpacing` | as for `Block` | letter styles (the platform's: 10 on all sides) |
| `border`, `borderRadius` | as for `Block` | none, 0 |
| `columnsGap` | `{ size: N, mobile: { size: N } }` — between the columns; on the phone, when the columns stack, the same gap turns vertical | `{ size: 20 }` |
| `rowsGap` | `{ size: N, mobile: { size: N } }` — a gap below this row, before the next one in the block; written on the last row it adds space under it | `{ size: 0 }` |
| `verticalAlign` | `{ align: "top" \| "middle" \| "bottom", mobile: { align } }` — of the columns' content; once the columns stack on the phone it has no effect, so the mobile branch matters only with `isColumnsMobileAdaptive={false}` | `{ align: "top" }` |
| `isColumnsMobileAdaptive` | boolean — `true`: on screens narrower than the email each column takes the full width, one under another; `false`: the columns stay in one line at their share of the width, and a long caption in a narrow column wraps by words | `true` |
| `columnVerticalDirection` | `{ direction: "ttb" \| "btt" }` — the order of the stacked columns on the phone; `btt` puts the last column first. Columns are written in desktop order, and the desktop does not change. Works only while the columns stack, with `isColumnsMobileAdaptive` true | `{ direction: "ttb" }` |
| `emptyVariableBehavior` | `"show"` \| `"hide"` — [personalization.md](personalization.md) | `"show"` |
| `visibilityOnDevices` | as for `Block`. A row hidden on a device leaves its block, the block's spacing and `gapAfterBlock` in place — to hide a whole section, hide the block; a hidden block takes its `gapAfterBlock` with it, so a strip that must stay on the phone goes on the previous block as `gapAfterBlock.mobile`, and a mobile-only block carries its own as `gapAfterBlock.mobile` too. Hiding switches at 500px, stacking at 600px: between them the desktop variant shows on the stacked layout | `"all"` |
| `targeting` | as for `Block` | — |

`RowStyle` covers `background` and `innerSpacing`, as `BlockStyle` does for a block. The row spacing of the styles
(10px on every side in the platform's) and the 20px `columnsGap` are part of every width and distance: for a mockup
reproduced to the pixel, set them to the mockup's values, writing 0 where the mockup has none.

A new row joins an existing block when it belongs to the same section, with the same background; a new section
is a new block.

## `<Column>`

| attribute | value | default |
|---|---|---|
| `size` | **required**, an integer 1..12; the sizes of one row sum to 12 | — |
| `background`, `border`, `borderRadius`, `innerSpacing` | as for `Block` | transparent, none, 0, 0 |

A column does not take `visibilityOnDevices` (`Unknown attribute`): hide the row, or the element inside.

An empty `<Column />` is a grid tool only: it fills out a row with an odd number of cards or narrows a card
(`3+6+3` for one half the email wide) when the mockup or the user shows it. On the phone the empty columns stack
like any other, so the narrowing holds on the desktop only. It is never a way to centre or to space anything: in
the preview and on the canvas an empty column draws a placeholder about 177px tall — the editor's drop zone — and
the user sees a broken layout, though the sent email has nothing there. Whatever must sit in the middle is centred
by its own `align` on a `12` column — a text, an image, a button; a pair side by side, an icon beside a number, is a
`<Split>` whose halves lean toward each other: the left element `align` right, the right one `align` left.

A card section — a feature grid in the brand's colours; the roles are copied from the reference, not the values:
the section's background, the card's one step lighter or darker, an accent on the heading, a muted description:

```jsx
<Block background={{ type: "color", value: "#1F2933" }} innerSpacing={{ top: 32, bottom: 32, left: 24, right: 24 }}>
  <FlexRow><Column size={12}><Text themeVariant="h1" style={{ color: "#FFFFFF", align: "center" }}>What the service includes</Text></Column></FlexRow>
  <FlexRow columnsGap={{ size: 16, mobile: { size: 12 } }} rowsGap={{ size: 16 }}>
    <Column size={6} background={{ type: "color", value: "#2C3844" }} borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12 }} innerSpacing={{ top: 20, bottom: 20, left: 20, right: 20 }}>
      <Text themeVariant="h3" style={{ color: "#F2B705" }}>Delivery</Text>
      <Text style={{ fontSize: 14, color: "#D5DBE1" }}>We pick up and deliver at a time that suits you</Text>
    </Column>
    <Column size={6} background={{ type: "color", value: "#2C3844" }} borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12 }} innerSpacing={{ top: 20, bottom: 20, left: 20, right: 20 }}>
      <Text themeVariant="h3" style={{ color: "#F2B705" }}>Support</Text>
      <Text style={{ fontSize: 14, color: "#D5DBE1" }}>We answer in chat seven days a week</Text>
    </Column>
  </FlexRow>
</Block>
```

## `<Split>`

An element: a row of columns inside a column, for lines of "icon beside text". Its columns carry only `size`
and hold 0..1 element each; a group may stand in one, `<Split>` may not.

```jsx
<Column size={12}><Split><Column size={5}><Text>Free delivery</Text></Column><Column size={7}><Button url="https://shop.example/delivery">Details</Button></Column></Split></Column>
```

| attribute | value | default |
|---|---|---|
| `columnsGap` | as for `FlexRow` | `{ size: 12 }` |
| `verticalAlign` | as for `FlexRow` | `{ align: "middle" }` |
| `innerSpacing`, `background`, `border`, `borderRadius` | as for `Block` | 0, transparent, none, 0 |
| `visibilityOnDevices` | as for `Block` | `"all"` |

Its columns stay side by side on the phone — a `<Split>` never stacks.

Inside a product row card a split may also carry `height` — [product-rows.md](product-rows.md). A price beside its old price — [text.md](text.md), "Two values in one text".

One under another is two elements in one column, the distance between them from their own `innerSpacing`; side by
side is the columns of a row, the cards of a product row or a `<Split>`. One under another inside a `<Split>` cannot
be built: its column holds one element.

## Synchronized rows

Static cards side by side with buttons at one height are not one `Column` per card — column heights are independent
and the buttons drift. Build one `FlexRow` per layer, the same column split in each:

```jsx
<FlexRow><Column size={6}><Image image={{ … }} /></Column><Column size={6}><Image image={{ … }} /></Column></FlexRow>
<FlexRow><Column size={6}><Text themeVariant="h3">River cruises</Text></Column><Column size={6}><Text themeVariant="h3">Parks</Text></Column></FlexRow>
<FlexRow><Column size={6}><Text>Three evening routes.</Text></Column><Column size={6}><Text>Quiet corners.</Text></Column></FlexRow>
<FlexRow><Column size={6}><Button url="https://shop.example/river">Water routes</Button></Column><Column size={6}><Button url="https://shop.example/parks">Green map</Button></Column></FlexRow>
```

The price is the phone: the columns stack layer by layer — all images, then all headings, then all buttons — not
card by card. A card-by-card mobile order is a product decision for the user (for example separate mobile rows with
`visibilityOnDevices`). Product cards from a mechanic do not need this: a `<CollectionRow>` draws every card from one
template ([product-rows.md](product-rows.md)).

## The grid

Widths are twelfths of the email width: `12` one column, `6+6`, `4+4+4`, `8+4`, `3+3+6`, `2+10`. Elements adjacent in one
row of the source (an HTML table row, a div row, another platform's row) stay in one `FlexRow`, and the source's
proportions become integer sizes summing to 12 (`600+600` of `1200` → `6+6`). A pixel width
from a mockup is rounded to the nearest twelfth, and the resulting pixels differ from the mockup's: 210px of 600 is
4.2 twelfths, written `4+8`, which is 200px and 400px of the grid width before the row's own spacing. `columnsGap`
is taken out of the column to its left: `8+4` with a gap of 24 on a 600 grid is 376 + 24 + 200, not 384 and 192. When the
mockup's gap between tiles and the tile widths do not both fit the twelfths, the gap stays: `columnsGap` takes the
mockup's value and the widths move to the nearest twelfth — the gap is what reads as the rhythm. Name the pixels that
moved and the true cause: the grid changes a width, never a gap. A lone
column of a row is `12`, not its share of a wider design. Each `<FlexRow>` and each `<Split>` sums to 12 on its
own.

## What spacing adds up from

An unwritten setting is not zero but the node's default, and a distance in the email is the sum of neighbours:
the block's padding, the row's 10, the column's 0, the element's own. Flush is written with explicit zeros. When
the rhythm comes from a mockup, set spacing on every node involved and check each against its attribute table:
the containers' above, an element's own spacing, gaps and alignment in [text.md](text.md), [button.md](button.md),
[divider.md](divider.md), [image.md](image.md), [label.md](label.md), [groups.md](groups.md); the heights inside a
product row card — [product-rows.md](product-rows.md), "Card heights and `autosizeKey`". For `Block` and
`FlexRow`, when the email's letter styles set a value, that one applies, not the own value in the table.
