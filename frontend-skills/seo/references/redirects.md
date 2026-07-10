# Redirects & URL Management

## Redirects in next.config.js

Use `redirects()` to move pages permanently or temporarily. Preserves SEO equity on permanent redirects.

```js
// next.config.js
module.exports = {
  async redirects() {
    return [
      // Permanent redirect (308 — modern 301)
      {
        source: '/old-blog/:slug',
        destination: '/news/:slug',
        permanent: true,
      },
      // Temporary redirect (307 — modern 302)
      {
        source: '/sale',
        destination: '/promotions',
        permanent: false,
      },
      // Wildcard — redirect all /docs/* to /help/*
      {
        source: '/docs/:path*',
        destination: '/help/:path*',
        permanent: true,
      },
    ]
  },
}
```

**Status codes:**
- `permanent: true` → 308 (equivalent to 301, passes SEO equity)
- `permanent: false` → 307 (equivalent to 302, temporary)

---

## Rewrites (cosmetic URL changes)

Rewrites serve content from a different path without changing the browser URL. Useful for clean public URLs that map to internal routes.

```js
// next.config.js
module.exports = {
  async rewrites() {
    return [
      // /api/user → proxied to external service
      {
        source: '/api/user/:id',
        destination: 'https://api.internal.com/v2/user/:id',
      },
      // /blog/:slug → internally served by /content/blog/:slug
      {
        source: '/blog/:slug',
        destination: '/content/blog/:slug',
      },
    ]
  },
}
```

---

## URL Structure Best Practices

| Rule | Example |
|------|---------|
| Lowercase, hyphenated slugs | `/my-page` not `/MyPage` or `/my_page` |
| No trailing slash (or consistent with/without) | Set `trailingSlash: true/false` in `next.config.js` |
| Dynamic segments for content | `/blog/[slug]` not `/blog?id=123` |
| Descriptive paths | `/products/running-shoes` not `/p/12345` |
| Avoid deep nesting (> 3 levels) | `/blog/tech/2024/post` → prefer `/blog/tech-post` |

```js
// next.config.js — enforce trailing slash consistency
module.exports = {
  trailingSlash: false, // or true, pick one and be consistent
}
```

---

## Programmatic Redirects (Server-side)

For auth-gated pages, redirect in server components or middleware:

```tsx
// app/dashboard/page.tsx
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const session = await getSession()
  if (!session) redirect('/login')
  return <DashboardContent />
}
```

```ts
// middleware.ts — redirect at the edge
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Redirect loop (A → B → A) | Check `source` + `destination` for circular paths; test in dev |
| Client-side `<Link>` navigation bypasses `next.config.js` redirects | Handle auth/redirect logic in middleware or server components too |
| Forgetting to redirect old URLs after restructure | Keep a redirect log; add entries to `next.config.js` before removing old routes |
| Using `permanent: false` for pages that moved forever | Use `permanent: true` so Google transfers link equity |
