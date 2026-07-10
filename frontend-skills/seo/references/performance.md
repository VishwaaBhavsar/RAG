# Performance — Core Web Vitals, Images, Scripts, Rendering

## Core Web Vitals Targets

| Metric | Target | What to watch |
|--------|--------|---------------|
| LCP (Largest Contentful Paint) | < 2.5s | Hero images, server response time |
| INP (Interaction to Next Paint) | < 200ms | JS bundle size, event handlers |
| CLS (Cumulative Layout Shift) | < 0.1 | Missing image dimensions, dynamic content |

---

## Image Optimization

Always use `next/image` instead of `<img>`. It auto-compresses, serves WebP/AVIF, and lazy-loads.

```tsx
import Image from 'next/image'

// Fixed size
<Image
  src="/hero.jpg"
  alt="Hero banner showing product dashboard"
  width={1200}
  height={600}
  priority           // use on above-the-fold / LCP images
/>

// Fill container (responsive)
<div className="relative h-64 w-full">
  <Image
    src="/cover.jpg"
    alt="Blog post cover"
    fill
    className="object-cover"
    sizes="(max-width: 768px) 100vw, 50vw"
  />
</div>
```

### Rules for images

- Add `priority` on the hero/LCP image — disables lazy-loading for that image
- Always provide `width` + `height` (or `fill`) to avoid CLS
- Always set `alt` — required for accessibility and SEO
- For external images, add the domain to `next.config.js`:

```js
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.example.com' },
    ],
  },
}
```

---

## Rendering Strategy Selection

```
Public content, rarely changes  → SSG (getStaticProps / export const dynamic = 'force-static')
Public content, updates hourly  → ISR (export const revalidate = 3600)
Personalized / auth-gated       → SSR (getServerSideProps / async Server Component)
Client-only (no SEO needed)     → Client Component with useEffect
```

### App Router

```tsx
// ISR — revalidate every hour
export const revalidate = 3600

// Force static
export const dynamic = 'force-static'

// Force SSR
export const dynamic = 'force-dynamic'
```

### Pages Router

```tsx
// SSG
export async function getStaticProps() {
  const data = await fetch('...')
  return { props: { data }, revalidate: 3600 } // ISR
}

// SSR
export async function getServerSideProps(context) {
  const data = await fetch('...')
  return { props: { data } }
}
```

**Pitfall:** Client-only data fetching (`useEffect + fetch`) means crawlers see empty HTML. Always use server-side fetching for indexable content.

---

## Script Loading

```tsx
import Script from 'next/script'

// Non-critical third-party (analytics, chat widgets)
<Script src="https://widget.example.com/embed.js" strategy="lazyOnload" />

// After hydration (e.g. Google Analytics)
<Script src="https://gtag..." strategy="afterInteractive" />

// Critical inline script
<Script id="theme-init" strategy="beforeInteractive">
  {`document.documentElement.setAttribute('data-theme', localStorage.getItem('theme') || 'light')`}
</Script>
```

Never place blocking `<script>` tags in `<Head>` — use `next/script` with appropriate strategy.

---

## Font Loading

```tsx
// app/layout.tsx — zero layout shift, self-hosted
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], display: 'swap' })

export default function RootLayout({ children }) {
  return <html className={inter.className}>{children}</html>
}
```

---

## Web Vitals Monitoring

```tsx
// app/layout.tsx (App Router)
'use client'
import { useReportWebVitals } from 'next/web-vitals'

export function WebVitals() {
  useReportWebVitals((metric) => {
    // Send to your analytics endpoint
    console.log(metric)
  })
  return null
}

// pages/_app.tsx (Pages Router)
export function reportWebVitals(metric) {
  console.log(metric)
}
```

---

## Caching Headers

```js
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ]
  },
}
```

---

## Lighthouse Audit Checklist

Run `npx lighthouse <url> --view` or use Chrome DevTools → Lighthouse tab.

- [ ] LCP image uses `priority` prop
- [ ] All images have `width` + `height` or `fill`
- [ ] No render-blocking scripts in `<head>`
- [ ] Fonts use `next/font` (eliminates FOUT)
- [ ] JS bundle split with `dynamic(() => import('./HeavyComponent'))` for below-fold content
- [ ] `next build` output shows no oversized chunks (> 500KB)
