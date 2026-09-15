# Product rows — `<CollectionRow>`

**When to read:** the email has products: recommendations, a product list, order products, viewed products, products from an event or a manually picked selection. Do not generate `<CollectionRow>` before reading this file.

**Return to:** Workflow / Self-check in `SKILL.md`; check the mechanic, all required settings, the lookup values, the placement of product `<Var>`s and that the family matches.

A product row is the second kind of block row: instead of columns it holds product cards. Everything about it
is here — how to assemble it, where it takes its products from, which chips are allowed in its card and what
breaks an email that contains one. An ordinary email does not need this file; it is opened when the email has
products; the rest of the DSL surface is in [dsl-surface.md](./dsl-surface.md).

```
Template  →  Block  →  CollectionRow  →  CardTemplate | CollectionCard  →  Column  →  element
```

```jsx
<Template>
  <Block>
    <CollectionRow dataSource={{ "key": "ProductShowcase" }} orientation="vertical" columnCount={{ "value": 3 }}>
      <CardTemplate>
        <Column size={12}>
          <Image image={{ mode: "dynamic", dynamic: [<Var param="ProductPictureUrl" />] }} url={[<Var param="ProductUrl" />]} height={{ "height": 180 }} />
          <Text><p style="margin: 0"><Var param="ProductName" formatString={{ "isTruncateEnabled": true, "truncateValue": 40 }} /></p></Text>
          <Text><p style="margin: 0"><Var param="ProductPrice" /></p></Text>
        </Column>
      </CardTemplate>
    </CollectionRow>
  </Block>
</Template>
```

This is a copy-safe example of card styling: the products are not picked yet. `ProductShowcase` without `<CollectionCard>` is legal; after generating, tell the user that the products need to be picked in the editor or named to you for a lookup.

**Products not picked yet — write no cards at all.** `<CollectionCard>` means "this very product stands
here", and without `product` it is not an empty slot but the rejection `A <CollectionCard> names the product it stands for`.
Placeholders are drawn by `<CardTemplate>` itself, and how many of them — the mechanic decides. A row **without `dataSource`** gives
a `columnCount × rowCount` grid of empty cards. `ProductShowcase` — one: it is the "I will fill it by hand" mechanic,
and the number of cards in it is set by the picked products; the grid only lays them out. So while the source is not
picked, do not invent a mechanic: a row without one is exactly the "added, not configured" state.

`formatString` on the name is not for looks: without it the preview pads the value with repeats up to 150 characters and
the card falls apart. For products from a mechanic set a limit; for manually picked ones — `isTruncateEnabled:
false`, so the preview shows the real name. Details — `references/personalization.md`,
"Long text".

## One card draws every product

`<CardTemplate>` is the card every product is drawn with; `columnCount` × `rowCount` say how many of them
to show, but **only on a vertical row**. By default a row is horizontal and draws one card
per line: `columnCount` is not read in it at all, and the converter rejects such a setting. Need a grid —
write `orientation="vertical"` together with `columnCount`, as in the example above.

Its `<Column>`s are the card's inner arrangement (the picture above the words or next to them), and their `size`
sums to 12, like the row's columns. **A row holds one `<CardTemplate>`**; a second one is the error
`A <CollectionRow> may hold only one <CardTemplate>`.

Product values are **chips**. A product chip is authored only inside such a row; do not put it in an ordinary
column, assemble a product row. `<Var>` forms — in `references/personalization.md`.

**The product picture is personal, not a file.** The address arrives as a chip, like a personal picture from
customer data: `image={{ mode: "dynamic", dynamic: [<Var param="ProductPictureUrl" />] }}`. A static
file in the card would mean the same picture for every product. The click link on the picture is a chip too:
`url={[<Var param="ProductUrl" />]}`, otherwise the picture leads nowhere. In a row that iterates a product
list, both chips take their names from the `ProductListItem*` family — see the table below.

**The chip family is set by the mechanic, not by the card.** The mechanic determines what exactly the row iterates, and
the chips must be from the same family:

| Mechanic | Chip family |
|---|---|
| `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS`, `FROM_SEGMENT`, `ORDER_PRODUCTS`, `ViewedProducts`, `ViewedProductsInSession`, `SessionProductCategoryViews`, `SessionGetAddedToListProducts`, `RecentlyBoughtProducts`, `CategoryProductsComputedField`, `FromCustomerComputedField`, `ProductShowcase` | `Product*` |
| `FROM_PRODUCT_LIST` | `ProductListItem*` |
| `ProductListItem` | `SingleProductListItem*` |
| `ORDER` | `OrderItem*` |
| `ProductView` | `ProductView*` |

**Names follow the product value.** The same value is named differently in different families, and a prefix
cannot simply be glued onto a name: the price of a product in an order is `OrderItemAmount`, not
`OrderItemProductPrice`. Here is the full table of common values:

| What to show | `Product*` | `ProductListItem*` | `OrderItem*` |
|---|---|---|---|
| name | `ProductName` | `ProductListItemProductName` | `OrderItemProductName` |
| picture | `ProductPictureUrl` | `ProductListItemProductPictureUrl` | `OrderItemProductPictureUrl` |
| link | `ProductUrl` | `ProductListItemProductUrl` | `OrderItemProductUrl` |
| price | `ProductPrice` | `ProductListItemProductPrice` | `OrderItemAmount` |
| price before discount | `ProductOldPrice` | `ProductListItemProductOldPrice` | `OrderItemBaseAmount` |
| description | `ProductDescription` | `ProductListItemProductDescription` | `OrderItemProductDescription` |
| discount | `ProductDiscount` | `ProductListItemProductDiscount` | `OrderItemDiscount` |
| SKU (vendor code) | `ProductVendorCode` | `ProductListItemProductVendorCode` | `OrderItemProductVendorCode` |
| manufacturer | `ProductVendorName` | `ProductListItemProductVendorName` | `OrderItemProductVendorName` |

For `SingleProductListItem*` and `ProductView*` the names are built the same way as for `ProductListItem*` — with their
own prefix instead of `ProductListItem`. A name that does not exist the converter will not accept: `Unknown personalization
parameter` — so guessing is useless, and the full list of product parameters by entity is in
`references/product-parameters.md`.

The family is chosen by the entity the mechanic iterates. A chip from another family the converter rejects and suggests the twin parameter from the right family. A product chip outside `<CollectionRow>` is a different case: do not put it in an ordinary column, assemble a product row.

## Where the products come from

`dataSource` names the mechanic in `key`, and its settings live under `model.settings.model`:

```jsx
<CollectionRow dataSource={{ "key": "RECIPIENT_RECOMMENDATIONS", "model": { "settings": { "model": { "recoMechanicSystemName": "<SYSTEM_NAME_FROM_LOOKUP>" } } } }}>
```

Do not copy this fragment before the lookup. The `<SYSTEM_NAME_FROM_LOOKUP>` value must be replaced with the exact `systemName` returned by `entities_list(entityType: "RecommendationMechanic")`; preview/save do not check a made-up name.

- **Write only what the mechanic declares.** A mechanic on its defaults is written as a single `key`.
- **Mechanic names and their settings are not guessed.** A mechanic that cannot fill a product row
  the converter rejects, listing the ones that exist in its message. Content and theme showcases are among the rejected:
  they iterate the root object, not products.
- **A row may have no mechanic at all** — that is the state right after adding it, before the source is chosen.
  Then `dataSource` is simply not written.
- **Do not write a mechanic without its required setting at all.** The setting is required by the package's policy.
  An exact incomplete example with `RECIPIENT_RECOMMENDATIONS` and no `recoMechanicSystemName` passed preview successfully,
  was saved and read back without the setting, so a successful preview/save is not a check of
  completeness. The value is found by lookup — the product list, products and the recommendation mechanic are in
  `entities_list` — and whatever is not there is asked from the user. There is no such thing as an empty setting or a placeholder.

## Mechanic settings

Required ones are marked **★** — without them the row does not work. The rest need not be written unless you change them:
as everywhere in the DSL, what is not declared stays as it is.

| Mechanic | Its settings |
|---|---|
| `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS` | **★ `recoMechanicSystemName`** — the system name of the recommendation mechanic (below, where to take it from) |
| `FROM_PRODUCT_LIST` | **★ `productListSystemName`** and **★ `productListInternalId`** — both; these are not two ways to name one thing (below, why); `availableForRecipient`, `enabledFilterBySegment`, `filterBySegmentDetails`, `singlePerGroup` |
| `FROM_SEGMENT` | **★ `segmentSystemName`** and **★ `segmentationInternalId`** — also both; `random`, `availableForRecipient`, `singlePerGroup`, `filterByRecipientComputedFieldSettings` |
| `SessionGetAddedToListProducts` | **★ `productListSystemName`** and **★ `productListInternalId`** — as with `FROM_PRODUCT_LIST`; `enabledFilterBySegment`, `filterBySegmentDetails`, `availableForRecipient`, `singlePerGroup` |
| `ORDER_PRODUCTS`, `ViewedProducts`, `ViewedProductsInSession`, `SessionProductCategoryViews`, `RecentlyBoughtProducts` | none required; `enabledFilterBySegment`, `filterBySegmentDetails`, `availableForRecipient`, `singlePerGroup` |
| `CategoryProductsComputedField` | **★ `recoMechanicSystemName`** and **★ `computedField`** — an object `{ "systemName": …, "internalId": … }`, both fields |
| `FromCustomerComputedField` | **★ `systemName`** and **★ `internalId`** — here the setting is the computed field object itself, i.e. `"settings": { "model": { "systemName": …, "internalId": … } }`; without the system name the expression stays `Recipient.CustomField` and the row fills nothing |
| `ORDER`, `ProductShowcase`, `ProductListItem`, `ProductView`, `Empty` | no settings — written as a single `key` |

### Where the recommendation mechanic comes from

The system name comes from `entities_list`, `entityType: RecommendationMechanic`. A result row has `systemName`,
`name` and three fields about suitability, because **not every mechanic will do**:

| column | what to do with it |
|---|---|
| `target` | must match what the row's mechanic accepts: `Customer` for `RECIPIENT_RECOMMENDATIONS`, `Offer` for `PRODUCT_RECOMMENDATIONS`, `Category` for `CategoryProductsComputedField` |
| `readyToUse` | only `true` is taken |
| `status` | only `RecalculationRequested` or `RecalculationFinished` is taken — these are two statuses out of eight |

The lookup returns the suitability fields, and the agent must apply them before generating: preview/save do not prove
that the mechanic suits the chosen row or is already ready for calculation. So the choice is made by the three columns, not by the
first row that looks right. Not a single suitable one found — tell the user, do not substitute an unsuitable one:
there is nothing to assemble a recommendation row from, and it is better to offer another filling mechanic.

Two pairs are easy to confuse, and confusing them means assembling a row with the wrong iterated entity:

- **`ORDER` versus `ORDER_PRODUCTS`.** The first iterates order lines and wants `OrderItem*` chips; the second
  iterates the products of those lines and wants `Product*`. If you need the product's name and price from the order — that is
  `ORDER_PRODUCTS`; if the amount and quantity per order line — `ORDER`.
- **`ProductListItem` versus `FROM_PRODUCT_LIST`.** The first is a single list line, and it draws one
  card (`columnCount` and `rowCount` are not needed for it); the second iterates the whole list.

`filterBySegmentDetails` is an object `{ "systemName": …, "internalId": … }`, and it is needed only when
`enabledFilterBySegment` is on.

**The system name and the internalId are not two ways of saying one thing, but two different readers.** The system name
goes into the sent email (`Recipient.GetProductList("...")`) — without it the campaign does not
build. The `internalId` does not get into the email, and does two other things: by it the editor
shows which list is selected (the select looks it up by `internalId` and looks at nothing else), and by it
the email's dependency on the list is declared — the thing that keeps the platform from deleting a list that is in use.
Write only the system name — the list expression will be built, but the user, opening the row in the
editor, will see an **empty select**, as if no list were selected, and the platform will consider the list
unused. The same goes for the segment (`segmentSystemName` + `segmentationInternalId`) and for the computed field.
`productListId` the canvas writes as a third field but reads nowhere — do not invent it yourself, and if you saw it in an email
you are editing — leave it as is.

**Where to take the values.** A product list — `entities_list`, entity `ProductList`: **`systemName` and
`internalId` are taken from one result row**, like a product's identifier triple. Recommendation mechanics —
`entities_list`, entity `RecommendationMechanic`; the lookup returns `systemName`, `name`, `target`,
`readyToUse` and `status`, and the agent applies the suitability rules above. The segment catalogue this file does not
describe: it is taken from the user or from the email you are editing. An example of a mechanic with a list:

```jsx
<CollectionRow dataSource={{ "key": "FROM_PRODUCT_LIST", "model": { "settings": { "model": { "productListSystemName": "<PRODUCT_LIST_SYSTEM_NAME_FROM_LOOKUP>", "productListInternalId": "<PRODUCT_LIST_INTERNAL_ID_FROM_LOOKUP>" } } } }}>
```

Do not copy this fragment before the lookup. The `<PRODUCT_LIST_SYSTEM_NAME_FROM_LOOKUP>` and
`<PRODUCT_LIST_INTERNAL_ID_FROM_LOOKUP>` values must be replaced with the exact `systemName` and `internalId` from one row of
`entities_list(entityType: "ProductList")`; preview/save do not check that the list exists.

- **Some mechanics work only in an automatic campaign.** They read the customer's action, and a bulk
  campaign has no action — the row will go out empty. These are `ORDER`, `ORDER_PRODUCTS` (order products),
  `ViewedProducts`, `ViewedProductsInSession`, `ProductView`, `SessionProductCategoryViews`,
  `SessionGetAddedToListProducts`, `RecentlyBoughtProducts`. Independent of the campaign kind are
  `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS`, `FROM_PRODUCT_LIST`, `FROM_SEGMENT`,
  `ProductShowcase`. The full list of what the converter accepts it lists itself in the error
  message; the campaign kind is set at creation and does not change afterwards — see skill `maestra-email-ops`.

## A manually selected list

`ProductShowcase` — the mechanic set by the "Filled manually" toggle — holds one
`<CollectionCard>` per picked product, and each card names its product with the
`product` attribute: the triple `internalId`, `externalId`, `externalSystemName`, as the lookup prints it in a row.
A card without content is drawn by the template; a card with its own columns — by them:

```jsx
<CollectionRow dataSource={{ "key": "ProductShowcase" }} orientation="vertical" columnCount={{ "value": 3 }}>
  <CardTemplate><Column size={12}><Text><p style="margin: 0"><Var param="ProductName" /></p></Text></Column></CardTemplate>
  <CollectionCard product={{ "internalId": "<PRODUCT_INTERNAL_ID_FROM_LOOKUP>", "externalId": "<PRODUCT_EXTERNAL_ID_FROM_LOOKUP>", "externalSystemName": "<PRODUCT_EXTERNAL_SYSTEM_NAME_FROM_LOOKUP>" }} />
  <CollectionCard product={{ "internalId": "<SECOND_PRODUCT_INTERNAL_ID_FROM_LOOKUP>", "externalId": "<SECOND_PRODUCT_EXTERNAL_ID_FROM_LOOKUP>", "externalSystemName": "<SECOND_PRODUCT_EXTERNAL_SYSTEM_NAME_FROM_LOOKUP>" }}><Column size={12}><Text>This very one</Text></Column></CollectionCard>
</CollectionRow>
```

Do not copy this fragment before the lookup. Each `product` triple must be replaced with the exact
`internalId`/`externalId`/`externalSystemName` from `entities_list(entityType: "Product")` or from the email
you are editing.

The rules of such a row, and breaking any one of them is an error:

- **A card always names a product.** A card that names none is not a second template but an error;
  if the products are not picked yet, write no cards at all — see the beginning of the file.
- **The triple is written whole and is not invented.** Two of the three values cannot be derived from the third, so a
  product named incompletely or with an extra field is rejected. The triple is taken from the lookup or from the email
  you are editing. Do not write a made-up triple: preview/save do not prove that such a product exists and is
  suitable.
- **Do not write keys or the `selections` map.** The row knows the product under its own name, but that name is made by the
  converter, like all other document ids. An email read from the editor sometimes arrives in the old
  form — `selectionId="…"` instead of `product` — it is readable, and there is no need to rewrite it; but both forms
  on one card are rejected: a product is named once.
- **Products are searched with `entities_list`, `entityType: Product`.** The user names a product in words ("Home Alone
  quest"), by SKU or by external id — any of the three is searched with a single `query`. A result row has exactly the
  triple the card asks for: `internalId`, `externalId`, `externalSystemName` — and next to it `name`,
  `price`, `vendorCode`, `isAvailable`, `url`, `pictureUrl`, so that the user can recognize the product.

  **More than one found — show them and ask, do not choose yourself.** A catalogue holds many products with the same name;
  the price and SKU are printed for exactly that. And do not silently offer a product with `isAvailable: false`.

  Nothing found — do not pick something similar and do not invent: ask the user for a more precise name,
  the SKU or the external id, or assemble the row without cards (below).
- **Product data is substituted automatically — no need to pass it.** The email stores only the identifier triple
  per card, and `visual_template_preview` itself reads the name, price and picture from the project's catalogue
  by those triples. It is enough for you to name the product correctly in `product` — the rest appears in the
  preview without your involvement, and there is no need to restate product data in the call. A product that is no longer
  in the catalogue the card draws as a placeholder; all cards are drawn the same way if the catalogue is unavailable —
  the layout renders in any case. A personal price and bonus points will never be in the preview: each
  recipient has their own, and nobody knows them before sending.
- **Products not picked yet — write the row without cards.** `ProductShowcase` with one `<CardTemplate>` and not a
  single `<CollectionCard>` is a legal row: the card styling is ready, the products are picked into it
  separately. Do exactly that when there is nowhere to take the products from, and **tell the user that they need to be picked** — in the
  editor or by naming them to you. Add the cards when the products appear.
- **Cards exist only under `ProductShowcase`.** Under a mechanic that finds products itself, the row
  would draw the cards and leave the mechanic unread.
- **A card without its own content needs a `<CardTemplate>`** in the row — otherwise there is nothing to draw it with. And
  such a card carries nothing but the named product: a setting on it would be lost, so it
  is rejected.

## Card heights and `autosizeKey`

`height` on a card element carries, next to the height, an **autosize key**: elements with the same key
are measured together and take the height of the tallest. The template is drawn once per product, so its
elements are one group by themselves; the key matters where several cards carry their own content.

**Measured together — only with `settingType: "manual"`.** It has two values, and they decide different things.
`manual` — the height as a number in px, and the element joins the autosize group: this is exactly how the row's cards
keep the same shape with any products. `original` — the height by content, and the element **drops out** of the
alignment: it will have no group in the markup, and an `autosizeKey` next to it does
nothing. Do not align text with a key while leaving it `original` — the key will be set, but the heights will not match.

**The default differs by element, and for a reason** (values — §6 of `dsl-surface.md`): text cannot know its length
in advance, so its height is by content, while products come in different proportions, so the picture has a
fixed one. Writing it yourself — keep to the same: `original` for text and the splitter, a number for the picture.

**Compute the picture height from the card width:** the email width minus the block's side `innerSpacing` minus the
`cardGap` between cards, divided by their number — with a 600 email, 24 padding and a 24 gap that is 168 px.
Otherwise the default container leaves empty space under a square photo.

- **Do not invent a uuid for the key.** It reads as carried over from a saved email, but groups
  nothing — the card silently drops out of the height it was supposed to share.
- **A key you did not write will appear by itself.** The converter issues a fresh one to every card element that
  had no key — so after reading the email you will see a uuid where you set nothing. This is
  not the same as an invented one: it is real, the element is in its group. When editing such an email, carry it over as
  is.
- **The key is either not written** (the card is measured on its own), **or carried over** from the email you are editing,
  **or it is a name in words** for a group you have designed: `autosizeKey: "the-picked-two"` on two
  cards puts them at one height.
- A card with its own content stands in its own group by default — just like a detached card on the
  canvas: its height becomes the author's business, which is what detaching is done for.

## Attributes of elements inside a card

An element in a card carries settings it does not have in an ordinary column — outside a card the same attributes
will be `Unknown attribute`:

| Attribute | On which elements | What it does |
|---|---|---|
| `height` | `Text`, `Image`, `Split` | The element's height and the autosize key. JSON: `{ "settingType": "original" \| "manual", "height": 180, "mobile": { … }, "autosizeKey": "…" }`. How the values differ and what to write by default — above, "Card heights" |
| `url` | `Text`, `Divider` | A link to the product — to lead to it not only with the button. Outside a card the same attribute on them is an error: there is nowhere to lead |

## Attributes of the row containers

| Container | Attributes |
|---|---|
| `CollectionRow` | `dataSource`, `columnCount`, `rowCount`, `orientation`, `cardGap`, `rowGap`, `isCheckerboardEnabled`, `background`, `border`, `borderRadius`, `innerSpacing`, `isColumnsMobileAdaptive`, `columnVerticalDirection`, `visibilityOnDevices` |
| `CardTemplate` | `url`, `columnGap`, `verticalAlign`, `background`, `border`, `borderRadius`, `innerSpacing` |
| `CollectionCard` | the same as `CardTemplate`, plus the required `product` — the product the card stands for |

Value shapes of the row: `columnCount` and `rowCount` — `{ "value": N }`; `cardGap` and `rowGap` —
`{ "size": N, "mobile": { "size": N } }`; `orientation` — a string: `"horizontal"` (the default) draws one
card per line and does not read the column count, `"vertical"` gives a `columnCount` × `rowCount` grid. The shape of what
is written is checked against the default, and the response to a wrong shape shows the whole default — you need not
remember the shape, it is enough to read the rejection.

`url` on a card leads to the product as a whole, not only its button. Inside a card `url` also appears on
`<Text>` and `<Divider>` — outside a card the same attribute on them is an error, because there is nowhere to lead.
