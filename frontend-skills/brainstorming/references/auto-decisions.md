# Auto-Decision Rules for Feature Inclusion

Rules for autonomous feature selection without user questions.

## Core Principle

**Max-Bound First**: Include all potentially relevant features, then filter based on context. It's easier to remove features than to remember forgotten ones.

---

## Auth Implementation Rule (Non-Negotiable)

**Whenever authentication is included — regardless of project type or complexity — it MUST be implemented using the `supabase-auth` skill.**

- Use `supabase.auth.signUp`, `supabase.auth.signInWithPassword`, `supabase.auth.signOut`
- Use `AuthProvider` + `useSession` + `useAuth` + `AuthService` as defined in `supabase-auth` skill
- **Never use localStorage, sessionStorage, or custom token stores for auth state**
- The `supabase-auth` skill must be loaded automatically when any auth feature is included

This applies to: login, signup, logout, protected routes, session guards, user profile access.

---

## Decision Framework

### Step 1: Include All Type-Specific Features
```
LOAD features WHERE projectType matches
INCLUDE all features with matching projectType

IF any auth feature is included (login, signup, protected routes, session):
  LOAD supabase-auth skill
  IMPLEMENT auth via supabase.auth.* only
  NEVER implement auth with localStorage/sessionStorage
```

### Step 2: Apply Complexity Filter
```
IF projectComplexity == 'simple':
  EXCLUDE features WHERE complexity == 'complex'
  LIMIT enhanced tier to 5 features
  LIMIT premium tier to 2 features

IF projectComplexity == 'medium':
  INCLUDE features WHERE complexity <= 'medium'
  INCLUDE complex features IF explicitly relevant
  LIMIT premium tier to 5 features

IF projectComplexity == 'complex':
  INCLUDE all relevant features
  No tier limits
```

### Step 3: Apply Audience Filter
```
IF audience == 'b2b':
  BOOST: data-export, team-features, integrations, security
  REDUCE: social-sharing, gamification

IF audience == 'b2c':
  BOOST: social-proof, personalization, engagement
  REDUCE: api-access, bulk-operations

IF audience == 'developer':
  BOOST: api-docs, keyboard-shortcuts, code-examples
  REDUCE: excessive-animations, redundant-ui

IF audience == 'creative':
  BOOST: visual-features, animations, typography
  REDUCE: data-heavy, generic-templates
```

### Step 4: Apply Style Filter
```
IF style contains 'minimal':
  REDUCE: animations, decorative-features
  BOOST: whitespace, typography, simplicity

IF style contains 'bold' OR 'playful':
  BOOST: animations, color-usage, interactions
  REDUCE: corporate-features

IF style contains 'professional':
  BOOST: trust-signals, clarity, efficiency
  REDUCE: playful-elements

IF style contains 'dark':
  INCLUDE: dark-mode as core
  BOOST: high-contrast, dramatic-visuals
```

---

## Inclusion Rules

### Always Include (Core)

These features are always included regardless of context:

**Landing Pages**:
- [ ] Hero section
- [ ] Navigation header
- [ ] Primary CTA
- [ ] Footer

**Dashboards**:
- [ ] Authentication (if data is protected) — **MUST use `supabase-auth` skill; never localStorage**
- [ ] Main navigation
- [ ] Overview/home screen
- [ ] User profile access

**E-commerce**:
- [ ] Product listing
- [ ] Product detail
- [ ] Add to cart
- [ ] Cart view
- [ ] Checkout flow

**Portfolios**:
- [ ] Project showcase
- [ ] About section
- [ ] Contact method
- [ ] Navigation

**Blogs**:
- [ ] Post listing
- [ ] Post detail
- [ ] Basic navigation
- [ ] Author info

### Conditionally Include

Rules for context-dependent features:

```yaml
# Testimonials
include_testimonials:
  if:
    - projectType in [landing, saas, portfolio]
    - complexity >= medium
    - OR audience == b2b
  tier: enhanced

# Pricing Table
include_pricing:
  if:
    - projectType in [landing, saas]
    - complexity >= medium
    - NOT single_product
  tier: enhanced

# Newsletter Signup
include_newsletter:
  if:
    - projectType in [landing, blog, portfolio]
    - NOT complexity == simple
  tier: enhanced

# Search
include_search:
  if:
    - contentVolume > 10 items
    - OR projectType in [ecommerce, blog, documentation]
  tier: core for high-volume, enhanced otherwise

# Dark Mode
include_dark_mode:
  if:
    - audience in [developer, creative]
    - OR style contains 'dark'
    - OR complexity >= medium
  tier: enhanced

# Real-time Features
include_realtime:
  if:
    - projectType == dashboard
    - complexity == complex
    - OR explicit_requirement
  tier: premium

# Animation Package
include_animations:
  if:
    - style NOT contains 'minimal'
    - audience in [creative, b2c]
  tier: enhanced
  intensity: based on style keywords
```

### Exclusion Rules

Features to exclude based on context:

```yaml
# Exit Intent Popup
exclude_exit_popup:
  if:
    - style contains 'minimal'
    - OR audience == developer
    - OR projectType == portfolio

# Live Chat
exclude_live_chat:
  if:
    - complexity == simple
    - OR style contains 'minimal'

# Complex Animations
exclude_complex_animations:
  if:
    - projectType == documentation
    - OR audience == enterprise
    - OR style contains 'professional'

# Social Features
exclude_social:
  if:
    - projectType == dashboard
    - audience == b2b AND NOT consumer-facing

# Gamification
exclude_gamification:
  if:
    - audience in [b2b, enterprise]
    - projectType in [dashboard, documentation]
```

---

## Decision Trees

### Landing Page Decision Tree

```
START
├── Include Core: hero, nav, features, cta, footer
├── complexity >= medium?
│   ├── YES: Include testimonials, pricing, faq
│   └── NO: Skip to style check
├── audience == b2b?
│   ├── YES: Boost social-proof, case-studies
│   └── NO: Boost personalization
├── style == minimal?
│   ├── YES: Reduce animations, decorative
│   └── NO: Include moderate animations
└── OUTPUT tiered features
```

### Dashboard Decision Tree

```
START
├── Include Core: auth, nav, overview, profile
├── complexity >= medium?
│   ├── YES: Include tables, charts, filters, export
│   └── NO: Basic data display only
├── audience == b2b?
│   ├── YES: Team features, audit logs
│   └── NO: Personal dashboard focus
├── realtime needed?
│   ├── YES: WebSocket, live updates
│   └── NO: Standard polling/refresh
└── OUTPUT tiered features
```

### E-commerce Decision Tree

```
START
├── Include Core: product-grid, detail, cart, checkout
├── complexity >= medium?
│   ├── YES: Include filters, wishlist, reviews
│   └── NO: Basic catalog only
├── product variety high?
│   ├── YES: Advanced filters, compare
│   └── NO: Simple navigation
├── style == luxury?
│   ├── YES: High-quality imagery, refined UX
│   └── NO: Functional focus
└── OUTPUT tiered features
```

---

## Confidence Levels

Assign confidence to each auto-decision:

### High Confidence (90%+)
- Explicit project type keyword
- Explicit feature request
- Industry-standard requirement
- Core functionality for type

### Medium Confidence (70-89%)
- Inferred from context
- Common for audience type
- Suggested by complexity level
- Style-appropriate

### Low Confidence (50-69%)
- Edge case application
- Unusual combination
- Conflicting signals
- Might need adjustment

---

## Decision Documentation

For each auto-decision, log:

```yaml
decision:
  feature: "Feature Name"
  action: include | exclude | tier_assignment
  tier: core | enhanced | premium | excluded
  confidence: high | medium | low
  reasoning:
    primary: "Main reason for decision"
    supporting:
      - "Supporting reason 1"
      - "Supporting reason 2"
  signals:
    - signal: "What triggered this decision"
      weight: 0.0-1.0
  alternatives:
    - "Alternative if user disagrees"
```

---

## Override Patterns

User can override auto-decisions with explicit keywords:

| User Says | Action |
|-----------|--------|
| "simple", "basic", "minimal" | Reduce to core features only |
| "full-featured", "comprehensive" | Include enhanced + some premium |
| "enterprise", "production-ready" | Include all tiers |
| "no [feature]" | Exclude specific feature |
| "must have [feature]" | Promote to core tier |
| "focus on [aspect]" | Boost related features |

---

## Example Decision Log

**Input**: "Modern SaaS dashboard for B2B analytics"

```yaml
decisions:
  - feature: Authentication
    action: include
    tier: core
    confidence: high
    reasoning:
      primary: "Dashboard requires user authentication"
      supporting:
        - "B2B implies protected data"
    signals:
      - signal: "dashboard keyword"
        weight: 1.0
      - signal: "B2B audience"
        weight: 0.9

  - feature: Data Tables
    action: include
    tier: core
    confidence: high
    reasoning:
      primary: "Analytics dashboard needs tabular data"
      supporting:
        - "B2B users expect data density"

  - feature: Charts
    action: include
    tier: core
    confidence: high
    reasoning:
      primary: "Analytics explicitly requested"
      supporting:
        - "Modern dashboards include visualizations"

  - feature: Real-time Updates
    action: include
    tier: enhanced
    confidence: medium
    reasoning:
      primary: "Modern analytics often includes live data"
      supporting:
        - "Not explicitly requested, so not core"
    alternatives:
      - "Move to core if user confirms live data need"

  - feature: Team Management
    action: include
    tier: enhanced
    confidence: medium
    reasoning:
      primary: "B2B typically involves teams"
      supporting:
        - "SaaS context suggests multi-user"

  - feature: Gamification
    action: exclude
    tier: excluded
    confidence: high
    reasoning:
      primary: "B2B analytics dashboard, not consumer app"
      supporting:
        - "Professional context"
```
