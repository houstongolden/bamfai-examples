# creator.new

A remixable, open-source creator studio built natively on BAMF.ai. Onboarding
asks which platforms and formats to draft for, then the app drafts in the
creator's voice through the BAMF API/MCP.

- Lovable project: <https://lovable.dev/projects/ac24b2af-427a-4e8f-9a63-22a389f153e5>
- Going live on the `creator.new` domain.

Accounts connect through BAMF, so the app has **no social OAuth of its own**.
There is no "connect your accounts" step; connections come from the creator's
BAMF space.

```text
browser -> authenticated Edge Function -> https://api.bamf.ai/v1
             (holds BAMF_API_KEY)          capabilities -> creator -> generate -> review
```

## Run it in Lovable

1. Open the [Lovable project](https://lovable.dev/projects/ac24b2af-427a-4e8f-9a63-22a389f153e5).
2. Choose **Remix** to copy it into your own Lovable workspace.
3. In Lovable Cloud / Supabase secrets, add `BAMF_API_KEY`. It must be a
   **creator-scoped** key created in BAMF.ai settings. It is never exposed to
   the client: every BAMF call goes through an edge function.
4. Publish.
5. Optionally attach a custom domain.

## Run it locally

Once the Lovable project is synced to GitHub:

```bash
git clone <synced-repo-url>
cd <synced-repo>
npm i
npm run dev
```

The source sync is pending. The code will land in this folder when it is
exported.

## The .new domain rule

A `.new` homepage must be a tool that creates something immediately, not a
marketing page. Landing on creator.new should put the visitor in the studio,
ready to draft, with onboarding inline rather than in front of it.

## Privacy defaults

- Private by default.
- Sharing a session shares an AI summary with private details redacted, never
  the raw session.

## Related

- Onboarding step prompt: [`ONBOARDING_PROMPT.md`](ONBOARDING_PROMPT.md)
- Staged security prompts and the edge function contract:
  [`../lovable-creator-app`](../lovable-creator-app)
