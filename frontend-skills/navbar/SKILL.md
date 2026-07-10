---
name: navbar
description: Build responsive navbars with animated hamburger menus for public/landing pages. Use this skill when adding a navbar, mobile menu, hamburger toggle, or responsive navigation to any page outside (auth) or (private) routes.
triggers:
  - navbar
  - navigation
  - hamburger
  - mobile menu
  - mobile nav
  - responsive nav
  - responsive navbar
  - mobile navigation
  - nav menu
  - header nav
---

# Navbar Skill

> Responsive, scroll-aware navbar with animated hamburger drawer for public/marketing pages.
> All animation patterns live in the `animation` skill → `references/navbar.md` (single source of truth).
> This skill is the orchestrator — it decides which path to follow and enforces the rules.

---

## 🚨 MANDATORY — Read Before Writing Any Code

**Invoke this skill FIRST whenever the user asks for:**

`navbar`, `navigation`, `hamburger`, `mobile menu`, `mobile nav`,
`responsive nav`, `responsive navbar`, `header nav`, `nav menu`

**DO NOT write a single line of navbar code before completing steps 1–3.**

---

## ⚠️ Required Workflow

1. **Invoke this skill** via the Skill tool — `skill: "navbar"` — before any implementation
2. **Check if `framer-motion` is installed** — `grep "framer-motion" package.json`
   - ✅ Installed → follow **Skills 1–6** in `animation` skill → `references/navbar.md`
   - ❌ Not installed → follow **Skills 7–11** in `animation` skill → `references/navbar.md`
3. **Read `animation` skill → `references/navbar.md`** — contains all patterns for both paths
4. Apply semantic color tokens from `styling` skill — never hardcode colors
5. Implement following the patterns
6. **Run Code Review Checklist** (REQUIRED — see below)
7. Fix any issues found

---

## When to Use This Skill

| Scenario | Action |
|----------|--------|
| Landing / marketing / public page | ✅ Use this skill |
| Any page outside `(auth)` and `(private)` routes | ✅ Use this skill |
| `(private)` dashboard topbar or sidebar | ❌ Use existing dashboard layout components |
| `(auth)` login / signup header | ❌ Keep minimal — no nav needed |

---

## Key Files

| File | Purpose |
|------|---------|
| `animation` skill → `references/navbar.md` | All animation patterns — Framer Motion (Skills 1–6) and CSS-only (Skills 7–11) |
| `src/app/landing/_components/LandingPage.tsx` | Reference implementation in this project |
| `src/app/globals.css` | Design tokens — `bg-background`, `text-foreground`, etc. |
| `src/lib/utils.ts` | `cn()` for conditional class composition |
| `src/middleware.ts` | Register new public routes under `isPublicPage` |

---

## Cross-Skill Dependencies

| Need | Skill | Reference |
|------|-------|-----------|
| All navbar animation patterns (Framer Motion + CSS-only) | `animation` | `references/navbar.md` |
| `cn()` + semantic color tokens | `styling` | `references/tailwind-patterns.md` |
| Button / Link styles | `styling` | `references/tailwind-patterns.md` |

---

## Rules

1. **`'use client'`** — navbar always needs state (scroll listener, menu open); always a client component
2. **Framer Motion: `AnimatePresence` wraps icon swap and drawer** — never conditionally render without exit animation
3. **Framer Motion: `mode="wait"` + `initial={false}` on icon swap** — clean sequential swap, no animation on first render
4. **Framer Motion: bezier ease typed as 4-tuple** — `[number, number, number, number]`, not `number[]` (v12 strict types)
5. **Framer Motion: drawer is sibling to `<nav>`, not child** — `position: fixed` inside `<nav>` can clip
6. **CSS-only: `grid-rows-[0fr→1fr]` for drawer height** — never animate `height` directly (layout reflow)
7. **CSS-only: `pointer-events-none` when drawer closed** — prevents invisible links from being interactive
8. **Both paths: lock body scroll when drawer is open** — `document.body.style.overflow = 'hidden'`; cleanup in `useEffect` return
9. **Both paths: backdrop closes drawer on tap** — always render a full-screen overlay with `onClick`
10. **Both paths: apply frosted bg when `menuOpen` even if not scrolled** — nav must be readable behind the open drawer
11. **Both paths: primary CTA always visible on mobile** — never hide the conversion action behind the hamburger
12. **Both paths: all links/CTAs inside drawer call `setMenuOpen(false)`** — no stale open state after navigation
13. **Both paths: passive scroll listener** — `addEventListener('scroll', handler, { passive: true })`
14. **Register route in `src/middleware.ts`** under `isPublicPage` for any new public page using this navbar
15. **All nav destinations must be functional** — every nav item points to an existing route or valid section anchor present on the page
16. **No inert nav controls** — avoid placeholder links/buttons that do not navigate or update state

---

## Code Review Checklist

**⚠️ MANDATORY: Do NOT consider the task complete until verified.**

- [ ] **`'use client'`** at the top of the navbar file
- [ ] **Scroll listener cleanup** — `removeEventListener` in `useEffect` return
- [ ] **Body scroll locked** — `overflow = 'hidden'` when `menuOpen === true`
- [ ] **Body scroll cleanup** — `useEffect` return resets `overflow = ''`
- [ ] **Backdrop rendered** behind the drawer, full-screen, closes on click
- [ ] **CTA always visible on mobile** — not hidden behind hamburger
- [ ] **All links/CTAs inside drawer** call `setMenuOpen(false)` on click
- [ ] **Semantic color tokens** — `text-foreground`, `bg-background`, not hardcoded values
- [ ] **Route in `middleware.ts`** — added to `isPublicPage` if this is a new public page
- [ ] **Mobile tested at 375px** — drawer doesn't overflow viewport
- [ ] **Nav destinations verified** — each item navigates to a real route/section (no broken or dead targets)
- [ ] **No placeholder nav actions** — all nav controls have real behavior

### Framer Motion only
- [ ] **`AnimatePresence`** wraps both icon swap and drawer+backdrop
- [ ] **`mode="wait"` + `initial={false}`** on icon swap `AnimatePresence`
- [ ] **Drawer outside `<nav>`** — sibling in a fragment `<>`
- [ ] **Bezier ease is a typed 4-tuple** — `const EASE: [number, number, number, number]`

### CSS-only only
- [ ] **`grid-rows-[0fr]` → `grid-rows-[1fr]`** for drawer — never animate `height` directly
- [ ] **`overflow-hidden` wrapper** inside the grid div
- [ ] **`pointer-events-none`** on drawer and backdrop when `menuOpen === false`
