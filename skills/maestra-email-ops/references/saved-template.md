# An email by a saved template

**When to read:** the user asks for an email "by template X", "from my templates", or to see their
saved templates.
**Return:** to the canonical workflow in `SKILL.md` — §3 for edits on top of the template, §4–§5 for
confirmation and save.

`visual_template_get` gives a saved template's blocks as JSX. Its width, background, CSS, letter styles and
product deduplication are not in it and go separately — `settingsSource`, the saved template. Without it the
email gets the template's blocks but not its look.

1. **Choosing the template.** `client_visual_template_list`. A template named in words with no exact match by
   name, or several — show the candidates and let the user choose. No look-alike.
2. **Target.** §1–§2 of the canonical workflow; a new campaign — "New campaign from scratch" first.
3. **Reading.** `visual_template_get` with `template` — the saved template.
4. **Letter styles**, when the generator needs them — `visual_template_theme_get` with `template` — the saved
   template — and `jsx`: after the save the email has the template's styles, not the campaign's.
5. **Confirmation** — §4, with the letter-styles line "the email's width, background, CSS and letter styles are
   taken from template <name>", plus "and changed by this document" if it has `<Theme>`.
6. **Save** — §5 with `settingsSource` — the saved template, in this one save only. The next edits are saved
   without it: the campaign already holds the settings, and passing it again overwrites what the user has
   changed in the editor since.
