# Accessibility & WCAG Compliance

Ensuring all generated themes meet accessibility standards.

## WCAG Contrast Requirements

### Minimum Ratios

| Content Type | WCAG AA | WCAG AAA |
|--------------|---------|----------|
| Normal text (< 18pt) | 4.5:1 | 7:1 |
| Large text (≥ 18pt or 14pt bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |
| Non-text decorative elements | No requirement | No requirement |

### Contrast Formula

```javascript
// Relative luminance from OKLCH lightness
// Note: This is an approximation; precise calculation requires color space conversion

function getRelativeLuminance(oklchLightness) {
  // OKLCH lightness maps roughly to perceived lightness
  // For precise calculations, convert to sRGB then calculate
  return Math.pow(oklchLightness / 100, 2.2);
}

function getContrastRatio(L1, L2) {
  const lighter = Math.max(L1, L2);
  const darker = Math.min(L1, L2);
  return (lighter + 0.05) / (darker + 0.05);
}
```

## OKLCH Accessibility Shortcuts

### Lightness-Based Estimation

With OKLCH, we can estimate contrast using lightness difference:

```
For WCAG AA (4.5:1):
- Background L < 50%: Text should have L > 75%
- Background L > 50%: Text should have L < 25%

For WCAG AAA (7:1):
- Background L < 40%: Text should have L > 85%
- Background L > 60%: Text should have L < 15%
```

### Safe Combinations

```css
/* Light backgrounds (L > 90%) */
--color-background: oklch(99% 0.005 250);  /* L: 99% */
--color-foreground: oklch(15% 0.02 250);   /* L: 15% - Safe */
--color-muted-foreground: oklch(45% 0.02 250); /* L: 45% - Check */

/* Dark backgrounds (L < 20%) */
--color-background: oklch(12% 0.015 250);  /* L: 12% */
--color-foreground: oklch(95% 0.01 250);   /* L: 95% - Safe */
--color-muted-foreground: oklch(65% 0.01 250); /* L: 65% - Safe */

/* Primary button */
--color-primary: oklch(55% 0.15 250);       /* L: 55% */
--color-primary-foreground: oklch(99% 0.005 250); /* L: 99% - Safe */
```

## Verification Checklist

### For Every Theme

1. **Text on Background**
   - [ ] Body text: foreground/background ≥ 4.5:1
   - [ ] Muted text: muted-foreground/background ≥ 4.5:1
   - [ ] Headings (large): foreground/background ≥ 3:1

2. **Interactive Elements**
   - [ ] Primary button: primary-foreground/primary ≥ 4.5:1
   - [ ] Secondary button: secondary-foreground/secondary ≥ 4.5:1
   - [ ] Links: distinguishable from surrounding text
   - [ ] Focus indicators: visible 3:1 contrast

3. **Status Colors**
   - [ ] Success: success-foreground/success ≥ 4.5:1
   - [ ] Warning: warning-foreground/warning ≥ 4.5:1
   - [ ] Error: destructive-foreground/destructive ≥ 4.5:1
   - [ ] Info: info-foreground/info ≥ 4.5:1

4. **UI Components**
   - [ ] Borders against background ≥ 3:1
   - [ ] Icons against background ≥ 3:1
   - [ ] Form input borders ≥ 3:1

## Common Accessibility Issues

### Issue 1: Low Contrast Muted Text
```css
/* Problem */
--color-muted-foreground: oklch(60% 0.02 250); /* Too light on white */

/* Solution */
--color-muted-foreground: oklch(45% 0.02 250); /* Darker, accessible */
```

### Issue 2: Colored Text on Colored Background
```css
/* Problem */
--color-primary: oklch(55% 0.15 250);
--color-primary-foreground: oklch(70% 0.10 250); /* Poor contrast */

/* Solution */
--color-primary-foreground: oklch(99% 0.005 250); /* High contrast white */
```

### Issue 3: Low Contrast in Dark Mode
```css
/* Problem */
--color-muted: oklch(25% 0.015 250);
--color-muted-foreground: oklch(50% 0.01 250); /* Too similar */

/* Solution */
--color-muted-foreground: oklch(65% 0.01 250); /* More contrast */
```

### Issue 4: Warning Colors
```css
/* Problem - Yellow text on white is low contrast */
--color-warning: oklch(85% 0.20 85);
--color-warning-foreground: oklch(99% 0.005 85); /* Fails */

/* Solution - Use dark text on yellow */
--color-warning: oklch(78% 0.15 85);
--color-warning-foreground: oklch(25% 0.05 85); /* Dark text works */
```

## Generating Accessible Palettes

### Step 1: Define Base Color
```css
--color-primary-500: oklch(55% 0.15 250);
```

### Step 2: Calculate Foreground
```javascript
function getAccessibleForeground(bgLightness) {
  // If background is light (L > 55%), use dark text
  // If background is dark (L < 55%), use light text
  if (bgLightness > 55) {
    return `oklch(${Math.min(bgLightness - 40, 25)}% 0.02 250)`;
  } else {
    return `oklch(${Math.max(bgLightness + 40, 95)}% 0.005 250)`;
  }
}
```

### Step 3: Verify All Combinations
```javascript
const pairs = [
  ['foreground', 'background'],
  ['muted-foreground', 'background'],
  ['muted-foreground', 'muted'],
  ['primary-foreground', 'primary'],
  ['secondary-foreground', 'secondary'],
  ['destructive-foreground', 'destructive'],
  // ... all pairs
];

pairs.forEach(([fg, bg]) => {
  const ratio = calculateContrastRatio(fg, bg);
  if (ratio < 4.5) {
    console.warn(`${fg}/${bg}: ${ratio.toFixed(2)} - FAILS WCAG AA`);
  }
});
```

## Focus Indicators

### Requirements
- Visible focus indicator for all interactive elements
- Minimum 3:1 contrast against adjacent colors
- Don't remove focus outlines

### Implementation
```css
@theme {
  --color-ring: oklch(55% 0.15 250);
}

/* Focus visible styles */
:focus-visible {
  outline: 2px solid var(--color-ring);
  outline-offset: 2px;
}

/* For dark backgrounds */
.dark :focus-visible {
  outline-color: oklch(65% 0.15 250); /* Brighter for visibility */
}
```

## Color Blindness Considerations

### Don't Rely on Color Alone
- Use icons + color for status
- Use patterns + color for charts
- Provide text labels

### Common Color Blindness Types
| Type | Affected | Solution |
|------|----------|----------|
| Protanopia | Red-Green | Add blue/yellow differentiation |
| Deuteranopia | Red-Green | Add blue/yellow differentiation |
| Tritanopia | Blue-Yellow | Add red/green differentiation |

### Safe Color Combinations
```css
/* Use hue separation > 60° */
--color-success: oklch(55% 0.16 145);  /* Green, H: 145 */
--color-error: oklch(55% 0.22 25);     /* Red, H: 25 */
/* Separation: 120° - Safe */

/* Add shape/icon differentiation */
.status-success::before { content: "✓"; }
.status-error::before { content: "✕"; }
```

## Accessibility Report Format

```yaml
accessibilityReport:
  level: 'AA'  # or 'AAA'

  passes:
    - pair: ['foreground', 'background']
      ratio: 15.2
      required: 4.5
      status: 'pass'
    - pair: ['primary-foreground', 'primary']
      ratio: 7.8
      required: 4.5
      status: 'pass'
    # ... more pairs

  warnings:
    - pair: ['muted-foreground', 'muted']
      ratio: 4.8
      message: 'Passes AA but consider improving for AAA'

  failures: []  # Empty if all pass

  recommendations:
    - 'Consider adding focus-visible styles'
    - 'Ensure color is not the only differentiator for status'
```

## Testing Tools

### Automated
- axe DevTools
- Lighthouse accessibility audit
- WAVE browser extension

### Manual
- Keyboard navigation test
- Screen reader test (VoiceOver, NVDA)
- High contrast mode test
- Color blindness simulators
