# Font Optimization

Use `next/font` for automatic font optimization with zero layout shift.

## Google Fonts

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  )
}
```

## Multiple Fonts

```tsx
import { Inter, Roboto_Mono } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

const robotoMono = Roboto_Mono({
  subsets: ['latin'],
  variable: '--font-roboto-mono',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${robotoMono.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

Configure in Tailwind v4:

```css
/* app/globals.css */
@import 'tailwindcss';

@theme {
  --font-sans: var(--font-inter);
  --font-mono: var(--font-roboto-mono);
}
```

Use in components:

```tsx
<p className="font-sans">Uses Inter font</p>
<code className="font-mono">Uses Roboto Mono font</code>
```

## Font Weights and Styles

```tsx
// Single weight
const inter = Inter({
  subsets: ['latin'],
  weight: '400',
})

// Multiple weights
const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '700'],
})

// Variable font (recommended) - includes all weights
const inter = Inter({
  subsets: ['latin'],
  // No weight needed - variable fonts support all weights
})

// With italic
const inter = Inter({
  subsets: ['latin'],
  style: ['normal', 'italic'],
})
```

## Tailwind CSS v4 Integration

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
})

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body>{children}</body>
    </html>
  )
}
```

```css
/* app/globals.css */
@import 'tailwindcss';

@theme {
  --font-sans: var(--font-inter);
}
```

Use in components:

```tsx
<p className="font-sans">Uses Inter font</p>
```

## Preloading Subsets

Only load needed character subsets:

```tsx
// Latin only (most common)
const inter = Inter({ subsets: ['latin'] })

// Multiple subsets
const inter = Inter({ subsets: ['latin', 'latin-ext', 'cyrillic'] })
```

## Display Strategy

Control font loading behavior:

```tsx
const inter = Inter({
  subsets: ['latin'],
  display: 'swap', // Default - shows fallback, swaps when loaded
})

// Options:
// 'auto' - browser decides
// 'block' - short block period, then swap
// 'swap' - immediate fallback, swap when ready (recommended)
// 'fallback' - short block, short swap, then fallback
// 'optional' - short block, no swap (use if font is optional)
```

## Don't Use Manual Font Links

Always use `next/font` instead of `<link>` tags for Google Fonts.

```tsx
// Bad: Manual link tag (blocks rendering, no optimization)
<link href="https://fonts.googleapis.com/css2?family=Inter" rel="stylesheet" />

// Good: Use next/font (self-hosted, zero layout shift)
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })
```

## Common Mistakes

```tsx
// Bad: Importing font in every component
// components/Button.tsx
import { Inter } from 'next/font/google'
const inter = Inter({ subsets: ['latin'] }) // Creates new instance each time!

// Good: Import once in layout, use CSS variable
// app/layout.tsx
const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

// Bad: Using @import in CSS (blocks rendering)
/* globals.css */
@import url('https://fonts.googleapis.com/css2?family=Inter');

// Good: Use next/font (self-hosted, no network request)
import { Inter } from 'next/font/google'

// Note: Variable fonts (like Inter) efficiently include all weights in one file
// Only specify weights for non-variable fonts to reduce bundle size
const roboto = Roboto({ subsets: ['latin'], weight: ['400', '700'] })

// Bad: Missing subset - loads all characters
const inter = Inter({})

// Good: Always specify subset
const inter = Inter({ subsets: ['latin'] })
```

## Font in Specific Components

```tsx
// For component-specific fonts, export from a shared file
// lib/fonts.ts
import { Inter, Playfair_Display } from 'next/font/google'

export const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
export const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' })

// components/Heading.tsx
import { playfair } from '@/lib/fonts'

export function Heading({ children }: { children: React.ReactNode }) {
  return <h1 className={playfair.className}>{children}</h1>
}
```
