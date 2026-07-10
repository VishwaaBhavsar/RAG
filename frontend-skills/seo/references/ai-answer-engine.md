# Answer Engine Optimization (AEO)

AEO is about structuring content so AI engines (Google AI Overviews, Perplexity, ChatGPT Search) extract and present your content as the answer to a user's query.

---

## Answer-First Content Pattern

AI engines look for the **most direct answer nearest to the question**. Structure every section like this:

```
Question (as heading)
→ Direct answer (1–2 sentences, ≤ 50 words)
→ Supporting detail / context
→ Code example / list / table
→ Related links
```

```tsx
// ✅ AEO-optimized section structure
<section>
  <h2>What is Incremental Static Regeneration in Next.js?</h2>
  {/* Direct answer first — this is what AI extracts */}
  <p>
    Incremental Static Regeneration (ISR) lets you update static pages after
    build time by revalidating content at a set time interval, without
    rebuilding the entire site.
  </p>
  {/* Supporting detail */}
  <p>
    ISR combines the performance of Static Generation with the freshness of
    Server-Side Rendering. Set it with <code>export const revalidate = 3600</code>
    in App Router, or return <code>revalidate</code> from <code>getStaticProps</code>
    in Pages Router.
  </p>
  <pre><code>{`// App Router
export const revalidate = 3600 // revalidate every hour`}</code></pre>
</section>
```

---

## FAQ Page Pattern

`FAQPage` schema directly feeds Google's "People Also Ask" and AI Overviews.

```tsx
// app/faq/page.tsx
const faqs = [
  {
    question: 'How do I add SEO metadata in Next.js App Router?',
    answer:
      'Export a metadata object from any page.tsx or layout.tsx file. ' +
      'Set title, description, and alternates.canonical at minimum. ' +
      'Use generateMetadata() for dynamic pages.',
  },
  {
    question: 'What is the difference between SSG and SSR in Next.js?',
    answer:
      'SSG (Static Site Generation) builds HTML at compile time for maximum speed. ' +
      'SSR (Server-Side Rendering) builds HTML on each request for dynamic content. ' +
      'Use SSG for public content and SSR for personalized or real-time data.',
  },
]

export default function FAQPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map(({ question, answer }) => ({
      '@type': 'Question',
      name: question,
      acceptedAnswer: { '@type': 'Answer', text: answer },
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main>
        <h1>Frequently Asked Questions</h1>
        {faqs.map(({ question, answer }) => (
          <section key={question}>
            <h2>{question}</h2>
            <p>{answer}</p>
          </section>
        ))}
      </main>
    </>
  )
}
```

---

## Definition / Glossary Pattern

AI engines love clear definitions. Use `DefinedTerm` schema + semantic HTML:

```tsx
<section>
  <h2>
    <dfn id="lcp">Largest Contentful Paint (LCP)</dfn>
  </h2>
  <p>
    Largest Contentful Paint (LCP) measures how long it takes for the largest
    visible content element on a page to load. Google targets LCP under 2.5
    seconds for a good user experience.
  </p>
</section>
```

```tsx
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'DefinedTerm',
  name: 'Largest Contentful Paint',
  description:
    'A Core Web Vital measuring the time until the largest visible content element loads. Target: under 2.5 seconds.',
  inDefinedTermSet: 'https://web.dev/vitals/',
}
```

---

## Writing for AI Extraction — Checklist

- [ ] Each `<h2>` is phrased as a question or clear topic statement
- [ ] Direct answer is the **first sentence** of the section (≤ 50 words)
- [ ] No vague intros ("In this section, we will explore...")
- [ ] Key terms defined clearly on first use
- [ ] Lists use `<ol>` / `<ul>` (not `<div>` bullets)
- [ ] Tables used for comparisons (AI extracts table data well)
- [ ] All content server-rendered (not behind `useEffect`)
- [ ] `FAQPage` or `QAPage` JSON-LD on Q&A content
