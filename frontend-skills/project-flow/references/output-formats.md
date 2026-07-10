# Inter-Skill Data Schemas

Standardized data formats for communication between skills.

## Master Context Object

```typescript
interface ProjectContext {
  // Metadata
  metadata: {
    flowId: string;
    startTime: string;
    originalPrompt: string;
    version: string;
  };

  // Phase 1: Enhanced Prompt
  enhanced: EnhancedSpec;

  // Phase 2: Features
  features: FeatureSpec;

  // Phase 3: Theme
  theme: ThemeSpec;

  // Phase 4: Design
  design: DesignSpec;

  // Phase 5: Compliance
  compliance: ComplianceSpec;

  // All decisions made
  decisions: Decision[];

  // Final implementation plan
  implementationPlan: ImplementationPlan;
}
```

## Phase 1: Enhanced Prompt Schema

```typescript
interface EnhancedSpec {
  projectType: ProjectType;
  audience: AudienceSpec;
  complexity: 'simple' | 'medium' | 'complex';
  aestheticDirection: AestheticSpec;
  pageStructure: PageSpec[];
  contentRequirements: ContentSpec;
  technicalContext: TechnicalSpec;
}

type ProjectType =
  | 'landing'
  | 'dashboard'
  | 'ecommerce'
  | 'saas'
  | 'portfolio'
  | 'blog'
  | 'documentation'
  | 'marketplace';

interface AudienceSpec {
  primary: 'b2b' | 'b2c' | 'developer' | 'creative' | 'enterprise';
  demographics: string;
  techSavviness: 'low' | 'medium' | 'high';
  expectations: string[];
}

interface AestheticSpec {
  style: string;
  mood: string;
  intensity: 'subtle' | 'moderate' | 'bold';
  keywords: string[];
  avoidances: string[];
}

interface PageSpec {
  name: string;
  route: string;
  sections: SectionSpec[];
  priority: 'critical' | 'important' | 'optional';
  seoRequired: boolean;
}

interface SectionSpec {
  name: string;
  purpose: string;
  components: string[];
  dataNeeds: string[];
}

interface ContentSpec {
  copyTone: string;
  imagery: 'photography' | 'illustrations' | 'abstract' | 'icons' | 'mixed';
  contentDensity: 'sparse' | 'balanced' | 'dense';
  cta: {
    primary: string;
    secondary?: string;
  };
}

interface TechnicalSpec {
  framework: 'next' | 'react' | 'vue';
  responsive: boolean;
  accessibility: 'A' | 'AA' | 'AAA';
  performance: 'standard' | 'optimized' | 'critical';
  features: string[];
}
```

## Phase 2: Features Schema

```typescript
interface FeatureSpec {
  core: Feature[];
  enhanced: Feature[];
  premium: Feature[];
}

interface Feature {
  name: string;
  description: string;
  components: ComponentRef[];
  dataRequirements: DataRequirement[];
  rationale: string;
}

interface ComponentRef {
  name: string;
  type: 'ui' | 'logic' | 'integration';
  complexity: 'simple' | 'medium' | 'complex';
}

interface DataRequirement {
  entity: string;
  fields: FieldSpec[];
  source: 'static' | 'api' | 'user-input';
}

interface FieldSpec {
  name: string;
  type: string;
  required: boolean;
}

interface ComponentInventory {
  ui: UIComponent[];
  logic: LogicComponent[];
}

interface UIComponent {
  name: string;
  usedBy: string[];
  variants: string[];
  props: string[];
}

interface LogicComponent {
  name: string;
  purpose: string;
  dependencies: string[];
}

interface DataSchema {
  entities: EntitySpec[];
}

interface EntitySpec {
  name: string;
  fields: FieldSpec[];
  relations: string[];
}
```

## Phase 3: Theme Schema

```typescript
interface ThemeSpec {
  name: string;
  description: string;

  lightMode: {
    css: string;  // Complete @theme block
  };

  darkMode: {
    css: string;  // Dark mode @theme block
  };

  semanticTokens: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    foreground: string;
    muted: string;
    border: string;
    success: string;
    warning: string;
    error: string;
    info: string;
  };

  accessibilityReport: AccessibilityReport;

  usage: {
    primaryUse: string;
    accentUse: string;
    backgroundPattern: string;
  };
}

interface AccessibilityReport {
  level: 'AA' | 'AAA';
  passes: ContrastCheck[];
  warnings: string[];
}

interface ContrastCheck {
  pair: [string, string];
  ratio: number;
  required: number;
  status: 'pass' | 'fail';
}
```

## Phase 4: Design Schema

```typescript
interface DesignSpec {
  aesthetic: {
    direction: string;
    keyElements: string[];
    avoidances: string[];
  };

  components: ComponentDesign[];
  pages: PageDesign[];

  animations: {
    intensity: 'minimal' | 'subtle' | 'moderate' | 'bold';
    pageLoad: AnimationSpec[];
    interactions: AnimationSpec[];
  };

  codeStructure: CodeStructure;
}

interface ComponentDesign {
  name: string;
  file: string;
  purpose: string;
  props: PropSpec[];
  styling: string;
  variants: string[];
}

interface PropSpec {
  name: string;
  type: string;
  required: boolean;
  default?: string;
}

interface PageDesign {
  route: string;
  layout: string;
  sections: SectionDesign[];
  metadata: MetadataSpec;
}

interface SectionDesign {
  name: string;
  component: string;
  order: number;
  animations: string[];
}

interface MetadataSpec {
  title: string;
  description: string;
  ogImage?: string;
}

interface AnimationSpec {
  name: string;
  trigger: 'load' | 'scroll' | 'hover' | 'click';
  duration: string;
  easing: string;
  properties: string[];
}

interface CodeStructure {
  files: FileSpec[];
  directories: string[];
}

interface FileSpec {
  path: string;
  purpose: string;
  dependencies: string[];
  exports: string[];
}
```

## Phase 5: Compliance Schema

```typescript
interface ComplianceSpec {
  status: 'pass' | 'warn' | 'fail';

  checks: ComplianceCheck[];
  recommendations: string[];

  fileStructure: {
    status: 'pass' | 'warn' | 'fail';
    issues: string[];
  };

  rscBoundaries: {
    status: 'pass' | 'warn' | 'fail';
    issues: string[];
  };

  metadata: {
    status: 'pass' | 'warn' | 'fail';
    issues: string[];
  };

  errorHandling: {
    status: 'pass' | 'warn' | 'fail';
    issues: string[];
  };

  performance: {
    status: 'pass' | 'warn' | 'fail';
    issues: string[];
  };
}

interface ComplianceCheck {
  name: string;
  category: string;
  status: 'pass' | 'warn' | 'fail';
  message: string;
  fix?: string;
}
```

## Decision Schema

```typescript
interface Decision {
  phase: string;
  decision: string;
  reason: string;
  confidence: 'high' | 'medium' | 'low';
  alternatives?: string[];
  override?: string;
  timestamp: string;
}
```

## Implementation Plan Schema

```typescript
interface ImplementationPlan {
  files: PlannedFile[];
  order: ImplementationStep[];
  dependencies: DependencySpec[];
  estimates: {
    componentCount: number;
    pageCount: number;
    complexity: 'simple' | 'medium' | 'complex';
  };
}

interface PlannedFile {
  path: string;
  purpose: string;
  type: 'component' | 'page' | 'layout' | 'hook' | 'util' | 'style' | 'config';
  dependencies: string[];
  priority: 'critical' | 'important' | 'optional';
}

interface ImplementationStep {
  order: number;
  description: string;
  files: string[];
  dependencies: string[];
}

interface DependencySpec {
  name: string;
  version: string;
  purpose: string;
  required: boolean;
}
```

## Compact Formats for Inter-Skill Transfer

### enhance-prompt → brainstorming

```yaml
context:
  type: landing
  audience: b2c
  complexity: medium
  style: modern-minimalist
  pages:
    - name: home
      sections: [hero, features, testimonials, cta]
```

### enhance-prompt → theme-factory

```yaml
context:
  type: landing
  style: modern-minimalist
  mood: professional
  intensity: moderate
  audience: b2b
```

### brainstorming → frontend-design

```yaml
context:
  features:
    core: [Feature...]
  components:
    ui: [Component...]
  dataSchema:
    entities: [Entity...]
```

### theme-factory → frontend-design

```yaml
context:
  themeName: modern-minimalist
  css:
    light: "@theme { ... }"
    dark: "@theme dark { ... }"
  tokens:
    primary: "oklch(55% 0.15 250)"
    background: "oklch(99% 0.005 250)"
```

### All → frontend-design (Full Context)

```yaml
context:
  enhanced:
    projectType: landing
    audience: { primary: b2c }
    aestheticDirection: { style: modern-minimalist }
    pageStructure: [...]
  features:
    core: [...]
    enhanced: [...]
  theme:
    name: modern-minimalist
    lightMode: { css: "..." }
    darkMode: { css: "..." }
```

## Output Serialization

All inter-skill data is serialized as YAML for readability and passed through the context object. Each skill reads its required inputs and writes its outputs to the appropriate keys.
