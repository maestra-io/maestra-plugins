---
description: "An image in an email: a source from a file or a parameter, click, size, alignment, alt text on every image, socials lines, an image as the email background, what the preview shows"
---

# Image — `<Image>`

A standalone element of a column or a line of `<Socials>`. No content, always a single tag; the source is set by
the mandatory `image` attribute.

## Source

`image` takes two modes.

**A file** — `mode: "static"`: the address and the file name.

```jsx
<Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
```

`url` is the address the image is loaded from in the email. `fileName` is a service name. For an image from the
gallery it is the `fileName` of its row in the gallery search; an image stored in the gallery as WebP is served at the
address of its PNG copy.

**From a parameter** — `mode: "dynamic"`: the address is assembled as a list of segments with a chip, like any
personalized value. In the editor this is the "Personalised picture for the customer" radio button.

```jsx
<Image image={{ mode: "dynamic", dynamic: [<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "<FROM_LOOKUP>", "type": "String", "name": "<FROM_LOOKUP>", "internalId": "<FROM_LOOKUP>" }} />] }} />
```

The parameter's value is the whole address; text before the chip (`dynamic: ["https://cdn.shop.example/",
<Var … />]`) becomes its prefix, and like any literal address in an email it is `https://`. The modes are mutually exclusive: write only the fields of the chosen one — `static`
for a file, `dynamic` for a parameter. The field's value is not checked at conversion: a non-URL value leaves the recipient with an image that
fails to load. An empty value is handled by `emptyVariableBehavior` — in the editor this is "Display
conditions" → "If the variables in the element are empty" — and a chip in `url` or `alt` counts the same as one in
`image`: an empty link field drops the picture itself, not only the click.

An image with no source — `<Image />` — converts, but in place of the address the platform substitutes a
built-in `data:` placeholder.

## Attributes

| attribute | what it does | default |
|---|---|---|
| `image` | the source, see above | mandatory |
| `url` | the click address — an HTTPS string or a list of segments with a chip: `url={["https://shop.example/points/", <Var … />]}` or a single `<Var>` as a whole; the converter does not validate the click address | no link |
| `size` | the size of a standalone image: `{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }` in pixels, or `{ type: "manual", width: N }` as a percentage of the column | `{ type: "inherit" }`: the full width of the column, and a narrower file is scaled up and blurred — a logo or an icon gets an explicit `size` |
| `align` | `{ align: "left" \| "center" \| "right", mobile: { align: "…" } }` | `{ align: "center" }` |
| `alt` | the caption in place of an image that failed to load: a string or a list of segments with a chip | empty |
| `emptyVariableBehavior` | what happens to the image in the sent email when a variable in its `image`, `url` or `alt` is empty — as on any element, [personalization.md](personalization.md), "Empty value" | `"hide"` |
| `innerSpacing` | as for `Block` | 0 on every side |
| `border`, `borderRadius`, `visibilityOnDevices` | as for `Block` | no border, no rounding, `"all"` |

`size` and `align` belong on the image itself: a narrower picture is not centred with side columns or side
`innerSpacing`, and a logo or an icon always gets a `size`.

In emails built in the editor `size` also carries `equalizedImageMaxWidth`: a string with the width of the
container, which the editor measures itself once the image has loaded on the canvas. It is not written for a
new image and is carried over as is when editing.

Inside a product row card an image also has `height` — [product-rows.md](product-rows.md).

## Alt text — always set it

Every image gets alt text wherever the format allows it — a Maestra rule, not optional polish. Many mail clients
block images by default, and the alt is what the recipient reads instead; screen readers read it too.

- **`<Image>`** — `alt="…"`. In a product row card it is the product name chip ([product-rows.md](product-rows.md));
  everywhere else a plain string.
- **`<img>` inside `<Html>`** — an `alt="…"` attribute on every `<img>` ([html.md](html.md)).
- **`<Socials>` lines** — the network name: `alt="Instagram"`, `alt="Facebook"`.
- **What to write:** what the image says or does, in the email's language. A banner with text → its text, shortened
  to the essentials (headline, offer, CTA label). A navigation tile or a button drawn as an image → its label
  ("Hot Deals", "Shop now"). A logo → the brand name. A photo → a short description ("Linen duvet set in sage").
  Read the text off the image itself (look at it through Ops's preview or the file); do not guess it from the file
  name.
- A purely decorative image (a spacer, a divider drawn as a picture, a background ornament) gets `alt=""` rather
  than a made-up caption.
- **Carrying over an email** (a copy, a port from another platform, a raw-HTML rebuild): keep the source's alt when
  it is meaningful; when it is missing, empty on a non-decorative image, or a placeholder ("image", "banner", a
  file name), write a proper one. Name in the response that alt text was added.
- When editing an existing email, add missing alt text to the images you touch; offer — not silently perform — the
  same for the rest of the email.

## `<Socials>` lines

Socials lines are the same `<Image image={{…}} />`; their size and alignment are set by the group:
`Socials.imageSize`, the `fixed` form of `size` only, and `Socials.align`.

## An image as the email background

`Template.background` accepts an image; the address is the same kind of source as for `<Image>`:

```jsx
<Template background={{
  type: "image",
  url: "https://cdn.example.com/background.jpeg",
  fileName: "background.jpeg",
  fallbackColor: "#ffffff",
  mode: "cover"
}}>
```

| `mode` | what it does |
|---|---|
| `cover` | fills the background area, cropping the excess along one side |
| `contain` | fits the image whole, leaving empty space along the other |
| `stretch` | stretches it over the whole area, distorting the proportions |
| `repeat` | tiles it with copies |

`fallbackColor` is the colour the recipient sees instead of the image: some email clients do not show a
background image at all, so the text on top must stay readable on the fallback colour, and an image that
carries meaning goes into `<Image>`, not into the background.

## In the preview

A static image with no source is drawn as a placeholder, a dynamic one as the placeholder picture for personal
content; a `url` with a chip is `href="#"` — [canvas.md](canvas.md).

## Where the address comes from

A link or a file the user gives — a `data:`/`blob:` string too — is uploaded to the gallery and
comes back as a gallery address; a mockup or a screenshot is a reference, not a source. An image already in the gallery is found by
a gallery search by a fragment of the name; several rows can match one name, and nothing in a row tells them apart but the
picture itself. A file that never reached the gallery has no address. Images inside a library block stay as they
came, like the rest of the block.
