---
name: next-best-practices
description: Enforces Next.js App Router file conventions, server vs client component boundaries, metadata, error boundaries, Suspense, image and font optimization. Use this skill when creating or modifying any Next.js file — page.tsx, layout.tsx, loading.tsx, error.tsx, route handlers, or any component that needs to respect RSC boundaries.
user-invocable: false
---

# Next.js Best Practices

Apply these rules when writing or reviewing Next.js code.

## File Conventions

See [file-conventions.md](./file-conventions.md) for:
- Project structure and special files
- Route segments (dynamic, catch-all, groups)
- Parallel and intercepting routes

## RSC Boundaries

Detect invalid React Server Component patterns.

See [rsc-boundaries.md](./rsc-boundaries.md) for:
- Async client component detection (invalid)
- Non-serializable props detection
- Server Action exceptions

## Directives

See [directives.md](./directives.md) for:
- `'use client'`, `'use server'` (React)
- `'use cache'` (Next.js)

## Functions

See [functions.md](./functions.md) for:
- Navigation hooks: `useRouter`, `usePathname`, `useSearchParams`, `useParams`
- Server functions: `cookies`, `headers`, `draftMode`
- Generate functions: `generateStaticParams`, `generateMetadata`

## Error Handling

See [error-handling.md](./error-handling.md) for:
- `error.tsx`, `global-error.tsx`, `not-found.tsx`
- `redirect`, `permanentRedirect`, `notFound`
- `forbidden`, `unauthorized` (auth errors)

## Metadata & OG Images

See [metadata.md](./metadata.md) for:
- Static and dynamic metadata
- `generateMetadata` function
- OG image generation with `next/og`
- File-based metadata conventions

## Image Optimization

See [image.md](./image.md) for:
- Always use `next/image` over `<img>`
- Remote images configuration
- Responsive `sizes` attribute
- Blur placeholders
- Priority loading for LCP
- SVG best practices

## Font Optimization

See [font.md](./font.md) for:
- `next/font` setup
- Google Fonts
- Tailwind CSS v4 integration
- Preloading subsets

## Hydration Errors

See [hydration-error.md](./hydration-error.md) for:
- Common causes (browser APIs, dates, invalid HTML)
- Debugging with error overlay
- Fixes for each cause

## Suspense Boundaries

See [suspense-boundaries.md](./suspense-boundaries.md) for:
- CSR bailout with `useSearchParams` and `usePathname`
- Which hooks require Suspense boundaries

## Environment Variables

See [environment-variables.md](./environment-variables.md) for:
- `NEXT_PUBLIC_` prefix for client-side access
- Build-time vs runtime variables
- Environment file priority (`.env`, `.env.local`, etc.)
- Type-safe validation with Yup

## Security Headers

See [security-headers.md](./security-headers.md) for:
- Production security headers (HSTS, X-Frame-Options, CSP)
- Content Security Policy configuration
- Path-specific header rules
