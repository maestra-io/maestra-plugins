# Feedback message examples

**When to read this:** you are composing the text for the MCP `feedback` per the
protocol in `SKILL.md` (section "Feedback about the skill via MCP feedback") and want
to see what well-filled `problem`/`context` look like on real runs. Read it if you're
unsure where the boundary between "the essence of the problem" and "context" lies,
or when the user asked you to pass on their words and you need to work out what to
add to `context` without replacing their wording.

**Return to:** the "Feedback about the skill via MCP feedback" section of `SKILL.md`.

The format is the same everywhere:

```text
[skill-feedback:v1]
skill=mailings-generator-editor
skillVersion=<from plugin.json>
source=user-report|agent-observation
problem=<the essence: what gets in the way, what went wrong>
context=<input data and requests, how the situation was reached, verbatim backend errors>
area=<layout|save|preview|gallery|personalization|other>
```

`area` is optional — add it only if the area is obvious. There is no separate field
for "reproduced/not reproduced": the fact of reproduction is part of `context`
(run date, one-off campaign, input data).

## Example 1. user-report: layout broke during a port

Who initiated: the user. Their words became `problem` verbatim; the agent added
`context`.

```text
[skill-feedback:v1]
skill=mailings-generator-editor
skillVersion=1.2.0
source=user-report
problem=The port from Klaviyo silently assembles the wrong layout: two adjacent images from one row of the source fall apart into a column.
context=Source: a 1200px container, two sibling images of 600px each. spec.json marked them as two full-width ones, so the generator built two 12+12 rows instead of 6+6. There were no backend errors — the port is formally "successful", but the rows in the email don't match the source. Repeated on several emails in a row.
area=layout
```

Why:

- `problem` is the user's words, not a retelling and not "packaging" into one sentence.
- `context` explains **why** the error went unnoticed: the backend didn't refuse,
  spec.json looked correct, the result was simply semantically wrong.
- `area=layout` — the area is obvious from the description, so the field is included.

## Example 2. agent-observation: partial persist on save

Who initiated: the agent. The agent writes both fields — it saw the problem itself
and can describe it with technical precision.

```text
[skill-feedback:v1]
skill=mailings-generator-editor
skillVersion=1.2.0
source=agent-observation
problem=visual_template_save can store the visual template but not attach it to the campaign; the response is easy to mistake for success.
context=One-off campaign in tenant Test-111, run of 2026-09-02. A save with a stale mailingRowVersion returned ChangeConflict with the verbatim text "The template itself WAS stored — only the campaign was not". A repeated campaign_get showed: the template grew to rowVersion=3, while the body attached to the email stayed at rowVersion=2. The subagent nevertheless reported "saved".
area=save
```

Why:

- `problem` is one or two lines: what exactly gets in the way and why it's dangerous.
- `context` is a verifiable chain: date, campaign, verbatim error, version
  numbers, what happened in the end.
- The fact of reproduction ("run of 2026-09-02, rowVersion=3 with body=2") is
  in `context`, not in a separate field.

## Example 3. agent-observation: tool description does not match the actual DTO

Who initiated: the agent. The problem is in the tool's documentation, not in the
backend's behavior; the context makes that clear.

```text
[skill-feedback:v1]
skill=mailings-generator-editor
skillVersion=1.2.0
source=agent-observation
problem=The description of gallery_images_list promises fields that aren't in the actual response — the skill's documentation has nothing to rely on.
context=Run of 2026-09-02, tenant Test-111. The tool description lists size/date; the actual response for the project contained only name, fileExtension, isSystem, url. With the .webp filter some URLs led to gallery-imgproxy (a conversion of the source file), some were direct S3. Both kinds of URL are valid for inserting into an email.
area=gallery
```

Why:

- `problem` draws the line: the tool works, but its description is misleading.
- `context` lists the actual set of fields and the `.webp` observation — that's
  what a developer will check first.
- No personal data, signed URLs, or email content — only the actual structure of
  the response.

## Anti-examples

### Anti-example 1. Too abstract a `problem`

```text
problem=The gallery works incorrectly.
```

Why it's bad: it's unclear what exactly gets in the way — search, upload, the URL,
the tool description. A developer won't be able to tell this feedback apart from a
dozen similar ones.

Fix: add specifics — "the tool description promises size/date, which aren't in the
response" (see Example 3).

### Anti-example 2. `context` without input data

```text
problem=Two images fell apart into a column.
context=The error was reproduced in a test run.
```

Why it's bad: `context` answers none of the questions — what the input data was,
how wide the container was, what the backend returned, on which campaign it was
reproduced.

Fix: add the container, the image widths, the absence of a backend error
(see Example 1).

### Anti-example 3. Replacing the user's words

The user said:

> The images from Klaviyo fell apart into a column when I was porting the email.

Wrong:

```text
problem=The layout doesn't adapt to mobile devices.
```

Why it's bad: the agent guessed the problem on the user's behalf — the user said
nothing about mobile devices. With `user-report`, `problem` is their words verbatim;
the agent puts its own interpretation into `context` as a separate phrase.

Right:

```text
problem=The images from Klaviyo fell apart into a column when I was porting the email.
context=A port from Klaviyo, a 1200px container with two sibling images of 600px each. The backend returned no errors, but the result is two full-width rows instead of 6+6.
```