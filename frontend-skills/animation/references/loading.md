# Loading Animations

> `animate-spin`, `animate-pulse`, `animate-bounce`, and `Skeleton` basic patterns are already in `references/tailwind-animations.md`. This file covers custom loading patterns and when to use each approach.

---

## Skill 7 — Loading Animations

### Which pattern to use

| Situation | Use |
|-----------|-----|
| Button submitting | `ButtonWithLoader` from `@/components` (see `components` skill) |
| Page / section data loading | `Skeleton` from `@/components` (see `references/tailwind-animations.md`) |
| Inline status (save indicator) | `Loader2 animate-spin` (see `references/tailwind-animations.md`) |
| Long background task | Progress bar (below) |
| AI / streaming response | Loading dots (below) |

---

## Progress Bar

Add token to `global.css` following the pattern in `references/tailwind-animations.md`:

```css
/* apps/frontend/src/app/global.css — @theme block */
--animate-progress: progress 1.5s ease-in-out infinite;

@keyframes progress {
  0%   { width: 0%; }
  50%  { width: 70%; }
  100% { width: 100%; }
}

/* @layer utilities block */
.animate-progress { animation: progress 1.5s ease-in-out infinite; }
```

```tsx
<div className="h-1 w-full bg-muted rounded-full overflow-hidden">
  <div className="h-full bg-primary animate-progress motion-reduce:animate-none" />
</div>
```

---

## Loading Dots

```css
/* apps/frontend/src/app/global.css — @theme block */
--animate-dot-bounce: dot-bounce 1.2s ease-in-out infinite;

@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40%           { transform: scale(1);   opacity: 1; }
}

/* @layer utilities block */
.animate-dot-bounce { animation: dot-bounce 1.2s ease-in-out infinite; }
```

```tsx
export function LoadingDots() {
  return (
    <div className="flex items-center gap-1" aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="size-1.5 rounded-full bg-current animate-dot-bounce motion-reduce:animate-none"
          style={{ animationDelay: `${i * 160}ms` }}
        />
      ))}
    </div>
  )
}
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Custom spinner instead of `Loader2` | Use `Loader2` from lucide-react with `animate-spin` |
| Custom button loading instead of `ButtonWithLoader` | Import from `@/components` |
| Missing `aria-label` on loading containers | Add `aria-label="Loading"` or `aria-busy="true"` |
