# Framer Motion

> Import from `'framer-motion'` — App Router components using motion must be `'use client'`.

---

## Core API

```tsx
import { motion, AnimatePresence, useScroll, useTransform, useAnimate, useReducedMotion, LayoutGroup } from 'framer-motion'
```

### Basic motion element

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: 'easeOut' }}
>
  Content
</motion.div>
```

Any HTML element: `motion.div`, `motion.section`, `motion.button`, `motion.li`, `motion.img`, etc.

---

## Transition Presets

Define once, reuse everywhere:

```tsx
// utils/transitions.ts
export const transitions = {
  spring:  { type: 'spring', stiffness: 300, damping: 30 },
  bouncy:  { type: 'spring', stiffness: 400, damping: 20 },
  smooth:  { duration: 0.4, ease: [0.4, 0, 0.2, 1] },
  snappy:  { duration: 0.2, ease: 'easeOut' },
}
```

```tsx
<motion.div
  initial={{ scale: 0.95, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={transitions.spring}
/>
```

---

## Skill 1 — Component Entry Animations

```tsx
'use client'
import { motion } from 'framer-motion'

export function FeatureCard({ title, description }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
      className="glass rounded-xl p-6"
    >
      <h3>{title}</h3>
      <p>{description}</p>
    </motion.div>
  )
}
```

---

## Skill 2 — Scroll Animations

```tsx
'use client'
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

// Scroll-driven parallax
export function ParallaxSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] })
  const y = useTransform(scrollYProgress, [0, 1], [60, -60])

  return (
    <section ref={ref}>
      <motion.div style={{ y }}>
        <img src="/hero.png" alt="Hero" />
      </motion.div>
    </section>
  )
}

// Fade in when scrolled into view — using whileInView
export function ScrollReveal({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 32 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  )
}
```

> `whileInView` + `viewport={{ once: true }}` replaces the manual `useInView` hook from `entry-scroll.md`.

---

## Skill 3 — Hover Animations

```tsx
'use client'
import { motion } from 'framer-motion'

// Card lift
<motion.div
  className="glass rounded-xl p-6 cursor-pointer"
  whileHover={{ y: -4, boxShadow: '0 20px 40px rgba(0,0,0,0.2)' }}
  transition={{ duration: 0.2 }}
/>

// Scale + glow
<motion.div
  whileHover={{ scale: 1.02 }}
  transition={transitions.snappy}
  className="rounded-xl"
/>
```

---

## Skill 4 — Button Interactions

```tsx
'use client'
import { motion } from 'framer-motion'

// Wrap existing Button or use motion.button
<motion.button
  className="px-6 py-3 rounded-lg bg-primary text-primary-foreground font-medium"
  whileHover={{ scale: 1.03, backgroundColor: 'hsl(var(--primary) / 0.9)' }}
  whileTap={{ scale: 0.96 }}
  transition={transitions.snappy}
>
  Get Started
</motion.button>

// Variants for states (hover, tap, disabled)
const buttonVariants = {
  idle:     { scale: 1 },
  hover:    { scale: 1.03 },
  tap:      { scale: 0.96 },
  disabled: { opacity: 0.5, scale: 1 },
}

<motion.button
  variants={buttonVariants}
  initial="idle"
  whileHover="hover"
  whileTap="tap"
  animate={isDisabled ? 'disabled' : 'idle'}
>
  Action
</motion.button>
```

---

## Skill 5 — Page Transitions (App Router)

```tsx
// components/PageTransition.tsx
'use client'
import { motion, AnimatePresence } from 'framer-motion'

export function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -8 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  )
}
```

```tsx
// app/landing/page.tsx
import { PageTransition } from '@/components/PageTransition'

export default function LandingPage() {
  return (
    <PageTransition>
      <main>...</main>
    </PageTransition>
  )
}
```

> `AnimatePresence` is needed in a layout wrapper to enable `exit` animations between routes.

---

## Skill 6 — Stagger Animations

Variants with `staggerChildren` — the cleanest stagger pattern:

```tsx
'use client'
import { motion } from 'framer-motion'

const container = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.1,    // delay between each child
      delayChildren: 0.2,      // initial delay before first child
    },
  },
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show:   { opacity: 1, y: 0, transition: { duration: 0.4, ease: 'easeOut' } },
}

export function FeatureGrid({ features }) {
  return (
    <motion.ul
      variants={container}
      initial="hidden"
      whileInView="show"
      viewport={{ once: true }}
      className="grid grid-cols-1 md:grid-cols-3 gap-6"
    >
      {features.map((f) => (
        <motion.li key={f.id} variants={item} className="glass rounded-xl p-6">
          <h3>{f.title}</h3>
          <p>{f.description}</p>
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

---

## Skill 7 — Loading Animations

```tsx
'use client'
import { motion } from 'framer-motion'

// Animated loading dots
export function LoadingDots() {
  return (
    <div className="flex items-center gap-1" aria-label="Loading">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="size-1.5 rounded-full bg-current"
          animate={{ scale: [0.6, 1, 0.6], opacity: [0.4, 1, 0.4] }}
          transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.16, ease: 'easeInOut' }}
        />
      ))}
    </div>
  )
}

// Skeleton shimmer (use Skeleton from @/components for standard cases)
// Use motion for custom animated empty states
export function AnimatedEmptyState() {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="flex flex-col items-center gap-4 py-12"
    >
      <p className="text-muted-foreground">No results found</p>
    </motion.div>
  )
}
```

---

## Skill 8 — Layout Animations

### Auto-animate layout changes with `layout` prop

```tsx
'use client'
import { motion, LayoutGroup } from 'framer-motion'

// Expanding card
export function ExpandableCard({ title, content }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <motion.div
      layout                              // animates size/position changes automatically
      className="glass rounded-xl p-6 cursor-pointer"
      onClick={() => setExpanded(!expanded)}
    >
      <motion.h3 layout="position">{title}</motion.h3>
      {expanded && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {content}
        </motion.p>
      )}
    </motion.div>
  )
}

// Shared layout animation (tabs underline, selected item indicator)
export function TabBar({ tabs, active, onSelect }) {
  return (
    <LayoutGroup>
      <div className="flex gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onSelect(tab.id)}
            className="relative px-4 py-2"
          >
            {tab.label}
            {active === tab.id && (
              <motion.div
                layoutId="tab-indicator"             // shared layoutId = smooth move between tabs
                className="absolute inset-x-0 bottom-0 h-0.5 bg-primary"
              />
            )}
          </button>
        ))}
      </div>
    </LayoutGroup>
  )
}
```

---

## Exit Animations with AnimatePresence

```tsx
'use client'
import { motion, AnimatePresence } from 'framer-motion'

// Modal
export function Modal({ open, onClose, children }) {
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div
            key="backdrop"
            className="fixed inset-0 bg-black/50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            key="modal"
            className="fixed inset-x-4 top-1/2 -translate-y-1/2 md:inset-x-auto md:w-full md:max-w-lg mx-auto glass rounded-xl p-6"
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={transitions.spring}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

---

## Reduced Motion

```tsx
'use client'
import { useReducedMotion } from 'framer-motion'

export function AnimatedSection({ children }) {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 24 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.4 }}
    >
      {children}
    </motion.div>
  )
}
```

---

## Reusable Components

Build these from the patterns above as needed:

- **`AnimatedContainer`** — wraps any element with a preset (`fadeUp`/`fadeIn`/`scaleIn`/`slideLeft`), `delay`, and `useReducedMotion()` guard. Use Skill 1 pattern + presets object.
- **`AnimatedList`** — `motion.ul` with `staggerChildren` variants, `whileInView`. Use Skill 6 stagger pattern with `React.Children.map` → `motion.li`.

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| `motion.*` in server component | Add `'use client'` to the file |
| Exit animation not working | Wrap with `<AnimatePresence>` |
| `layout` prop causes jumpy animations | Add `layout` to all siblings too, or wrap in `<LayoutGroup>` |
| `whileInView` fires multiple times | Add `viewport={{ once: true }}` |
| Animating layout-reflow properties | Use `transform`/`opacity` only |
| No reduced motion handling | Use `useReducedMotion()` hook |
