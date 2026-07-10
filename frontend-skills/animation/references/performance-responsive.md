# Performance-Optimized + Responsive Animations

> `motion-reduce:` pattern is in `references/tailwind-animations.md`. This file covers GPU performance rules and responsive animation strategy.

---

## Skill 9 — Performance-Optimized Animations

### Animate only compositor-friendly properties

| Property | Performance | Notes |
|----------|-------------|-------|
| `transform`, `opacity` | ✅ GPU-composited | Always prefer |
| `filter` (`blur`) | ⚠️ Expensive on large areas | Use on small elements only |
| `width`, `height`, `margin`, `top`, `left` | ❌ Layout reflow | Never animate |

```tsx
// ✅ GPU — smooth 60fps
<div className="transition-transform hover:scale-105" />
<div className="transition-opacity hover:opacity-80" />

// ❌ Reflow — janky
<div className="transition-all hover:w-48" />
<div className="transition-all hover:mt-2" />
```

### `will-change-transform` — sparingly

Only on elements that animate continuously or on deliberate hover:

```tsx
// ✅ On a card that lifts on hover
<div className="will-change-transform hover:scale-105 transition-transform">

// ❌ Not on static content
<div className="will-change-transform">Static text</div>
```

### `transform-gpu` for continuous animations

```tsx
<Loader2 className="animate-spin transform-gpu" />
```

### Avoid animating large blurred surfaces

```tsx
// ❌ Full-page backdrop-blur animation is expensive
<div className="fixed inset-0 backdrop-blur-xl animate-fade-in" />

// ✅ Animate a contained element
<div className="max-w-sm rounded-xl backdrop-blur-xl animate-fade-in" />
```

---

## Skill 10 — Responsive Animations

### Disable on mobile, enable on desktop

```tsx
// No animation on mobile, fade-in on md+
<div className="md:animate-fade-in motion-reduce:animate-none">

// Hover only on desktop (touch has no hover)
<div className="md:hover:scale-105 md:transition-transform motion-reduce:md:transition-none">
```

### Lower Intersection Observer threshold on mobile

```tsx
// Smaller viewport needs earlier trigger
const { ref, inView } = useInView({ threshold: 0.05 })
```

### Shorter stagger delays on mobile

```tsx
{items.map((item, i) => (
  <div
    key={item.id}
    className="animate-fade-in motion-reduce:animate-none"
    style={{ animationDelay: `${i * 50}ms` }} // 50ms mobile vs 100ms desktop
  >
    {item.content}
  </div>
))}
```

---

## Performance Checklist

- [ ] Only animating `transform` and `opacity`
- [ ] `will-change-transform` only on continuously-animating elements
- [ ] Large blurred overlays not animated
- [ ] `motion-reduce:` on every animated element (see `references/tailwind-animations.md`)
- [ ] `transform-gpu` on continuous animations
- [ ] Stagger total duration capped at 1s
- [ ] Simplified or disabled animations on mobile
