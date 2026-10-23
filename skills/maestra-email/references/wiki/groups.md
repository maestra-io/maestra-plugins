---
description: "The line groups Menu, BulletList and Socials: what a line is, which attributes belong to the group and which to a line, the bullet icon and its two forms, defaults, what the editor allows where"
---

# Groups — `<Menu>`, `<BulletList>`, `<Socials>`

A group is one element whose children are lines written directly, without `<Column>`. The group decides the row:
the gaps between the lines, their alignment, the background and spacing around them. The words of a line look as
that line says, like any text or button — the group adds nothing to them. Each group holds one kind of line, and
all its lines are of that kind:

| group | lines | what it is for |
|---|---|---|
| `<Menu>` | `<Text>` or `<Button>`, not both | a horizontal row of links |
| `<BulletList>` | `<BulletItem>` | short one-line points with a marker in front |
| `<Socials>` | `<Image image={{…}} />` | a row of icons of equal size |

`<Labels>` is the fourth group — [label.md](label.md). `<Split>` is not a group but a row of columns — [containers.md](containers.md).

**Where a group may stand.** In a regular column or in a `<Split>` column. A line holds nothing beside its own
words — a badge next to a menu item is [label.md](label.md). The editor's canvas does not offer
`Menu`, `BulletList` or `Socials` inside a product row card; the converter lets them through there — a node the
editor cannot show — so a
successful preview proves nothing — a card holds plain elements.

```jsx
<Menu align={{ align: "center", mobile: { align: "center" } }} itemsGap={{ size: 16, mobile: { size: 16 } }}><Text><p style="margin: 0;"><a href="https://shop.example/catalogue">Catalogue</a></p></Text><Text><p style="margin: 0;"><a href="https://shop.example/delivery">Delivery</a></p></Text><Text><p style="margin: 0;"><a href="https://shop.example/contacts">Contacts</a></p></Text></Menu>
<BulletList bulletIcon={{ url: "https://cdn.shop.example/dot.png", fileName: "dot.png" }}>
  <BulletItem>Free delivery</BulletItem>
  <BulletItem><p style="margin: 0;">Returns <strong>within 30 days</strong></p></BulletItem>
</BulletList>
<Socials imageSize={{ type: "fixed", width: 32 }}>
  <Image image={{ mode: "static", static: { url: "https://cdn.shop.example/instagram.png", fileName: "instagram.png" } }} url="https://instagram.com/shop" alt="Instagram" />
</Socials>
```

## What a line carries

A line is the element it is named: a menu `<Text>` takes `style`, `themeVariant` and markup like any text
([text.md](text.md)), its link being an `<a>` in that markup; a menu `<Button>` takes `url`, `simpleTextStyles` and
the rest of [button.md](button.md); a socials `<Image>` takes `image`, `url` and `alt` from [image.md](image.md); a
`<BulletItem>` takes the content and `style` of a `<Text>` and follows the `text` variant of the letter styles field
by field unless `themeVariant` names another ([theme.md](theme.md)).

Where a line's own default differs from the standalone element's — it shows wherever the letter styles set nothing:

| line | setting | own default |
|---|---|---|
| `<Button>` in `<Menu>` | `iconDisplay` | `{ position: "LEFT" }` — the platform's placeholder icon, drawn in the preview and in the sent email; a standalone button's is `EMPTY` |
| | `background` | `{ type: "transparent" }` |
| | `innerSpacing` | 0 on all sides |
| | `simpleTextStyles` | `Inter`/`Tahoma` 16, `"1.0"`, `#000000`, no inscription |
| `<BulletItem>` | `style` | `Inter` 16; a standalone text's is `Arial` 18 |

What the group decides, the line cannot, so do not write it there: a socials `<Image>` with its own `size` is
accepted, and the group's `imageSize` draws; a `<BulletItem>` with its own `bulletIcon` or `iconTextGap` is
stored, and the list's values draw. `visibilityOnDevices` works on the group and on a single line alike.

## Attributes of the groups

| attribute | on | value | default |
|---|---|---|---|
| `align` | `Menu`, `Socials` | `{ align: "left" \| "center" \| "right", mobile: { align } }` — not on `BulletList` | `{ align: "center" }` |
| `itemsGap` | all | `{ size: N, mobile: { size: N } }` — between lines; on `Menu` and `Socials` horizontal only: a row that does not fit the phone wraps, and the wrapped lines touch — vertical `innerSpacing` on the lines gives the gap | `Menu` 20, `BulletList` 8, `Socials` 12 |
| `imageSize` | `Socials` | `{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }` — the width of every icon; only `fixed`, unlike `Image.size` | `{ type: "fixed", width: 40 }` |
| `bulletIcon` | `BulletList` | below | the editor's preset dot — its `data:` SVG breaks the `src`, a broken-image placeholder draws instead; write `bulletIcon` always, below |
| `iconTextGap` | `BulletList` | `{ size: N, mobile: { size: N } }` — between the marker and the words | `{ size: 8 }` |
| `iconTopPadding` | `BulletList` | `{ top, bottom, left, right, mobile: { … } }` — around the marker; `top` lines it up with the first line of text | `{ top: 6, bottom: 0, left: 0, right: 0 }` |
| `innerSpacing` | all | as for `Block` | 0 on all sides |
| `background` | all | as for `Block`; on `BulletList` only `transparent` or `color` | `{ type: "transparent" }` |
| `border`, `borderRadius` | all | as for `Block` | none, 0 |
| `visibilityOnDevices` | all | `"all"` \| `"desktop"` \| `"mobile"` | `"all"` |

## The bullet icon

`bulletIcon` is one image for every line of the list. Its value merges onto the editor's preset dot,
`{ type: "predefined", url: <the preset's data: SVG>, fileName, color, size: 4 }`:

```jsx
bulletIcon={{ url: "https://cdn.shop.example/dot.png", fileName: "dot.png" }}
bulletIcon={{ type: "custom", url: "https://cdn.shop.example/one.png", fileName: "one.png", size: 40 }}
```

The first form keeps the preset's `size`: a 4px-wide marker, a dot or a simple circle. The second is a marker of
its own width, a numbered badge or an icon; `size: 40` draws a 40px marker in the stored template and in the sent HTML alike. The address is one the gallery returned, like any image source; a value in
the shape of `image` (`{ mode: "static", static: … }`) is accepted and ignored, the broken preset draws.

**Always write `bulletIcon`.** The preset's `data:` SVG goes into `src` with its quotes unescaped, the attribute
breaks off, and the sent email shows a broken-image placeholder instead of a dot — in the preview too.

One list, one icon, one `size` on desktop and mobile; the file is a gallery image, and for a plain dot the gallery has one.
Different markers per line — "1", "2", "3" — need a file per number: separate
lists, one line each, or a fixed-size `<Image>` beside a `<Text>` in a two-column row; without files, a large number
as its own `<Text>` in a narrow column. A marker that must stay a
separate editable element in the editor is a `<BulletList>` line or an `<Image>`, not a styled `<span>` inside a
text and not `<Html>`: those draw but give the editor nothing to select. A badge that overlaps its text on the
phone gets a smaller `size` or becomes a standalone `<Image>` with `size.mobile.width`.

## What a list is not

A `<BulletList>` is for short one-liners. Features, plans, benefits, metrics with a heading and a description each
are a grid of columns, not a list. A list inside a paragraph, with no marker image, is `<ul>`
markup inside `<Text>` — [text.md](text.md).
