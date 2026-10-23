---
description: "A block rendered by an editor template, <QuokkaBlock>: where it comes from, what is carried over as is, how a setting is changed through the template's description, the value shape of every setting type, <Collection> and <Item>, dataSource and count, layout attributes, what is never invented"
---

# A block rendered by an editor template — `<QuokkaBlock>`

Not every block is laid out in the document. The editor has block templates whose layout lives in the template
itself; the email holds only a reference to it and the values the author changed. Such a block comes as
`<QuokkaBlock>` directly in `<Template>`, next to ordinary `<Block>` elements:

```jsx
<Template>
  <Block><FlexRow><Column size={12}><Text>Header</Text></Column></FlexRow></Block>
  <QuokkaBlock templateId="0f8fad5b-d9cb-469f-a165-70867728950e" accent="#FF0000">
    <Collection name="items" dataSource={{ "key": "ORDER" }} count={3} />
  </QuokkaBlock>
</Template>
```

**Where it comes from.** Only from an email that was read, or from the library: a library block of `kind`
`quokka` reads back as this tag, `templateId` included. A new `<QuokkaBlock>` cannot be
built from scratch — you do not have the template it would refer to.

**`templateId` is never invented.** It is the template's identifier, not its name. An identifier the project
does not have is rejected on preview and on save with that identifier named.

**It is edited through its settings, not through its markup.** Having read the email, return the block as it
came, except what you were asked to change. The block can be deleted as a whole or moved between blocks; the other
blocks of the email are edited as usual meanwhile.

## Changing a setting

The template's description, read by the block's `templateId`, gives every setting the
template has — the attribute's name, its **type** and its group — and the template's markup, which shows where
each attribute lands: match the spot the person named by that markup, two attributes of the same type that could both be it
cannot be told apart from the JSX alone. Write the attribute **onto the tag that already stands in the email**. Nothing in the answer belongs to that
spot — the template does not hand that setting over, and only changing the template itself would; it cannot be done from the email.

The name is opaque (`prop_SIMPLE_TEXT_6_23`), so the type says which shape the value takes — the table below. A
name the template does not know is rejected. Values equal to the template's are not printed, so the block that
was read does not show all of its settings: add the one you were asked about, do not restore the rest.

**Partial merge** works as for any node — the object is completed from defaults — with two differences: the default
a value merges onto is the template's, not a new node's, and what the email prints is already the difference — a
field that is not there is the template's, not empty. A field written in another kind, a number where an object
belongs, is refused by the converter, which names it.

Besides the template's settings, the block takes what every block takes: `visibilityOnDevices` and `gapAfterBlock`
as on a `<Block>`, and `targeting` comes over as it came ([containers.md](containers.md)).

### Value shape by setting type

Types whose shape is that of an ordinary attribute:

| type | shape |
|---|---|
| `ALIGN` | `{ align: "left" \| "center" \| "right" }` — [button.md](button.md) |
| `ALT`, `SIMPLE_TEXT` | a plain string |
| `BACKGROUND` | [containers.md](containers.md), `Block`; an image background is `{ type: "image", url, fileName }` |
| `BORDER` | [containers.md](containers.md), `Block` |
| `BORDER_RADIUS` | [containers.md](containers.md), `Block` |
| `BUTTON_SIZE` | [button.md](button.md) |
| `COLOR` | `"#RRGGBB"` |
| `GAP` | [containers.md](containers.md), `columnsGap` |
| `IMAGE` | [image.md](image.md), `image` |
| `INNER_SPACING` | [containers.md](containers.md), `Block` |
| `SIMPLE_TEXT_STYLES` | [typography.md](typography.md) |
| `TEXT_STYLES` | [typography.md](typography.md), [text.md](text.md) |
| `URL` | the address itself as a string |
| `VERTICAL_ALIGN` | [containers.md](containers.md), `FlexRow` |

Types whose shape exists only here:

| type | shape |
|---|---|
| `ABSOLUTE_SIZE` | `{ size: N }` |
| `CONTENT_DIRECTION` | `{ direction: "ltr" \| "rtl" }` |
| `DISPLAY_TOGGLE` | `{ isDisplayed: true \| false }` |
| `GRID_SIZE` | `{ rowCount: N, columnCount: N }` |
| `HEIGHT` | `{ height: N \| "auto", autosizeKey: "…" }` |
| `HEIGHTV2` | `{ settingType: "manual" \| …, height: N, autosizeKey: "…", mobile: { height: N } }` |
| `ICON` | `{ url: "<HTTPS URL>", fileName: "…" }` |
| `ICON_DISPLAY` | `{ position: "EMPTY" \| … }` |
| `IS_MOBILE_ADAPTIVE_ENABLED`, `VISIBILITY_TOGGLE` | `true` \| `false`, no wrapper |
| `NUMBER` | `{ number: N }` |
| `PADDINGS` | `{ vertical: N, horizontal: N }` |
| `PRICE` | `{ text: "…", currency: "$" }` — `text` is markup, [text.md](text.md) |
| `SIZE` | `{ type: "inherit" \| …, width: N, equalizedImageMaxWidth: "…", mobile: { … } }` |
| `SIZE_IN_PERCENTS` | `{ widthInPercents: N }` |
| `TEXT` | `{ text: "<p>…</p>" }` — markup, [text.md](text.md) |
| `TEXT_SIZE` | `{ containerHeight: N, containerHeightMobile: N }` |
| `TIMER`, `VIDEO` | a large settings object this page does not spell out: change a field the email already prints, otherwise the setting is changed in the editor |
| `VERTICAL_SPACING` | `{ top: N, bottom: N }` |

## `<Collection>` and `<Item>`

**Only `<Collection>` fits between the tags, and inside it only `<Item>`** — the layout lives in the template. The
card of the collection and its chips are the template's, so the rules of [product-rows.md](product-rows.md)
about them do not apply here: the converter re-points the template's chips at whatever mechanic the collection
has, and none is written by hand ([personalization.md](personalization.md)). An `<Item>` takes no children: a
position states its settings as attributes.

**A collection always states how many positions it has**, in one of three ways:

- `count={N}` with no children — that many positions, as the template renders them;
- `count={N}` and exactly one `<Item>` — that many positions, all from this card;
- a list of `<Item>` without `count` — one position per element, each its own.

`count` is a whole number, zero or more. `count={0}` is a collection the author emptied, and only
`ProductShowcase`, `ContentShowcase` and `TopicsShowcase` can be: every other mechanic finds the positions itself,
needs at least one, and refuses the whole email without it. An emptied `ProductShowcase` is the one case where it
carries `count`: filled, it has one `<Item>` per product and no `count` at all. A missing `<Collection>` means
"as in the template".

**The form follows the positions, so do not rewrite it to tidy it up.** An edit that makes the positions differ
writes each of them out as its own `<Item>` and drops `count` — while `count` stands, every position takes the
attributes of the first `<Item>`. An edit that applies to all of them stays in the single `<Item>` and keeps
`count`; without it one position is left of the collection. The preview draws both losses without an error.

**An attribute standing on an `<Item>` does not move** when the mechanic changes — it is kept as written, so a
card spelled out by hand goes on naming the old mechanic's fields, silently. A position that was only repeating
the template is better given back to it: drop the `<Item>`.

## `dataSource` — the collection's product source

It stands in the email and can be changed. `dataSource` is written on every `<Collection>` the converter prints;
`Empty` is the mechanic meaning none has been chosen, and it still wants a position. **Write the attribute back on
every collection you write, changed or not:** without it the collection falls back to the template's default
source, usually `Empty`, and draws nothing, and the email saves without an error. The tool answers for the template's own settings; `dataSource` is
not among them and is read off the email.

- **Not asked to change it** — carry it over exactly as read. Asked to change one of its settings, change that
  field and leave the rest standing: beside `key` a mechanic carries fields the settings table does not list
  (`showAllPositionsSetting` on `ORDER`, `emptyConditionSetting` on most product mechanics), and rebuilding the
  attribute from the table drops them silently.
- **Asked to replace it** — write the mechanic anew by all the rules of [product-rows.md](product-rows.md).
- **It arrived incomplete** — its required setting never filled in the editor, and the converter refuses the email
  over an attribute nobody asked about (`needs a value in …`). Do not complete it from a lookup — that points the
  block at a source its author never chose. The source is the author's choice.
- **`ContentShowcase` and `TopicsShowcase`** draw content rather than products. On a collection of their own they
  are written back like any other mechanic. They cannot move: neither onto a collection of products, nor one in
  place of the other, and a collection of theirs takes no other key — each refuses the whole email.
- **A manual product selection** (`dataSource={{ "key": "ProductShowcase" }}`) holds one `<Item product={…}>` per
  product and no `count` — the products are the count; the triple exactly as for `<CollectionCard>`
  ([product-rows.md](product-rows.md)). For a position of any other mechanic `product` is rejected: the mechanic
  finds the products itself.

## Layout attributes

`columns`, `isAdaptive`, `columnsSpacing`, `rowsSpacing`, `columnsDivider`, `rowsDivider`, `containerWidth` exist
only on collections whose templates handed the grid over to the editor. The converter prints them; preserve them as
is and do not add them — a template that renders the grid itself rejects such attributes, and one that hands over
only some of them rejects each of the rest by name.

## What the DSL does not write at all

Positions selected by topics, except an empty collection: the converter rejects an email with such a block. This
is not a reason to fix it by hand — pass the rejection on verbatim.
