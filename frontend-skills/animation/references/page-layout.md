# Page Transitions + Layout Animations

> **Framer Motion is installed** — use `framer-motion.md` Skills 5 + 8 for page transitions (`AnimatePresence`) and layout animations (`layout`, `layoutId`, `LayoutGroup`).

## CSS-Only Fallback — Page Transitions

- Route entry: `<main className="animate-fade-in motion-reduce:animate-none">` in `page.tsx`
- Deliberate entry: add `--animate-page-enter: page-enter 0.35s ease-out` token to `global.css @theme` (same keyframe pattern as `tailwind-animations.md`)
- Tab switching: toggle `opacity-100 animate-fade-in` vs `opacity-0 pointer-events-none absolute` via `cn()`

---

## Layout Animations

Animating layout changes: expanding sections, collapsing drawers, sliding panels.

### Accordion / collapsible (Radix-based)

The existing `animate-accordion-down` / `animate-accordion-up` tokens handle Radix `<Accordion>` automatically via shadcn. Use `Accordion` from `@/components`:

```tsx
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@/components'

// Animation is built-in via animate-accordion-down/up tokens
<Accordion type="single" collapsible>
  <AccordionItem value="item-1">
    <AccordionTrigger>Is it animated?</AccordionTrigger>
    <AccordionContent>Yes, automatically.</AccordionContent>
  </AccordionItem>
</Accordion>
```

### Smooth height expand (CSS-only pattern)

For custom collapsibles without Radix:

```tsx
'use client'
import { useState } from 'react'
import { cn } from '@/lib/utils'

export function Collapsible({ label, children }) {
  const [open, setOpen] = useState(false)

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-2 w-full text-left"
      >
        <ChevronDown className={cn(
          'size-4 transition-transform duration-200 motion-reduce:transition-none',
          open && 'rotate-180'
        )} />
        {label}
      </button>
      <div className={cn(
        'grid transition-all duration-300 ease-out motion-reduce:transition-none',
        open ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'
      )}>
        <div className="overflow-hidden">{children}</div>
      </div>
    </div>
  )
}
```

> The `grid-rows-[0fr]` → `grid-rows-[1fr]` trick animates height without JS measurement and avoids layout reflow.

### Sidebar / drawer slide

```tsx
'use client'
import { cn } from '@/lib/utils'

export function Sidebar({ open, children }) {
  return (
    <aside className={cn(
      'fixed inset-y-0 left-0 w-64 bg-card border-r border-border',
      'transition-transform duration-300 ease-out',
      'motion-reduce:transition-none',
      open ? 'translate-x-0' : '-translate-x-full'
    )}>
      {children}
    </aside>
  )
}
```

### Notification / toast slide-in

```tsx
// Slide in from bottom-right
<div className="
  fixed bottom-4 right-4
  animate-slide-up motion-reduce:animate-none
">
  <div className="glass rounded-lg p-4 shadow-lg">
    Notification message
  </div>
</div>
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Animating `height: 0` → `height: auto` directly | Use `grid-rows-[0fr]` → `grid-rows-[1fr]` trick instead |
| Page transition flickers on fast nav | Keep duration under 350ms; use `ease-out` not `ease-in-out` |
| Drawer blocks interaction when closed | Add `pointer-events-none` when `translate-x-full` |
| Animation replays on re-render | Apply animation class conditionally only on mount |
