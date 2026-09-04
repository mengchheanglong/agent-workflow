---
name: uxpeak-ux-ui-design
description: "UX/UI design audit and redesign skill synthesized from UX Peak's YouTube channel: psychology, conversion, mobile navigation, visual hierarchy, ecommerce, Figma prototyping, 3D/AI visual workflows."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [ux, ui, product-design, conversion, mobile, ecommerce, psychology, figma, prototyping, animation, ai-design]
    related_skills: [phone-first-pwa-ux, popular-web-designs, claude-design, standalone-html-ui-artifacts]
---

# UX Peak UX/UI Design

## Source coverage

This skill distills the reusable lessons from the UX Peak YouTube channel inventory at `https://www.youtube.com/@uxpeak/videos`:

- 20 long-form videos from the channel Videos tab.
- 1 Short from the Shorts tab, counted by YouTube in the channel total.
- English transcripts/subtitles were available for 20/21 items; the Short had metadata only.
- The synthesis paraphrases lessons and design patterns; it does not store transcripts or reproduce copyrighted video text.

See `references/uxpeak-video-inventory.md` for the source list and lesson map.

The local source corpus used for upkeep—21 channel records with captured metadata, VTT captions, and cleaned transcript text—is preserved but not loaded by default under `references/source/uxpeak-channel-2026-07-07/`. Read its `README.md` only when auditing or improving this skill; paraphrase lessons rather than reproducing transcript text.

## When to use

Use this skill when the user asks to:

- design, redesign, or critique a UX/UI screen;
- improve onboarding, paywalls, checkout, product pages, pricing cards, booking flows, search, empty states, order tracking, mobile navigation, or dashboard cards;
- make a UI feel more senior, polished, trustworthy, persuasive, or easier to use;
- create a Figma/prototyping plan for animations, smart-animate states, bottom navigation, 3D hero interactions, carousels, scroll prototypes, or AI-generated visual assets;
- write a design handoff prompt for Codex/Gemini/Stitch/Claude/OpenCode that needs concrete UX/UI rules.

Pair with `phone-first-pwa-ux` for deep mobile/PWA implementation gates. Pair with `popular-web-designs` or `claude-design` for brand/landing-page visual systems.

## Core stance

UX Peak's strongest lesson is: **a screen is not just a layout; it asks the user a question.** Better UX changes the question from hard, risky, abstract, or effortful into easy, safe, specific, and valuable.

Examples of question-shaping:

- Paywall: do not ask “Is this worth $19/month?” before value is felt. Ask “Can I safely try this for free?” with a trial timeline, reminder, and cancellation reassurance.
- Ride/booking choice: do not ask “How much price risk am I accepting?” with ambiguous ranges. Ask “Which clear option do I want?” with one comparable price/ETA per option when accurate.
- Booking page: do not ask users to fill a cold form. Help them imagine the trip with a strong visual, sensory title, dates with day names, night count, total price, and cancellation reassurance.
- Ecommerce product page: do not merely show a product. Guide the user from “this looks interesting” to “I understand it, trust it, and know what to do next.”

## UX psychology patterns

Use these ethically. Do not fake urgency, scarcity, progress, reviews, ratings, results, demand, or availability.

### 1. Smart defaults reduce decision fatigue

Blank forms make every field a decision. Pre-fill the most common, defensible choices and let users adjust.

Apply when:

- booking/search forms have common defaults;
- onboarding asks for settings that can be inferred;
- filters have a likely default state.

Rules:

- Default values should be correct for most users, not manipulative.
- Make the default visible and easy to change.
- Replace generic CTA copy with result-oriented copy when possible: “Show 12 results,” “Find matches,” “Continue setup.”

### 2. Endowed progress creates momentum

Starting at 0% feels like standing still. Showing legitimate progress already earned makes users more likely to finish.

Apply when:

- onboarding has multiple steps;
- profile completion matters;
- setup or checklist flows risk abandonment.

Rules:

- Count real completed setup, imported data, first action, or account creation as progress.
- Show the next most valuable action, not a huge checklist.
- Avoid fake progress bars that claim work is done when it is not.

### 3. Give value before asking for commitment

Reciprocity works because users feel helped before they are asked to sign up, pay, or save.

Apply when:

- lead magnets, reports, calculators, quizzes, or AI outputs require account creation;
- users need evidence before trust;
- signup is blocking first value.

Rules:

- Let users see useful output first, then ask them to save, customize, export, or continue.
- Frame signup as preserving value they already received, not as a wall before value.

### 4. Let users build or personalize before signup

The IKEA/endowment effect: people value what they helped create. A user who has chosen goals, style, name, language, or first content has something to lose by abandoning.

Apply when:

- onboarding can include a meaningful first choice;
- customization makes the product feel personal;
- a blank signup form currently appears too early.

Rules:

- Keep pre-signup creation lightweight.
- Make the saved artifact visible: profile, plan, report, card, first lesson, selected destination.
- Do not trap users; preserve agency and explain why account creation is needed.

### 5. Use loss framing carefully

Loss aversion can motivate action, but it easily becomes dark-pattern territory. Show the real cost of inaction only when it protects the user.

Apply when:

- data loss, storage, security, cancellation, missed deadlines, or failed backups are real risks;
- the user already owns or created something.

Rules:

- Frame the concrete thing at risk, not a generic threat.
- Use honest wording; never invent countdowns or scarcity.
- Give a calm escape path; avoid shame copy.

### 6. Anchor numbers in context

A number shown alone feels different from the same number shown beside a meaningful reference.

Apply when:

- pricing add-ons are compared with a larger purchase;
- discounts and bundles need context;
- dashboards show metrics without benchmarks.

Rules:

- Show honest reference points: original price, total trip price, percentage of cart value, before/after metric, benchmark.
- Do not manufacture fake crossed-out prices.
- Control what the user sees first because the first number becomes the ruler for the next number.

### 7. Reduce evaluative effort

Users avoid decisions that require too much comparison, uncertainty, or mental math.

Apply when:

- prices are shown as broad ranges;
- users must calculate totals, nights, discounts, or balances;
- options look equally weighted when one is usually better.

Rules:

- Prefer one clear comparable value per option when possible.
- Show totals and consequences before confirmation.
- Use small labels like “cheaper,” “recommended,” or “most popular” only when true and useful.

### 8. Prefer recognition over recall

Interfaces become safer when users recognize people, actions, destinations, and categories instead of remembering exact details.

Apply when:

- sending money or messages;
- selecting recipients/accounts;
- category browsing;
- search and recent history.

Rules:

- Use avatars, logos, icons, category visuals, recent recipients, and saved items.
- Put exact identifiers near the visual cue when risk is high.
- Do not rely on ambiguous icon-only controls for unfamiliar actions.

## Conversion and ecommerce UX checklist

Use this for product pages, checkout flows, pricing pages, subscriptions, trial screens, and paid CTAs.

### Product page structure

- [ ] The hero image bridges the imagination gap: show the product in use, consumed, worn, installed, or producing its promised outcome.
- [ ] The first badge/status label is truthful and frames the product: best-seller, new arrival, top-rated, recommended, clinically tested, etc.
- [ ] Review and rating numbers are specific and real: e.g. `4.9 stars · 221 reviews`, not vague placeholders.
- [ ] Social proof answers “Am I the first person taking this risk?” with real demand or credible proof.
- [ ] Flavor/variant choices are visible as cards/chips when the set is small; avoid lazy dropdowns that hide basic options.
- [ ] Trust elements are specific: money-back guarantee, cancellation, shipping window, ingredients, safety, warranty, return policy.

### Pricing/subscription cards

- [ ] Recommended plans are visually guided, not forced.
- [ ] Fear reducers live inside the decision card: “cancel anytime,” “reminder before charge,” “free cancellation,” “priority dispatch,” “save 15%.”
- [ ] Bundles use progressive disclosure: keep the first decision clean, then reveal money-saving quantity options if relevant.
- [ ] The CTA states the next concrete outcome: `Reserve €445 total`, `Start free trial`, `Add 3-month bundle`, not just `Submit`.
- [ ] Totals, recurring charges, billing dates, and cancellation policies are visible before payment.

### Ethical guardrail

Good conversion UX supports both the business and the user. If a design would increase conversion by making users less informed, less autonomous, or more pressured by false information, reject it.

## Visual hierarchy and UI polish

### Plan hierarchy before styling

Before designing, list every element the screen needs, then rank it by user importance.

Rules:

- Values usually matter more than labels in metric cards.
- The current task/action usually matters more than decoration.
- Secondary actions should not compete with the primary CTA.
- If every card has the same weight, no card is important.

### Use size, weight, color, position, and cues intentionally

- Use larger type, stronger weight, color, or placement for the primary information.
- Use lighter labels for supporting metadata.
- Use icons, avatars, logos, images, badges, and progress/timeline visuals to make information scannable.
- Avoid presenting all data as identical label-value rows.

### Shadows and depth

- Use soft shadows that blend with the background.
- Avoid harsh black/gray shadows on colored backgrounds.
- Tint shadows toward the background or surface color when appropriate.
- Use depth to clarify layering, not to decorate every card.

### Visual consistency

- Category cards and image-heavy layouts need stylistic consistency: matching crop style, lighting, color treatment, and visual rhythm.
- Random stock photos can make a screen feel less branded even if each image is individually attractive.
- A polished screen should be readable in seconds, not merely impressive at first glance.

### Creative layouts must still reduce effort

Creative card layouts can make option sets more memorable than plain lists, but only if they improve scan speed and comprehension.

Prefer creative layouts when:

- options benefit from images, icons, or examples;
- users must compare categories or plans;
- the layout makes the next action clearer.

Avoid creative layouts when:

- they hide information;
- text contrast is weak;
- visual style overwhelms usability;
- users must read more, not less.

## Friction-removal patterns

### Expose value directly

Do not hide first value behind a banner, card, or vague promise if the content can be shown immediately.

- Bad: `Discover 100+ recipes` banner that requires a tap.
- Better: show a few relevant recipes immediately, with a way to explore more.

### Search should not become a blank dead end

When the user taps search, support intent.

Include, when relevant:

- recent searches;
- popular items;
- personalized recommendations;
- categories/chips;
- suggestions that can be ignored if the user already knows what to type.

### Empty states should teach and invite action

A bare `No projects` state is a dead end.

A strong empty state includes:

- plain explanation of what belongs here;
- a concrete benefit;
- a sample or illustration if helpful;
- one primary CTA.

### Post-purchase/order tracking reduces anxiety

After payment, the user is waiting and uncertain. Design for reassurance.

Include:

- confident status message: `Your order is on the way`;
- delivery window and address with clear visual cues;
- courier/person/service info with quick contact actions;
- visual timeline for progress;
- item summary without forcing users to parse raw text.

### Choose input by context, not by aesthetics

- One-time, low-precision values in a known range: sliders, wheels, pickers can work well.
- Frequent, precise, repetitive values: text fields, steppers, or number inputs are usually better.
- High-risk inputs: show consequences immediately, such as new balance, total charge, account debited, recipient, or cancellation date.

## Mobile bottom navigation

Fundamentals come before microinteractions.

### Destination selection

- [ ] Bottom navigation contains the most frequent top-level destinations only.
- [ ] Aim for 3–5 tabs; max 6 only with strong justification.
- [ ] Do not put Help/FAQ, legal pages, logout, one-off settings, or rarely used admin pages in bottom nav.
- [ ] Prioritize destinations by user behavior, not org chart.

### User fit

- [ ] Know the audience age, technical comfort, device size, and primary jobs.
- [ ] Use labels when the audience or icons are not obvious.
- [ ] Icon-only nav is acceptable only for highly familiar destinations and tech-comfortable users.

### Touch, layout, and safe area

- [ ] Tap areas are at least 44×44 px; preferably 48×48 px in implementation.
- [ ] Nav is not cramped against the home indicator/safe area.
- [ ] Bar height is balanced: visible enough to tap, not so bulky that it steals content space.
- [ ] Main content has enough bottom padding so it is not hidden behind fixed nav.

### Active/inactive state

- [ ] Current tab is immediately obvious.
- [ ] Use active color, filled icon, label weight, underline, pill, or other cue.
- [ ] Inactive icons remain visible; do not drop contrast too far.
- [ ] Use one icon style across tabs, with the selected state as the intentional exception.

### Visual style

- [ ] Icons are simple, familiar, and semantically accurate.
- [ ] Labels are short, single-line, and plain.
- [ ] Colors stay neutral and brand-consistent; do not assign every tab a random color.
- [ ] Separate nav from content using a subtle border, background difference, or soft shadow.
- [ ] Notification badges are subtle, readable, and not overused.

### Microinteractions

Add only after the fundamentals pass.

Good microinteractions:

- quick tap feedback: color, scale, ripple, or pressed state;
- smooth active indicator movement;
- icon transition between outline/filled state;
- soft fade or slide between screens;
- durations that feel responsive, not slow.

Bad microinteractions:

- animation that hides delay;
- large motion for common navigation;
- effects that make the user unsure where they landed;
- motion that ignores reduced-motion needs.

## Figma and prototyping workflow

### Fast Figma productivity moves

Use these before slow manual cleanup:

- **Delete and heal vectors:** use Figma's heal behavior when simplifying paths so geometry stays smooth instead of broken.
- **Select all with same property:** bulk-select matching fill, stroke, text style, effect, or component instances for consistency sweeps.
- **Smart selection / tidy:** normalize spacing in grids, chip rows, card arrays, and icon groups before fine-tuning.
- **Nudge settings:** adjust small/big nudge values for dense UI and pixel-polish work.
- **Image styles and multiple fills:** reuse image fills and add gradient/color overlays directly on images to improve text readability without extra overlay clutter.
- **Copy/paste properties:** transfer repeated fills, strokes, shadows, radii, and typography quickly.
- **Ignore auto layout temporarily:** use the spacebar override when an item needs free positioning inside an auto-layout group.
- **Built-in calculator:** use math directly in width/height/position fields for precise proportional sizing.
- **Arc tool:** use native arc controls for radial/progress/ring visuals instead of hand-drawn approximations.

### Foundation setup

1. Start with a brief: product, target user, primary goal, top objections, desired action.
2. Set up frames for target devices early.
3. Define grid, spacing rhythm, text styles, and color styles before scaling the design.
4. Use auto layout for repeatable rows, cards, nav items, chips, and sections.
5. Use named layers, frames, and components so Smart Animate can match states reliably.

### Styles and systems

- Create named color styles instead of relying on raw hex codes.
- Create text styles for headings, body, labels, and UI metadata.
- Use shared active/inactive color styles for nav and controls.
- Detach styles only for intentional one-off changes.

### Smart Animate patterns

Use duplicated frames/components as explicit states.

Rules:

- Keep layer names consistent between states.
- Use frames/components/variants for interactive states rather than unstructured groups.
- Move/rotate/resize the same named objects between states.
- Use `On click` → `Change to`/navigate → `Smart Animate`.
- Typical timing from the videos: ~600ms for carousel transitions; ~1000ms for slower nav demonstrations. In production, shorten if it feels sluggish.
- Use gentle easing; avoid abrupt teleports.

### Component variants for navigation

For animated bottom navigation:

1. Build the nav bar and each tab hit area.
2. Make touch areas large enough before polishing visuals.
3. Create one state per active tab.
4. Combine states as variants.
5. Wire each inactive icon to the corresponding active variant.
6. Preview in the mobile frame and check that the active cue, motion, and target size all work.

### Scroll prototypes

For horizontal chips/cards inside a vertical mobile screen:

1. Put the scrolling items in auto layout.
2. Constrain the scrolling container to the viewport width.
3. Set overflow/scroll behavior in Prototype mode.
4. Test with enough items to confirm the scroll actually works.
5. Keep primary actions outside hidden horizontal overflow unless the user expects a carousel.

### 3D / animated hero patterns

- Use 3D/AI visuals as storytelling and brand memory, not pure decoration.
- Separate foreground/midground/background layers when an animation needs parallax or scroll movement.
- Duplicate frames for each animation state and adjust positions/rotations gradually.
- For carousels, keep the sequence logic consistent forward and backward; test both directions.
- Add shadows/glows/background color changes to support depth, but keep text readable.

### Dora / no-code 3D workflow

When using Figma + Dora-style tools:

1. Match the destination frame size/height before importing.
2. Paste/import Figma layers; inspect and fix misaligned elements.
3. Source lightweight, licensed, downloadable 3D models.
4. Add camera/model keyframes incrementally.
5. Set constraints/responsiveness in the destination tool, not only in Figma.
6. Preview multiple viewport sizes; note tool limitations honestly.

### AI-generated visual workflow

Use AI image tools to break out of generic stock visuals, but keep control of product fit.

1. Gather mood references first: palette, lighting, composition, subject, emotional tone.
2. Prompt with product context, style, aspect ratio, and intended screen placement.
3. Generate variations; pick for usability and brand fit, not just beauty.
4. Integrate into Figma with overlays/gradients if text sits on top.
5. Check licensing, consistency, and whether the generated visuals accurately represent the product.

## Interactive web and UI trend guidance

UX Peak highlights interactive sites with 3D, WebGL/Three.js, scroll-triggered motion, custom cursors, huge typography, and cinematic product storytelling. Treat these as tools, not obligations.

Use advanced visuals when they:

- help users understand a product from multiple angles;
- make a technical/industrial/service offering easier to grasp;
- support narrative progression as the user scrolls;
- create brand memory without hiding the message.

Avoid advanced visuals when they:

- slow the page before value is visible;
- reduce accessibility or keyboard usability;
- make text contrast worse;
- distract from the CTA;
- are copied because they are trendy rather than because they solve a communication problem.

Minimalism remains valid: every element should have a purpose. Huge typography can become the visual system, but word choice must be sharp because the text is carrying both message and composition.

## Project framing and research workflow

Before high-fidelity UI work, force the design through a small strategy pass:

1. **Define the brief** — product type, target user, primary user job, business goal, and desired action.
2. **Separate assumptions from evidence** — note what is assumed, what comes from competitors/reviews/forums/analytics, and what comes from direct user research.
3. **Write a specific problem statement** — name the user group, need, context, and desired outcome. Avoid vague prompts like “make a marketplace.”
4. **Map the journey** — identify before/during/after states, especially post-purchase, empty, error, loading, complete, and return-user moments.
5. **Choose fidelity deliberately** — low-fi for structure, mid-fi for UI shape, high-fi/prototype for realistic testing and handoff.
6. **Test interaction, not just visuals** — clickable prototypes reveal navigation, scroll, state, and motion issues that static screens hide.
7. **Handoff with specs** — include dimensions, spacing, responsive behavior, component states, and interaction timing.

## UX/UI audit procedure

When reviewing a screen, work through this order:

1. **User and job** — Who is the user, what are they trying to do, and what is their current context?
2. **Question audit** — What question does the current screen ask? Is it too hard, risky, abstract, or effortful?
3. **First value** — Does the first viewport show value, clarity, and next action?
4. **Friction** — What decisions, taps, fields, mental math, hidden content, or uncertainty can be removed?
5. **Trust** — What proof, policy, total, consequence, or reassurance should appear before the user worries?
6. **Hierarchy** — Are the most important values/actions visually dominant? Are labels and metadata secondary?
7. **Recognition** — Can users recognize people, options, categories, and state instead of remembering details?
8. **States** — Are empty, loading, selected, inactive, complete, error, post-purchase, and already-done states designed?
9. **Mobile** — Are tap targets, thumb zones, bottom nav, labels, safe area, and content padding correct?
10. **Motion** — Does animation clarify state/change, or is it decoration? Does it respect reduced motion?
11. **Ethics** — Is every claim, badge, countdown, discount, review, result, and scarcity cue truthful?
12. **Handoff** — Are dimensions, spacing, styles, responsiveness, interactions, and edge cases specified for implementation?

## Personal dashboard / Profile-Me screens

For personal-intelligence, habit, quest, or self-improvement products, Profile/Me should not become a passive stats/settings dump. Apply the UX Peak question-shaping rule:

- Weak question: “Here are your stats and settings.”
- Better question: “What should I do next, and can I still manage my data safely?”

Recommended order: screen-purpose framing → identity/progression hero → one context-aware next-best-action card → momentum metrics → quick routes/settings → data ownership. For no-data/new users, prefer a value-first baseline action such as `Check in now` over sending them to insights or declaring “all clear.” Preserve export/delete controls visibly, but do not lead with account management unless the screen’s job is specifically privacy/settings.

Do not let UX framing become product-theater copy. If a Profile/Me redesign adds generic meta sections such as “operating profile,” “command center,” “next best action,” “why now,” “effort,” or “trust,” verify they earn their space in the live UI. For this user, remove over-explaining command-center copy when it crowds the profile; keep the profile focused on identity/progression, stats, quick actions, and ownership controls.

### Visible redesign calibration

If the user asks for a redesign, “world-class” UI, or says the result does not look very different, escalate beyond copy and minor card ordering. The first viewport should visibly change through composition, scale, and hierarchy: a screen-level framing panel, a reworked hero, a dominant next-best-action card, and a different layout rhythm. UX-correct but subtle changes can still miss the user's intent when they are judging the live website visually.

When adapting a screen from a provided reference project or screenshot, do not only copy behavior/data flow and then wrap it in the local app’s generic card/module style. Preserve the reference’s recognizable layout skeleton first: navigation placement, primary panel split, density, chrome level, action placement, and information hierarchy. Then apply the local design tokens. If the user asks “is this what you took from it?” or dislikes a section, treat that as a fidelity failure: re-open the reference, compare screenshots side-by-side, and replace the mismatched skeleton rather than defending a functionally equivalent UI.

For coding/workspace-style references, the skeleton often matters more than decorative branding: challenge/problem navigation, compact topbar, problem statement panel, editor/terminal panel, run/submit toolbar, and result state should remain visibly recognizable. Avoid converting a workspace into a large marketing/assessment card with oversized headers, horizontal chips, or extra instructional callouts unless the reference used that shape.

If a coding/workspace UI still feels chaotic after matching the skeleton, simplify before adding polish: remove redundant instruction blocks, reduce uppercase label noise, make the active challenge state subtle, shrink utility controls, balance problem/editor columns, and browser-check that challenge labels do not truncate. See `references/coding-workspace-redesign-calibration.md` for the Evalora coding-assessment lesson.

For candidate-management/reporting surfaces, avoid duplicating navigation concepts. A candidate report is usually a candidate/session detail artifact, not a separate top-level app area. If the user provides separate candidate-detail and candidate-report screenshots, first match the route skeleton and remove redundant top-level report navigation. For Evalora specifically, keep admin/interviewer candidate detail and report routes inside the normal app shell/sidebar when they are reached from the Candidates tab; only candidate-owned test-taking flows should be no-sidebar/focused. Candidate detail should use only the needed tabs (Overview + Report), and report access should come from candidate context rather than a redundant `Candidates Reports` sidebar item. See `references/evalora-candidate-detail-report-calibration.md` for the Evalora candidate detail/report lesson, and `references/evalora-candidate-assessment-entry-calibration.md` for invite-only assessment entry screens.

For chat/AI companion surfaces, calibrate against the metaphor the user named. If they ask for ChatGPT/Grok-style, the recognizable pattern is a wide full-background conversation canvas with minimal chrome, centered empty prompt, and bottom composer. A side explainer panel or dashboard card shell may be visually “more designed” but still wrong because it changes the product question from “what do you want to ask?” to “manage this dashboard.”

After implementation, open the exact screen and inspect a screenshot. If old and new look broadly similar at a glance, push the redesign further before reporting completion. If adapting from a reference, explicitly check whether the screenshot still has the reference’s layout skeleton before running final build/commit. If the user says a page is “too big” or “too small,” treat it as scale calibration rather than a binary reversal: adjust shared spacing, type, controls, and container width in moderate increments; browser-check the exact route after each change; avoid overcorrecting from one extreme to the other.

When the user invokes “world-class,” “Trello/Notion level,” or says the UI still looks horrible, treat that as a quality escalation, not a request for more explanation. Use the strongest relevant product metaphors and any good UI libraries already in the project for real interaction polish. Keep iterating on visible defects from browser screenshots — clipped table columns, wrapped pills, cramped drawers, accidental overflow, raw counts, and weak hierarchy — even if typecheck/build already pass.

### Chat interface calibration

When the user asks for a ChatGPT/Grok-style chat surface, interpret that as a full-bleed conversational canvas, not a dashboard redesign. Avoid adding side explainer panels, dense cards, or a centered module shell unless explicitly requested. The accepted shape is usually: minimal top bar, large open message area, bottom composer, broad background coverage, and only intentional inner content width. If a parent dashboard layout has a max-width/padded wrapper, remove or bypass it for the chat route before judging the result.

Composer polish matters as much as the shell: the input should read as a compact chat rail, not a tall form card. Full-bleed background does not require full-width controls; if the user says the text bar is too wide, keep the page/background full-bleed and narrow only the composer. If a user says the text bar is too big, shrink vertical padding/min-height and remove extra helper copy before changing page structure. If the send button looks uneven, use a true square icon button with centered flex layout rather than a generic button component that may add hidden spans/gaps.

See `references/digital-twin-profile-me-redesign.md` for the Digital Twin Profile/Me pattern and CTA selection rule. See `references/profile-me-visible-redesign-calibration.md` for the session-specific lesson on making a Profile/Me redesign visibly obvious. See `references/collabai-dark-collab-ui-redesign.md` for the Trello + Notion + ChatGPT pattern for dark AI-powered collaborative project-management screens.

## Common anti-patterns

- Blank onboarding forms when smart defaults or value-first setup are possible.
- Signup/payment walls before the user has felt any value.
- Pricing or totals shown in isolation with no honest context.
- Price ranges where users need one accurate comparable value.
- Dropdowns hiding a small set of basic product options.
- Review counts, badges, scarcity, urgency, or “most popular” labels that are fabricated.
- Equal-weight metric cards that hide the important value behind labels.
- Harsh black shadows, random stock imagery, weak text contrast, or inconsistent icon styles.
- Empty states that only say “nothing here.”
- Search screens that become blank after focus.
- Order tracking that dumps data instead of reducing anxiety.
- Bottom nav with too many tabs, legal/logout/help destinations, tiny hit areas, or no separation from content.
- Beautiful animations that ignore usability, performance, accessibility, or reduced motion.

## Design handoff prompt template

Use this when asking a design/build agent to improve UI:

```text
Use the `uxpeak-ux-ui-design` skill to redesign/review this screen.

Product/context:
- Product: <name>
- User: <target user>
- Main job: <what they are trying to do>
- Current problem: <confusing, low conversion, ugly, too much friction, etc.>
- Desired action: <signup, purchase, reserve, continue, check in, complete setup>

Required analysis:
1. Identify the hard question the current screen asks.
2. Rewrite the screen so it asks an easier, safer, more specific question.
3. Remove interaction cost, hidden value, mental math, and unnecessary choices.
4. Improve trust with truthful proof, totals, consequences, policy, or reassurance.
5. Improve visual hierarchy using size, weight, color, spacing, and cues.
6. Check mobile nav/tap targets/safe area if the screen is mobile.
7. Specify selected/empty/loading/error/complete states.
8. If using motion, define purpose, state changes, easing, duration, and reduced-motion fallback.

Constraints:
- Do not fake urgency, scarcity, progress, reviews, ratings, demand, or results.
- Conversion matters, but user trust matters more.
- Prioritize usability before decorative animation.

Deliverables:
- Before/after rationale.
- Component-level changes with exact file paths if implemented.
- UX checklist pass/fail notes.
- Verification: lint/build if code changed, plus viewport/prototype check when available.
```

## Verification checklist

Before presenting a UX/UI recommendation or implementation:

- [ ] The recommendation is tied to a specific user job and screen question.
- [ ] Any persuasive psychology pattern is ethical and truth-based.
- [ ] Primary CTA and primary information are visually obvious.
- [ ] Users see value before major commitment where possible.
- [ ] Hidden friction, mental math, and unnecessary input are reduced.
- [ ] Trust/cancellation/total/consequence information appears before the user worries.
- [ ] Mobile tap targets and safe areas are checked when relevant.
- [ ] Motion has a purpose and fallback.
- [ ] Source claims are attributed when reporting research; design advice is paraphrased rather than copied from transcripts.
