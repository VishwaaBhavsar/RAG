# Design System Defaults by Project Type

Pre-configured design system parameters for each project type.

## Landing Page Defaults

```yaml
typography:
  scale: 'dramatic'  # Large headlines, clear hierarchy
  headingFont: 'display'  # Distinctive display font
  bodyFont: 'readable'  # Highly readable body font
  baseSize: '18px'
  lineHeight: 1.6

spacing:
  density: 'spacious'  # Generous whitespace
  sectionPadding: '6rem'
  componentGap: '2rem'

colors:
  strategy: 'brand-forward'  # Strong brand presence
  contrast: 'high'  # Clear CTAs
  accentUsage: 'strategic'  # Accent for CTAs only

components:
  - hero-section
  - feature-grid
  - testimonial-carousel
  - pricing-table
  - faq-accordion
  - cta-banner
  - footer-comprehensive

animations:
  intensity: 'moderate'
  pageLoad: true  # Staggered entrance
  scroll: true  # Scroll-triggered
  hover: true  # Micro-interactions

layout:
  maxWidth: '1280px'
  style: 'full-bleed-sections'  # Edge-to-edge sections
```

---

## Dashboard Defaults

```yaml
typography:
  scale: 'compact'  # Dense information display
  headingFont: 'system'  # Fast loading
  bodyFont: 'system'  # Consistent with OS
  baseSize: '14px'
  lineHeight: 1.5

spacing:
  density: 'dense'  # Efficient use of space
  sectionPadding: '1.5rem'
  componentGap: '1rem'

colors:
  strategy: 'neutral-base'  # Neutral with semantic colors
  contrast: 'functional'  # Status colors prominent
  accentUsage: 'semantic'  # Colors convey meaning

components:
  - stat-card
  - data-table
  - chart-container
  - filter-bar
  - sidebar-navigation
  - header-toolbar
  - modal-dialog
  - toast-notification
  - dropdown-menu
  - tabs
  - breadcrumbs

animations:
  intensity: 'subtle'
  pageLoad: false  # Fast, no delays
  scroll: false  # Instant response
  hover: true  # Feedback on interactive

layout:
  maxWidth: 'none'  # Full width
  style: 'sidebar-main'  # Navigation sidebar
```

---

## E-commerce Defaults

```yaml
typography:
  scale: 'balanced'  # Clear but compact
  headingFont: 'modern'  # Contemporary feel
  bodyFont: 'readable'  # Product descriptions
  baseSize: '16px'
  lineHeight: 1.6

spacing:
  density: 'balanced'  # Room to browse
  sectionPadding: '3rem'
  componentGap: '1.5rem'

colors:
  strategy: 'product-focus'  # Products are hero
  contrast: 'clear'  # Prices, CTAs visible
  accentUsage: 'purchase'  # Accent = buy actions

components:
  - product-card
  - product-gallery
  - price-display
  - add-to-cart-button
  - cart-drawer
  - checkout-form
  - category-nav
  - search-bar
  - filter-sidebar
  - review-stars
  - quantity-selector

animations:
  intensity: 'moderate'
  pageLoad: false  # Fast to browse
  scroll: true  # Lazy load products
  hover: true  # Product previews
  cart: true  # Cart feedback

layout:
  maxWidth: '1440px'
  style: 'grid-based'  # Product grids
```

---

## SaaS Application Defaults

```yaml
typography:
  scale: 'balanced'
  headingFont: 'modern'
  bodyFont: 'system'  # Performance
  baseSize: '15px'
  lineHeight: 1.5

spacing:
  density: 'balanced'
  sectionPadding: '2rem'
  componentGap: '1rem'

colors:
  strategy: 'professional'  # Trust and clarity
  contrast: 'functional'
  accentUsage: 'action'  # Accent = primary actions

components:
  # Marketing pages
  - hero-section
  - feature-showcase
  - pricing-comparison
  - testimonials
  # App pages
  - app-header
  - sidebar-nav
  - workspace-switcher
  - data-views
  - forms
  - modals
  - notifications

animations:
  intensity: 'subtle'
  pageLoad: true  # Marketing only
  scroll: false  # App is instant
  hover: true
  transitions: true  # Page transitions

layout:
  maxWidth: '1200px'  # Marketing
  appLayout: 'sidebar-main'
```

---

## Portfolio Defaults

```yaml
typography:
  scale: 'expressive'  # Creative hierarchy
  headingFont: 'distinctive'  # Personality
  bodyFont: 'elegant'  # Refined reading
  baseSize: '17px'
  lineHeight: 1.7

spacing:
  density: 'generous'  # Let work breathe
  sectionPadding: '5rem'
  componentGap: '2rem'

colors:
  strategy: 'personality'  # Unique to creator
  contrast: 'dramatic'  # Visual impact
  accentUsage: 'highlight'  # Selective emphasis

components:
  - hero-intro
  - project-grid
  - project-detail
  - image-gallery
  - video-embed
  - about-section
  - skills-display
  - timeline
  - contact-form
  - social-links

animations:
  intensity: 'expressive'
  pageLoad: true  # Grand entrance
  scroll: true  # Reveal on scroll
  hover: true  # Image interactions
  pageTransitions: true  # Smooth navigation

layout:
  maxWidth: '1400px'
  style: 'editorial'  # Magazine-like
```

---

## Blog Defaults

```yaml
typography:
  scale: 'readable'  # Optimized for reading
  headingFont: 'editorial'  # Publication feel
  bodyFont: 'serif'  # Classic readability
  baseSize: '18px'
  lineHeight: 1.8
  contentWidth: '720px'  # Optimal reading width

spacing:
  density: 'comfortable'
  sectionPadding: '3rem'
  componentGap: '1.5rem'
  articleSpacing: '2rem'

colors:
  strategy: 'minimal'  # Content focus
  contrast: 'readable'  # Easy on eyes
  accentUsage: 'links'  # Interactive elements

components:
  - article-header
  - article-body
  - author-bio
  - share-buttons
  - related-posts
  - newsletter-signup
  - post-card
  - category-tags
  - search
  - comments

animations:
  intensity: 'minimal'
  pageLoad: false  # Fast content access
  scroll: false  # No distractions
  hover: true  # Link feedback

layout:
  maxWidth: '1200px'
  contentWidth: '720px'
  style: 'centered-content'
```

---

## Documentation Defaults

```yaml
typography:
  scale: 'functional'
  headingFont: 'system'  # Fast, familiar
  bodyFont: 'system'
  codeFont: 'monospace'
  baseSize: '16px'
  lineHeight: 1.7

spacing:
  density: 'organized'
  sectionPadding: '2rem'
  componentGap: '1rem'

colors:
  strategy: 'minimal'  # Code focus
  contrast: 'clear'  # Syntax highlighting
  accentUsage: 'navigation'  # Current section

components:
  - sidebar-nav
  - table-of-contents
  - code-block
  - callout-box
  - tabs
  - search
  - prev-next-nav
  - copy-button
  - version-selector

animations:
  intensity: 'none'  # Pure function
  pageLoad: false
  scroll: false
  hover: true  # Link states

layout:
  maxWidth: '1400px'
  contentWidth: '800px'
  style: 'docs-layout'  # Sidebar + content + TOC
```

---

## Marketplace Defaults

```yaml
typography:
  scale: 'scannable'  # Quick browsing
  headingFont: 'modern'
  bodyFont: 'readable'
  baseSize: '15px'
  lineHeight: 1.5

spacing:
  density: 'efficient'  # Many items
  sectionPadding: '2rem'
  componentGap: '1rem'

colors:
  strategy: 'neutral'  # Products/sellers shine
  contrast: 'clear'  # Prices, ratings
  accentUsage: 'action'  # Buy, contact

components:
  - listing-card
  - seller-profile
  - search-filters
  - category-tree
  - price-range
  - rating-display
  - message-thread
  - cart-checkout
  - review-system
  - comparison-view

animations:
  intensity: 'minimal'
  pageLoad: false
  scroll: true  # Infinite scroll
  hover: true  # Card interactions

layout:
  maxWidth: '1440px'
  style: 'filter-grid'  # Sidebar filters + grid
```

---

## Universal Defaults

These apply to all project types unless overridden:

```yaml
responsive:
  breakpoints:
    sm: '640px'
    md: '768px'
    lg: '1024px'
    xl: '1280px'
    2xl: '1536px'
  mobileFirst: true

accessibility:
  level: 'AA'
  focusVisible: true
  reducedMotion: true
  colorContrast: 4.5

performance:
  fontLoading: 'swap'
  imageOptimization: true
  lazyLoading: true

darkMode:
  support: true
  default: 'system'
  toggle: true
```
