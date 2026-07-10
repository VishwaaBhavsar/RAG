# Metadata — Titles, Descriptions, OG Tags, Canonical, Hreflang

## App Router (Next.js 13+)

### Static metadata

```tsx
// app/page.tsx or any layout/page
export const metadata = {
  title: 'Home - Acme Co',
  description: 'Welcome to Acme Co, your source for...',
  alternates: {
    canonical: 'https://example.com/',
  },
  openGraph: {
    title: 'Home - Acme Co',
    description: 'Welcome to Acme Co...',
    url: 'https://example.com/',
    siteName: 'Acme Co',
    images: [{ url: 'https://example.com/og.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Home - Acme Co',
    description: 'Welcome to Acme Co...',
    images: ['https://example.com/og.png'],
  },
}
```

### Title template (set in root layout, override in pages)

```tsx
// app/layout.tsx
export const metadata = {
  title: {
    template: '%s | Acme Co',
    default: 'Acme Co',
  },
  description: 'Acme Co — your source for...',
}

// app/about/page.tsx — renders "About Us | Acme Co"
export const metadata = { title: 'About Us' }
```

### Dynamic metadata (SSR / ISR pages)

```tsx
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await fetchPost(params.slug)
  return {
    title: post.title,
    description: post.excerpt,
    alternates: { canonical: `https://example.com/blog/${params.slug}` },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage }],
    },
  }
}
```

---

## Pages Router

```tsx
// pages/about.tsx
import Head from 'next/head'

export default function About() {
  return (
    <>
      <Head>
        <title>About Us | Acme Co</title>
        <meta name="description" content="Learn about Acme Co..." />
        <link rel="canonical" href="https://example.com/about" key="canonical" />
        <meta property="og:title" content="About Us | Acme Co" />
        <meta property="og:description" content="Learn about Acme Co..." />
        <meta property="og:image" content="https://example.com/og.png" />
        <meta name="twitter:card" content="summary_large_image" />
      </Head>
      {/* page content */}
    </>
  )
}
```

---

## Hreflang (Multilingual)

```tsx
// App Router — app/[locale]/page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  return {
    alternates: {
      canonical: `https://example.com/${params.locale}`,
      languages: {
        'en-US': 'https://example.com/en',
        'sv-SE': 'https://example.com/sv',
      },
    },
  }
}
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Missing or duplicate `<title>` | Use `title.template` in root layout |
| No `description` on inner pages | Always set `description` in each page's metadata |
| Missing canonical on paginated/filtered URLs | Add `alternates.canonical` pointing to the clean URL |
| OG image not specified | Add `openGraph.images` array with `width` + `height` |
| `noindex` accidentally set | Audit `robots` field in metadata; remove or set `index: true` |
