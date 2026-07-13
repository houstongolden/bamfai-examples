# Lovable Creator App

Build a small creator workspace in Lovable with Vite, React, Supabase, and the
public BAMF API. Because Lovable cannot start from an existing GitHub repo, use
the staged copy/paste prompts in [`LOVABLE_PROMPTS.md`](LOVABLE_PROMPTS.md) in a
new Lovable project, then export the generated project to GitHub.

The target flow is intentionally narrow:

```text
browser -> authenticated Supabase Edge Function -> https://api.bamf.ai/v1
                                                   |
             capabilities -> creator -> generate job -> review -> draft
                                                               -> schedule
```

Generation returns a reviewable candidate; it does not create a post. Creating
a draft requires approval of the exact content, first comment, and media.
Scheduling requires a second confirmation of the exact date, time, and
timezone. The app never offers or calls publish-now.

## Security contract

- Create a **creator-scoped** BAMF key for this one creator space.
- Add it through Lovable/Supabase secret storage as exactly `BAMF_API_KEY`.
- Only an Edge Function may read the secret or send the bearer header.
- Never put the key in browser code, Vite environment variables, tables,
  repository files, screenshots, prompts, chat history, analytics, or logs.
- Authenticate the browser user before the Edge Function accepts a request.
- Use a server-side action allowlist; do not expose an arbitrary BAMF URL proxy.
- Redact authorization headers and response secrets from logs and errors.
- Send a fresh `Idempotency-Key` on every changed mutation. Reuse it only when
  retrying the exact same request body.

Recommended minimum creator-key scopes:

```text
creator_spaces:read
posts:read
posts:write
ai:generate
```

Add `analytics:read` only for analytics views. Add `posts:schedule` only after
the scheduling UI and its separate confirmation have passed QA. Do not grant
`posts:publish`.

## Required Edge Function actions

Keep one typed action per allowed operation:

| Action | BAMF request | Mutation gate |
|---|---|---|
| `capabilities` | `GET /v1/agent/capabilities` | none |
| `auth` | `GET /v1/me` | none |
| `creator` | `GET /v1/creator-spaces` | none |
| `generate` | `POST /v1/generate/posts` | user starts generation + idempotency |
| `job` | `GET /v1/jobs/{job_id}` | none; poll to terminal state |
| `createDraft` | `POST /v1/posts` | exact content approval + idempotency |
| `schedule` | `POST /v1/posts/{post_id}/schedule` | separate time approval + idempotency |

On load, fetch capabilities before enabling actions, then run the read-only
`/me` and `/creator-spaces` smoke checks. Show unavailable actions as disabled
with the missing scope or capability; do not guess endpoints.

## Lovable LinkedIn connector boundary

The optional Lovable LinkedIn connector is builder-owned OAuth. Its documented
surface is basic member profile, primary email, and member-post publishing. A
connection represents one LinkedIn account shared by linked projects; it is not
per-end-user LinkedIn login.

It does **not** replace BAMF creator context, voice, generation, knowledge,
analytics, drafts, approvals, or scheduling. The starter must include a
**Connector Diagnostics / Contract** page that records:

- connected account and environment, owner, scopes, and last successful check;
- supported reads/writes and documented connector limitations;
- whether BAMF or Lovable owns identity, generation, draft, schedule, and post;
- the single enabled publishing transport.

Default to BAMF as the only scheduling/publishing transport. If a builder
chooses Lovable member posting, disable BAMF scheduling for that workflow and
require its own final confirmation. Never let both paths act on one post.

## Public versus private boundary

Safe to publish: BAMF endpoint names, scopes, request/response shapes, typed
client code, approval state machines, idempotency behavior, connector contracts,
and generic UI patterns.

Keep private: BAMF internal prompts, voice-synthesis logic, template corpus,
ranking and performance heuristics, provider credentials, private BAMF OS/admin
tools, client CRM mappings, raw creator knowledge, and service-role access. The
app consumes those capabilities through the scoped BAMF API; it does not
reimplement or expose them.

## Official references

- [Lovable authenticated API integrations](https://docs.lovable.dev/integrations/introduction)
- [Lovable + Supabase Edge Functions and secrets](https://docs.lovable.dev/integrations/supabase)
- [Lovable security overview](https://docs.lovable.dev/features/security)
- [Lovable LinkedIn connector](https://docs.lovable.dev/integrations/linkedin)
- [Lovable GitHub sync and import limitation](https://docs.lovable.dev/integrations/github)
- [BAMF developer docs](https://bamf.ai/docs)
