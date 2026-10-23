---
description: "The text block: the three forms of its content, the editor's markup vocabulary, the data-rich-* markers, one size and one font per block, what style adds to the letter-styles typography, the defaults"
---

# Text — `<Text>`

A text is two things written in two places: what it says, with its markup, between the tags; how it looks as a
whole in the `style` attribute.

## Content

| form | written as | what the converter does |
|---|---|---|
| plain words | `<Text>Summer sale starts today</Text>` | wraps them in `<p style="margin: 0">` and marks the run with `data-rich-text` |
| markup | `<Text><p style="margin: 0;">Summer <strong>sale</strong></p></Text>` | stores it as written, adding the markers; inline-only markup (`Hi <strong>there</strong>`) is wrapped in the paragraph like plain words |
| quoted string | `<Text>{"Code: &lt;SALE20&gt; {braces}"}</Text>` | stores the characters as written, escaped, so the editor shows `<SALE20>` as words; the sent email decodes entities once on output, so in the sent email `<…>` written in the string acts as a tag, and `&lt;`/`&gt;` are the way to show brackets |

A quoted string is for words JSX would read as its own syntax (`{`, `}`, `"`, `<`, a line break) and for carrying over
existing personalization; markup goes in as JSX tags. A bare `&` passes as itself everywhere. Plain words behave the
same way at the end: `<Text>&lt;SALE20&gt;</Text>` is decoded by JSX, stored escaped, and decoded again on output,
so it reaches the recipient as a tag; a bracket the recipient must see is `&lt;` inside a quoted string.

### Markup vocabulary

The converter admits exactly what the editor's text tool can produce. Anything else is refused with the tag's
name: `<div> is not allowed in a text`, `<img> is not allowed in a text`.

| | tags |
|---|---|
| blocks | `p`, `h1`–`h6`, `blockquote`, `ul`, `ol`, `li`, `pre`, `hr` — `ul`/`ol` is a list inside the text; a list with its own icon is the `<BulletList>` element |
| inline | `strong`, `em`, `u`, `s`, `code`, `br`, `a`, `span` — `s` adds no CSS of its own and relies on the mail client; a struck-through whole text is `inscription: ["crossed"]` |
| chip | `<Var>` when writing; `personalization-parameter` is its stored form in a read email |

Not admitted: `div`, `table` and its parts, `img`, `iframe`, `script`, `style`. A table goes into `<Html>`, a
picture into `<Image>`. Void tags are written self-closing: `<br/>`, `<hr/>`.

| attributes | where the editor puts them (the converter refuses only `class` outside `a`) |
|---|---|
| `style`, `align` | any tag |
| `href`, `target`, `rel`, `data-name`, `class` | `a` |
| `data-color` | `span`, beside the `style` that colours it |
| `start` | `ol` |
| `model` | `personalization-parameter`, the stored chip of a read email — carried over as is |
| `data-rich-text`, `data-rich-link`, `data-rich-list-item` | the markers, see below |

An attribute inside markup is a plain string or a bare marker: `<p style="margin: 0;">`, `<span data-rich-text>`.
An expression (`style={{ margin: 0 }}`) is refused: ``Attribute `style` on <p> must be a plain string``.

### The `data-rich-*` markers

`data-rich-text` on a `<span>`, `data-rich-link` on an `<a>`, `data-rich-list-item` on an `<li>`: the hooks the
`style` attribute is applied to. New text — do not write them, the converter adds them. A read email — leave
them where they are: a missing marker is restored, a moved one is kept and styles the wrong node (a `data-rich-text`
on an `<a>` styles the link as text and as a link at once) without an error.

## `style`

The typography of the whole text, what the editor's bottom panel edits. `<strong>` inside the markup bolds a
word; `inscription: ["bold"]` in `style` bolds the text. The fields, the font lists and `inscription` values are
shared with `simpleTextStyles` — [typography.md](typography.md). `Text.style` adds:

| field | value | note |
|---|---|---|
| `align` | `"left"` \| `"center"` \| `"right"` \| `"justify"` | `align`, `fontSize`, `color` are not attributes of `<Text>`: they live inside `style` |
| `link` | `{ color, inscription }` | the look of `<a>` inside the text, apart from the words |
| `mobile.align` | as `align` | next to `mobile.fontSize`; without `mobile` the phone shows the desktop alignment |

A text whose mockup names the font, size, colour, link look and alignment:

```jsx
style={{ font: { family: "Montserrat" }, fallbackFontFamily: "Verdana", fontSize: 16, color: "#111111",
  link: { color: "#0000E7", inscription: ["underlined"] }, align: "center", mobile: { fontSize: 14, align: "left" } }}
```

## One size and one font per text

In the editor the style of a text block applies to the whole block, so text of different sizes or fonts in one block
cannot be adjusted separately. A heading is always its own `<Text>`, and so is any line that differs from its
neighbours in size or font: a subheading, a caption, fine print. Set the heading level with `themeVariant`; an
`h1`–`h6` tag carried over from a source stays the only content of its `<Text>`, never a line next to a `<p>`. Do not
change the size or the font with a `<span style="font-size: …">` or `font-family`. Everything that keeps the size and
the font stays inside one block — bold, italics, underline, strikethrough, a link, the colour of a word, a
personalization chip, a line break, a list.

```jsx
<Column size={12}>
  <Text themeVariant="h2" innerSpacing={{ top: 10, bottom: 4 }}>Last day of the sale</Text>
  <Text innerSpacing={{ top: 4, bottom: 10 }}><p style="margin: 0;">Save <strong>20%</strong> on everything before midnight.</p></Text>
</Column>
```

A source that keeps a heading and a paragraph in one section — a text block from Klaviyo or another email platform,
an HTML cell, a block of a mockup — is split the same way: a `<Text>` per size or font, one under another. A `<Split>`
column holds one element ([containers.md](containers.md)), so when such text sits side by side with something else,
build that part as its own `FlexRow` with ordinary `Column`s instead of a `<Split>`: a `Column` holds any number of
elements. The gap between them is the sum of their own `innerSpacing`; match it to the source by lowering the
heading's `bottom` and the paragraph's `top`.

The rule applies to text you write or carry over. Do not restructure existing text that the request does not touch,
a library block or a `<QuokkaBlock>`; if an existing block mixes sizes and the user is editing it, name it and offer
the split.

## Two values in one text

Two `<Var>` in one `<Text>` are one cell: the values cannot be separated by look or by empty-value behaviour, and in
the editor they are edited only together. Price and old price, price and discount, name and SKU are kept as separate
elements: a price beside its old price is two elements in a `<Split>`, the old one `inscription: ["crossed"]`
([containers.md](containers.md)); one `<Text>` with a struck-through span is a simplification, and it is named to the
user as one.

## Attributes of the element

| attribute | value | when absent | written in part, the fields left out |
|---|---|---|---|
| `style` | see above | letter styles ([theme.md](theme.md)) | the same |
| `themeVariant` | `"h1"` \| `"h2"` \| `"h3"` \| `"text"` — which set of the email's letter styles the text follows ([theme.md](theme.md)) | `"text"` | — |
| `innerSpacing` | as for `Block` | `{ top: 10, bottom: 10, left: 0, right: 0 }` | the same |
| `background` | as for `Block` | `{ type: "transparent" }` | the same |
| `border` | as for `Block` | `{ type: "none" }` | the same |
| `borderRadius` | as for `Block` | 0 | the same |
| `emptyVariableBehavior` | as on any element with a chip — [personalization.md](personalization.md) | `"hide"` | — |

Plus `visibilityOnDevices`, as on any element. Inside a product row card a text may also carry `url` and `height` —
[product-rows.md](product-rows.md).

On the canvas every `<a>` inside `<Text>` is `href="#"`; the sent email keeps the written address — [canvas.md](canvas.md).
