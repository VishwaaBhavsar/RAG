# Typography

> Font sizes, weights, and text utilities for consistent typography.

---

## Tailwind v4 Note

Tailwind CSS v4 uses CSS variables for font scales. The pixel values below are approximate defaults - actual values are computed at build time. Always test visually rather than relying on exact pixel values.

---

## Font Changes (Next.js)

Use `next/font` for optimized font loading. Never use `@import url()` in CSS.

```tsx
// In layout.tsx - CORRECT approach
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
```

```css
/* In global.css - WRONG (causes Tailwind v4 parsing errors) */
@import url('https://fonts.googleapis.com/css2?family=Inter...');
```

---

## Font Scale & Weight

| Size | Class | Usage | Common Weight |
|------|-------|-------|---------------|
| ~12px | `text-xs` | Captions, badges | `font-medium` |
| ~14px | `text-sm` | Labels, metadata | `font-medium` |
| ~16px | `text-base` | Body text | `font-normal` |
| ~18px | `text-lg` | Card titles | `font-semibold` |
| ~20px | `text-xl` | Section headings | `font-semibold` |
| ~24px | `text-2xl` | Page titles | `font-bold` |
| ~30px | `text-3xl` | Page headings | `font-bold` |
| ~36px+ | `text-4xl`/`5xl` | Hero text | `font-bold` |

---

## Heading Hierarchy

| Element | Classes |
|---------|---------|
| Page Title | `text-2xl font-bold` or `text-3xl font-bold` |
| Section Title | `text-xl font-semibold` |
| Card Title | `text-base font-semibold` or `text-lg font-semibold` |
| Label | `text-sm font-medium` |

---

## Line Height

| Class | Value | Usage |
|-------|-------|-------|
| `leading-tight` | 1.25 | Headings |
| `leading-normal` | 1.5 | Body text (default) |
| `leading-relaxed` | 1.625 | Readable paragraphs |

---

## Text Alignment

| Class | Usage |
|-------|-------|
| `text-left` | Default |
| `text-center` | Empty states, centered content |
| `text-right` | Numbers, prices |

---

## Common Patterns

```tsx
// Page header
<div className="space-y-1">
  <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
  <p className="text-muted-foreground">Manage your account preferences</p>
</div>

// Form label with required indicator
<Label className="text-sm font-medium">
  Email <span className="text-destructive">*</span>
</Label>
```
