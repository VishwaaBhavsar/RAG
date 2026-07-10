---
name: accessibility
description: Audits and enforces WCAG 2.1 AA compliance for any UI element. Use this skill when building components, forms, modals, interactive elements, or any user-facing page — it covers semantic HTML, keyboard navigation, ARIA attributes, focus management, color contrast, and screen reader announcements.
---

# Accessibility — Next.js / React

> Act as an Accessibility Expert. Audit and enforce WCAG 2.1 AA compliance on every UI task.

---

## Auto-Trigger Rules

**Invoke this skill automatically — WITHOUT user saying "accessible" — when:**

- Creating or modifying any React component or page
- Adding forms, inputs, buttons, or interactive elements
- Building modals, dialogs, drawers, dropdowns, or popovers
- Writing any clickable/interactive UI element
- Adding dynamic content that updates without page reload
- Creating navigation, menus, or route-level pages

---

## Core Rules (Non-Negotiable)

| # | Rule | Quick Check |
|---|------|-------------|
| 1 | Use semantic HTML — `<button>`, `<nav>`, `<main>`, `<section>`, `<article>` | No `<div onClick>` |
| 2 | All images need `alt` — decorative images use `alt=""` | No bare `<img>` without alt |
| 3 | Every interactive element is keyboard reachable and operable | Tab + Enter/Space works |
| 4 | One `<h1>` per page; headings in strict order (h1→h2→h3) | No skipped levels |
| 5 | All form inputs have associated `<label>` or `aria-label` | `htmlFor` matches input `id` |
| 6 | Dynamic content changes announced via `aria-live` | Toasts, alerts, async results |
| 7 | ARIA only when native HTML semantics are insufficient | No redundant `role="button"` on `<button>` |
| 8 | Sufficient color contrast — 4.5:1 normal text, 3:1 large text | Use design tokens, not arbitrary colors |
| 9 | Focus trapped inside modals; restored to trigger on close | `FocusTrap` or `Dialog` component |
| 10 | Route changes announce page title or new content to SR | Use `aria-live` region or router hook |
| 11 | Interactive affordance is visible | Clickable controls show pointer + hover/focus state |

---

## Quick Patterns

### Interactive Elements

```tsx
// CORRECT
<button type="button" onClick={handleClick} className="cursor-pointer hover:bg-muted">Save</button>
<a href="/path" className="cursor-pointer hover:underline">Go to page</a>

// WRONG — never do this
<div onClick={handleClick}>Save</div>
<span onClick={handleClick} role="button">Click me</span>
```

### Images

```tsx
// Meaningful image
<Image src={logo} alt="Company logo" />

// Decorative image — empty string, NOT omitted
<Image src={divider} alt="" aria-hidden="true" />
```

### Form Labels

```tsx
// CORRECT — explicit label
<label htmlFor="email">Email address</label>
<input id="email" type="email" />

// CORRECT — aria-label when visual label is absent
<input type="search" aria-label="Search records" />

// WRONG — no label
<input type="email" placeholder="Email" />
```

### Heading Hierarchy

```tsx
// CORRECT
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>

// WRONG — skipped level
<h1>Page Title</h1>
  <h3>Section</h3>
```

### Dynamic Content (aria-live)

```tsx
// Status updates, toasts, async results
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Critical alerts (interrupts)
<div role="alert">
  {errorMessage}
</div>
```

### Focus Management in Modals

```tsx
// Dialog component handles trap + restore automatically
// If building custom: restore focus on close
const triggerRef = useRef<HTMLButtonElement>(null);

const handleClose = () => {
  setOpen(false);
  triggerRef.current?.focus(); // restore focus
};
```

### Skip Navigation

```tsx
// Add once at root layout — lets keyboard users skip nav
<a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 bg-white px-4 py-2 rounded">
  Skip to main content
</a>
<main id="main-content">...</main>
```

---

## Mandatory Checklist

**STOP before saying "Done" — verify ALL items:**

- [ ] No `<div onClick>` or `<span onClick>` — replaced with `<button>` or `<a>`
- [ ] All `<img>` / `<Image>` have `alt` (empty string for decorative)
- [ ] All form inputs have `<label htmlFor>` or `aria-label`
- [ ] Heading levels are sequential — no skipped levels
- [ ] Keyboard navigation works: Tab, Shift+Tab, Enter, Space, Escape
- [ ] Clickable items have clear affordance (`cursor-pointer` + visible hover/focus style)
- [ ] Dynamic updates use `aria-live="polite"` or `role="alert"`
- [ ] Modals trap focus and restore on close
- [ ] Color choices use design tokens with verified contrast ratios
- [ ] ARIA attributes used only where native HTML is insufficient
- [ ] `sr-only` used for screen-reader-only text (not `display:none`)

---

## ARIA Usage Guide

```tsx
// Use ARIA only when HTML semantics can't express the role

// GOOD — native semantics
<button aria-expanded={isOpen} aria-controls="menu-list">Toggle</button>
<ul id="menu-list" role="menu">...</ul>

// GOOD — status region
<div aria-live="polite" role="status">{loadingStatus}</div>

// BAD — redundant ARIA
<button role="button">Click</button>   // role="button" is redundant
<h2 aria-level="2">Title</h2>         // aria-level is redundant on <h2>

// BAD — hiding content from keyboard but not screen reader
<div aria-hidden="false" tabIndex={-1}>...</div>
```

---

## Cross-Skill Dependencies

| Need | Use skill |
|------|-----------|
| Landmark regions, heading hierarchy, semantic elements | `seo` skill → `references/semantic-html.md` |
| Design tokens, `sr-only`, focus ring utilities, animations | `styling` skill |
| Accessible component primitives (Dialog, Button, AlertDialog) | `components` skill |
| Translated `aria-label` / screen-reader text | `translation` skill |
| Image optimization (`next/image`, `alt`, `sizes`) | `next-best-practices` → `image.md` |

---

## References (load only when needed)

| File | Load when... |
|------|--------------|
| `references/semantic-html.md` | Choosing correct HTML element, table scope, multiple navs |
| `references/keyboard-focus.md` | Focus rings, tab order, focus trapping, skip link, route focus |
| `references/aria.md` | ARIA roles, states, properties — when and how to use |
| `references/forms.md` | Label association, validation errors, fieldsets, required fields |
| `references/dynamic-content.md` | `aria-live`, `role="alert"`, toasts, SPA route announcements |
| `references/color-contrast.md` | WCAG contrast ratios, failure patterns, testing tools |

---

## Audit Tools

```bash
npm run lint  # eslint-plugin-jsx-a11y catches violations at build time

# Manual audit:
# 1. Keyboard-only — Tab through entire page without mouse
# 2. Screen reader — VoiceOver (Mac: Cmd+F5), NVDA (Windows), TalkBack (Android)
# 3. axe DevTools browser extension — zero violations target
# 4. Lighthouse → Accessibility tab — target score 95+
# 5. Color contrast — Chrome DevTools Elements → Accessibility → contrast ratio
```

---

## Rules

1. Never use `<div>` or `<span>` for interactive elements — always `<button>` or `<a>`
2. Never omit `alt` on images — empty string `alt=""` for decorative
3. Never skip heading levels — h1 → h2 → h3 in strict order
4. Never use `aria-hidden="true"` on focusable elements
5. Never use `tabIndex > 0` — breaks natural tab order
6. Always associate labels with inputs via `htmlFor` + `id` or `aria-label`
7. Always include `aria-live` region for dynamic status updates
8. Always restore focus when modals, drawers, or popovers close
9. Always verify color contrast before using any custom color
10. Always add `type="button"` to `<button>` inside forms to prevent accidental submit
11. Always provide visible affordance for clickable controls (`cursor-pointer` + hover/focus state)
