# Stagger Animations

> **Framer Motion is installed** — use `framer-motion.md` Skill 6 (`variants` + `staggerChildren`) for all stagger animations.
> This file is a **CSS-only fallback** for environments where Framer Motion is not available.

---

## CSS-Only Fallback

Static list: `animate-fade-in opacity-0` + inline `animationDelay: i * 100ms` + `animationFillMode: 'forwards'`.

Scroll-triggered: combine `useInView` hook (see `entry-scroll.md`) + `transitionDelay: i * 120ms` toggled on `inView`.

Card grid: same pattern with `opacity-0 scale-[0.97]` → `opacity-100 scale-100` on `inView`.

---

## Stagger Delay Reference

| Items | Delay per item | Total duration |
|-------|---------------|----------------|
| 2–4 | 150ms | 450–600ms |
| 5–8 | 100ms | 500–800ms |
| 9–12 | 80ms | 720–960ms |
| 12+ | 60ms | Keep total under 1s |

> Cap total stagger duration at ~1s. If you have 20 items, use 50ms delay, not 100ms.

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Items stay invisible after animation | Add `animationFillMode: 'forwards'` to inline style |
| Delay applied but no transition class | `transitionDelay` only works with `transition-*` class present |
| Too many items all staggering | Cap delay at 60ms for lists > 10 items |
| Stagger without scroll trigger | All items animate immediately on page load before user sees them — use `useInView` |
