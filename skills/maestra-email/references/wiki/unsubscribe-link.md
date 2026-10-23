---
description: "The unsubscribe link: the canonical anchor inside Text and the chip in a button or image, the ready-made footer, the two accepted reasons for leaving it out, what the preview shows, a SyncBlock that hides it"
---

# Unsubscribe link

A marketing email leaves with one canonical unsubscribe link in the footer, in small grey text; it is left out only
for a transactional email or when the wrapper or the campaign settings carry it. This page is the forms, the footer and
the diagnostics.

## The two forms

In the preview both forms show `href="#"`: not a defect and not a reason to replace the token or the chip — [canvas.md](canvas.md).

**Text link** — the default. The exact token `${Message.UnsubscribeLink}` as the plain-string `href` of an `<a>` inside
`<Text>`. This is the one place a raw `${...}` template token is written instead of a chip: an attribute of the markup must be a
plain string, and a `<Var>` in `href` is refused, so no chip can stand there. The caption, when the user names none, is the standard one: "If you no longer want these emails — unsubscribe"; for an email in another language translate it, keeping the anchor and the token.

```jsx
<Text><p style="margin: 0;">If you no longer want these emails — <a href="${Message.UnsubscribeLink}">unsubscribe</a></p></Text>
```

**Button or clickable image** — when the user asks for a button. In a prop value the chip works, and unsubscribe has
its own parameter, `SpecialLinkUnsubscribeLink`, whose expression is exactly `Message.UnsubscribeLink`. The exact token
as a plain string, `url="${Message.UnsubscribeLink}"`, works too; the chip is preferred because the editor shows it
as the unsubscribe link, while the token is just text in the link field.

```jsx
<Button url={[<Var param="SpecialLinkUnsubscribeLink" />]}>Unsubscribe</Button>
```

Nothing else is an unsubscribe link: not an invented address, not a preferences page, not another token.

## The ready-made footer

English email; for another language the paragraph is translated, the anchor and the token stay.

```jsx
<Block innerSpacing={{ "top": 20, "bottom": 20, "left": 24, "right": 24, "mobile": { "top": 16, "bottom": 16, "left": 16, "right": 16 } }}>
  <FlexRow><Column size={12}>
    <Text style={{ "fontSize": 12, "color": "#888888", "link": { "color": "#888888" }, "mobile": { "fontSize": 11 } }}>
      <p style="margin: 0;">If you no longer want these emails — <a href="${Message.UnsubscribeLink}">unsubscribe</a></p>
    </Text>
  </Column></FlexRow>
</Block>
```

## Inside a `<SyncBlock>`

**A `<SyncBlock>` hides its content from the JSX, the link included,** while the preview draws it. An email with a
`<SyncBlock>` and no canonical link in its JSX: look at the preview where the sync block stands. An unsubscribe
caption there — the link is inside the block: no second link, nothing written into the sync block ([sync-block.md](sync-block.md)). No caption there — the usual rule, the link is added.
