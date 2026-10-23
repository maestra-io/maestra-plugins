---
name: maestra-email
description: Creates and edits emails for the Maestra email editor (visual builder) from a text description. Use when the user asks to create or change an email, describes an email template, or asks to make a campaign — including personalized content, product recommendation rows and letter styles. The technical layout is handed over for preview and saving through the companion skill maestra-email-ops.
metadata:
  author: Maestra.io
  version: 1.18.2
---

# maestra-email — email generation

The Maestra email editor stores an email as a tree of blocks; this skill writes that tree as JSX — `<Template>`, `<Block>`, `<FlexRow>`, `<Column>` and the elements inside — from the user's words, a mockup or an email read back from a campaign. The converter turns the JSX into the editor's JSON and refuses what it cannot read; each tag's page under `references/wiki/` holds its attributes and defaults, this file holds the procedure and the rules that span tags.

## Skill boundaries

Every operational action — gallery and uploads, conversion, preview, reading a campaign or
its template, saving — belongs to the companion skill **maestra-email-ops** ("Ops" below); this skill (the Generator) writes the JSX and corrects it from Ops's
feedback; it fixes errors about the JSX and none about the operation (gallery, ids, network). Campaigns, recipients, test sends are Ops's. A change of the template type ("rebuild it in the visual
editor", "convert it to HTML") is Ops's route too: the JSX is assembled after Ops decides where it will be saved.

## Communicating with the user

As `maestra-email-ops`, "Communicating with the user": say "email", "layout", "content", "preview", "saving" — no JSX, GUIDs or `rowVersion` unless the user asked for code or technical details.

## Feedback to developers

A critical problem in these rules, or the user asking to pass feedback to the developers, goes through `maestra-email-ops` and its protocol: the full text is shown to the user first, sent
only after their explicit confirmation.

## Workflow

0. **Email details card — mandatory before a new email.** Building a new email — from a description, a mockup or a reference, a rebuild or redesign of an existing one, a copy into a new campaign, a port from another platform, an email by one of the project's saved templates — starts with one card that gathers every open question: where to save it, automatic or manual, which data to show, the product layout, which reference images to take, the style — and, when the look is not given, where to take it from (the brand's last 3 one-off emails, the last 3 flow emails, the website, or the client's brand book uploaded right in the card). **You MUST read `references/email-details-card.md` first.** Find out what the project and the reference already tell (`campaign_get`, `entities_list`, the reference itself), put that in as preselected options, and ask only the rest, 2–5 questions. With the visualization tool in the host (`show_widget`) the card is drawn with it; without it — the host's native choice tool; without either — one message of numbered questions. Nothing is generated, uploaded or created (`campaign_create`, image upload, JSX) before the answer, a Skip, or — when nothing is open — one line saying what you decided. Small edits of an existing email (a text, a color, one block) don't get a card.

1. **Read the request.** Identify the blocks (heading, body, CTA, image, divider); a new marketing email gets a footer with an unsubscribe link (`references/wiki/unsubscribe-link.md`). The situation changes what step 3 writes:
   - **Adding headings or buttons to an existing email** ("Letter styles" below) — look named (in the request, the mockup, by example): write it inline, do not ask whether to take the email's look instead. Look not named: write no styles, the nodes follow the letter styles. "Like the heading above": copy that node; if it follows the styles, the new one stays empty.
   - **Editing an existing email** — everything the request did not name is written back as read, even when it looks odd (*Read email* below); list to the user only what breaks the sent email: a placeholder link, an image without a source.
   - **Building a new email into a format that already contains one** — Ops asks the user before generation; build by their answer. "In the existing styles" — nodes without styles, the variant by `themeVariant`. "New styles" or "reset to platform defaults" — an explicit `<Theme>` (`references/wiki/theme.md`, "An email without its own letter styles"); without it the previous styles remain. "Let's start over" in the middle of editing is the same case: a replacement, not an edit — Ops asks again first.
   - **An email by a saved template** — Ops reads the template and hands over its JSX: work on it as on an email that was read (the "Editing an existing email" case). Ops saves it with the template's letter styles — no `<Theme>` unless the user asks to change the styles.
   - **A reference is given** (a website, a brand, a screenshot) — fix before generation: 2–3 brand colors in `#RRGGBB`, a contrasting pair of sections, three levels of text size, and apply them through the structure of sections, background and color, not only text. The default styles are a stub for when nothing is known, not the target look.
   - **Restyling an existing node that follows the letter styles** — Ops first names how many nodes the styles cover and asks (`maestra-email-ops`); "this one" — on the node, "all of them" — in the styles.
   - **A saved editor block is asked for** ("our footer from the editor") — Ops finds it and the user picks it (`maestra-email-ops`, the saved-block route); place it instead of the named section and leave the rest untouched: `kind` `block` comes as ordinary `<Block>` JSX and is placed as it came, `quokka` and `sync` as their tags. If the email uses a theme, warn: the block's styles are fixed values and no longer follow it. Nothing found — say so, then offer to build it.

2. **Get the inputs through Ops before generating:** every image address, the theme fragment when a look moves into the letter styles, the product mechanic and tenant names from lookups.

3. **Generate JSX** along `Template → Block → FlexRow → Column → elements`; before the first node of any tag read its page from "Tags and pages". A styled attribute as "Letter styles" says; where nothing was said about the look, write no styles (step 1), but economy of edits is not giving up styling — set color, size and background where the design requires them; heading levels by `themeVariant`. Enumerations of features, plans, benefits, metrics are a **grid** — `FlexRow` 6+6 or 4+4+4 with `background` and `borderRadius` on `Column` — not a list, unless the user asked for a list.

4. **Check the output against "Rules across elements" and "Letter styles"** — the converter does not catch them. With a mockup, compare it element by element and the spacing number by number — spacing is where an email diverges from the original most often, and the preview does not show the difference; whatever is not carried over is named to the user, and pixels rounded to twelfths are named with the cause (`references/wiki/containers.md`, "The grid").

5. **Before the first save** — not before handing the email to Ops — when two or more nodes repeat the same covered look (spacing is not a look), offer to move it into the letter styles: "Save this email's styles as its letter styles? Then you'll be able to change headings and buttons across the whole email at once." If the document already carries `<Theme>`, the question is about moving the repeating look into that tag. Consent, or an explicit "make these styles the email's design" — move them by `references/wiki/theme.md`; a node whose look differs on mobile is moved only after its own question — the difference is lost (`references/wiki/theme.md`, "Moving styles"). A refusal is a legitimate outcome. **One conversation — one such question:** the answer holds to the end, whatever previews, saves or edits follow.

6. **Output to Ops: bare JSX** — no fences, no comments, no prose. Preview and save are Ops's (`maestra-email-ops`, "Checks, preview and QA"); an error about the JSX comes back to you — fix it and repeat only the requested check. After a successful save, Ops closes with a one-line offer of an inbox-style mockup of the email — before/after when there is an earlier version (`maestra-email-ops`, "Inbox mockup: before/after"); the Generator builds nothing for it.

## Tags and pages

```text
Template → Block → FlexRow → Column → elements        Block → CollectionRow (the product row) → cards → Column
```

`Template` holds at least one of `Block`, `QuokkaBlock`, `SyncBlock`; a `Block` at least one row; a row at least one `Column`; the converter refuses a broken chain and names the tag. A row is a `FlexRow` or the product `CollectionRow`. The page of a tag holds every attribute with its default and the snippets; here only what decides which tag to pick.

| tag | where it stands / what it holds | what it is for, and when to pick it | page |
|---|---|---|---|
| `Template` | the root, exactly one; `<Theme>` first, then the blocks | the email's width and background | `references/wiki/containers.md` |
| `Block` | an email section; rows or a `CollectionRow` | one section with its background and spacing; a strip of the page between sections (`gapAfterBlock`) only when asked for | `references/wiki/containers.md` |
| `FlexRow` | columns | the row of a section; decides whether its columns stack on the phone | `references/wiki/containers.md` |
| `Column` | elements; empty only for the grid, never to centre or to space | `size` in twelfths, one row's sizes sum to 12; a card is `background`, `borderRadius`, `innerSpacing` on the column; cards side by side with buttons at one height — "Synchronized rows" | `references/wiki/containers.md` |
| `Text` | one size and one font per block: a heading and its paragraph are two `<Text>` | words and markup: a heading, a paragraph, a link in a line, a plain list inside a paragraph (`<ul>` markup, no marker image) | `references/wiki/text.md`; fonts `references/wiki/typography.md` |
| `Button` | | the call to action: a plain caption and an address | `references/wiki/button.md` |
| `Divider` | self-closing | a horizontal line | `references/wiki/divider.md` |
| `Html` | a quoted string between the tags | the last resort — a table, Outlook conditionals — never for what the elements above express | `references/wiki/html.md` |
| `Image` | self-closing; also a line of `Socials`; always with `alt` | a picture from the gallery, or a dynamic one whose address comes from a parameter — a customer field, a product picture in a card (`mode: "dynamic"`: a chip, not a file) | `references/wiki/image.md` |
| `Menu` | lines without `<Column>`: only `Text` or only `Button` | a horizontal row of links; each line is one `Text` or one `Button`, nothing else — a badge beside a menu item is `references/wiki/label.md` | `references/wiki/groups.md` |
| `BulletList` → `BulletItem` | lines without `<Column>` | short one-line points with one marker image for the whole list, or any list the user asked for by name; a different marker per line — "The bullet icon" | `references/wiki/groups.md` |
| `Socials` | lines: `Image` | a row of icons of one size | `references/wiki/groups.md` |
| `Split` | an element, not a row of the section: stands inside a column like `Text` or `Button` and lays its own `Column size={N}` side by side, 0..1 element each; no `Split` inside | things side by side within one column — an icon beside text, a price beside its old price; never stacks on the phone | `references/wiki/containers.md`; `references/wiki/text.md`, "Two values in one text" |
| `Labels` → `Label` | **only inside a product row card**; lines: `Label` | badges on a product card; a badge anywhere else is a `<Text>` with its own `background` in a narrow column | `references/wiki/label.md` |
| `CollectionRow` → `CardTemplate` / `CollectionCard` → `Column` | the product row, a child of `Block`; a card's columns hold the same elements plus `Labels`, minus `Menu` / `BulletList` / `Socials` | products from a mechanic — recommendations, a list, order items, viewed products, a manual selection; the mechanic, its required settings and the lookup names come first | `references/wiki/product-rows.md` |
| `Var` | inside `<Text>` markup, in a value's segment list (a personal link, a dynamic image, button words, a label), between `<Button>` or `<Label>` tags | the editor's personalization chip: every personal value — a name, a promo code, a price, a field of the customer; the parameter's entity decides where the chip may stand; a few chips print their own sign or word — the currency after a price, the bonus word, the greeting — never written next to them again; an unread `<personalization-parameter>` is carried over and named | `references/wiki/personalization.md`; a parameter not among the common ones `references/wiki/personalization-parameters.md`, a product value `references/wiki/product-parameters.md` |
| `QuokkaBlock` → `Collection` → `Item` | a block laid out in an editor template | **only carried over** from a read email or the library, never generated; its settings via Ops's `visual_template_quokka_block_describe` | `references/wiki/quokka-block.md` |
| `SyncBlock` | self-closing | a block shared between emails ("universal block" to the user): **only carried over**, never generated, its content not edited through MCP | `references/wiki/sync-block.md` |
| `Theme` → `TextStyle`, `ButtonStyle`, `LabelStyle`, `BlockStyle`, `RowStyle` | not an element: inside `<Template>` before the blocks, one at most | the letter styles ("Letter styles", *Styles*) | `references/wiki/theme.md` |

**Forbidden:** any tag not in the table (`MenuItem`, `SplitColumn`, …).

Pages that belong to no single tag:

| signal | page |
|---|---|
| The unsubscribe link (step 1): the two accepted forms, an existing one kept, one hidden inside a `<SyncBlock>` named rather than duplicated | `references/wiki/unsubscribe-link.md` |
| A pixel mockup onto the twelfths grid, what spacing adds up from, mobile stacking and order; «tighter», «more air», «stuck together», «too much air» | `references/wiki/containers.md` |
| What the preview shows that the email will not: `href="#"`, sample values, placeholders, blurred blocks | `references/wiki/canvas.md` |
| Building a new email — the mandatory step 0, before anything else | `references/email-details-card.md` |

## Letter styles

An email carries a set of styles per variant — `themeVariant` `h1`/`h2`/`h3`/`text` for text, `primary`/`secondary` for buttons and labels. A node that writes none of the attributes those styles cover *follows* them and changes with them. Writing a covered attribute gives the node its *own look*; write only the fields you change — the ones left out, the phone side included, come from the styles of the node's variant (`Block` and `FlexRow` have one set each, no variant), so a button with a size of its own writes `widthMobile`/`heightMobile` next to `width`/`height`. The current values are the *fragment* `visual_template_theme_get` returns through Ops — for moving a look into the styles and checking the values after the move. The `<Theme>` tag, the move of a look into the styles — `references/wiki/theme.md`.

## Rules across elements

- **Image sources.** Every address — `Image`, `Template.background`, `<img>` inside `<Html>`, `bulletIcon`, `iconSrc` — is the `{url, fileName}` pair Ops returned, never one of your own or the user's; nothing to give Ops — ask before generating; several gallery candidates — the user picks, never one by name; a file Ops could not place — the image part stops and is named (`references/wiki/image.md`, "Where the address comes from").
- **Alt text on every image.** `<Image>` takes `alt` (in a product card — the product name chip), every `<img>` inside `<Html>` carries `alt`, a `<Socials>` line gets the network name; the text is what the image says or does, read off the image, `alt=""` only for a decorative one; a carried-over email keeps meaningful alts and gets the missing ones written (`references/wiki/image.md`, "Alt text").
- **No address.** A new node never gets a placeholder URL. A button, an image or a menu line that needs an address and has none: ask once, for all such elements together; then write it without `url` and name it in the response (`references/wiki/button.md`, "No address").
- **Personal values.** A personal value is `<Var>`, never a `${…}` expression written as text. `param` and every tenant-specific setting come from `entities_list` lookups or from the user, carried as the row returned them — `systemName`, `name`, `internalId`, `type` for a custom field — never invented.
- **Read email.** Everything the request did not name — in a read email or in a library block taken via Ops — is written back as read: markup with its `data-rich-*` markers, `font` objects, `<QuokkaBlock>`, `<SyncBlock>`, placeholders and the editor's storage forms. A carried-over node gets no `style.mobile`, no number converted from a string, no attribute completed or trimmed — trimmed, it would fall under the letter styles on the next read.
- **One `<Text>` — one size and one font.** In the editor the style of a text block applies to the whole block, so a heading is its own `<Text>`, and so is any line that differs from its neighbours in size or font — a subheading, a caption, fine print; no `<span>` with `font-size` or `font-family`, no `h1`–`h6` next to other lines in one `<Text>`. Bold, italics, a link, the colour of a word, a chip, a line break, a list stay inside one block. A source section that mixes them is split into several `<Text>` one under another (`references/wiki/text.md`, "One size and one font per text"); text the request does not touch, a library block or a `<QuokkaBlock>` is not restructured.
- **Fonts.** A new `font.family` only from the lists in `references/wiki/typography.md`; a family that is not there — the closest, and tell the user. A project's own font already in the email (a `font` with an `internalId`) is not on the lists and stays as it came.
- **`targeting`** is never written: a block for a segment is set in the editor; one read with the email is carried over.
- **Styles.** A look asked for the whole email ("Montserrat everywhere", brand colors for all buttons) is `<Theme>` at once; a look given per element stays on the element until step 5 offers the move.

- **Page rules a preview passes silently** — `url` on every `<CardTemplate>` and `<CollectionCard>` (`references/wiki/product-rows.md`); every text chip in a card carries `formatString`, *(automated only)* parameters absent from a bulk campaign, product chips only inside a card (`references/wiki/personalization.md`); `bulletIcon` on every `<BulletList>` (`references/wiki/groups.md`); `<Labels>` only inside a product row card (`references/wiki/label.md`); `mobile` written where the phone must differ, not as a copy of the desktop, and for every `FlexRow` with 2+ columns decided whether they stack (`references/wiki/typography.md`, `references/wiki/containers.md`).

## Value rules

- Strings in quotes; numbers, objects and lists in `{}`. Literals only: an expression, a variable or a comment is refused.
- **On a new node write only what you change.** An object is completed field by field from the node's own defaults — or, for a covered attribute, from the letter styles — never from the previously saved email. A value of another kind is new rather than an edit — a `border` of `type: "none"`, a background of another `type`, a `font` replace the one there whole. Units are written with their width — `widthType` in `buttonSize`, a side's `type` in an image's `size`. A list is replaced whole; to reset a setting write its empty value — `0`, `""`, `{ type: "none" }`, `{ type: "transparent" }` — not nothing. A node read from the email is written back whole (*Read email*). `mobile={{…}}` is not an attribute: mobile values live inside the attribute's object (`innerSpacing={{ top: 24, mobile: { top: 12 } }}`). A covered attribute — "Letter styles".
- **A setting keeps the shape of its default.** A wrong shape is refused with the expected one shown — read the message. An unknown attribute on a tag is refused; an unknown field inside a setting's object is stored and ignored silently, so field names come from the element pages, not from memory.

## Refuse or simplify

- A backend error about parameters — “The campaign contains unknown parameters: …” on the campaign card or at save (an invented or wrong name in a chip or a mechanic setting), or `Line N, symbol M: Invalid symbol` (an empty setting) → re-check every `<Var>` and every mechanic setting against the lookups — `references/wiki/personalization.md`, "Errors from the backend". A converter refusal names its cause and is passed on verbatim.
- Dynamic content (RSS, a feed) → refuse. A countdown timer or a video block → not writable in JSX: say so and build the rest; the user adds the block in the editor after the save. Meanwhile a video is an `<Image>` preview with the link in `url` — that is what the sent email carries anyway; a deadline is plain text.
- A request the DSL cannot express, as the tag's page states it → say so and offer the ways out that page gives; never an approximation passed off as the request.
- No visual format, or a template that is not JSX → offer the editor UI, no workaround JSON; `mailingInternalId`, `variantInternalId`, `formatInternalId` are never invented.
