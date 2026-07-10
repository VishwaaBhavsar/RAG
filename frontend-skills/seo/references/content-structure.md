# Content Structure Optimization

Well-structured content is crawled more accurately, earns more featured snippets, and ranks higher. This covers how to organize content in Next.js pages for maximum SEO value.

---

## Page Content Architecture

Every SEO-optimized page should follow this structure:

```
<title>        → Primary keyword + brand
<h1>           → Mirrors title, primary keyword at start
<intro para>   → Answers the user intent in first 100 words
<h2> sections  → Cover sub-topics, include secondary keywords
<h3> sub-items → Break down complex sections
<conclusion>   → Summarize, include CTA with internal link
```

---

## Content Must Be Server-Rendered

Never put indexable content inside `useEffect` or client-only components. Crawlers see the initial HTML.

```tsx
// ✅ Server Component (App Router) — content in HTML
export default async function ProductPage({ params }) {
  const product = await fetchProduct(params.slug) // fetched server-side
  return (
    <article>
      <h1>{product.name}</h1>
      <p>{product.description}</p>   {/* In the HTML, crawlers see this */}
    </article>
  )
}

// ❌ Client-only — crawlers see empty <div>
'use client'
export default function ProductPage({ params }) {
  const [product, setProduct] = useState(null)
  useEffect(() => {
    fetch(`/api/products/${params.slug}`).then(r => r.json()).then(setProduct)
  }, [])
  return <div>{product?.description}</div>  // empty on first load
}
```

---

## Keyword Placement Priority

| Location | Importance | Example |
|----------|-----------|---------|
| `<title>` | Highest | `"Next.js SEO Guide - Acme Co"` |
| `<h1>` | Highest | `<h1>Next.js SEO: Complete Guide</h1>` |
| First 100 words of body | High | Intro paragraph with keyword naturally |
| `<h2>` headings | High | Cover related keywords |
| Image `alt` text | Medium | Describe what's in image using relevant terms |
| URL slug | Medium | `/blog/nextjs-seo-guide` |
| Meta description | Medium | 50–160 chars, includes keyword, drives click-through |

---

## Writing Content for Featured Snippets

Google extracts snippets from well-structured HTML. Format content to match snippet types:

### Paragraph snippet (definition / "what is")
```tsx
<section>
  <h2>What is Incremental Static Regeneration (ISR)?</h2>
  <p>
    Incremental Static Regeneration (ISR) is a Next.js feature that lets you
    update static pages after build time by revalidating them on a set interval,
    combining the speed of SSG with the freshness of SSR.
  </p>
</section>
```

### List snippet (how-to / steps)
```tsx
<section>
  <h2>How to Add SEO to a Next.js Page</h2>
  <ol>
    <li>Export a <code>metadata</code> object with <code>title</code> and <code>description</code></li>
    <li>Add a self-referencing canonical URL via <code>alternates.canonical</code></li>
    <li>Use <code>next/image</code> for all images with descriptive <code>alt</code> text</li>
    <li>Include JSON-LD structured data in a server-rendered <code>&lt;script&gt;</code> tag</li>
  </ol>
</section>
```

### Table snippet
```tsx
<section>
  <h2>Next.js Rendering Strategy Comparison</h2>
  <table>
    <thead>
      <tr>
        <th>Strategy</th><th>Best For</th><th>SEO Impact</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>SSG</td><td>Rarely-changing public content</td><td>Best — fast TTFB</td></tr>
      <tr><td>ISR</td><td>Frequently-updated public content</td><td>Good — fresh + cached</td></tr>
      <tr><td>SSR</td><td>Personalized or real-time content</td><td>Good — slower TTFB</td></tr>
      <tr><td>CSR</td><td>Auth-gated dashboards</td><td>None — not indexed</td></tr>
    </tbody>
  </table>
</section>
```

---

## Meta Description Best Practices

```tsx
export const metadata = {
  description:
    'Learn how to add SEO to your Next.js app with metadata, sitemaps, ' +
    'structured data, and Core Web Vitals optimization. Step-by-step guide.',
  // ↑ 50–160 characters, includes keyword, has a value proposition
}
```

- 50–160 characters
- Include primary keyword naturally
- Write as a call-to-action or value statement
- Unique per page — never duplicate

---

## Thin Content Prevention

"Thin" pages (blank, spinner-only, or minimal text) hurt rankings.

```tsx
// ❌ Thin — loading spinner, no server-rendered content
export default function Page() {
  const { data, isLoading } = useQuery(...)
  if (isLoading) return <Spinner />
  return <div>{data?.content}</div>
}

// ✅ Rich — server renders content, client enhances
export default async function Page({ params }) {
  const data = await fetchData(params.slug)  // server
  return (
    <article>
      <h1>{data.title}</h1>
      <p>{data.description}</p>
      <section>
        <h2>Key Points</h2>
        <ul>{data.points.map(p => <li key={p}>{p}</li>)}</ul>
      </section>
      <ClientInteractions data={data} />  {/* interactive bits client-only */}
    </article>
  )
}
```

---

## Content Length Guidelines

| Page Type | Minimum Content | Notes |
|-----------|----------------|-------|
| Landing / home | 300+ words | Focus on value prop + keywords |
| Blog post | 800–2000 words | Comprehensive coverage of topic |
| Product page | 300+ words | Description, specs, benefits |
| Category page | 200+ words | Intro paragraph + curated links |
| FAQ page | 50+ words per answer | Structured for featured snippet |

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Page title ≠ `<h1>` content | Align them — same topic, can vary slightly in wording |
| Keyword stuffing | Write naturally; use keyword once in h1, intro, and a few times in body |
| Duplicate meta descriptions | Each page must have unique description |
| Content behind tabs/accordions (client-rendered) | Render all content in HTML; use CSS `hidden` for visual toggle |
| Empty category / tag pages | Add introductory content (2–3 sentences minimum) |
| No internal links from content | Add 2–5 contextual links per page to related content |
