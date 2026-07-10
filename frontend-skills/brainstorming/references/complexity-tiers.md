# Complexity Tiers Definition

Rules for assigning features to Core, Enhanced, and Premium tiers.

## Tier Definitions

### Core Tier (MVP)
**Criteria**: Essential for the product to function and deliver basic value.

- **Must-have**: Product is unusable without these features
- **Immediate value**: User gets value on first interaction
- **Low risk**: Well-understood, standard patterns
- **Implementation**: Can be built quickly with standard components

**Examples by Project Type**:
| Project | Core Features |
|---------|--------------|
| Landing | Hero, navigation, features, CTA, footer |
| Dashboard | Auth, navigation, overview, basic data display |
| E-commerce | Product grid, product detail, cart, basic checkout |
| Portfolio | Project grid, project detail, about, contact |
| Blog | Post list, post detail, navigation |
| SaaS | Landing page, auth, core app functionality |

### Enhanced Tier (Value-Add)
**Criteria**: Significantly improves user experience and conversion.

- **Should-have**: Product works without, but is noticeably better with
- **Competitive advantage**: Features users expect from quality products
- **Moderate effort**: Requires additional components or integrations
- **Measurable impact**: Can show ROI or improved metrics

**Examples by Project Type**:
| Project | Enhanced Features |
|---------|------------------|
| Landing | Testimonials, pricing table, FAQ, newsletter |
| Dashboard | Charts, advanced filtering, export, notifications |
| E-commerce | Reviews, wishlist, filters, related products |
| Portfolio | Category filters, page transitions, testimonials |
| Blog | Search, newsletter, related posts, TOC |
| SaaS | Onboarding, team features, integrations |

### Premium Tier (Delight)
**Criteria**: Creates memorable experiences and differentiation.

- **Nice-to-have**: Delightful but not expected
- **Differentiation**: Sets product apart from competitors
- **Higher effort**: Complex implementation or third-party services
- **Emotional impact**: Creates "wow" moments

**Examples by Project Type**:
| Project | Premium Features |
|---------|-----------------|
| Landing | Animated stats, interactive demos, personalization |
| Dashboard | Real-time updates, command palette, custom dashboards |
| E-commerce | 360 view, AR try-on, personalized recommendations |
| Portfolio | Custom cursor, sound design, 3D elements |
| Blog | Comments, bookmarks, reading progress |
| SaaS | AI features, advanced analytics, white-labeling |

---

## Tier Assignment Algorithm

```
FOR each feature in feature_matrix:

  # Check explicit tier assignment
  IF feature.explicitTier:
    ASSIGN feature.explicitTier
    CONTINUE

  # Check project complexity level
  IF projectComplexity == 'simple':
    IF feature.complexity == 'complex':
      ASSIGN 'excluded'
      CONTINUE
    IF feature.complexity == 'medium':
      ASSIGN 'premium'
      CONTINUE

  # Apply tier rules
  IF feature.isEssential(projectType):
    ASSIGN 'core'
  ELIF feature.addsSignificantValue(projectType, audience):
    ASSIGN 'enhanced'
  ELSE:
    ASSIGN 'premium'
```

---

## Tier Rules by Feature Category

### Navigation Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Header navigation | Core | Core | Core |
| Mobile menu | Core | Core | Core |
| Sticky header | Enhanced | Core | Core |
| Mega menu | Excluded | Enhanced | Core |
| Command palette | Excluded | Premium | Enhanced |
| Breadcrumbs | Enhanced | Core | Core |

### Authentication Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Basic login | Core* | Core | Core |
| Social login | Excluded | Enhanced | Core |
| Password reset | Core* | Core | Core |
| Two-factor auth | Excluded | Premium | Enhanced |
| SSO/SAML | Excluded | Excluded | Premium |

*If auth is required for the project type

### Data Display Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Basic lists | Core | Core | Core |
| Data tables | Enhanced | Core | Core |
| Sortable columns | Excluded | Core | Core |
| Filterable data | Excluded | Enhanced | Core |
| Charts | Excluded | Enhanced | Core |
| Real-time updates | Excluded | Premium | Enhanced |

### Content Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Static sections | Core | Core | Core |
| FAQ accordion | Enhanced | Core | Core |
| Testimonials | Enhanced | Core | Core |
| Video embed | Enhanced | Enhanced | Core |
| Interactive demos | Excluded | Premium | Enhanced |
| User-generated content | Excluded | Premium | Enhanced |

### Conversion Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| CTA buttons | Core | Core | Core |
| Contact form | Core | Core | Core |
| Newsletter signup | Enhanced | Core | Core |
| Pricing table | Excluded | Enhanced | Core |
| Calculator/estimator | Excluded | Premium | Enhanced |
| Exit intent popup | Excluded | Premium | Enhanced |

### E-commerce Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Product grid | Core | Core | Core |
| Product detail | Core | Core | Core |
| Cart | Core | Core | Core |
| Basic checkout | Core | Core | Core |
| Filters | Enhanced | Core | Core |
| Wishlist | Excluded | Enhanced | Core |
| Reviews | Excluded | Enhanced | Core |
| Recommendations | Excluded | Premium | Enhanced |

### Visual/UX Features
| Feature | Simple | Medium | Complex |
|---------|--------|--------|---------|
| Responsive design | Core | Core | Core |
| Dark mode | Excluded | Enhanced | Core |
| Animations (basic) | Enhanced | Core | Core |
| Animations (complex) | Excluded | Enhanced | Enhanced |
| Page transitions | Excluded | Premium | Enhanced |
| Custom cursor | Excluded | Excluded | Premium |

---

## Complexity-to-Tier Mapping

### Feature Complexity Assessment

**Simple Features** (1-2 hours implementation):
- Static content display
- Basic forms
- Simple navigation
- Standard buttons/links
- Icon displays

**Medium Features** (2-8 hours implementation):
- Interactive components (accordions, tabs)
- Form validation
- Data fetching and display
- Basic animations
- Responsive variations
- Simple integrations

**Complex Features** (8+ hours implementation):
- Real-time functionality
- Complex state management
- Third-party integrations
- Advanced animations
- Multi-step flows
- Authentication systems
- Payment processing

### Mapping Rules

```
# For SIMPLE project complexity:
simple_feature → Core or Enhanced
medium_feature → Enhanced or Premium
complex_feature → Excluded

# For MEDIUM project complexity:
simple_feature → Core
medium_feature → Core or Enhanced
complex_feature → Enhanced or Premium

# For COMPLEX project complexity:
simple_feature → Core
medium_feature → Core or Enhanced
complex_feature → Enhanced or Premium (based on value)
```

---

## Audience-Based Adjustments

### B2B Audiences
**Promote to higher tiers**:
- Data export functionality
- Team/collaboration features
- Integration capabilities
- Security features
- Audit logs

**Demote to lower tiers**:
- Social sharing
- Gamification elements
- Personalization (unless enterprise)

### B2C Audiences
**Promote to higher tiers**:
- Social proof elements
- Personalization
- Engagement features
- Mobile optimizations
- Quick actions

**Demote to lower tiers**:
- Complex reporting
- API access
- Bulk operations

### Developer Audiences
**Promote to higher tiers**:
- API documentation
- Code examples
- Keyboard shortcuts
- CLI tools
- Technical depth

**Demote to lower tiers**:
- Visual bells and whistles
- Excessive animations
- Redundant UI patterns

### Creative Audiences
**Promote to higher tiers**:
- Visual excellence
- Unique interactions
- Portfolio presentation
- Animation quality
- Typography choices

**Demote to lower tiers**:
- Generic templates
- Standard patterns
- Data-heavy features

---

## Output Format

When assigning tiers, document:

```yaml
feature:
  name: "Feature Name"
  assignedTier: core | enhanced | premium | excluded
  reasoning:
    - "Primary reason for tier assignment"
    - "Secondary consideration"
  complexityScore: simple | medium | complex
  audienceRelevance: high | medium | low
  projectTypeMatch: high | medium | low
```
