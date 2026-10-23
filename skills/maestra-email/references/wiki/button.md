---
description: "The button: attributes and their value shapes, what the converter accepts in url, width in percent or pixels"
---

# Button — `<Button>`

The caption is the content between the tags: plain text or a list of segments with a chip ([personalization.md](personalization.md)), no markup.

## `url`

An empty or absent `url` is saved as a button with an empty link: visible in the email, not clickable. A written
value is checked against a loose pattern: `https://…`, `http://…`, `tel:…`, `mailto:…`, an address without a scheme
(`shop.example/sale`, which the email then carries as a relative link) and the bare `https://` all pass. The link type is inferred from the value (`tel:` → phone, `mailto:` → email, else website);
`href` is not an attribute. A value with a chip is not checked.

## No address

Placeholders — `https://`, `#`, `/`, `about:blank`, `https://example.com` — are not addresses; a written address carries
its scheme. The forms of an element left without one: a `<Button>` without `url` (visible, not clickable, like a fresh
one in the editor), an `<Image>` without `url`, a `<Menu>` text line as plain words without an `<a>`. A button is not
imitated with a column with a background and text. An image nobody asked to make clickable gets no `url`; in a product
row card the link is the product chip ([product-rows.md](product-rows.md)).

## Attributes

| attribute | value | when absent | written in part, the fields left out |
|---|---|---|---|
| `url` | `"https://…"`, `"tel:…"`, `"mailto:…"`, or a list of segments with a chip | empty link | — |
| `themeVariant` | `"primary"` \| `"secondary"` — which set of the email's letter styles the button follows ([theme.md](theme.md)) | `"primary"` | — |
| `align` | `{ align: "left" \| "center" \| "right", mobile: { align: "…" } }` — visible only while the button is narrower than its column | `{ align: "center" }` | the same |
| `innerSpacing` | as for `Block` — the space around the button | `{ top: 10, bottom: 10, left: 0, right: 0 }` | the same |
| `buttonSize` | `{ height: N, widthType: "percent" \| "pixels", width: N, heightMobile: N, widthMobile: N }` — `width` and `widthMobile` are both read in `widthType` units, so the unit is written next to them; the phone side — [theme.md](theme.md) | letter styles | the same |
| `background` | as for `Block` | letter styles | the same |
| `simpleTextStyles` | `{ font: { family }, fallbackFontFamily, fontSize: N, lineHeight: "1.15", letterSpacing: N, color: "#RRGGBB", inscription: [], mobile: { fontSize: N } }` — fields, font lists and `inscription` values in [typography.md](typography.md) | letter styles | the same |
| `border` | as for `Block` | letter styles | the same |
| `borderRadius` | as for `Block` | letter styles | the same |
| `emptyVariableBehavior` | as on any element with a chip — [personalization.md](personalization.md) | `"hide"` | — |
| `iconDisplay` | `{ position: "LEFT" \| "RIGHT" \| "EMPTY" }` — where the icon stands; `EMPTY` is no icon | `{ position: "EMPTY" }`; a line of `<Menu>` — [groups.md](groups.md) | — |
| `iconSrc` | `{ url, fileName }` — a gallery image, like any image source | a platform placeholder icon, hidden while `iconDisplay` is `EMPTY` | — |
| `iconAlt` | string | empty | — |
| `iconSizeInPercents` | `{ widthInPercents: N }` — the icon's share of the button width | `{ widthInPercents: 25 }` | the same |

Plus `visibilityOnDevices`, as on any element.

"letter styles": from the email's styles for the `themeVariant`, frozen once the node has a look of its own
([theme.md](theme.md)).

A percent width is a share of the column's width and shrinks with it on mobile. On the phone the width is
`widthMobile`, in the same unit: a pixel one stays in pixels (`width: 240px !important`), so in a column narrower than
the value the button is cut off. A button that names no `buttonSize` takes the size of its variant's styles — on the
platform's `primary` 160 px, 150 on the phone, height 50, wider than a column of 4 twelfths, so a button in a narrow
card or column gets its own `buttonSize` (`secondary` is 70% of the column). «240 px on the desktop, full width on the
phone» is not expressible; the two ways out are percent on both, or pixels with a `widthMobile` that fits the phone.

