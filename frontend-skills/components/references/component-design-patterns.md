# Component Design Patterns

Architectural patterns for organizing React components.

---

## Component Classification

| Type | State | Location | Example |
|------|-------|----------|---------|
| **UI Primitive** | Props only | `components/ui/` | `Button`, `Card`, `Badge` |
| **Stateful UI** | Local UI state | `components/ui/` | `DeleteButton`, `SearchInput` |
| **Feature Component** | Props only | `components/[domain]/` | `ProjectCard`, `MemberItem` |
| **State Component** | Props only | `components/` | `EmptyState`, `LoadingState` |
| **Container** | Fetches data | `components/[domain]/` or page | `ProjectListContainer` |
| **Form** | Form state | `components/[domain]/` | `CreateProjectForm` |

---

## 1. UI Primitive (Stateless)

Pure presentation, fully controlled via props. No internal state.

**Location:** `components/ui/`

**Rules:**
- No `useState`, no `useEffect`
- No API calls
- All behavior via props
- Use `forwardRef` when extending shadcn/ui

| Pattern | Reference File |
|---------|----------------|
| Extended Button | `components/ui/ButtonWithLoader.tsx` |
| Extended Button with Icon | `components/ui/ButtonWithIcon.tsx` |

---

## 2. Stateful UI Component

Has **local UI state** (modals, toggles, debounce), but logic is passed via props.

**Location:** `components/ui/`

**Reference:** `components/ui/DeleteButton.tsx`

**Rules:**
- Local state for UI only (open/close, loading visual, mode toggle)
- Business logic via props (`mutation`, `onSuccess`, `onSave`)
- Reusable across domains

**Common Stateful UI Components:**

| Component | UI State | Reference/Behavior |
|-----------|----------|----------|
| DeleteButton | Dialog open/close | `components/ui/DeleteButton.tsx` |
| SearchInput | Debounced value | Internal debounce timer, emits final value via `onChange` |

---

## 3. Feature Component (Presentational)

Domain-specific display component. No state, props-driven.

**Location:** `components/[domain]/`

**Rules:**
- No `useState`, no `useEffect`
- Data received via props
- Callbacks via props (`onClick`, `onEdit`)

| Pattern | Reference File |
|---------|----------------|
| Card | `components/projects/ProjectCard.tsx` |
| List Item | `components/team/MemberItem.tsx` |
| List Item with Invite | `components/team/PendingInviteItem.tsx` |
| Stat Card | `components/usage/UsageStatCard.tsx` |

---

## 4. State Component

Shows UI states (loading, error, empty). Presentational, no internal state.

**Location:** `components/` or `components/ui/`

| State | Reference File |
|-------|----------------|
| Empty | `components/EmptyState.tsx` |
| Loading | `components/LoadingState.tsx` |
| Error | `components/ErrorState.tsx` |

---

## 5. Container Component

Fetches data, manages state, renders presentational components.

**Location:** `components/[domain]/` or directly in page

**Pattern:**
```tsx
export function ProjectListContainer() {
  const { data, isLoading, error } = useProjectsQuery();

  if (isLoading) return <ProjectListSkeleton />;
  if (error) return <ErrorState message={error.message} />;
  if (!data?.length) return <EmptyState title="No projects" />;

  return <ProjectList projects={data} />;
}
```

---

## 6. Composition Pattern

For complex UI with multiple slots, use compound components.

```tsx
// Compound component pattern
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Description>Description</Card.Description>
  </Card.Header>
  <Card.Content>Content</Card.Content>
  <Card.Footer>Footer</Card.Footer>
</Card>

// vs Prop drilling (avoid for complex cases)
<Card
  title="Title"
  description="Description"
  content={<div>Content</div>}
  footer={<Button>Action</Button>}
/>
```

**When to use Composition:**
- Multiple content slots
- Flexible content arrangement
- Complex nested structures

---

## 7. Use Enums for Conditional Rendering

**See:** `coding-principles` skill → [references/typescript.md#2-use-enums-for-conditional-rendering](../../coding-principles/references/typescript.md#2-use-enums-for-conditional-rendering)

---

## Decision Tree

```
Creating a new component?
│
├─ Is it a basic UI element (button, input, badge)?
│  └─ YES → UI Primitive in components/ui/
│
├─ Does it need local UI state (modal, dropdown)?
│  └─ YES → Stateful UI in components/
│
├─ Is it domain-specific display (ProjectCard)?
│  └─ YES → Feature Component in components/[domain]/
│
├─ Does it fetch data or manage complex state?
│  └─ YES → Container in components/[domain]/ or page
│
└─ Is it a form with validation?
   └─ YES → Form Component (see creating-forms.md)
```

---

## Folder Structure

```
components/
├── ui/                     # Primitives + Stateful UI
│   ├── Button.tsx          # Primitive
│   ├── Card.tsx            # Primitive (with composition)
│   ├── DeleteButton.tsx    # Stateful UI
│   └── ButtonWithLoader.tsx # Extended Primitive
├── projects/               # Domain: Projects
│   ├── ProjectCard.tsx     # Feature (presentational)
│   └── index.ts            # Barrel export
├── team/                   # Domain: Team
│   ├── MemberItem.tsx      # Feature (presentational)
│   └── InviteMemberForm.tsx # Form
├── skeletons/              # Loading skeletons
│   └── ProjectsSkeleton.tsx # Domain-specific skeleton
└── index.ts                # Barrel exports
```

---

## Related Skills (Required)

| Skill | Use for |
|-------|---------|
| `styling` | Colors, spacing, cn() utility, design tokens, Tailwind patterns |
| `translation` | Static labels, placeholders, button text, error messages |

---

## Checklist

**Before creating:**
- [ ] Component doesn't already exist (check references above)
- [ ] Similar component doesn't exist that can be extended
- [ ] Correct folder identified: `ui/` vs `[domain]/` vs root

**After creating:**
- [ ] Uses named export (not default)
- [ ] Props interface exported with component
- [ ] Accepts `className` prop for style overrides
- [ ] Uses `cn()` for className composition
- [ ] Added to barrel exports

**Required:**
- [ ] **Styling:** Follow `styling` skill for colors, spacing, design tokens
- [ ] **Translation:** Use `translation` skill for all static text (labels, placeholders, buttons, errors)
- [ ] **TypeScript:** Follow `coding-principles` skill → `references/typescript.md` for enums, strict typing

---

## Barrel Export

```tsx
// feature/index.ts
export { MyComponent, type MyComponentProps } from './MyComponent';

// components/index.ts (if shared)
export * from './feature';
```
