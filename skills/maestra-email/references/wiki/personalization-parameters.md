---
description: "Every root <Var> parameter of the email with its attributes, and which ones work only in an automated campaign"
---

# Personalization parameters — what can be built from JSX

A root parameter is not a product parameter, and an *(automated only)* parameter is empty in a bulk (`Manual`) campaign ([personalization.md](personalization.md)).

49 parameters of the email itself, with the attributes of each. The other 127 are product parameters; they live only inside
a product row and are listed in [product-parameters.md](./product-parameters.md).

**The entity decides where a parameter can go, and the campaign kind decides whether it is available at all.** An email parameter
(`root`) goes anywhere in the email, including order data: the 26 rows marked *(automated only)*
read the order, and in a bulk campaign they have nothing to read, while in an automated email such a parameter goes
anywhere — in a heading, in text, in a button — and not only in a product row card. Three of them
read not the order itself but a level inside it: `OrderItemStatusName` — an order line, `OrderPaymentAmount`
and `OrderPaymentType` — a payment; in the email body they will be sent empty. The three special links and the authentication
ticket are provided by the email channel itself; they are available to any kind.

A setting attribute that refers to a project reference list is required — which ones, and where each is looked up:
`personalization.md`, "Settings from a lookup".

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
| `MailingTopicName` | `caseFormatter`, `affixVariableText` |
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
| `OrderPresentmentGiftCardAmount` *(automated only)* | `numericFilter`, `formatMoney`, `affixVariableText` |
| `OrderPresentmentTotalAmount` *(automated only)* | `numericFilter`, `formatMoney`, `affixVariableText` |
| `OrderPresentmentTotalDiscounts` *(automated only)* | `discountSettings`, `numericFilter`, `formatMoney`, `affixVariableText` |
| `OrderPresentmentTotalShipping` *(automated only)* | `numericFilter`, `formatMoney`, `affixVariableText` |
| `OrderPresentmentTotalTax` *(automated only)* | `numericFilter`, `formatMoney`, `affixVariableText` |
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
| `RecipientGreeting` | `affixVariableText` — the greeting words; see “What a chip prints on its own” in [personalization.md](./personalization.md) |
| `RecipientMobilePhone` | `caseFormatter`, `affixVariableText` |
| `RecipientNearestExpirationBonuses` | `balance`, `numericFilter`, `formatInteger`, `pluralizationAffix`, `affixVariableText` |
| `RecipientNearestExpirationBonusesDate` | `balance`, `formatDate`, `affixVariableText` |
| `SpecialLinkAccessibilityLink` | `affixVariableText` |
| `SpecialLinkTopicUnsubscribeLink` | `affixVariableText` |
| `SpecialLinkUnsubscribeLink` | `affixVariableText` |

## Product parameters are listed separately

Besides the email, parameters have five more entities — product, viewed product, product list row,
single list row and order line. These are the remaining 127 parameters, and they are listed by entity in
[product-parameters.md](./product-parameters.md); they stand only inside a product row card
([personalization.md](./personalization.md), "Where a chip stands").

**When asked to display order products, a cart, recommendations or viewed products, do not pick a similar
parameter from the list above** — build a product row.
