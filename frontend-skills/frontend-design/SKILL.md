---
name: frontend-design
description: Defines the visual structure, layout hierarchy, spacing, and design decisions for any UI. Use this skill when building or modifying any page, component, or layout — it ensures distinctive, production-grade design that avoids generic AI aesthetics. Covers visual hierarchy, typography choices, component anatomy, and design patterns for the specific UI being built.
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

---

## Orchestrator Integration

When invoked through the `project-flow` orchestrator, this skill receives context from previous skills and outputs to downstream skills.

### Input Context

This skill may receive pre-processed context from upstream skills:

```yaml
# From enhance-prompt skill
enhanced:
  projectType: landing | dashboard | ecommerce | saas | portfolio | blog
  audience: b2b | b2c | developer | creative
  complexity: simple | medium | complex
  aestheticDirection:
    style: string        # e.g., "modern-minimalist"
    mood: string         # e.g., "professional, trustworthy"
    intensity: subtle | moderate | bold
  pageStructure:
    - name: string
      sections: Section[]
      priority: critical | important | optional

# From brainstorming skill
features:
  core: Feature[]
  enhanced: Feature[]
  premium: Feature[]
componentInventory:
  ui: Component[]
  logic: Component[]

# From theme-factory skill
theme:
  name: string
  lightMode:
    css: string          # Complete @theme block
  darkMode:
    css: string          # Dark mode @theme block
  semanticTokens: Record<string, string>
```

### Using Upstream Context

When context is provided:

1. **Honor the aesthetic direction** from `enhance-prompt` - don't contradict the established mood and style
2. **Use the theme CSS** from `theme-factory` - apply the provided design tokens
3. **Implement the features** from `brainstorming` - prioritize core features
4. **Follow the page structure** - build sections in the defined order

```yaml
# Example: Received context
enhanced:
  projectType: landing
  aestheticDirection:
    style: modern-minimalist
    mood: professional, trustworthy
    intensity: subtle

# Design response:
# - Clean layouts with generous whitespace
# - Subtle animations (150-200ms)
# - Professional typography choices
# - Restrained color usage
# - Focus on content clarity
```

### Output Format

When in orchestrator flow, output includes implementation details:

```yaml
design:
  aesthetic:
    direction: string
    keyElements: string[]
    avoidances: string[]

  components:
    - name: string
      file: string
      props: string[]
      styling: string     # Key styling decisions

  pages:
    - route: string
      sections:
        - name: string
          component: string
          animations: string[]

  codeStructure:
    files:
      - path: string
        purpose: string
        dependencies: string[]

decisions:
  - decision: string
    reason: string
```

### Standalone Mode

When invoked directly (not through orchestrator):

1. Apply the full Design Thinking process
2. Make autonomous aesthetic decisions
3. Generate all context internally
4. Output production-ready code

### Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `enhance-prompt` | Receives aesthetic direction |
| `brainstorming` | Receives component inventory |
| `theme-factory` | Receives CSS variables |
| `next-best-practices` | Code must comply |
| `styling` | Use generated tokens |
| `seo` | Apply to public pages |

### Quality Gates

Before outputting code:

1. **Theme compliance**: Using provided CSS variables
2. **Component coverage**: All core features implemented
3. **Accessibility**: WCAG AA minimum
4. **Responsiveness**: Mobile-first approach
5. **Performance**: Optimized assets and animations
6. **Mobile alignment audit**: Validate layouts at 320px and 375px with no horizontal overflow, overlap, or clipped action rows
7. **Clickable affordance audit**: Ensure every interactive element includes pointer affordance and visible hover/focus state
