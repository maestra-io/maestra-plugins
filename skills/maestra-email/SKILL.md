---
name: maestra-email
description: Creates and modifies emails for the Maestra editor (visual builder) from a text description. Use when the user asks to create or modify an email, or describes an email template — including personalized content, product recommendation rows and letter styles. The technical layout is passed for preview and saving to the linked skill maestra-email-ops.
metadata:
  author: Maestra.io
  version: 1.11.0
---

# maestra-email — email generation

Generates a technical email layout from a text description. The internal output for Ops is valid JSX, which is then converted into the Maestra editor's JSON.

## Skill boundaries

This is a portable JSX generator. It does **not work directly** with gallery/upload tools,
mailing ID and rowVersion, VNet, or saving to Maestra. All operational
actions — uploading and searching images via Ops, JSX → JSON conversion, HTML rendering, PNG preview,
reading campaign metadata/visual template, and saving — are performed by the linked skill **maestra-email-ops**.
The Generator uses JSON/HTML/PNG feedback from Ops to self-correct the JSX, but does not fix
operational errors on its own and does not invent URLs.
A request to change the template type ("redo it in the visual editor", "convert it to HTML") is not
generation either: Ops leads the route, and the JSX is assembled after it decides where to save.

## Communicating with the user

JSX, internal IDs, and rowVersion are internal details of the Generator–Ops interaction.
In a normal dialogue with a CSM, use "email", "email layout", "email content",
"preview", and "saving" — not JSX, `mailingInternalId`, `variantInternalId`,
`formatInternalId`, `rowVersion`, or `visualTemplateRowVersion`. Do not replace the terms Active/Draft:
if they are needed to pick the exact version, use Active/Draft verbatim.
Do not show raw JSX or GUIDs unless the user explicitly requested code, an export,
markup, or technical details. Return backend errors verbatim, even if they
contain technical terms, tag names, line numbers, or identifiers.

## Feedback to the developers

Pass feedback about the skill's operation to the linked operational skill for Maestra email —
the one whose annotation covers preview, save, gallery and calls to the Maestra MCP
(`maestra-email-ops` in this package). It is the one that calls the MCP tools of the current
Maestra MCP server. If you see a critical problem in the Generator's rules
or the user asks to pass feedback to the developers — hand it to Ops and follow
its protocol: first show the full feedback text to the user, then obtain
explicit confirmation, and only then send it.

## Not implemented (deliberately)

- **Do not set** `targeting` on Block/Row — it is an external setting, not accessible from the DSL.
- **Do not use** `mobile={{…}}` — mobile values are written inside the attribute's JSON structure (for example `innerSpacing={{ top: 24, mobile: { top: 12 } }}`).
- **Do not write personalization as raw `${...}` template expressions** (`{{name}}`, `${Customer...}`, `${Order...}`) — there is the `<Var>` tag for it, see the "Personalization" section. The only surviving exception is the exact token `${Message.UnsubscribeLink}` in the `href` of an `<a>` link inside `<Text>` per the rules of the "Unsubscribe link" section: a chip cannot be assembled in an HTML attribute of the markup, the converter escapes it into text. In prop values (`Button.url`, `Image.url`) the chip works — the token is not needed there.
- **`<Image>` is allowed only with a source.** There are two kinds of source: a file — `image={{ mode: "static", static: { url, fileName } }}`, and a personal one — `image={{ mode: "dynamic", dynamic: [<Var … />] }}`, when the image address lives in the customer's or order's data. Bare `<Image />` is forbidden, because the backend substitutes a base64 placeholder. Source rules are in the "Images" section.
- **`<BulletList>` without `bulletIcon` breaks the layout.** The default system marker renders as a giant black circle: the backend inserts SVG into `src` without escaping quotes. Always set an HTTPS icon explicitly. For a small dot use the live-verified flat form `bulletIcon={{ url, fileName }}` — it renders a marker 4px wide. For a large editable marker/number badge use the editor-compatible form `bulletIcon={{ type: "custom", url, fileName, size: N }}` — the stored template and live preview/HTML confirmed an actual width of `N`. The form `{{ mode: "static", static: {...} }}` is silently ignored; a string crashes the preview with `Internal server error`.
- **Standalone** `<Timer>`, `<Video>`, `<BulletItem>` have no safe shorthand. `<BulletItem>…</BulletItem>` works as an item only inside `<BulletList>`; simplify a timer or video down to `<Text>` or `<Button>`.
- **`<Html>` is a fallback only.** Always try to build the design with the standard flexible blocks first (`Text`, `Button`, `Image`, `Menu`, `BulletList`, `Socials`, `Split` with spacing/backgrounds/grid) — they are responsive and survive manual edits in the editor. Switch to `<Html>` only if what is needed cannot be expressed with standard blocks (table-based layout, non-standard entities) **or the user explicitly asks for arbitrary HTML**. The content is a single quoted string only: `<Html>{"<table>…</table>"}</Html>`; the live backend rejects direct JSX inside `<Html>` (`<Html> may only contain text`). Warn that manually editing such a block is unsafe.

## Workflow

1. Analyze the text description: identify the blocks (heading, body, CTA, image, divider) and add a footer with an unsubscribe link to them — every marketing email needs one, even when the description does not mention it. Apply the "Unsubscribe link" section and do not disguise it as a regular URL.
   **Adding headings or buttons to an existing email** — the look of the new elements is decided not by the state of the email but by whether it was stated. If it was stated neither in the request, nor in the mockup, nor by example — write no styles: the nodes go under the letter styles of the email (the editor's Design tab), whatever those are, and change along with them from then on. If it was stated — inline it as asked, and do not ask whether to take the look from the email instead: that would mean undoing what was said. A reference to a neighboring element ("like the heading above") does not count as a stated look — the look is taken from that node, and if it goes under the letter styles, the new one stays empty.
   **Building a new email into a format that already holds an email** — Ops sees this via `visual_template_get` and asks the user before generation; build according to their answer. "In the existing styles" — the new nodes write no styles of their own, the variant is set via `themeVariant`, the look comes from the letter styles. "New styles" and "reset to platform styles" — write `<Theme>` explicitly: without it the previous styles remain (§8 `dsl-surface.md`), and the new nodes will take their look from them. The same applies when the user says "let's start over" in the middle of edits: that is a replacement, not an edit, and Ops asks the same questions again — do not start a new email until they have been asked.
   **If a reference is given** (a website, a brand, a screenshot, "like on our landing page"), fix before generation: 2–3 brand colors in `#RRGGBB`, a contrasting pair of sections (dark/light), and three text size levels — heading, subheading, body — and apply them throughout the email. A reference is carried over via section structure, background, and color, not just via text: a branded email cannot consist of sections with no background and text of a single size. The default styles are a stand-in for when nothing is known about the style, not the target look.
2. **If the user asks for a saved block from the editor — take it, do not draw it anew.** The signal: words about the library ("saved block", "our footer from the editor"), with or without a name. Via Ops call `visual_template_saved_block_list` — with `nameSubstring` if the block is named. The user chooses in the panel: do not choose yourself, do not ask them to name the block in words, do not iterate over name variants and do not call the tool again — wait for the reply with the choice, then `visual_template_saved_block_get` by the `internalId` from it. No panel (Claude Code, CLI) — show the names from the response, the user picks by name, take the `internalId` from the same row. Nothing found — say so first, then offer to build it yourself.
   On an edit, the block takes the place of the named section; leave the rest of the email untouched. If the email follows letter styles — warn the user: the block's styles are fixed as explicit values, it no longer follows the letter styles.
3. **Resolve all images.** Every `<Image>` needs a confirmed HTTPS URL: an external URL from the user (as is), a URL from the gallery/search MCP workflow that Ops returns, or a URL from the JSX of a library block. If there is no source — request an upload/search via `maestra-email-ops` before generating JSX. If the result must be saved into a specific campaign, Ops starts the image lookup/upload only after `campaign_get`, target selection, and `visual_template_get`/bootstrap discovery; the "images before JSX" rule still holds.
   A personal (dynamic) image is the exception: its source is not a file but a parameter, so it needs neither the gallery nor an upload. What has to be resolved before generation is something else — the `param` and, if it is tenant-specific, the `systemName` from `entities_list`. See "Images" → "Personal image for the customer".
4. Generate JSX following the hierarchy: `Template → Block → FlexRow → Column → Text|Button|Divider|Html|Image|Menu|BulletList|Socials|Split`. `Template` must contain at least one `Block`, `Block` at least one row, a row at least one `Column`; an empty `Column` is allowed. The second kind of row is the product `CollectionRow` with cards instead of columns (`references/product-rows.md`). For groups, respect the item types and the Split grid rule. Try to express every visual device with standard blocks first; `<Html>` is a fallback only (see "Not implemented").
5. For text styles use `style={{...}}` with partial merge — write only the fields you are changing. For a button — `simpleTextStyles={{...}}`. Partial merge is about economy of edits, not about skipping styling: set color, size, and background wherever the design requires them. But for an element whose look is stated neither in the description, nor in the examples, nor in the mockup, and there is no similar one in the email yet — write no styles at all: the look will come from the letter styles of the email and will change along with them from then on (§8 `dsl-surface.md`). Set heading levels via `themeVariant`, not via invented sizes.
   Do not carry a new `font.family` over from a layout by name and do not guess: the MCP cannot
   fetch the list of standard/custom fonts available in the editor. Preserve
   the existing `font.family` on round-trip. Set a new family only after explicit
   confirmation from the user that it is already uploaded or available in the editor; otherwise
   keep the theme's family and reproduce the style via size, color, weight, line-height,
   and alignment.
   Assemble lists of features, plans, benefits, metrics as a **grid** — a `FlexRow` of 6+6 or 4+4+4 with `background` and `borderRadius` on the `Column` — not as a vertical list. Reserve `BulletList` for short one-liners and explicitly styled numbered-point/badge elements per the dedicated pattern below.
6. Check yourself against the Self-check checklist.
7. **Before the first save** of the email — not before the handoff to Ops — offer to move the nodes' look into the letter styles. Both conditions are checked against the document itself, not against the state of the email:
   - **there is something to move**: at least one node itself names a setting covered by the letter styles — color, size, weight, background, radius (§8 `dsl-surface.md`);
   - **moving would give something**: the same look repeats on two or more nodes. If every node has its own look, there is nothing to move: the number of variants is finite, and the family resemblance that the move exists for would not arise.

   If both hold — ask: "Save this email's styles as its letter styles? Then you will be able to change headings and buttons across the whole email at once later". If the document already carries a `<Theme>` — for example, the styles were just reset to the platform ones — the question is the same in meaning, but about that tag: whether to move the repeating look of the nodes into it. Consent — move it per the procedure in §8; refusal is a legitimate result, the email is saved with its own styles on each element. **One dialogue — one such question:** any answer holds until the end of the dialogue, and neither a second save nor edits between saves re-arm it.
   Going **only to a preview** does not close this step: the question is armed by the turn when a save is first requested. The state of the email ("platform styles", "own styles") has nothing to do with it: after a reset to platform styles they are formally its own, but there is still somewhere to move the nodes' look.
   **A node with a mobile difference is moved only with the user's consent:** the mobile side of the styles is one per variant, so such a node either stays unique or loses its difference. Name the element and ask — §8 `dsl-surface.md`.
8. For handoff to Ops, the Generator's result is **JSX only** — no Markdown fences, no comments, no explanations. Do not show this JSX to the user in a normal dialogue; show raw code only on an explicit request for code/export/markup/technical diagnostics. Clarifying questions and messages about limitations should be in the user's language.
9. If the request includes verification, preview, diagnostics, or saving, step 8 is not the end: hand the JSX to Ops. Ops does not call preview automatically after every edit. After a JSX change, the previous widget/link is stale: the user gets the message "the previous preview no longer matches the current version; if you like, I can show a new one". `visual_template_preview` is called only when the user asks for a preview, HTML/PNG QA, desktop/mobile/debug, or comments on specific content/rendering; it renders the editor canvas, where personalization is substituted with sample values, so the substituted values and `#` links are not considered defects. In a supporting host, the HTML preview opens an MCP App widget and provides a fallback link; local HTML is downloaded only for HTML QA/debug, and the desktop/mobile PNG links arrive in the same preview response — there is no separate call for them. Fix backend preview/save errors in the JSX and repeat only the requested check. Never assemble HTML/preview by hand. The primary preview for the user is the MCP App widget/fallback link before save and the editor canvas after save; save is allowed after explicit confirmation with the preview status.
10. If the user asks to create/save a new campaign with metadata, do not handle
   this in the Generator: pass it to Ops. The Generator is responsible for the JSX; Ops handles
   `campaign_create`/`campaign_edit_content`/`campaign_edit` and separately reports that
   recipients/send/activate are configured in the UI.
11. Accept a "backend unavailable" status only from Ops after a call to the specific MCP
   tool of the current operation (`campaign_get`, `visual_template_get`,
   `visual_template_preview`, or `visual_template_save`) and an actual error/status.
   Do not transfer the result of a ping, the root, or a neighboring host onto the needed MCP route.

## Hierarchy (18 tags)

```text
Template         exactly one root
└─ Block         1..n, email section
   ├─ FlexRow    1..n, row (grid container)
   │   └─ Column  1..n, size is required; the sum of size within one FlexRow == 12
   │         └─ Text | Button | Divider | Html | Image | Menu | BulletList | Socials | Split | Labels    0..n elements
   └─ CollectionRow    product row: cards instead of columns, rules in product-rows.md
       ├─ CardTemplate     0..1, the card every product is drawn with
       └─ CollectionCard   0..n, the card of a manually selected product
             └─ Column  the sum of size == 12; inside — the same elements
```

`Menu`, `BulletList`, `Socials` and `Labels` contain direct item elements without `<Column>`; for `Split` the items are `<Column size={N}>`. A group may stand in a regular column or in a `Split` column, except `Split` inside `Split`.

## Allowlist

| Tag | Required attribute | Optional attributes | Purpose |
|-----|----------------------|----------------------|------------|
| `Template` | — | `containerWidth`, `background` | Root (exactly one) |
| `Block` | — | `background`, `border`, `borderRadius`, `innerSpacing`, `gapAfterBlock`, `externalBackground`, `visibilityOnDevices` | Email section |
| `FlexRow` | — | `background`, `border`, `borderRadius`, `innerSpacing`, `columnsGap`, `rowsGap`, `verticalAlign`, `isColumnsMobileAdaptive`, `columnVerticalDirection`, `visibilityOnDevices` | Row (grid container) |
| `Column` | `size={1..12}` | `background`, `border`, `borderRadius`, `innerSpacing` | Grid column |
| `CollectionRow` / `CardTemplate` / `CollectionCard` | see reference | see reference | Product row. The full allowlist, card attributes and constraints are only in `references/product-rows.md` |
| `Text` | — | `style`, `themeVariant` (`h1`/`h2`/`h3`/`text`), `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Text block (supports HTML markup inside) |
| `Button` | — | `url`, `align`, `themeVariant` (`primary`/`secondary`), `innerSpacing`, `buttonSize`, `background`, `simpleTextStyles`, `border`, `borderRadius`, `iconSrc`, `iconAlt`, `iconDisplay`, `iconSizeInPercents`, `visibilityOnDevices` | CTA button; `url` is required for generation by policy |
| `Divider` | — | `innerSpacing`, `border`, `visibilityOnDevices` | Divider line (self-closing) |
| `Html` | — | `visibilityOnDevices` | Arbitrary HTML block |
| `Image` | `image` | `url`, `size`, `align`, `innerSpacing`, `border`, `borderRadius`, `visibilityOnDevices` | Image with a confirmed source URL (self-closing); `size`/`align` control the image itself, `url` makes it clickable; do not set `background` — the backend rejects it |
| `Label` | — | `url`, `background`, `border`, `borderRadius`, `innerSpacing`, `contentSpacing`, `simpleTextStyles`, `iconSrc`, `iconAlt`, `iconDisplay`, `iconSizeInPercents`, `emptyVariableBehavior`, `boolFieldVisibility`, `themeVariant` (`primary`/`secondary`) | Label: short text on a background with an optional icon. **Place it only in a product-row card and only as an item of `<Labels>`**: the restriction lives in the editor canvas, the converter will let a label in a regular row through — a successful preview proves nothing here. Placed directly in a `<Column>`, the editor rejects it. A label has no `visibilityOnDevices` (`Unknown attribute`); it is set on the `<Labels>` group. The content is text or a list of segments `{["−", <Var … />]}`; a chip as a child element is rejected: `<Label> may only contain text`. Disappears entirely if the variable in it has no value — `references/dsl-surface.md`, §6 |
| `Menu` | — | `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Menu; children are only `<Text>` or only `<Button>` |
| `Labels` | — | `align`, `itemsGap`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | A row of labels in a product-row card; children are only `<Label>…</Label>` |
| `BulletList` | `bulletIcon` | `background`, `border`, `borderRadius`, `innerSpacing`, `itemsGap`, `iconTextGap`, `iconTopPadding`, `visibilityOnDevices` | Short single-line lists; children are `<BulletItem>…</BulletItem>`. Assemble features with a heading and a description as a grid, not a list |
| `Socials` | — | `background`, `align`, `innerSpacing`, `itemsGap`, `imageSize`, `border`, `borderRadius`, `visibilityOnDevices` | Social links; children are `<Image image={{...}} />` with the URL of each icon |
| `Split` | — | `columnsGap`, `verticalAlign`, `innerSpacing`, `background`, `border`, `borderRadius`, `visibilityOnDevices` | Children are `<Column size={N}>`; the sum of `size` == 12, 0..1 element per column |
| `Var` | `param` | the settings, formatters and affixes of its parameter | Personalization chip (self-closing); stands inside `<Text>` markup, in a value's list of segments, or between `<Button>` tags. The list of parameters is in `references/personalization.md` |

If the email contains products — recommendations, a product list, order products, viewed products, products
from an event or a manual selection — you MUST read `references/product-rows.md` before generating.
`<CollectionRow>` is the second kind of row and a direct child of `<Block>`; do not generate it before reading the reference.

Successful preview and save do not prove the mechanic is complete: a live check saved
`RECIPIENT_RECOMMENDATIONS` without the required `recoMechanicSystemName` and did not show this error.

Product-row safeguards:
1. Do not proceed until the mechanic, all of its required settings and the project's real values are chosen.
2. Do not invent `systemName` and identifiers: for recommendations use `RecommendationMechanic`, for a list — `ProductList`, for a manual product — `Product`.
3. Place product `<Var>`s only inside a product-row card and from the family matching the chosen mechanic.

**Forbidden:** `MenuItem`, `SplitColumn` and any other tags outside this table. The exception is `<Theme>` and the style tags inside it (`TextStyle`, `ButtonStyle`, `LabelStyle`, `BlockStyle`, `RowStyle`): these are not email elements, they live directly inside `<Template>` and are described in §8 `dsl-surface.md`. Do not generate bare `<Image />`, standalone `<Timer>`, `<Video>`, `<BulletItem>`, `<Label>`.

## Images

For a new `<Image>` always write the self-closing form:

```jsx
<Image image={{ mode: "static", static: { url: "https://cdn.example.com/banner.png", fileName: "banner.png" } }} />
```

`https://cdn.example.com/banner.png` here is only an illustration: in your response use a URL
only from the user or one returned by Ops from the gallery. Do not convert an external URL into
an internal one yourself: an external HTTPS URL is inserted as is, and the backend will process it on save.

Set the size and alignment of a standalone image on the `Image` itself; do not imitate them
with extra columns or side `innerSpacing`:

```jsx
<Image
  align={{ align: "center", mobile: { align: "center" } }}
  size={{ type: "fixed", width: 120, mobile: { type: "fixed", width: 80 } }}
  image={{ mode: "static", static: { url: "https://cdn.example.com/icon.png", fileName: "icon.png" } }}
/>
```

Preserve `size.equalizedImageMaxWidth` from stored templates on round-trip, but do not compute or
invent it for a new fixed-size Image. Inside `<Socials>`, set the items' size via `Socials.imageSize`
and alignment via `Socials.align`.

`Image.url` is an optional HTTPS link that is followed when the image is clicked; it is not
the image source. Create it only from an explicit URL given by the user. Do not insert a
placeholder. Preserve an existing `Image.url` on round-trip unless the user
asked to change the link. Stored JSX may contain serialization artifacts:
an `Image.url` with a bare `https://` and no path, or a URL inside `fileName` — do not treat these as
defects and do not "fix" them without a user request.

### Personal image for the customer

If the user asks for a "personal image", a "dynamic image link", an image "from the
customer's data" or to "put a field value into the image" — that is `mode: "dynamic"`, the same mode as
the "Personal image for the customer" radio button in the editor. The image address in the email is taken from
the parameter's value:

```jsx
<Image image={{ mode: "dynamic", dynamic: [<Var param="RecipientCustomFieldString" customFieldType={{ "systemName": "<CUSTOM_FIELD_SYSTEM_NAME_FROM_LOOKUP>" }} />] }} />
```

- **Do not ask for a file, the gallery or a base domain.** The field's value is the whole address. Add a prefix
  only if the user named it themselves:
  `dynamic: ["https://cdn.example.com/", <Var … />]`. An invented domain breaks the image for every recipient.
- **`static` need not be written** — fields absent from `image` are merged onto the default, and in dynamic
  mode the static source is not rendered.
- What to ask about here is not the image but the parameter: which field to substitute. From there on — the usual rules
  of the "Personalization" section: `param` from `references/personalization.md`, a tenant-specific `systemName` — from
  `entities_list`.
- **The field's content is not validated.** If for a recipient it is empty or not a URL, the email will go out with a broken
  image. The empty-variable behavior is configured in the editor on the "Display" tab and cannot be set from
  the DSL — warn the user, do not substitute a placeholder.
- The clickable address is personalized the same way: `url={["https://shop.example/points/", <Var … />]}` or
  a single `<Var>` as a whole, if the link lies entirely in the field. The converter does not apply `https://`
  validation to such a value.

### External URL from the user

- Accept only a direct HTTPS URL and insert it as is.
- `fileName` is taken from the name given by the user, or from a non-empty unambiguous basename of the URL path.
  If the name cannot be determined unambiguously — ask, do not invent.

### An attached file or a gallery image — via Ops

The Generator does not upload files and does not access gallery/search tools itself. Delegate to `maestra-email-ops`:

- **An attached file:** pass the file path to Ops. After the MCP upload link and HTTP 200, Ops
  returns the source as `url: fileUrl`; if the JSX needs a `fileName`, it is only
  a service name from the original file, not the image source. On an upload error, do not
  pick an asset silently — stop and inform the user.
- **An already uploaded image:** ask Ops to search by name. With a single candidate, Ops
  returns `{url, fileName}`; with several — show the user the safe metadata
  (`name`, extension, size/date if available, system/project source) and ask. Do not pick by name automatically.
- If Ops reports an upload/list error — stop, do not generate JSX with the image, and do not
  pick an image by name.

An image as the email background follows the same source rules; the value shape and modes are in §4 `dsl-surface.md`, "Image background".

### Hard rules

- Do not invent URLs. Author-supplied `data:`, `base64`, `blob:`, `file:`, and `cid:` are forbidden.
- The image URL must be HTTPS by skill policy. This is not a statement about the converter's
  runtime validation for Image.
- Bare `<Image />` is forbidden both in new and in edited JSX: replace it with a confirmed URL
  (via Ops) before writing it back — or with a personal source, if the image is taken from data.
- The invented-URL rules extend to a personal image as a ban on an invented prefix: the
  address itself comes from the project's data, not from the model's response.
- `<Html>` does not bypass the image rules: if the quoted HTML contains `<img>`, its `src` must
  be a confirmed HTTPS URL; prefer `<Image>`.
- Do not place important text, a price, a CTA, or terms only inside an image.

## Fonts

- `style.font.family` on `Text` and `simpleTextStyles.font.family` on `Button` exist
  in the DSL, but the mere presence of the string in JSX does not mean that such a font is installed in
  the editor or available in the email.
- When editing an existing email, preserve the already stored `font.family` unless
  the user asked to change the font.
- Do not add a new family by name from a layout, a website, or a "set the font to X" request.
  First tell the user that the MCP cannot check the font catalog, and ask them to confirm
  that X is already uploaded/available in the editor. Without confirmation, do not write the family.
- If the font is unavailable or its availability is unknown, keep the theme's family and convey
  the character of the typography via `fontSize`, `inscription`, `color`, `lineHeight`, text case,
  and `align`.

## Editable numbered points / badges

- If a number, dot, or badge must remain a separate editable element
  of the editor, do not draw it with a styled `<span>` inside `<Text>` and do not use
  `<Html>`. Such a rich-text/CSS trick may look right in the email, but it does not give
  the user a proper separate editor element.
- Use only separate editor elements: `<BulletList>` or `<Image>` +
  `<Text>`; the choice of form, the rule about distinct digits, and the mobile settings are not duplicated in the core.
- If the digit/icon asset is missing, first find/upload it via Ops or offer
  the user a simple confirmed bullet; do not draw a replacement with inline CSS.
- **Before any numbered-point block, you MUST read
  `references/examples.md` §14**: without it, it is easy to apply one icon to all the digits,
  lose the mobile setting, or again end up with a non-editable CSS badge.

## Spacing between blocks

- In a new or modified layout, do not use `gapAfterBlock` by default for
  ordinary vertical spacing. Create the spacing via `innerSpacing.top/bottom`
  on the `Block`, `FlexRow`, or `Column` itself, so the section background continues under the spacing.
- `gapAfterBlock` creates an outer inter-block gap. Use it only when
  the user explicitly asks for an outer gap or the layout clearly shows a stripe/gap
  in the outer background color that differs from the background of the adjacent blocks.
- On round-trip, do not remove an existing `gapAfterBlock` in a part of the email the
  user did not ask to change. The rule governs new/modified layout; it does not
  authorize incidentally reworking the entire email.
- **If a mockup is given — take the spacing from it, do not estimate by eye:** spacing is
  exactly where the email diverges from the original most often, and in a preview such a divergence
  is almost invisible. Saying nothing about a spacing means taking the element's default, not "flush": zero
  is written explicitly, and the defaults themselves are collected in §6 `dsl-surface.md`, "Defaults that appear on their own".

## Personalization

A personalized value is written with the `<Var>` tag: `param` is the parameter name, the remaining attributes are its
settings and formatters. The converter assembles a real chip out of this, so the email remains editable in
the editor.

```jsx
<Text><p style="margin: 0;">Hello, <Var param="RecipientGreeting" />!</p></Text>
```

- **Rules and common parameters — `references/personalization.md`.** Open it before the first personalization
  in an email: `param` cannot be guessed, and the parameter's entity decides where it resolves. If the one you need is not in
  the list of common ones — open `references/personalization-parameters.md` (email parameters) or
  `references/product-parameters.md` (product parameters, by entity), do not pick a similar one. **Order data are email parameters:** in an automatic email `OrderTotalAmount`,
  `OrderExternalId`, `OrderDateTime`, order custom fields and the other `Order*` stand anywhere in the email.
  But product and list-line parameters (`ProductName`, `ProductListItemProductPrice`, `OrderItemProductName`,
  …) resolve only inside a product-row card, and which of the five families to take is decided by its
  mechanic: see `references/product-rows.md`. Do not use a product chip in a regular column: for products,
  build a product row.
- **Take tenant-specific names only from `entities_list`** — promo code pools (`PromoCodePool`), custom fields
  (`CustomField` + `ownerEntityType` by the field's owner), bonus balances (`Balance`), external systems
  (`ExternalSystem`), product lists (`ProductList`) for a product-row mechanic, the products themselves
  (`Product`) for a manually selected row, recommendation mechanics (`RecommendationMechanic`) for
  a row with recommendations. The order number is a special case: its catalogue is not `ExternalSystem` but
  `CustomField` with `ownerEntityType: OrderExternalId`; which setting to ask for with what — the table in
  `references/personalization.md`. Carry all fields from the response into the JSX: `systemName` goes into the email,
  `name` and `internalId` are needed by the editor for the preview and the select.
- **Do not invent `systemName` and do not leave it empty.** Preview/save do not prove the existence of a
  tenant-specific value and do not always catch an unfilled source setting. A non-existent or empty name
  produces validation/runtime problems, so take every `systemName` from a lookup or from the user, and if
  there is no name — do not write the parameter and ask. A value is required by `customFieldType`, `externalSystem`,
  `orderExternalIdSelection`, `promoCodePool`, `balance`, `hostname`, and an enabled `discountQuery`.
- **Do not carry the custom field's value type into the chip.** It is used to choose the `param`, and the `type` field in
  `customFieldType` is derived by the converter itself — one written by hand it will not reject, but will store incorrectly.
- **Personalization lives not only in text.** A list of segments is accepted by the string of any value: the address
  of a personal image (`image.dynamic`), a link (`url`), a button's words, the content of a `<Label>`. If the user asks for
  a "dynamic" image or link — this is it, not a request for a file and not a raw `${...}` template expression. The forms are in
  `references/personalization.md`, section "Where it can stand"; for an image — "Images" → "Personal
  image for the customer".
- **A chip the converter did not recognize** arrives in the stored form `<personalization-parameter model="…">`.
  Leave it as is.
- If the user asks for personalization for which a name from the catalogue is missing — ask for the name,
  do not offer static text: that used to be the only way out, it no longer is.

## Unsubscribe link

- **The unsubscribe link is needed by default, not on request.** A marketing email is not handed off without it:
  add the canonical rich-text anchor to the email's footer — as the last `<Block>`, in small grey text —
  even if the user did not say a word about unsubscribing. No need to ask permission.
- Do not add it in two cases: the user said the unsubscribe comes from the email wrapper or
  the campaign settings, or the email is transactional (password, receipt, order status). **Name both cases in
  the response** — "I did not add an unsubscribe link because …" — so that its absence is a choice, not a
  forgotten step.
- On an explicit request for an unsubscribe link/button — the same canonical rich-text anchor inside `<Text>`.
- Use only the exact `href="${Message.UnsubscribeLink}"`. The correct form is
  `<p style="margin: 0;">… <a href="${Message.UnsubscribeLink}">unsubscribe from this mailing list</a></p>`
  inside `<Text>`; if the link text is not specified, use the standard text:
  "If you no longer want these emails — unsubscribe from this mailing list".
- The full example and the explanation of why the literal token in the preview is not a defect are in
  `references/dsl-surface.md` §"Unsubscribe link"; open it when diagnostics are needed.
- Do not write the token in a prop value — neither `<Button url="${Message.UnsubscribeLink}">` nor in `Image.url`.
  A chip is written there: unsubscribe has its own parameter, and it yields the same expression.
- **An unsubscribe button or clickable image** is the `SpecialLinkUnsubscribeLink` chip in `url`:
  `<Button url={[<Var param="SpecialLinkUnsubscribeLink" />]}>Unsubscribe</Button>`. Such a chip remains
  editable in the editor, unlike the token. Do this if the user asks specifically for a button;
  by default the footer is a text link.
- Fake URLs (`/unsubscribe`, `#`, `https://example.com/unsubscribe`) and other `${...}` tokens are forbidden.
- If the canonical link already exists, do not add a second one. When editing, preserve the existing
  text, position, and styling unless the user asked to change them.
- **The presence of a footer does not replace the link:** "present" means the exact `${Message.UnsubscribeLink}` or the chip, not
  a block with a caption about unsubscribing. The same goes for a footer from the library and for the footer of an email you are editing;
  adding the anchor to such a footer is allowed — it is an edit of text and a link.

A ready-made footer that can be placed as is:

```jsx
<Block innerSpacing={{ "top": 20, "bottom": 20, "left": 24, "right": 24, "mobile": { "top": 16, "bottom": 16, "left": 16, "right": 16 } }}>
  <FlexRow><Column size={12}>
    <Text style={{ "fontSize": 12, "color": "#888888", "mobile": { "fontSize": 11 } }}>
      <p style="margin: 0;">If you no longer want these emails — <a href="${Message.UnsubscribeLink}">unsubscribe from this mailing list</a></p>
    </Text>
  </Column></FlexRow>
</Block>
```

## Divider and placeholder links

- `<Divider />` is fully supported. But set `border` in full (`type`, `color`, all four
  `size` sides with one thickness, usually `1`) and do not zero out `innerSpacing` — otherwise the line exists in
  the markup but is not visible in the email. A thickness only in `size.top` does not draw the line: with unequal sides
  it is not visible at all, and the converter rejects such a value. A full-width divider is its own `FlexRow` with `<Column size={12}>`.
- If a divider was in the description or reference and the user requested preview/QA — verify
  that it is **visible in the preview**, not merely present in the JSX.
- Do not generate placeholder URLs (`https://`, `#`, `/`, `about:blank`, `https://example.com`).
  If there is no address for the CTA or the image click — one clarifying question; do not create the button/`Image.url`.
- On round-trip of an existing email, keep placeholders as is, but list them to the user.

```jsx
<FlexRow><Column size={12}>
  <Divider innerSpacing={{ top: 18, bottom: 18, mobile: { top: 12, bottom: 12 } }} border={{ type: "solid", color: "#cfcfcf", size: { top: 1, right: 1, bottom: 1, left: 1 } }} />
</Column></FlexRow>
```

## Value rules (partial merge)

**Write only what you are changing.** Objects are filled in from the new node's defaults, not from a
previously saved email; arrays are replaced wholesale. Write strings in quotes, numbers/objects in
`{}`.

Copy-safe forms of common attributes (the numbers and colors below are illustrative; the syntax is valid):

```jsx
background={{ type: "color", value: "#F5F5F5" }}
background={{ type: "transparent" }}
border={{ type: "solid", color: "#CCCCCC", size: { top: 1, right: 1, bottom: 1, left: 1 } }}
border={{ type: "none" }}
borderRadius={{ topLeft: 12, topRight: 12, bottomLeft: 12, bottomRight: 12, mobile: { topLeft: 8, topRight: 8, bottomLeft: 8, bottomRight: 8 } }}
innerSpacing={{ top: 24, bottom: 24, left: 24, right: 24, mobile: { top: 16, bottom: 16, left: 16, right: 16 } }}
style={{ fontSize: 16, color: "#111111", inscription: ["bold"], align: "left", mobile: { fontSize: 14, align: "left" } }}
simpleTextStyles={{ fontSize: 16, color: "#FFFFFF", inscription: ["bold"], mobile: { fontSize: 14 } }}
```

For other forms — `buttonSize`, the standalone `align`, `gapAfterBlock`, `verticalAlign`,
as well as `Image.size`/`align`/`url`, `image`, and `bulletIcon` — **you MUST check
`references/formats.md` before generating**: their exact value shapes are not
duplicated in the core, and a guessed shape produces a bare `Internal server error` on
convert/preview with no line number.

**A setting keeps the shape of its default value.** An object is written as an object, a single
value as a single value. This rule is general, and `*Gap` is just the most common case: `itemsGap`,
`columnsGap`, `rowsGap`, `iconTextGap`, `cardGap`, `rowGap` take `{ size: N, mobile: { size: N } }`,
and `columnCount` and `rowCount` on a product row take `{ value: N }`, not a number. A product grid requires
`orientation="vertical"`: a horizontal row does not read the column count.

Anything written in a different shape the converter rejects and **shows the default in full** — that is, the response itself
names the required shape, no need to look it up in the reference:

```
`cardGap` takes an object like {"size":16,"mobile":{"size":16}}, and states a number
```

So the shape of `*Gap` and the counters need not be memorized: if unsure — write it as you understand it and read
the response. This does not work for the shapes in the list above: there the converter answers with a bare `Internal server error`
with no hint, which is why they are checked in advance.

## Text — markup inside text

`<Text>` supports HTML markup inside the tag. Write the markup directly:

```jsx
<Text>
  <p style="margin: 0;">Summer <strong>sale</strong>, <a href="https://shop.example">see more</a></p>
</Text>
```

Available tags: `p`, `h1`–`h6`, `blockquote`, `ul`, `ol`, `li`, `strong`, `em`, `u`, `s`, `span`, `a`, `code`, `pre`, `br`, `hr`, `personalization-parameter`. The live backend rejects `div` and tables (`table`, `thead`, `tbody`, `tr`, `td`, `th`) inside `<Text>` (`<div> is not allowed in a text`) — move table-based layout out into `<Html>{"<table>…</table>"}</Html>`. In explicit JSX markup, write `<br/>` and `<hr/>`. Do not generate `img`, `iframe`, `script`, `style` without a separate live check; prefer an image via standalone `<Image>` or inside `<Socials>`.
Available attributes: `style`, `align`, `href`, `target`, `rel`, `model`, `data-rich-*`. Attributes inside rich-text markup must be plain strings or value-less markers only: `<p style="margin: 0;">`, `<a href="https://...">`, `<span data-rich-text>` are correct. `<p style={{ margin: 0 }}>`, spread attributes, and expressions are not allowed — the live backend returns the error `Attribute \`...\` on <...> must be a plain string`.

Plain text (with no markup of its own) is automatically wrapped in `<p style="margin: 0">…</p>`.

The style of the text as a whole (font, size, color) is set via `style={{...}}` on `<Text>` — not to be confused with inline markup like `<strong>` inside it.

## Cards with aligned CTAs

This is about cards of **static** content that you write yourself. Product cards from a mechanic — recommendations, viewed products, order products — are a `<CollectionRow>` product row (`references/product-rows.md`), where the heights are synchronized on their own. The full list of mechanics is in `references/product-rows.md`; what is called a "cart" is not among them: the closest is `SessionGetAddedToListProducts`, the products added to a list during the session.

If you need cards in a row with buttons at the same height, do not assemble each card entirely within its own `Column` — column heights are independent, and the CTAs will drift. Assemble **synchronized rows** instead: separate `FlexRow`s (4+4+4 or 6+6) for images, headings, descriptions, and buttons — then all the CTAs sit in one row at the same top coordinate. The cost: on mobile stacking, the order becomes "all images → all headings → …" rather than card by card; if a card-by-card mobile order matters, that is a product decision (separate mobile rows via `visibilityOnDevices`) — discuss it with the user. Full example: `references/examples.md` §12.

## visibilityOnDevices and "blurred" blocks in the canvas

Blocks hidden for the current device (`visibilityOnDevices="mobile"`/`"desktop"`) are shown by the Maestra canvas editor as **blurred — this is an editor visualization, not a defect in the email**: in the sent HTML, hiding works via media queries, and the PNG preview at desktop viewport shows only the desktop variant. Therefore:

- do not remove device variants just to clean up the canvas — doing so silently sacrifices the mobile layout;
- if the user is alarmed by "blurred cards" in the editor — explain that these are device-hidden duplicates, not broken images;
- the decision to drop the responsive variants and keep a single layout is a product decision — discuss it with the user explicitly.

## Self-check (mandatory before output)

**"Values", "Value shapes" and "Mobile typography" do not apply to a library block**: do not add `style.mobile`, do not convert string numbers into numbers, do not complete partial attributes. Check everything else as usual.

- **Visual hierarchy** (for emails longer than one section): at least two sections with an opaque `background`, at least one of them contrasting with the rest; three text size levels — given either by different `fontSize` values or by different `themeVariant`s (`h1`/`h2`/`text`), and the latter is no worse: the sizes live in the letter styles of the email; the CTA has a brand `background` set, if the brand or reference is known; lists are assembled as a grid, not a single column. An email made of sections with no background, text of a single size, and a black-and-white button is unfinished, even if valid.
- **Grid:** the sum of `size` across all columns in every `FlexRow` and `<Split>` **equals 12** (strictly ==, not ≤). For example: `12` (one), `6+6` (two), `4+4+4` (three), `8+4`, `3+3+6`. Empty columns fill out the grid or narrow the composition, when a narrow one is visible in the mockup or named by the user — but they do not center: a single centered row is given by `Column size={12}` with `style.align`, not by margins made of empty columns on the sides.
- **Migration:** elements adjacent in one source HTML/Klaviyo container
  (table row/div-row) lie in one `FlexRow`, and have not drifted apart into several `12` rows;
  the container's proportions are translated into integer `Column.size` values summing to 12 (`600+600` out of `1200` → `6+6`).
- **Completeness of a port from a mockup** — the source of the look can be anything: an image, Figma, HTML, a link to a page.
  Verified against the source that the images and logos are in place, all text blocks, spacing and sizes,
  the buttons with their links, the footer's composition, and when porting a whole email — the background and width on
  `<Template>`. The goal is one-to-one, even if the request says nothing beyond "make it like the mockup".
  Whatever could not be ported is named to the user as a list: there must be no silently dropped elements and no silently
  simplified styling.
- **Pixel → grid:** `Column.size` is an integer 1..12 only. A pixel width does not map onto
  the grid directly: 480px out of 1200px = 4.8/12 and will be rejected by the backend. Choose the cut of a stripe
  along twelfth boundaries: 480 → 500 (`5+7`). Do not write fractional sizes —
  the backend rejects them, it does not round.
- **Inter-block spacing:** in a new/modified layout, ordinary spacing is done via
  `innerSpacing`, so the section background is preserved. Every new `gapAfterBlock` is justified by an
  explicit request or a visible outer color gap in the layout; an untouched existing
  gap is preserved on an unrelated edit.
- **Button width:** if `buttonSize.width` is set, `widthType` stands next to it — without it the number is read
  as percent (the default), and `{ width: 240 }` will turn out to be 240%, not 240px. Both kinds are accepted: `"percent"` and
  `"pixels"`. Pixels are for a mockup with a specific width and with the caveat that they do not shrink on
  mobile and will be clipped in a column or card narrower than their value.
- **Runtime-required attribute:** `Column.size`. For a new CTA, `Button.url` is required by policy, but the converter only validates the URL if the attribute is present.
- **Minimum nesting:** `Template` contains at least one `Block`; every `Block` contains at least one row — a `FlexRow` or a `CollectionRow`. Every `FlexRow` contains at least one `Column`. For the card structure of a `CollectionRow`, apply the mandatory `references/product-rows.md`.
- **Root tag:** exactly one `<Template>`, nothing outside it. `<Theme>`, if present, is a single one and directly inside `<Template>`.
- **Button.url is validated** by the converter: `https://`, `tel:`, `mailto:`; survey links are an error. A separate HTTPS policy from the "Images" section applies to Image.
- **Values:** strings in quotes, numbers and objects in `{}`. Objects are partial merge (only changed fields). Arrays are a full replacement.
- **Value shapes:** for every `*Gap` (including `cardGap`, `rowGap`) the value is an object `{ size: N }`, not a number; for `columnCount` and `rowCount` — `{ value: N }`. In general, a setting keeps the shape of its default.
- **Mobile typography:** for every `<Text>` where `style.fontSize` or `style.align` is set, `style.mobile` is specified with deliberate `fontSize`/`align`. A `<Button>` with `simpleTextStyles.fontSize` set has `simpleTextStyles.mobile.fontSize`. After convert, there is no unexpected `{ fontSize: 18, align: "left" }` for important desktop text. For a `FlexRow` with 2+ columns it has been decided whether to collapse them on mobile: by default the columns stack vertically, a row of tiles or icons is kept in a line via `isColumnsMobileAdaptive={false}` (§4 `dsl-surface.md`).
- **Fonts:** no new `font.family` is present unless the user confirmed that the
  family is already available in the editor; an existing family is not changed on round-trip
  without a request.
- **Escaping in text:** write markup inside `<Text>` only as explicit JSX tags (`<br/>`, `<strong>…</strong>`). A quoted string in `<Text>` is **literal text**: the live backend escapes it (a `<p>` becomes visible text, not a paragraph). Move raw HTML fragments (an unclosed `<br>`, a comment, an `&nbsp;` entity, a table) out into `<Html>{"…"}</Html>`. Do not mix bare text and a quoted string in one element — live rejects it (`<Text> may only contain text`).
- **Button content:** plain text only, no markup.
- **Divider:** self-closing `<Divider />`, content forbidden; `border` set in full with one thickness on all four sides, `innerSpacing` not zeroed out, a full-width divider is in its own `FlexRow`; if preview/QA is performed, the line is visible in the preview.
- **Links:** no placeholder URL in any new `Button`/`<a>`/`Image.url`; a clickable
  `Image.url` is set only from an explicit HTTPS URL given by the user; placeholders from an existing
  email are preserved and listed to the user.
- **Groups:** at least one item. In `<Menu>`, all items are either only `<Text>` or only `<Button>` (do not mix); in `<BulletList>` — only `<BulletItem>`; in `<Socials>` — only `<Image image={{...}} />` with a confirmed URL.
- **`BulletList`:** a supported `bulletIcon` is set: a flat `{ url, fileName }` for
  a small 4px dot, or `{ type: "custom", url, fileName, size: N }` for a large
  marker/badge. Without it, the default marker breaks the layout. Different numbered icons are not
  placed as items in one list sharing a common icon; a list of ordinary features with a heading
  and description is assembled as a grid, not as a list.
- **Split:** contains only `<Column size={N}>`; a column has only `size` and 0..1 element. Do not nest `<Split>` inside `<Split>`.
- **The format already held an email:** the replacement is confirmed by the user — including when "let's start over" was said in the middle of edits — and the look of the new content is built per their own answer: "in the existing styles" means nodes without their own styles plus `themeVariant`, "new" and "reset to platform styles" mean an explicit `<Theme>`; there is no silently inherited styling.
- **Letter styles** (§8 `dsl-surface.md`): a node names nothing from the covered set or names it in full; a part of the set — only where the node's look must not change along with the letter styles. The fields inside `<Theme>` are taken from the `visual_template_theme_get` fragment and only from there. `<Theme>` itself is written only on a request to change the styling of the whole email: exactly one, inside `<Template>` before the blocks.
- **The move into letter styles** (if there was one) is verified against §8 `dsl-surface.md`: the set in the variant matches the one taken off field by field, by values, not by preview; the mobile sides are carried over; the surplus looks are left unique and their number is named; `<Theme>`, the removed styles and `themeVariant` went out as one document.
- **Group visibility:** set `visibilityOnDevices` on `<Menu>`, `<BulletList>`, `<Socials>`, `<Labels>`, or `<Split>`, but not on their items: `<Label>` has no such attribute at all.
- **Images:** every authored `<Image>` has a source — `image={{ mode: "static", static: { url, fileName } }}` or `image={{ mode: "dynamic", dynamic: [<Var … />] }}` without an invented prefix. The source URL starts with `https://` and came from the user or was returned by Ops from a confirmed gallery DTO; there is no bare Image, no author-supplied forbidden schemes, and no invented Socials URLs. If size/alignment of a standalone image was requested, they are set via `Image.size`/`Image.align`, not via extra columns or side `innerSpacing`; a fixed size has a deliberate mobile branch. A source that arrived inside a library block is already confirmed.
- **Unsubscribe:** the email **has** the canonical unsubscribe link — or the response says why it is absent (a transactional email, or unsubscribe from the wrapper/campaign settings). Then by form: the canonical link is not duplicated; a new `${Message.UnsubscribeLink}` is allowed only as the exact `href` of an `<a>` inside `<Text>`, and in a button's or image's `url` the `SpecialLinkUnsubscribeLink` chip stands instead of the token. No `<Button url="${Message.UnsubscribeLink}">`, fake `/unsubscribe`, preferences-as-unsubscribe, or other new `${...}`/`{{...}}` variables — personalization is written with `<Var>`, not as a raw `${...}` template string.
- **Personalization:** every `<Var>` has a `param` from `references/personalization.md`; no tenant-specific setting (`customFieldType`, `externalSystem`, `orderExternalIdSelection`, `promoCodePool`, `balance`, `hostname`) is empty or invented; the product families (`Product*`, `ProductView*`, `ProductListItem*`, `SingleProductListItem*`, `OrderItem*`) stand only inside a product-row card, not in a regular column; *(automated only)* parameters did not end up in a bulk campaign. Every tenant-specific `systemName` came from `entities_list` or from the user, none is invented; `name` and `internalId` are carried over alongside if they are in the response. No `type` is written in `customFieldType`. Existing `<personalization-parameter model="…">` are not rewritten. Every text chip in a product-row card (`ProductName`, `ProductDescription`, `ProductVendorName` and their twins in the other families) has a `formatString`: a limit from the presets `40`/`80`/`120`/`200` for products from a mechanic, `isTruncateEnabled: false` for manually selected ones. The default 150 breaks the card heights.

## Unsupported → decline or simplify

The prohibitions themselves are stated in "Not implemented" and the topical sections; this is
what to do instead, when a request runs into them.

- `<Var>` is not a blanket-unsupported tag: use it only per the rules of `references/personalization.md`, with a known `param` and the required settings filled in. Do not invent an unknown `param` or its settings. If the parameter is absent from the static list but the user names it exactly, check it through the converter; relay the converter's rejection verbatim.
- A request to change the look of a single node when the node goes under the letter styles of the email → take
  it off them by writing out the **whole** set explicitly (§8 `dsl-surface.md`), do not edit the letter styles:
  an edit to the letter styles will ride through the whole email. Take the missing values from
  `visual_template_theme_get`, do not invent them.
- `targeting` on Block/Row → explain that it is an external setting: it cannot be
  emulated via JSX and is configured outside the email.
- Dynamic content (RSS, a feed) → decline.
- An image without a confirmed HTTPS URL (rules in "Images") → ask for an HTTPS URL or hand the file to Ops for the gallery; do not substitute anything from a forbidden scheme.
- A request for a "personal", "dynamic" image or an image from a customer/order field → this is `mode: "dynamic"`, not a missing source: ask for the parameter, not for a file, the gallery or a base domain.
- A bare `<Image />` in existing JSX → ask for a URL or obtain one via Ops per the gallery rules and replace the Image before writing it back.
- The converter error `needs a value in ...` → the named setting of a chip is not filled in: get the name via `entities_list` or from the user; do not remove the attribute and do not substitute a placeholder.
- The editor error **"The campaign contains unknown parameters"** has several causes. First read the expression itself: `Recipient.Recommendations...`, `GetProductList(...)`, `Products.GetBySegment(...)` → open `product-rows.md` and check the mechanic, the source settings and the family; `Order.IDs...`, a promo-code, balance, custom field or external-system path → open `personalization.md` and check the exact catalogue and `systemName`; an expression that matches no known pattern → do not diagnose from memory, show it verbatim and check the corresponding reference/lookup.
- The error `Line N, symbol M: Invalid symbol` on link enrichment or save → the email has a chip with an empty tenant-specific setting: the expression came out without a name (`Order.IDs.`). Find the `<Var>` whose lookup-based setting is not filled in, get the name via `entities_list` or from the user and rewrite the JSX. The number of errors = the number of broken places.
- A timer or video → explain the limitation and offer Text/Button.
- An unclear CTA or a clickable image with no URL → ask one clarifying question.
  No `https://example.com`, `https://`, `#`; do not create a `<Button>`
  or `Image.url` without a link. A clickable image is expressed via `Image.url`.
- A divider with zeroed-out `border` or `innerSpacing` → do not hand it off as a finished result: the line will not be visible.
- The user asks for an unsubscribe button → make it a `SpecialLinkUnsubscribeLink` chip in `url`, not a token in a string. Do not generate fake URLs or arbitrary tokens.
- Editing an existing campaign "by ID only" → hand the task to Ops:
  `campaign_get` → `visual_template_get`. If the template cannot be expressed in JSX or there is no
  visual format, do not run a workaround JSON conversion: suggest the UI. A separately
  provided JSX can be edited/shown, but do not write it into an unconfirmed or
  incompatible format. Do not invent `mailingInternalId`, `variantInternalId`, or
  `formatInternalId`.

## Where to go for details

| Situation / signal | File | What's there |
|---|---|---|
| Any value shapes beyond the copy-safe forms in the "Value rules" section — MANDATORY before generating | `references/formats.md` | Exact value shapes: `buttonSize`, standalone `align`, `gapAfterBlock`, `verticalAlign`, `Image.size`/`align`/`url`, `bulletIcon` |
| Unsure which tag/attribute to use, need the full markup grammar | `references/dsl-surface.md` | Full DSL specification: attributes, hierarchy, grid, text markup |
| Need the layout's rhythm: which spacing, height or size will appear on its own — MANDATORY before generating | `references/dsl-surface.md` §6 | "Defaults that appear on their own": the only place with the default values |
| The email contains products — recommendations, cart, viewed products, order products, a product list — MANDATORY before generating | `references/product-rows.md` | The product row in full: the mechanics and their required settings, which chip family gets you what, the card and its heights, manually selected products |
| A request about the letter styles of the email ("Design"), the email's width or background, `themeVariant` — MANDATORY before generating | `references/dsl-surface.md` §8 and §4 | How a node is taken off the letter styles, why the set is written in full, the `<Theme>` tags and the root's attributes |
| The first personalization in the email — MANDATORY before generating | `references/personalization.md` | The forms of `<Var>` in text / a value / words / structure, what comes from a lookup, the common parameters |
| A personal image or a personal link | `references/personalization.md` § "Where it can stand" | The `image={{ mode: "dynamic", … }}` form and the segmented `url` |
| The needed parameter is not among the common ones | `references/personalization-parameters.md` | 43 parameters of the email itself with attributes: recipient, promo code, points, custom fields, order data |
| The needed product value is not in the "value → name" table | `references/product-parameters.md` | 125 product parameters by entity: `product`, `productListItem`, `singleProductListItem`, `orderItem`, `productView` |
| A label, a badge, a "discount on a background", a "bestseller" corner tag — MANDATORY before generating | `references/dsl-surface.md` §6 "Labels and Label" | That `<Label>` lives only inside `<Labels>`, the content form with a list of segments, the behavior on an empty variable and the "display filter" |
| Any numbered-point block — MANDATORY before generating | `references/examples.md` §14 | Sample `BulletList` custom icon and notes on mobile |
| Need a typical email fragment as a sample | `references/examples.md` | Input→output examples by block type |

