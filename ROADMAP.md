# Roadmap

What's next for this repo, in priority order. Two tracks: **examples** (small,
pullable, session-scoped) and **starters** (full apps, scaffold-a-project).
Everything builds on the BAMF API / MCP / BAMF Stack.

Work is organized by audience. **For creators** (single-creator workflows) is
the only track being built right now, in priority order. **For agencies**
(multi-creator/agency workflows) is planned and documented below, but not
being built yet.

## For creators — building now

All items below are single-creator workflows. This is the active build track,
in priority order.

### Shipped foundations

- `post-review-html`: local, exact-line-break draft review page.
- `lovable-creator-app`: staged Lovable prompts for a Vite + React + Supabase
  app with a creator-scoped BAMF Edge Function, capability discovery, approval
  gates, scheduling confirmation, and optional LinkedIn connector diagnostics.

### Track 1 — Next examples

#### 1. Media in the review page (image + carousel previews) — next up

**Audience:** creator

The `post-review-html` template already ships a `media` slot per post. The work
is the pipeline, not the page:

- Render `POST /generate/images` output (quote cards, portraits, infographics)
  inline under the post copy, with job status while generating.
- Carousel review: slide-by-slide horizontal strip per post, plus a link to the
  LinkedIn-ready PDF from `bamf.generate_carousel` / `POST /generate/carousel-pdfs`.
- Scale/likeness QA notes surfaced next to each asset so approval covers the
  image, not just the copy.
- Extend `review.json` schema: `media[].kind` (`image` | `carousel_slide` | `pdf`),
  `media[].job_id`, `media[].status`.

Why first: it completes the single most common agent flow (draft + asset
approval in one page) and the schema hook already exists.

#### 2. Calendar / schedule review page

**Audience:** creator

A second single-file HTML view: the creator's upcoming queue on a simple week
strip (`GET /posts?status=scheduled&include=media,first_comment,preview`),
with per-slot copy preview. Agents render it before proposing schedule times so
"your queue is full through Thursday" is visible, not asserted. Read-only —
scheduling still goes through approval in chat.

#### 3. Interview kit

**Audience:** creator

Terminal-friendly mini-interview runner: renders the 3-question flow from
`bamf-interview` into a small HTML form the creator fills locally, output saved
as `mini_interview_answers` JSON the agent feeds to `POST /generate/posts`.
Removes the copy/paste dance for creator stories.

#### 4. Analytics snapshot page

**Audience:** creator

One-file HTML report from `GET /analytics/summary` + top posts: what's working,
what shape of post over/under-performs, rendered with the same brand chrome.
Useful as the opening move of a content-planning session.

#### 5. Review-page polish backlog (small, anytime)

**Audience:** creator

- Copy-to-clipboard button per post (content + first comment).
- Inline diff view when re-rendering after a PATCH (old vs. new).
- Optional `?post=c2` deep link for sharing one concept.

### Track 2 — Future starter apps (`starters/`) — plan only, not building yet

Structure: one directory per starter, each fully self-contained with its own
README, `.env.example` (`BAMF_API_KEY`, `BAMF_API_BASE`), and a
`starters` entry in `examples.json`. Keep every starter deployable in one
command (Vercel/Netlify) and runnable locally with one install step.

#### S1. `nextjs-creator-dashboard`

**Audience:** creator

Next.js (app router) + BAMF API: creator space overview, draft list with the
review-page rendering built in as a component, schedule calendar, analytics.
The reference implementation for "build your own BAMF front-end."

#### S2. `vite-review-widget`

**Audience:** creator

The post-review page as an embeddable Vite/React component library — the same
review UX teams can drop into an existing internal tool. Shares the
`review.json` schema with the HTML example so agents can target either.

#### S3. `webhook-worker`

**Audience:** creator

Minimal serverless worker (Netlify/Cloudflare) consuming BAMF webhooks: post
published → notify Slack/Telegram, job succeeded → post asset preview into a
channel. The template for event-driven BAMF integrations.

#### S4. `mcp-agent-starter`

**Audience:** creator

A headless agent script (Claude Agent SDK) wired to the BAMF MCP: scheduled
content-pipeline runs (context → ideas → drafts for human review) with the
approval gates preserved. The reference for cron/CI usage of BAMF.

#### S5. `x-thread-studio`

**Audience:** creator

Small app focused on X/Twitter: `POST /generate/x-posts` thread candidates,
thread-by-thread review UI, character budget per item. Exercises the X surface
the same way post-review-html exercises LinkedIn.

## For agencies — coming soon (planned only, not building yet)

Multi-creator/agency workflows. These ideas are good and will be built, but
only after the single-creator track above is solid. Nothing in this section
has a schedule yet — treat it as a plan, not a queue.

#### Multi-creator roster dashboard

**Audience:** agency

One view across every client in an agency's roster: each creator's draft
queue, scheduled posts, and analytics summary side by side, so an agency
operator can see who needs attention without opening each creator space
individually.

#### Client approval portal

**Audience:** agency

A link-based review flow where the agency drafts content in BAMF and the
client approves or requests changes through a hosted page — no BAMF login or
terminal access required on the client side. Approval events flow back into
the normal BAMF approval gate.

#### Cross-creator calendar

**Audience:** agency

An agency-wide schedule view layering every client's queue onto one calendar,
so an operator can spot collisions, gaps, and over-scheduled weeks across the
whole roster at a glance. Read-only, same as the single-creator calendar page.

#### Agency webhook hub

**Audience:** agency

A fan-out version of `webhook-worker` (Track 2, S3): one webhook receiver that
routes BAMF events to the right per-client Slack/Telegram channel, so each
client's team gets their own digest without the agency wiring up N separate
workers.

## Conventions for new entries (either track)

1. Self-contained; dependency-light (examples: stdlib/no-build only).
2. README states when an agent should reach for it, with the full schema.
3. Register in `examples.json` (`examples` or `starters` array).
4. Never embed keys; read `BAMF_API_KEY` from the environment.
5. Approval-gated mutations, idempotency keys, no publish-now — same as the
   BAMF Stack safety rules.
6. Brand chrome: BAMF logo, dark-mode aware, grayscale accents, no
   boxes-in-boxes.
7. Every entry declares its audience (`creator` | `agency`). Agency entries
   stay plan-only — not built, not scheduled — until the creator track is
   solid.
