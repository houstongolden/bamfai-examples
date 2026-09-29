# Onboarding prompt: platforms and formats

Copy/paste this into the Lovable chat for the creator.new project to improve the
"Which platforms should drafts be written for?" step.

````text
Improve the onboarding step "Which platforms should drafts be written for?".

Icons
- Replace text labels with the official app icons for X, LinkedIn, Instagram,
  TikTok, YouTube, and Threads. Use real brand marks, never a letter.

Layout
- Group by platform. Each platform is one row with its icon and name, and the
  formats it supports as selectable chips beneath it.
- Selecting a chip selects that platform + format. Selecting the platform icon
  toggles its default formats.
- Formats marked "coming soon" render as disabled chips with a subtle label.

Formats per platform
- X: Posts, Threads, Video, Image, Articles (coming soon)
- LinkedIn: Text posts (authentic long-form plain text), Image,
  Carousel / document, Video, Articles (coming soon), Newsletter (coming soon)
- Instagram: Carousel, Reel, Image, Caption
- TikTok: Short video scripts, Hooks
- YouTube: Short video scripts, Hooks
- Threads: Posts
- Long-form destinations, both coming soon: Blog, Newsletter

Flow
- Keep it clean and minimal. One screen, one primary "Continue" button.
- Do NOT add a "connect your accounts" step. Accounts and connections come from
  BAMF; this app has no social OAuth.
- Persist the selection and pass it to drafting so each draft targets the chosen
  platform and format through the BAMF edge function.

Focus styles
- Keep input focus styles on the wrapper, not the inner input. The input gets
  outline-none; use focus-within ring/border on the parent wrapper only. No
  focus:border, focus:ring, or box-shadow on the inner input/textarea.
````
