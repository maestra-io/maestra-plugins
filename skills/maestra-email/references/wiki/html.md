---
description: "The Html element: raw markup as a quoted string, its one attribute, what Html is not for"
---

# Html — `<Html>`

Raw email markup, passed through as it is. A last resort: only when the standard elements cannot express the design,
or the user asks for arbitrary HTML.

```jsx
<Html>{"<table><tr><td>A table, a comment, an unclosed <br> — anything</td></tr></table>"}</Html>
```

The content is one quoted string `{"…"}`: markup written as JSX between the tags is refused, bare words are joined
into one line. The string reaches the email unchanged. An `<img>` inside it is an image source like any other: an
address the gallery returned, never invented — and it carries an `alt` attribute ([image.md](image.md), "Alt text").

## Attributes

| attribute | value | default |
|---|---|---|
| `visibilityOnDevices` | `"all"` \| `"desktop"` \| `"mobile"` | `"all"` |

Nothing else: spacing, background and width are whatever the markup draws.

Not for aligned cards and CTAs — those are synchronized `<FlexRow>` rows ([containers.md](containers.md)); not for an
editable marker, badge or number — [groups.md](groups.md).
