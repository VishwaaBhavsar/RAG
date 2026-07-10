# Tailwind Animations

> Transitions, built-in animations, skeleton loading, reduced motion, and custom keyframes using Tailwind CSS v4.

---

## Transitions

| Class | Use Case |
|-------|----------|
| `transition-colors` | Color/background changes |
| `transition-opacity` | Fade effects |
| `transition-transform` | Scale/rotate |
| `transition-all` | Multiple properties |
| `duration-300` | Slower (default 200ms) |

```tsx
<div className="hover:text-primary transition-colors" />
<Card className="hover:border-primary/30 hover:shadow-lg transition-all" />
<div className="hover:scale-105 transition-transform" />
```

---

## Built-in Animations

| Class | Usage |
|-------|-------|
| `animate-spin` | Loading spinners |
| `animate-pulse` | Skeleton loading |
| `animate-bounce` | Attention indicator |

```tsx
<Loader2 className="size-4 animate-spin" />
<Skeleton className="h-4 w-3/4 animate-pulse" />
```

---

## Skeleton Loading

```tsx
<Skeleton className="h-4 w-3/4" />           // Text line
<Skeleton className="size-10 rounded-full" /> // Avatar
<Skeleton className="h-32 w-full" />          // Card image
```

---

## Reduced Motion

```tsx
<div className="motion-safe:animate-spin" />
<div className="motion-reduce:animate-none" />
<div className="motion-reduce:transition-none" />
```

---

## Custom Animations (Tailwind v4)

Define in the `@theme` block in `apps/frontend/src/app/global.css`:

```css
@theme {
  --animate-fade-in: fade-in 0.5s ease-in-out;

  @keyframes fade-in {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
}

@layer utilities {
  .animate-fade-in { animation: fade-in 0.5s ease-in-out; }
}
```

```tsx
<div className="animate-fade-in motion-reduce:animate-none">Fades in</div>
```

---

## Project Custom Animations

| Class | Effect | Duration |
|-------|--------|----------|
| `animate-fade-in` | Fade in + slide up | 0.5s |
| `animate-accordion-down` | Expand height (Radix) | 0.2s |
| `animate-accordion-up` | Collapse height (Radix) | 0.2s |
