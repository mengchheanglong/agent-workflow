# UI Component Libraries

Curated libraries of production-ready React/Next.js components with code.

---

## ⭐ PRIMARY Sources (go through these first)

These two are the most important references for this workflow. Always check here first.

### shadcn UI Kit (Admin Dashboard)
- **URL:** https://shadcnuikit.com
- **Admin Dashboard:** https://shadcnuikit.com/admin-dashboard
- **Description:** 12-15 production-ready admin dashboards, 10-17 web apps, 30-40+ subpages built on shadcn/ui.
- **Use for:** CRM, e-commerce, sales, finance, crypto, project management, file manager, hospital management, academy, analytics, HR, real estate, hotel dashboards.
- **Also includes:** 100+ reusable components, marketing blocks (hero sections, CTA, changelog, pricing, features, testimonials, team, integrations, newsletter, contact, how it works, stats, FAQs, footers, navbars), e-commerce blocks (checkout, product list, product category, product details, product features).
- **Stack:** Next.js 16 + React 19 + Tailwind CSS v4 + TypeScript + Recharts + TanStack Table + Zod + React Hook Form.
- **Why primary:** Most comprehensive pre-built UI for admin + marketing + e-commerce. Launch projects faster.

### Atlassian Design System
- **URL:** https://atlassian.design
- **Components:** https://atlassian.design/components
- **Description:** 60+ production components from Atlassian with usage guidelines, design tokens, and accessibility standards.
- **Use for:** Forms (Button, Checkbox, Radio, Select, Text field, Textarea, Toggle), Layout (Page, Panel, Grid, Stack, Inline, Flex), Navigation (Breadcrumbs, Tabs, Pagination), Messaging (Banner, Modal, Tooltip, Empty state, Flag, Section message), Status (Badge, Lozenge, Progress bar, Progress indicator, Spinner, Skeleton), Primitives (Box, Pressable, Anchor, Inline, Stack, Flex, Grid, Bleed, Text, MetricText, Focusable).
- **Also includes:** Design tokens (color, typography, elevation, spacing), iconography, motion utilities, CSS-in-JS (XCSS), accessibility guide, Figma Motion integration.
- **Why primary:** Best reference for interaction patterns, when to use which component, enterprise-grade UX guidelines. Use as UX authority.
- **Do NOT:** Copy Atlassian's visual styling or install Atlaskit packages. Use only as UX reference.

---

## Secondary Sources (check after primary)

Use these for additional inspiration, specific components, or when primary sources don't cover the need.

## Magic UI
- **URL:** https://magicui.design
- **Description:** 150+ free animated components with React, TypeScript, Tailwind CSS, and Motion (Framer Motion). Perfect companion for shadcn/ui.
- **Use for:** Landing page animations, text effects, background effects, buttons.
- **Notable components:** Meteors, Text Animate, Text Reveal, Animated Beam, Shine Border, Magic Card, Retro Grid, Ripple.
- **Install:** `pnpm dlx shadcn@latest add @magicui/<component>`

### Specific Magic UI components for this workflow:
| Component | URL | Use |
|-----------|-----|-----|
| Meteors | https://magicui.design/docs/components/meteors | Additional animation style for some component |
| Text Animate | https://magicui.design/docs/components/text-animate | Text animation for some part |
| Text Reveal | https://magicui.design/docs/components/text-reveal | Text reveal for some part |

## Aceternity UI
- **URL:** https://ui.aceternity.com
- **Description:** 200+ production-ready components, blocks, and templates. Copy-paste, customize, and ship.
- **Use for:** Hero sections, bento grids, feature sections, navbars, footers, pricing, testimonials.
- **Notable components:** Hero Parallax, Bento Grid, Floating Dock, Lamp Effect, Macbook Scroll, Moving Border, Sparkles, Text Generate Effect.
- **Stack:** React + Tailwind CSS + Framer Motion

## Uiverse
- **URL:** https://uiverse.io
- **Description:** Largest library of open-source UI elements. Copy as HTML/CSS, Tailwind, React, and Figma.
- **Use for:** Buttons, cards, loaders, inputs, toggles, checkboxes, tooltips, patterns, glassmorphism.
- **Browse by:** Loading UI, Button Effects, Card Components, Modern Styles (glassmorphism, neumorphism, dark mode), Forms & Inputs.
- **Stats:** 7,400+ elements, 360,000+ contributors, 100% free.

## shadcn/ui
- **URL:** https://ui.shadcn.com (also https://shadcn.com)
- **Description:** Built on Radix UI + Tailwind CSS. Copy and paste. Accessible, customizable, open-source.
- **Use for:** Forms, buttons, dialogs, dropdowns, navigation, data display — foundational building blocks.
- **Install:** `npx shadcn@latest add <component>`
- **Primitives:** https://www.radix-ui.com
