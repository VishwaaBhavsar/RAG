# Entity Authority & LLMO (LLM Optimization)

LLMs (ChatGPT, Claude, Gemini, Perplexity) build knowledge about brands and products from crawled web content. LLMO ensures your brand/product is represented accurately and consistently so LLMs cite, mention, and recommend it correctly.

---

## What is an Entity?

An entity is a distinct, identifiable concept (person, organization, product, place). Search engines and LLMs build knowledge graphs from entity relationships. If your brand is a well-defined entity, AI engines recognize and cite it confidently.

---

## Organization Entity (Home Page)

Every site should have a complete `Organization` schema on the home page. This is the primary entity signal for LLMs.

```tsx
// app/page.tsx
const organizationSchema = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  '@id': 'https://example.com/#organization',   // unique entity ID
  name: 'Acme Co',                               // EXACT brand name — use consistently everywhere
  alternateName: ['Acme', 'AcmeCo'],             // known aliases
  url: 'https://example.com',
  logo: {
    '@type': 'ImageObject',
    url: 'https://example.com/logo.png',
    width: 512,
    height: 512,
  },
  description:
    'Acme Co is a project management platform for software teams, ' +
    'offering workspaces, task tracking, and team collaboration tools.',
  foundingDate: '2022',
  sameAs: [
    // Link to authoritative external sources — critical for LLM entity recognition
    'https://www.linkedin.com/company/acmeco',
    'https://twitter.com/acmeco',
    'https://github.com/acmeco',
    'https://www.crunchbase.com/organization/acmeco',
    // Add Wikipedia/Wikidata if available
  ],
  contactPoint: {
    '@type': 'ContactPoint',
    email: 'hello@example.com',
    contactType: 'customer support',
  },
}
```

---

## WebSite Entity (Sitelinks Search Box)

```tsx
const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': 'https://example.com/#website',
  url: 'https://example.com',
  name: 'Acme Co',
  publisher: { '@id': 'https://example.com/#organization' },
  potentialAction: {
    '@type': 'SearchAction',
    target: {
      '@type': 'EntryPoint',
      urlTemplate: 'https://example.com/search?q={search_term_string}',
    },
    'query-input': 'required name=search_term_string',
  },
}
```

---

## Product Entity

For SaaS / product pages — establishes product as a distinct entity:

```tsx
const productSchema = {
  '@context': 'https://schema.org',
  '@type': 'SoftwareApplication',
  '@id': 'https://example.com/product/#software',
  name: 'Acme Workspace',
  applicationCategory: 'ProjectManagementApplication',
  operatingSystem: 'Web',
  description:
    'Acme Workspace is a collaborative project management tool with ' +
    'real-time task tracking, team channels, and AI-powered insights.',
  offers: {
    '@type': 'Offer',
    price: '0',
    priceCurrency: 'USD',
    description: 'Free tier available',
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: '4.8',
    reviewCount: '320',
  },
  publisher: { '@id': 'https://example.com/#organization' },
}
```

---

## Consistent Entity Naming Rules

LLMs get confused by inconsistent brand mentions. Apply these everywhere:

```
Brand name in <title>     → always "Acme Co"
Brand name in metadata    → always "Acme Co"
Brand name in JSON-LD     → always "Acme Co"
Brand name in body text   → always "Acme Co" on first mention per page
Alt names in sameAs       → list known variations once in Organization schema
```

Audit for inconsistencies:
```bash
# Find all brand name variations (adjust pattern to your brand)
grep -r "Acme\|AcmeCo\|acme-co" apps/frontend/src --include="*.tsx" -l
```

---

## Author Entities (Person Schema)

For blog / documentation sites, author entities strengthen E-E-A-T signals:

```tsx
const personSchema = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  '@id': 'https://example.com/authors/jane-smith/#person',
  name: 'Jane Smith',
  jobTitle: 'Senior Frontend Engineer',
  worksFor: { '@id': 'https://example.com/#organization' },
  url: 'https://example.com/authors/jane-smith',
  image: 'https://example.com/authors/jane-smith.jpg',
  sameAs: [
    'https://github.com/janesmith',
    'https://linkedin.com/in/janesmith',
    'https://twitter.com/janesmith',
  ],
  knowsAbout: ['Next.js', 'React', 'Web Performance', 'SEO'],
}
```

---

## @id Cross-Referencing

Link entities together using `@id` references — this builds the knowledge graph:

```tsx
// Article references its author and publisher
const articleSchema = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: 'Next.js SEO Guide',
  author: { '@id': 'https://example.com/authors/jane-smith/#person' },
  publisher: { '@id': 'https://example.com/#organization' },
  isPartOf: { '@id': 'https://example.com/#website' },
}
```

---

## LLMO Checklist

- [ ] `Organization` schema on home page with complete `sameAs` array
- [ ] Brand name is identical across all pages, metadata, and JSON-LD
- [ ] Product has `SoftwareApplication` or `Product` schema with `@id`
- [ ] Authors have `Person` schema with `sameAs` to external profiles
- [ ] Entities are cross-referenced via `@id` in Article/HowTo schemas
- [ ] `WebSite` schema present with `SearchAction` if site has search
- [ ] Company description is consistent in meta descriptions, About page, and JSON-LD
- [ ] External profiles (LinkedIn, GitHub, Crunchbase) mention the same brand name
