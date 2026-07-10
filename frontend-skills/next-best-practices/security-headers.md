# Security Headers

Configure HTTP security headers in `next.config.ts` for production hardening.

## Quick Setup

```ts
// next.config.ts
import type { NextConfig } from 'next'

const securityHeaders = [
  {
    key: 'X-DNS-Prefetch-Control',
    value: 'on',
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  },
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  {
    key: 'Permissions-Policy',
    value: 'camera=(), microphone=(), geolocation=()',
  },
]

const nextConfig: NextConfig = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ]
  },
}

export default nextConfig
```

## Header Reference

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| `Strict-Transport-Security` | Force HTTPS | `max-age=63072000; includeSubDomains; preload` |
| `X-Frame-Options` | Prevent clickjacking | `SAMEORIGIN` or `DENY` |
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `Referrer-Policy` | Control referrer info | `strict-origin-when-cross-origin` |
| `X-DNS-Prefetch-Control` | DNS prefetching | `on` |
| `Permissions-Policy` | Disable browser features | `camera=(), microphone=()` |
| `Content-Security-Policy` | XSS protection | See CSP section below |

## Content Security Policy (CSP)

CSP prevents XSS attacks by controlling which resources can load.

### Basic CSP

```ts
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
`

const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: ContentSecurityPolicy.replace(/\s{2,}/g, ' ').trim(),
  },
  // ... other headers
]
```

### CSP Directives Quick Reference

| Directive | Controls | Common Values |
|-----------|----------|---------------|
| `default-src` | Fallback for all | `'self'` |
| `script-src` | JavaScript | `'self'`, `'unsafe-inline'`, domains |
| `style-src` | CSS | `'self'`, `'unsafe-inline'` |
| `img-src` | Images | `'self'`, `data:`, `https:` |
| `font-src` | Fonts | `'self'`, font CDN domains |
| `connect-src` | XHR, fetch, WebSocket | `'self'`, API domains |
| `frame-ancestors` | Who can embed | `'none'`, `'self'` |
| `frame-src` | Iframes | `'self'`, embed domains |

### Adding External Services

```ts
// Example: Adding analytics, fonts, and API
const ContentSecurityPolicy = `
  default-src 'self';
  script-src 'self' 'unsafe-eval' 'unsafe-inline' https://www.googletagmanager.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  img-src 'self' data: https: blob:;
  font-src 'self' https://fonts.gstatic.com;
  connect-src 'self' https://api.myapp.com https://www.google-analytics.com;
  frame-ancestors 'none';
`
```

## Path-Specific Headers

```ts
// next.config.ts
const nextConfig: NextConfig = {
  async headers() {
    return [
      // All routes
      {
        source: '/:path*',
        headers: securityHeaders,
      },
      // Static assets - aggressive caching
      {
        source: '/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ]
  },
}
```

## Common Patterns

### Development vs Production

```ts
const isDev = process.env.NODE_ENV === 'development'

const securityHeaders = [
  // HSTS only in production
  ...(!isDev ? [{
    key: 'Strict-Transport-Security',
    value: 'max-age=63072000; includeSubDomains; preload',
  }] : []),
  // Always include these
  {
    key: 'X-Frame-Options',
    value: 'SAMEORIGIN',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
]
```

### Embedding in Iframes

```ts
// Allow specific domains to embed your site
{
  key: 'Content-Security-Policy',
  value: "frame-ancestors 'self' https://trusted-site.com",
}

// Or use X-Frame-Options (older browsers)
{
  key: 'X-Frame-Options',
  value: 'ALLOW-FROM https://trusted-site.com', // Note: deprecated, use CSP instead
}
```

## Verification

Test your headers at:
- [securityheaders.com](https://securityheaders.com)
- [observatory.mozilla.org](https://observatory.mozilla.org)

Check in browser DevTools: Network tab → Select request → Headers tab
