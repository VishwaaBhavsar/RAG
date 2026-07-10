# Environment Variables

Configure environment variables correctly to avoid common gotchas.

## Client vs Server Variables

| Prefix | Access | Bundled | Use Case |
|--------|--------|---------|----------|
| `NEXT_PUBLIC_` | Client + Server | Yes (exposed in browser) | API URLs, feature flags, analytics IDs |
| No prefix | Server only | No (secure) | API keys, database URLs, secrets |

```tsx
// Server Component - can access all env vars
const apiKey = process.env.API_SECRET_KEY // ✅ Works

// Client Component - only NEXT_PUBLIC_ vars
const apiUrl = process.env.NEXT_PUBLIC_API_URL // ✅ Works
const apiKey = process.env.API_SECRET_KEY // ❌ undefined
```

## Common Gotcha: Missing NEXT_PUBLIC_

```tsx
// .env.local
API_URL=https://api.example.com

// components/ClientComponent.tsx
'use client'

// ❌ This will be undefined in the browser!
const url = process.env.API_URL

// Fix: Add NEXT_PUBLIC_ prefix
// .env.local
NEXT_PUBLIC_API_URL=https://api.example.com

// ✅ Now works in client components
const url = process.env.NEXT_PUBLIC_API_URL
```

## Environment File Priority

Files are loaded in order (later overrides earlier):

| File | Environment | Git |
|------|-------------|-----|
| `.env` | All | Commit |
| `.env.local` | All (except test) | Ignore |
| `.env.development` | `next dev` | Commit |
| `.env.development.local` | `next dev` | Ignore |
| `.env.production` | `next build/start` | Commit |
| `.env.production.local` | `next build/start` | Ignore |
| `.env.test` | Jest/testing | Commit |
| `.env.test.local` | Jest/testing | Ignore |

**Rule:** Commit `.env.example` with placeholder values, ignore `.local` files.

## Type-Safe Environment Variables

```ts
// env.ts - validate at build time
import * as yup from 'yup'

const envSchema = yup.object({
  // Server-only
  DATABASE_URL: yup.string().url().required(),
  API_SECRET_KEY: yup.string().min(1).required(),

  // Client-accessible
  NEXT_PUBLIC_API_URL: yup.string().url().required(),
  NEXT_PUBLIC_APP_ENV: yup.string().oneOf(['development', 'staging', 'production']).required(),
})

// Validate and export
export const env = envSchema.validateSync({
  DATABASE_URL: process.env.DATABASE_URL,
  API_SECRET_KEY: process.env.API_SECRET_KEY,
  NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  NEXT_PUBLIC_APP_ENV: process.env.NEXT_PUBLIC_APP_ENV,
})
```

## Runtime vs Build-Time

Environment variables are **inlined at build time**, not read at runtime.

```tsx
// This value is baked into the bundle at build time
const apiUrl = process.env.NEXT_PUBLIC_API_URL

// To use runtime env vars (e.g., Docker), use next.config.ts:
```

```ts
// next.config.ts - runtime environment variables
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  env: {
    // These are still build-time, but pulled from next.config.ts
    CUSTOM_VAR: process.env.CUSTOM_VAR,
  },
  // For true runtime config, use publicRuntimeConfig (Pages Router only)
  // For App Router, use server components
}

export default nextConfig
```

## Security Checklist

| Do | Don't |
|----|-------|
| Use server components for secrets | Expose API keys with `NEXT_PUBLIC_` |
| Validate env vars at startup | Trust env vars exist without checking |
| Use `.env.local` for local secrets | Commit `.env.local` to git |
| Add `.env.local` to `.gitignore` | Share production secrets in `.env` |

## Common Patterns

### Feature Flags

```ts
// .env
NEXT_PUBLIC_FEATURE_NEW_DASHBOARD=true

// Usage
const showNewDashboard = process.env.NEXT_PUBLIC_FEATURE_NEW_DASHBOARD === 'true'
```

### API Base URLs

```ts
// .env.development
NEXT_PUBLIC_API_URL=http://localhost:3001

// .env.production
NEXT_PUBLIC_API_URL=https://api.myapp.com

// Usage - automatically uses correct URL per environment
const api = process.env.NEXT_PUBLIC_API_URL
```

### Conditional Logic

```tsx
// Only in development
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info')
}

// Custom environment detection
const isProduction = process.env.NEXT_PUBLIC_APP_ENV === 'production'
```
