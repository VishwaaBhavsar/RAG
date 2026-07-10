# Flow State Machine

State definitions and transitions for the project-flow orchestrator.

## State Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌─────────────────┐       │
│  │  IDLE    │───▶│ INITIALIZING │───▶│ ENHANCING_PROMPT│       │
│  └──────────┘    └──────────────┘    └────────┬────────┘       │
│       ▲                                       │                 │
│       │                                       ▼                 │
│       │                              ┌─────────────────┐        │
│       │                              │  BRAINSTORMING  │        │
│       │                              └────────┬────────┘        │
│       │                                       │                 │
│       │                                       ▼                 │
│       │                              ┌─────────────────┐        │
│       │                              │ THEMING         │        │
│       │                              └────────┬────────┘        │
│       │                                       │                 │
│       │                                       ▼                 │
│       │                              ┌─────────────────┐        │
│       │                              │  DESIGNING      │        │
│       │                              └────────┬────────┘        │
│       │                                       │                 │
│       │                                       ▼                 │
│       │                              ┌─────────────────┐        │
│       │                              │  VALIDATING     │        │
│       │                              └────────┬────────┘        │
│       │                                       │                 │
│       │          ┌───────────┐                ▼                 │
│       └──────────│ COMPLETED │◀───────┬─────────────────┐       │
│                  └───────────┘        │   GENERATING    │       │
│                        │              └─────────────────┘       │
│                        ▼                                        │
│                  ┌───────────┐                                  │
│                  │  FAILED   │                                  │
│                  └───────────┘                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## State Definitions

### IDLE
**Description**: Initial state, waiting for user input.

```yaml
state: IDLE
transitions:
  - trigger: user_prompt_received
    target: INITIALIZING
context: null
```

### INITIALIZING
**Description**: Setting up flow context and validating input.

```yaml
state: INITIALIZING
entry_actions:
  - create_flow_context
  - validate_input
  - log_flow_start
transitions:
  - trigger: context_ready
    target: ENHANCING_PROMPT
  - trigger: invalid_input
    target: FAILED
context:
  originalPrompt: string
  flowId: string
  startTime: timestamp
```

### ENHANCING_PROMPT
**Description**: Running enhance-prompt skill.

```yaml
state: ENHANCING_PROMPT
entry_actions:
  - invoke_enhance_prompt_skill
  - extract_keywords
  - detect_project_type
  - infer_context
exit_actions:
  - store_enhanced_result
  - log_decisions
transitions:
  - trigger: enhancement_complete
    target: BRAINSTORMING
  - trigger: enhancement_failed
    target: BRAINSTORMING  # Use defaults
context:
  enhanced:
    projectType: string
    audience: object
    complexity: string
    aestheticDirection: object
    pageStructure: array
```

### BRAINSTORMING
**Description**: Running brainstorming skill for feature generation.

```yaml
state: BRAINSTORMING
entry_actions:
  - invoke_brainstorming_skill
  - load_feature_matrix
  - apply_filters
  - assign_tiers
exit_actions:
  - store_features_result
  - log_decisions
transitions:
  - trigger: brainstorming_complete
    target: THEMING
  - trigger: brainstorming_failed
    target: THEMING  # Use defaults
context:
  features:
    core: array
    enhanced: array
    premium: array
  componentInventory: object
  dataSchema: object
```

### THEMING
**Description**: Running theme-factory skill for theme selection/generation.

```yaml
state: THEMING
entry_actions:
  - invoke_theme_factory_skill
  - select_theme
  - generate_css
  - verify_accessibility
exit_actions:
  - store_theme_result
  - log_decisions
transitions:
  - trigger: theming_complete
    target: DESIGNING
  - trigger: theming_failed
    target: DESIGNING  # Use default theme
context:
  theme:
    name: string
    lightMode: object
    darkMode: object
    accessibilityReport: object
```

### DESIGNING
**Description**: Running frontend-design skill for implementation design.

```yaml
state: DESIGNING
entry_actions:
  - invoke_frontend_design_skill
  - apply_theme
  - design_components
  - plan_layouts
exit_actions:
  - store_design_result
  - log_decisions
transitions:
  - trigger: designing_complete
    target: VALIDATING
  - trigger: designing_failed
    target: VALIDATING  # Partial design
context:
  design:
    aesthetic: object
    components: array
    pages: array
    animations: object
```

### VALIDATING
**Description**: Running all validation skills for comprehensive compliance check.

```yaml
state: VALIDATING
entry_actions:
  # Core validation
  - invoke_next_best_practices_skill
  - check_file_structure
  - verify_rsc_boundaries
  - validate_patterns

  # Code quality validation
  - invoke_coding_principles_skill
  - check_dry_compliance
  - verify_kiss_patterns
  - validate_srp

  # SEO validation (conditional - public pages only)
  - check_if_public_page
  - invoke_seo_skill  # If public
  - validate_metadata
  - verify_structured_data
  - check_llms_txt

  # Styling validation
  - invoke_styling_skill
  - check_semantic_colors
  - verify_responsive_design
  - validate_tailwind_patterns

exit_actions:
  - store_validation_result
  - log_recommendations
  - aggregate_compliance_status
transitions:
  - trigger: validation_complete
    target: GENERATING
  - trigger: validation_failed
    target: GENERATING  # With warnings
context:
  compliance:
    status: pass | warn | fail

    nextBestPractices:
      status: pass | warn | fail
      checks: array
      recommendations: array

    codingPrinciples:
      dry: pass | warn | fail
      kiss: pass | warn | fail
      srp: pass | warn | fail
      recommendations: array

    seo:
      applied: boolean  # false for private routes
      metadata: pass | warn | fail
      structuredData: pass | warn | fail
      llmsTxt: pass | warn | fail
      recommendations: array

    styling:
      semanticColors: pass | warn | fail
      responsiveDesign: pass | warn | fail
      tailwindPatterns: pass | warn | fail
      recommendations: array
```

### GENERATING
**Description**: Generating final output specification.

```yaml
state: GENERATING
entry_actions:
  - compile_all_results
  - generate_implementation_plan
  - create_file_list
  - format_output
exit_actions:
  - store_final_output
  - calculate_metrics
transitions:
  - trigger: generation_complete
    target: COMPLETED
  - trigger: generation_failed
    target: FAILED
context:
  projectSpec:
    metadata: object
    enhanced: object
    features: object
    theme: object
    design: object
    compliance: object
    decisions: array
    implementationPlan: object
```

### COMPLETED
**Description**: Flow successfully completed.

```yaml
state: COMPLETED
entry_actions:
  - log_completion
  - emit_success_event
context:
  result: projectSpec
  duration: number
  decisionCount: number
```

### FAILED
**Description**: Flow failed with unrecoverable error.

```yaml
state: FAILED
entry_actions:
  - log_error
  - emit_failure_event
  - cleanup_resources
context:
  error:
    phase: string
    message: string
    stack: string
  partialResult: object | null
```

## Transition Guards

### Can Transition Rules

```javascript
const guards = {
  // Must have valid prompt
  canInitialize: (context) => {
    return context.prompt && context.prompt.length > 0;
  },

  // Must have project type
  canBrainstorm: (context) => {
    return context.enhanced?.projectType != null;
  },

  // Must have features
  canTheme: (context) => {
    return context.features?.core?.length > 0;
  },

  // Must have theme
  canDesign: (context) => {
    return context.theme?.name != null;
  },

  // Must have design
  canValidate: (context) => {
    return context.design?.components?.length > 0;
  },

  // Must have validation result
  canGenerate: (context) => {
    return context.compliance != null;
  }
};
```

## Error Recovery

### Fallback Strategies

```yaml
fallbacks:
  ENHANCING_PROMPT:
    strategy: use_defaults
    defaults:
      projectType: landing
      audience: { primary: b2c }
      complexity: medium
      aestheticDirection:
        style: modern-minimalist
        mood: professional
        intensity: moderate

  BRAINSTORMING:
    strategy: minimal_features
    defaults:
      core:
        - name: Basic Layout
          components: [Header, Footer, MainContent]

  THEMING:
    strategy: default_theme
    defaults:
      name: modern-minimalist
      # Use bundled default CSS

  DESIGNING:
    strategy: generic_design
    defaults:
      aesthetic:
        direction: clean-functional
      components: []  # Will be generated from features

  VALIDATING:
    strategy: skip_with_warning
    defaults:
      status: warn
      message: "Validation skipped, manual review recommended"
```

## Flow Events

### Event Types

```typescript
type FlowEvent =
  | { type: 'FLOW_STARTED'; flowId: string; prompt: string }
  | { type: 'PHASE_STARTED'; phase: string }
  | { type: 'PHASE_COMPLETED'; phase: string; duration: number }
  | { type: 'DECISION_MADE'; phase: string; decision: Decision }
  | { type: 'ERROR_OCCURRED'; phase: string; error: Error }
  | { type: 'FALLBACK_USED'; phase: string; fallback: string }
  | { type: 'FLOW_COMPLETED'; result: ProjectSpec }
  | { type: 'FLOW_FAILED'; error: Error };
```

### Event Handlers

```yaml
handlers:
  FLOW_STARTED:
    - log_start
    - init_metrics

  PHASE_COMPLETED:
    - update_progress
    - log_phase_result

  DECISION_MADE:
    - store_decision
    - update_context

  ERROR_OCCURRED:
    - log_error
    - attempt_recovery
    - notify_if_critical

  FLOW_COMPLETED:
    - calculate_metrics
    - generate_summary
    - cleanup
```

## Progress Tracking

```yaml
progress:
  phases:
    - name: enhance-prompt
      weight: 10
      skills: [enhance-prompt]
    - name: brainstorming
      weight: 15
      skills: [brainstorming]
    - name: theme-factory
      weight: 15
      skills: [theme-factory, styling]
    - name: frontend-design
      weight: 25
      skills: [frontend-design, components]
    - name: validation
      weight: 25
      skills: [next-best-practices, coding-principles, seo, styling]
    - name: generate
      weight: 10
      skills: []

  calculation: |
    completed_weight = sum(phase.weight for phase in completed_phases)
    total_weight = 100
    progress_percent = completed_weight / total_weight * 100

  skill_tracking:
    core:
      - enhance-prompt
      - brainstorming
      - theme-factory
      - frontend-design
      - next-best-practices
    supporting:
      - coding-principles  # Always in validation
      - styling            # Theme + validation
      - components         # Design phase
    conditional:
      - seo                # Public pages only
      - api-integration    # Data features
      - translation        # Multi-language
```
