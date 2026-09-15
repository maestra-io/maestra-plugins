# Value formats (production contract)

**When to read:** before generating value shapes beyond the copy-safe forms in the
"Value rules" section in `SKILL.md` — this has the exact shapes that aren't in the core.
**Return to:** Workflow / Self-check in `SKILL.md`.

Exact JSX attribute formats for the production converter. A violation is a validation error or a silent loss of data.

## 1. Strings

- Write in quotes: `url="https://example.com"`, `visibilityOnDevices="mobile"`.
- A string with special characters (`"`, `&`, `<`, `>`, `{`, `}`, `\`, a line break) goes in curly braces as a JSON string:
  ```jsx
  <Button url={"https://shop.example/?from=email&utm=sale"}>Shop</Button>
  ```
- In `<Text>` a quoted string is **literal text**: `{"<p>One&nbsp;Two<br>Next</p>"}` will be escaped and shown as visible text, not markup. Write markup as explicit JSX tags; put raw HTML (an unclosed `<br>`, a comment, entities, a table) into `<Html>{"…"}</Html>`. A quoted string in `<Text>` is needed for literal text with special characters and existing personalization. Don't mix bare text and a quoted string in the same element — live rejects it (`<Text> may only contain text`).

## 2. Numbers

- Write in curly braces: `size={12}`.
- Integers for `size`, `fontSize`, padding, radii.

## 3. Objects (JSON structures)

- Write in curly braces as JSON: `innerSpacing={{ top: 24 }}`, `style={{ fontSize: 24 }}`.
- **Partial merge**: write only the changed fields — the rest are filled in from the new node's prop default, not from the previously saved email.

### background

```jsx
background={{ type: "color", value: "#RRGGBB" }}
background={{ type: "transparent" }}
```

### border

```jsx
border={{ type: "solid", color: "#RRGGBB", size: { top: N, right: N, bottom: N, left: N } }}
border={{ type: "none" }}
```

### borderRadius

```jsx
borderRadius={{ topLeft: N, topRight: N, bottomLeft: N, bottomRight: N, mobile: { … } }}
```

### innerSpacing

```jsx
innerSpacing={{ top: N, bottom: N, left: N, right: N, mobile: { … } }}
```

### columnsGap

```jsx
columnsGap={{ size: N, mobile: { size: N } }}
```

### style (Text)

```jsx
style={{
  font: { family: "…" },
  fallbackFontFamily: "Tahoma",
  fontSize: N,
  lineHeight: "1.8",
  letterSpacing: N,
  color: "#RRGGBB",
  inscription: ["bold"|"italic"|"underlined"|"crossed"],
  link: { color: "…", inscription: […] },
  align: "left"|"center"|"right",
  mobile: { fontSize: N, align: "left"|"center"|"right" }
}}
```

Strikethrough is `crossed`. The converter silently accepts `strikethrough` and draws nothing:
there will be no error, and there will be no strikethrough in the email either.

These are the nine fields that reading an email prints in full on a node outside the letter styles
(the editor's Design tab; §8 `dsl-surface.md`). `lineHeight` is a string (`"1.0"`, `"1.8"`), `letterSpacing` is a number:
the layout's letter-spacing is reproduced, not declared impossible; the live preview has been verified on both.
`fallbackFontFamily` follows the font rules — preserve it on a round-trip, don't invent a new one.

If `Text.style` sets `fontSize` or `align`, set `style.mobile` deliberately.
Without it the backend substitutes the mobile default `{ fontSize: 18, align: "left" }`,
which can break the mobile hierarchy.

`font.family` is a genuinely existing field of the format, but not a font catalog. The MCP has no way to
check whether the family is loaded into the editor. So on a round-trip, preserve the already
stored value, and write a new family only after the user has explicitly confirmed
it's available in the editor. A name taken from a layout is not, by itself, such
confirmation.

### simpleTextStyles (Button)

```jsx
simpleTextStyles={{
  font: { family: "…" },
  fontSize: N,
  color: "#RRGGBB",
  inscription: […],
  mobile: { fontSize: N }
}}
```

If you change a button's desktop `simpleTextStyles.fontSize`, set
`simpleTextStyles.mobile.fontSize`. Otherwise the mobile label may fall back to the
backend default.

The same availability rule as for `Text.style.font.family` above applies to
`simpleTextStyles.font.family`.

### buttonSize

```jsx
buttonSize={{ height: N, widthType: "percent"|"pixels", width: N }}
buttonSize={{ height: N, heightMobile: N, widthType: "pixels", width: N, widthMobile: N }}
```

`widthType` is required next to `width`: without it the number is read as a percentage. Write `heightMobile` and
`widthMobile` only when the mobile value differs from the desktop one — without them the mobile
side is synchronized with desktop. On choosing between percent and pixels, see `dsl-surface.md`, §6
"Button".

### align

```jsx
align={{ align: "left"|"center"|"right", mobile: { align: "…" } }}
```

### gapAfterBlock

```jsx
gapAfterBlock={{ desktop: N, mobile: N }}
```

This is an outer inter-block gap, not the standard way to add vertical spacing. For
regular spacing inside a section use `innerSpacing`, so its background is preserved.
Set a new `gapAfterBlock` only on an explicit request or when the layout calls for a
distinct strip of the outer background; preserve an existing value on an unrelated round-trip.

### verticalAlign

```jsx
verticalAlign={{ align: "top"|"middle"|"bottom", mobile: { align: "…" } }}
```

## 4. Lists

- **Lists replace, they don't merge**: `inscription: ["bold"]` replaces the whole list.
- Write the list in full: `["bold", "italic"]`.

## 5. Color (hex)

- Format: `#RRGGBB` (6 hex digits).
- Not validated automatically — check it yourself.
- Used inside: `background.value`, `border.color`, `style.color`, `simpleTextStyles.color`.

## 6. URL

- Attribute: `Button.url` (not `href`). For a new CTA it is required by policy; the absence of the attribute is not a runtime error in the converter.
- Allowed schemes: `https://`, `tel:`, `mailto:`.
- The backend validates the format and rejects survey links.
- A URL with `&`, `=`, `"` goes in quotes inside `{}`:
  ```jsx
  <Button url={"https://shop.example/?from=email&utm=sale"}>Shop</Button>
  ```

## 7. image (Image)

```jsx
image={{ mode: "static", static: { url: "<HTTPS URL>", fileName: "<file name>" } }}
image={{ mode: "dynamic", dynamic: [<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "<CUSTOM_FIELD_SYSTEM_NAME_FROM_LOOKUP>" }} />] }}
```

- `mode: "dynamic"` is a personal image: the address is taken from the parameter's value. `static` is not
  written in this form; the missing fields are merged onto the default. A domain prefix before `<Var>` is allowed
  only on the user's direct instruction.
- For gallery assets: if `name` already ends with `fileExtension`, `fileName = name`; otherwise
  `fileName = name + fileExtension`.
- Besides the required `image`, a standalone Image accepts `url`, `size`, `align`,
  `innerSpacing`, `border`, `borderRadius`, `visibilityOnDevices`. The live
  backend rejects `background`.

### size (standalone Image)

Fixed-size form, verified live in preview for desktop/mobile:

```jsx
size={{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }}
```

The stored JSX from the editor also has, and round-trips, this form:

```jsx
size={{ equalizedImageMaxWidth: "N" }}
```

or both kinds of fields together. `equalizedImageMaxWidth` is a string; preserve it on a
round-trip of an existing template, but don't compute or invent it for a new fixed-size
Image.

### align (standalone Image)

```jsx
align={{ align: "left"|"center"|"right", mobile: { align: "…" } }}
```

### url (click-through on Image)

```jsx
url="https://shop.example/item"
```

This is an optional HTTPS click-through link, not the image source. For a static source
use `image.static.url`; for a personal one, `image.dynamic`. A placeholder or invented
`url` is forbidden by policy.

A personal click-through link is written as a list of segments:

```jsx
url={["https://shop.example/points/", <Var param="RecipientBonusBalance" balance={{ "systemName": "<BALANCE_SYSTEM_NAME_FROM_LOOKUP>" }} />]}
```

The converter does not apply scheme validation to a value with a chip — the correctness of the address is
up to the field's contents.

## 8. Grid (Column.size)

- Integer 1..12, required.
- The sum within one FlexRow and within `<Split>` **== 12** (strictly, not ≤).
- A `<Split>` column accepts only `size` and contains 0..1 elements.
- Error: `Column sizes in a <FlexRow> must sum to 12 (got N)` or `Column sizes in a <Split> must sum to 12 (got N)`.

## 9. Visibility (visibilityOnDevices)

- String: `"all"` (default), `"desktop"`, `"mobile"`.

## 10. Group attributes

Use these forms only on the group that owns the attribute. The `itemsGap` defaults are in `dsl-surface.md` §6, "Defaults that appear on their own".

### itemsGap and iconTextGap

```jsx
itemsGap={{ size: N, mobile: { size: N } }}
iconTextGap={{ size: N, mobile: { size: N } }}
```

### iconTopPadding

```jsx
iconTopPadding={{ top: N, bottom: N, left: N, right: N, mobile: { top: N, bottom: N, left: N, right: N } }}
```

### imageSize

```jsx
imageSize={{ type: "fixed", width: N, mobile: { type: "fixed", width: N } }}
```

### bulletIcon

A small dot/circle (actual width 4px):

```jsx
bulletIcon={{ url: "https://cdn.example.com/dot.png", fileName: "dot.png" }}
```

A large constructor-compatible marker/number badge:

```jsx
bulletIcon={{ type: "custom", url: "https://cdn.example.com/one.png", fileName: "one.png", size: N }}
```

`bulletIcon` is required by policy: the default `data:` SVG breaks the HTML attribute and
renders as a giant circle. `type: "custom"` and `size` are confirmed by the stored
editor template and by live preview/HTML; the actual width equals `size`. The URL in the
examples is illustrative — use only a user's or a gallery asset. The Image
form `{ mode: "static", static: ... }` does not work for bulletIcon.

`align`, `verticalAlign`, and `columnsGap` use the forms from the corresponding sections above. `align` applies to Menu and Socials; `verticalAlign` and `columnsGap` apply to Split.

## 11. What can't be removed

- Omitting an attribute means keeping the new node's default, not "removing" it.
- To reset: an empty string, zero, `{ type: "none" }` for border, `{ type: "transparent" }` for background.
