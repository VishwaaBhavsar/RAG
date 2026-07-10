# Project Type Detection Heuristics

Rules and algorithms for autonomous project type detection.

## Detection Algorithm

```
1. Check for EXPLICIT keywords (100% confidence)
2. Check for IMPLICIT signals (80% confidence)
3. Apply CONTEXT inference (60% confidence)
4. Use DEFAULT if no signals (landing page for unclear cases)
```

## Project Type Definitions

### Landing Page
**Purpose**: Convert visitors to leads/customers

**Explicit Keywords**: "landing page", "landing", "marketing page", "conversion page"

**Implicit Signals**:
- "waitlist", "early access", "beta signup"
- "launch", "announcement", "coming soon"
- "hero", "call to action", "CTA"
- "testimonials", "social proof"
- Company/product name + "page"

**Page Structure**:
```yaml
pages:
  - name: index
    sections:
      - hero: headline, subheadline, CTA
      - features: 3-6 feature blocks
      - social-proof: testimonials, logos
      - pricing: plans comparison (optional)
      - faq: common questions
      - cta-footer: final conversion push
```

---

### Dashboard
**Purpose**: Display and manage data/workflows

**Explicit Keywords**: "dashboard", "admin panel", "control panel", "admin", "back office"

**Implicit Signals**:
- "analytics", "metrics", "KPIs"
- "reports", "reporting"
- "data", "tables", "charts", "graphs"
- "manage", "management"
- "overview", "summary"
- "settings", "configuration"

**Page Structure**:
```yaml
pages:
  - name: overview
    sections:
      - key-metrics: 4-6 stat cards
      - charts: 2-4 data visualizations
      - recent-activity: activity feed
      - quick-actions: action buttons
  - name: data-view
    sections:
      - filters: search, filter controls
      - data-table: sortable, paginated
      - bulk-actions: multi-select actions
  - name: detail
    sections:
      - header: entity info
      - tabs: related data sections
      - actions: CRUD operations
  - name: settings
    sections:
      - profile: user settings
      - preferences: app settings
      - integrations: third-party connections
```

---

### E-commerce
**Purpose**: Sell products online

**Explicit Keywords**: "e-commerce", "ecommerce", "online store", "shop", "marketplace"

**Implicit Signals**:
- "products", "catalog", "inventory"
- "cart", "shopping cart", "basket"
- "checkout", "payment", "buy"
- "orders", "shipping"
- "categories", "collections"

**Page Structure**:
```yaml
pages:
  - name: homepage
    sections:
      - hero: featured promotion
      - categories: product categories
      - featured-products: curated selection
      - new-arrivals: recent products
  - name: category
    sections:
      - header: category info
      - filters: faceted search
      - product-grid: product cards
      - pagination: load more
  - name: product
    sections:
      - gallery: product images
      - info: price, description, variants
      - add-to-cart: purchase controls
      - reviews: customer reviews
      - related: similar products
  - name: cart
    sections:
      - items: cart contents
      - summary: totals, discounts
      - actions: checkout, continue shopping
  - name: checkout
    sections:
      - shipping: address form
      - payment: payment method
      - review: order summary
      - confirmation: success state
```

---

### SaaS Application
**Purpose**: Multi-feature web application

**Explicit Keywords**: "SaaS", "app", "application", "platform", "tool"

**Implicit Signals**:
- "subscription", "pricing", "plans"
- "teams", "collaboration", "workspace"
- "features" + complexity signals
- Product name + "app"

**Page Structure**:
```yaml
pages:
  - name: marketing-home
    sections:
      - hero: value proposition
      - features: capability showcase
      - pricing: plan comparison
      - testimonials: social proof
  - name: app-home
    sections:
      - workspace-selector: team/project picker
      - recent: recent activity/items
      - quick-actions: common tasks
  - name: feature-pages
    sections:
      - varies by feature
  - name: settings
    sections:
      - account: user settings
      - workspace: team settings
      - billing: subscription management
```

---

### Portfolio
**Purpose**: Showcase work and attract opportunities

**Explicit Keywords**: "portfolio", "showcase", "personal site", "agency site"

**Implicit Signals**:
- "my work", "projects", "case studies"
- "about me", "hire me", "contact"
- "freelance", "agency", "studio"
- Personal name in prompt

**Page Structure**:
```yaml
pages:
  - name: home
    sections:
      - hero: intro, title, tagline
      - featured-work: 3-6 projects
      - services: what you offer
      - about-preview: brief bio
      - contact-cta: get in touch
  - name: work
    sections:
      - filter: category filters
      - project-grid: all projects
  - name: project-detail
    sections:
      - header: project info
      - gallery: visuals
      - description: process, results
      - next-project: navigation
  - name: about
    sections:
      - bio: detailed about
      - skills: capabilities
      - experience: timeline
  - name: contact
    sections:
      - form: contact form
      - info: email, social links
```

---

### Blog
**Purpose**: Publish and share content

**Explicit Keywords**: "blog", "articles", "posts", "magazine", "publication"

**Implicit Signals**:
- "content", "writing", "publish"
- "categories", "tags"
- "author", "byline"
- "newsletter", "subscribe"

**Page Structure**:
```yaml
pages:
  - name: home
    sections:
      - featured: hero post
      - recent: latest posts grid
      - categories: topic navigation
      - newsletter: subscription form
  - name: archive
    sections:
      - filters: category, date, search
      - post-grid: paginated posts
  - name: post
    sections:
      - header: title, meta, author
      - content: article body
      - author-bio: about author
      - related: similar posts
      - comments: discussion (optional)
  - name: category
    sections:
      - header: category info
      - posts: filtered posts
```

---

### Documentation
**Purpose**: Technical documentation and guides

**Explicit Keywords**: "documentation", "docs", "API reference", "guide", "manual"

**Implicit Signals**:
- "reference", "tutorial"
- "API", "SDK", "integration"
- "getting started", "quickstart"
- "examples", "code"

**Page Structure**:
```yaml
pages:
  - name: home
    sections:
      - hero: product intro
      - quickstart: getting started
      - sections: doc categories
  - name: doc-page
    sections:
      - sidebar: navigation
      - content: documentation
      - toc: table of contents
      - prev-next: page navigation
  - name: api-reference
    sections:
      - endpoints: API endpoints
      - parameters: request/response
      - examples: code samples
```

## Complexity Scoring Algorithm

Automatically determine project complexity based on signal detection.

### Signal Point System

| Signal | Points | Detection Keywords |
|--------|--------|-------------------|
| auth_required | +1 | "login", "signup", "auth", "user account" |
| multi_page (>3 pages) | +1 | "pages", "sections", explicit page mentions |
| real_time_data | +2 | "real-time", "live", "websocket", "streaming" |
| payments | +2 | "payment", "checkout", "subscription", "billing" |
| user_dashboard | +1 | "dashboard", "profile", "settings", "preferences" |
| admin_panel | +2 | "admin", "management", "moderation", "CMS" |
| third_party_integrations | +1 | "integrate", "API", "connect to", service names |
| file_uploads | +1 | "upload", "file", "image", "media", "attachments" |
| search_functionality | +1 | "search", "filter", "find", "query" |
| multi_user_roles | +1 | "roles", "permissions", "team", "organization" |

### Complexity Thresholds

| Score | Complexity | Description |
|-------|------------|-------------|
| 0-2 | simple | Single-purpose, minimal interactivity |
| 3-5 | medium | Multiple features, moderate state management |
| 6+ | complex | Full application, advanced architecture |

### Example Calculations

**"Build a waitlist landing page"**
- No signals detected
- Score: 0 → **simple**

**"Create a blog with user comments and newsletter signup"**
- auth_required (comments): +1
- multi_page: +1
- Score: 2 → **simple**

**"Build a SaaS dashboard with team management and billing"**
- auth_required: +1
- user_dashboard: +1
- payments: +2
- multi_user_roles: +1
- admin_panel: +2
- Score: 7 → **complex**

**"E-commerce site with product search and cart"**
- multi_page: +1
- search_functionality: +1
- payments: +2
- Score: 4 → **medium**

## Confidence Scoring

### 100% Confidence (Explicit)
Direct mention of project type keyword. No further analysis needed.

### 80% Confidence (Implicit)
Strong signals from feature/domain keywords:
- 3+ implicit signals from same category
- Primary use case clearly implied

### 60% Confidence (Inferred)
Context-based inference:
- Single implicit signal
- Industry/domain context
- User type implies project type

### Default (No Signals)
When no clear signals exist:
- Default to **landing** for unclear commercial intent
- Default to **portfolio** for personal/creative context
- Ask for clarification only if truly ambiguous

## Detection Order

1. **Exact match** project type keywords
2. **Feature-based** inference (what it does)
3. **Audience-based** inference (who uses it)
4. **Context-based** inference (industry, domain)
5. **Default** with logged decision

## Edge Cases

### Multiple Types
When signals suggest multiple types:
- Prioritize explicit > implicit > inferred
- Choose the more specific type
- Log both as potential types

### Hybrid Projects
Some projects combine types:
- "SaaS with blog" → SaaS primary, blog secondary
- "E-commerce with dashboard" → E-commerce primary
- Generate page structure for both, prioritize primary

### Unclear Intent
When truly ambiguous:
- Default to landing page (most common)
- Add disclaimer in decisions log
- Include versatile page structure
