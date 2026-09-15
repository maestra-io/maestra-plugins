# CHANGELOG

## 1.1.0 — 2026-09-15

`maestra-email` + `maestra-email-ops` synced with the upstream visual-editor skills, version 1.11.0
(both skills now carry `metadata.version: 1.11.0`). The generator and the ops skill were re-ported in
full rather than patched, so the two stay diffable against the next upstream release.

New in the generator (`maestra-email`):

- Personalization with the `<Var>` chip: recipient, promo code, bonus balance, custom fields, order
  data; tenant-specific names come only from `entities_list`. New references
  `personalization.md`, `personalization-parameters.md` (43 email parameters) and
  `product-parameters.md` (125 product parameters by entity).
- Product rows `<CollectionRow>` / `<CardTemplate>` / `<CollectionCard>`: recommendations, product
  lists, order products, viewed products, manual selections — new reference `product-rows.md`.
- Letter styles: `<Theme>`, `themeVariant`, taking a node off the letter styles, moving repeated
  node styles into the theme (`dsl-surface.md` §8).
- `<Label>` / `<Labels>` inside product cards, dynamic images (`image.mode: "dynamic"`), saved
  blocks from the editor library, `Template.containerWidth` / `background`, element defaults
  (`dsl-surface.md` §6), pixel → grid and port-completeness self-checks.
- Rule changes: the unsubscribe link is added to every marketing email by default; an unsubscribe
  button is the `SpecialLinkUnsubscribeLink` chip; `Divider.border` needs one thickness on all four
  sides; `buttonSize.width` requires `widthType`.

New in ops (`maestra-email-ops`):

- Writes go to every visual-compatible format of the variant — Draft first, then Active.
- Test sends: `campaign_test_recipients` → `campaign_send_test`.
- Template-type change ("redo in the visual editor") is routed to a new campaign; `mailingKind` is a
  mandatory decision; folder/brand are resolved via `entities_list`.
- Letter styles via `visual_template_theme_get`; saved blocks via
  `visual_template_saved_block_list` / `_get`; feedback to the developers via MCP `feedback`
  (new reference `feedback-examples.md`).
- PNG preview links now arrive in the `visual_template_preview` response; `ChangeConflict` has no
  automatic retry.

## 1.0.0 — 2026-08-27

Initial public release: one `maestra` plugin carrying four skills.

- `maestra-email` + `maestra-email-ops` — create and edit emails for the Maestra visual
  editor: layout generation, gallery image search and upload, PNG preview, saving into
  your campaign as a draft.
- `filter-build` + `filter-explain` — build a CDP filter from a request in plain words,
  or explain a stored filter's JSON. Read-only.
