# AI-Targeted Schema Types

These Schema.org types are specifically prioritized by AI search engines for extraction, citation, and rich result generation.

---

## QAPage — For Q&A / Support Content

```tsx
// app/support/[question]/page.tsx
export default async function QuestionPage({ params }) {
  const qa = await fetchQuestion(params.question)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'QAPage',
    mainEntity: {
      '@type': 'Question',
      name: qa.question,
      text: qa.question,
      answerCount: qa.answers.length,
      dateCreated: qa.createdAt,
      acceptedAnswer: {
        '@type': 'Answer',
        text: qa.acceptedAnswer.text,
        dateCreated: qa.acceptedAnswer.createdAt,
        upvoteCount: qa.acceptedAnswer.votes,
        url: `https://example.com/support/${params.question}#accepted`,
      },
    },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main>
        <h1>{qa.question}</h1>
        <article>
          <p>{qa.acceptedAnswer.text}</p>
        </article>
      </main>
    </>
  )
}
```

---

## HowTo — For Step-by-Step Guides

AI Overviews heavily feature HowTo content. Each step must be self-contained.

```tsx
const howToSchema = {
  '@context': 'https://schema.org',
  '@type': 'HowTo',
  name: 'How to Add SEO to a Next.js App Router Page',
  description: 'Add metadata, canonical tags, and structured data to a Next.js App Router page.',
  totalTime: 'PT15M',
  step: [
    {
      '@type': 'HowToStep',
      position: 1,
      name: 'Export a metadata object',
      text: 'In your page.tsx, export a metadata constant with title and description.',
      url: 'https://example.com/blog/nextjs-seo#step-1',
    },
    {
      '@type': 'HowToStep',
      position: 2,
      name: 'Add a canonical URL',
      text: 'Set alternates.canonical in the metadata object to the page\'s absolute URL.',
      url: 'https://example.com/blog/nextjs-seo#step-2',
    },
    {
      '@type': 'HowToStep',
      position: 3,
      name: 'Add JSON-LD structured data',
      text: 'Insert a <script type="application/ld+json"> in the page component with Article or relevant schema.',
      url: 'https://example.com/blog/nextjs-seo#step-3',
    },
  ],
}
```

Matching HTML (IDs must match `url` fragment):

```tsx
<ol>
  <li id="step-1">
    <h3>Export a metadata object</h3>
    <p>In your <code>page.tsx</code>, export a metadata constant...</p>
  </li>
  <li id="step-2">
    <h3>Add a canonical URL</h3>
    <p>Set <code>alternates.canonical</code> in the metadata object...</p>
  </li>
  <li id="step-3">
    <h3>Add JSON-LD structured data</h3>
    <p>Insert a <code>&lt;script type="application/ld+json"&gt;</code>...</p>
  </li>
</ol>
```

---

## Speakable — For AI Summary / Voice Extraction

```tsx
const speakableSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebPage',
  name: 'Next.js SEO Guide',
  speakable: {
    '@type': 'SpeakableSpecification',
    cssSelector: [
      'h1',
      '.page-summary',   // mark your intro/summary div
      'h2',
    ],
  },
  url: 'https://example.com/blog/nextjs-seo',
}
```

```tsx
// Mark the element AI should extract for summaries
<p className="page-summary">
  Next.js provides a complete SEO toolkit: the Metadata API for titles and
  descriptions, built-in sitemap and robots.txt generation, and next/image
  for automatic image optimization.
</p>
```

---

## DefinedTerm — For Glossary / Technical Definitions

```tsx
const definedTermSchema = {
  '@context': 'https://schema.org',
  '@type': 'DefinedTerm',
  name: 'Incremental Static Regeneration',
  alternateName: 'ISR',
  description:
    'A Next.js rendering strategy that updates static pages after build time ' +
    'by revalidating them at a configurable time interval.',
  inDefinedTermSet: {
    '@type': 'DefinedTermSet',
    name: 'Next.js Glossary',
    url: 'https://example.com/glossary',
  },
  url: 'https://example.com/glossary#isr',
}
```

---

## ItemList — For Category / Index Pages

AI engines extract lists of items from category pages when `ItemList` schema is present:

```tsx
const itemListSchema = {
  '@context': 'https://schema.org',
  '@type': 'ItemList',
  name: 'Next.js SEO Articles',
  description: 'Complete guides for optimizing Next.js apps for search engines',
  numberOfItems: posts.length,
  itemListElement: posts.map((post, i) => ({
    '@type': 'ListItem',
    position: i + 1,
    name: post.title,
    url: `https://example.com/blog/${post.slug}`,
    description: post.excerpt,
  })),
}
```

---

## Schema Type → AI Surface Map

| Schema Type | Best for | AI Surface |
|-------------|----------|------------|
| `FAQPage` | FAQ pages | AI Overviews, People Also Ask |
| `QAPage` | Support/community Q&A | AI Overviews |
| `HowTo` | Step-by-step guides | AI Overviews, rich results |
| `Speakable` | Articles, landing pages | Voice assistants, AI summaries |
| `DefinedTerm` | Glossary, technical docs | Definitions in AI answers |
| `ItemList` | Category, list pages | AI-generated lists |
| `Article` | Blog posts, news | AI citations |
| `Organization` | About, home page | Brand knowledge graph |

---

## Validation Tools

- Google Rich Results Test — confirms schema parses correctly
- Schema.org validator — checks for required fields
- Google Search Console → Enhancements — monitors live schema status
