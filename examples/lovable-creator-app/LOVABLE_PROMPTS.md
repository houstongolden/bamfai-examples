# Lovable Copy/Paste Prompts

Start a new Lovable project and paste these prompts in order. Do not paste a
BAMF API key into chat. When Lovable asks for the credential, enter the
creator-scoped key only through its secure secret input as `BAMF_API_KEY`.

## 1. Scaffold

```text
Build a focused creator app using Vite, React, TypeScript, Tailwind, and a
Supabase backend. Add Supabase email authentication. Use a clean full-width
layout with strong typography, section bands, dividers, and row structure; do
not use nested cards. Inputs must use outline-none on the inner element and put
focus-within styling on the parent wrapper.

Create routes for Dashboard, Generate, Review, Schedule, and Connector
Diagnostics / Contract. The app state must distinguish candidate, approved
draft, and scheduled post. Generation is not draft creation. Draft approval and
schedule confirmation are separate human actions. Add accessible loading,
empty, error, retry, and disabled states. Do not add any publish-now control.

Do not add a BAMF credential yet. Do not place secrets in VITE_ variables,
frontend code, database rows, sample data, logs, screenshots, or documentation.
```

## 2. BAMF integration

```text
Integrate the BAMF public REST API at https://api.bamf.ai/v1 using an
authenticated Supabase Edge Function. Follow https://bamf.ai/docs and the
authenticated-API pattern at https://docs.lovable.dev/integrations/supabase.

Ask me to add one creator-scoped secret named BAMF_API_KEY through the secure
secret UI. Never ask me to paste its value into chat and never expose it to the
browser, repository, database, logs, errors, analytics, prompt history, or
screenshots. The Edge Function must verify the signed-in Supabase user, read the
secret server-side, redact sensitive values, enforce request size limits, and
use a fixed typed action allowlist—not an arbitrary URL/path proxy.

Implement these actions only:
- capabilities: GET /agent/capabilities
- auth: GET /me
- creator: GET /creator-spaces
- generate: POST /generate/posts
- job: GET /jobs/{job_id}
- createDraft: POST /posts
- schedule: POST /posts/{post_id}/schedule

On app load, fetch capabilities first, then run read-only auth and creator-space
checks. Pin the UI to the creator returned by the creator-scoped key. Disable
unsupported actions and show missing scopes/capabilities. The minimum scopes are
creator_spaces:read, posts:read, posts:write, and ai:generate. Treat
analytics:read and posts:schedule as optional. Never request posts:publish and
never call or expose publish-now.

For POST actions create an Idempotency-Key. Keep the same key only while
retrying the byte-equivalent request; create a new key when the payload changes.
Generate a candidate, poll its job to a terminal state, and render exact content,
first comment, and media for review. POST /posts is enabled only after a checkbox
and confirmation dialog show the exact approved payload. Scheduling remains
disabled unless posts:schedule exists and requires a second dialog showing the
exact post, local date/time, timezone, and resulting ISO timestamp.
```

## 3. LinkedIn connector audit

```text
Read the current official LinkedIn connector documentation at
https://docs.lovable.dev/integrations/linkedin before changing code. Treat this
as an optional builder-owned OAuth connector for one workspace-managed LinkedIn
account. Its expected contract is basic profile, primary email, and optional
member posting; it is not per-end-user LinkedIn login and it does not replace
BAMF creator context, voice, generation, knowledge, analytics, drafts, approval,
or scheduling.

Build the Connector Diagnostics / Contract page. Show connection/environment,
account identity, owner, granted scopes, supported operations, documented
limitations, last check, and a responsibility matrix for identity, generation,
draft storage, scheduling, and final posting. Never render tokens.

Default to BAMF as the only scheduling and publishing transport. Keep Lovable
LinkedIn member posting disabled unless the builder explicitly selects it. Add
an invariant and tests that exactly one transport can be enabled for a workflow.
If Lovable posting is selected, disable BAMF scheduling for that workflow and
require a separate exact-content confirmation. Never fan out or retry through a
second transport after an ambiguous failure.
```

## 4. QA, docs, and screenshots

```text
Perform a security and behavior QA pass. Prove from the generated code that
BAMF_API_KEY appears only as a server-side secret lookup; no VITE_ secret or
browser Authorization header exists; the Edge Function allowlists actions and
authenticates users; every mutation sends idempotency; draft creation requires
exact-payload approval; schedule requires a second exact-time confirmation; and
publish-now is absent. Verify only one LinkedIn publishing transport can be on.

Test capability failure, invalid/expired BAMF key, missing scope, generation job
success/failure/timeout, duplicate click, changed payload, timezone/DST display,
network retry, and ambiguous transport failure. Do not make a real draft or
schedule without my explicit approval.

Add a concise README with setup, architecture, scope table, threat model,
approval state machine, diagnostics contract, test checklist, and official links
to https://docs.lovable.dev/integrations/supabase,
https://docs.lovable.dev/features/security,
https://docs.lovable.dev/integrations/linkedin, and https://bamf.ai/docs.

Capture screenshots with fake content and no PII or secrets: signed-out page,
capability/auth smoke success, creator dashboard, candidate review before
approval, draft confirmation, schedule confirmation with timezone, connector
diagnostics, and representative error state. Add alt text and list every image
in the README. Stop and report any security or publishing-path ambiguity.
```
