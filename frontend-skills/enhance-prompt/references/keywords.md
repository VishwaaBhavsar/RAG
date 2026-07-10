# UI/UX Vocabulary & Keywords Reference

Comprehensive keyword taxonomy for prompt analysis and context extraction.

## Domain Keywords

### Project Type Indicators

| Keyword | Project Type | Confidence |
|---------|-------------|------------|
| dashboard | dashboard | 100% |
| admin panel | dashboard | 100% |
| analytics | dashboard | 90% |
| metrics | dashboard | 85% |
| reporting | dashboard | 85% |
| e-commerce | ecommerce | 100% |
| store | ecommerce | 95% |
| shop | ecommerce | 95% |
| marketplace | marketplace | 100% |
| products | ecommerce | 80% |
| cart | ecommerce | 95% |
| checkout | ecommerce | 100% |
| landing page | landing | 100% |
| marketing | landing | 85% |
| conversion | landing | 90% |
| signup | landing | 75% |
| waitlist | landing | 90% |
| portfolio | portfolio | 100% |
| showcase | portfolio | 85% |
| my work | portfolio | 90% |
| projects | portfolio | 70% |
| blog | blog | 100% |
| articles | blog | 90% |
| posts | blog | 85% |
| documentation | documentation | 100% |
| docs | documentation | 95% |
| API reference | documentation | 100% |
| saas | saas | 100% |
| application | saas | 70% |
| platform | saas | 75% |
| tool | saas | 65% |

### Feature Indicators

| Keyword | Implied Features |
|---------|-----------------|
| authentication | login, signup, password reset, sessions |
| auth | login, signup |
| login | authentication system |
| payments | checkout, stripe/payment integration |
| billing | subscription management, invoices |
| subscriptions | recurring payments, plan management |
| notifications | toast system, email notifications |
| real-time | websockets, live updates |
| search | search bar, filters, results |
| filters | faceted search, sorting |
| settings | preferences, account management |
| profile | user profile, avatar, bio |
| teams | multi-user, roles, permissions |
| collaboration | real-time editing, comments |
| uploads | file upload, media management |
| exports | PDF, CSV, data export |
| integrations | third-party APIs, webhooks |
| analytics | charts, graphs, metrics |
| charts | data visualization |

## Aesthetic Keywords

### Style Directions

| Keyword | Style Mapping | Characteristics |
|---------|--------------|-----------------|
| modern | modern-minimalist | clean, geometric, sans-serif |
| minimal | minimalist | whitespace-heavy, reduced elements |
| minimalist | minimalist | extreme simplicity, essential only |
| clean | modern-minimalist | organized, uncluttered |
| sleek | tech-innovation | polished, streamlined |
| bold | bold-corporate | strong colors, large type |
| vibrant | playful-vibrant | saturated colors, energetic |
| playful | playful-vibrant | rounded shapes, fun animations |
| fun | playful-vibrant | whimsical, colorful |
| professional | bold-corporate | structured, trustworthy |
| corporate | bold-corporate | formal, business-appropriate |
| elegant | luxury-elegant | refined, sophisticated |
| luxury | luxury-elegant | premium feel, exclusive |
| premium | luxury-elegant | high-end aesthetic |
| organic | warm-organic | natural colors, soft shapes |
| natural | natural-earth | earth tones, sustainable feel |
| earthy | natural-earth | browns, greens, warm |
| warm | warm-organic | cozy, inviting colors |
| dark | dark-mode-pro | dark backgrounds, high contrast |
| night | dark-mode-pro | dark theme primary |
| soft | soft-pastel | muted colors, gentle |
| pastel | soft-pastel | light, subtle tones |
| brutalist | brutalist-raw | raw, unconventional |
| edgy | brutalist-raw | unconventional choices |
| retro | custom | vintage-inspired |
| futuristic | tech-innovation | cutting-edge feel |
| tech | tech-innovation | technology-forward |
| creative | custom | artistic, unique |
| artistic | custom | expressive, unconventional |

### Mood Indicators

| Keyword | Mood |
|---------|------|
| trustworthy | professional, secure, reliable |
| innovative | forward-thinking, modern |
| friendly | approachable, welcoming |
| serious | formal, authoritative |
| exciting | energetic, dynamic |
| calm | peaceful, serene |
| powerful | strong, confident |
| sophisticated | refined, cultured |
| accessible | inclusive, easy-to-use |
| cutting-edge | latest, innovative |

## Audience Keywords

### Primary Audience Signals

| Keyword | Audience Type |
|---------|--------------|
| enterprise | b2b |
| business | b2b |
| teams | b2b |
| companies | b2b |
| organizations | b2b |
| workflow | b2b |
| productivity | b2b |
| consumers | b2c |
| users | b2c |
| customers | b2c |
| personal | b2c |
| lifestyle | b2c |
| developers | developer |
| API | developer |
| SDK | developer |
| code | developer |
| technical | developer |
| engineers | developer |
| design | creative |
| creative | creative |
| agency | creative |
| studio | creative |
| artists | creative |
| photographers | creative |

### Demographics Indicators

| Context | Demographics Inference |
|---------|----------------------|
| startup | tech-savvy, 25-40, early adopters |
| enterprise | professionals, 30-55, decision makers |
| consumer app | general public, 18-45, mobile-first |
| developer tool | engineers, 22-45, technical |
| creative tool | designers, 20-40, visual thinkers |
| e-commerce | shoppers, 18-65, varied |
| education | students/educators, 15-60 |
| healthcare | patients/providers, 25-70 |
| finance | professionals/consumers, 25-65 |

## Complexity Indicators

### Simple Complexity
- "simple"
- "basic"
- "single page"
- "one page"
- "static"
- "brochure"

### Medium Complexity
- "multi-page"
- "interactive"
- "dynamic"
- "with forms"
- "contact"
- "newsletter"

### High Complexity
- "authentication"
- "database"
- "real-time"
- "payments"
- "subscriptions"
- "API"
- "integrations"
- "admin"
- "user management"

## Next.js 16 Specific Keywords

### App Router Signals
- "app router"
- "server components"
- "RSC"
- "streaming"
- "suspense"

### Feature Keywords
- "SSR"
- "SSG"
- "ISR"
- "API routes"
- "middleware"
- "edge"

## Extraction Priority

When analyzing prompts, extract in this order:

1. **Explicit project type** (highest priority)
2. **Domain context** (business domain)
3. **Aesthetic direction** (style keywords)
4. **Audience signals** (who uses it)
5. **Feature requirements** (what it does)
6. **Complexity indicators** (how complex)
7. **Technical constraints** (framework, etc.)
