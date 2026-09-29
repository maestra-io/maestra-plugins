[![Maestra](assets/maestra-green.svg)](https://maestra.io)

# Agent skills

Skills that let Claude work in your [Maestra.io](https://maestra.io) account: set up once, then just chat. The setup is two steps: connect Maestra to Claude, then install the skills.

## What's inside

| Skills | What they do |
|---|---|
| **Emails** | Create and edit emails in the visual editor from a text description: layout, images, personalization chips, product recommendation rows, letter styles, preview, saving into your campaign, test sends to your staff test recipients. Live sending stays in Maestra. |
| **Filters** | Build a filter from a request in plain words and get a link to the list in your account; edit an existing filter without losing its conditions; explain a filter your account already stores. It can't save or change anything. |
| **Flows** | Summarize what an existing flow does; audit one flow or all of them for known anti-patterns, with a fix per finding; audit them on business results — revenue, orders, funnel and rates per flow — and get back what to change in the flow. Build a new draft flow from a request in plain words, or build into a flow that is already running — a draft is created from it. Launching stays with you. |

The skills see only what you can see in Maestra.

## Setup

Stuck at any point? Paste the link to this page into Claude and ask it to walk you through, or write to us in the Maestra support chat.

### Step 1. Connect Maestra to Claude

1. In Maestra, open **Integrations → MCP server** and copy your account's connector link.
2. In Claude, go to **Settings → Connectors → Add custom connector** and paste the link ([step-by-step guide](https://help.maestra.io/api-integrations/connect-an-ai-assistant-to-maestra-via-mcp)).

**On a Team or Enterprise plan** — only the workspace Owner can add connectors: send them the connector link.

### Step 2. Install the skills

1. In Claude, open **Settings → Plugins** — your personal settings, not the organization's.
2. Click **Add → Add marketplace**, paste `https://github.com/maestra-io/maestra-plugins`, and click **Sync**.
3. The **Maestra** plugin appears — click **+** to install it.

**On a Team or Enterprise plan** — everyone installs the skills for themselves. If you see **Sync from GitHub** instead of **Add marketplace**, you are in the organization's settings: go back to your own **Settings → Plugins**.

Using a different AI tool? See [Other AI tools](#other-ai-tools).

## Try it

First, check the connection:

- "What Maestra tools do you have?"

Phrases like "create an email" or "build a filter" wake the right skill:

- "Create an email in Maestra: a spring-sale promo with a hero image, two product cards, and a discount code. Show me a preview before saving."
- "Add a row of recommended products and greet the customer by name."
- "Build a filter: customers with a confirmed email who bought Nike in the last 90 days."
- "Add a condition to this filter: exclude anyone who ordered in the last 7 days." (paste the filter JSON)
- "Explain this filter — who does it select?" (paste the filter JSON)
- "What does the Welcome flow do?"
- "Audit our flows and tell me what to fix."
- "Which flows earned the most last month, and what should we change in the ones that did not?"
- "Build an abandoned cart flow: wait 30 minutes, skip anyone who ordered, then one email and an SMS a day later."
- "Add an SMS a day after the email to our running Welcome flow — keep it as a draft."

## What the skills do in your account and on your computer

The skills work through the Maestra connector with your permissions.

- **Read:** your projects; emails, campaign settings, letter styles, saved blocks, and the image gallery; flows; campaign and flow reports; the lists needed to name things — folders, brands, segments, products, promo codes, custom fields. For a test email, your staff test recipients' names, emails, and phones.
- **Change — only what you ask for:** save an email into a campaign; edit a campaign's name, settings, subject, or HTML; create an email campaign or a folder; build a draft flow — new, or a copy of a running one — adding, changing, or removing its blocks and filters; put a flow into testing mode; send a test email to your staff test recipients. Saving an email, a test send, and testing mode each wait for your explicit yes; a flow is built once you have answered its questions. The filter skills save nothing. Live sending, launching, and deleting flows or campaigns stay in Maestra.
- **Send:** an image you attach or point to on your computer goes to your Maestra gallery through an upload link the connector returns. When a tool misbehaves or you say a result is wrong, the skills may send Maestra's developers a technical report through the connector's `feedback` tool — your request and the tool calls with their answers. They are told to leave personal data out. The email skills show you the text first and ask; the others may send it without asking.
- **Run:** HTTP requests such as `curl` for that upload and to download an email preview's HTML; the bundled script `gallery_contact_sheet.py`, which downloads gallery images and puts small copies of them on one page in Cowork — for it, the skills may install the Python package Pillow from PyPI without asking. If a preview comes back without snapshots, the email skills may open it in Claude in Chrome, only to look.
- **Files:** downloads, reports you ask for, and the audits' working notes (a log of every call, a progress list for a project-wide audit) are saved in your working folder and stay there until you delete them.

Account data goes only to Maestra, `feedback` reports included, and to the links Maestra returns. The skills also open pages you point them to — say, a website to take brand colours from — and PyPI for Pillow; neither gets your account data. Some steps run in Claude sub-agents, inside the same Claude session. Nothing changes Claude's settings or permissions.

## Other AI tools

**ChatGPT** — this repository works there as a plugin too: in the ChatGPT app, open **Plugins → Add → Add a marketplace** and paste `https://github.com/maestra-io/maestra-plugins`.

For developers — the skills follow the open [Agent Skills](https://skills.sh) standard, so Codex, Cursor, and other compatible agents can use them:

```
npx skills add maestra-io/maestra-plugins
```

## License

[Apache-2.0](LICENSE)
