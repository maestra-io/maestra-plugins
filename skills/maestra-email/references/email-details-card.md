# Email details card

**When to read this:** you are about to build a new email (step 0 of the Workflow in `SKILL.md`):
from a description, a mockup or a reference, a rebuild or redesign of an existing email, a copy
into a new campaign, a port from another platform.
**Return to:** step 1 of the Workflow, with the answers.

One card with every question the build needs, shown before anything is created or generated.
It replaces a string of questions in the chat and the silent guesses the user only finds out
about after the save.

## 1. Before the card: find out what you can

The card asks only what cannot be read from the request, the project or the reference. So first:

- the project (tenant) — unambiguous from the conversation, or `tenants_list`;
- the target, if the user named one: `campaign_get` → its folder, brand, kind, formats;
- folders and brands for a new campaign: `entities_list(entityType: "Folder")` — the card offers
  real folders, not invented ones;
- the reference (a link, a screenshot, an older email, a brand book): colors, blocks, images;
- tenant catalogues the email will need: product lists, recommendation mechanics, promo code
  pools, order identifiers (`entities_list`).

What you found goes into the card as the preselected option or into the subtitle of an option,
never into a question. If everything is known, there is no card: write one line with what you
decided ("Saving into a new campaign in *Transactional emails*, automatic, order number only")
and build.

## 2. What to ask — 2 to 5 questions, in this order, only the ones that are open

| Question | Ask when | Options |
|---|---|---|
| Where to save it? | no target named | new campaign (folder + brand from the lookup in the subtitle) · an existing campaign (by link or ID, "Other" field) · don't save, preview only |
| Which time zone? | a new campaign | the time zone of the brand's recent campaigns (from `campaign_get`) preselected · "Other" field for an IANA name |
| Automatic or manual? | the kind is not obvious from the request **and** it changes the content (order data, cart, viewed products) | automatic (flow, live data) · manual (to a segment, placeholders) — say in the subtitle what each gives |
| Which data to show? | personalization or order/product data is in play | multi-select of the concrete values: first name, order number, date, total, order items, promo code… |
| How many products, which layout? | the email has a product row | 6 (3×2) · 3 (3×1) · 4 (2×2) |
| Which images from the reference? | the reference has images beyond the logo and icons | one card per image with its subject and offer in the subtitle; multi-select |
| Where to take the look from? | the look is not given — no mockup, reference, brand book or earlier email in the request or the project notes | cards: the last 3 one-off (bulk) emails of this brand · the last 3 flow emails · design from the website (URL field, the brand's site prefilled when known) · the client's brand book (file upload with a text fallback) — multi-select |
| Style / blocks | a redesign, or the description leaves the look open | preview tiles for the layout; cards for optional blocks |

Don't ask about subject, sender or copy tone unless the user raised them: Claude proposes them
and the user edits after. Don't ask for identifiers — the card shows names.

## 3. How to show it

**Host with the visualization tool** (`show_widget` and its `read_me`; claude.ai, Claude desktop,
Cowork): the card is mandatory. Load the tool's `elicitation` module with `read_me` first, then
render with `show_widget` using the skeleton below. Follow the module's rules: header icon
byte-for-byte, `data-value` on every option, no `<script>`, sentence case, choice formats varied
(cards for options with a subtitle, preview tiles for layouts, plain pills for short labels).

**Host without it, but with a native choice tool** (`AskUserQuestion` and the like): the same
questions, same order, same preselected defaults, in one call.

**Neither** (Claude Code, Codex, a CLI): one message with numbered questions and lettered options,
the default marked; the user answers like "1a 2b 3 — order number and date".

The title is "Email details" in the user's language ("Детали письма"). Questions are phrased as
questions from you. The footer buttons are Skip / Continue in the user's language.

```html
<h2 class="sr-only">Questions before building the email</h2>
<form class="elicit">
  <div class="elicit-header">
    <!-- the File icon SVG from the elicitation module, byte-for-byte -->
    <span>Email details</span>
  </div>
  <div class="elicit-body">
    <div class="elicit-group">
      <label class="elicit-question">Where should I save the email on <project>?</label>
      <div class="elicit-pills" data-name="target" data-multi="false">
        <button type="button" class="elicit-pill" data-value="New campaign: <folder>, <brand>"
          style="border-radius:12px; padding:14px 16px; display:flex; gap:12px; align-items:flex-start; text-align:left; min-width:200px; box-shadow:0 1px 2px rgba(0,0,0,0.04)">
          <i class="ti ti-mail-plus" style="font-size:20px" aria-hidden="true"></i>
          <span><span style="font-size:13px; font-weight:500">New campaign</span><br>
          <span style="font-size:11px; color:var(--text-muted)"><folder>, brand <brand></span></span>
        </button>
        <button type="button" class="elicit-pill" data-value="Existing campaign" data-other
          style="border-radius:12px; padding:14px 16px; display:flex; gap:12px; align-items:flex-start; text-align:left; min-width:200px; box-shadow:0 1px 2px rgba(0,0,0,0.04)">
          <i class="ti ti-folder" style="font-size:20px" aria-hidden="true"></i>
          <span><span style="font-size:13px; font-weight:500">Existing campaign</span><br>
          <span style="font-size:11px; color:var(--text-muted)">By link or ID</span></span>
        </button>
      </div>
      <input type="text" class="elicit-other" data-for="target" placeholder="Campaign link or ID" hidden>
    </div>
    <!-- further .elicit-group blocks: kind, data, product layout, images, style -->
  </div>
  <div class="elicit-footer">
    <button type="button" class="elicit-skip">Skip</button>
    <button type="button" class="elicit-submit">Continue</button>
  </div>
</form>
```

Preselect the default you would choose anyway with `aria-pressed="true"` on that option, so
"Continue" without clicks is a valid answer.

The look-source question takes the brand book as a file: put the module's file-upload group
(dropzone + textarea fallback) inside that group, under the cards, so the user can drop the PDF
right there; preselect "the last 3 one-off emails" when the brand has sent any.

## 4. After the answer

**The look source, when it was asked.** Collect the look before generating, then say it in one
line (colors, fonts, block order, button shape) and build with native blocks — never by copying
the source's HTML.

- *The last 3 one-off emails* — `entities_list(entityType: "Mailing")` with the filter
  `{"brandInternalIds": [<brand>], "states": ["Completed"]}`, page through, keep `channel` Email
  and `mailingKind` Manual. The listing has no dates: rank by the sending date from `campaign_get`
  (names often carry a date — use it to narrow first). For the 3 newest: `campaign_get` →
  `visual_template_get` of the active format (raw HTML — `campaign_get` with
  `includeBodyForVariants`), and the preview snapshots if you need to see them.
- *The last 3 flow emails* — the same with `mailingKind` Automatic and running states (states
  are listed by the tool when a wrong one is sent); take the 3 most recently changed.
- *The website* — open it (web fetch, or the browser where the host has one): logo, palette,
  fonts, button style, tone; take the logo from the gallery or upload it per `maestra-email-ops`.
- *The brand book* — read the attached file (or the pasted text): palette, typography, logo
  rules, voice. If several sources were chosen, the brand book wins over emails, emails over the
  site.

Nothing found (no sent emails, the site does not open) — say so and fall back to the next
chosen source, then to the platform defaults.

- The answers come back as one line ("Email details — Target: … · Data: …"). Read them, say in
  one line what you are building, and continue with step 1. Don't ask the same things again.
- **Skip** — build with the preselected defaults and name them in one line.
- A value the user typed into an "Other" field that needs a lookup (a campaign link, a pool
  name) — resolve it before the build; if it does not resolve, ask about that one value only.
- The card is not consent to write. Saving still waits for the confirmation in
  `maestra-email-ops` §4, and creating a campaign follows "New campaign from scratch" there.
