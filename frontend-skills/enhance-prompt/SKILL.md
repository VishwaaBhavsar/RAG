---
name: enhance-prompt
description: Converts a vague or high-level user request into a detailed, structured spec ready for implementation. Use this skill when the task description is ambiguous, broad, or lacks enough detail to start building — it clarifies scope, audience, and direction without asking the user any questions.
---

# Enhance Prompt Skill

Transform vague prompts into comprehensive specifications ready for downstream skills. Operates **autonomously** - makes intelligent decisions without user questions.

## Core Principles

| Principle | Description |
|-----------|-------------|
| No Questions | All decisions via keyword analysis and intelligent defaults |
| Context Extraction | Extract maximum information from minimal input |
| Intelligent Defaults | Apply sensible defaults based on project type |
| Transparency | Log all auto-decisions for user visibility |

## Input → Output Quick Reference

| Vague Input | Enhanced Output |
|-------------|-----------------|
| "Build me a dashboard" | projectType: dashboard, audience: b2b, style: modern-minimalist |
| "Create an online store" | projectType: ecommerce, audience: b2c, style: modern-minimalist |
| "Make a portfolio" | projectType: portfolio, audience: creative, style: brutalist-raw |
| "Landing page for SaaS" | projectType: landing, audience: b2b, style: tech-innovation |
| "Build a blog" | projectType: blog, audience: b2c, style: warm-organic |

## Processing Pipeline

### Step 1: Keyword Analysis

Reference: `references/keywords.md`

| Category | Examples |
|----------|----------|
| Domain | dashboard, store, portfolio, landing, blog |
| Aesthetic | modern, minimal, bold, playful, professional |
| Audience | business, creative, developer, consumer, enterprise |
| Features | authentication, payments, analytics, notifications |

### Step 2: Project Type Detection

Reference: `references/project-detection.md`

| Type | Trigger Keywords | Use Case |
|------|------------------|----------|
| landing | landing page, marketing, conversion | Marketing/conversion focused |
| dashboard | dashboard, analytics, admin, metrics | Data/admin interface |
| ecommerce | store, shop, products, cart, checkout | Product catalog + checkout |
| saas | saas, app, platform, workflow | Multi-page application |
| portfolio | portfolio, my work, projects, hire me | Personal/agency showcase |
| blog | blog, articles, posts, content | Content-focused site |
| documentation | docs, API, reference, guide | Technical docs |
| marketplace | marketplace, vendors, multi-seller | Multi-vendor platform |

### Step 3: Apply Design System Defaults

Reference: `references/design-system-defaults.md`

Each project type has pre-configured: typography scale, spacing system, color tokens, component inventory, animation intensity.

### Step 4: Generate Page Structure

| Project Type | Core Pages/Sections |
|--------------|---------------------|
| Landing | Hero, Features, Social Proof, Pricing, FAQ, CTA/Footer |
| Dashboard | Auth, Overview, Data Tables, Detail Views, Settings |
| E-commerce | Home, Category, Product Detail, Cart, Checkout, Account |
| Portfolio | Projects, About, Contact, Experience |
| Blog | Home, Post List, Post Detail, Categories |

### Step 5: Output Enhanced Specification

Reference: `references/prompt-templates.md`

## Output Format

```yaml
enhanced:
  projectType: 'landing' | 'dashboard' | 'ecommerce' | 'saas' | 'portfolio' | 'blog'
  audience:
    primary: 'b2b' | 'b2c' | 'developer' | 'creative' | 'enterprise'
    demographics: string
  complexity: 'simple' | 'medium' | 'complex'
  aestheticDirection:
    style: string       # e.g., "modern-minimalist"
    mood: string        # e.g., "professional and trustworthy"
    intensity: 'subtle' | 'moderate' | 'bold'
  pageStructure:
    - name: string
      sections: Section[]
      priority: 'critical' | 'important' | 'optional'
  contentRequirements:
    copyTone: string
    imagery: string
  technicalContext:
    framework: 'next'   # Default
    responsive: true    # Default
    accessibility: 'AA' # Default

decisions:
  - decision: string
    reason: string
    confidence: 'high' | 'medium' | 'low'
```

## Auto-Decision Rules

### Confidence Levels

| Level | Source | Confidence |
|-------|--------|------------|
| Explicit | Direct keywords ("dashboard", "e-commerce") | 100% (high) |
| Implicit | Contextual signals ("analytics", "cart") | 80% (high) |
| Inferred | Context patterns (company = landing) | 60% (medium) |
| Default | No signals → landing page | 50% (low) |

### Audience Detection

| Signal | Audience |
|--------|----------|
| enterprise, business, teams, workflow | B2B |
| consumers, users, personal, lifestyle | B2C |
| API, SDK, documentation, code | Developer |
| design, portfolio, agency, studio | Creative |

### Complexity Assessment

| Level | Indicators |
|-------|------------|
| Simple | Single page, few sections, static content |
| Medium | Multi-page, some interactivity, moderate data |
| Complex | Authentication, real-time data, complex state |

### Aesthetic Mapping

| Keyword | Style Direction |
|---------|----------------|
| modern | clean lines, minimal, geometric |
| minimal | whitespace-heavy, reduced elements |
| bold | strong colors, large typography |
| playful | rounded shapes, vibrant colors |
| professional | structured, corporate, trustworthy |
| creative | unique layouts, artistic elements |
| dark | dark mode, dramatic contrast |
| luxury | elegant, refined, premium feel |

## Integration

| Direction | Skill | Data Passed |
|-----------|-------|-------------|
| Receives | User | Raw prompt string |
| Passes To | brainstorming | Enhanced specification for feature generation |
| Passes To | theme-factory | Aesthetic direction for theme selection |
