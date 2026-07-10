# Structured Data — JSON-LD / Schema.org

Structured data helps search engines understand your content and enables rich results (star ratings, breadcrumbs, FAQ dropdowns, etc.).

**Rule:** Always place JSON-LD in server-rendered HTML — never inside `useEffect`. Crawlers may not execute client-side JS.

---

## App Router

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }) {
  const post = await fetchPost(params.slug)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: { '@type': 'Person', name: post.author },
    image: post.coverImage,
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      {/* page content */}
    </>
  )
}
```

---

## Pages Router

```tsx
// pages/products/[slug].tsx
import Head from 'next/head'

export default function ProductPage({ product }) {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD',
      availability: 'https://schema.org/InStock',
    },
  }

  return (
    <>
      <Head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </Head>
      {/* page content */}
    </>
  )
}
```

---

## Common Schema Types

### BreadcrumbList

```tsx
const breadcrumb = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://example.com' },
    { '@type': 'ListItem', position: 2, name: 'Blog', item: 'https://example.com/blog' },
    { '@type': 'ListItem', position: 3, name: 'Post Title', item: 'https://example.com/blog/post-slug' },
  ],
}
```

### FAQPage

```tsx
const faq = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: 'What is Acme Co?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'Acme Co is a platform for...',
      },
    },
  ],
}
```

### Organization (home page)

```tsx
const org = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Acme Co',
  url: 'https://example.com',
  logo: 'https://example.com/logo.png',
  sameAs: [
    'https://twitter.com/acmeco',
    'https://linkedin.com/company/acmeco',
  ],
}
```

---

## Validation

After adding JSON-LD, validate with:
- Google Rich Results Test: `search.google.com/test/rich-results`
- Schema.org validator: `validator.schema.org`

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| JSON-LD in `useEffect` | Move to server component / `getServerSideProps` |
| Invalid JSON (trailing commas, unquoted keys) | Use `JSON.stringify()` — never write raw JSON strings |
| Missing required fields for rich result type | Check Google's Rich Results documentation for required vs recommended fields |
| Multiple `@type` on same page without nesting | Use `@graph` to combine multiple schemas |
