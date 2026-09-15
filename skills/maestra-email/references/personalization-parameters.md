# Personalization parameters — what can be assembled from JSX

**When to read:** the root parameter you need is not among the common ones in `personalization.md`, or you need to check its exact attributes and the campaign-kind restriction.

**Return to:** `personalization.md`, then Self-check in `SKILL.md`; do not substitute a product parameter for a root parameter and do not use an automated-only parameter in a Manual campaign.

The 43 parameters of the email itself, with the attributes of each. The remaining 125 are product parameters; they live only inside
a product row and are listed in [product-parameters.md](./product-parameters.md).

**The entity decides where a parameter can stand, and the campaign kind — whether it is available at all.** An email parameter
(`root`) stands anywhere in the email, order data included: the 21 rows marked *(automated only)*
read the order, and in a bulk campaign they have nothing to read, while in an automatic email such a parameter stands
anywhere — in the heading, in the text, in a button — and not only in a product-row card. Three of them
read not the order itself but a level inside it: `OrderItemStatusName` — an order line, `OrderPaymentAmount`
and `OrderPaymentType` — a payment; in the email body they will go out empty. The four special links, the authentication
ticket and both personal prices are provided by the email channel itself; they are available to any kind.

A setting attribute that refers to a project catalogue (`customFieldType`, `externalSystem`,
`orderExternalIdSelection`, `promoCodePool`, `balance`, `hostname`) is required: the converter rejects a chip in
which it is not filled in; if an empty setting did make it into the email, late validation answers with
a broken-expression error. The rules are in `personalization.md`.

The list was taken from the platform at the time the skill was built. A parameter that appeared on the platform later can be authored and
works, but it will not be in this list — if the user names a parameter that is not here, do not
refuse right away; try it and see whether the converter accepts it.

### The email itself (`root`)

| `param` | its attributes |
|---|---|
| `EmailAuthenticationHexTicket` | `caseFormatter`, `affixVariableText` |
| `EmailAuthenticationTicket` | `caseFormatter`, `affixVariableText` |
| `EmailConfirmationLinkTicket` | `caseFormatter`, `affixVariableText` |
| `MailingSendingDateTime` | `formatDateTime`, `affixVariableText` |
| `OrderAppliedDiscount` *(automated only)* | `discountSettings`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderBaseAmount` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderBaseAmountFull` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderChargedBonuses` *(automated only)* | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `OrderCustomFieldDate` *(automated only)* | `customFieldType`, `formatDate`, `affixVariableText` |
| `OrderCustomFieldDateTime` *(automated only)* | `customFieldType`, `formatDateTime`, `affixVariableText` |
| `OrderCustomFieldDecimal` *(automated only)* | `customFieldType`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderCustomFieldEnum` *(automated only)* | `customFieldType`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderCustomFieldInteger` *(automated only)* | `customFieldType`, `numericFilter`, `formatInteger`, `affixVariableText` |
| `OrderCustomFieldString` *(automated only)* | `customFieldType`, `formatString`, `caseFormatter`, `affixVariableText` |
| `OrderDateTime` *(automated only)* | `formatDateTime`, `affixVariableText` |
| `OrderDeliveryCost` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderDiscount` *(automated only)* | `discountSettings`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `OrderEmail` *(automated only)* | `caseFormatter`, `affixVariableText` |
| `OrderExternalId` *(automated only)* | `orderExternalIdSelection`, `affixVariableText` |
| `OrderItemStatusName` *(automated only)* | `caseFormatter`, `affixVariableText` |
| `OrderMobilePhone` *(automated only)* | `caseFormatter`, `affixVariableText` |
| `OrderPaymentAmount` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderPaymentType` *(automated only)* | `caseFormatter`, `affixVariableText` |
| `OrderTotalAmount` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `OrderTotalAmountWithoutDelivery` *(automated only)* | `numericFilter`, `formatDecimalPrice`, `affixVariableText` |
| `PromoCodeExpirationDateTime` | `promoCodePool`, `formatDate`, `affixVariableText` |
| `PromoCodeValue` | `promoCodePool`, `caseFormatter`, `affixVariableText` |
| `RecipientBonusBalance` | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `RecipientCustomFieldDate` | `customFieldType`, `formatDate`, `affixVariableText` |
| `RecipientCustomFieldDateTime` | `customFieldType`, `formatDateTime`, `affixVariableText` |
| `RecipientCustomFieldDecimal` | `customFieldType`, `numericFilter`, `formatDecimal`, `affixVariableText` |
| `RecipientCustomFieldEnum` | `customFieldType`, `formatString`, `caseFormatter`, `affixVariableText` |
| `RecipientCustomFieldIdentifier` | `customFieldType`, `caseFormatter`, `affixVariableText` |
| `RecipientCustomFieldInteger` | `customFieldType`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `RecipientCustomFieldString` | `customFieldType`, `formatString`, `caseFormatter`, `affixVariableText` |
| `RecipientEmail` | `caseFormatter`, `affixVariableText` |
| `RecipientGreeting` | `greetingWithNameInput`, `greetingNoNameInput`, `affixVariableText` |
| `RecipientMobilePhone` | `caseFormatter`, `affixVariableText` |
| `RecipientNearestExpirationBonuses` | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `RecipientNearestExpirationBonusesDate` | `balance`, `formatDate`, `affixVariableText` |
| `SpecialLinkAccessibilityLink` | `affixVariableText` |
| `SpecialLinkTopicUnsubscribeLink` | `affixVariableText` |
| `SpecialLinkUnsubscribeLink` | `affixVariableText` |

## Product parameters live separately

Besides the email, parameters have five more entities — a product, a viewed product, a product-list line,
the single list line and an order line. These are the remaining 125 parameters, and they are listed by entity in
[product-parameters.md](./product-parameters.md). They come alive only inside the product row
`<CollectionRow>` with its cards ([product-rows.md](./product-rows.md)): such a chip placed in a regular column
is not a correct way to output a product. Do not use product chips outside a product-row
card.

**When asked to output the order's products, the cart, recommendations or viewed products, do not pick a similar
parameter from the list above** — build a product row.
