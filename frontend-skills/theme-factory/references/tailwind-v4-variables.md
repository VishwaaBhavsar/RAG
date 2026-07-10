# Tailwind v4 CSS Variables Format

Technical reference for @theme directive and CSS variable structure.

## @theme Directive

Tailwind v4 introduces the `@theme` directive for defining design tokens:

```css
@theme {
  /* All your design tokens here */
  --color-primary: oklch(55% 0.15 250);
  --font-sans: 'Inter', system-ui, sans-serif;
  --radius-md: 0.5rem;
}
```

## Complete Theme Structure

```css
@theme {
  /* ================================
     COLOR SYSTEM
     ================================ */

  /* Primary Palette */
  --color-primary-50: oklch(97% 0.01 250);
  --color-primary-100: oklch(94% 0.02 250);
  --color-primary-200: oklch(88% 0.04 250);
  --color-primary-300: oklch(78% 0.08 250);
  --color-primary-400: oklch(65% 0.12 250);
  --color-primary-500: oklch(55% 0.15 250);
  --color-primary-600: oklch(48% 0.14 250);
  --color-primary-700: oklch(40% 0.12 250);
  --color-primary-800: oklch(32% 0.10 250);
  --color-primary-900: oklch(25% 0.08 250);
  --color-primary-950: oklch(18% 0.06 250);

  /* Secondary Palette */
  --color-secondary-50: oklch(97% 0.005 250);
  --color-secondary-100: oklch(95% 0.008 250);
  /* ... continue for full scale */

  /* Gray/Neutral Palette */
  --color-gray-50: oklch(98% 0.003 250);
  --color-gray-100: oklch(96% 0.005 250);
  --color-gray-200: oklch(92% 0.005 250);
  --color-gray-300: oklch(87% 0.008 250);
  --color-gray-400: oklch(70% 0.01 250);
  --color-gray-500: oklch(55% 0.01 250);
  --color-gray-600: oklch(45% 0.01 250);
  --color-gray-700: oklch(35% 0.01 250);
  --color-gray-800: oklch(25% 0.01 250);
  --color-gray-900: oklch(18% 0.01 250);
  --color-gray-950: oklch(12% 0.01 250);

  /* Semantic Colors */
  --color-background: oklch(99% 0.005 250);
  --color-foreground: oklch(15% 0.02 250);
  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(15% 0.02 250);
  --color-popover: oklch(100% 0 0);
  --color-popover-foreground: oklch(15% 0.02 250);
  --color-muted: oklch(96% 0.005 250);
  --color-muted-foreground: oklch(45% 0.02 250);
  --color-border: oklch(90% 0.01 250);
  --color-input: oklch(90% 0.01 250);
  --color-ring: oklch(55% 0.15 250);

  /* Component Colors */
  --color-primary: oklch(55% 0.15 250);
  --color-primary-foreground: oklch(99% 0.005 250);

  --color-secondary: oklch(96% 0.005 250);
  --color-secondary-foreground: oklch(25% 0.02 250);

  --color-accent: oklch(96% 0.005 250);
  --color-accent-foreground: oklch(25% 0.02 250);

  --color-destructive: oklch(55% 0.22 25);
  --color-destructive-foreground: oklch(99% 0.005 25);

  /* Status Colors */
  --color-success: oklch(55% 0.16 145);
  --color-success-foreground: oklch(99% 0.005 145);

  --color-warning: oklch(75% 0.15 85);
  --color-warning-foreground: oklch(25% 0.05 85);

  --color-info: oklch(55% 0.15 250);
  --color-info-foreground: oklch(99% 0.005 250);

  /* ================================
     TYPOGRAPHY
     ================================ */

  /* Font Families */
  --font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
  --font-serif: 'Georgia', ui-serif, serif;
  --font-mono: 'JetBrains Mono', ui-monospace, monospace;
  --font-heading: 'Plus Jakarta Sans', var(--font-sans);

  /* Font Sizes (with line-height) */
  --text-xs: 0.75rem;
  --text-xs--line-height: 1rem;
  --text-sm: 0.875rem;
  --text-sm--line-height: 1.25rem;
  --text-base: 1rem;
  --text-base--line-height: 1.5rem;
  --text-lg: 1.125rem;
  --text-lg--line-height: 1.75rem;
  --text-xl: 1.25rem;
  --text-xl--line-height: 1.75rem;
  --text-2xl: 1.5rem;
  --text-2xl--line-height: 2rem;
  --text-3xl: 1.875rem;
  --text-3xl--line-height: 2.25rem;
  --text-4xl: 2.25rem;
  --text-4xl--line-height: 2.5rem;
  --text-5xl: 3rem;
  --text-5xl--line-height: 1;
  --text-6xl: 3.75rem;
  --text-6xl--line-height: 1;

  /* Font Weights */
  --font-weight-thin: 100;
  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
  --font-weight-black: 900;

  /* Letter Spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0em;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;

  /* ================================
     SPACING
     ================================ */

  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0_5: 0.125rem;
  --spacing-1: 0.25rem;
  --spacing-1_5: 0.375rem;
  --spacing-2: 0.5rem;
  --spacing-2_5: 0.625rem;
  --spacing-3: 0.75rem;
  --spacing-3_5: 0.875rem;
  --spacing-4: 1rem;
  --spacing-5: 1.25rem;
  --spacing-6: 1.5rem;
  --spacing-7: 1.75rem;
  --spacing-8: 2rem;
  --spacing-9: 2.25rem;
  --spacing-10: 2.5rem;
  --spacing-12: 3rem;
  --spacing-14: 3.5rem;
  --spacing-16: 4rem;
  --spacing-20: 5rem;
  --spacing-24: 6rem;
  --spacing-28: 7rem;
  --spacing-32: 8rem;
  --spacing-36: 9rem;
  --spacing-40: 10rem;
  --spacing-44: 11rem;
  --spacing-48: 12rem;
  --spacing-52: 13rem;
  --spacing-56: 14rem;
  --spacing-60: 15rem;
  --spacing-64: 16rem;

  /* ================================
     BORDER RADIUS
     ================================ */

  --radius-none: 0;
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-3xl: 1.5rem;
  --radius-full: 9999px;

  /* ================================
     SHADOWS
     ================================ */

  --shadow-sm: 0 1px 2px 0 oklch(0% 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px oklch(0% 0 0 / 0.1), 0 2px 4px -2px oklch(0% 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px oklch(0% 0 0 / 0.1), 0 4px 6px -4px oklch(0% 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px oklch(0% 0 0 / 0.1), 0 8px 10px -6px oklch(0% 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px oklch(0% 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 oklch(0% 0 0 / 0.05);
  --shadow-none: 0 0 0 0 transparent;

  /* ================================
     TRANSITIONS
     ================================ */

  --duration-75: 75ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
  --duration-700: 700ms;
  --duration-1000: 1000ms;

  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* ================================
     Z-INDEX
     ================================ */

  --z-0: 0;
  --z-10: 10;
  --z-20: 20;
  --z-30: 30;
  --z-40: 40;
  --z-50: 50;
  --z-auto: auto;
}
```

## Dark Mode Theme

Use the `dark` variant for dark mode:

```css
@theme dark {
  /* Override only what changes in dark mode */
  --color-background: oklch(12% 0.015 250);
  --color-foreground: oklch(95% 0.01 250);
  --color-card: oklch(15% 0.015 250);
  --color-card-foreground: oklch(95% 0.01 250);
  --color-popover: oklch(15% 0.015 250);
  --color-popover-foreground: oklch(95% 0.01 250);
  --color-muted: oklch(20% 0.015 250);
  --color-muted-foreground: oklch(65% 0.01 250);
  --color-border: oklch(25% 0.015 250);
  --color-input: oklch(20% 0.015 250);
  --color-ring: oklch(55% 0.15 250);

  --color-primary: oklch(65% 0.15 250);
  --color-primary-foreground: oklch(12% 0.015 250);

  --color-secondary: oklch(20% 0.015 250);
  --color-secondary-foreground: oklch(95% 0.01 250);

  --color-accent: oklch(20% 0.015 250);
  --color-accent-foreground: oklch(95% 0.01 250);

  /* Shadows in dark mode */
  --shadow-sm: 0 1px 2px 0 oklch(0% 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px oklch(0% 0 0 / 0.4);
  --shadow-lg: 0 10px 15px -3px oklch(0% 0 0 / 0.4);
}
```

## Using Variables in Tailwind Classes

```html
<!-- Direct usage -->
<div class="bg-primary text-primary-foreground">
  Primary colored element
</div>

<div class="bg-card text-card-foreground border border-border rounded-lg shadow-md">
  Card component
</div>

<!-- With opacity modifier -->
<div class="bg-primary/50">
  50% opacity primary background
</div>

<!-- Custom values -->
<div class="bg-[oklch(55%_0.15_250)]">
  Custom OKLCH color
</div>
```

## File Organization

Place theme in your CSS entry point:

```css
/* app/globals.css or styles/main.css */

@import "tailwindcss";

@theme {
  /* Your theme tokens */
}

@theme dark {
  /* Dark mode overrides */
}

/* Component styles */
@layer components {
  .btn-primary {
    @apply bg-primary text-primary-foreground rounded-md px-4 py-2;
  }
}
```

## Integration with shadcn/ui

The token names are compatible with shadcn/ui:

```css
@theme {
  /* shadcn/ui compatible tokens */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(15% 0.02 250);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(15% 0.02 250);

  --color-popover: oklch(100% 0 0);
  --color-popover-foreground: oklch(15% 0.02 250);

  --color-primary: oklch(55% 0.15 250);
  --color-primary-foreground: oklch(99% 0.005 250);

  --color-secondary: oklch(96% 0.005 250);
  --color-secondary-foreground: oklch(25% 0.02 250);

  --color-muted: oklch(96% 0.005 250);
  --color-muted-foreground: oklch(45% 0.02 250);

  --color-accent: oklch(96% 0.005 250);
  --color-accent-foreground: oklch(25% 0.02 250);

  --color-destructive: oklch(55% 0.22 25);
  --color-destructive-foreground: oklch(99% 0.005 25);

  --color-border: oklch(90% 0.01 250);
  --color-input: oklch(90% 0.01 250);
  --color-ring: oklch(55% 0.15 250);

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}
```
