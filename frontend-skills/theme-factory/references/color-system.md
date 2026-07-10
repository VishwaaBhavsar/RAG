# OKLCH Color System & 60-30-10 Rule

Technical guide for perceptually uniform color generation.

## OKLCH Color Space

### What is OKLCH?

OKLCH is a perceptually uniform color space consisting of:

```
oklch(L C H)

L = Lightness (0% = black, 100% = white)
C = Chroma (0 = gray, ~0.4 = maximum saturation)
H = Hue (0-360 degrees on color wheel)
```

### Why OKLCH?

1. **Perceptual uniformity**: Equal numerical changes = equal visual changes
2. **Predictable lightness**: Easy to create accessible color scales
3. **Independent channels**: Adjust L, C, H separately without side effects
4. **Wide gamut**: Supports P3 displays
5. **Native CSS support**: `oklch()` function in modern browsers

### OKLCH vs Other Spaces

| Feature | HSL | RGB | OKLCH |
|---------|-----|-----|-------|
| Perceptually uniform | No | No | Yes |
| Easy lightness control | Partial | No | Yes |
| Wide gamut support | No | No | Yes |
| CSS native | Yes | Yes | Yes |
| Predictable mixing | No | No | Yes |

---

## Color Scale Generation

### Creating a 10-Step Scale

Generate consistent color scales by varying lightness:

```css
/* Primary scale - Blue (hue 250) */
--color-primary-50:  oklch(97% 0.01 250);  /* Very light */
--color-primary-100: oklch(94% 0.02 250);
--color-primary-200: oklch(88% 0.04 250);
--color-primary-300: oklch(78% 0.08 250);
--color-primary-400: oklch(65% 0.12 250);
--color-primary-500: oklch(55% 0.15 250);  /* Base color */
--color-primary-600: oklch(48% 0.14 250);
--color-primary-700: oklch(40% 0.12 250);
--color-primary-800: oklch(32% 0.10 250);
--color-primary-900: oklch(25% 0.08 250);
--color-primary-950: oklch(18% 0.06 250);  /* Very dark */
```

### Scale Generation Rules

1. **Lightness progression**: Even steps from 97% to ~18%
2. **Chroma curve**: Peak at 500, reduce at extremes
3. **Hue consistency**: Keep hue constant (or slight shift for warmth)

```javascript
// Generate scale programmatically
function generateScale(hue, peakChroma = 0.15) {
  const steps = [
    { step: 50,  L: 97, C: peakChroma * 0.07 },
    { step: 100, L: 94, C: peakChroma * 0.13 },
    { step: 200, L: 88, C: peakChroma * 0.27 },
    { step: 300, L: 78, C: peakChroma * 0.53 },
    { step: 400, L: 65, C: peakChroma * 0.80 },
    { step: 500, L: 55, C: peakChroma * 1.00 },  // Peak
    { step: 600, L: 48, C: peakChroma * 0.93 },
    { step: 700, L: 40, C: peakChroma * 0.80 },
    { step: 800, L: 32, C: peakChroma * 0.67 },
    { step: 900, L: 25, C: peakChroma * 0.53 },
    { step: 950, L: 18, C: peakChroma * 0.40 },
  ];

  return steps.map(s =>
    `--color-primary-${s.step}: oklch(${s.L}% ${s.C.toFixed(3)} ${hue});`
  );
}
```

---

## 60-30-10 Rule

### Distribution Principle

The 60-30-10 rule creates visual harmony:

```
60% - Dominant color (background, large areas)
30% - Secondary color (supporting elements)
10% - Accent color (highlights, CTAs)
```

### Application in UI

```
60% Dominant:
- Page background
- Card backgrounds
- Large content areas
- Negative space

30% Secondary:
- Navigation
- Borders
- Secondary buttons
- Supporting text
- Muted backgrounds

10% Accent:
- Primary CTAs
- Links
- Active states
- Notifications
- Highlights
```

### Implementation Example

```css
/* 60% Dominant - Background */
--color-background: oklch(99% 0.005 250);
--color-card: oklch(100% 0 0);
--color-muted: oklch(96% 0.008 250);

/* 30% Secondary - Supporting */
--color-border: oklch(90% 0.01 250);
--color-secondary: oklch(96% 0.008 250);
--color-muted-foreground: oklch(45% 0.02 250);

/* 10% Accent - Highlights */
--color-primary: oklch(55% 0.15 250);
--color-accent: oklch(60% 0.18 30);
```

---

## Color Harmony Techniques

### Monochromatic
Same hue, varying lightness and chroma:

```css
--color-mono-light: oklch(85% 0.08 250);
--color-mono-base:  oklch(55% 0.15 250);
--color-mono-dark:  oklch(35% 0.12 250);
```

### Complementary
Opposite hues (180° apart):

```css
--color-primary: oklch(55% 0.15 250);   /* Blue */
--color-complement: oklch(55% 0.15 70); /* Orange (250 + 180 = 430 → 70) */
```

### Analogous
Adjacent hues (30° apart):

```css
--color-primary: oklch(55% 0.15 250);   /* Blue */
--color-analog-1: oklch(55% 0.15 220);  /* Blue-cyan */
--color-analog-2: oklch(55% 0.15 280);  /* Blue-purple */
```

### Split Complementary
Primary + two colors adjacent to complement:

```css
--color-primary: oklch(55% 0.15 250);   /* Blue */
--color-split-1: oklch(55% 0.15 40);    /* Red-orange */
--color-split-2: oklch(55% 0.15 100);   /* Yellow-green */
```

### Triadic
Three colors 120° apart:

```css
--color-primary: oklch(55% 0.15 250);   /* Blue */
--color-triad-1: oklch(55% 0.15 10);    /* Red */
--color-triad-2: oklch(55% 0.15 130);   /* Green */
```

---

## Semantic Color Mapping

### Status Colors

```css
/* Success - Green family */
--color-success: oklch(55% 0.16 145);
--color-success-foreground: oklch(99% 0.005 145);

/* Warning - Yellow/Orange family */
--color-warning: oklch(75% 0.15 85);
--color-warning-foreground: oklch(25% 0.05 85);

/* Error/Destructive - Red family */
--color-destructive: oklch(55% 0.22 25);
--color-destructive-foreground: oklch(99% 0.005 25);

/* Info - Blue family */
--color-info: oklch(55% 0.15 250);
--color-info-foreground: oklch(99% 0.005 250);
```

### Interactive States

```css
/* Base button */
--btn-bg: oklch(55% 0.15 250);

/* Hover - Slightly lighter or darker */
--btn-hover: oklch(50% 0.16 250);

/* Active - Darker */
--btn-active: oklch(45% 0.14 250);

/* Disabled - Desaturated */
--btn-disabled: oklch(70% 0.03 250);
```

---

## Dark Mode Transformation

### Lightness Inversion

For dark mode, invert lightness while maintaining chroma:

```css
/* Light mode */
--color-background: oklch(99% 0.005 250);  /* L: 99% */
--color-foreground: oklch(15% 0.02 250);   /* L: 15% */

/* Dark mode - invert */
--color-background: oklch(12% 0.015 250);  /* L: 12% */
--color-foreground: oklch(95% 0.01 250);   /* L: 95% */
```

### Primary Color Adjustment

Primary colors often need slight lightness boost in dark mode:

```css
/* Light mode primary */
--color-primary: oklch(55% 0.15 250);

/* Dark mode primary - lift lightness */
--color-primary: oklch(65% 0.15 250);
```

### Chroma Considerations

- Reduce chroma slightly for large dark surfaces
- Maintain chroma for accent colors
- Watch for OLED issues with pure black

---

## Practical Tips

### 1. Start with the 500 Step
Define your base color at 500, then derive the scale.

### 2. Test Lightness Visually
OKLCH lightness is perceptual - trust your eyes.

### 3. Chroma Limits
- Most UI: 0.05-0.20
- Accents: up to 0.25
- Grays: 0.005-0.02

### 4. Hue Shifts
Slight hue shift toward warmth (+ degrees) for more vibrant scales.

### 5. Browser Support
OKLCH has excellent modern browser support. Provide fallbacks for older browsers:

```css
/* Fallback */
--color-primary: hsl(220, 60%, 50%);
/* Modern */
--color-primary: oklch(55% 0.15 250);
```
