---
name: components
description: Discovers and reuses existing React components from apps/frontend/src/components/ before building new ones. Use this skill when you need any UI element — buttons, inputs, modals, cards, tables, forms — to check what already exists and get the correct import paths and usage patterns instead of creating duplicates.
---

# Components Skill

> Find and reuse existing components from `apps/frontend/src/components/`

## ⚠️ Required Workflow

1. **Read this skill doc** before starting
2. Search for existing components first
3. Create/modify components
4. **Run through Code Review Checklist** (REQUIRED - see below)
5. Fix any issues found
6. Report completion

---

## Quick Import

```tsx
// ALWAYS import from barrel export - NOT from individual files
import { Button, Card, CardContent, Input, Badge } from '@/components';

// Import utility
import { cn } from '@/utils/cn';
```

---

## Import Rules

| Do | Don't |
|----|-------|
| `import { Accordion } from '@/components'` | `import { Accordion } from '@/components/ui/accordion'` |
| `import { Button, Card } from '@/components'` | `import { Button } from '@/components/ui/Button'` |

All UI components are re-exported from `@/components/index.ts`. Never import directly from `@/components/ui/*` paths.

---

## References (load only when needed)

| File | Load when... |
|------|--------------|
| `references/ui-primitives.md` | Need Button, Input, Card, Dialog, Form, Table, Badge, Avatar, Toast, Skeleton, or any shadcn/ui component |
| `references/feature-components.md` | Working with Billing, Projects, Team, Notifications, Usage, Settings, Editor, or Landing pages |
| `references/shared-components.md` | Need Layout, Auth guards, Providers, FormError, or root-level shared components |
| `references/component-design-patterns.md` | Creating NEW component: architecture patterns, file references, checklist |
| `references/creating-forms.md` | Creating NEW form: types, validation, hooks, component workflow |

---

## Before Creating New Component

- [ ] Search existing components in reference files above
- [ ] Check if similar component exists that can be extended
- [ ] Identify correct folder: `ui/` (primitive) vs feature folder vs root
- [ ] Review existing patterns in similar components

---

## Styling

For styling guidelines, colors, and class composition:
- Use the `styling` skill

---

## Code Review Checklist

**⚠️ MANDATORY: Do NOT consider the task complete until you have verified ALL items below.**

After creating or modifying components, verify:

- [ ] **Imports from barrel**: All UI imports use `from '@/components'`, not `from '@/components/ui/*'`
- [ ] **Section centering**: All sections with `.container` have `flex items-center justify-center` (see styling skill)
- [ ] **Mobile-first design**: Base styles for mobile, `md:` / `lg:` for larger screens (see styling skill)
- [ ] **Responsive tested**: Test on mobile (375px), tablet (768px), desktop (1280px+)
- [ ] **No TypeScript errors**: Check IDE diagnostics before completing
- [ ] **Existing components used**: Checked for existing components before creating new ones
- [ ] **Consistent patterns**: Follows existing component patterns in the codebase
- [ ] **Interactive controls are functional**: No visual-only nav tabs, filters, sort controls, or buttons without working handlers
- [ ] **Filter/sort wiring complete**: Controls update rendered data (or query params / route state) and can be reset/cleared
- [ ] **Navigation wiring complete**: All nav items lead to a real destination or section and update UI state correctly
- [ ] **No fake interactions**: Remove placeholder onClick handlers and inert controls before completion

### After Creating New Feature Components

- [ ] Export added to feature's `index.ts`
- [ ] Feature folder exported in main `@/components/index.ts` if needed
- [ ] Component tested in browser (visual review)
- [ ] Component tested for behavior (functional review): click, keyboard interaction, state updates, and empty/reset states

### Enforcement Rules

- [ ] **STOP** before saying "Done" - run through the checklist first
- [ ] **READ** the actual code you wrote, don't assume it's correct
- [ ] **FIX** issues immediately, don't defer to user

If you skip this step, the user will have to fix issues manually.

---

## Directory Structure

```
apps/frontend/src/components/
├── ui/           # shadcn/ui primitives
├── billing/      # Billing domain
├── projects/     # Projects domain
├── team/         # Team domain
├── form/         # Reusable form components
├── providers/    # Context providers
└── index.ts      # Barrel export
```
