---
description: "Labels in a product row card: the Labels group and its Label lines, content with a chip, attributes and defaults, the boolean-field visibility, what the converter lets through that the editor does not have"
---

# Labels — `<Labels>` and `<Label>`

A label is short text on a rounded background with an optional icon: "New", "−20%", "Bestseller". Labels come as a
group, `<Labels>`, whose lines are `<Label>` elements.

**Labels live only inside a product row card.** The rule is the editor's canvas: it offers `Labels` only inside a
card and refuses to drop them anywhere else. The converter does not check it: it accepts `<Labels>` in an ordinary
column, and even a `<Label>` outside `<Labels>`, and the preview draws both. So a successful preview proves
nothing here: a label in an ordinary row is a node the editor cannot show. A badge in a regular section is a
`<Text>` with its own `background`, `borderRadius` and `innerSpacing` in a narrow column: the background fills the
column's width, so the column's `size` is the badge's width, and the row carries `isColumnsMobileAdaptive={false}`
— otherwise the column stacks on the phone and the badge becomes a strip of the full width. Inside a card or a
synchronized row, where the row cannot change, the badge is the second column of a `<Split>` beside the name: a split never stacks. A `<Menu>` line holds
nothing beside its words: the word goes into the line itself («Delivery · new»), or the menu is laid out as columns of `<Text>`.

```jsx
<FlexRow isColumnsMobileAdaptive={false} columnsGap={{ size: 8 }} verticalAlign={{ align: "middle" }}>
  <Column size={9}><Text>Delivery</Text></Column>
  <Column size={3}><Text background={{ type: "color", value: "#E53935" }} borderRadius={{ topLeft: 8, topRight: 8, bottomLeft: 8, bottomRight: 8 }} innerSpacing={{ top: 2, bottom: 2, left: 6, right: 6 }} style={{ fontSize: 11, color: "#FFFFFF", align: "center" }}>new</Text></Column>
</FlexRow>
```

```jsx
<Labels itemsGap={{ size: 8 }}>
  <Label>New</Label>
  <Label themeVariant="secondary">{["−", <Var param="ProductDiscount" discountSettings={{ "format": "percent" }} affixVariableText={{ "aroundText": { "before": "", "after": "%" } }} />]}</Label>
  <Label iconDisplay={{ position: "LEFT" }} iconSrc={{ url: "https://cdn.shop.example/fire.png", fileName: "fire.png" }}>Hit</Label>
</Labels>
```

## Content

The caption is a plain string, as on `<Button>`: words between the tags, a quoted string `{"…"}` when the words
hold `{` or `}`, and a chip as a list of segments — a discount chip: [personalization.md](personalization.md),
"What a chip prints on its own". No markup inside.

## Attributes of `<Labels>`

| attribute | value | default |
|---|---|---|
| `align` | `{ align: "left" \| "center" \| "right", mobile: { align } }` | `{ align: "left" }` |
| `itemsGap` | `{ size: N, mobile: { size: N } }` — the space between labels | `{ size: 8 }` |
| `innerSpacing` | as for `Block` | 0 on all sides |
| `background`, `border`, `borderRadius` | as for `Block` | transparent, none, 0 |
| `visibilityOnDevices` | `"all"` \| `"desktop"` \| `"mobile"` | `"all"` |

Children — only `<Label>`.

## Attributes of `<Label>`

| attribute | value | when absent | written in part, the fields left out |
|---|---|---|---|
| `themeVariant` | `"primary"` \| `"secondary"` — which set of the email's letter styles the label follows ([theme.md](theme.md)) | `"primary"` | — |
| `url` | a string, as on `<Button>`; inside a card the product link is the chip ([product-rows.md](product-rows.md)) | empty link | — |
| `background` | as for `Block` | letter styles | the same |
| `border` | as for `Block` | letter styles | the same |
| `borderRadius` | as for `Block` | letter styles | the same |
| `contentSpacing` | `{ top, bottom, left, right }` — the padding inside the label, around the words | letter styles | the same |
| `simpleTextStyles` | the letter-styles typography fields — [typography.md](typography.md) | letter styles | the same |
| `innerSpacing` | as for `Block` — the **outer** space around the label, what the editor calls it | `{ top: 0, bottom: 8, left: 0, right: 0 }` | the same |
| `iconDisplay` | `{ position: "LEFT" \| "RIGHT" \| "EMPTY" }` — an object, a bare string is refused | `{ position: "EMPTY" }` | — |
| `iconSrc` | `{ url, fileName }` — a gallery image, like any image source | a platform placeholder, hidden while `iconDisplay` is `EMPTY` | — |
| `iconAlt` | string | empty | — |
| `iconSizeInPercents` | `{ widthInPercents: N }` — the icon's share of the label width | `{ widthInPercents: 25 }` | the same |
| `visibilityOnDevices` | as on the group; works on a single line | `"all"` | — |
| `emptyVariableBehavior` | as on any element — [personalization.md](personalization.md) | `"hide"` | — |
| `boolFieldVisibility` | below | `{ enabled: false }` | — |

"letter styles": from the email's styles for the `themeVariant`, frozen once the node has a look of its own
([theme.md](theme.md)).

## "Boolean field filter" — `boolFieldVisibility`

Shows the label by a boolean custom field, separately from an empty variable. In the editor: the "Boolean field
filter" section.

```jsx
<Label boolFieldVisibility={{ "enabled": true, "boolField": { "systemName": "<FROM_LOOKUP>", "internalId": "<FROM_LOOKUP>", "fieldFor": "product" }, "mode": { "type": "FILLED", "value": true } }}>Hit</Label>
```

`mode.type` — `FILLED` with `value` (in the editor "Filled and" → yes/no), `FILLED_ANY` ("Filled and
any"), `NOT_FILLED` ("Not filled"). `fieldFor` — `recipient`, `product`,
`productListItem`, `order`, `orderItem`; `systemName` and `internalId` come from
the lookup of entity `CustomField`; invented ones are not rejected on conversion.

**The field must be boolean.** The lookup row has `valueType` and `isMultiple` — only
`valueType: Bool` with `isMultiple: false` fits. The converter and the preview accept a string field silently: the
condition simply does not work for the recipient, and the preview cannot tell. The condition goes only into the sent email and works only where the
field's entity is in scope: a `product` field works inside a card.
