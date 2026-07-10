---
name: brainstorming
description: Produces a tiered feature list (Core/Enhanced/Premium) with component inventory and data requirements for any UI feature or page. Use this skill when deciding what to build — what screens, components, states, and interactions a feature needs before implementation starts.
---

# Brainstorming Skill

Generate comprehensive, tiered feature lists using a **max-bound approach**. Start with ALL possible features, then organize by priority tier. This approach ensures nothing is missed and makes it easier to scope down than to add forgotten features later.

## Core Principles

1. **Max-Bound**: Generate ALL possible features first
2. **Tiered Output**: Organize into Core (MVP) → Enhanced (Value-Add) → Premium (Delight)
3. **No Questions**: Auto-include based on project context
4. **Component Mapping**: Every feature maps to implementation components
5. **Data Awareness**: Identify data requirements for each feature
6. **Functional-First UX**: Any user-visible control (nav, tabs, filters, sort, pagination, search) must include working behavior, not just UI shells

## Input

Enhanced prompt specification from `enhance-prompt` skill:

```yaml
context:
  projectType: landing | dashboard | ecommerce | saas | portfolio | blog
  audience: b2b | b2c | developer | creative
  complexity: simple | medium | complex
  style: string
  pages: PageSpec[]
```

## Processing Pipeline

### Step 1: Load Feature Matrix

Based on project type, load the complete feature matrix. Reference: `references/feature-matrix.md`

### Step 2: Apply Context Filters

Filter features based on:
- Audience type (B2B vs B2C features)
- Complexity level (exclude advanced for simple)
- Aesthetic direction (animation-heavy vs minimal)

### Step 3: Tier Assignment

Assign each feature to a tier:
- **Core**: Essential for MVP, must-have functionality
- **Enhanced**: Adds significant value, should-have
- **Premium**: Delightful extras, nice-to-have

Reference: `references/complexity-tiers.md`

### Step 4: Component Mapping

For each feature, identify:
- UI components needed
- State management requirements
- API/data dependencies
- Third-party integrations
- Interaction contracts (what each control changes and expected user-visible outcome)

### Step 5: Auto-Decision Rules

Apply inclusion rules. Reference: `references/auto-decisions.md`

## Output Format

```yaml
features:
  core:
    - name: string
      description: string
      components:
        - name: string
          type: 'ui' | 'logic' | 'integration'
          complexity: 'simple' | 'medium' | 'complex'
      dataRequirements:
        - entity: string
          fields: string[]
          source: 'static' | 'api' | 'user-input'
      rationale: string  # Why this is core

  enhanced:
    - name: string
      description: string
      components: [...]
      dataRequirements: [...]
      rationale: string  # Why this adds value

  premium:
    - name: string
      description: string
      components: [...]
      dataRequirements: [...]
      rationale: string  # Why this delights

componentInventory:
  ui:
    - name: string
      usedBy: string[]  # Feature names
      variants: string[]
      props: string[]

  logic:
    - name: string
      purpose: string
      dependencies: string[]

dataSchema:
  entities:
    - name: string
      fields:
        - name: string
          type: string
          required: boolean
      relations: string[]

decisions:
  - decision: string
    reason: string
    tier: 'core' | 'enhanced' | 'premium'
```

## Feature Generation by Project Type

See `references/feature-matrix.md` for complete feature taxonomy by project type.

### Quick Reference

| Project Type | Core (Always) | Enhanced (Medium+) | Premium (Complex) |
|--------------|---------------|--------------------|--------------------|
| Landing | hero, nav, features, footer | testimonials, pricing, faq | stats, demos, chat |
| Dashboard | auth, nav, overview, profile | tables, charts, export | real-time, shortcuts |
| E-commerce | listing, detail, cart, search | filters, wishlist, reviews | compare, recommendations |
| Portfolio | projects, about, contact | filtering, galleries, transitions | case studies, prototypes |
| Blog | posts, categories, search | newsletter, share, related | comments, RSS, series |
| SaaS | homepage, pricing, auth | onboarding, settings, billing | integrations, API, SSO |

### Tier Assignment Rules

- **Core**: Essential for MVP, must-have functionality
- **Enhanced**: Adds significant value, include for `complexity >= medium`
- **Premium**: Delightful extras, include for `complexity == complex` or explicit request

## Auto-Decision Rules

### Inclusion Rules

```
IF projectType == 'landing' AND complexity >= 'medium':
  INCLUDE testimonials, pricing, faq

IF projectType == 'dashboard':
  ALWAYS INCLUDE authentication
  IF complexity >= 'medium': INCLUDE data-tables, charts

IF projectType == 'ecommerce':
  ALWAYS INCLUDE cart, product-detail
  IF complexity >= 'medium': INCLUDE filters, wishlist

IF audience == 'b2b':
  PRIORITIZE: professional features, data export, team features

IF audience == 'b2c':
  PRIORITIZE: engagement features, social sharing, personalization

IF style contains 'minimal':
  REDUCE: animations, decorative features

IF style contains 'bold' OR 'playful':
  INCREASE: animations, micro-interactions
```

### Exclusion Rules

```
IF complexity == 'simple':
  EXCLUDE: premium tier features
  LIMIT: enhanced tier to top 3 features

IF projectType == 'portfolio' AND audience != 'developer':
  EXCLUDE: code-heavy features (syntax highlighting, etc.)

IF projectType == 'landing':
  EXCLUDE: complex state management features
```

## Component & Data Generation

For each feature, generate:
- **UI Components**: Visual elements (e.g., TestimonialCard, Avatar)
- **Logic Components**: Hooks and state (e.g., useTestimonials)
- **Data Requirements**: Entities with fields and source (static/api/user-input)
- **Behavior Requirements**: Functional acceptance checks for controls (e.g., filter narrows list, clear resets state, nav target exists)

## Integration with Flow

### Receives From
- `enhance-prompt`: Project context, type, complexity, pages

### Passes To
- `frontend-design`: Component inventory for implementation
- `project-flow`: Complete feature specification

## Example: Landing Page (B2B, Medium Complexity)

| Tier | Features | Rationale |
|------|----------|-----------|
| Core | Hero, Navigation, Features, Footer | Essential for any landing page |
| Enhanced | Testimonials, Pricing, FAQ | B2B needs social proof, pricing transparency |
| Premium | Animated Stats, Live Demo | Adds polish and credibility |

**Sample Decision Log**:
- Include testimonials (enhanced): B2B audience requires social proof
- Include pricing table: Medium complexity + B2B suggests pricing transparency
- Exclude live chat: Modern-minimalist style conflicts with chat widgets
