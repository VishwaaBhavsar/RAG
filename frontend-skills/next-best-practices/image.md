# Image Optimization

Use `next/image` for automatic image optimization.

## Always Use next/image

```tsx
// Bad: Avoid native img
<img src="/hero.png" alt="Hero" />

// Good: Use next/image
import Image from 'next/image'
<Image src="/hero.png" alt="Hero" width={800} height={400} />
```

## Required Props

Images need explicit dimensions to prevent layout shift:

```tsx
// Local images - dimensions inferred automatically
import heroImage from './hero.png'
<Image src={heroImage} alt="Hero" />

// Remote images - must specify width/height
<Image src="https://example.com/image.jpg" alt="Hero" width={800} height={400} />

// Or use fill for parent-relative sizing
<div style={{ position: 'relative', width: '100%', height: 400 }}>
  <Image src="/hero.png" alt="Hero" fill style={{ objectFit: 'cover' }} />
</div>
```

## Remote Images Configuration

Remote domains must be configured in `next.config.ts`:

```ts
// next.config.ts
import { composePlugins, withNx } from '@nx/next';
import type { WithNxOptions } from '@nx/next/plugins/with-nx';

const nextConfig: WithNxOptions = {
  nx: {},
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
        pathname: '/images/**',
      },
      {
        protocol: 'https',
        hostname: '*.cdn.com',
      },
    ],
  },
};

const plugins = [withNx];
export default composePlugins(...plugins)(nextConfig);
```

### Remote Pattern Template

Each external image source requires a `remotePatterns` entry:

```ts
{
  protocol: 'https',
  hostname: 'images.example.com',  // Replace with actual hostname
  pathname: '/images/**',          // Optional: restrict to specific paths
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `protocol` | Yes | `'http'` or `'https'` |
| `hostname` | Yes | Domain name (supports `*` wildcard for subdomains) |
| `pathname` | No | Restrict to specific paths (e.g., `/uploads/**`) |
| `port` | No | Specific port if needed |

### Common Image Hostnames

Common services for stock photos and AI-generated placeholders:

| Provider | Hostname | Use Case |
|----------|----------|----------|
| Unsplash | `images.unsplash.com` | High-quality stock photos |
| Pexels | `images.pexels.com` | Free stock photos & videos |
| Pixabay | `pixabay.com` | Stock photos, vectors, videos |
| Lorem Picsum | `picsum.photos` | Random placeholder images |
| Placehold.co | `placehold.co` | Custom placeholder images |
| Placeholder.com | `via.placeholder.com` | Simple placeholder images |
| DummyImage | `dummyimage.com` | Configurable placeholders |
| RandomUser | `randomuser.me` | Random avatar photos |

**Configuration example with common providers:**

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
      { protocol: 'https', hostname: 'images.pexels.com' },
      { protocol: 'https', hostname: 'picsum.photos' },
      { protocol: 'https', hostname: 'placehold.co' },
    ],
  },
}

export default nextConfig
```

**Security tip:** Only add providers you actually use. Each entry is a security allowlist.

## Responsive Images

Use `sizes` to tell the browser which size to download:

```tsx
// Full-width hero
<Image
  src="/hero.png"
  alt="Hero"
  fill
  sizes="100vw"
/>

// Responsive grid (3 columns on desktop, 1 on mobile)
<Image
  src="/card.png"
  alt="Card"
  fill
  sizes="(max-width: 768px) 100vw, 33vw"
/>

// Fixed sidebar image
<Image
  src="/avatar.png"
  alt="Avatar"
  width={200}
  height={200}
  sizes="200px"
/>
```

## Blur Placeholder

Prevent layout shift with placeholders:

```tsx
// Local images - automatic blur hash
import heroImage from './hero.png'
<Image src={heroImage} alt="Hero" placeholder="blur" />

// Remote images - provide blurDataURL
<Image
  src="https://example.com/image.jpg"
  alt="Hero"
  width={800}
  height={400}
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRg..."
/>

// Or use color placeholder
<Image
  src="https://example.com/image.jpg"
  alt="Hero"
  width={800}
  height={400}
  placeholder="empty"
  style={{ backgroundColor: '#e0e0e0' }}
/>
```

## Priority Loading

Use `priority` for above-the-fold images (LCP):

```tsx
// Hero image - loads immediately
<Image src="/hero.png" alt="Hero" fill priority />

// Below-fold images - lazy loaded by default (no priority needed)
<Image src="/card.png" alt="Card" width={400} height={300} />
```

## Common Mistakes

```tsx
// Bad: Missing sizes with fill - downloads largest image
<Image src="/hero.png" alt="Hero" fill />

// Good: Add sizes for proper responsive behavior
<Image src="/hero.png" alt="Hero" fill sizes="100vw" />

// Bad: Using width/height for aspect ratio only
<Image src="/hero.png" alt="Hero" width={16} height={9} />

// Good: Use actual display dimensions or fill with sizes
<Image src="/hero.png" alt="Hero" fill sizes="100vw" style={{ objectFit: 'cover' }} />

// Bad: Remote image without config
<Image src="https://untrusted.com/image.jpg" alt="Image" width={400} height={300} />
// Error: Invalid src prop, hostname not configured

// Good: Add hostname to next.config.js remotePatterns
```

## Static Export

When using `output: 'export'`, use `unoptimized` or custom loader:

```tsx
// Option 1: Disable optimization per image
<Image src="/hero.png" alt="Hero" width={800} height={400} unoptimized />

// Option 2: Custom loader (Cloudinary, Imgix, etc.)
const cloudinaryLoader = ({ src, width, quality }: { src: string; width: number; quality?: number }) => {
  return `https://res.cloudinary.com/demo/image/upload/w_${width},q_${quality || 75}/${src}`
}

<Image loader={cloudinaryLoader} src="sample.jpg" alt="Sample" width={800} height={400} />
```

```ts
// next.config.ts - Global unoptimized config
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  output: 'export',
  images: { unoptimized: true },
}

export default nextConfig
```

## SVG Best Practices

### Icon Libraries (Industry Standard)

Use icon libraries for UI icons. This is the standard approach used by shadcn/ui, Tailwind, and most production React apps.

**Recommended:** `lucide-react` (used by shadcn/ui)

```tsx
import { Check, X, ChevronDown, Loader2 } from 'lucide-react'

// Basic usage
<Check className="w-5 h-5" />

// With Tailwind styling
<Check className="w-4 h-4 text-green-500" />

// Animated spinner
<Loader2 className="w-4 h-4 animate-spin" />

// In a button
<button className="flex items-center gap-2">
  <ChevronDown className="w-4 h-4" />
  Dropdown
</button>
```

**Other popular libraries:**
- `@heroicons/react` - by Tailwind team
- `@radix-ui/react-icons` - minimal, for Radix UI

### SVGR (For Custom Brand Assets)

Use SVGR only for custom logos and brand SVGs that aren't available in icon libraries.

```ts
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  webpack(config) {
    config.module.rules.push({
      test: /\.svg$/,
      use: ['@svgr/webpack'],
    })
    return config
  },
}

export default nextConfig
```

```tsx
// Usage - for logos and custom brand assets
import Logo from '@/assets/logo.svg'
import BrandIcon from '@/assets/brand-icon.svg'

<Logo className="h-8 w-auto" />
```

### When to Use What

| Use Case | Approach |
|----------|----------|
| UI icons (arrows, check, close, etc.) | `lucide-react` |
| Company logo | SVGR |
| Custom brand illustrations | SVGR |
| Decorative background SVG | `next/image` with `unoptimized` |
