# Post Review HTML

A BAMF-branded, single-file, local HTML page for reviewing generated post drafts.
Terminal output is a bad surface for reviewing LinkedIn content — this page renders
drafts with exact LinkedIn line-break semantics so the creator sees what will
actually post.

Built for coding agents (Claude Code, Codex, Cursor, etc.) working with the
BAMF API / MCP / BAMF Stack: generate drafts, render this page, `open` it,
then keep editing in the chat.

## What it looks like

- BAMF logo top-left (dark-mode aware, links to bamf.ai)
- Creator avatar + name in the header (pulled from their BAMF creator space)
- One section per post: tag, title, content, first comment, word/paragraph stats, `post_id`
- Left sticky nav of post titles; collapses to hover-labeled dots on narrow windows
- Light/dark theme toggle (respects system preference, remembers choice, no flash)
- Footer for open decisions (unconfirmed names, excluded facts, scheduling)
- Fully self-contained: zero external requests at view time

## Usage

```bash
python3 render.py sample.review.json --open
```

Real flow:

1. Generate drafts via `POST /generate/posts` (or `bamf.generate_post`), get approval, create drafts via `POST /posts`.
2. Build a `review.json` (schema below) from the created drafts.
3. `python3 render.py review.json -o review.html --open`
4. Tell the user the file path so they can reopen it anytime.

## review.json schema

```jsonc
{
  "page_title": "…",               // browser tab title
  "heading": "Three post concepts",// page H1
  "creator": {
    "name": "Justin Murphy",
    "meta": "AtlasGTM · prepared 2026-07-08",
    "avatar_url": "https://…"      // creator_space.linkedin_profile.profile_image_url
                                   // from GET /creator-spaces; empty -> initials circle
  },
  "status_html": "<b>Saved as drafts…</b>",  // trusted HTML, keep it short
  "posts": [{
    "key": "c1",                   // section anchor, unique
    "tag": "Concept 1",            // small uppercase label
    "badge": "saved as draft",     // optional, renders after the tag
    "title": "…",                  // section H2
    "subtitle": "…",               // one-line description
    "nav_label": "Alignment",      // short title for the sidebar
    "content": "…",                // EXACT post text — see line breaks below
    "first_comment": "…",          // optional
    "meta_left": "Vocabulary: …",  // optional footer-left note
    "post_id": "uuid",             // BAMF post id, shown for PATCH follow-ups
    "media": [{                    // optional image/carousel previews
      "kind": "image",             // image (default) | carousel | pdf | pending
      "url": "https://…",          // image/pdf: or "data_uri": "data:…"
      "slides": ["https://…"],     // carousel: slide image urls
      "pdf_url": "https://…",      // carousel: LinkedIn-ready PDF
      "job_id": "uuid",            // pending: generation job to poll
      "alt": "…", "caption": "…"
    }]
  }],
  "footer_notes": ["<b>Open decisions…</b>", "…"]  // trusted HTML strings
}
```

### Line breaks are the point

Post `content` must be the **byte-exact** text that will be posted. The renderer
maps a blank line to a paragraph gap and a single `\n` to a tight stacked line —
the same semantics LinkedIn uses. Never normalize or strip whitespace in content.

### Notes for agents

- `status_html` and `footer_notes` are injected as HTML. Only put your own
  generated markup there — never raw text from knowledge docs, transcripts, or
  other untrusted sources. Everything else is escaped by the renderer.
- The avatar is fetched once at render time and embedded as a data URI, so the
  page keeps working offline. If the fetch fails you get an initials circle.
- Copy style that creators have preferred: ~5th–6th grade reading level, no
  jargon, and no repeated distinctive phrases across posts in one batch.
- After rendering, keep the session going: edits go through
  `POST /generate/post-edits` → user approval → `PATCH /posts/{post_id}`,
  then re-render this page with the updated content.

## Files

| File | Purpose |
|---|---|
| `template.html` | Page chrome with `{{TOKENS}}`, BAMF logo baked in |
| `render.py` | Stdlib-only renderer: `review.json` → HTML |
| `sample.review.json` | Working sample with schema notes inline |
