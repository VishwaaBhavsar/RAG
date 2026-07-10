# Semantic HTML Structure

Semantic HTML tells search engines what each piece of content means, not just how it looks. Google uses it to understand page hierarchy, extract featured snippets, and determine content relevance.

---

## Heading Hierarchy Rules

- **One `<h1>` per page** — contains the primary keyword, matches or closely mirrors the `<title>`
- `<h2>` for major sections, `<h3>` for sub-sections — never skip levels
- Never use headings just for visual size — use CSS instead
- Never use `<div>` styled as a heading

```tsx
// ✅ Correct
export default function BlogPost({ post }) {
  return (
    <article>
      <h1>{post.title}</h1>          {/* Primary keyword here */}
      <section>
        <h2>Introduction</h2>
        <p>{post.intro}</p>
      </section>
      <section>
        <h2>Key Features</h2>
        <h3>Feature One</h3>
        <p>...</p>
        <h3>Feature Two</h3>
        <p>...</p>
      </section>
    </article>
  )
}

// ❌ Wrong — skips h2, uses div as heading
<h1>Title</h1>
<div className="text-2xl font-bold">Section</div>  {/* invisible to crawlers */}
<h3>Sub-section</h3>                                {/* skipped h2 */}
```

---

## Landmark Elements (Page Structure)

Use these semantic containers — they create ARIA landmarks for screen readers and help crawlers identify page regions:

```tsx
export default function Layout({ children }) {
  return (
    <>
      <header>           {/* Site header, logo, nav */}
        <nav>            {/* Primary navigation */}
          <ul>
            <li><Link href="/">Home</Link></li>
            <li><Link href="/about">About</Link></li>
          </ul>
        </nav>
      </header>

      <main>             {/* Main unique content — one per page */}
        {children}
      </main>

      <aside>            {/* Supplementary content (sidebar, related posts) */}
        <h2>Related Articles</h2>
      </aside>

      <footer>           {/* Site footer */}
        <address>        {/* Contact info */}
          <a href="mailto:hello@example.com">hello@example.com</a>
        </address>
      </footer>
    </>
  )
}
```

---

## Content Elements

| Element | Use for |
|---------|---------|
| `<article>` | Self-contained content (blog post, product card, news item) |
| `<section>` | Thematic grouping within a page — give each a heading |
| `<aside>` | Tangentially related content (sidebar, callout boxes) |
| `<figure>` + `<figcaption>` | Images, charts, diagrams with captions |
| `<time datetime="...">` | Dates (helps crawlers parse publish dates) |
| `<address>` | Contact info for the nearest `<article>` or page |
| `<mark>` | Highlighted / relevant text |
| `<abbr title="...">` | Abbreviations — crawlers read the expansion |

```tsx
// Article with semantic time and figure
<article>
  <h1>How to Build Fast Next.js Apps</h1>
  <p>Published <time dateTime="2024-03-15">March 15, 2024</time></p>

  <figure>
    <Image src="/diagram.png" alt="Architecture diagram showing SSR flow" width={800} height={400} />
    <figcaption>Fig 1: Server-side rendering flow in Next.js App Router</figcaption>
  </figure>

  <section>
    <h2>Rendering Strategies</h2>
    <p>...</p>
  </section>
</article>
```

---

## Lists

Use `<ul>` / `<ol>` / `<dl>` for actual list content — not `<div>` with CSS spacing.

```tsx
// ✅ Semantic list (Google can extract as featured snippet)
<section>
  <h2>Top 5 Next.js SEO Tips</h2>
  <ol>
    <li>Use SSG for public content</li>
    <li>Optimize images with next/image</li>
    <li>Add canonical tags on every page</li>
    <li>Use structured data (JSON-LD)</li>
    <li>Generate a sitemap.xml</li>
  </ol>
</section>

// Definition list for glossary / key-value pairs
<dl>
  <dt>LCP</dt>
  <dd>Largest Contentful Paint — measures load time of the main visible element</dd>
  <dt>CLS</dt>
  <dd>Cumulative Layout Shift — measures visual stability</dd>
</dl>
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Multiple `<h1>` on one page | Keep exactly one `<h1>`; use layout headings as `<h2>` |
| `<div>` and `<span>` for everything | Replace with `<article>`, `<section>`, `<nav>`, `<header>`, etc. |
| Missing `<main>` | Wrap primary content in `<main>` for ARIA + crawlers |
| Heading levels skipped (h1 → h3) | Always go h1 → h2 → h3 in order |
| Dates as plain text | Wrap in `<time dateTime="ISO-date">` |
| Navigation not in `<nav>` | Wrap `<Link>` lists in `<nav>` |

---

## ESLint Enforcement

Add `eslint-plugin-jsx-a11y` to catch semantic HTML issues automatically:

```bash
npm install -D eslint-plugin-jsx-a11y
```

```json
// .eslintrc.json
{
  "extends": ["next/core-web-vitals", "plugin:jsx-a11y/recommended"]
}
```
