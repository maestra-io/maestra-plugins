# CHANGELOG

## 1.3.0 — 2026-09-22

`filter-build` + `filter-explain` re-ported in full from the upstream `filters` plugin 1.3.0 (author
"AI tribe", the same team as the email and flow skills; both skills now carry
`metadata.version: 1.3.0`). Upstream rewrote both skills against the current filter tool family —
`filter_wiki_ls` / `filter_wiki_grep` / `filter_wiki_read`, `filter_search_entities`,
`filter_sql_validate`, `filter_compile_preview`, `filter_json_to_sql` — which is the family the
Maestra MCP server exposes today; the previous skills described a route through the shared `wiki`
tool and the retired lookup/build tools, so on a current server they had no working procedure.

New in `filter-build`:

- **Edits an existing filter**, not only builds a new one: the stored JSON is read back with
  `filter_json_to_sql`, every condition kept, the change applied, then validated and compiled again.
- The workflow is spelled out with tool-call examples: read the wiki's live `README.md` first, choose
  the root and editor (`root/…` pages, `filterablePropertySet`), consult recipes, glossary, patterns
  and — explicitly — `help`, resolve catalogue records with `filter_search_entities` (match and list
  modes, cursors, segmentations vs. segments) **before** drafting FilterSQL, clarify disputed
  choices, validate the complete draft with a `coverage` log of request → decision → reason, then
  compile once and require `status: ready` + `platform: accepted`.
- Regex search examples cover Russian and English word forms — the wiki's recipe, glossary and
  pattern pages carry both.
- JSON is requested (`includeFilterJson=true`) only when the user or another skill needs the payload,
  e.g. `flow-create` configuring a condition block; otherwise the link alone.
- A feedback template for a wrong result: the correct-filter URL, the trace URL or ID, and the
  chronological tool calls with arguments and responses, sent through the server's `feedback` tool.
- Bilingual trigger phrases (Russian and English) in the description.
- The CSM **starter set** (thirteen standard filters, the Texas geo segment, the two "bots"
  segments) stays as a Maestra appendix until the wiki ships it as a pattern.

New in `filter-explain`:

- Explains from the recovered FilterSQL: `filter_json_to_sql` first, then wiki lookups for each
  concept, catalogue lookups for values that stayed IDs, and a fixed answer shape — Result,
  Conditions, Limits and gaps — that preserves AND/OR grouping, negation, boundaries, time windows,
  segment-vs-segmentation and current-vs-historical distinctions.
- `unlabelled` / `unsupported` / `UNSUPPORTED_FILTER(...)` are disclosed as gaps, never rebuilt away.
- Bilingual trigger phrases in the description.

Plugin: `.codex-plugin/plugin.json` and `skills/filter-*/agents/openai.yaml` added (Codex / ChatGPT
metadata, as upstream ships); plugin description now mentions editing and explaining filters.

## 1.2.1 — 2026-09-22

- **`flow-business-audit`**: the frontmatter `description` was 1,335 characters; claude.ai's plugin
  marketplace caps it at 1,024 and left the skill out of the sync with a warning. Shortened to under
  1,000 characters with the same triggers and exclusions. No behaviour change.

## 1.2.0 — 2026-09-21

Four flow skills added, ported from the upstream `flow` plugin 1.27.0 (author "AI tribe") — the same
team whose visual-editor skills became `maestra-email` and `maestra-email-ops`. The upstream pack was
already English and already written against the flow tool family this platform exposes, so three of
the four are near-verbatim ports; the fourth was rewired onto this platform's own reporting.

- **`flow-summary`** (read-only) — a concise, structured business summary of one flow from its
  structure: trigger, logic, goal. Reads the graph with `flows_lookup` and decodes blocks, events and
  steps from the Flows wiki. Optionally folds in ~30-day execution counts.
- **`flow-issues-audit`** (read-only) — a technical audit of one flow or a whole project against known
  anti-patterns (processing load, communication correctness), each finding with a concrete fix and a
  short why. Offers a presentation-ready HTML checklist on request.
- **`flow-create`** (writes drafts) — builds a correct draft flow from a plain-language request:
  reads the wiki, resolves entities to ids, creates and fills blocks, wires outputs, verifies every
  block by reading it back, and hands over a link. Filter bodies are delegated to `filter-build` in a
  sub-agent and written back unchanged; marketing mechanics come from the wiki's mechanics folder,
  never from memory. Creates a mailing per send step; launches nothing.
- **`flow-business-audit`** (read-only) — a business audit that ends in fixes to the flows themselves:
  the figures find the flows worth opening, then their construction says why they move and what to
  change. Two report forms, full report or client-ready deck.

**`flow-business-audit` runs on `flow_report`, not on SQL.** Upstream computed every figure with
hand-written ClickHouse over two scenario marts; this platform's analytics catalogue does not carry
them, and its `flow_report` tool answers money, volume, funnel and every rate for every flow and for
the project **in one call** — the same computation behind the Scenarios screen, so a figure in the
report and a figure in the admin UI are the same figure. The skill's template handles were kept
(T1, T1m, T2, T10, T3f …) and their definitions replaced; `metrics-map.md`, `rates.md`,
`beyond-the-overview.md`, `invariants.md` and `calling-the-tools.md` were rewritten around the new
source. The datamart-coverage and recalculation-freshness handles retire with the marts, and the
revenue-by-mailing-type split is now read from construction plus the wiki's `flow_types` rather than
from a column — all three losses are stated in the skill rather than papered over.

Other adaptations: cross-skill references point at `maestra:` (`maestra:filter-build`,
`maestra:flow-summary`); flow links build on `https://<systemName>.maestra.io/scenarios/<id>`;
worked examples, both HTML report templates and the client deck are English with US currency;
`flow-summary`'s three output headings and `flow-issues-audit`'s project table are English by
default, translated with the report when the reader works in another language.

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
