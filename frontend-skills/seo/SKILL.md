---
name: seo
description: Applies SEO and AI-search optimization to Next.js pages. Use this skill when building any public-facing page — landing pages, home pages, marketing pages, blog pages, or any route accessible without login. Covers metadata, Open Graph, robots.txt, sitemap, structured data, semantic HTML, and performance. Not needed for auth or private dashboard routes.
---

# SEO — Next.js (Traditional + AI Search)

This project uses **App Router** (Next.js 13+). Pages Router patterns do not apply.

---

## Auto-Trigger Rules

**Use this skill automatically — WITHOUT waiting for "SEO friendly" in the prompt — whenever the user asks to:**

- Create a landing page
- Create a marketing page
- Build a home page
- Build a public-facing website or page
- Create any page outside `(auth)` or `(private)` route groups

The user does NOT need to say "SEO friendly" or "SEO" for this skill to apply. All public pages MUST follow these standards.

---

## Required Deliverables — Every Public Page

When creating any public/landing/marketing page, ALL of the following files are **mandatory**. Do not consider the task complete without them:

| # | File | What to create |
|---|------|----------------|
| 1 | `apps/frontend/src/app/<route>/layout.tsx` | Full metadata: title, description, OG, Twitter, canonical, robots |
| 2 | `apps/frontend/src/app/<route>/page.tsx` | Server component with semantic HTML + JSON-LD structured data |
| 3 | `apps/frontend/src/app/sitemap.ts` | Create if missing — auto-served at `/sitemap.xml` |
| 4 | `apps/frontend/src/app/robots.ts` | Create if missing — auto-served at `/robots.txt` |
| 5 | `apps/frontend/public/llms.txt` | **REQUIRED** — LLM/AI engine site summary (see format below) |
| 6 | `apps/frontend/public/llms-full.txt` | **REQUIRED** — Full page content in Markdown for AI ingestion |

---

## `llms.txt` — Format & Purpose

`llms.txt` is the AI equivalent of `robots.txt`. It is placed at `/public/llms.txt` so it is served at `https://yourdomain.com/llms.txt`. It tells LLMs (ChatGPT, Perplexity, Claude, Gemini, Bing Copilot) what your site is about and which URLs to read.

**Always create this file when building any public page.**

```markdown
# <ProductName>

> <One-sentence description of what the product does — plain English, ≤ 30 words>

## Product
- [<Page Title>](<URL>): <What this page covers>
- [Features](<URL>#features): <Feature summary>
- [Pricing](<URL>#pricing): <Pricing summary>
- [FAQ](<URL>#faq): <What questions are answered>

## How it works
- [Guide](<URL>#how-it-works): <Step-by-step summary>

## Optional
- [llms-full.txt](<BASE_URL>/llms-full.txt): Full site content for AI ingestion
```

**`llms-full.txt`** is the same structure but contains the actual page content (headings + paragraphs) in clean Markdown — no HTML, no JSX. AI engines use this to read the full content without parsing HTML.

---

## Project File Locations

| What | File | Notes |
|------|------|-------|
| Root metadata + title template | `apps/frontend/src/app/layout.tsx` | Already has `export const metadata` — update here |
| Landing page metadata | `apps/frontend/src/app/landing/layout.tsx` | Add `export const metadata` per page |
| Sitemap | `apps/frontend/src/app/sitemap.ts` | Create if missing — served at `/sitemap.xml` |
| Robots.txt | `apps/frontend/src/app/robots.ts` | Create if missing — served at `/robots.txt` |
| **llms.txt** | `apps/frontend/public/llms.txt` | **Always create** — served at `/llms.txt` |
| **llms-full.txt** | `apps/frontend/public/llms-full.txt` | **Always create** — full Markdown content for AI |
| Image domains config | `apps/frontend/next.config.js` → `images.remotePatterns` | Already has gstatic, simpleicons, github |
| Redirects / rewrites | `apps/frontend/next.config.js` → `redirects()` / `rewrites()` | Add inside `nextConfig` |
| Per-page metadata | `apps/frontend/src/app/<route>/page.tsx` | Export `metadata` or `generateMetadata` |

---

## Page SEO Strategy

| Route | SEO Treatment |
|-------|--------------|
| `app/marketing/**` | Full SEO — metadata, canonical, structured data, OG tags, llms.txt |
| `app/landing/**` | Full SEO — metadata, canonical, structured data, OG tags, llms.txt |
| `app/page.tsx` (root) | Full SEO — home page, Organization schema, llms.txt |
| `app/(auth)/**` | `robots: { index: false }` — login/signup should not be indexed |
| `app/(private)/**` | `robots: { index: false }` — auth-gated, never index |
| `app/create-workspace/**` | `robots: { index: false }` — onboarding flow |

---

## Cross-Skill Dependencies

| Need | Use skill |
|------|-----------|
| Using `<Image>` component | `components` skill — import from `@/components` |
| Styling SEO components (breadcrumbs, etc.) | `styling` skill |
| Adding translated SEO text | `translation` skill |

---

## When to use this skill

Use this skill for all public pages as defined in **Auto-Trigger Rules** above.

**Traditional SEO**
- Adding `<title>`, `<meta>` description, Open Graph, Twitter Card tags
- Setting up `robots.txt` or `sitemap.xml`
- Creating `llms.txt` / `llms-full.txt` for LLM optimization
- Adding canonical tags or hreflang links
- Embedding structured data (JSON-LD / Schema.org)
- Optimizing images with `next/image` (LCP / CLS)
- Configuring redirects / rewrites in `next.config.js`
- Writing semantic HTML (`<article>`, `<section>`, heading hierarchy)
- Adding internal links with `next/link` and breadcrumbs
- Structuring page content for featured snippets

**AI Search Optimization**
- Making content appear in Google AI Overviews (SGE)
- Getting cited by Perplexity, ChatGPT Search, or Bing Copilot
- Structuring FAQ / Q&A / HowTo content for AI extraction
- Adding `Speakable`, `QAPage`, `HowTo`, `DefinedTerm` schema
- Building brand entity authority for LLM knowledge graphs (LLMO)
- Creating and maintaining `llms.txt`/`llms-full.txt` for AI discovery

---

## Reference

### Traditional SEO

| File | Read when |
|------|-----------|
| `references/metadata.md` | Setting titles, descriptions, OG/Twitter tags, canonical, hreflang |
| `references/semantic-html.md` | Heading hierarchy, landmark elements, semantic tags |
| `references/performance.md` | Core Web Vitals, image optimization, scripts, caching, rendering strategy |
| `references/internal-linking.md` | `next/link`, breadcrumbs, anchor text, orphan pages |
| `references/structured-data.md` | JSON-LD: Article, Product, BreadcrumbList, FAQ, Org |
| `references/crawlability.md` | robots.txt, sitemap.xml, noindex control |
| `references/redirects.md` | 301/308 redirects, rewrites, SEO-friendly URL structure |
| `references/content-structure.md` | Content architecture, keyword placement, featured snippets, thin content |

### AI Search Optimization (AEO / GEO / LLMO)

| File | Read when |
|------|-----------|
| `references/ai-answer-engine.md` | Writing answer-first content, FAQPage schema, definition markup |
| `references/ai-geo.md` | GEO structure, Speakable schema, E-E-A-T signals, citing statistics |
| `references/ai-schema-types.md` | QAPage, HowTo, Speakable, DefinedTerm, ItemList schema |
| `references/ai-entity-authority.md` | Organization/Person `@id`, `sameAs`, brand entity consistency for LLMs |

---

## Rules

### Core (every page)
1. **Always server-render SEO-critical content** — use SSG / SSR / App Router async components; never client-only fetching
2. **One `<h1>` per page** — with the primary keyword; use `<h2>`, `<h3>` in strict order
3. **Every image needs `alt` text** — use `<Image alt="...">` from `next/image`, never bare `<img>`
4. **Unique title + description per page** — extend root `metadata` in `app/layout.tsx` using `title.template`
5. **Canonical on every page** — self-referencing canonical prevents duplicate-content penalties
6. **JSON-LD must be server-rendered** — in page component or `generateMetadata`, never in `useEffect`
7. **Permanent redirects via `next.config.js`** — `permanent: true` (308) passes SEO equity
8. **Defer non-critical scripts** — `<Script strategy="lazyOnload">` or `"afterInteractive"`
9. **`(auth)` and `(private)` routes must be `noindex`** — never let auth-gated pages get indexed
10. **Prefer SSG/ISR for landing/public content** — SSR on every request hurts TTFB and crawl budget
11. **`<Link>` for all internal navigation** — never bare `<a>`; enables prefetch
12. **Semantic HTML landmarks** — `<main>`, `<nav>`, `<article>`, `<section>`, `<header>`, `<footer>`
13. **App brand mark — `src/app/icon.ai.tsx` + `src/app/apple-icon.ai.tsx` (mandatory):** any brand icon used across app UI (navbar/header/sidebar/footer/auth/cards) and the icon visuals in both AI icon files must stay visually identical and be created/updated in the same workflow step. Prefer one shared brand icon component and render that same component wherever brand icon appears and in both AI icon files. AI branding edits belong in **`icon.ai.tsx`** and **`apple-icon.ai.tsx`**. Default active icon files (`icon.tsx`, `apple-icon.tsx`) must remain unchanged during AI generation.
14. **H1 phrase alignment is mandatory** — key H1 phrase terms must appear naturally in paragraph copy (intro + at least one additional section)
15. **Avoid duplicate anchor text for different destinations** — anchor labels must be distinct unless they intentionally target the same URL/section
16. **Public pages should include share options** — include at least one visible social sharing area or outbound social profile links

### AI Search (public content pages)
17. **Answer first, expand second** — direct answer in the first sentence of each section (≤ 50 words)
18. **`FAQPage` or `HowTo` schema** on Q&A and guide pages — feeds AI Overview extraction
19. **Consistent entity naming** — exact same brand/product name in every title, description, and JSON-LD
20. **`Organization` schema with `sameAs`** on home page — establishes brand entity for LLMs
21. **ALWAYS create `llms.txt`** — every public page build MUST produce `/public/llms.txt` and `/public/llms-full.txt`. These are not optional. LLMs cannot discover your content without them.

---

## Completion Checklist (Mandatory Before Marking Done)

For every public page, verify all checks below before completion:

1. **Title quality**  
   - Not a single word  
   - Includes primary topic + brand/entity  
   - Approximate rendered width target: ~200-580px (avoid very short titles)
2. **Meta description quality**  
   - Concise and specific to page content  
   - Approximate rendered width target: <= 1000px (avoid overlong descriptions)
3. **H1 quality**  
   - Exactly one H1 on page  
   - H1 length must be >= 20 characters  
   - Important H1 terms must appear in the intro paragraph and at least one additional section paragraph
4. **Body content depth**  
   - Must contain real paragraph text (not only cards/stats/buttons)  
   - Home/landing pages must target at least ~800 useful words unless the page is intentionally minimal by explicit user request
5. **Heading consistency**  
   - No duplicate heading blocks that repeat the same text without purpose  
   - Heading hierarchy remains logical (`h1` -> `h2` -> `h3`)
6. **Internal linking quality**  
   - Include at least 3 meaningful internal links on content pages  
   - Avoid repeating identical anchor text for different destinations
7. **Social sharing presence**  
   - Include visible social sharing options or outbound social profile links on public marketing/landing pages
