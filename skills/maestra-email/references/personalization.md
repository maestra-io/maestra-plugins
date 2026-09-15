# Personalization — chips in the email

**When to read:** the first `<Var>`, dynamic image/link or tenant-specific personalization setting appears in the email.

**Return to:** Workflow / Self-check in `SKILL.md`; check the exact `param`, the allowed place, the required settings and the lookup of every `systemName`.

A personalized value (a promo code, the recipient's name, a price) is written with the `<Var>` tag. The converter assembles
a **chip** out of it — the same thing the editor inserts as an inline tag — so a chip from the email opens and is edited
in the editor as usual. Raw `${...}` template expressions (`${Customer...}`, `${Order...}`) are not needed for this and
must not be written: the only exception is `${Message.UnsubscribeLink}` in `href` per the rules of SKILL.md.

## Form

`param` is the parameter name, the remaining attributes are its settings, formatters and affixes:

```jsx
<Text><p style="margin: 0;">Your promo code: <Var param="PromoCodeValue" promoCodePool={{ "systemName": "<PROMO_CODE_POOL_SYSTEM_NAME_FROM_LOOKUP>", "name": "<PROMO_CODE_POOL_NAME_FROM_LOOKUP>", "internalId": "<PROMO_CODE_POOL_INTERNAL_ID_FROM_LOOKUP>" }} caseFormatter={{ "format": "uppercase" }} /></p></Text>
```

Do not copy tenant-specific values before the lookup: take the `systemName`, `name` and `internalId` fields from one row
of `entities_list(entityType: "PromoCodePool")`.

Write only what you change: every part has a default, extra fields are not needed.

An attribute this parameter does not have is a converter error naming the parameter. The list of parameters and their
attributes is at the end of the file.

## Where it can stand

**In text** — as above, inside the markup of `<Text>` or `<BulletItem>`.

**In a value's string** — as a list of segments: the text around it and a `<Var>` in place of the chip.

```jsx
<Button url={["https://shop.example/sale?promo=", <Var param="PromoCodeValue" promoCodePool={{ "systemName": "<PROMO_CODE_POOL_SYSTEM_NAME_FROM_LOOKUP>", "name": "<PROMO_CODE_POOL_NAME_FROM_LOOKUP>", "internalId": "<PROMO_CODE_POOL_INTERNAL_ID_FROM_LOOKUP>" }} />]}>Claim</Button>
```

**In a label** — the same way between the `<Label>` tags, as a list of segments. A label with an empty variable disappears
entirely instead of leaving an empty space: this is how a "−30%" badge is made, which a product without a discount does not have.
Labels live in a product-row card: the converter will let them through in a regular row too, but on the editor canvas they are not there. Details —
`references/dsl-surface.md` §6 "Labels and Label".

```jsx
<Labels><Label>{["−", <Var param="ProductDiscount" />]}</Label></Labels>
```

**In a button's words** — the same form between the tags. Tenant-specific settings here are also taken from the lookup:

```jsx
<Button>{["Redeem ", <Var param="RecipientBonusBalance" balance={{ "systemName": "<BALANCE_SYSTEM_NAME_FROM_LOOKUP>" }} />, " points"]}</Button>
```

**Inside a structure** — at any depth. This is how a personal image is set: `mode: "dynamic"`, and the address
comes from the parameter in full. Fields absent from the value are merged onto the default, so `static` does not need
to be written:

```jsx
<Image image={{ "mode": "dynamic", "dynamic": [<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "<CUSTOM_FIELD_SYSTEM_NAME_FROM_LOOKUP>" }} />] }} />
```

Write a domain prefix before the `<Var>` only when the user named it
(`"dynamic": ["https://cdn.example.com/", <Var param="ProductPictureUrl" />]`). By default the field's value is
the whole address: an invented prefix breaks the image for every recipient.

A string without a chip stays a string — the list is needed only where there is a chip. And the other way round: an array without a `<Var>`
the converter reads as an array of values, so concatenating two texts is not expressed as a list.

## The entity matters more than the name

Every parameter has its own entity. From a regular column only one is available — the email itself (`root`), and that is 43
parameters, including all order data: in an automatic email `OrderTotalAmount`, `OrderExternalId`,
`OrderDateTime`, order custom fields and the other `Order*` stand anywhere — in the heading, in the text, in a
button. The five product entities (`product`, `productView`, `productListItem`, `singleProductListItem`,
`orderItem`) are the remaining 125, and they come alive only inside a block that iterates over products — that is, the
product row `<CollectionRow>` with its cards (`references/product-rows.md`). A chip of an entity other than the one
the row's mechanic iterates over is rejected by the converter, which itself names the twin from the right family. A product
chip is not placed in a regular column: for products, build a `<CollectionRow>`. The list of email parameters is in
`personalization-parameters.md`,
product ones by entity — in `product-parameters.md`.

The campaign kind restricts too: the 21 parameters marked *(automated only)* read the order, and in a bulk
campaign they have nothing to read.

## `type` inside `customFieldType` is not written

It is derived from `param` — a string field's chip is never a date — and it is the only chip field the
converter will **not** reject: the value will be merged onto the default and go into storage incorrect.

The trap here is in the lookup response: a custom field has a value type, and it must not be carried into the chip. The value
type is used to choose the `param`, but it is not copied inside the chip.

The rest of what the converter derives itself (`versionNumber`, `parameterString`) does not need to be remembered: the parameter
has no attribute with that name, and an attempt comes back as an error with that text.

## Tenant-specific names — only from the lookup

A setting that refers to a project catalogue requires a real name. **Do not invent a
`systemName`.** It goes into the email's expression as is, and the converter does not consult the catalogue. What
comes out depends on what the name turned out to be:

| what is in the setting | what is in the email | how it comes back |
|---|---|---|
| empty | `Order.IDs.` | the expression does not parse: `Invalid symbol`, save and link enrichment refuse |
| a name the project does not have | `Order.IDs.Backend` | "The campaign contains unknown parameters" — a template error on the campaign card |
| a real name, but the customer has no value | `Order.IDs.website` | a silently empty spot in the sent email |

Only the third case stays silent, and it is expected. The first two the platform catches and shows to the
user, and the second also arrives in the save response as a validation remark: if it is there,
show it to the user instead of reporting a clean save.

**And all the more, do not leave such a setting empty.** The name is substituted into the expression as a path segment
(`Order.IDs.<systemName>`, `PromoCode.WithType<systemName>.Value`), so an empty value yields
`Order.IDs.` — an expression without a name, and the email as a whole stops being valid.

The converter rejects such a chip, naming the unfilled attribute:

```
<Var param="OrderExternalId"> needs a value in `orderExternalIdSelection`
```

If an empty setting did make it into the email, later checks may answer `Line N, symbol M: Invalid
symbol`, one error per place with a broken expression. The rule is the same: first fill the setting from the
lookup or from the user.

A value is required by: `customFieldType`, `externalSystem`, `orderExternalIdSelection`, `promoCodePool`,
`balance`, `hostname` (on `*AddToCartUrl`) — a non-empty name; `discountQuery` — when enabled; `amount` —
greater than zero; `affixVariableText` — the replacement text, when `emptyBehavior.mode` is `fallback`.

Hence the rule: **no name — do not write the parameter.** A parameter with an unfilled setting is not "a chip the
user will finish filling in the editor" but a broken email. Ask for the name or offer a parameter that
does not need a catalogue.

Which setting to ask for with which entity type (the calling rules are in the tool's own description):

| setting | what to ask with | parameters |
|---|---|---|
| `promoCodePool` | `entityType: PromoCodePool` | `PromoCodeValue`, `PromoCodeExpirationDateTime`, the `discountQuery` setting |
| `customFieldType` | `entityType: CustomField` + `ownerEntityType` by the parameter's entity | all `*CustomField*` |
| `balance` | `entityType: Balance` | `RecipientBonusBalance`, `RecipientNearestExpirationBonuses*` |
| `externalSystem` | `entityType: ExternalSystem` | `ProductExternalId` and its relatives, `*AddToCartUrl` |
| `orderExternalIdSelection` | `entityType: CustomField`, `ownerEntityType: OrderExternalId` | `OrderExternalId` |
| `productListSystemName` + `productListInternalId` | `entityType: ProductList` | the settings of product-row mechanics with a list; take both values from one lookup row |
| `recoMechanicSystemName` | `entityType: RecommendationMechanic` | the setting of a product row's recommendation mechanics |
| `product` | `entityType: Product` | the manual `ProductShowcase` card |

`ownerEntityType` for custom fields is taken by the field's owner, not by the parameter name: `Customer` for
`Recipient*`, `Order` for `Order*CustomField*`, `OrderLine` for `OrderItem*`, `Product` for `Product*`,
`ProductListItem` for `ProductListItem*`.

**External systems and external order identifiers are different catalogues.** `ExternalSystem` is the list of the
project's integrations ("Shopify", "an ERP"), and it is needed by product parameters. The order number has a different catalogue: it is
a custom-field type with the owner `OrderExternalId`, and that is exactly what the editor asks for in its popover.
An integration name put into `orderExternalIdSelection` will not be a converter error — the platform
will answer "The campaign contains unknown parameters" on the campaign card.

From the lookup response carry into the JSX all the fields that exist in the setting's model. For regular chips `systemName`
takes part in the email's expression, while `name` and `internalId` are needed by the editor: the chip's preview on the
canvas is drawn from `name`, the select in the popover is preselected from `internalId`. Do not delete them as "extra" if the lookup returned them.

For product-row mechanics with a list a separate rule applies: `productListSystemName` and
`productListInternalId` are both needed and are taken from one row of `entities_list(entityType: ProductList)`.
Details — in `product-rows.md`.

Two restrictions on pools the lookup will not warn about. A promo code is read only from pools of one-time
codes and referral pools — a pool of another type does not work in a chip. And a pool's system name is optional: if the
response does not have it, the chip cannot be assembled — show the user such pools and ask them to pick another one or to set up
a system name.

`hostname` on `*AddToCartUrl` does not live in the lookup — it is the store's domain, and it is asked from the user;
`amount` and `destinationRoute` there have working defaults.

Custom fields are the only setting where the lookup is also needed to choose the `param` itself: exactly one of the
seven parameters per entity fits a given field, and it is chosen by the field's value type and owner type.
Multi-value fields fit no parameter.

## Long text: `formatString`

Text parameters (`ProductName`, `ProductDescription`, `ProductVendorName` and their twins in the other
families) have truncation enabled, and the default limit is **150 characters**. In the preview, though, the chip does not
cut but pads: it repeats the value up to the limit. A 72-character name is shown twice plus a
tail, and the card sprawls over five or six lines, although exactly 72 will arrive in the email.

What to write depends on whether the products are known.

**The products are selected manually** — turn truncation off: the preview will show the real name, exactly what will be sent.

```jsx
<Var param="ProductName" formatString={{ "isTruncateEnabled": false }} />
```

**The products come from a mechanic** (recommendations, a list, the order) — the limit is needed: the names are not known in advance
and will arrive at any length. The editor's presets are `40`, `80`, `120`, `200`; a value outside them will appear in the
editor as "Other"; `40` — a name in a narrow card, `80`–`120` — a description and full-width.

```jsx
<Var param="ProductName" formatString={{ "isTruncateEnabled": true, "truncateValue": 40 }} />
```

## An empty value

The `affixVariableText` affix decides what happens if the value is not found: `hide` removes it silently, `fallback`
substitutes text. It also carries the "text around the variable" — `aroundText` is printed only when there is a value.

```jsx
<Text><p style="margin: 0;">Points: <Var param="RecipientBonusBalance" balance={{ "systemName": "<BALANCE_SYSTEM_NAME_FROM_LOOKUP>" }} affixVariableText={{ "emptyBehavior": { "mode": "fallback", "fallbackText": "0" } }} /></p></Text>
```

An empty value can also be hidden as a whole row: `emptyVariableBehavior="hide"` on a `<FlexRow>` removes the
row from the email when a variable in it has no value. This is a node setting, not a chip setting, and it works only
on sending — in the preview the row is always visible. The same is written on an element too.

```jsx
<FlexRow emptyVariableBehavior="hide"><Column size={12}><Text><p style="margin: 0">Delivery: <Var param="OrderDeliveryCost" /></p></Text></Column></FlexRow>
```

## A chip that cannot be read

A parameter absent from this campaign's registry, or an unparseable model, arrives in the stored form:

```jsx
<Text><p style="margin: 0;">Code: <personalization-parameter model="bm90LWEtbW9kZWw="></personalization-parameter></p></Text>
```

Leave such fragments as they are — the converter did not understand them, and rewriting loses the chip. In the conversation you may
say that the email contains personalization this project does not recognize.

## Common parameters

Enough for most emails. The first seven are email parameters (`root`) and stand anywhere in it; the rows
marked *(automated only)* require an order, that is, an automatic campaign. The rest are product parameters and
stand only in a product-row card: the entity of `Product*` is `product`, of `ProductListItem*` —
`productListItem`, and the choice between them is not free — the row's mechanic decides it. The "mechanic →
family" table is in `references/product-rows.md`.

| `param` | what it is | its attributes |
|---|---|---|
| `RecipientGreeting` | greeting by name | `greetingWithNameInput`, `greetingNoNameInput`, `affixVariableText` |
| `PromoCodeValue` | promo code | `promoCodePool`, `caseFormatter`, `affixVariableText` |
| `PromoCodeExpirationDateTime` | the date until which the promo code is valid | `promoCodePool`, `formatDate`, `affixVariableText` |
| `RecipientBonusBalance` | points on the balance | `balance`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `OrderTotalAmount` *(automated only)* | order total | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderExternalId` *(automated only)* | order number | `orderExternalIdSelection`, `affixVariableText` |
| `OrderDateTime` *(automated only)* | order date | `formatDateTime`, `affixVariableText` |
| `ProductName` | product name | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductPrice` | product price | `productSegment`, `formatDecimalPrice`, `affixVariableText` |
| `ProductOldPrice` | price before the discount | `productSegment`, `formatDecimalPrice`, `affixVariableText` |
| `ProductPictureUrl` | product image URL | `productSegment` |
| `ProductUrl` | link to the product | `productSegment`, `affixVariableText` |
| `ProductListItemProductName` | product name in a list line | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductPrice` | product price in a list line | `productSegment`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemProductPictureUrl` | product image in a list line | `productSegment` |

**The parameter you need is not here — open the full list:** email parameters in
`references/personalization-parameters.md`, product ones by entity in `references/product-parameters.md`.
Do not pick one with a similar name from this list: a name that is not in the registry the converter will reject, and a similar
parameter of another entity is not a correct substitute.
