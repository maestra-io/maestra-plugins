# Inbox mockup: before/after

**When to read this:** the user said yes to the inbox-mockup offer from §6 "Post-operation
report", or asks on their own for a picture of an email as it looks in an inbox, a "screenshot"
for the client, or a before/after comparison.
**Return to:** the user, with the images; nothing is saved to Maestra in this procedure.

The mockup is a presentation picture. It is not QA and it does not replace the preview: QA
still goes through `visual_template_preview` and its snapshots (`references/preview-qa.md`).
What the mockup adds is the look of a received email: the backend render at phone width under
a mail-app header, realistic sample values instead of the editor's placeholders, and, with an
earlier version, the two versions side by side.

## 1. Pick the versions

| Situation | "After" | "Before" |
|---|---|---|
| The email was edited in place | the saved JSX, its format | the §2 snapshot JSX — the one read before the edit — same format |
| The email was rebuilt as a copy or in a new campaign | the new campaign's format | the source campaign: `campaign_get` → `visual_template_get` of its format |
| A brand-new email | the new format | none — one mockup, no comparison |
| The earlier version is raw HTML (`Rawhtml`, `html: yes`) | the new format | none: it has no visual render; make the single mockup and say why |

The snapshot is only rendered, never written back. If the user did not keep the conversation
where the snapshot was read and the email was overwritten, there is no "before" left: say so
and make the single mockup.

## 2. Render each version

One `visual_template_preview(jsx, formatInternalId)` call per version, each with **its own**
format. Take `htmlUrl` from each response, and keep the mobile snapshot link too — it is the
fallback input. Each call opens a new preview widget in hosts that have them; that is expected
here, the user asked for the pictures.

The links are temporary: render and run the script in one go, don't park them for later.

If this edit wrote a `<Theme>` into the format, the "before" rendered under the same format
picks up the new letter styles. Say so when handing the pictures over.

## 3. Choose the sample values and the header

1. List what the editor substituted:

   ```bash
   python3 <skill>/scripts/inbox_mockup.py --before "<before htmlUrl>" --after "<after htmlUrl>" --list-chips
   ```

   It prints the sample value of every personalization chip per version, for example
   `Hello Name!`, `330770`, `sample@mail.com`.
2. Pick a replacement for each, without asking the user — then name the values in the
   hand-over:
   - a neutral invented first name, written into the greeting the way the email words it
     (`Hello Name!` → `Hello, Sarah!`);
   - an invented order number of the same length, a code in the same shape, a date in the
     email's format;
   - `name@example.com` for an address.

   Never a real customer's data. The same values in both versions, so the comparison is fair.
3. The header:
   - `--sender` — `senderName` from `campaign_get`;
   - `--subject` — the subject **as the recipient sees it**: resolve its personalization by
     hand with the sample name, for example
     `@{if not IsEmpty(recipient.firstname)}${Recipient.FirstName}, T@{else}T@{end if}hank You`
     → `Sarah, Thank You`. If the two versions have different subjects, run the script once
     per version with its own subject and build the side-by-side with the fallback mode from
     the two PNGs;
   - `--to` — the sample first name;
   - `--accent` — the brand's main color as the email uses it (the avatar and the AFTER label).

Links in the canvas render are `#`; in a picture that does not matter.

## 4. Run the script

```bash
python3 <skill>/scripts/inbox_mockup.py \
  --before "<before htmlUrl>" --after "<after htmlUrl>" \
  --sender "<senderName>" --subject "<subject as seen>" --to "Sarah" \
  --replace "Hello Name!=Hello, Sarah!" --replace "330770=481527" \
  --replace "sample@mail.com=sarah@example.com" \
  --accent "#RRGGBB" --out-dir "<output folder>" --prefix "<campaign-slug>"
```

Without `--before` it renders the single mockup. Output: `<prefix>-after.png`,
`<prefix>-before.png`, `<prefix>-before-after.png` (phone width 390 px at 2x).

Dependencies: Python 3; Playwright with a Chromium it can launch (Cowork has both); Pillow for
the side-by-side image. The script installs nothing. Install Pillow from PyPI if it is missing,
as for the gallery contact sheet; don't download browsers.

**Exit code 3** — Playwright or Chromium is not available. Fall back to the preview's mobile
snapshots:

```bash
python3 <skill>/scripts/inbox_mockup.py --before-png "<before mobile snapshot>" \
  --after-png "<after mobile snapshot>" --out-dir "<output folder>" --prefix "<campaign-slug>"
```

This gives the side-by-side image only, without the mail-app header, and the editor's sample
values and chip outlines stay visible. Say so in the hand-over.

## 5. Check and hand over

Look at every image before sending it: no chip left with an editor placeholder (`Name`, a
dashed outline), no `[email protected]`, no broken image, the header not cut. A leftover
placeholder means a `--replace` pair is missing: run `--list-chips` again.

Hand over with the host's file-delivery tool, the side-by-side image first. In one or two lines:

- it is a mockup built from the platform's render, with invented sample values (name them);
- long images get compressed by messengers when sent as a photo — send them as a file;
- the letter-styles caveat from step 2, if it applies.

Don't relay `containerWidth`, don't present the sample values as customer data, and don't send
the pictures anywhere yourself.
