# Internal Linking

Internal links distribute page authority (link equity), help crawlers discover content, and signal content relationships to search engines. Next.js `<Link>` also prefetches linked pages in production for faster navigation.

---

## Always Use `next/link` for Internal Navigation

```tsx
import Link from 'next/link'

// ✅ Correct — descriptive anchor text, next/link for prefetch
<Link href="/features/analytics">View analytics features</Link>

// ❌ Wrong — bare <a> skips prefetch; generic anchor text
<a href="/features/analytics">click here</a>
```

---

## Navigation Component Pattern

```tsx
// components/Navigation.tsx
import Link from 'next/link'

const navItems = [
  { href: '/', label: 'Home' },
  { href: '/features', label: 'Features' },
  { href: '/pricing', label: 'Pricing' },
  { href: '/blog', label: 'Blog' },
]

export function Navigation() {
  return (
    <nav aria-label="Main navigation">
      <ul>
        {navItems.map(({ href, label }) => (
          <li key={href}>
            <Link href={href}>{label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}
```

---

## Contextual Links (In-content linking)

Link to related pages naturally within content — this passes link equity and helps crawlers understand topic relationships.

```tsx
// ✅ In-content contextual links
<p>
  To configure performance settings, see our{' '}
  <Link href="/docs/performance">performance optimization guide</Link>.
  For analytics setup, visit the{' '}
  <Link href="/docs/analytics">analytics documentation</Link>.
</p>
```

---

## Related Content / "See Also" Sections

```tsx
// components/RelatedPosts.tsx
import Link from 'next/link'

export function RelatedPosts({ posts }) {
  return (
    <aside aria-label="Related articles">
      <h2>Related Articles</h2>
      <ul>
        {posts.map((post) => (
          <li key={post.slug}>
            <Link href={`/blog/${post.slug}`}>{post.title}</Link>
          </li>
        ))}
      </ul>
    </aside>
  )
}
```

---

## Breadcrumbs (Both Navigation + SEO)

Breadcrumbs create internal links AND enable BreadcrumbList schema for rich results.

```tsx
// components/Breadcrumb.tsx
import Link from 'next/link'

type Crumb = { label: string; href: string }

export function Breadcrumb({ crumbs }: { crumbs: Crumb[] }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: crumbs.map((crumb, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: crumb.label,
      item: `https://example.com${crumb.href}`,
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <nav aria-label="Breadcrumb">
        <ol>
          {crumbs.map((crumb, i) => (
            <li key={crumb.href}>
              {i < crumbs.length - 1 ? (
                <Link href={crumb.href}>{crumb.label}</Link>
              ) : (
                <span aria-current="page">{crumb.label}</span>
              )}
            </li>
          ))}
        </ol>
      </nav>
    </>
  )
}
```

Usage:
```tsx
<Breadcrumb crumbs={[
  { label: 'Home', href: '/' },
  { label: 'Blog', href: '/blog' },
  { label: 'Post Title', href: '/blog/post-slug' },
]} />
```

---

## Prefetch Behaviour

```tsx
// Production: prefetches automatically when link enters viewport
<Link href="/about">About</Link>

// Disable prefetch for less important or many links on page
<Link href="/archive/2019" prefetch={false}>2019 Archive</Link>

// Prefetch even in development
<Link href="/important-page" prefetch={true}>Important</Link>
```

---

## `rel="nofollow"` for Untrusted Links

```tsx
// For user-generated content or paid/sponsored links
<a href="https://external-site.com" rel="nofollow noopener noreferrer" target="_blank">
  External site
</a>
```

---

## Rules

1. **No orphan pages** — every page must be linked from at least one other page or the sitemap
2. **Descriptive anchor text** — never "click here" or "read more"; use the keyword phrase
3. **Use `<Link>`** for all internal URLs — never `<a href="">` for internal navigation
4. **Breadcrumbs on deep pages** — add on pages 2+ levels deep (blog posts, product pages, docs)
5. **Limit links per page** — Google recommends keeping it reasonable (< ~100 links per page)

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Generic anchor text ("click here") | Use descriptive text matching the target page topic |
| Bare `<a>` for internal links | Replace with `<Link>` from `next/link` |
| Orphan pages (no inbound links) | Add to sitemap + link from a relevant parent page |
| Broken internal links | Run `next lint` + use a link checker (e.g. `broken-link-checker`) |
| Too many links per page (> 100) | Paginate, or move secondary links to footer/sidebar |
