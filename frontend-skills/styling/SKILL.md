---
name: styling
description: Provides the correct Tailwind CSS v4 class patterns, design tokens, and color variables for this project. Use this skill when writing any className, applying spacing/colors/typography, or composing layouts — it ensures styles use the project's design system instead of arbitrary values.
---

# Styling Skill

> Tailwind CSS v4 patterns and design tokens for `apps/frontend/`

## ⚠️ Required Workflow

1. **Read this skill doc** before starting
2. Create/modify styles and components
3. **Run through Code Review Checklist** (REQUIRED - see below)
4. Fix any issues found
5. Report completion

---

## Key Files

| File | Purpose |
|------|---------|
| `apps/frontend/src/utils/cn.ts` | `cn()` utility for class composition |
| `apps/frontend/src/app/global.css` | Theme colors, CSS variables, custom utilities |

---

## Rules

1. **Margin at usage site** - Use `space-y-*` or `gap-*` on parent, never margin inside reusable components
2. **Semantic colors only** - Add colors to `global.css` first, then use token names (`text-success`, not `text-green-500`)
3. **Dark mode via tokens** - Use `bg-background`, `text-foreground` etc. They adapt automatically.
4. **Clickable affordance required** - Any clickable non-disabled element (`button`, `a`, tab trigger, card trigger, icon action) must include clear affordance: at minimum `cursor-pointer` + visible hover/focus styles.
5. **Small-screen alignment first** - Build and verify alignment at 320-375px before adding `sm:`/`md:`/`lg:` overrides.
6. **Toolbar overflow prevention** - For action rows/toolbars, default to `flex-wrap` on mobile and avoid fixed-width items that cause overflow.

---

## cn() Utility

```tsx
import { cn } from '@/utils/cn';

const className = cn(
  'base-styles',
  isActive && 'active-styles',
  variant === 'danger' && 'text-destructive',
  className, // Allow prop override
);
```

---

## Design Tokens

Defined in `apps/frontend/src/app/global.css`

### Colors

| Token | Usage |
|-------|-------|
| `text-foreground` | Primary text |
| `text-muted-foreground` | Secondary/subtle text |
| `text-primary` | Brand/accent text |
| `text-destructive` | Error/danger |
| `text-success` | Success |
| `text-warning` | Warning |
| `bg-background` | Page background |
| `bg-card` | Card background |
| `bg-muted` | Subtle background |
| `bg-primary` | Brand/accent background |
| `border-border` | Default border |

Use opacity modifiers: `bg-primary/10`, `border-border/50`

### Custom Utilities (from global.css)

| Class | Effect |
|-------|--------|
| `glass` | Glass morphism effect |
| `gradient-text` | Gradient text using primary colors |
| `glow` | Box shadow glow |
| `gradient-card-{color}` | Blue/orange/green/purple gradient backgrounds |

---

## Quick Reference

```tsx
// Spacing: size-4 for equal w/h, gap-4 for spacing, p-4 for padding
<Icon className="size-4" />
<div className="flex gap-4 p-4">...</div>

// Shadows: shadow-sm → shadow → shadow-md → shadow-lg → shadow-xl
// Radius: rounded-sm → rounded → rounded-md → rounded-lg → rounded-full
```

---

## Mobile-First Design (REQUIRED)

**Always design for mobile first, then scale up.** Write base styles for mobile, add breakpoint prefixes for larger screens. **Breakpoints, mobile-first pattern, and common responsive patterns:** see [Responsive Design](references/tailwind-patterns.md#responsive-design) in tailwind-patterns.md.

### Mobile Alignment Guardrails (REQUIRED)

- Use `flex-1 min-w-0` on text/content columns in horizontal rows.
- Add `truncate` for single-line labels in constrained rows.
- Use `w-full sm:w-auto` for stacked-to-inline action controls.
- In dense control rows, prefer `justify-start` on mobile and `sm:justify-between` for wider screens.
- For fixed bottom bars, ensure content wraps with `flex-wrap` and keep CTA controls reachable above mobile nav.

### Clickable Cursor Policy (REQUIRED)

- Add `cursor-pointer` to interactive elements unless native behavior is intentionally overridden.
- Keep disabled elements non-clickable with `disabled:cursor-not-allowed`.
- If a container is clickable, do not rely on nested text/icon only; make the clickable root visibly interactive.

---

**Container centering and all ways to center content (Tailwind v4):** see [Centering content](references/tailwind-patterns.md#centering-content-tailwind-v4) in tailwind-patterns.md.

---

## Code Review Checklist

**⚠️ MANDATORY: Do NOT consider the task complete until you have verified ALL items below.**

Before completing any styling work, verify:

- [ ] **Container centering**: All `<section>`, `<nav>`, `<footer>`, `<header>` with `.container` have `flex items-center justify-center`
- [ ] **Semantic colors**: Using `text-foreground`, `bg-background` etc., not hardcoded colors like `text-gray-900`
- [ ] **No @import url()**: Don't use `@import url()` in CSS - use `next/font/google` in layout.tsx instead (see [typography.md](references/typography.md))
- [ ] **Design tokens**: Using `p-4`, `gap-4` etc., not arbitrary values like `p-[16px]`
- [ ] **Theme consistency**: New colors added to `global.css` CSS variables, not inline
- [ ] **Responsive design**: Test on mobile (375px), tablet (768px), and desktop (1280px+) breakpoints
- [ ] **Narrow mobile pass**: Test at 320px and verify no overlap, clipping, or horizontal scroll
- [ ] **Responsive classes**: Use `sm:`, `md:`, `lg:` prefixes for breakpoint-specific styles
- [ ] **No mobile overflow**: Flex toolbars: `flex-1 min-w-0` + `truncate`; icons `shrink-0`. [tailwind-patterns.md#flex-row-overflow](references/tailwind-patterns.md#flex-row-overflow)
- [ ] **Clickable affordance**: Every clickable item has `cursor-pointer` and visible hover/focus feedback

### Enforcement Rules

- [ ] **STOP** before saying "Done" - run through the checklist first
- [ ] **READ** the actual code you wrote, don't assume it's correct
- [ ] **FIX** issues immediately, don't defer to user

If you skip this step, the user will have to fix issues manually.

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| `text-gray-900 bg-white` | `text-foreground bg-background` |
| Margin inside components | `space-y-*` on parent |
| `p-[16px]` arbitrary values | `p-4` design tokens |
| `sm:p-2 md:p-3 lg:p-4 xl:p-5` | `p-4 md:p-6 lg:p-8` |

---

## References

| Topic | File |
|-------|------|
| Layout, flex, grid, centering, z-index | [tailwind-patterns.md](references/tailwind-patterns.md) |
| Font sizes, weights, headings | [typography.md](references/typography.md) |
| Transitions, animations, hover | [`animation` skill](../animation/SKILL.md) → [`references/tailwind-animations.md`](../animation/references/tailwind-animations.md) |
