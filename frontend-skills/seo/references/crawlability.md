# Crawlability — robots.txt, Sitemap, Index Control

## robots.txt

### App Router — dynamic (recommended)

```ts
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: {
      userAgent: '*',
      allow: '/',
      disallow: ['/private/', '/admin/'],
    },
    sitemap: 'https://example.com/sitemap.xml',
  }
}
```

Next.js serves this at `/robots.txt` automatically.

### Pages Router — static file

Place `public/robots.txt`:

```
User-agent: *
Allow: /
Disallow: /private/
Sitemap: https://example.com/sitemap.xml
```

---

## XML Sitemap

### App Router — dynamic (recommended)

```ts
// app/sitemap.ts
import type { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await fetchAllPosts() // your data source

  const postEntries = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }))

  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    ...postEntries,
  ]
}
```

Served at `/sitemap.xml` automatically.

### Pages Router

Use the `next-sitemap` package or create `public/sitemap.xml` manually.

---

## Controlling Indexation

### Block a specific page from indexing (App Router)

```tsx
// app/admin/page.tsx
export const metadata = {
  robots: {
    index: false,
    follow: false,
  },
}
```

### Block via HTTP header in next.config.js

```js
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/private/:path*',
        headers: [{ key: 'X-Robots-Tag', value: 'noindex, nofollow' }],
      },
    ]
  },
}
```

---

## Canonical Tags

Self-referencing canonical on every page prevents duplicate-content penalties.

### App Router

```tsx
export const metadata = {
  alternates: {
    canonical: 'https://example.com/about',
  },
}
```

### Pages Router

```tsx
<Head>
  <link rel="canonical" href="https://example.com/about" key="canonical" />
</Head>
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Sitemap not regenerated after adding routes | Re-deploy or use `revalidate` on sitemap route |
| `disallow: /` on production (copy-paste from dev) | Always audit `robots.txt` before launch |
| Missing sitemap URL in `robots.txt` | Add `sitemap:` directive |
| Duplicate content from `?page=1` or `?sort=` params | Add canonical pointing to the base URL |
| Important pages accidentally `noindex` | Search for `noindex` / `robots: { index: false }` across all layouts |
