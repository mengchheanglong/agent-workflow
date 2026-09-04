# Digital Twin Plan Routing

Use this reference when routing Digital Twin / Transcendiverse implementation work.

## Current routing principle

If `C:/Users/User/archive/retired/digital-twin/project-plan/PLAN.md` exists, read it before recommending implementation slices. The user's current plan prioritizes phone-first daily usage, MongoDB reliability, HTTPS/PWA deployment, and compact Hermes summary sync before NPC/world expansion.

## Important user correction

The user clarified that PWA is not the final vision. PWA is a stepping stone and web fallback. The deeper target is phone integration: native app, widgets, and eventually Android launcher behavior where Digital Twin feels merged with the phone.

Route this as a staged bridge, not a leap:

```text
Next.js web app = cloud brain / dashboard / data source
Mobile API substrate = stable compact server contract
Native Android companion = daily phone use
Widgets = home-screen integration
Launcher mode = later, after daily native/widget loop is proven
```

## Recommended next-slice hierarchy

1. If deployment/PWA basics are broken, fix those only enough for web fallback:
   - HTTPS deployment
   - env vars
   - manifest PNG icons
   - minimal no-cache service worker if needed
2. If the user asks for launcher/native direction, do not start with launcher UI. Start with a compact mobile API substrate, especially:
   - `GET /api/mobile/today`
   - authenticated
   - `Cache-Control: no-store`
   - compact Today state and launcher actions
3. After deployed authenticated smoke succeeds, plan native Android companion/widget v0.
4. Only recommend one-room NPC/world work after the phone-first daily loop and Hermes summary loop are stable or the user explicitly redirects.

## Privacy rule

Mobile/native/launcher APIs must be compact read models, not raw logs:

- no raw journal
- no raw chat messages
- no email
- no secrets/tokens
- sanitize user-controlled fields
- avoid dumping full `TwinContextPack` unless the consumer is an internal AI agent and the endpoint is explicitly designed for that purpose

## Phrase-to-route mapping

- “Add to Home Screen doesn’t appear” → `phone-first-pwa-ux` + PWA installability reference.
- “This is more than PWA / merge with phone / launcher” → `phone-first-pwa-ux` + native launcher bridge reference; recommend mobile API substrate first.
- “Proceed” after launcher discussion → write a bounded Codex handoff for Mobile API / Launcher Substrate v0, not full launcher UI.
