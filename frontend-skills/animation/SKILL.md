---
name: animation
description: Add animations to the frontend using Framer Motion v12 and Tailwind CSS v4. Use this skill for component entry animations, scroll-triggered animations, hover effects, button interactions, page transitions, stagger animations, loading states, layout animations, performance optimization, and responsive animations.
triggers:
  - animation
  - animations
  - animate
  - animated
  - transition
  - motion
  - scroll reveal
  - scroll animation
  - fade in
  - fade out
  - hover effect
  - stagger
  - page transition
  - entry animation
  - loading animation
  - floating
  - parallax
  - typewriter
  - count up
---

# Animation Skill

> **Primary:** Framer Motion **v12.38.0** (installed) for interactive, complex, and sequence animations.
> **Secondary:** Tailwind CSS + keyframes for simple hover/transition effects and loading states.

---

## Framer Motion Version

**`framer-motion` v12.38.0 is installed in this project.** Do not check for installation.

### v12 Breaking Changes — Read Before Writing Any Animation Code

| Change | Wrong (pre-v12) | Correct (v12) |
|--------|----------------|---------------|
| Bezier ease array | `ease: [0.4, 0, 0.2, 1]` (inferred `number[]`) | `ease: [0.4, 0, 0.2, 1] as const` or type as `[number, number, number, number]` |
| Function variants | `visible: (i) => ({ ... })` assigned to `Variants` type | Cast with `as Variants` or avoid assigning to `Variants` directly |
| `useInView` | from external lib | from `'framer-motion'` directly |
| Spring params | `stiffness`, `damping` only | Also supports `visualDuration` + `bounce` shorthand |
| Imperative animate | not available | `import { animate } from 'framer-motion'` |
| Scroll utility | not available | `import { scroll } from 'framer-motion'` |

**Always declare bezier ease as a typed 4-tuple:**
```tsx
const EASE: [number, number, number, number] = [0.4, 0, 0.2, 1]
// or inline:
transition={{ ease: [0.4, 0, 0.2, 1] as const }}
```

---

## Required Workflow

1. **Invoke this skill via the Skill tool** — `skill: "animation"` — before any implementation
2. **Read `references/framer-motion.md`** — framer-motion v12 is already installed; use it for all complex animations
3. **Read the relevant reference files** based on what animations are needed (see Reference table below)
4. Decide: Framer Motion or Tailwind CSS? (see decision table below)
5. Check existing tokens in `references/tailwind-animations.md` — **never add keyframes to a new CSS file**
6. Implement animation following the reference patterns
7. **Run through Code Review Checklist** (REQUIRED — see below)
8. Fix any issues found

---

## Framer Motion vs Tailwind — When to Use Which

| Use Framer Motion | Use Tailwind CSS |
|-------------------|-----------------|
| Page transitions (`AnimatePresence`) | Simple hover color / shadow change |
| Exit animations (modal close, toast dismiss) | Loading spinner (`animate-spin`) |
| Stagger list/grid reveals (`staggerChildren`) | Skeleton (`animate-pulse`) |
| Shared layout animations (`layoutId`) | Accordion expand (`animate-accordion-*`) |
| Scroll-driven animations (`useScroll`) | One-time entry (`animate-fade-in`) |
| Gesture interactions (drag, swipe) | Basic `active:scale-95` button press |
| Orchestrated sequences | Static CSS transitions |
| Responsive navbar (hamburger + drawer) — **if installed** | Responsive navbar (hamburger + drawer) — **if NOT installed** |

---

## Project File Locations

| What | File |
|------|------|
| Custom keyframes + animation tokens | `apps/frontend/src/app/global.css` → `@theme` block |
| Custom utility classes | `apps/frontend/src/app/global.css` → `@layer utilities` |
| `cn()` for conditional animation classes | `apps/frontend/src/utils/cn.ts` |

---

## Cross-Skill Dependencies

| Need | Use |
|------|-----|
| Existing Tailwind animation tokens (`animate-fade-in` etc.) | `styling` skill → `references/animations.md` |
| `transition-*`, `duration-*`, `motion-reduce:` classes | `styling` skill → `references/animations.md` |
| How to add new keyframe to `global.css` | `styling` skill → `references/animations.md` |
| `Skeleton`, `Button`, `ButtonWithLoader` components | `components` skill |
| Design tokens, `cn()` utility | `styling` skill |
| Responsive navbar — Framer Motion or CSS-only | `navbar` skill + `references/navbar.md` (this skill) |

---

## Reference

| File | Read when |
|------|-----------|
| `references/framer-motion.md` | Page transitions, exit animations, stagger, layout, gestures, scroll — all Framer Motion patterns |
| `references/entry-scroll.md` | CSS-only entry animations, `useInView` hook (when Framer Motion not yet installed) |
| `references/hover-button.md` | Hover card/link patterns, button press interactions (Tailwind + Framer Motion) |
| `references/page-layout.md` | Page transitions, expand/collapse, drawer slide |
| `references/stagger.md` | CSS-only stagger (fallback when Framer Motion not available) |
| `references/loading.md` | Progress bars, loading dots, which loading pattern to use |
| `references/performance-responsive.md` | GPU hints, `will-change`, responsive animation, reduced motion |
| `references/navbar.md` | Responsive navbar with animated hamburger — Framer Motion path (→ `navbar` skill) **or** CSS-only slider fallback |

---

## Code Review Checklist

**⚠️ Do NOT consider the task complete until verified.**

- [ ] **`AnimatePresence` wraps exit animations** — modals, toasts, conditional renders
- [ ] **Reduced motion handled** — `useReducedMotion()` or `motion-reduce:`
- [ ] **Only `transform`/`opacity` animated** — no layout-reflow properties
- [ ] **`cn()` used** for conditional Tailwind class logic
- [ ] **New keyframes in `global.css` `@theme`** — not inline, not a separate file
- [ ] **Correct component imports** — `Skeleton`, `ButtonWithLoader` from `@/components`
- [ ] **Subtle animations in `(private)` dashboard** — no distracting motion in productivity UI
- [ ] **Mobile tested** — no jank at 375px; reduce or disable heavy animations
