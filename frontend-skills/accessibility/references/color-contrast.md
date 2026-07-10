# Color Contrast — Accessibility Reference

> For design tokens (`text-foreground`, `bg-background`, `text-destructive`, etc.) and Tailwind color usage, see the `styling` skill — tokens are already verified for accessible contrast.

---

## WCAG 2.1 AA Requirements

| Text type | Minimum ratio | Target |
|-----------|--------------|--------|
| Normal text (< 18pt / < 14pt bold) | **4.5:1** | 7:1 |
| Large text (≥ 18pt / ≥ 14pt bold) | **3:1** | 4.5:1 |
| UI components & focus indicators | **3:1** | — |
| Decorative elements | exempt | — |
| Disabled elements | exempt | — |

---

## Rules

1. **Always use design tokens** (see `styling` skill) — never arbitrary hex/rgb for text
2. **Never convey information by color alone** — add icon, text, or pattern
3. **Check contrast for all states** — default, hover, focus, disabled, error
4. **Dark mode** — verify contrast in both themes if supported

---

## Common Failure Patterns

```tsx
// Placeholder text — always low contrast, AND not a label replacement
<input placeholder="Full name" />  // fails contrast + missing label

// Arbitrary gray — almost always fails
<p className="text-gray-400">Secondary text</p>   // likely fails 4.5:1
<p style={{ color: '#aaa' }}>Light text</p>       // likely fails

// Error: use semantic token, not arbitrary red
<p className="text-red-300">Invalid email</p>     // fails
<p className="text-destructive">Invalid email</p> // correct
```

---

## Status / State — Never Color-Only

```tsx
// WRONG — color is the only differentiator
<span className="text-green-500">Active</span>
<span className="text-red-500">Inactive</span>

// CORRECT — color + text/icon
<span className="flex items-center gap-1 text-success">
  <CheckCircleIcon className="h-4 w-4" aria-hidden="true" />
  Active
</span>
<span className="flex items-center gap-1 text-destructive">
  <XCircleIcon className="h-4 w-4" aria-hidden="true" />
  Inactive
</span>
```

---

## Focus Ring Contrast

Focus ring must meet 3:1 against the adjacent background. Use `focus-visible:` utilities from the design system — pre-verified.

```tsx
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2">
  Save
</button>
```

---

## Testing Tools

| Tool | How to use |
|------|-----------|
| Chrome DevTools | Elements panel → Accessibility tab → contrast ratio |
| axe DevTools extension | Run audit — flags contrast failures automatically |
| Colour Contrast Analyser (desktop app) | Pick colors from screen — shows exact ratio |
| WAVE browser extension | Shows contrast errors in context |

---

## Checklist

- [ ] All text uses design tokens, not arbitrary colors (see `styling` skill)
- [ ] Normal text ≥ 4.5:1 contrast ratio
- [ ] Large text ≥ 3:1 contrast ratio
- [ ] Focus indicators meet 3:1 against background
- [ ] Status/state not conveyed by color alone — add icon or text
- [ ] Error messages use `text-destructive` token
- [ ] Placeholder is never the sole label (and is low contrast — don't rely on it)
