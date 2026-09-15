# DSL surface — what you can write in JSX

**When to read:** when it is unclear which tag/attribute to use or how the allowed
JSX/rich-text markup is structured. Exact value shapes are picked separately via the `SKILL.md` router.
**Return to:** Workflow / Self-check in `SKILL.md`.

This is a reference for the JSX markup used to generate and edit Maestra emails. It covers only what can be expressed in the markup; everything else (UUID, envelope, subject, targeting, materialization, etc.) is added by the serializer itself or ignored.

This reference describes the currently accepted DSL; the mandatory backend check is performed via `convert` in `maestra-email-ops`.

## 1. Structure

The four outer containers always go in this order; after `<Column>` comes an element, including a group:

```
Template  →  Block  →  FlexRow  →  Column  →  Text | Button | Divider | Html | Image | Menu | BulletList | Socials | Split
```

```jsx
<Template>
  <Block>
    <FlexRow>
      <Column size={8}><Text>Main column</Text></Column>
      <Column size={4}><Text>Side column</Text></Column>
    </FlexRow>
  </Block>
</Template>
```

Rules:

- **Exactly one `<Template>`** per document, and nothing outside it. Use only `<Template>` as the root. `<Email>`, `<Root>`, or any other root tag is rejected: `The root element must be <Template>`.
- **Each container holds only its own kind of child.** `<Template>` — blocks; `<Block>` — rows; `<FlexRow>` — columns; only `<Column>` — elements or groups. Putting `<Text>` directly into `<FlexRow>` is an error, not a shortcut.
- **A block has a second kind of row — `<CollectionRow>`**, the product row. It holds product cards rather than columns, and is described in [product-rows.md](./product-rows.md). Everything else in this file is about `<FlexRow>`.
- **Use `<FlexRow>`, not `<Row>`.** The row tag in the production converter is `FlexRow`. `<Row>` is rejected as `Unknown element <Row>`.
- **Every container requires at least one child** — except the column. An empty `<Template>`, `<Block>`, or `<FlexRow>` is an error. An empty `<Column>` is allowed.
- **A column requires `size`** — an integer from 1 to 12. The `size` values of the columns in one `<FlexRow>` must sum to 12 (see §5).
- **A group requires at least one item.** `<Menu>` contains only `<Text>` or only `<Button>`; `<BulletList>` — only `<BulletItem>`; `<Socials>` — only `<Image image={{...}} />`.
- **`<Split>` contains only `<Column size={N}>`.** Their `size` values sum to 12; a Split column carries only `size` and contains 0..1 element. Any group is allowed inside it, except `<Split>`.

## 2. Value grammar — literals only

Attributes accept only strings, numbers, JSON objects, and arrays; do not generate expressions,
spread, imports, executable code, comments, or Markdown fences. This file is responsible
for the allowed tags/attributes and the markup structure; for value shapes go back to the
`SKILL.md` router.

## 3. Write only what you are changing

JSX → template creates a new node with defaults. An attribute changes the specified setting; omitting one
does not restore the value from a previously saved email.

```jsx
<Divider innerSpacing={{ top: 30 }} />
```

Objects are filled in from defaults key by key; lists are replaced wholesale. To reset, specify
an explicit empty/zero value, `{ type: "none" }` for a border, or `{ type: "transparent" }`
for a background.

A rule about you, not about the converter: **reading an email prints the whole look set for a node that does
not follow the letter styles (the editor's Design tab)** — for text that is all nine `style` fields. All nine are
printed, even though the letter styles do not govern each of them: alignment is part of the printed set but does
not fall under the letter styles (§8). This is
by design: a node that stayed silent about these fields would turn out to follow the letter styles on the next
read, and its look would drift. Do not trim such sets when editing — keep them as they are and change in them
what you were asked to.

## 4. Containers — attributes

Only these attributes. Anything else is `Unknown attribute` (not a silent drop).

| Container | Attribute | What it does |
|---|---|---|
| `Template` | `containerWidth` | Email width in pixels. Number: `700` |
| `Template` | `background` | Email background — what is visible behind the column. JSON: same as `Block` |
| `Block` | `background` | Background. JSON: `{ type: "color", value: "#f5f5f5" }` or `{ type: "transparent" }` |
| `Block` | `border` | Border. JSON: `{ type: "solid", color: "#cccccc", size: { top: 1, right: 1, bottom: 1, left: 1 } }` or `{ type: "none" }` |
| `Block` | `borderRadius` | Corner rounding. JSON: `{ topLeft: 0, topRight: 0, bottomLeft: 0, bottomRight: 0, mobile: { … } }` |
| `Block` | `innerSpacing` | Inner padding. JSON: `{ top, bottom, left, right, mobile: { … } }`. **Do not write `padding`** — no such attribute exists; use `innerSpacing` |
| `Block` | `gapAfterBlock` | Outer gap after the block. JSON: `{ desktop, mobile }`. For ordinary spacing inside a colored section, use `innerSpacing` by default; a new `gapAfterBlock` — only on explicit request or when a visible gap showing the outer background color is intended |
| `Block` | `externalBackground` | Outer background |
| `Block` | `visibilityOnDevices` | Visibility. String: `"all"` (default), `"desktop"`, `"mobile"` |
| `FlexRow` | `background` | same as `Block` |
| `FlexRow` | `border` | same as `Block` |
| `FlexRow` | `borderRadius` | same as `Block` |
| `FlexRow` | `innerSpacing` | same as `Block`. **Not `padding`** |
| `FlexRow` | `columnsGap` | Gap between columns. JSON: `{ size: 20, mobile: { size: 20 } }` |
| `FlexRow` | `rowsGap` | Gap between rows (mobile-stacked) |
| `FlexRow` | `verticalAlign` | Vertical alignment. JSON: `{ align: "middle", mobile: { align: "middle" } }` |
| `FlexRow` | `isColumnsMobileAdaptive` | Whether to collapse the columns into a stack on a screen narrower than the email. Boolean, `true` by default: a column takes the full width, and `columnsGap` turns from horizontal into vertical. `false` — the columns stay in a row at their share of the width, and a long caption in a narrow column wraps by words |
| `FlexRow` | `columnVerticalDirection` | Column order when collapsing. JSON: `{ direction: "ttb" }` (default) or `{ direction: "btt" }` — on mobile the last column comes first, the desktop order does not change. Takes effect only with `isColumnsMobileAdaptive: true`; otherwise there is no collapsing and no order to change |
| `FlexRow` | `visibilityOnDevices` | same as `Block` |
| `FlexRow` | `emptyVariableBehavior` | String: `"show"` (default) or `"hide"`. `hide` removes the row from the **sent** email if a variable in it is empty; in the preview the row is always visible |
| `Column` | `size` | **Required.** Integer 1..12 |
| `Column` | `background` | same as `Block` |
| `Column` | `border` | same as `Block` |
| `Column` | `borderRadius` | same as `Block` |
| `Column` | `innerSpacing` | same as `Block`. **Not `padding`** |

The root attributes are about the email as a whole, and both are optional: not named — left as it was. The "Global (CSS) styles" and the Gmail annotation have no attributes and are edited only in the editor; on save they are carried over.

`Column.size` is the only required attribute among containers. The attribute `flexColumnSize` must not be used — that is the internal prop name; write `size`.

`innerSpacing` and `gapAfterBlock` are not interchangeable: `innerSpacing` keeps the container's
background under the spacing, `gapAfterBlock` shows the outer background between sections. When
creating/editing, do ordinary vertical spacing via `innerSpacing`; do not remove an untouched
existing `gapAfterBlock` during an unrelated round-trip edit.

### Image background

The email background is not just a color: `Template.background` accepts an image.

```jsx
<Template background={{
  type: "image",
  url: "https://cdn.example.com/62B73F41….jpeg",
  fileName: "62B73F41….jpeg",
  fallbackColor: "#ffffff",
  mode: "cover"
}}>
```

The image address (a URL exactly as the gallery returned it) is obtained the same way as for `<Image>` — the "Images" section in `SKILL.md`.

`mode` decides how the image fills the background area:

| `mode` | what it does |
|---|---|
| `cover` | fills it, cropping the excess on one side |
| `contain` | fits it in whole, leaving empty space on the other |
| `stretch` | stretches it over the whole area, distorting the proportions |
| `repeat` | tiles it with copies |

`fallbackColor` is not a decorative field: some email clients will not show a background image at all, so
the text on top must be readable against it too, and a meaningful image goes in an `<Image>`, not into the background.

**Targeting** is deliberately not part of the DSL: it points outward from the email, stays as it is, and writing it is an error.

A node's subscription to the letter styles has no separate attribute either, and it **is not written but inferred**: a node that named none of the settings the letter styles cover follows them; a node that named all of them is taken off them. Which settings those are and why the set cannot be written halfway — in §8.

## 5. Grid

The `size` values of the columns in each `<FlexRow>` and `<Split>` **must sum to 12**.
`Column.size` is only an integer 1..12: the backend rejects fractional values rather than rounding them.

```jsx
<FlexRow><Column size={6}>…</Column><Column size={6}>…</Column></FlexRow>
<FlexRow><Column size={4}>…</Column><Column size={4}>…</Column><Column size={4}>…</Column></FlexRow>
```

Do not write `size={6}` on a lone column of a multi-column row — the sum will not reach 12 and it will be an error. For a single column spanning the whole row use `size={12}`. Rows and Split are independent: each sums to 12 separately.

Pixel → grid is computed in twelfths of the container, not by an arbitrary pixel
width. For example, 480px in a 1200px container is 4.8/12; such a
`size` cannot be expressed; the nearest valid cut is 500px = `5/12`, that is `5+7`.

## 6. Elements

Elements live inside `<Column>`. Fully supported: `<Text>`, `<Button>`, `<Divider>`, `<Html>`, `<Image>`, `<Menu>`, `<BulletList>`, `<Socials>`, `<Split>`, `<Labels>`. Do not generate `<Timer>` or `<Video>` without a separately verified stored schema; `<BulletItem>…</BulletItem>` is allowed only as an item of `<BulletList>`, `<Label>…</Label>` — only as an item of `<Labels>`.

Empty nodes are emitted self-closing: `<Column size={4} />`, `<Html />`, `<Divider />`, `<Image ... />`. On write, both forms (`<Column size={4}></Column>` and `<Column size={4} />`) are read identically.

**Inside a product-row card the attribute set is wider** — an element there has settings that the same element
in an ordinary column lacks: `height` on `<Text>`, `<Image>` and `<Split>`, `url` on `<Text>` and
`<Divider>`. The tables below are about an ordinary column; the card additions are in [product-rows.md](./product-rows.md).

**Several values side by side are better kept as separate elements.** Two `<Var>` in one `<Text>` are one
cell: the values cannot be told apart by look or by empty-value behavior, and in the editor they are edited
only together. Price and old price, price and discount, name and SKU are usually worth
separating.

The layout is then decided by the column and the spacing: one below the other — two `<Text>` in a row in one column
(the distance between them comes from their own `innerSpacing`); side by side — the columns of a row, of a card or of a
`<Split>`. One below the other cannot be built inside a `<Split>`: its column holds only one element.

### Defaults that appear on their own

An unwritten setting is not zero but the element's default, and the distance in the email adds up from the
neighbors. **Flush is written with explicit zeros**: `innerSpacing={{ top: 0, bottom: 0 }}`. When taking the rhythm from
a mockup, set the spacing on every element that takes part in it, and check against this table —
the defaults live only here, they are not duplicated in place.

| setting | on | default |
|---|---|---|
| `innerSpacing` | `Text`, `Button` | 10 top and bottom |
| | `Divider` | 20 top and bottom |
| | `Label` | 8 bottom; on a label this is the **outer** spacing |
| | `Image`, `Menu`, `BulletList`, `Socials`, `Labels`, `Split` | 0 |
| `contentSpacing` | `Label` | 8 on all sides — the padding inside the label |
| `itemsGap` | `Labels`, `BulletList` | 8 |
| | `Socials` | 12 |
| | `Menu` | 20 |
| `buttonSize` | `Button` | `{ height: 50, widthType: "percent", width: 100 }` |
| `height` — **only inside a product-row card** | `Image` | 220 px, `manual` |
| | `Split` | 58 px, `manual` |
| | `Text` | by content, `original` |

The height container reserves space even when the content is shorter than it: in a card this is the main source
of a broken rhythm. What to do about it — [product-rows.md](./product-rows.md), "Card heights".

### Text

Content: the text itself or HTML markup, between the tags (see §7). The `style` attribute — typography of the text as a whole.

```jsx
<Text>Summer sale starts today</Text>
<Text innerSpacing={{ top: 24, bottom: 24 }} background={{ type: "color", value: "#f5f5f5" }}>
  Text with spacing and background
</Text>
<Text style={{ fontSize: 24, inscription: ["bold"] }}>
  <p style="margin: 0;">Summer <strong>sale</strong>, <a href="https://shop.example">see the offers</a></p>
</Text>
```

| Attribute | What it does |
|---|---|
| `style` | Typography of the whole text (font, fontSize, color, inscription, link, align, mobile). JSON. **Do not write `fontSize`, `color`, `align` as separate attributes** — they do not exist; nest them inside `style={{ … }}`. If `fontSize` or `align` is set, set `style.mobile` deliberately. A new `font.family` — only for a font the user has confirmed as already available in the Maestra editor; an existing family is preserved on round-trip |
| `innerSpacing` | same as `Block` |
| `background` | same as `Block` |
| `border` | same as `Block` |
| `borderRadius` | same as `Block`. **Not `radius`** |
| `visibilityOnDevices` | same as `Block` |

### Button

Content: the button label, between the tags. **Plain text only.** Markup inside `<Button>` is forbidden — `<strong>…</strong>` yields `<Button> may only contain text`.

```jsx
<Button url="https://shop.example/sale">Shop now</Button>
<Button url="mailto:hi@example.com" buttonSize={{ widthType: "percent", width: 60 }} borderRadius={{ topLeft: 24, topRight: 24, bottomLeft: 24, bottomRight: 24 }}>
  Write to us
</Button>
```

**Width comes in two kinds, and the kind is chosen explicitly.** `widthType` is `"percent"` (default) or `"pixels"`,
both accepted by the editor. If you write `width`, write `widthType` next to it; otherwise the number is merged onto the default
`percent`, and `{{ width: 240 }}` turns out to be 240 percent, not pixels. The whole default is
`{ height: 50, widthType: "percent", width: 100 }`: for a full-width button write nothing.

Percent is safer: a pixel width stays in pixels on mobile too (`240px !important`), and in
a column or card narrower than its value the button gets clipped. So `"pixels"` is a deliberate choice for
a mockup with a specific width, not the default form. `widthMobile` and `heightMobile` are optional:
without them the mobile side repeats the desktop one — that is synchronization, not an omission. Write them when
the mobile value must differ.

| Attribute | What it does |
|---|---|
| `url` | Link. Write `url`, **not `href`** — `href` is rejected as `Unknown attribute`. For a new CTA, `url` is required by policy; when the attribute is absent the converter leaves the default. `https://`, `tel:`, `mailto:` (the type is inferred from the value) |
| `align` | Alignment. JSON: `{ align: "center", mobile: { align: "center" } }` |
| `innerSpacing` | same as `Block` |
| `buttonSize` | Size. JSON: `{ height, heightMobile, widthType: "percent", width: 100, widthMobile: 100 }`. Width is in percent; for pixel width and the mandatory `widthType` see above |
| `background` | same as `Block`. Default `{ type: "color", value: "#000000" }` |
| `simpleTextStyles` | Label typography. JSON: `{ font: { family: "Arial" }, fontSize: 14, color: "#ffffff", inscription: [], mobile: { fontSize: 14 } }`. `family` here illustrates an existing/confirmed font, not permission to guess a new one. If a desktop `fontSize` is set, set `mobile.fontSize` deliberately |
| `border` | same as `Block` |
| `borderRadius` | same as `Block`. Default 8 on each corner |
| `iconSrc` | Icon next to the label. JSON: `{ url: "https://cdn.example.com/cart.png" }` |
| `iconAlt` | Icon alt text |
| `iconDisplay` | JSON: `{ position: "EMPTY" }` (default — no icon) |
| `iconSizeInPercents` | JSON: `{ widthInPercents: 30 }` |
| `visibilityOnDevices` | same as `Block` |

### Divider

A horizontal line. No content, always a single tag: `<Divider />`.

```jsx
<Divider />
<Divider innerSpacing={{ top: 18, bottom: 18 }} border={{ type: "solid", color: "#cccccc", size: { top: 1, right: 1, bottom: 1, left: 1 } }} />
```

| Attribute | What it does |
|---|---|
| `innerSpacing` | same as `Block`. Default `{ top: 20, bottom: 20, left: 0, right: 0, mobile: { … } }` |
| `border` | The line as a whole. JSON: `{ type: "solid", color: "#000000", size: { top: 1, right: 1, bottom: 1, left: 1 } }`. **Do not write `color` and `thickness` as separate attributes** — they do not exist; nest `color` and `size` inside `border={{ … }}`. **Specify the whole object** — with a partial merge, `border={{ color: "…" }}` takes `type` and `size` from the default. **One thickness for all four sides** (usually `1`): the line is drawn only from a value with equal sides, and with unequal ones it is not drawn at all — the converter rejects such a value |
| `visibilityOnDevices` | same as `Block` |

### Html

Arbitrary HTML between the tags. Order of preference: standard flexible blocks first (`Text`/`Button`/`Image`/`Menu`/`BulletList`/`Socials`/`Split`); `<Html>` is only a fallback when what is needed cannot be expressed otherwise, or on the user's direct request. Text, a button, and an image will survive manual edits in the Maestra editor; an html block will not.

```jsx
<Html>{"<table><tr><td>Raw table markup</td></tr></table>"}</Html>
```

There is one form: a single quoted string (`<Html>{"<table>…</table>"}</Html>`). Use it for
required raw markup that cannot be expressed with standard blocks. Direct JSX inside
`<Html>` is rejected by the backend; an empty `<Html />` creates a library placeholder.

| Attribute | What it does |
|---|---|
| `visibilityOnDevices` | same as `Block` |

### Image

`<Image>` is a standalone image or an item of `<Socials>`. A complete source is required:

```jsx
<Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
<Image
  url="https://shop.example/item"
  align={{ align: "center", mobile: { align: "center" } }}
  size={{ type: "fixed", width: 120, mobile: { type: "fixed", width: 80 } }}
  image={{ mode: "static", static: { url: "https://cdn.example.com/icon.png", fileName: "icon.png" } }}
/>
```

The URL in the example is illustrative. The URL source and the rules for choosing a gallery asset are defined in
`SKILL.md`; the allowed shape of `image` and `fileName` is shown in the example and the table below.

The second kind of source is a personal image: the address comes from the customer's or order's data,
and instead of `static` you fill `dynamic` with a segment list containing a chip. `static` need not be
written then; the missing fields are merged onto the default:

```jsx
<Image image={{ mode: "dynamic", dynamic: [<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "<CUSTOM_FIELD_SYSTEM_NAME_FROM_LOOKUP>" }} />] }} />
```

The click is personalized the same way: `url={["https://shop.example/points/", <Var … />]}` or a single `<Var>`
as the whole value. The rules are in `SKILL.md`, section "Images" → "Personal image for the customer".

| Attribute | What it does |
|---|---|
| `image` | **Required.** File: `{ mode: "static", static: { url: "<HTTPS URL>", fileName: "<name>" } }`. Personal image: `{ mode: "dynamic", dynamic: [<Var … />] }` |
| `url` | Optional HTTPS click-through link for the image. This is not the image source; do not write a placeholder. Personalized with a segment list |
| `size` | Size of a standalone image. Fixed: `{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }`. Stored constructor templates also round-trip `{ equalizedImageMaxWidth: "N" }`; preserve this field, but do not invent it |
| `align` | Alignment of a standalone image: `{ align: "left"|"center"|"right", mobile: { align: "…" } }` |
| `innerSpacing` | same as `Block` |
| `border` | same as `Block` |
| `borderRadius` | same as `Block` |
| `visibilityOnDevices` | same as `Block` |

Do not generate `background` (the backend rejects it), or the HTML attributes `src`, `href`, `alt`,
`width`, or `radius`. Use `image` for the source, the constructor attr `url` for the click,
`size` for the size, and `align` for alignment. For `<Socials>` items, size and
alignment are set on the parent `Socials.imageSize`/`Socials.align`.
A bare `<Image />` is forbidden by policy, because the backend substitutes a base64 placeholder.

### Labels and Label

A label: short text on a background with rounded corners and an optional icon.

**Put labels only in a product-row card.** The restriction lives in the editor's canvas, not in the converter: it will both accept and render an ordinary row with a label, but in the editor such a label does not exist — so a successful preview here is not permission, but exactly the case where it proves nothing.
And **`<Label>` lives only inside `<Labels>`**.

The content is text or a segment list with a chip; a chip as a child element is rejected
(`<Label> may only contain text`).

```jsx
<Labels itemsGap={{ size: 8 }}>
  <Label background={{ type: "color", value: "#ffe8e8" }} borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12 }} simpleTextStyles={{ fontSize: 12 }}>Bestseller</Label>
  <Label iconDisplay={{ position: "LEFT" }} iconSrc={{ url: "https://cdn.example.com/fire.png", fileName: "fire.png" }}>{["−", <Var param="ProductDiscount" />]}</Label>
</Labels>
```

| Attribute | Value |
|---|---|
| `Labels` | `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` |
| `url` | A string, as on `<Button>`: makes the label clickable |
| `contentSpacing` | The padding inside the label, around the text. Default is 8 on all sides |
| `simpleTextStyles` | Typography of the caption, as on `<Button>` |
| `iconSrc`, `iconAlt`, `iconSizeInPercents` | The icon, its alt and its size |
| `iconDisplay` | Object `{ "position": "LEFT" \| "RIGHT" \| "EMPTY" }`. **Not a string** |
| `background`, `border`, `borderRadius` | same as on the other elements |
| `innerSpacing` | The **outer** spacing of the label — that is what the editor calls it. Default is 8 at the bottom; the inner padding is set by `contentSpacing` |
| `themeVariant` | The label variant from the letter styles: `primary` or `secondary` (§8, the `LabelStyle` tag) |
| ~~`visibilityOnDevices`~~ | The label itself does not have it — the converter answers `Unknown attribute`. Only the `<Labels>` group can be hidden per device |

**A label with an empty variable disappears entirely** — not just the chip, but the whole node with its background and icon. This
is the default, nothing needs to be written; in the editor it is the "Display" tab → "If the variables in the element are empty".
`emptyVariableBehavior` changes it: `"hide"` (default), `"show_height_only"` — remove the content but keep
the space, `"show"`. It works at send time; in the preview the label is always visible. On `<FlexRow>` the default is the opposite,
`"show"` (§4).

**The "display filter" is `boolFieldVisibility`.** Showing the label by a boolean custom field, independently of the empty
variable:

```jsx
<Label boolFieldVisibility={{ "enabled": true, "boolField": { "systemName": "<FROM_LOOKUP>", "internalId": "<FROM_LOOKUP>", "fieldFor": "product" }, "mode": { "type": "FILLED", "value": true } }}>Hot</Label>
```

`mode.type` is `FILLED` with `value` (in the editor "Filled and" → yes/no), `FILLED_ANY` ("Filled"),
`NOT_FILLED` ("Not filled"). `fieldFor` is `recipient`, `product`, `productListItem`, `order`,
`orderItem`; `systemName` and `internalId` come from `entities_list(entityType: "CustomField")`; made-up ones
are not rejected at conversion.

**The field must be boolean, and you are the one who checks it.** The lookup row has `valueType` and `isMultiple` —
only `valueType: Bool` with `isMultiple: false` will do. A string field is accepted silently by the converter and the
preview: the condition simply will not fire for the recipient, and there is no way to learn that from the preview. No
suitable field — tell the user, do not substitute a similar one. The condition goes only into the sent email, and only where the field's entity
is in scope: a `product` field works inside a card; in an ordinary column the prop is saved and does
nothing.

### Timer, Video, BulletItem

Do not generate `<Timer>` or `<Video>` without a verified stored schema. `<BulletItem>text</BulletItem>`
works only inside `<BulletList>`.

### Group elements: Menu, BulletList, Socials, Split, Labels

A group is a single element with direct items. It requires at least one item; `visibilityOnDevices` is set only on the group, not on an item. `globalThemeSync` may appear in a JSON fixture, but it is not part of the DSL.

#### Menu

In a menu all items are of one kind: only `<Text>` or only `<Button>`, no mixing.

| Menu attributes |
|---|
| `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` |

#### BulletList

`<BulletList>` contains only `<BulletItem>…</BulletItem>`. `align` on the list is not confirmed and is not part of the DSL.

**Always** set `bulletIcon`: the system default serializes as a `data:` SVG, but the backend does not
escape the quotes inside `src`, the attribute gets cut off, and the marker renders as a giant black circle.
There are two confirmed authored forms:

```jsx
bulletIcon={{ url: "https://cdn.example.com/dot.png", fileName: "dot.png" }}
bulletIcon={{ type: "custom", url: "https://cdn.example.com/one.png", fileName: "one.png", size: 40 }}
```

The flat form renders a small marker 4px wide and is suitable for a dot/circle.
`type: "custom"` + `size` round-trips from the Maestra editor, and the live preview/HTML renders
the actual `size` width; use it for a separately editable numbered badge.
`{{ mode: "static", static: {...} }}` is silently ignored, and a string crashes the preview with
`Internal server error`. All URLs must be confirmed HTTPS assets.

One group applies a shared `bulletIcon` to all items. For different icons 1/2/3,
use a separate BulletList per item, or a standalone fixed-size Image + Text. Do not
draw a structural badge via a styled span inside Text or via Html if it must
be editable in the Maestra editor. A custom marker has one `size` for desktop/mobile,
so visually check mobile; if a separate mobile size is needed, use a
standalone Image with `size.mobile.width`.

| BulletList attributes |
|---|
| `bulletIcon` (always set it; flat 4px dot or a custom `size` badge), `background`, `border`, `borderRadius`, `innerSpacing`, `itemsGap`, `iconTextGap`, `iconTopPadding`, `visibilityOnDevices` |

#### Socials

`<Socials>` contains only `<Image image={{...}} />` items. The URLs below are illustrative;
the source rules are the same as for a regular Image.

| Socials attributes |
|---|
| `background`, `align`, `innerSpacing`, `itemsGap`, `imageSize`, `border`, `borderRadius`, `visibilityOnDevices` |

#### Split

`<Split>` contains only `<Column size={N}>`; the sum of all `size` values is strictly 12. A Split column carries only `size`, contains 0..1 element, and may be empty. Simple elements and groups are allowed inside it, except `<Split>`.

| Split attributes |
|---|
| `columnsGap`, `verticalAlign`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` |

Each group has its own `itemsGap` default — the values are in §6, "Defaults that appear on their own"; specify your own only when a different gap is needed.

## 7. Text — content and inline markup

`<Text>` is two places at once: what is written (with markup) between the tags, and how it looks as a whole (font, size, color, links) — in the `style` attribute.

### Plain text — auto-wrapped in `<p>`

Text without its own markup is written as words:

```jsx
<Text>Summer sale starts today</Text>
```

The converter itself wraps such words in a paragraph: the result becomes `<p style="margin: 0">Summer sale starts today</p>`. Such a paragraph comes back in the same form on read. Auto-wrapping fires only if there is no block tag among the top-level children: if the markup already contains a block element, the converter wraps nothing.

### Full HTML markup

Markup is written as markup, exactly as the email stores it. **Do not rewrite what you did not come to change**: the email wraps text in its own way, and replacing that wrapper edits the email invisibly.

```jsx
<Text>
  <p style="margin: 0;"><span data-rich-text>Inspiring <u>stories</u> of people, </span><a data-rich-link href="https://example.com/stories">read them</a></p>
</Text>
```

**Tags you may use:** paragraphs and headings (`p`, `h1`–`h6`, `blockquote`), lists (`ul`, `ol`, `li`), inline marks (`strong`, `em`, `u`, `s`, `span`, `a`, `code`, `pre`), breaks (`br`, `hr`), and `personalization-parameter`. The live backend rejects `div` and tables (`table`, `thead`, `tbody`, `tr`, `td`, `th`) inside `<Text>` (`<div> is not allowed in a text`) — move table and div layout into `<Html>` as a quoted string (§6). Write explicit JSX void tags self-closing: `<br/>`, `<hr/>`. Do not generate `img`, `iframe`, `script`, `style` without a separate live check. Put an image in `<Image>` standalone or inside `<Socials>`.

**Attributes you may use:** `style`, `align`, `href`, `target`, `rel`, `model`, `data-name`, and the `data-rich-*` markers that the editor sets. Attributes inside rich-text markup are only plain strings or a marker without a value: correct is `<p style="margin: 0;">`, `<a href="https://...">`, `<span data-rich-text>`. Not allowed: `<p style={{ margin: 0 }}>`, spread attributes, expressions — the live backend returns `Attribute \`...\` on <...> must be a plain string`.

### Quoted string in `<Text>` — literal text

A quoted string in `<Text>` is **literal text, not markup**. The live backend escapes it: `<Text>{"<p>One<br>Next</p>"}</Text>` serializes as `<p style="margin: 0"><span data-rich-text>&lt;p&gt;One&lt;br&gt;Next&lt;/p&gt;</span></p>` — the tags become visible text in the email. So write markup only with explicit JSX tags from the allowlist above, and move raw HTML (tables, an unclosed `<br>`, comments, entities) into `<Html>{"…"}</Html>`. Do not mix bare text and a quoted string in one element — live rejects it (`<Text> may only contain text`). The quoted string remains necessary for literal text with special characters (`"`, `{`, `}`, a line break) and for existing personalization (§7).

### `data-rich-*` markers

The markers `data-rich-text` (on `<span>`), `data-rich-link` (on `<a>`), `data-rich-list-item` (on `<li>`) are placed by the converter — **do not write them when creating**. When reading existing text — **leave them in place, do not move them**: a missing marker is restored, but a moved marker is not removed and breaks styling (for example, `data-rich-text` on an `<a>` styles the link both as text and as a link). A marker without a value is stored as `data-rich-text=""`.

### Personalization

New personalization is written with the `<Var>` tag — the rules and the parameter list are in
`references/personalization.md`:

```jsx
<Text><p style="margin: 0;">Hello, <Var param="RecipientGreeting" />!</p></Text>
```

Do not write raw `${...}` template expressions in text: a parameter written as a string will remain literal text.
Preserve existing fragments in that form unchanged, unless the user asked to
rework them:

```jsx
<Text>{"Hello, ${Customer.FirstName}!"}</Text>
```

A chip the converter did not recognize (the parameter is not in this campaign's registry, the model does not
decode) comes back in its stored form — leave it as is:

```jsx
<Text><p style="margin: 0;">Hello, <personalization-parameter model="bm90LWEtbW9kZWw="></personalization-parameter>!</p></Text>
```

#### Unsubscribe link

The unsubscribe link is part of a marketing email by default — the rules for when it is not placed are in `SKILL.md`
§"Unsubscribe link".

A chip cannot be assembled inside an HTML attribute of the markup: the converter escapes `<a href="<personalization-parameter …>">`,
and text goes into the email instead of a parameter. So the href of a text unsubscribe link remains
the exception to the ban on raw `${...}` template expressions: the exact `${Message.UnsubscribeLink}` as the plain-string `href` value
of an `<a>` inside `<Text>`.

In prop values the chip does work, and unsubscribe has its own parameter — `SpecialLinkUnsubscribeLink`; its
expression is exactly `Message.UnsubscribeLink`. That is how an unsubscribe button or clickable image is made:

```jsx
<Button url={[<Var param="SpecialLinkUnsubscribeLink" />]}>Unsubscribe</Button>
```

Correct:

```jsx
<Text>
  <p style="margin: 0;">If you no longer want these emails — <a href="${Message.UnsubscribeLink}">unsubscribe from this mailing list</a></p>
</Text>
```

Incorrect:

```jsx
<Button url="${Message.UnsubscribeLink}">Unsubscribe</Button>
```

```jsx
<Text><p style="margin: 0;">Hello, ${Customer.FirstName}</p></Text>
```

Correct — with the tag: `<Text><p style="margin: 0;">Hello, <Var param="RecipientGreeting" />!</p></Text>`

```jsx
<Text><p style="margin: 0;"><a href="/unsubscribe">Unsubscribe</a></p></Text>
```

The token will not be in the preview HTML: the preview draws the editor's canvas, and in it
every link inside `<Text>` has `href="#"`. This is not a defect and not a reason to replace the token
with a fake URL — the canonical `${Message.UnsubscribeLink}` lives in the JSX, and substitution happens at
send time. Preserve an existing canonical token, its label, and its placement unchanged,
unless the user asked to change the link.

### `style` — typography of the whole text

The `style` attribute holds what the editor's bottom panel edits — it applies to the text as a whole, not to a fragment:

```jsx
<Text style={{ fontSize: 16, color: "#111111", link: { color: "#0000E7", inscription: ["underlined"] }, mobile: { fontSize: 16, align: "left" } }}>
  Styled from end to end
</Text>
```

The same rule as everywhere: write the fields you are changing, the rest stay. If you change
`fontSize` or `align`, set `style.mobile`: without it, the backend may substitute
`{ fontSize: 18, align: "left" }` and break the mobile hierarchy.

Note the two kinds of "bold". `<strong>` inside the markup makes one word bold; `inscription: ["bold"]` in `style` makes the whole text bold. They are stored in different places and do not replace each other.

The `inscription` values are `bold`, `italic`, `underlined`, `crossed`; strikethrough is `crossed`.

## 8. Letter styles

An email has its own set of styles — the letter styles (the editor's Design tab): what a heading looks like, what the primary
button looks like, what background a block has. Do not confuse them with the subject: the subject
is edited via `campaign_edit_content` and has nothing to do with the markup.

### A node either follows the letter styles or has its own look

This is not declared by anything; it is **inferred** from what the node wrote:

```jsx
<Text themeVariant="h1">Summer sale</Text>
<Button url="https://shop.example">Buy</Button>
```

Neither said anything about its look — both follow the letter styles. Name a value
that the letter styles set, and the node is taken off them.

Only what is named from the set counts. Text alignment lives in the same `style` prop as
the typography, but the letter styles do not set alignment — so the heading below stays under them
and is centered at the same time:

```jsx
<Text themeVariant="h1" style={{ align: "center" }}>Summer sale</Text>
```

The letter styles cover only this, and only on these nodes:

| node | what the letter styles cover |
|---|---|
| `Block`, `FlexRow` | `background`, `innerSpacing` |
| `Text`, `BulletItem` | inside `style`: font, size, spacing, color, link styling — not the words and not `align` |
| `Button` | `background`, `border`, `borderRadius`, `buttonSize`, `simpleTextStyles` |

The same name is covered on one node and not on another: a `<Text>` with its own `background`
still takes its typography from the letter styles, because a text's background is not part of the set.

**Nothing said about the look — write no styles.** You are building an email from scratch, there is nothing about this element's
look in the description, the examples or the mockup, and there is no similar element in the email yet — leave it without style
attributes: the look will come from the letter styles and will keep changing with them. A made-up
`fontSize` instead takes the node off the styles and freezes the rest of the set. A similar element already
exists — take the look from it; there is a mockup or a reference — write the styles, the look is stated there. A reference to a neighboring
element ("like the heading above") does not count as a stated look: it is the same case, the look is taken from that
node, and if it follows the letter styles the new one stays empty too. Heading levels
are set by `themeVariant`, not by different numbers.

### Half a set is completed from the letter styles

An unwritten prop reads as "take it from the letter styles", so a node that wrote three out of
five takes the other two from the styles it is leaving — as they were at the moment the document
was read. From then on it keeps them: the node is already detached, and an edit to the styles does not catch up with it.

The reading itself depends on the styles: the same document, read before and after they are edited,
yields nodes with a different look. So the choice is binary: either name nothing from the set — the node
follows the letter styles and their edits — or name the whole set, with values from
`visual_template_theme_get` (Ops). The converter will accept part of a set, but the result is a look nobody
wrote: what you named is yours, the rest is frozen on the styles of that minute.

A short form like `<Text style={{ fontSize: 20 }}>` is legitimate and common: you said
"this text is larger", and the node carried the font and color over from the styles. Just know that from now on they
will not follow the styles, and do not write it that way where the node must change together with the email.

### `themeVariant`

Says which variant the node is assigned to: `h1`, `h2`, `h3`, `text` for text, `primary` or
`secondary` for a button. A block and a row have a single variant, and it is not written. Only a
variant different from the default one is written.

**The names are not interchangeable.** On a node the attribute is called `themeVariant`, inside `<Theme>` —
`variant`. The converter rejects `variant` on a node and `themeVariant` inside `<Theme>` as an
unknown attribute, and that does not mean there is no way to assign the node to a variant: it means
the wrong name was taken.

```jsx
<Theme><TextStyle variant="h1" simpleTextStyles={{ fontSize: 32 }} /></Theme>
<Text themeVariant="h1">Summer sale</Text>
```

The presence of a variant says nothing about whether the node follows the letter styles: those are read from
different places.

### Editing the letter styles themselves — `<Theme>`

Written once, directly inside `<Template>`, before the blocks, one tag per kind of style:

```jsx
<Template>
  <Theme>
    <TextStyle variant="h1" simpleTextStyles={{ fontSize: 32, inscription: ["bold"] }} />
    <ButtonStyle variant="primary" background={{ type: "color", value: "#ff6600" }} />
  </Theme>
  <Block><FlexRow><Column size={12}><Text>Body</Text></Column></FlexRow></Block>
</Template>
```

It reads as a patch: what is named replaces the email's value, what is not named stays as it was.
Completeness of the set is **not required** here — that rule is about nodes, not about styles.

| tag | variants | props |
|---|---|---|
| `BlockStyle`, `RowStyle` | one, `variant` is not written | `background`, `innerSpacing` |
| `TextStyle` | `h1`, `h2`, `h3`, `text` | `simpleTextStyles` |
| `ButtonStyle` | `primary`, `secondary` | `background`, `border`, `borderRadius`, `buttonSize`, `simpleTextStyles` |
| `LabelStyle` | `primary`, `secondary` | same as `ButtonStyle`, but `contentSpacing` instead of `buttonSize` |

The typography inside `<TextStyle>` is called `simpleTextStyles`, while on `<Text>` itself the same
set is called `style`. The name in the style set and the name on the node do not always match — check against
this table and the table above, not from memory.

**Inside a style write only the fields that are present in the fragment from `visual_template_theme_get`** —
it is the complete list of what the styles set. Fields outside it the letter styles cannot provide:
the converter will reject such a record rather than accept it silently. Most often this is attempted with
alignment — it is not in the set, it lives on the node:

```jsx
<Theme><TextStyle variant="h2" simpleTextStyles={{ fontSize: 14, color: "#3C4043" }} /></Theme>
<Text themeVariant="h2" style={{ align: "right" }}>Gmail</Text>
```

`LabelStyle` is the letter styles for `<Label>` labels; it arrives in the fragment from `visual_template_theme_get`.
Insert it together with the rest.

Editing a letter style changes **all** nodes that follow it, including those the document did not
touch. So change the letter styles only on an explicit request — "make the buttons orange throughout
the email", not "make this button orange".

Reading an email does not return `<Theme>`: the document carries it only when it changes something.
Ask `visual_template_theme_get` for the effective values — it returns a ready fragment
in exactly this form. Pass it the current document: otherwise the answer will not account for a not-yet-saved
`<Theme>`, and replacing the tag with such an answer will erase the edits.

### Moving styles from nodes into `<Theme>`

The request "move the styles into the letter styles" is three actions in one document:

1. write the values into `<Theme>`;
2. **remove** those styles from the nodes that go under them;
3. assign `themeVariant` where the variant is not the default.

Skipping the second is the most common mistake, and it is invisible: the look will not drift, the preview will show nothing, and
the letter styles will turn out to be applied to nothing. The user finds out on their first edit of the styles.

**The look after the move matches the previous one pixel for pixel.** Hence:

- **there is a finite number of variants** — text `h1`/`h2`/`h3`/`text`, button and label
  `primary`/`secondary`, block and row one each. Different values are not merged into one variant;
- **values are not adjusted**: 12px stays 12px, no rounding, no "almost the same";
- **a different mobile size is a different look**, even if the desktop one matches;
- **more looks than variants** — name it as a number and leave the extra ones unique: "found six
  text sizes, there are four variants; I will move the four most frequent and leave two unique — they are in
  the footer". Pulling a look toward the nearest variant is not allowed;
- **alignment stays on the node** — it is not part of the set and is not removed from the node during the move.

**The mobile side moves along with the rest.** The letter-styles set holds it, and in two forms:
nested (`mobile: { height: 48 }`) and as a flat sibling field (`widthMobile`). Both are written inside
`<ButtonStyle>` / `<TextStyle>` on a par with the desktop value. So "the letter styles do not store
a separate mobile button height" is not a limitation but an unwritten field: look in the
`visual_template_theme_get` fragment at what the set defines, and move over everything the node had.

**But the mobile values live in the variant itself, not on the node:** all buttons on `primary` have the same mobile
height, from the styles. So a node that needs something other than the variant on mobile will not keep
that under the letter styles — for a button, label, block and row the prop comes from the
styles whole, mobile part included. Text is different: of the mobile side, the styles set only the font
size; the rest of the mobile values stays on the node.

Such a node is not moved silently: name the element and the difference, and ask whether it is acceptable for it to follow the letter
styles on mobile. Yes — it goes along with the rest and the difference disappears; no — it stays
unique. Rewriting the variant for the sake of one node is not allowed: all nodes of the variant would get the new values.

**A look that drifted after the move is always an incomplete set, not a platform limit.** Do not explain
the shift by the latter: either write in the missing side, or leave that node unique and say that it did not
move and why.

This is verified by values, not by a picture: for every node you took the styles off, the set from the variant
matches the removed one field by field. Before the move the values are written in the document; after it, in the
`visual_template_theme_get` fragment. The preview is the second step: a one-pixel shift and an extra line break are not always
visible in a snapshot.

### An email without letter styles of its own

Every email has effective styles; not every email has its own. One that has not set them up takes
the platform styles and stays that way: reading and saving do not turn them into its own styles,
frozen at today's values. The tool says so directly — do not relay the platform values to the
user as the design of their email.

## 9. URL

`Button.url` accepts `https://`, `tel:`, and `mailto:`; the backend validates the format and rejects
survey links. Write a simple link as a string: `url="https://shop.example"`; a URL with
special characters (`&`, `=`, quotes) — as a JSON string in an expression:
`url={"https://shop.example/?from=email&utm=sale"}`.

## 10. What the serializer adds itself

All service fields of the JSON (UUID, envelope, subject, targeting, sampling, materialization, etc.) are added by the serializer automatically. You only need what is listed in §4–§6: tags, hierarchy, column `size`, and element attributes.

The email settings — width, background, "Global (CSS) styles", the Gmail annotation — and the letter styles are **carried over from the previous version of the email** on save. Those the document does not name stay as they were; width and background can be named with the root attributes (§4), the letter styles with the `<Theme>` tag (§8). The other two settings are not reachable from the markup and change only in the editor.

## 11. Runtime validation and self-check

The backend checks the structure, the tag/attribute allowlist, literal-only values, the grid,
group composition, Button URL, and the allowed content of leaf elements. Report an error as
stage + status/code + a short message; the full response body is needed only for separate diagnostics.

The Generator itself additionally checks policy that the backend does not guarantee:

- a static Image URL is confirmed by the user or Ops and uses HTTPS; a personal image has no made-up domain prefix;
- no bare Image, no fake unsubscribe; every tenant-specific `systemName` in `<Var>` came from a lookup or from the user;
- colors are written as `#RRGGBB`, numeric values are reasonable;
- if a desktop `style.fontSize`/`style.align` or `simpleTextStyles.fontSize` is set, the mobile branch is set deliberately;
- device variants and mobile ordering match the request;
- the JSX contains no comments, imports, or executable expressions.

## 12. Product rows — `<CollectionRow>`

A block has a second kind of row: it holds product cards rather than columns, and draws the card once per
product from the mechanic — recommendations, order products, the cart, the project's product list.

```
Template  →  Block  →  CollectionRow  →  CardTemplate | CollectionCard  →  Column  →  element
```

**The full rules are in [product-rows.md](./product-rows.md), and it must be opened before generating an email with
products.** The row cannot be assembled from memory: which chips are allowed is decided by the mechanic; the mechanic has
required settings, and a successful preview/save does not prove they are filled in; the grid requires an orientation;
manually selected products are named by identifiers, which are not invented.
