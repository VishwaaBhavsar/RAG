---
name: project-flow
description: Master orchestrator that runs all frontend skills in the correct order for any page or feature build. Use this skill when building a full page, feature, or UI from scratch — it automatically chains enhance-prompt, brainstorming, theme-factory, frontend-design, next-best-practices, coding-principles, and seo without requiring manual coordination between them.
---

# Project Flow Orchestrator

Transform a vague user prompt into a complete, production-ready project specification by chaining specialized skills in sequence.

## Flow Diagram

```
User Prompt
     │
     ▼
┌─────────────────┐
│ enhance-prompt  │  ← Transform vague → structured spec
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  brainstorming  │  ← Generate max-bound features
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   web-search    │  ← Research domain palette/trends
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  theme-factory  │  ← Generate tokens + write CSS
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ frontend-design │  ← Design implementation
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│          VALIDATION PHASE           │
├─────────────────────────────────────┤
│ • next-best-practices               │
│ • coding-principles                 │
│ • seo (public pages only)           │
│ • styling                           │
└────────┬────────────────────────────┘
         │
         ▼
    Implementation Spec
```

## Phase Summary

| Phase | Skill | Input | Output |
|-------|-------|-------|--------|
| 1 | `enhance-prompt` | Raw prompt | projectType, audience, complexity, aesthetic, pages |
| 2 | `brainstorming` | Enhanced spec | Features (core/enhanced/premium), components, data |
| 3 | `web-search` | Domain + feature context | Palette/trend references + accessibility-safe cues |
| 4 | `theme-factory` | Aesthetic direction + web findings | Theme CSS, refreshes global.css |
| 5 | `frontend-design` | All context | Layouts, component styling, pages |
| 6 | Validation | Design spec | Compliance checks, recommendations |

## Core Principles

| Principle | Description |
|-----------|-------------|
| Autonomous | No user questions during flow |
| Transparent | Log all auto-decisions with reasoning |
| Context-Aware | Pass rich context between skills |
| Fail-Safe | Sensible defaults at every step |
| Reversible | User can override any decision |

## Phase Details

### Phase 1: Prompt Enhancement

**Skill**: `enhance-prompt`

| Step | Action |
|------|--------|
| 1 | Extract keywords and signals from prompt |
| 2 | Detect project type (landing, dashboard, ecommerce, etc.) |
| 3 | Infer audience (B2B/B2C) and complexity |
| 4 | Determine aesthetic direction and intensity |
| 5 | Generate page structure with sections |

### Phase 2: Feature Brainstorming

**Skill**: `brainstorming`

| Step | Action |
|------|--------|
| 1 | Load feature matrix for project type |
| 2 | Apply complexity/audience filters |
| 3 | Assign tiers (core/enhanced/premium) |
| 4 | Map features to UI/logic components |
| 5 | Identify data entities and requirements |

### Phase 3: Domain Theme Research

**Tool**: `WebSearch`

| Step | Action |
|------|--------|
| 1 | Identify domain from user request (e.g. fintech, healthcare, ecommerce) |
| 2 | Search for current visual and color trends in that domain |
| 3 | Capture palette direction and anti-patterns to avoid |
| 4 | Keep accessibility-safe color guidance (contrast, readability) |
| 5 | Pass findings to theme-factory as required context |

### Phase 4: Theme Generation

**Skills**: `theme-factory` + `styling`

| Step | Action |
|------|--------|
| 1 | Use web-search findings + context to select or generate theme direction |
| 2 | Generate/update light + dark OKLCH token systems |
| 3 | Verify WCAG accessibility compliance |
| 4 | **Refresh `apps/frontend/src/app/global.css` first, before UI build** |
| 5 | Preserve non-theme sections while replacing theme markers only |

### Phase 5: Design Implementation

**Skills**: `frontend-design` + `components`

| Step | Action |
|------|--------|
| 1 | Apply aesthetic direction from context |
| 2 | Find existing components to reuse |
| 3 | Design new components with theme CSS |
| 4 | Create page layouts with sections |
| 5 | **App brand mark (`icon.ai.tsx` + `apple-icon.ai.tsx`) is mandatory:** whenever you create or change a brand icon used anywhere in the app (navbar/header/sidebar/footer/auth/cards), use one shared brand icon component and update **`src/app/icon.ai.tsx`** and **`src/app/apple-icon.ai.tsx`** in the **same step** so visuals stay identical — no drift, no follow-up pass. Never edit default active icon files (`src/app/icon.tsx`, `src/app/apple-icon.tsx`) in AI branding tasks. |
| 6 | Add appropriate animations/transitions |

### Phase 6: Compliance Validation

| Skill | Checks | When |
|-------|--------|------|
| `next-best-practices` | File structure, RSC boundaries, metadata, error handling | Always |
| `coding-principles` | DRY, KISS, SRP, separation of concerns | Always |
| `seo` | Metadata, JSON-LD, llms.txt, semantic HTML | Public pages only |
| `styling` | Semantic colors, responsive design, Tailwind patterns | Always |
| `accessibility` | Semantic interactivity, keyboard support, pointer/hover/focus affordance | Always for UI work |
| Functional UX gate | User controls do real work (nav/filter/sort/search/pagination) | Always for UI work |

## Supporting Skills

| Skill | Purpose | Load When |
|-------|---------|-----------|
| `components` | Find/reuse existing components | Component work |
| `styling` | Tailwind v4 patterns, design tokens | Styling work |
| `seo` | Traditional + AI search optimization | Public pages (auto-trigger) |
| `coding-principles` | Code quality validation | Always in validation |
| `api-integration` | TanStack Query + generated API | Data fetching features |
| `translation` | i18next multi-language support | i18n requirement |
| `supabase-auth` | Supabase Auth — login/signup/OAuth/session/guards | Any auth requirement |

## Skill Loading Strategy

**Always Load (Core Flow)**:
```
enhance-prompt → brainstorming → web-search → theme-factory → frontend-design → next-best-practices
```

**Auto-Trigger Rules**:

| Condition | Load Skill |
|-----------|------------|
| Any validation | `coding-principles` |
| Public pages (landing, marketing, portfolio) | `seo` |
| Component creation | `components` |
| Features with data fetching | `api-integration` |
| Multi-language requirement | `translation` |
| Authentication required (login/signup/protected routes/guards) | `supabase-auth` |

## Final Output Structure

```yaml
projectSpec:
  metadata: { generatedAt, flowVersion, originalPrompt }
  enhanced: { projectType, audience, complexity, aesthetic, pages }
  features: { core, enhanced, premium, componentInventory, dataSchema }
  theme: { name, lightMode, darkMode, accessibilityReport }
  design: { aesthetic, components, pages }
  compliance: { nextBestPractices, codingPrinciples, seo, styling }
  decisions: [{ phase, decision, reason, confidence }]
  implementationPlan: { files, order }
```

## Decision Logging

Every auto-decision is logged:
```yaml
decision:
  phase: string        # Which skill made it
  decision: string     # What was decided
  reason: string       # Why
  confidence: high|medium|low
  override: string     # How user can change it
```

## User Overrides

Users can override decisions at any point. The flow can be re-run from any phase:
- "Make it dark mode" → Re-run from theme-factory
- "Use brutalist styling" → Re-run from theme-factory
- "Remove real-time features" → Update features, re-run from Phase 4

## Error Handling

If any phase fails: log error → apply fallback defaults → continue flow → mark as "fallback"

## Functional UX Gate (Mandatory Before Completion)

Apply this gate to every UI feature/page before marking implementation complete:

- Any visible control must produce a visible outcome.
  - Examples: nav changes route/section, filter narrows data, sort changes order, pagination changes page, search updates results.
- No inert UI controls.
  - Remove placeholder controls (or wire them) if they do nothing.
- Filters/sort/search must include reset behavior.
  - Provide a clear/reset path that restores baseline view.
- Navigation destinations must exist.
  - Route targets or section anchors must be valid and reachable.
- Validate behavior, not only appearance.
  - Include click + keyboard interaction checks and state update checks in completion criteria.

## References

- State machine: `references/flow-states.md`
- Output schemas: `references/output-formats.md`
