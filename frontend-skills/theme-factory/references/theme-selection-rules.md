# Theme Selection Algorithm

Rules for autonomous theme selection based on project context.

## Selection Matrix

| Project Type | Audience | Style Hint | Recommended Theme |
|--------------|----------|------------|-------------------|
| landing | b2b | professional | bold-corporate |
| landing | b2b | modern | modern-minimalist |
| landing | b2b | tech | tech-innovation |
| landing | b2c | modern | modern-minimalist |
| landing | b2c | playful | playful-vibrant |
| landing | b2c | warm | warm-organic |
| landing | creative | any | brutalist-raw |
| dashboard | any | modern | modern-minimalist |
| dashboard | developer | any | dark-mode-pro |
| dashboard | enterprise | any | bold-corporate |
| ecommerce | luxury | any | luxury-elegant |
| ecommerce | modern | any | modern-minimalist |
| ecommerce | sustainable | any | natural-earth |
| portfolio | creative | any | brutalist-raw |
| portfolio | professional | any | modern-minimalist |
| portfolio | artistic | any | playful-vibrant |
| blog | personal | warm | warm-organic |
| blog | professional | modern | modern-minimalist |
| blog | accessible | any | soft-pastel |
| saas | tech | modern | tech-innovation |
| saas | enterprise | any | bold-corporate |
| saas | startup | any | modern-minimalist |
| any | developer | any | dark-mode-pro |
| any | any | luxury | luxury-elegant |
| any | any | organic/natural | natural-earth |
| any | any | playful/fun | playful-vibrant |
| any | any | gentle/soft | soft-pastel |
| any | any | bold/edgy | brutalist-raw |
| documentation | any | any | dark-mode-pro |
| marketplace | any | any | modern-minimalist |
| any | any | unknown/fallback | modern-minimalist |

## Selection Algorithm

```python
def select_theme(context):
    """
    Priority-based theme selection algorithm.
    """

    # Priority 1: Explicit style keyword match
    style_mapping = {
        'minimal': 'modern-minimalist',
        'minimalist': 'modern-minimalist',
        'modern': 'modern-minimalist',
        'clean': 'modern-minimalist',
        'tech': 'tech-innovation',
        'futuristic': 'tech-innovation',
        'innovation': 'tech-innovation',
        'warm': 'warm-organic',
        'organic': 'warm-organic',
        'cozy': 'warm-organic',
        'corporate': 'bold-corporate',
        'professional': 'bold-corporate',
        'enterprise': 'bold-corporate',
        'playful': 'playful-vibrant',
        'fun': 'playful-vibrant',
        'vibrant': 'playful-vibrant',
        'colorful': 'playful-vibrant',
        'luxury': 'luxury-elegant',
        'elegant': 'luxury-elegant',
        'premium': 'luxury-elegant',
        'sophisticated': 'luxury-elegant',
        'natural': 'natural-earth',
        'earth': 'natural-earth',
        'sustainable': 'natural-earth',
        'eco': 'natural-earth',
        'dark': 'dark-mode-pro',
        'developer': 'dark-mode-pro',
        'code': 'dark-mode-pro',
        'soft': 'soft-pastel',
        'pastel': 'soft-pastel',
        'gentle': 'soft-pastel',
        'accessible': 'soft-pastel',
        'brutalist': 'brutalist-raw',
        'raw': 'brutalist-raw',
        'bold': 'brutalist-raw',
        'edgy': 'brutalist-raw',
        'artistic': 'brutalist-raw',
    }

    for keyword, theme in style_mapping.items():
        if keyword in context.style.lower():
            return theme, 'style_keyword', 'high'

    # Priority 2: Audience + Project Type combination
    if context.audience == 'developer':
        return 'dark-mode-pro', 'developer_audience', 'high'

    if context.projectType == 'dashboard' and context.audience == 'enterprise':
        return 'bold-corporate', 'enterprise_dashboard', 'high'

    # Priority 3: Project Type defaults
    type_defaults = {
        'landing': 'modern-minimalist',
        'dashboard': 'modern-minimalist',
        'ecommerce': 'modern-minimalist',
        'saas': 'tech-innovation',
        'portfolio': 'modern-minimalist',
        'blog': 'warm-organic',
        'documentation': 'dark-mode-pro',
        'marketplace': 'modern-minimalist',
    }

    if context.projectType in type_defaults:
        return type_defaults[context.projectType], 'type_default', 'medium'

    # Priority 4: Fallback
    return 'modern-minimalist', 'fallback', 'low'
```

## Confidence Scoring

### High Confidence (90%+)
- Explicit style keyword match
- Direct project type + audience match
- User-specified theme preference

### Medium Confidence (70-89%)
- Project type default
- Inferred from industry/domain
- Mood keyword partial match

### Low Confidence (50-69%)
- Fallback selection
- Ambiguous signals
- Multiple conflicting matches

## Mood-to-Theme Mapping

| Mood Keywords | Primary Theme | Alternatives |
|---------------|---------------|--------------|
| professional, trustworthy | bold-corporate | modern-minimalist |
| innovative, cutting-edge | tech-innovation | modern-minimalist |
| warm, welcoming, friendly | warm-organic | soft-pastel |
| playful, fun, energetic | playful-vibrant | warm-organic |
| luxurious, premium, exclusive | luxury-elegant | bold-corporate |
| calm, peaceful, natural | natural-earth | soft-pastel |
| focused, productive, efficient | dark-mode-pro | modern-minimalist |
| gentle, accessible, kind | soft-pastel | warm-organic |
| bold, unconventional, artistic | brutalist-raw | playful-vibrant |

## Industry Mapping

| Industry | Recommended Themes |
|----------|-------------------|
| Technology/SaaS | tech-innovation, modern-minimalist, dark-mode-pro |
| Finance/Banking | bold-corporate, modern-minimalist |
| Healthcare | soft-pastel, modern-minimalist |
| E-commerce (General) | modern-minimalist, warm-organic |
| E-commerce (Luxury) | luxury-elegant |
| E-commerce (Sustainable) | natural-earth |
| Creative/Design | brutalist-raw, playful-vibrant |
| Education | soft-pastel, warm-organic |
| Food/Restaurant | warm-organic, playful-vibrant |
| Fitness/Sports | bold-corporate, tech-innovation |
| Real Estate | luxury-elegant, bold-corporate |
| Travel | warm-organic, natural-earth |

## Theme Compatibility Matrix

Which themes work well together for multi-page sites:

| Primary Theme | Compatible Secondary |
|---------------|---------------------|
| modern-minimalist | dark-mode-pro (toggle) |
| tech-innovation | dark-mode-pro, modern-minimalist |
| warm-organic | soft-pastel, natural-earth |
| bold-corporate | modern-minimalist |
| playful-vibrant | soft-pastel |
| luxury-elegant | modern-minimalist |
| natural-earth | warm-organic |
| dark-mode-pro | modern-minimalist (light mode) |
| soft-pastel | warm-organic |
| brutalist-raw | (standalone - highly distinctive) |

## Override Rules

User signals that override default selection:

### Explicit Overrides
```
"I want a dark theme" → dark-mode-pro
"Make it brutalist" → brutalist-raw
"Keep it minimal" → modern-minimalist
"Very colorful" → playful-vibrant
```

### Context Overrides
```
"Developer tools" → dark-mode-pro (regardless of style)
"Luxury brand" → luxury-elegant (regardless of type)
"Children's app" → playful-vibrant or soft-pastel
"Enterprise software" → bold-corporate (regardless of style)
```

## Output Format

```yaml
themeSelection:
  selected: 'modern-minimalist'
  confidence: 'high'
  reasoning:
    primary: "B2B landing page with 'modern' keyword"
    supporting:
      - "Professional audience implies clean aesthetic"
      - "SaaS context favors minimalist approach"
  alternatives:
    - theme: 'tech-innovation'
      reason: "Also suitable for tech SaaS"
    - theme: 'bold-corporate'
      reason: "Consider for enterprise focus"
  signals:
    - signal: "keyword: modern"
      weight: 0.9
    - signal: "projectType: landing"
      weight: 0.7
    - signal: "audience: b2b"
      weight: 0.6
```

## Decision Logging

Every theme selection should log:

1. **Input context**: All signals received
2. **Matching rules**: Which rules triggered
3. **Confidence level**: How certain the selection is
4. **Alternatives**: What other themes were considered
5. **Final selection**: The chosen theme and why
