# Evalora candidate assessment entry calibration

Use when implementing or reviewing invite-only candidate assessment entry screens in Evalora.

## Lesson from session

The candidate assessment route (`/assessment/[sessionId]`, e.g. `/assessment/demo-session`) needs a dedicated first screen before the assessment intro/modules screen. The user provided a reference with a centered “Welcome to interview” card and expected it to appear first.

## Desired route flow

1. **Name-entry welcome screen** — first thing the candidate sees.
2. Existing assessment intro/modules page.
3. Module flow: AI interview → coding → behavioral → leadership → submit.
4. Submission success screen.

This is still a candidate-owned flow, so it should remain no-sidebar/focused. Do not add the admin/interviewer `AppShell` here.

## Visual skeleton

- Full-page pale lavender/blue background.
- Centered white card, roughly 620px wide, generous vertical padding, subtle border/shadow, rounded corners.
- Top row centered: small bot/AI icon + title block.
- Title: `Welcome to interview`.
- Subtitle: `Please enter your name to continue to assessment`.
- Required `Your Name *` label.
- Soft gray input with placeholder `Enter your full name`.
- Full-width cyan CTA: `Continue to interview →`.
- Small lock/confidentiality reassurance below.
- Below card: three compact trust/duration/module feature blocks with circular purple icons and vertical separators on desktop:
  - Secure & Private — Your information is protected.
  - 30–60 Minutes — Complete at your own pace.
  - Multiple Sections — AI, coding, behavioral, and communication.

## Implementation notes

- Use a separate pre-start state such as `currentStep === -1` so the existing intro remains `currentStep === 0`.
- Keep the timer stopped on all pre-module states (`currentStep <= 0`).
- Store the typed candidate name in local state and use it in the final submission summary when available.
- Make the Continue button a real form submit with `required` input so empty names do not advance.

## Verification

- Open `/assessment/demo-session`: welcome/name-entry screen appears first.
- Enter a name and click Continue: existing assessment intro/modules screen appears.
- Run `pnpm lint && pnpm typecheck && pnpm build`.
