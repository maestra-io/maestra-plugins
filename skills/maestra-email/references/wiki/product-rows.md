---
description: "The product row <CollectionRow>: recommendations, a product list, order or viewed products, products from an event, a manual collection — the mechanic and its required settings, the card, the chips a card takes"
---

# Product rows — `<CollectionRow>`

A product row is the second kind of block row: instead of columns it holds product cards. Everything about
it is here — how to build it, where it gets its products, which chips are allowed in its card and what an
email with it breaks on.

```
Template  →  Block  →  CollectionRow  →  CardTemplate | CollectionCard  →  Column  →  element
```

## The card the editor provides

A product row is added to the canvas as a ready-made preset: image, name, price next to the crossed-out
old price, a button — and all links already lead to the product. The most common preset is three cards in
a row, image above the words; here it is in JSX:

```jsx
<Template>
  <Block>
    <CollectionRow dataSource={{ "key": "ProductShowcase" }} orientation="vertical" columnCount={{ "value": 3 }} rowCount={{ "value": 1 }}>
      <CardTemplate url={[<Var param="ProductUrl" />]}>
        <Column size={12}>
          <Image image={{ mode: "dynamic", dynamic: [<Var param="ProductPictureUrl" />] }} url={[<Var param="ProductUrl" />]} alt={[<Var param="ProductName" formatString={{ "isTruncateEnabled": false }} />]} height={{ "height": 180 }} />
          <Text themeVariant="h3"><p style="margin: 0"><Var param="ProductName" formatString={{ "isTruncateEnabled": false }} /></p></Text>
          <Split columnsGap={{ "size": 0 }} innerSpacing={{ "top": 10, "bottom": 10 }} height={{ "height": 40 }}>
            <Column size={6}><Text innerSpacing={{ "top": 0, "bottom": 0 }}><p style="margin: 0"><Var param="ProductPrice" /></p></Text></Column>
            <Column size={6}><Text innerSpacing={{ "top": 0, "bottom": 0 }} style={{ "fontSize": 16, "inscription": ["crossed"], "color": "#666666" }}><p style="margin: 0"><Var param="ProductOldPrice" /></p></Text></Column>
          </Split>
          <Button url={[<Var param="ProductUrl" />]} themeVariant="secondary" align={{ "align": "left" }} innerSpacing={{ "top": 12, "right": 16, "bottom": 12 }}>Buy</Button>
        </Column>
      </CardTemplate>
    </CollectionRow>
  </Block>
</Template>
```

The name's `formatString` is off here because `ProductShowcase` is a manual selection; under a mechanic the card sets a limit — [personalization.md](personalization.md), "Long text".

This is a copy-safe example: no products are selected yet. Its `ProductShowcase` is the manual-selection mechanic,
which needs no settings and is legal without `<CollectionCard>`; a row whose source is not known at all is written
without `dataSource`. With the mechanic known, it is set; the products are selected later, in the editor or by name for a lookup.

**This is the base example, not the only correct card.** No mockup and no special requests — build this one.
The user brought a mockup or described the card in words — lay it out accordingly, but build the links, chips
and the connection to the styles the same way as here. Trimming the card on your own initiative (dropping
the old price, the button) is not allowed: that is the user's or the mockup's decision.

**The editor offers three layouts,** and all three are a legal card: three in a row (the example above), two
in a row (`columnCount` 2, image height 260) and a list — `orientation="horizontal"`, a card of two
`<Column size={6}>`: image on the left, name with price and button on the right. Which one to take is said
by the mockup or the user; if nobody said, take the example above.

**The card's `url` is the link of everything inside it.** The converter hands the card's `url` down to the
`Image`, `Button`, `Text` and `Divider` in the card, over their own `url`: a `<CardTemplate>` and every
`<CollectionCard>` with its own columns carries `url={[<Var param="ProductUrl" />]}`, and `Image.url` and
`Button.url` repeat the same chip — the editor shows it on them. A card without `url` passes preview and looks the
same, but in the sent email nothing in it is clickable, the picture and the button included. The address comes from the mechanic, not from a person: nobody is asked for it, and it is never a placeholder.

A price chip prints the currency sign itself — `<Var param="ProductPrice" />` alone is "$1,234", with a $ written beside it "$1,234 $" ([personalization.md](personalization.md), "What a chip prints on its own").

**The card writes no styles, except for the crossed-out price.** The look of the name and the button comes
from the email's letter styles via `themeVariant`. Own styling is not forbidden, but a node that names a field of the covered set leaves the styles
(`wiki/theme.md`); `align` and `innerSpacing` may be written.
The self-check requirement "the CTA has a brand `background`" does not apply to the card button.

**No products selected yet — do not write cards at all.** `<CollectionCard>` means "this exact product stands
here", and without `product` it is not an empty slot but a refusal `A <CollectionCard> names the product it stands for`.
Placeholders are drawn by `<CardTemplate>` itself, and how many is decided by the mechanic. A row **without
`dataSource`** gives a `columnCount × rowCount` grid of empty cards. `ProductShowcase` gives one: it is the
"I'll fill it by hand" mechanic, the number of cards in it is set by the selected products, and the grid only
lays them out. So while the source is not chosen, do not invent a mechanic: a row without one is exactly the
"added, not configured" state.

`formatString` on the name keeps the preview from padding it to 150 characters — `references/wiki/personalization.md`,
“Long text — `formatString`”.

## One card renders every product

`<CardTemplate>` is the card that renders every product; `columnCount` × `rowCount` say how many of them to
show, but **only on a vertical row**. By default the row is horizontal and draws one card per line:
`columnCount` is not read there at all — the converter silently accepts it, and the row still draws one card
per line. A grid is
`orientation="vertical"` together with the column count, as in the example above.

Its `<Column>` is the inner structure of the card, and it follows the orientation: a vertical card has one
`<Column size={12}>` — image above the words, a horizontal one has two of `size={6}` — image next to the
words. `size` sums to 12, as with row columns. **A row holds one `<CardTemplate>`**; a second one is the error
`A <CollectionRow> may hold only one <CardTemplate>`.

Product values are **chips**, and they stand only inside such a row — `references/wiki/personalization.md`, "Where a chip stands".

**The product image is personal, not a file.** The address comes as a chip, like a personal image from
customer data: `image={{ mode: "dynamic", dynamic: [<Var param="ProductPictureUrl" />] }}`. A static file in
the card would mean the same image for all products. The link and `alt` are chips too; the card's
composition is above. In a row that iterates over a product list, all card chips are taken from the
`ProductListItem*` family — see the table below.

**The chip family is set by the mechanic, not by the card.** The mechanic determines what exactly the row
iterates over, and the chips must be from the same family:

| Mechanic | Chip family |
|---|---|
| `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS`, `FROM_SEGMENT`, `ORDER_PRODUCTS`, `ViewedProducts`, `ViewedProductsInSession`, `SessionProductCategoryViews`, `SessionGetAddedToListProducts`, `RecentlyBoughtProducts`, `CategoryProductsComputedField`, `FromCustomerComputedField`, `ProductShowcase` | `Product*` |
| `FROM_PRODUCT_LIST` | `ProductListItem*` |
| `ProductListItem` | `SingleProductListItem*` |
| `ORDER` | `OrderItem*` |
| `ProductView` | `ProductView*` |

**Names by product value.** The same value is named differently in different families, and you cannot just
glue a prefix onto a name: the price of a product in an order is `OrderItemAmount`, not
`OrderItemProductPrice`. Here is the full table of common values:

| What to output | `Product*` | `ProductListItem*` | `OrderItem*` |
|---|---|---|---|
| name | `ProductName` | `ProductListItemProductName` | `OrderItemProductName` |
| image | `ProductPictureUrl` | `ProductListItemProductPictureUrl` | `OrderItemProductPictureUrl` |
| link | `ProductUrl` | `ProductListItemProductUrl` | `OrderItemProductUrl` |
| price | `ProductPrice` | `ProductListItemProductPrice` | `OrderItemAmount` |
| price before discount | `ProductOldPrice` | `ProductListItemProductOldPrice` | `OrderItemBaseAmount` |
| description | `ProductDescription` | `ProductListItemProductDescription` | `OrderItemProductDescription` |
| discount | `ProductDiscount` | `ProductListItemProductDiscount` | `OrderItemDiscount` |
| vendor code (SKU) | `ProductVendorCode` | `ProductListItemProductVendorCode` | `OrderItemProductVendorCode` |
| manufacturer | `ProductVendorName` | `ProductListItemProductVendorName` | `OrderItemProductVendorName` |

For `SingleProductListItem*` and `ProductView*` names are built the same way as for `ProductListItem*` — with
their own prefix instead of `ProductListItem`. A name that does not exist will not be accepted by the
converter: `Unknown personalization parameter` — so guessing is pointless, and the full list of product
parameters by entity is in `references/wiki/product-parameters.md`.

The converter rejects a chip from another family and suggests the counterpart parameter from the right family.

## Where the products come from

`dataSource` names the mechanic in `key`, and its settings sit under `model.settings.model`:

```jsx
<CollectionRow dataSource={{ "key": "RECIPIENT_RECOMMENDATIONS", "model": { "settings": { "model": { "recoMechanicSystemName": "<SYSTEM_NAME_FROM_LOOKUP>" } } } }}>
```

Do not copy this fragment before the lookup. The value `<SYSTEM_NAME_FROM_LOOKUP>` must be replaced with the exact `systemName` returned by the lookup of entity `RecommendationMechanic`; preview/save do not check an invented name.

- **Write only what the mechanic declared.** A mechanic on its defaults is written with a single `key`.
- **Mechanic names and their settings are not guessed.** A mechanic that cannot fill a product row is
  rejected by the converter, and the message lists the ones that exist. Content and topic showcases are among
  the rejected: they iterate over the root object, not over products.
- **A row may have no mechanic at all** — that is the state right after adding it, before a source is chosen.
  Then `dataSource` is simply not written.
- **A mechanic is written with its required settings (★ in the table below)** — without them preview and save
  refuse, naming the setting. The value is found by lookup — the product list, products and the recommendation mechanic are
  entities of the project — and what is not there is asked of the user. There is no such thing as an empty setting or a placeholder.

## Mechanic settings

Required ones are marked **★** — without them the row does not work. The rest need not be written unless you
change them: as everywhere in the DSL, what is not declared keeps its value.

| Mechanic | Its settings |
|---|---|
| `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS` | **★ `recoMechanicSystemName`** — system name of the recommendation mechanic (see below for where to get it) |
| `FROM_PRODUCT_LIST` | **★ `productListSystemName`** and **★ `productListInternalId`** — both; these are not two ways of naming one thing (see below for why); `availableForRecipient`, `enabledFilterBySegment`, `filterBySegmentDetails`, `singlePerGroup` |
| `FROM_SEGMENT` | **★ `segmentSystemName`** and **★ `segmentationInternalId`** — also both; `random`, `availableForRecipient`, `singlePerGroup`, `filterByRecipientComputedFieldSettings` |
| `SessionGetAddedToListProducts` | **★ `productListSystemName`** and **★ `productListInternalId`** — as for `FROM_PRODUCT_LIST`; `enabledFilterBySegment`, `filterBySegmentDetails`, `availableForRecipient`, `singlePerGroup` — products added to the list during the session: «products from the cart» in an automated campaign, where the action that fired it is the adding; in a bulk campaign the cart is `FROM_PRODUCT_LIST` over the project's cart list (`ProductListItem*`), with quantities and line totals |
| `ORDER_PRODUCTS`, `ViewedProducts`, `ViewedProductsInSession`, `SessionProductCategoryViews`, `RecentlyBoughtProducts` | none required; `enabledFilterBySegment`, `filterBySegmentDetails`, `availableForRecipient`, `singlePerGroup` |
| `CategoryProductsComputedField` | **★ `recoMechanicSystemName`** and **★ `computedField`** — an object `{ "systemName": …, "internalId": … }`, both fields |
| `FromCustomerComputedField` | **★ `systemName`** and **★ `internalId`** — here the setting is the computed field object itself, i.e. `"settings": { "model": { "systemName": …, "internalId": … } }`; without the system name the expression stays `Recipient.CustomField` and the row fills nothing |
| `ORDER`, `ProductShowcase`, `ProductListItem`, `ProductView` | no settings — a single `key` is written; `Empty` is how a read email prints a row with no source yet — carried over as is, never written anew (a new row without a source has no `dataSource`) |

### Where the recommendation mechanic comes from

The system name comes from the lookup of entity `RecommendationMechanic`. A result row has `systemName`,
`name` and three suitability fields, because **not every mechanic will do**:

| column | what to do with it |
|---|---|
| `target` | must match what the row's mechanic accepts: `Customer` for `RECIPIENT_RECOMMENDATIONS`, `Offer` for `PRODUCT_RECOMMENDATIONS`, `Category` for `CategoryProductsComputedField` |
| `readyToUse` | only `true` is taken |
| `status` | only `RecalculationRequested` or `RecalculationFinished` are taken — two statuses out of eight |

The lookup returns the suitability fields, and the agent must apply them before generation: preview/save do not
prove that the mechanic fits the chosen row or is ready for calculation. So the choice is made by the three
columns, not by the first matching row. With no suitable one there is nothing to build a recommendations row with, and another filling mechanic
is the way out. A mechanic the person names goes through the same three columns — being asked for is not a
column. One that fails them is not written; the column it failed names the reason,
because nothing further down the line will catch it and the block goes out empty.

Two pairs are easy to confuse, and mixing them up means building a row with the wrong iteration entity:

- **`ORDER` vs `ORDER_PRODUCTS`.** The first iterates over order lines and wants `OrderItem*` chips; the second
  iterates over the products of those lines and wants `Product*`. If you need the name and price of a product
  from an order, that is `ORDER_PRODUCTS`; if the amount and quantity per order line, that is `ORDER`.
- **`ProductListItem` vs `FROM_PRODUCT_LIST`.** The first is one list line, and it draws one card
  (`columnCount` and `rowCount` are not needed); the second iterates over the whole list.

`filterBySegmentDetails` is an object `{ "systemName": …, "internalId": … }`, and it is needed only when
`enabledFilterBySegment` is on.

**The system name and internalId are not two ways of saying one thing, but two different readers.** The system
name goes into the sent email (`Recipient.GetProductList("...")`) — without it the campaign cannot be
built. `internalId` does not get into the email, and does two other things: by it the editor shows which list
is selected (the select looks it up by `internalId` and looks at nothing else), and by it the email's dependency
on the list is declared — what keeps the platform from deleting a list in use.
Write only the system name and the list expression will be built, but the user, opening the row in the
editor, will see an **empty select**, as if no list were selected, and the platform will consider the list
unused. The same goes for a segment (`segmentSystemName` + `segmentationInternalId`) and for a computed field.
The canvas writes `productListId` as a third field but never reads it — do not invent it yourself, and if you
see it in an email you are editing, leave it as is.

**Where to get the values.** A product list — entity `ProductList`: **`systemName` and
`internalId` are taken from the same result row**, like the product identifier triple. Recommendation mechanics —
entity `RecommendationMechanic`; the lookup returns `systemName`, `name`, `target`,
`readyToUse` and `status`, and the agent applies the suitability rules above. This file does not describe a
lookup for segments: a segment is taken from the user or from the email you are editing. An example of a mechanic with a list:

```jsx
<CollectionRow dataSource={{ "key": "FROM_PRODUCT_LIST", "model": { "settings": { "model": { "productListSystemName": "<PRODUCT_LIST_SYSTEM_NAME_FROM_LOOKUP>", "productListInternalId": "<PRODUCT_LIST_INTERNAL_ID_FROM_LOOKUP>" } } } }}>
```

Do not copy this fragment before the lookup. The values `<PRODUCT_LIST_SYSTEM_NAME_FROM_LOOKUP>` and
`<PRODUCT_LIST_INTERNAL_ID_FROM_LOOKUP>` must be replaced with the values from one row of
the lookup of entity `ProductList`; preview/save do not check that the list exists.

- **Some mechanics work only in an automated campaign.** They read a customer action, and a bulk
  campaign has no action — the row will go out empty. These are `ORDER`, `ORDER_PRODUCTS` (order products),
  `ViewedProducts`, `ViewedProductsInSession`, `ProductView`, `SessionProductCategoryViews`,
  `SessionGetAddedToListProducts`, `RecentlyBoughtProducts`. Independent of the campaign kind are
  `RECIPIENT_RECOMMENDATIONS`, `PRODUCT_RECOMMENDATIONS`, `FROM_PRODUCT_LIST`, `FROM_SEGMENT`,
  `ProductShowcase`. The converter itself lists everything it accepts in the error message; the campaign kind
  is set at creation and does not change afterwards.

## Manually selected list

`ProductShowcase` — the mechanic set by the “Fill manually” toggle — holds one
`<CollectionCard>` per selected product, and each card names its product with the `product`
attribute: the triple `internalId`, `externalId`, `externalSystemName`, as the lookup prints it in a row.
A card without content is drawn by the template; a card with its own columns — by them. The template in the
example below is cut down to one element so that the cards themselves are visible; the card styling is taken
from the beginning of the file, not from here:

```jsx
<CollectionRow dataSource={{ "key": "ProductShowcase" }} orientation="vertical" columnCount={{ "value": 3 }}>
  <CardTemplate url={[<Var param="ProductUrl" />]}><Column size={12}><Text><p style="margin: 0"><Var param="ProductName" formatString={{ "isTruncateEnabled": false }} /></p></Text></Column></CardTemplate>
  <CollectionCard product={{ "internalId": "<PRODUCT_INTERNAL_ID_FROM_LOOKUP>", "externalId": "<PRODUCT_EXTERNAL_ID_FROM_LOOKUP>", "externalSystemName": "<PRODUCT_EXTERNAL_SYSTEM_NAME_FROM_LOOKUP>" }} />
  <CollectionCard product={{ "internalId": "<SECOND_PRODUCT_INTERNAL_ID_FROM_LOOKUP>", "externalId": "<SECOND_PRODUCT_EXTERNAL_ID_FROM_LOOKUP>", "externalSystemName": "<SECOND_PRODUCT_EXTERNAL_SYSTEM_NAME_FROM_LOOKUP>" }} url={[<Var param="ProductUrl" />]}><Column size={12}><Text>This exact one</Text></Column></CollectionCard>
</CollectionRow>
```

Do not copy this fragment before the lookup. Each `product` triple must be replaced with the exact
`internalId`/`externalId`/`externalSystemName` from the lookup of entity `Product` or from the email
you are editing.

The rules of such a row, and breaking any of them is an error:

- **A card always names a product.** A card that names none is not a second template but an error
  ("No products selected yet", above).
- **The triple is written in full and is not invented.** Two values out of three are not derived from the third, so
  a product named incompletely or with an extra field is rejected. The triple is taken from the lookup or from the
  email you are editing. Do not write an invented triple: preview/save do not prove that such a product exists and
  is usable.
- **Do not write keys or the `selections` map.** The row knows the product under its own name, but that name is
  made by the converter, like all other ids of the document. An email read from the editor sometimes comes in the
  old form — `selectionId="…"` instead of `product` — it is readable and does not need rewriting; but both forms
  on one card are rejected: a product is named once.
- **Products are looked up as entity `Product`.** The user names a product in words
  (“Home Alone quest”), by vendor code or by external id — any of the three is one search string.
  The result row has exactly the triple the card asks for: `internalId`, `externalId`, `externalSystemName` — and
  next to it `name`, `price`, `vendorCode`, `isAvailable`, `url`, `pictureUrl`, so the person can recognize the product.

  **Several rows can match one name.** The catalog holds many products with the same name; price and vendor code
  are printed to tell them apart, and `isAvailable: false` marks one not for sale. A name that matches nothing is
  found by vendor code or external id, or the row goes without cards (below).
- **Product data is filled in on its own — it does not need to be passed.** The email stores only the identifier
  triple per card, and the preview itself reads the name, price and image from the project catalog
  by these triples. It is enough for you to name the product correctly in `product` — the rest will appear in the
  preview without your involvement, and there is no need to restate product data in the call. A product that is
  no longer in the catalog will be drawn by the card as a placeholder; all cards will be drawn the same way if the
  catalog is unavailable — the layout will render in any case. A personal price and bonuses will never be in the
  preview: they are individual for each recipient, and nobody knows them before sending.
- **No products selected yet — the row without cards** ("No products selected yet", above), the products are selected
  later, in the editor or by name for a lookup; cards are added when they appear.
- **Cards exist only under `ProductShowcase`.** Under a mechanic that finds products itself, the row would
  draw the cards and leave the mechanic unread.
- **A card without its own content needs a `<CardTemplate>`** in the row — otherwise there is nothing to draw it
  with. And such a card carries nothing but the named product: a setting on it would be lost, so it is
  rejected.

## Card heights and `autosizeKey`

`height` on a card element carries, next to the height, an **autosize key**: elements with the same key are
measured together and take the height of the tallest one. The template is drawn once per product, so its
elements are one group by themselves; the key matters where several cards carry their own content.

**Measured together — only with `settingType: "manual"`.** It has two values, and they decide different things.
`manual` — height as a number in px, and the element joins the autosize group: this is exactly how the row's
cards keep the same shape whatever the products. `original` — height by content, and the element **drops out**
of alignment: it will have no group in the markup, and an `autosizeKey` next to it does nothing. Do not align
text with a key while leaving it `original` — the key will be set, but the heights will not match.

**The default differs between elements, and for a reason**: an image is 220 px `manual`, a `<Split>` 58 px
`manual`, a text `original`. Text length cannot be guessed in advance, so text has height by content, while
products come in different proportions, so the image has a fixed one. A height container reserves its space even
when the content is shorter: in a card this is the main source of a broken rhythm. When writing it yourself, stick to the same: `original` for text, a number for the image and the splitter.

**Image height in the editor's layouts is 180** for three in a row and for the list, **260** for two in a row;
if you take a layout from there, take this too. For your own layout, compute from the card width: email width
minus the block's side `innerSpacing` minus `cardGap` between cards, divided by their number. Otherwise the
default container will leave empty space under a square photo.

- **Do not invent a uuid for the key.** It reads as carried over from a saved email, but it groups
  emptiness — the card will silently drop out of the height it was supposed to share.
- **A key you did not write will appear on its own.** The converter issues a fresh one to every card element
  that had no key — so after reading the email you will see a uuid where you set nothing. This is
  not the same as an invented one: it is real, the element is in its group. When editing such an email, carry it
  over as is.
- **The key is either not written** (the card is measured by itself), **or carried over** from the email you are
  editing, **or it is a name in words** for a group you have in mind: `autosizeKey: "the-picked-two"` on two
  cards will put them at the same height.
- A card with its own content stands in its own group by default — the same as a detached card on the
  canvas: its height becomes the author's business, which is what detaching is for. Two such cards side by side
  therefore differ in height when their content does — one `autosizeKey` evens them out.

## Attributes of elements inside a card

A card holds the plain elements and `<Labels>` (`wiki/label.md`); the editor does not offer `Menu`, `BulletList`
or `Socials` there (`wiki/groups.md`).

An element in a card carries settings it does not have in an ordinary column — outside a card the same
attributes will be `Unknown attribute`:

| Attribute | On | What it does |
|---|---|---|
| `height` | `Text`, `Image`, `Split` | Element height and autosize key. JSON: `{ "settingType": "original" \| "manual", "height": 180, "mobile": { … }, "autosizeKey": "…" }`. How the values differ and what to write by default — above, “Card heights and `autosizeKey`” |
| `url` | `Text`, `Divider` | the product link, as on the card itself ("The card's `url`", above) |

## Attributes of row containers

| Container | Attributes |
|---|---|
| `CollectionRow` | `dataSource`, `columnCount`, `rowCount`, `orientation`, `cardGap`, `rowGap`, `isCheckerboardEnabled`, `background`, `border`, `borderRadius`, `innerSpacing`, `isColumnsMobileAdaptive`, `columnVerticalDirection`, `visibilityOnDevices` |
| `CardTemplate` | `url`, `columnGap`, `verticalAlign`, `background`, `border`, `borderRadius`, `innerSpacing` |
| `CollectionCard` | the same as `CardTemplate`, plus the required `product` — the product the card stands for |

Row value forms: `columnCount` and `rowCount` — `{ "value": N }`; `cardGap` and `rowGap` —
`{ "size": N, "mobile": { "size": N } }`; `orientation` — a string: `"horizontal"` (default) draws one
card per line and does not read the column count, `"vertical"` gives a `columnCount` × `rowCount` grid. A wrong
form is refused with the default shown, cut at 70 characters.

`url` on a card makes the whole card lead to the product — "The card's `url`", above.
