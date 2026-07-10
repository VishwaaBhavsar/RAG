# Entry Animations + Scroll-Triggered Animations

> **Framer Motion is installed** — use `framer-motion.md` Skills 1 + 2 (`initial/animate`, `whileInView`) for all entry and scroll animations.
> This file is a **CSS-only fallback** for environments where Framer Motion is not available.

---

## CSS-Only Fallback — Entry Animations

Simple entry: `animate-fade-in motion-reduce:animate-none` (already in `global.css`).

Directional variants — add to `global.css` `@theme` if needed (follow `tailwind-animations.md` pattern):

```css
--animate-slide-up: slide-up 0.4s ease-out;
@keyframes slide-up { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
.animate-slide-up { animation: slide-up 0.4s ease-out; }
/* Same pattern for slide-left (translateX) and scale-in (scale 0.95→1) */
```

---

## CSS-Only Fallback — Scroll Trigger (`useInView` hook)

```tsx
// apps/frontend/src/hooks/useInView.ts
import { useEffect, useRef, useState } from 'react'
export function useInView(options?: IntersectionObserverInit) {
  const ref = useRef<HTMLDivElement>(null)
  const [inView, setInView] = useState(false)
  useEffect(() => {
    const el = ref.current; if (!el) return
    const observer = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setInView(true); observer.disconnect() } }, { threshold: 0.15, ...options })
    observer.observe(el)
    return () => observer.disconnect()
  }, [])
  return { ref, inView }
}
```

Usage: set `opacity-0 translate-y-6 transition-all`, toggle to `opacity-100 translate-y-0` when `inView`.

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Animation reruns on scroll | `observer.disconnect()` after first trigger |
| Flash of invisible content | Start `opacity-0` in CSS before JS loads |
| `useInView` in server component | Add `'use client'` |
