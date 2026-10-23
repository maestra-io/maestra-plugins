---
description: "What the preview and the editor canvas draw that the sent email does not: links as #, sample values, placeholders, blurred device-hidden blocks, a preview without a format — and what not to fix because of it"
---

# The canvas — what the preview shows

The preview draws the email the way the editor's work area draws it, in editing mode: a layout to
check, not the bytes a recipient gets. Each line below is the canvas, not a defect of the JSX, and nothing here is
repaired by changing the document.

| on the canvas | in the sent email | home |
|---|---|---|
| every `<a>` inside `<Text>` is `href="#"`, a real address included; a `Button`/`Image` url is `#` when it holds a chip | the written address; the chip's value substituted at send time | — |
| chips show sample values; no `${…}` token is visible in the HTML | the recipient's data | [personalization.md](personalization.md) |
| a text chip with truncation on is padded with repeats up to its limit | the real value, cut at the limit | [personalization.md](personalization.md), "Long text" |
| an element with an empty variable is always visible | hidden, or its space kept, per `emptyVariableBehavior` | [personalization.md](personalization.md), "An empty variable" |
| an empty `<Column />` draws a drop zone | nothing | [containers.md](containers.md), "`<Column>`" |
| a static `<Image />` with no source draws a placeholder | the platform's `data:` placeholder | [image.md](image.md) |
| a dynamic image draws the placeholder picture for personal content | the field's file; an empty field — nothing, or the space, per `emptyVariableBehavior` | [image.md](image.md) |
| a block or row hidden for the current device is drawn **blurred** (`visibilityOnDevices`) | hidden by a media query, absent from that device's layout; the desktop picture shows only the desktop branch, the mobile one only the mobile | — |
| a label or a group where the editor has no such node draws fine | it is sent, but it is a node the editor cannot show | [label.md](label.md), [groups.md](groups.md) |
| without the template the email takes its settings from — the campaign's or a saved one — or with one that has nothing saved, its width, background, CSS and letter styles are absent — a `<Theme>` and the root attributes written in the JSX still draw | the template's own under the document | pass that template to the preview |

What follows from the table:

- addresses, the unsubscribe token and chip settings are checked against the JSX, never against the canvas HTML;
- device-hidden duplicates are not removed for a clean canvas — that silently sacrifices the mobile layout; a user
  alarmed by "blurred cards" is told they are the hidden device variants, and giving up responsive variants for one
  layout is a product decision made with the user;
- a successful preview proves the layout, not the data: an invented `systemName`, a missing lookup value or a
  string field in a boolean filter draw just as well.
