# Product parameters — only inside a product row

**When to read:** the needed product value is not in the short table of `product-rows.md`, or you need to pick a product `<Var>` for a card.

**Return to:** `product-rows.md`, then to Self-check in `SKILL.md`; the parameter must match the entity the chosen mechanic iterates.

Five product entities — a product (`product`), a viewed product (`productView`), a product list line
(`productListItem`), the only line of a list (`singleProductListItem`) and an order line (`orderItem`) —
125 parameters out of 168, with the attributes of each. Opened when the needed product value is not in the
"value → parameter name" table in [product-rows.md](./product-rows.md). The parameters of the email itself are in
[personalization-parameters.md](./personalization-parameters.md).

Such a parameter is authored only inside a block that iterates products — that is the product row
`<CollectionRow>` with its cards (`references/product-rows.md`). Do not use product chips outside a card of a
product row: for products, assemble a `<CollectionRow>`.

**The family is chosen not by the author but by the row's mechanic.** A chip of a different entity than the one the mechanic iterates
the converter rejects, and itself names the twin parameter from the right family ("Use `ProductListItemProductName` — the
same value, read from `productListItem`"). The "mechanic → family" table is in `references/product-rows.md`;
here it is repeated in the table headings.

**When asked to show order products, the cart, recommendations or viewed products, do not pick a similar-looking
parameter from the email's list above** — assemble a product row. A row with recommendations or another
automatic mechanic can be assembled from JSX entirely. A row with manually picked products — too: the
products themselves are found by lookup (`entities_list`, `entityType: Product`) or taken from the email you are editing, and
never invented. Nowhere to take them from — assemble the styling and say that the products need to be picked.

## `product` — a product (19)

Mechanics `Recipient.Recommendations`, `Products.GetBySegment`, `SessionGetViewProducts`, `SessionGetAddedToListProducts` and the other twelve — everything except the three below.

| `param` | its attributes |
|---|---|
| `ProductAddToCartUrl` | `hostname`, `externalSystem`, `amount`, `discountQuery`, `destinationRoute`, `productSegment`, `affixVariableText` |
| `ProductBonus` | `inputLimitSetting`, `productSegment`, `numericFilter`, `formatDecimal`, `pluralizationAffix`, `affixVariableText` |
| `ProductCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `ProductCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `ProductCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `ProductCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductDescription` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductDiscount` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductExternalId` | `externalSystem`, `productSegment`, `affixVariableText` |
| `ProductName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductOldPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductPersonalPrice` | `personalPriceTypeSettings`, `inputLimitSetting`, `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixPersonalPriceEditor`, `affixVariableText` |
| `ProductPictureUrl` | `productSegment` |
| `ProductPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductUrl` | `productSegment`, `affixVariableText` |
| `ProductVendorCode` | `productSegment`, `caseFormatter`, `affixVariableText` |
| `ProductVendorName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |

## `productListItem` — a product list line (33)

Mechanic `FROM_PRODUCT_LIST` — the row iterates a product list of the project.

| `param` | its attributes |
|---|---|
| `ProductListItemCount` | `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemCurrentPriceOfLine` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `ProductListItemCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `ProductListItemCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `ProductListItemCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemDiscountByOldProductPrice` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemDiscountByPriceOfLine` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemOldPriceOfLine` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemPriceOfLine` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemProductAddToCartUrl` | `hostname`, `externalSystem`, `amount`, `discountQuery`, `destinationRoute`, `productSegment`, `affixVariableText` |
| `ProductListItemProductBonus` | `inputLimitSetting`, `productSegment`, `numericFilter`, `formatDecimal`, `pluralizationAffix`, `affixVariableText` |
| `ProductListItemProductCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `ProductListItemProductCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `ProductListItemProductCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemProductCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `ProductListItemProductCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductDescription` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductDiscount` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemProductDiscountByPriceInList` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductListItemProductExternalId` | `externalSystem`, `productSegment`, `affixVariableText` |
| `ProductListItemProductName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductOldPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemProductPersonalPrice` | `personalPriceTypeSettings`, `inputLimitSetting`, `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixPersonalPriceEditor`, `affixVariableText` |
| `ProductListItemProductPictureUrl` | `productSegment` |
| `ProductListItemProductPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductListItemProductUrl` | `productSegment`, `affixVariableText` |
| `ProductListItemProductVendorCode` | `productSegment`, `caseFormatter`, `affixVariableText` |
| `ProductListItemProductVendorName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |

## `singleProductListItem` — the only line of a list (26)

Mechanic `ProductListItem`.

| `param` | its attributes |
|---|---|
| `SingleProductListItemCount` | `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `SingleProductListItemCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `SingleProductListItemCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `SingleProductListItemCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `SingleProductListItemCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `SingleProductListItemCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `SingleProductListItemProductAddToCartUrl` | `hostname`, `externalSystem`, `amount`, `discountQuery`, `destinationRoute`, `productSegment`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `SingleProductListItemProductCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemProductDescription` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemProductDiscount` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `SingleProductListItemProductDiscountByPriceInList` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `SingleProductListItemProductExternalId` | `externalSystem`, `productSegment`, `affixVariableText` |
| `SingleProductListItemProductName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemProductOldPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `SingleProductListItemProductPictureUrl` | `productSegment` |
| `SingleProductListItemProductPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `SingleProductListItemProductUrl` | `productSegment`, `affixVariableText` |
| `SingleProductListItemProductVendorCode` | `productSegment`, `caseFormatter`, `affixVariableText` |
| `SingleProductListItemProductVendorName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |

## `orderItem` — an order line (28)

Mechanic `ORDER` — the row iterates the order's line items.

| `param` | its attributes |
|---|---|
| `OrderItemAmount` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderItemBaseAmount` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderItemBasePricePerUnit` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderItemCount` | `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderItemCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `OrderItemCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `OrderItemCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderItemCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `OrderItemCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemDiscount` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderItemDiscountPerUnit` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderItemPricePerUnit` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderItemProductAddToCartUrl` | `hostname`, `externalSystem`, `amount`, `discountQuery`, `destinationRoute`, `productSegment`, `affixVariableText` |
| `OrderItemProductCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `OrderItemProductCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `OrderItemProductCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderItemProductCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemProductCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `OrderItemProductCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemProductDescription` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemProductExternalId` | `externalSystem`, `productSegment`, `affixVariableText` |
| `OrderItemProductName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemProductPictureUrl` | `productSegment` |
| `OrderItemProductUrl` | `productSegment`, `affixVariableText` |
| `OrderItemProductVendorCode` | `productSegment`, `caseFormatter`, `affixVariableText` |
| `OrderItemProductVendorName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderItemStatus` | `productSegment`, `caseFormatter`, `affixVariableText` |

## `productView` — a viewed product (19)

Mechanic `ProductView`.

| `param` | its attributes |
|---|---|
| `ProductViewPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductViewProductAddToCartUrl` | `hostname`, `externalSystem`, `amount`, `discountQuery`, `destinationRoute`, `productSegment`, `affixVariableText` |
| `ProductViewProductCustomFieldDate` | `customFieldType`, `productSegment`, `formatDate`, `affixVariableText` |
| `ProductViewProductCustomFieldDateTime` | `customFieldType`, `productSegment`, `formatDateTime`, `affixVariableText` |
| `ProductViewProductCustomFieldDecimal` | `customFieldType`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductViewProductCustomFieldEnum` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductViewProductCustomFieldInteger` | `customFieldType`, `productSegment`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `ProductViewProductCustomFieldString` | `customFieldType`, `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductViewProductDescription` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductViewProductDiscount` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductViewProductDiscountByViewedPrice` | `discountSettings`, `productSegment`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `ProductViewProductExternalId` | `externalSystem`, `productSegment`, `affixVariableText` |
| `ProductViewProductName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
| `ProductViewProductOldPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductViewProductPictureUrl` | `productSegment` |
| `ProductViewProductPrice` | `productSegment`, `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `ProductViewProductUrl` | `productSegment`, `affixVariableText` |
| `ProductViewProductVendorCode` | `productSegment`, `caseFormatter`, `affixVariableText` |
| `ProductViewProductVendorName` | `productSegment`, `formatString`, `caseFormatter`, `affixVariableText` |
