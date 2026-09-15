---
name: maestra-email-ops
description: Operational actions for Maestra emails — preview, reading and saving the visual template, letter styles, saved blocks, reading/editing campaign metadata, test sends, searching gallery assets via MCP, uploading attached/local images via MCP upload link, PNG preview links. Use together with the maestra-email generator when you need images, preview, validation, test sends, or writes to Maestra.
metadata:
  author: Maestra.io
  version: 1.11.0
---

> Note: `Mindboxeditor` is the platform's literal editor-kind value returned by the API (legacy name); do not rename it.

# maestra-email-ops — Maestra operations for emails

Project-aware executor of all integration actions. The JSX generator is
`maestra-email`; this skill does not invent email content and **does not change JSX
silently**. Return preview errors to the generator verbatim — this is editor
text that contains line numbers; do not rephrase or classify it.

## Communicating with the user

JSX, internal IDs, and rowVersion are internal execution details. In ordinary conversation with
a CSM, say "email," "email layout," "content," "preview," and "save" —
not JSX, `mailingInternalId`, `variantInternalId`, `formatInternalId`, `rowVersion`,
or `visualTemplateRowVersion`. Don't replace the terms Active/Draft: when they're needed for
precise version selection, use exactly Active/Draft. Don't show raw JSX or GUIDs
unless the user has explicitly asked for code, export, markup, or technical details.
Return backend errors verbatim, even if they contain technical terms, tag
names, line numbers, or identifiers.

## Feedback about the skill via MCP feedback

The MCP `feedback` tool of the current Maestra MCP server is an optional channel for passing
confirmed feedback about the skill's operation to the developers. Use one of two entry points:

1. **Agent initiative.** If you have confirmed a critical problem that can't be
   solved with the current skill's own means — a mismatch between the instructions or
   catalogues and the actual backend behavior, repeated errors of one type, a blocked
   safe workflow — offer the user to send feedback to the developers. Don't send
   without explicit consent.
2. **User initiative.** If the user asks how to pass a message/feedback to the
   developers, answer: "The feature is available. What message would you like to
   send?" Then format their words using the format below.

The sending protocol is mandatory in both cases:

1. First compose the exact message text. The first line is the marker
   `[skill-feedback:v1]`, then the fields `skill=mailings-generator-editor`,
   `skillVersion=<from plugin.json>`, `source=user-report|agent-observation`,
   `problem` and `context`. `problem` is the essence: what gets in the way, what went
   wrong. For `user-report`, put the user's verbatim words into `problem` and write
   `context` yourself. For `agent-observation`, you write both fields. `context` is
   brief: the input data and requests, how the current situation was reached, verbatim
   backend error texts, reproduction facts (run date, one-off
   campaign). Add `area=<layout|save|preview|gallery|personalization|other>`
   only if the area is obvious.
2. **Always show the user the full text to be sent first** and ask for
   explicit permission, for example: "Send this feedback to the developers?"
3. Call `feedback` in exactly the current Maestra MCP server through which this
   skill's operations are performed, and only after an unambiguous confirmation.
   If the user asks to change the text, show the corrected version again
   and get confirmation again.
4. Don't send feedback covertly, don't assume consent, and don't attach it
   silently to another operation. Don't include email content, personal data,
   secrets, signed URLs, or tokens.

## Capabilities

- on user request or for diagnostics, renders JSX via
  `visual_template_preview`: the user gets a fallback `htmlUrl` link, and in a
  supporting host an MCP App widget opens;
- reads campaign metadata (`campaign_get`);
- reads the existing visual JSX of the selected format (`visual_template_get`) and the JSX of saved blocks the user picked in the panel (`visual_template_saved_block_list` → `visual_template_saved_block_get`);
- hands the generator the email's current letter styles (the editor's Design tab) as a `<Theme>`
  fragment (`visual_template_theme_get`);
- saves JSX to the selected campaign format after explicit confirmation
  (`visual_template_save`);
- changes basic campaign settings (`campaign_edit`);
- changes subject/sender/reply-to/preheader or raw HTML on explicit request (`campaign_edit_content`);
- creates an empty email campaign after an explicit folder/brand/timezone choice (`campaign_create`);
- sends a test email to staff test recipients after the user has explicitly chosen them
  and confirmed (`campaign_test_recipients` → `campaign_send_test`);
- searches for existing gallery assets via MCP `gallery_images_list` and returns ready-made `{url, fileName}` to the generator;
- uploads attached/local images via MCP `visual_template_image_upload_link` and uses the returned `fileUrl`;
- builds a visual contact sheet for picking images from the gallery: remote HTML for
  Codex/local and self-contained HTML for the Cowork side panel;
- optionally verifies the content of downloaded HTML and inspects the desktop/mobile PNG snapshots
  that arrive as links in the same preview response; this is supplementary
  QA diagnostics, not a gate on the main workflow.

Live send/activate/delete and recipient edits are not available in MCP — they are done in the campaign UI. A test send to staff test recipients is available — see the "Test send" section.

## MCP tools and local helpers

Gallery operations are performed only via MCP. Don't set up a project-local env,
cookie, or token for searching/uploading images: MCP tools already run in
the project's context. If a gallery MCP tool returns an error, pass it to the user
as a tool error and don't diagnose it via local authorization.

Local scripts in this skill are used only for the visual gallery contact sheet.
PNGs arrive as links in the preview response, with no local rendering or screenshots.

| Script | Purpose | Key arguments |
|--------|-----------|--------------------|
| `gallery_contact_sheet.py` | JSON from `gallery_images_list` → self-contained HTML with base64 thumbnails for the Cowork side panel | `<images.json> <out.html> [--max-px 96] [--quality 80]` |

## Quickstart: pick a route

| Task | Route |
|---|---|
| New JSX email | target discovery, if a save is needed → gallery → Generator → stale-preview notice / optional preview+QA → canonical visual save workflow |
| Editing an existing email by ID | `campaign_get` → canonical visual workflow with `visual_template_get` |
| Saved editor block | `visual_template_saved_block_list` → the user picks in the panel → `visual_template_saved_block_get` by the `internalId` from their reply |
| Changing the hero/content inside the email body | canonical visual workflow, not subject |
| Changing the template type: "redo it in the visual editor", "convert it to HTML" | "Changing the template type" section: the type doesn't change, the email is ported to a new campaign |
| Changing subject/sender/preheader | `campaign_get` → `campaign_edit_content` |
| Changing name/UTM/schedule | `campaign_get` → `campaign_edit` |
| New campaign from scratch | end-to-end workflow below: `campaign_create` → `campaign_get` → metadata/content edits → visual save; live recipients/send/activate — UI |
| Test send of an email | "Test send" section: `campaign_get` → `campaign_test_recipients` → recipient choice → confirmation → `campaign_send_test` |
| Gallery search/upload | MCP `gallery_images_list` / `visual_template_image_upload_link` |
| PNG | desktop/mobile links in the `visual_template_preview` response |

If data is missing:

- no mailing internalId for reading/editing by ID — stop and ask;
- no precise target for save (`variantInternalId` + `formatInternalId` of each target format) or save confirmation with preview status — stop and ask;
- don't invent `mailingInternalId`, `variantInternalId`, `formatInternalId`, a URL, a gallery asset, or `fileName`.

## Images: confirmation procedure

The Generator uses only URLs that Ops returned or that the user explicitly
provided. Ops never chooses silently.

If the email is to be saved into a specific campaign, before searching for or uploading
images, first run `campaign_get`, select the exact target, and complete
`visual_template_get`/bootstrap discovery. Only after confirming that the target
is available for the visual workflow should you perform image lookup/upload and pass the URL to the Generator.
For standalone generation with no target campaign, this preliminary discovery is not needed.

### Searching for an already-uploaded image

1. Call MCP `gallery_images_list` with `nameSubstring` from the user's request,
   `fileExtensions: [".gif", ".png", ".jpeg", ".jpg"]`, `includeSystemImages: true`,
   and a sufficient `limit` (usually 100). For an email-constructor-compatible search,
   always pass exactly this list of extensions: don't include `.webp`.
2. If the user explicitly asks for project assets only, pass
   `includeSystemImages: false`. Otherwise, system images
   are included by default.
3. The tool searches across all project and platform folders; there is no separate folder workflow.
   Don't narrow the search with local folder workarounds.
4. If there are no candidates, say that no suitable image was found and ask
   for an external HTTPS URL or a file to upload.
5. If there is one candidate, return `{url, fileName}` to the Generator. Take `url` exactly from
   the tool output string: don't assemble, edit, or shorten it. `fileName` is
   `name + fileExtension`, if `name` doesn't already end with that extension;
   otherwise use `name` as is.
6. If there are several candidates, don't choose silently. Show the user safe
   metadata from the actual MCP row: `name`, `fileExtension`, `isSystem`,
   and size/date only if they are actually present in the response. `isSystem: true`
   means a platform shared system icon, otherwise it's a project asset. Show the URL
   only if the user can't tell the options apart without it.
7. When offering an image to the user, explicitly say whether it's a system icon
   from the platform or a project asset.

### Visual selection of images from the gallery

A text list remains the default quick response. Build a visual contact sheet
only when the user asks to look at the images visually, or when there are
several similar candidates and a text list isn't enough.

Selection invariants (apply even before reading the file):

- the email always gets the original `url` from `gallery_images_list`, exactly as
  MCP printed it; with a `.webp` filter the URL may point to an imgproxy conversion of the
  original file rather than the original S3 object — that's normal; `fileName = name + fileExtension`,
  if `name` doesn't already end with that extension;
- the user picks the card number; don't choose similar variants silently;
- a base64/data URL is allowed only for thumbnails in the contact sheet; in email JSX
  a `data:` URL is forbidden;
- Codex/local — remote `<img>` HTML in an external browser; Cowork — self-contained
  HTML via `scripts/gallery_contact_sheet.py` (side panel/CSP), otherwise
  fall back to remote HTML.

**When this scenario triggers, you MUST read `references/visual-gallery-selection.md`**:
it has the full Codex/Cowork procedure, checking and installing Pillow, the remote sheet's
card template, and the result format after selection. Without the file, don't assemble
the contact sheet from memory — it's easy to mix up the remote path and the Cowork path.

### Attached/local image upload

1. For a user's file, call MCP `visual_template_image_upload_link` with the exact
   `contentType`: `image/png`, `image/jpeg`, `image/jpg`, or `image/gif`.
   Don't use other types for this upload workflow.
2. Upload the file's bytes to the returned `uploadUrl` using the exact HTTP method from the response and
   the exact `Content-Type` header matching the requested `contentType`.
3. `uploadUrl` is sensitive and temporary: don't show it to the user, don't
   paste it in full into reports, and don't save it into the template. If the link has expired,
   request a new one via MCP.
4. Upload success is HTTP 200 only. After that, use the returned `fileUrl` in
   the current email template: it becomes the image's source, not the future gallery
   URL. If the Generator asks for a `{url, fileName}` pair, pass `url: fileUrl`, and
   take `fileName` from the original file name only as a service DSL name; don't
   use `fileName` as the image source.
5. `fileUrl` is safe for the email and for a user-facing report. The uploaded
   image will later appear in the gallery/search, but immediately after upload, only
   `fileUrl` is known for the current email — not the final gallery URL.

### External HTTPS URL

If the user gave a direct HTTPS URL for an image, use it as is. Don't
re-upload it to the gallery or convert it into an internal URL without a separate
request from the user.

### Gallery unavailable/errors

If `gallery_images_list` or `visual_template_image_upload_link` returns an error,
pass the meaning of the error to the user and stop the image-dependent part of the workflow.
Don't invent a reason, don't substitute a similar image, and don't ask for local
credentials. Without a confirmed URL, the email can only be assembled without that
image, or with explicit placeholder text agreed with the user.

### Social icons and utility badges

Search for social icons and utility badges with the same `gallery_images_list`, with system
images included by default. System entries come back with `isSystem: true`; these are
platform shared system icons, not project assets. Icons are ordinary HTTPS URLs and
go into `<Image image={{ mode: "static", ... }}>` like any other image.
A single social network often has several styling variants — show the metadata and
ask, don't choose on your own. If the needed social network isn't there, request an external HTTPS URL or
a file; don't substitute a similar icon.

## Verification, preview, and QA

Preview invariants (not deferred to references; full procedure is below the trigger):

- **Preview is no longer an automatic step after every edit.** Each call to
  `visual_template_preview` opens a new MCP App widget in a supporting host;
  old widgets don't refresh. After any JSX change, previous
  preview/HTML/PNG links are stale: say "The previous preview no longer
  matches the current version. I can show you a new preview if you'd like."
- **`visual_template_preview` is called only** when the user asks for
  a preview, HTML/PNG QA, desktop/mobile/debug, comments on specific
  content/rendering, or as read-only for a non-editable campaign.
- **The preview is the editor's canvas, not the email that gets sent**: personalization in it
  is filled with sample values, and they are not customer data. What can and can't be checked on
  the canvas is in `references/preview-qa.md`. The `containerWidth` from the response is for the panel;
  don't relay it to the user.
- **Pass `formatInternalId` as soon as it's known.** With it, the render carries under the
  document its own width, background, "Global (CSS) styles" and letter styles — that
  is, it shows the email. Otherwise the picture is only the document, and it looks no less
  convincing for that. This happens in two ways: the format isn't named, or nothing has been
  saved to it yet — and the tool's response says outright what exactly was drawn. Trust the
  response, not what you passed: a format with a typo lands in the same case.
- **If you inspect the rendering yourself, look at both snapshots.** The mobile layout differs from
  the desktop one in more than details: by default a row's columns collapse into a stack, and what
  sits straight on desktop may fall apart on mobile. A verdict based on one snapshot doesn't
  cover it.
- **HTML is downloaded only for HTML QA/diagnostics; PNG is always links from the preview
  response, there is no separate call for them.** A local screenshot is not the standard
  path (the emergency Cowork fallback is Claude in Chrome, explicitly marked as a fallback). Return
  preview/editor/save errors to the generator verbatim; silent repair is forbidden.
- **Before saving**, show the target, the change, and the preview's freshness status; without
  a fresh preview, the confirmation must explicitly allow saving without a new
  preview. Preview/QA never implies consent to write.
- Never assemble the email's HTML/preview by hand.

Resolve a simple "show/refresh the preview" request per the invariants above:
`visual_template_preview` → widget/fallback link; `references/preview-qa.md` is
not needed for this. **If you need HTML download, PNG, mobile/desktop, QA/debug,
diagnosis of a specific rendering issue, or a fallback, you MUST read
`references/preview-qa.md`**: it covers the download file name, working with MCP PNG links,
QA retries, and fallback branches; without the file, don't perform the extended procedure.
## Editing the visual template

This is the only detailed workflow for reading, editing, and writing JSX. Other sections
only pick the route and don't repeat the save algorithm.

### 1. Target preparation

1. Call `campaign_get(mailingInternalId)`.
2. Record the campaign name, `mailingInternalId`, the current `mailingRowVersion`,
   the variants, the available formats, and any pre-existing validation errors.
3. Before choosing a target, check `kind` and `state` from `campaign_get`. If `kind: Automatic`
   and `state` is not `InDevelopment` — the campaign is already sending, and a write to Active will go out
   to customers immediately. Stop the workflow, save nothing, and tell the user
   that such a campaign needs to be edited in the editor. The same applies when `transactional: yes`.
   `visual_template_preview` is still allowed here — it writes nothing.
4. Determine the exact write target: `variantInternalId` + `formatInternalId`.
5. The visual-write targets are **all formats of the variant for which the visual workflow is allowed**:
   Draft, if there is one, and Active. The draft is a separate version of the same email, and it
   will replace the active one when it's activated, so an edit that went only into Active may
   never make it into the sent email. Don't offer a choice between them — write to all of them,
   **starting with Draft**: if something goes wrong on it, the active version stays
   untouched.
   A format for which the visual workflow is forbidden per item 6 (`Rawhtml` with `html: yes`) doesn't
   become a target: write to the compatible one and tell the user which one stayed as it was.
   The skill cannot create a Draft — formats are created only in the editor.
6. Record the editor kind of each target format from `campaign_get`:
    - `Mindboxeditor` — visual workflow allowed;
    - `Rawhtml` with `html: yes` — this is existing raw HTML, visual workflow forbidden; handle a request
      to move this email into the visual editor via the "Changing the template type" section;
    - `Rawhtml` with `html: no` — an empty-bootstrap candidate: don't ask for the UI, proceed to
      `visual_template_get` and choose the bootstrap/recovery branch based on its response;
      the bootstrap trigger is the verbatim response `No visual template was saved for
      format '…' yet`;
    - editor kind missing or unrecognized — don't guess compatibility and stop.
7. If there is exactly one suitable A/B variant, don't ask an unnecessary question, but show
   the choice in the final confirmation. If there are several variants,
   ask the user to choose the target before editing.
8. Don't invent `variantInternalId` or `formatInternalId`. Here,
   `variantInternalId` means the campaign's A/B variant, not the JSX attribute `themeVariant`,
   which refers to the node's letter-styles variant.

### 2. Reading the initial state

1. Call `visual_template_get(formatInternalId)` for each target format —
   `Mindboxeditor` or `Rawhtml` with `html: no`. Each format has its own JSX snapshot and
   `visualTemplateRowVersion`; don't carry the version of one over to another. The draft may not
   have a visual template yet — then the bootstrap branch from item 3 applies to it, and the
   ordinary one to Active.
2. If the tool returns JSX and `visualTemplateRowVersion`, this is an existing visual
   template. For `Mindboxeditor + html: yes`, save the exact JSX as a snapshot. For
   `html: no`, regardless of editor kind, first perform attachment recovery: after
   confirmation, save exactly this JSX with the current `mailingRowVersion` and
   `visualTemplateRowVersion`, then verify the attachment as the first bootstrap save.
   Don't change the JSX and don't create a new version before recovery succeeds.
2a. An existing visual template, and the task is to build a new email (a mockup, a description, a prompt):
    before generating, ask what to do with what's already in the format — build a new one as a replacement
    or edit the existing one. A replacement is a different email, not an edit, and the user decides that.
    Pass the answer to the generator together with the JSX snapshot.
    The gate is tied to the intent, not to this step: "let's start over", "redo everything", "from scratch"
    in the middle of edits is the same replacement, and 2a–2b are walked through again, no matter how many
    iterations have already passed. The snapshot and the styles are re-read anew at that point
    (`visual_template_get`, `visual_template_theme_get`): they may have been changed over the iterations,
    including by your own saves.
2b. Replacement chosen — call `visual_template_theme_get(formatInternalId, jsx)` and see whether the
    email has its own letter styles or the platform ones. Its own — a second question is **mandatory**, and
    it has three answers: build the new content **in these styles** (headings and buttons take their look
    from them and later change together with the whole email), **give the email new ones**, or **reset to
    the platform ones**. Platform ones already — don't ask.
    A full rewrite of the template doesn't erase the styles: they belong to the format and carry over on
    save. That's why both "new" and "reset" mean an explicit `<Theme>` in the new document, not the
    absence of the tag; without it the new email inherits the previous look. The values for a reset come
    from the same tool called **without both arguments** — that's the only way to get the platform
    ones. And say it plainly: there's no full "as if nobody had configured anything" from the markup — the
    email will look unconfigured, but its styles will remain its own, just equal to the platform ones.
    Pass all the answers to the generator.
3. If the tool literally reports `No visual template was saved for format '…' yet`,
   check the original `campaign_get`:
    - the chosen format has `html: no` and the editor kind is `Mindboxeditor` or
      `Rawhtml` — this is a bootstrap of a new visual template: record the absence of a
      stored JSX, the snapshot, and `visualTemplateRowVersion`; the first save happens
      after explicit confirmation with preview status and without
      `visualTemplateRowVersion`;
   - the format already has a body (`html: yes`), or its emptiness isn't confirmed — don't treat
     this as a bootstrap and don't overwrite the format: it may contain raw HTML.
4. If `visual_template_get` reports that the existing template can't be expressed in JSX,
   don't continue editing blindly and don't overwrite it: suggest the UI. JSX
   separately supplied by the user can be edited/shown via the route below, but
   it may be saved only to a confirmed, compatible visual target under the usual gates.

### 3. Editing, freshness, and optional preview/QA

1. The Generator makes only the requested changes.
2. Any JSX change makes previous preview/HTML/PNG links stale. Tell this to the
   user and offer a new preview or full QA, but don't call preview
   automatically.
3. A request to redo the email from scratch in the middle of edits is a replacement, not an edit: go back to §2
   items 2a–2b, re-read the snapshot and the styles, and ask both questions again. Silently starting a new
   email on top of the work done is not allowed, no matter how many iterations have already passed.
4. If the user asks for preview/QA/debug, `visual_template_preview` renders the
   current JSX **with the target format's `formatInternalId`**; return editor/preview errors to the
   generator verbatim; silent repair is forbidden.
5. If the generator needs the current values of the letter styles — to take a node off
   them or to write a set into `<Theme>` — call
   `visual_template_theme_get(formatInternalId, jsx)`. **Pass the current JSX**: without it the
   response won't account for the document's not-yet-saved `<Theme>`, and replacing that tag with the
   response will erase the edits. The response is a ready-made fragment; hand it to the generator as is.
   If there is no email yet — call it without both arguments and the platform values come back; the tool
   says so outright, and you must not relay them to the user as the styling of their email.
6. A request to change the look of nodes that go under the letter styles — the number first.
   Count from the document how many more elements an edit of the letter styles would affect: a node under
   them writes no styles of its own, so they're visible. Name the number and ask whether to edit the letter
   styles or take the named nodes off them. Without the number the user has nothing to decide with.
7. For QA/debug, download HTML if an HTML check is needed, and/or get PNG links
   via MCP per the rules in the "Verification, preview, and QA" section. For an ordinary edit
   without QA, no download is performed.

The state of the letter styles needs to be known only when the document actually names a look (see
§4). It can be learned without an extra call:

- the format isn't named or doesn't exist yet — the styles are the platform ones, that follows from the fact itself;
- `visual_template_get` literally answered `No visual template was saved for format '…' yet` — the same:
  there was nothing to save, so the styles are the platform ones;
- the format has an email — then this is already branch 2a–2b, where `visual_template_theme_get` is called
  for another reason; no separate call is needed.

Don't call the tool for this one question alone: its response is the full set of styles, it's large, and
pulling it into the context for nothing is expensive.

### 4. Confirmation

Before `visual_template_save`, you need one explicit user confirmation. It must
show the preview's freshness status: fresh, stale after the last
edit, or never opened. If there's no fresh preview, the confirmation must explicitly
allow saving without a new preview:

```text
- campaign: <name and internalId if needed>
- A/B variant: <human-readable description, show only if the campaign has several variants>
- formats: Active — or "Draft and Active" in write order, if the variant has a draft
- change: short description
- preview: fresh / stale after last edit / never opened
- letter styles: the line is mandatory in **every** confirmation and is read straight from the document, not
  from memory of the questions asked — three mutually exclusive cases:
  - the document has a `<Theme>` → "this document sets the email's letter styles";
  - no `<Theme>`, and the nodes name their own look → "the email is saved with its own styles on each
    element";
  - no `<Theme>` and the nodes don't name a look → "the email's letter styles stay as they are, the nodes go
    under them".

  No line — the confirmation is incomplete. Separately from the line: if by the conditions of step 7 of
  `maestra-email/SKILL.md` the offer to move the nodes' look into the letter styles is due, and it hasn't
  been made in this conversation — ask it right here, together with the other save parameters: "Save this
  email's styles as its letter styles? Then headings and buttons can later be changed across the whole
  email at once". One conversation — one such question: the answer holds until its end, and neither a
  second save nor edits re-arm it
- existing email: only if the format already had a visual template and replacement was chosen —
  "the email in the format is replaced entirely"
- style transfer: only if the edit moves the nodes' styles into the email's letter styles — "the styles move
  into the letter styles, the look doesn't change; from then on they can be edited across the whole email at once"
- draft line: only if the variant has a Draft format — "This campaign has a draft started in the
  editor; the edit will save into it first, then into the active
  version"
```

If the target is ambiguous, the target-selection question is asked earlier and separately from
the write confirmation.

### 5. Save

1. Call `visual_template_save` for one chosen `formatInternalId`.
2. One save — one `formatInternalId`; there's no batch write. If there are two targets, there are two
   calls as well, with the same JSX: **Draft first, then Active**. The order isn't cosmetic —
   what doesn't go out to customers goes first.
3. For an existing visual template, pass the versions from discovery:
   `mailingRowVersion` and `visualTemplateRowVersion`. The second call gets the
   `mailingRowVersion` **from the first call's response** — the campaign is one, and its version has grown —
   while `visualTemplateRowVersion` is taken from the format you're writing to: each has its own.
   If the first save (Draft) was refused — don't write to Active: stop, show the refusal, and
   ask what to do. If the second was refused, don't rewrite the first and don't roll it back:
   tell the user which format was updated and which stayed as it was, and why.
4. Only for the confirmed bootstrap branch from step 2, pass
   `mailingRowVersion` and omit `visualTemplateRowVersion`.
5. From a successful response, save the new `mailingRowVersion`, `visualTemplateRowVersion`,
   state, and validation errors. Use these versions for subsequent
   `campaign_edit`, `campaign_edit_content`, and a repeat save.
6. After the first bootstrap save, you must independently re-read `campaign_get` and
   find the same `formatInternalId` the save was performed into, with its original
   Active or Draft status. Success is confirmed only if the format has become
   `Mindboxeditor` and `html: yes`. If it remains `Rawhtml`, `html: no`, has disappeared, or
   the response doesn't let you confirm both facts, don't say "saved" and don't repeat
   the same save automatically: tell the user the visual template didn't attach to the email.
   The only way forward is attachment recovery per item 8, after `visual_template_get` and
   a new confirmation.
7. The transfer of styles into the letter styles goes in **one** save: `<Theme>`, the nodes whose styles
   were taken off, and `themeVariant` — one document. Don't save the theme separately from the nodes:
   between two saves the email would be left without a look.
8. If save explicitly reports that the visual template was saved but the campaign was not, save
   the returned `visualTemplateRowVersion`: don't create a new template and don't repeat
   the save without this version. After a fresh `campaign_get`, attachment recovery uses
   exactly this same JSX and the version obtained.

### 6. Post-operation report

1. Briefly report the campaign, format, and result. If there were two targets, name both and
   the result for each.
2. Split validation errors into those pre-existing at the time of the original `campaign_get`
   and those introduced/changed by the current edit.
2b. Distinguish `visual template stored` from `campaign updated/attached`. A response with
    `The template itself WAS stored — only the campaign was not` is a partial persist,
    not a success: don't say "saved"; further actions — per §5 item 8.
3. Don't make a repeat `campaign_get` mandatory after every ordinary successful save:
   the save response is the primary result. Re-read `campaign_get` and, if needed,
   `visual_template_get`, only if the save response is incomplete, the version is lost, a
   subsequent operation is needed, or independent verification is needed. The first bootstrap save is an exception:
   it always goes through independent verification per step 5.

### 7. `ChangeConflict`

`ChangeConflict` is a concurrency event, not a way to find out the current version.

On conflict:

1. Re-read `campaign_get`.
2. Re-read `visual_template_get`.
3. Compare the freshly stored JSX with the original snapshot from step 2, not with the edited JSX.

If the fresh JSX matches the snapshot, the template body hasn't changed since it was read, and the
conflict relates to a different campaign/metadata version. **There is no automatic retry
here either:** say that the campaign was changed concurrently, name exactly what diverged, and
ask whether to apply the edit on top. Only after an explicit "yes" is one retry of the same JSX
with fresh versions allowed; a repeat preview isn't needed if the JSX hasn't
changed. A second `ChangeConflict` — stop and tell the user.

If the fresh JSX doesn't match the snapshot, the template was changed concurrently. It is forbidden to
blindly repeat the save, overwrite the fresh JSX with the old edit, or automatically
merge. Stop and say:

> The template changed after it was read. The save was stopped to avoid overwriting someone else's edit.

If the user wants to continue: fresh JSX → reapply the requested
change → tell them the previous preview is stale → optional preview/QA on request →
confirmation → save.

In the bootstrap branch, before the first successful save, there's no snapshot. On
`ChangeConflict`, don't apply the usual snapshot comparison and don't repeat the save
automatically:

1. First re-read only `campaign_get` and find the same `formatInternalId` the save
   was performed into.
2. Continue the bootstrap check only if this format still explicitly
   has `html: no`, and the editor kind is `Mindboxeditor` or `Rawhtml`. On `html: yes`,
   an unknown editor kind, or a target that disappeared/changed, stop and go to
   `visual_template_get`, as with a concurrent edit.
3. Only after that, call `visual_template_get`. If a visual template has appeared,
   don't repeat the bootstrap without a version: proceed to attachment recovery with the found JSX
   and `visualTemplateRowVersion`.
4. If the visual template is still absent and the same empty target is confirmed,
   show the user the unchanged target and request a new explicit confirmation.
5. After confirmation, exactly one bootstrap retry is allowed, with a fresh
   `mailingRowVersion` and without `visualTemplateRowVersion`. A repeat preview isn't needed
   only if the JSX hasn't changed since the previous save attempt; preview doesn't
   need to run unless the user has themselves asked to refresh the preview.
6. If the bootstrap retry again returns `ChangeConflict`, stop; there are no further
   automatic attempts.

## Routes

### New email

If the email is being saved into a campaign: `campaign_get` → choose target →
`visual_template_get`/bootstrap discovery → if the format already has an email, the question about
replacement and about its letter styles (§2 items 2a–2b) → the Generator determines the needed images
→ Ops finds existing assets or uploads attached/local files via MCP and
returns links → the Generator creates JSX → Ops reports that the previous preview
is stale/never opened, and offers a new preview or a full HTML/PNG QA via MCP →
the Generator adjusts the JSX if needed → the canonical visual workflow saves the
email after confirmation with preview status. Images are still
resolved before JSX generation, but attached/local upload isn't performed before the target is verified.

### Editing an existing email by ID

`campaign_get` → check `kind`/`state`/`transactional` → choose
`variantInternalId` + the target formats (Draft, if there is one, and Active) →
`visual_template_get` → canonical visual workflow. If the template can't be expressed in JSX,
stop and suggest the UI; if the email is raw HTML and a visual one is requested — the "Changing the
template type" section. There is no longer a workaround conversion from serialized JSON.

### Changing the template type

"Redo it in the visual editor", "convert it to HTML" — the template type belongs to the format and
can't be changed via MCP: there's no tool, `visual_template_save` into `Rawhtml` with `html: yes` is forbidden,
`htmlBody` can only do the reverse. The formats of one campaign are of one type, so looking inside
it for a format for the other route is pointless. The refusal is known in advance, so trying tools one
after another, saving "on a trial basis", and retrying after a refusal are forbidden.

The only path is a new campaign in which the same email is built straight away with the needed
editor; the original stays untouched. Offer it and wait for explicit consent; without it
nothing is created. After consent: `campaign_create` per the "New campaign from scratch" section with
the same `mailingKind`, carry over subject/sender/preheader via `campaign_edit_content`,
name/UTM via `campaign_edit`, then the canonical visual workflow. Take the email's source
from `campaign_get` with `includeBodyForVariants`; don't reconstruct it from memory. Say in advance that
recipients, segment, subscription, and schedule aren't copied, and that table layouts and non-standard
HTML don't port one-to-one into editor blocks.

### Hero/subject clarification

- "header," hero, heading, or content inside the email — visual JSX workflow;
- "email subject" / subject — `campaign_edit_content`, no JSX;
- "styling", "design", "letter styles", "the style of all buttons/headings" — this is **not** the
  subject but the email's letter styles: `visual_template_theme_get` and the `<Theme>` tag in the JSX.

### Editing supplied JSX

Ops accepts the input → the Generator makes only the requested changes → Ops marks
the previous preview stale and runs preview/QA only on user request
or for diagnostics → the user confirms → Ops saves if there's a target mailing.
Existing personalization, the unsubscribe token, Html, and other round-trip-sensitive
values aren't changed without a request from the user.

## `campaign_edit`, `campaign_edit_content`, `campaign_create`

For `campaign_edit` and `campaign_edit_content`, no preview is performed. An explicit request
from the user naming a specific campaign and exact new values counts as
confirmation for an ordinary metadata edit. Show the exact diff and request a separate
confirmation if the target/value was inferred by the agent, the plan changed, or
only part of the request is being fulfilled. Always confirm changes to the schedule, transactional/restriction flags, and
overriding restrictions separately before calling.

### Campaign version chain

`rowVersion` in `campaign_get`/`campaign_edit`/`campaign_edit_content` and
`mailingRowVersion` in `visual_template_save` are the same optimistic-locking token
for the campaign; don't confuse it with the separate `visualTemplateRowVersion`.

1. Start with `currentMailingRowVersion = campaign_get.rowVersion`.
2. Every `campaign_edit` or `campaign_edit_content` receives the current token and, on
   success, returns a new `rowVersion`; immediately replace
   `currentMailingRowVersion` with it.
3. The next write operation receives only the updated token. Don't reuse the old version after
   a successful edit/save.
4. `visual_template_save` receives this token as `mailingRowVersion`, and its
   successful response again replaces `currentMailingRowVersion`.
5. If the token is lost, the response was incomplete, or there's any doubt, re-read
   `campaign_get` before the next write operation.

### New campaign from scratch

If the user wants to create and prepare a campaign with no existing mailingId,
follow a single route:

1. Ask the user for **the folder and brand in words, not identifiers**, and the timezone. Find the
   actual values for `campaign_create` yourself: `entities_list(entityType: "Folder")` returns the
   folder's `internalId` and its brands, `entities_list(entityType: "Brand")` — the brand's system name
   (in this tool the brand is set by that, not by a GUID). Nothing found, or several candidates —
   show the user what was found and let them choose, but don't ask them to dictate a GUID. To prepare for
   sending, gather confirmed `name`, subject/sender/reply-to/preheader, UTM,
   schedule/timezone/rate, and restriction flags. Don't invent values.

   **`mailingKind` is a decision, not an optional field.** By default the tool
   creates `Manual`, and **after creation the campaign kind can't be changed**: `campaign_edit`
   doesn't accept it, and it can only be fixed with a new campaign. Determine the kind from what
   the user described:

   - **`Automatic`** — the email is sent by a flow in response to an event: abandoned
     cart, viewed products, welcome, order status, reactivation, birthday,
     any "when a customer …". Such an email has access to the event's data —
     the order, the cart, the views.
   - **`Manual`** — a one-off send to a segment that a person launches from the
     interface: a promotion, an announcement, a digest.

   Don't guess by default: if the kind can't be read unambiguously from the request, ask
   in one question before creating. The content depends on the kind — see below.
2. `campaign_create` → immediately `campaign_get`; from then on, track `currentMailingRowVersion`.
3. `campaign_edit_content` — subject/sender/reply-to/preheader;
   `campaign_edit` — name/UTM/schedule/timezone/rate/restrictions. After each
   write, update rowVersion per the chain above.
4. Email body: the Generator creates JSX → canonical visual workflow/bootstrap below →
   optional preview/QA → confirmed `visual_template_save`.
5. Recipients, segment/filter, topic/subscription, and live send/activate/delete are not
   configured via MCP: at the end, explicitly say this needs to be done in the UI. Offer a test
   send of the finished email per the "Test send" section.

**The campaign kind restricts the email's content.** In `Manual` there is no event that can be
read, so the following are meaningless in it:

- personalization parameters marked *(automated only)* — they read the order;
- product rows on mechanics that look at the customer's action — cart,
  viewed products, order products. Recommendations and product lists work in
  both: they don't depend on the event.

If the email the user asks for relies on such data, the kind must be
`Automatic` — say so before creating, not after the email has been built in `Manual`.

### `campaign_edit`

Use for campaign settings: name, UTM, schedule, rate limit, timezone, and
sending restrictions. Always pass a fresh `mailingRowVersion`: from a fresh
`campaign_get` or from the last successful save/edit. If the version is lost or
in doubt, re-read `campaign_get`. UTM, schedule, and rate are supported by the tool's
contract; only the name change is considered live-verified.

### `campaign_edit_content`

Use for subject, senderName/senderEmail, replyToName/replyToEmail, preheader,
and raw HTML — only on an explicit request for raw HTML. A fresh `mailingRowVersion` is
required before the call. v1 supports only a single-variant email campaign: if
`campaign_get` returned several A/B variants, stop and report the limitation.
Don't ask the user to choose `variantInternalId` — `campaign_edit_content` doesn't accept it,
and making that choice won't make the call valid; direct the user to the UI or another
confirmed route. Subject/preheader can be set to non-empty values;
don't clear subject/preheader to empty/null via the current MCP — report the
limitation and direct them to the UI. Nullable behavior and `preHeaderPresentationMode`
aren't covered by the current contract — don't use them.

`htmlBody` is not a fallback for `visual_template_save`; switching to raw HTML
is allowed only on an explicit request from the user.

### `campaign_create`

1. Call `campaign_create` only after the user has explicitly chosen folder/brand/timezone;
   don't invent values.
2. After creation, you must call `campaign_get(new internalId)` and discover
   the variants/formats.
3. An empty format (`html: no`) can exist before the visual template is initialized,
   and allows bootstrap when the editor kind is `Mindboxeditor` or `Rawhtml`.
4. For the empty format found, call `visual_template_get`. The response
   `No visual template was saved for format '…' yet` together with `html: no` enables the
   bootstrap branch of the canonical workflow: new JSX → stale-preview notice →
   optional preview/HTML/PNG QA on request → confirmation with preview status
   → first `visual_template_save` without `visualTemplateRowVersion`.
5. If no format is found, don't invent an ID and don't save "on a trial basis"; report that
   format initialization is required in the UI, or use another confirmed route.
6. Don't overwrite `Rawhtml` with `html: yes` with a visual save. Handle `Rawhtml` with `html: no`
   as bootstrap/recovery based on the `visual_template_get` result.

## Test send

A test email is a real send to staff test recipients, not a preview.
What goes out is the published (Active) content of the chosen variant.

1. Call `campaign_test_recipients`: it returns the staff account's test
   recipients — `recipientId`, name, email, and phone, with the platform's verdict on
   the validity of each contact.
2. Show the list to the user by names and contacts, never by id, and wait for
   an explicit choice of recipients and consent to send. Don't choose recipients silently,
   even if there's only one candidate.
3. Call `campaign_send_test` with `campaignInternalId` and `variantInternalId` from
   `campaign_get`, a fresh `rowVersion` per the campaign version chain, and `recipientIds`
   only from a fresh `campaign_test_recipients` response — never a customer id and
   never an email. If there are several A/B variants, the user chooses the variant.
4. Report the result by contacts, not by id.
5. If the backend answered `is not ready for test sending` — the variant is incomplete
   (subject/sender/content/DKIM): return the error verbatim and don't retry.
6. On a timeout or no response, don't repeat the call: the send may already have
   happened. Tell the user; a retry — only on their explicit request.

## Safety boundaries

1. Don't invent `mailingInternalId`, `variantInternalId`, or `formatInternalId`.
2. Don't silently choose an ambiguous A/B variant. The visual-write targets are all formats of the variant for which the visual workflow is allowed: Draft first, if there is one, then Active, with the same JSX and two calls.
3. The skill doesn't edit an active automatic campaign (`kind: Automatic`, `state` not `InDevelopment`) or a transactional one — preview only; editing is done in the editor.
4. Preview doesn't run automatically after every edit and isn't a
   mandatory gate on save. Before saving, the user must see the preview's
   status; if it's stale or was never opened, the confirmation must explicitly allow
   saving without a new preview, or must first trigger preview/QA.
5. One save — one `formatInternalId`; there's no batch write.
6. Before `visual_template_save` — one explicit confirmation with preview status;
   for `campaign_edit` and `campaign_edit_content`, the separate metadata policy
   from the corresponding section applies.
7. On `ChangeConflict`, the freshly stored JSX is compared with the original snapshot, not the edited JSX; there is no automatic retry: the agent names the divergence and asks the user whether to apply the edit on top, and only after explicit consent makes one attempt. In the bootstrap branch, a retry is allowed only after re-confirming the same `formatInternalId` the save was performed into, with `html: no` and editor kind `Mindboxeditor` or `Rawhtml`, a `visual_template_get` result, and new user consent; a repeat conflict always stops the workflow.
8. `htmlBody` is not a fallback for the visual save; switching to raw HTML is allowed only on an explicit request from the user.
9. Don't clear subject/preheader to empty/null via MCP — nullable behavior isn't covered by the contract; report the limitation and direct the user to the UI.
10. Live send/activate/delete and recipient edits via MCP are not available — UI only. A test send (`campaign_send_test`) — only to `recipientId`s from a fresh `campaign_test_recipients`, after the user has explicitly chosen the recipients and consented to the send; on a timeout the call isn't repeated.
11. Preview/save/editor errors are returned verbatim; silent repair is forbidden.
12. Validation errors are split into pre-existing ones and ones introduced by the current edit.
13. For images, use only the user's external HTTPS URL, the `url` from `gallery_images_list`, or `fileUrl` after a successful MCP upload; don't assemble URLs by hand.
14. A format's template type can't be changed via MCP: there is no workaround, and retrying a refused save or `htmlBody` isn't one. The route is the "Changing the template type" section: a visual format of the same campaign, otherwise a new campaign after the user's consent.
15. Anything that isn't in the MCP tools (activation, live send, deletion, format creation, changing the template type, recipients and segment) the agent doesn't do on the user's behalf: neither in the editor nor through browser automation. The browser is allowed read-only — preview and the contact sheet. If you run into such an action — name it, say where the user can do it, and stop.
16. `Rawhtml/html:yes` is never a target for the visual save. `Rawhtml/html:no`
    allows bootstrap/recovery based on the `visual_template_get` result; success of the first
    save is confirmed by a fresh `campaign_get`: the `formatInternalId` that was written to,
    with its original status, `Mindboxeditor`, and `html: yes`.

## References

| Situation / signal | File | What's there |
|---|---|---|
| Composing the MCP `feedback` text and it's unclear how to write `problem`/`context` | `references/feedback-examples.md` | Examples of user-report and agent-observation from real runs + anti-examples |
| The user asks to visually view/select images from the gallery | `references/visual-gallery-selection.md` | Full Codex/Cowork contact sheet procedure, Pillow, card template, result format |
| HTML download, PNG, mobile/desktop, QA/debug, rendering diagnosis, or fallback (simple preview stays in core) | `references/preview-qa.md` | Extended QA procedure: HTML download, MCP PNG links, complaint diagnosis, retries, and fallback |
