# Hover Animations + Button Interactions

> Base `transition-*` classes and basic `hover:scale-105` patterns are in `references/tailwind-animations.md`. This file covers compound hover patterns and button press interactions.

---

## Skill 3 — Hover Animations

### Card hover — lift + border

```tsx
<div className="
  border border-border rounded-lg p-6
  transition-all duration-200
  hover:border-primary/30 hover:shadow-lg hover:-translate-y-1
  motion-reduce:hover:translate-y-0 motion-reduce:transition-none
">
```

### Glass card hover (uses `glass` utility from `styling` skill)

```tsx
<div className="
  glass transition-all duration-200
  hover:bg-card/80 hover:border-border/80 hover:shadow-lg
  motion-reduce:transition-none
">
```

### Image zoom inside container

```tsx
<div className="overflow-hidden rounded-lg">
  <img className="
    w-full transition-transform duration-300
    hover:scale-105 motion-reduce:hover:scale-100
  " src={src} alt={alt} />
</div>
```

### Link — underline slide-in

```tsx
<a className="
  relative
  after:absolute after:bottom-0 after:left-0
  after:h-px after:w-0 after:bg-primary
  after:transition-all after:duration-200
  hover:after:w-full
  motion-reduce:after:hidden
">
  Learn more
</a>
```

### Link — icon shift on hover

```tsx
<Link className="
  flex items-center gap-1 text-muted-foreground
  transition-colors duration-150 hover:text-primary
  hover:[&>svg]:translate-x-0.5 [&>svg]:transition-transform
  motion-reduce:transition-none motion-reduce:[&>svg]:transition-none
">
  View details <ArrowRight className="size-4" />
</Link>
```

### Glow hover (uses `glow` utility from `styling` skill)

```tsx
<div className="
  rounded-xl transition-shadow duration-300
  hover:glow motion-reduce:hover:shadow-none
">
```

---

## Skill 4 — Button Interactions

For `Button` and `ButtonWithLoader` — import from `@/components` (see `components` skill).

### Add press feedback to existing `Button`

```tsx
import { Button } from '@/components'

<Button className="active:scale-95 transition-transform motion-reduce:active:scale-100">
  Click me
</Button>
```

### Custom interactive element

```tsx
<button className="
  px-4 py-2 rounded-lg bg-primary text-primary-foreground
  transition-all duration-150
  hover:bg-primary/90 hover:shadow-md
  active:scale-95 active:shadow-sm
  focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring
  disabled:opacity-50 disabled:pointer-events-none
  motion-reduce:transition-none motion-reduce:active:scale-100
">
```

### Icon button

```tsx
<button className="
  size-9 rounded-md flex items-center justify-center
  text-muted-foreground transition-colors duration-150
  hover:text-foreground hover:bg-muted
  active:bg-muted/70
  motion-reduce:transition-none
">
  <Settings className="size-4" />
</button>
```

---

## Timing Reference

| Interaction | Duration |
|-------------|----------|
| Button press `active:` | 100–150ms |
| Color / text change | 150–200ms |
| Card lift / shadow | 200ms |
| Scale / transform | 200ms |
| Glow effect | 300ms |

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| No `transition-*` paired with `hover:` | Changes are instant without it |
| Image scale without `overflow-hidden` | Scale bleeds outside container |
| No `focus-visible` on custom buttons | Add `focus-visible:ring-2 focus-visible:ring-ring` |
| No `active:` state | Users need press feedback — add `active:scale-95` |
