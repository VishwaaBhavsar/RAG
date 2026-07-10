# Generative Engine Optimization (GEO)

GEO optimizes content for generative AI systems (Google AI Overviews, Perplexity, ChatGPT Search) that synthesize answers from multiple sources. The goal: be one of the sources cited.

---

## What GEO-Optimized Content Looks Like

Generative AI engines prefer content that is:
- **Factual and specific** — named entities, numbers, dates over vague generalities
- **Structured** — headings, lists, tables over wall-of-text paragraphs
- **Authoritative** — cites sources, has author expertise signals, consistent with other indexed pages
- **Comprehensive** — covers the topic thoroughly; AI engines synthesize the "best" source

---

## Content Structure for GEO

```tsx
// ✅ GEO-optimized page structure
export default async function ArticlePage({ params }) {
  const article = await fetchArticle(params.slug)

  return (
    <article itemScope itemType="https://schema.org/Article">
      {/* Clear, keyword-rich title */}
      <h1 itemProp="headline">{article.title}</h1>

      {/* Author + date — authority signals */}
      <p>
        By <span itemProp="author">{article.author}</span> ·{' '}
        <time itemProp="datePublished" dateTime={article.publishedAt}>
          {formatDate(article.publishedAt)}
        </time>
        {article.updatedAt && (
          <> · Updated <time itemProp="dateModified" dateTime={article.updatedAt}>
            {formatDate(article.updatedAt)}
          </time></>
        )}
      </p>

      {/* TL;DR / Summary — AI often extracts this */}
      <section aria-label="Summary">
        <p><strong>Summary:</strong> {article.summary}</p>
      </section>

      {/* Main content with structured sections */}
      <div itemProp="articleBody">
        {article.sections.map(section => (
          <section key={section.id}>
            <h2>{section.heading}</h2>
            <p>{section.content}</p>
          </section>
        ))}
      </div>
    </article>
  )
}
```

---

## Speakable Schema (AI Overviews + Voice)

`Speakable` marks which parts of the page are most suitable for AI summary/voice reading:

```tsx
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: 'Complete Next.js SEO Guide',
  speakable: {
    '@type': 'SpeakableSpecification',
    cssSelector: ['h1', '.article-summary', 'h2'],
    // OR use xPath:
    // xpath: ['/html/head/title', "//h1", "//p[contains(@class,'summary')]"]
  },
  url: 'https://example.com/blog/nextjs-seo',
}
```

```tsx
// Mark the summary element for speakable targeting
<p className="article-summary">
  Next.js provides built-in SEO tools including the Metadata API,
  automatic sitemap generation, and image optimization through next/image.
</p>
```

---

## Statistics and Facts Pattern

AI engines heavily cite pages with specific, verifiable statistics:

```tsx
// ✅ Citable — specific, attributed facts
<p>
  Pages using Next.js Static Generation achieve a median TTFB of under 50ms,
  compared to 200–600ms for server-rendered pages (Vercel, 2024).
</p>

// ❌ Not citable — vague
<p>Next.js is really fast and good for SEO.</p>
```

---

## Source Citation Pattern

Link to primary sources — AI engines favor pages that demonstrate research:

```tsx
<section>
  <h2>Core Web Vitals Thresholds</h2>
  <p>
    Google defines good Core Web Vitals as LCP under 2.5s, INP under 200ms,
    and CLS under 0.1{' '}
    <a
      href="https://web.dev/vitals/"
      rel="noopener noreferrer"
      target="_blank"
    >
      (Google Web Vitals, 2024)
    </a>.
  </p>
</section>
```

---

## E-E-A-T Signals in HTML

Google's E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) affects AI Overview citations:

```tsx
// Author bio with Person schema
const authorSchema = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: 'Jane Smith',
  jobTitle: 'Senior Frontend Engineer',
  url: 'https://example.com/authors/jane-smith',
  sameAs: [
    'https://github.com/janesmith',
    'https://linkedin.com/in/janesmith',
  ],
}

// In page
<section aria-label="About the author">
  <Image src="/authors/jane.jpg" alt="Jane Smith" width={64} height={64} />
  <div>
    <strong>Jane Smith</strong>
    <p>Senior Frontend Engineer with 8 years of Next.js experience.</p>
  </div>
</section>
```

---

## GEO Checklist

- [ ] Article has author name + `datePublished` + `dateModified`
- [ ] Contains a summary paragraph (first 100 words answer the main question)
- [ ] Uses specific numbers/statistics with attribution
- [ ] Headings are descriptive questions or statements (not "Introduction")
- [ ] `Speakable` schema marks summary and key headings
- [ ] `Article` or `WebPage` JSON-LD with full metadata
- [ ] Author has `Person` schema with `sameAs` links to external profiles
- [ ] Content matches / does not contradict what's on your other pages (entity consistency)
