---
description: "The typography fields shared by Text.style, simpleTextStyles of Button and Label, and TextStyle in Theme: value shapes, the editor's font lists, inscription values, the mobile branch"
---

# Typography — `style` and `simpleTextStyles`

One set of fields serves `Text.style`, `simpleTextStyles` on `<Button>` and `<Label>`, and `<TextStyle>` inside
`<Theme>`. Write the fields you change; how the rest is filled in on a node under the letter styles —
[theme.md](theme.md). A read email prints the whole set on a node with its own look.

| field | value | note |
|---|---|---|
| `font` | `{ family: "<one of the names below>" }` | left out, the node takes the font of the email's styles — on the platform theme Helvetica/Tahoma, never the element's own Arial — so a font from a mockup is always written, on the node or in `<Theme>`. A read email may carry `{ internalId: "…" }`, sometimes with a `family` beside it — the project's own font; copy the object unchanged |
| `fallbackFontFamily` | one of the web-safe ten | written next to a Google Fonts family; default `Tahoma` |
| `fontSize` | number, px | |
| `lineHeight` | string, one of the editor's `"1.0"`, `"1.15"`, `"1.5"`, `"2.0"` | the converter takes any string and prints it as is; another value reaches the email but has no entry in the editor |
| `letterSpacing` | number, px | written when the mockup has it |
| `color` | `"#RRGGBB"` | |
| `inscription` | list of `"bold"`, `"italic"`, `"underlined"`, `"crossed"` | `"strikethrough"` is accepted and draws nothing; strike-through is `crossed`. There is no upper-case setting: capitals are typed |
| `mobile` | `{ fontSize }` | without it the phone shows the desktop size, or the variant's mobile `fontSize` when the letter styles set one for a `Text` |

`Text.style` adds `align`, `link` and `mobile.align` — [text.md](text.md).

## Fonts

**Web-safe (10)**, on the recipient's side: `Arial`, `Helvetica`, `Times New Roman`, `Verdana`,
`Courier / Courier New`, `Tahoma`, `Georgia`, `Palatino`, `Trebuchet MS`, `Geneva`.

**Google Fonts (9)**: `Roboto`, `Open Sans`, `Montserrat`, `Inter`, `Poppins`, `Bebas Neue`, `Overpass`,
`Nunito Sans`, `Fira Sans`. Written with a `fallbackFontFamily` from the first list: an email client that does not
load web fonts shows the fallback, otherwise `Tahoma`, then `sans-serif`.

The lists are the editor's font picker, the same for every project. A name outside them is written into the email as
is, with the fallback after it and a Google Fonts link generated for it — the converter does not check the name; a
family outside the lists is replaced by the closest listed one.
