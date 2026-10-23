---
description: "The <Var> chip: its form, where it stands, which settings come from a lookup, what it prints on its own, empty values, formatString, the common parameters, the two backend errors that do not name their cause"
---

# Personalization — `<Var>`

`param` is the parameter name; the other attributes are its settings, formatters and affixes, and only the changed
ones are written — every part has a default. The converter builds the editor's own chip from the tag, so it opens
and is edited in the editor as usual. An attribute the parameter does not have is a converter error naming it. A raw template
string already in a read email (`<Text>{"Hello, ${Customer.FirstName}!"}</Text>`) stays as it came unless the user asked to redo it.

```jsx
<Text><p style="margin: 0;">Your promo code: <Var param="PromoCodeValue" promoCodePool={{ "systemName": "<FROM_LOOKUP>", "name": "<FROM_LOOKUP>", "internalId": "<FROM_LOOKUP>" }} caseFormatter={{ "format": "uppercase" }} /></p></Text>
```

A chip that prints a sign or a word itself — the greeting, the bonus word, the currency sign — must not get the same
sign or word from you again: "What a chip prints on its own".

## Where a chip stands

| where | form |
|---|---|
| in text — `<Text>`, `<BulletItem>` | inside the markup, as above |
| in a value string — a link, button words, a label's caption | a list of segments: `url={["https://shop.example/sale?promo=", <Var param="PromoCodeValue" promoCodePool={{ … }} />]}`, `<Button>{["Redeem ", <Var … />, " points"]}</Button>`; a list only where there is a chip |
| in a label — `<Label>` caption | the same list; a discount chip takes `percent` and the `%` affix — "What a chip prints on its own" |
| inside a structure, at any depth — a personal image | `<Image image={{ "mode": "dynamic", "dynamic": [<Var param="RecipientCustomFieldString" customFieldType={{ … }} />] }} />` |

## Settings from a lookup

A setting that names a project reference list takes a real name from one row of the lookup of the entity named below.

| setting | entity | parameters |
|---|---|---|
| `promoCodePool` | `PromoCodePool` — only single-use and referral pools work in a chip, and a pool without a system name cannot be built | `PromoCodeValue`, `PromoCodeExpirationDateTime`, the `discountQuery` setting |
| `customFieldType` | `CustomField`, its owner by the parameter's suffix: `Customer` for `Recipient*`, `Order` for `Order*CustomField*`, `Product` for `…ProductCustomField*` and `Product*`, `ProductListItem` / `OrderLine` for `…ItemCustomField*` | all `*CustomField*` |
| `balance` | `Balance` | `RecipientBonusBalance`, `RecipientNearestExpirationBonuses*` |
| `externalSystem` | `ExternalSystem` — the project's integrations | `ProductExternalId` and related, `*AddToCartUrl` |
| `orderExternalIdSelection` | `CustomField` owned by `OrderExternalId` — not `ExternalSystem`: an integration name here passes the converter and fails on the campaign card | `OrderExternalId` |
| `productListSystemName` + `productListInternalId` | `ProductList`, both from one row | product row mechanics with a list |
| `recoMechanicSystemName` | `RecommendationMechanic` | product row recommendation mechanics |
| `product` | `Product` | the manual card `ProductShowcase` |

Carry `systemName`, `name` and `internalId` (and `type` for a custom field) into the JSX as the row returned them: `systemName` goes into the
expression, `name` draws the chip on the canvas, `internalId` is harmless. A chip with an empty setting is a broken email, not a draft. Values are also
required by `hostname` on `*AddToCartUrl` (the store's domain, asked from the user), `discountQuery` when enabled,
`amount` when written (greater than zero), and `affixVariableText` when `emptyBehavior.mode` is `fallback`.

## A custom field

The `param` follows the lookup row: `valueType` `String`, `Integer`, `Decimal`, `Date`, `DateTimeUtc` (→ `DateTime`) or `Enum`
names the parameter `…CustomField<Type>`; any other `valueType` has no chip. The owner picks the family — `Recipient*`, `Order*`, in a row
`…ItemCustomField*` for the row's own field and `…ItemProductCustomField*` for the product's
([product-parameters.md](./product-parameters.md)). `Identifier` exists for the customer only; `Bool`,
`TechnicalIdentity` and any field with `isMultiple: true` have no chip — a boolean field shows or hides a label
instead (`wiki/label.md`, `boolFieldVisibility`).

```jsx
<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "WalletCardLink", "type": "String", "name": "Wallet card link", "internalId": "<FROM_LOOKUP>" }} />
```

`type` is written from the row's `valueType`: the converter does not derive it from `param` and stores `Date` when it
is left out — the sent email is unaffected, the editor may show the field with the wrong type. Nothing found — ask
the user and try the other owner before concluding the field does not exist; the lookup matches a fragment of the name.

## What a chip prints on its own

Every chip takes `affixVariableText`; for most parameters its default is empty. A few print a sign or a word
themselves — do not write it again next to the chip: `<Var param="ProductPrice" /> $` with the $ affix is sent as
"$1,234 $". The preview draws the chip's own sign and `%`, but not always your `aroundText`; the JSX is what is sent, the
sample is not.

| parameters | printed by default | to change it |
|---|---|---|
| prices and amounts — every parameter with `formatDecimalPrice`: `*Price`, `*OldPrice`, `*PriceOfLine`, `*Amount`, `OrderDeliveryCost`, `OrderItem*PricePerUnit` | the project's currency sign — after the number or before it, by the project's locale | `affixVariableText={{ "aroundText": { "before": "…", "after": "…" } }}` — it replaces the default whole, so `before` alone drops the sign: repeat the sign in `after`, or put the word outside the chip (`from <Var … />`) and keep the default |
| discounts — every parameter with `discountSettings` | the same currency sign: `format` is `absolute` by default, and the sign is the affix, not part of the format | `discountSettings={{ "format": "percent" }}` **together with** `affixVariableText={{ "aroundText": { "before": "", "after": "%" } }}`; `percent` alone changes only the number and the badge reads "$14.56" |
| `RecipientGreeting` | the whole phrase, "Hello, Anna!", and "Hello!" for a customer without a name — in the project's language | `affixVariableText`, both blocks: `aroundText` alone leaves the nameless customer with the default phrase, and the preview does not show it |
| `ProductBonus`, `ProductListItemProductBonus` | the bonus word in the plural form the number takes (one / few / many) | `pluralizationAffix` with all three forms — the converter refuses a partial set; on `RecipientBonusBalance`, `RecipientNearestExpirationBonuses`, `OrderChargedBonuses`, `RecipientCustomFieldInteger` it is off and needs `"isEnabled": true` |

```jsx
<Var param="RecipientGreeting" affixVariableText={{ "aroundText": { "before": "Hi, ", "after": "!" }, "emptyBehavior": { "mode": "fallback", "fallbackText": "Hi!" } }} />
<Var param="RecipientBonusBalance" balance={{ "systemName": "<FROM_LOOKUP>", "name": "<FROM_LOOKUP>", "internalId": "<FROM_LOOKUP>" }} pluralizationAffix={{ "isEnabled": true, "pluralForms": { "one": "<ONE>", "few": "<FEW>", "many": "<MANY>" } }} />
```

## Empty value

`affixVariableText.emptyBehavior` decides what the chip prints when the value is not found: `hide` removes it
silently, `fallback` prints `fallbackText` instead of the whole chip, affixes included — a unit or a word goes into the text
("0 points"); `aroundText` is printed only when the value exists. A chip with a
fallback is not empty, but a node hides when any other chip in it is — a text mixing a fallback chip with a plain one
needs `emptyVariableBehavior="show"`. A real name whose value the customer lacks is a silent empty spot in the sent
email — expected.

`emptyVariableBehavior` is a node setting, not a chip setting (the editor's "Display conditions" → "If element
variables are empty"): what the node does in the sent email when a variable inside it is empty. It works only on
send — the preview always shows the node.

| on | values | default |
|---|---|---|
| any element with a chip in its content or props (`Text`, `Button`, `Image`, `Label`, …) | `"hide"` — the element drops out entirely, with its background and icon; `"show_height_only"` — the content is removed, the space stays; `"show"` | `"hide"` |
| `FlexRow` | `"show"`, `"hide"` — the whole row drops out | `"show"` |

A `Text` hidden inside a row left on `"show"` leaves the row and its spacing in place — hide the row to drop both. A group whose lines are all hidden this way disappears with them, spacing and background included.

```jsx
<FlexRow emptyVariableBehavior="hide"><Column size={12}><Text><p style="margin: 0">Delivery: <Var param="OrderDeliveryCost" /></p></Text></Column></FlexRow>
```

## Long text — `formatString`

Text parameters with `formatString` (`ProductName`, `ProductDescription`, `ProductVendorName` and their counterparts in
the other families, string custom fields) truncate at **150 characters** by default, and the preview pads instead of cutting: it repeats the sample
up to the limit. Manually selected products — turn it off, the preview then shows the real name; products from a
mechanic — set a limit, the editor presets are `40`, `80`, `120`, `200` (`40` a name in a narrow card, `80`–`120` a
description or full width); another value shows in the editor as “other”.

```jsx
<Var param="ProductName" formatString={{ "isTruncateEnabled": false }} />
<Var param="ProductName" formatString={{ "isTruncateEnabled": true, "truncateValue": 40 }} />
```

## Common parameters

Email parameters (`root`) stand anywhere; rows marked *(automated only)* read the order and have nothing to read in a
bulk campaign. Product families stand only in a product row card, where the row's mechanic picks the family
(`references/wiki/product-rows.md`): outside a card the converter accepts the chip and the preview draws it, and only this
rule keeps it where it resolves.

| `param` | what it is | its attributes |
|---|---|---|
| `RecipientGreeting` | the full greeting by name | `affixVariableText` — the greeting words |
| `PromoCodeValue` | promo code | `promoCodePool`, `caseFormatter`, `affixVariableText` |
| `PromoCodeExpirationDateTime` | the date until which the promo code is valid | `promoCodePool`, `formatDate`, `affixVariableText` |
| `RecipientBonusBalance` | bonus points on the balance | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `RecipientNearestExpirationBonuses`, `…Date` | the points about to expire and their date | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix` / `formatDate`, `affixVariableText` |
| `OrderTotalAmount` *(automated only)* | order total | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderExternalId` *(automated only)* | order number | `orderExternalIdSelection`, `affixVariableText` |
| `OrderDateTime` *(automated only)* | order date | `formatDateTime`, `affixVariableText` |
| `ProductName` | product name | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductPrice` | product price | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductOldPrice` | price before discount | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductPictureUrl` | product image address, always the whole address | `productSegment` |
| `ProductUrl` | product link | `productSegment`, `affixVariableText` |
| `ProductListItemProductName` | product name in a list row | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductPrice` | product price in a list row | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemProductPictureUrl` | product image in a list row | `productSegment` |

Not here — the full lists: email parameters in `personalization-parameters.md`, product parameters by entity in
`product-parameters.md`. A similarly named parameter of another entity is not a substitute.

`formatDate` and `formatDateTime` take `{ "format": <key> }` with one of the editor's keys — `mm/dd/yyyy`, `dd month`,
`month yyyy`, `day of week, dd month, yyyy`, `yyyy`, and for a date-time also `mm/dd/yyyy hh:mm`, `hh:mm`; any other
value is silently replaced by the first key. The preview draws a sample date and reflects the pattern only in part.

## Errors from the backend

The converter names what it refuses and the message is enough. Two errors come from the backend after the converter — the campaign card and the save remark name the expression, not the `<Var>`:

| where and what | cause | what to do |
|---|---|---|
| save or link enrichment: `Line N, symbol M: Invalid symbol` | an empty setting got into the email — the expression lost its name (`Order.IDs.`) | find the `<Var>` whose setting is empty, fill it, rewrite the JSX; one error per broken place |
| campaign card or a save remark: “The campaign contains unknown parameters: …” | a name the project does not have, or the wrong reference list (an integration name in `orderExternalIdSelection`), or a product mechanic expression | read the expression: `Recipient.Recommendations…`, `GetProductList(…)`, `Products.GetBySegment(…)` → the mechanic and its settings, [product-rows.md](./product-rows.md); `Order.IDs…`, a promo code, a balance, a custom field or an external system → the lookup table above and the `systemName`; an unknown pattern → do not diagnose from memory, show it verbatim |

A read email may hold `<personalization-parameter model="…">` — a chip the converter could not read. Rewriting loses it; it is
personalization the project does not recognize.
