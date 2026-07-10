# Navbar Animations

> Single source of truth for all responsive navbar animation patterns.
> **Decision first:** check if `framer-motion` is installed, then follow the matching path below.
>
> - ✅ Framer Motion installed → **Framer Motion Path** (Skills 1–6)
> - ❌ Not installed → **CSS-Only Path** (Skills 7–11)

---

## Setup (both paths)

```tsx
'use client'
import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'
import Link from 'next/link'

const NAV_LINKS = [
  { label: 'Features',     href: '#features' },
  { label: 'How it Works', href: '#how-it-works' },
  { label: 'About',        href: '#about' },
]
```

Framer Motion path also adds:
```tsx
import { motion, AnimatePresence } from 'framer-motion'

// framer-motion v12 — number[] not assignable to Easing; must be a typed 4-tuple
const EASE: [number, number, number, number] = [0.4, 0, 0.2, 1]
```

---

# ✅ Framer Motion Path

---

## Skill 1 — Scroll-Aware Navbar Bar (Framer Motion)

Animates in on mount. Transitions to frosted glass at `scrollY > 20`.
Also applies frosted glass when `menuOpen` so the bar is always readable behind the open drawer.

```tsx
const [scrolled, setScrolled] = useState(false)
const [menuOpen, setMenuOpen] = useState(false)

useEffect(() => {
  const handler = () => setScrolled(window.scrollY > 20)
  window.addEventListener('scroll', handler, { passive: true })
  return () => window.removeEventListener('scroll', handler)
}, [])
```

```tsx
<motion.nav
  initial={{ opacity: 0, y: -16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, ease: 'easeOut' }}
  className={cn(
    'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
    scrolled || menuOpen
      ? 'bg-background/95 backdrop-blur-md shadow-sm border-b border-border'
      : 'bg-transparent'
  )}
>
  <div className="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
    {/* Logo, desktop links, desktop CTAs, mobile controls */}
  </div>
</motion.nav>
```

---

## Skill 2 — Desktop vs Mobile Layout

Desktop links and CTAs use `hidden md:flex`. Mobile gets a visible primary CTA + hamburger.
Never hide the primary CTA behind the hamburger — conversion action must always be one tap away.

```tsx
{/* Desktop links */}
<div className="hidden md:flex items-center gap-8">
  {NAV_LINKS.map((item) => (
    <a key={item.label} href={item.href}
      className="text-muted-foreground hover:text-foreground text-sm font-medium transition-colors duration-200">
      {item.label}
    </a>
  ))}
</div>

{/* Desktop CTAs */}
<div className="hidden md:flex items-center gap-3">
  <Link href="/auth/login" className="text-muted-foreground hover:text-foreground text-sm font-medium transition-colors">
    Sign in
  </Link>
  <Link href="/auth/login"
    className="inline-flex items-center gap-1.5 rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 active:scale-95 transition-all duration-150">
    Get Started →
  </Link>
</div>

{/* Mobile: primary CTA always visible + hamburger */}
<div className="flex md:hidden items-center gap-3">
  <Link href="/auth/login"
    className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground hover:bg-primary/90 active:scale-95 transition-all duration-150">
    Get Started
  </Link>
  <button
    onClick={() => setMenuOpen((o) => !o)}
    aria-label={menuOpen ? 'Close menu' : 'Open menu'}
    aria-expanded={menuOpen}
    className="h-9 w-9 flex items-center justify-center rounded-lg text-foreground hover:bg-muted transition-colors">
    {/* Icon swap — see Skill 3 */}
  </button>
</div>
```

---

## Skill 3 — Hamburger Icon Swap (Framer Motion)

`AnimatePresence mode="wait"` ensures ☰ fully exits before ✕ enters — no visual overlap.
`initial={false}` prevents the icon animating on first render.

```tsx
<AnimatePresence mode="wait" initial={false}>
  {menuOpen ? (
    <motion.svg key="close"
      initial={{ opacity: 0, rotate: -45 }} animate={{ opacity: 1, rotate: 0 }}
      exit={{ opacity: 0, rotate: 45 }} transition={{ duration: 0.18 }}
      className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
    </motion.svg>
  ) : (
    <motion.svg key="burger"
      initial={{ opacity: 0, rotate: 45 }} animate={{ opacity: 1, rotate: 0 }}
      exit={{ opacity: 0, rotate: -45 }} transition={{ duration: 0.18 }}
      className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
    </motion.svg>
  )}
</AnimatePresence>
```

---

## Skill 4 — Body Scroll Lock

Required in both paths. Lock body scroll when drawer is open so the page behind doesn't scroll through.

```tsx
useEffect(() => {
  document.body.style.overflow = menuOpen ? 'hidden' : ''
  return () => { document.body.style.overflow = '' }
}, [menuOpen])
```

---

## Skill 5 — Mobile Drawer + Backdrop (Framer Motion)

Drawer and backdrop must be **siblings to `<nav>`**, not children — `position: fixed` inside `<nav>` can clip.
Wrap both in a React fragment `<>`. `AnimatePresence` handles true entry + exit for both elements.

```tsx
<AnimatePresence>
  {menuOpen && (
    <>
      {/* Backdrop */}
      <motion.div key="backdrop"
        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
        className="fixed inset-0 z-40 bg-black/20 backdrop-blur-sm md:hidden"
        onClick={() => setMenuOpen(false)}
      />

      {/* Drawer panel — positioned below the navbar */}
      <motion.div key="drawer"
        initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -8 }}
        transition={{ duration: 0.22, ease: EASE }}
        className="fixed top-[65px] left-4 right-4 z-50 rounded-2xl bg-background shadow-xl border border-border p-5 md:hidden">
        {/* Nav links + auth CTAs — see Skill 6 */}
      </motion.div>
    </>
  )}
</AnimatePresence>
```

---

## Skill 6 — Staggered Nav Links + Auth CTAs (Framer Motion)

Each link animates in with a staggered delay. All links/CTAs call `setMenuOpen(false)` on click.

```tsx
const handleNavClick = () => setMenuOpen(false)
```

```tsx
<nav className="flex flex-col gap-1">
  {NAV_LINKS.map((item, i) => (
    <motion.a key={item.label} href={item.href} onClick={handleNavClick}
      initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }}
      transition={{ delay: i * 0.06, duration: 0.2 }}
      className="flex items-center rounded-xl px-4 py-3 text-sm font-medium text-foreground hover:bg-muted transition-colors">
      {item.label}
    </motion.a>
  ))}
</nav>

<div className="mt-4 pt-4 border-t border-border flex flex-col gap-2">
  <Link href="/auth/login" onClick={handleNavClick}
    className="flex items-center justify-center rounded-xl border border-border px-4 py-2.5 text-sm font-semibold text-foreground hover:bg-muted transition-colors">
    Sign in
  </Link>
  <Link href="/auth/login" onClick={handleNavClick}
    className="flex items-center justify-center gap-2 rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 transition-colors">
    Get Started free →
  </Link>
</div>
```

---

## Framer Motion — Full Component Structure

```tsx
export function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {                                         // Skill 1
    const handler = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', handler, { passive: true })
    return () => window.removeEventListener('scroll', handler)
  }, [])

  useEffect(() => {                                         // Skill 4
    document.body.style.overflow = menuOpen ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [menuOpen])

  const handleNavClick = () => setMenuOpen(false)

  return (
    <>
      <motion.nav ...>                                      {/* Skill 1 — bar */}
        <div className="...flex items-center justify-between">
          {/* Logo */}
          <div className="hidden md:flex ..."> ... </div>   {/* Skill 2 — desktop links */}
          <div className="hidden md:flex ..."> ... </div>   {/* Skill 2 — desktop CTAs */}
          <div className="flex md:hidden ...">              {/* Skill 2 — mobile CTA + burger */}
            <Link ...>Get Started</Link>
            <button ...><AnimatePresence ...> ... </AnimatePresence></button>  {/* Skill 3 */}
          </div>
        </div>
      </motion.nav>

      <AnimatePresence>                                     {/* Skill 5 — drawer + backdrop */}
        {menuOpen && (
          <>
            <motion.div key="backdrop" ... />
            <motion.div key="drawer" ...>
              {/* Skill 6 — stagger links + CTAs */}
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
```

---

# ❌ CSS-Only Path (Framer Motion not installed)

> Framer Motion **is installed** in this project — use the path above. Only use this section if FM is explicitly unavailable.

Key differences vs FM path:
- **Bar**: plain `<nav>` + `transition-all`, no mount animation
- **Icon swap**: two `absolute` SVGs, toggle `opacity/rotate/scale` via `cn()`
- **Drawer**: `grid-rows-[0fr]→[1fr]` + `opacity` (stays in DOM); inner `overflow-hidden` div clips during transition; add `pointer-events-none` when closed
- **Backdrop**: `opacity-0 pointer-events-none` toggle (stays in DOM)
- **Body scroll lock**: same `useEffect` as Skill 4

---

## Framer Motion vs CSS-Only — Differences

| Behaviour | Framer Motion (Skills 1–6) | CSS-Only (Skills 7–11) |
|-----------|---------------------------|------------------------|
| Navbar mount | `motion.nav` fade+slide in | Plain `<nav>`, no entry animation |
| Drawer entry/exit | True unmount with `AnimatePresence` | Stays in DOM; `grid-rows` + `opacity` toggle |
| Icon swap | `AnimatePresence mode="wait"` sequential | Layered icons, CSS crossfade |
| Backdrop exit | True unmount via `AnimatePresence` | `opacity-0 pointer-events-none` |
| Stagger links | `motion.a` with `delay: i * 0.06` | All links appear together |
| Body scroll lock | JS `useEffect` (same) | JS `useEffect` (same) |
| Bundle impact | +framer-motion (~40kb gzip) | Zero additional |

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Exit animation not playing (Framer Motion) | Wrap drawer + backdrop in `<AnimatePresence>` |
| Both icons visible at once (Framer Motion) | Use `AnimatePresence mode="wait"` on icon swap |
| Icon animates on first render (Framer Motion) | Add `initial={false}` to icon `AnimatePresence` |
| TS error: `number[]` not assignable to `Easing` | Type as `const EASE: [number, number, number, number]` (v12) |
| Drawer clips when inside `<nav>` | Render drawer outside `<nav>` — sibling in a fragment `<>` |
| Drawer visible but not interactive (CSS) | Remove `pointer-events-none` when `menuOpen === true` |
| Height doesn't animate (CSS) | Wrap in `overflow-hidden` div inside `grid` wrapper |
| `height: 0 → auto` won't animate | Use `grid-rows-[0fr→1fr]` trick, never animate `height` directly |
| Page scrolls behind open drawer | `document.body.style.overflow = 'hidden'` in `useEffect` |
| Nav bar transparent behind open drawer | Apply frosted bg when `menuOpen === true`, not only when scrolled |
