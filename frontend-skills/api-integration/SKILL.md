---
name: api-integration
description: Wires frontend components to backend APIs using TanStack Query v5 and the generated API client. Use this skill when adding any API call, writing query or mutation hooks, building loading skeletons, or handling delete confirmations — it provides the correct patterns for services layer, query keys, and generated types from libs/types/src/lib/client/index.ts.
---

# API Integration

Integrate APIs from the auto-generated file: `libs/types/src/lib/client/index.ts`

---

## References

| File | Read when |
|------|-----------|
| `references/workflow.md` | Step-by-step for any new API endpoint |
| `references/get-with-skeleton.md` | GET API with skeleton loading |
| `references/mutation-with-loader.md` | POST/PUT/PATCH with button loading |
| `references/delete-with-confirmation.md` | DELETE with AlertDialog |
| `references/skeletons.md` | Creating skeleton components (Card, Table, Detail) |
| `references/folder-structure.md` | Where files belong |

---

## Key Components

| Component | Import | Use for |
|-----------|--------|---------|
| `ButtonWithLoader` | `import { ButtonWithLoader } from '@/components'` | Button with `isLoading` + `loadingText` |
| `Skeleton` | `import { Skeleton } from '@/components'` | Loading placeholders |
| `AlertDialog` | `import { AlertDialog } from '@/components'` | Delete confirmations |

---

## Quick Reference

| Concern | File |
|---------|------|
| Api client | `apps/frontend/src/lib/axios/apiClient.ts` |
| Query client | `apps/frontend/src/lib/query/queryClient.ts` |
| Toast utilities | `apps/frontend/src/lib/toast` - exports `showSuccessToast`, `showErrorToast`, `showToast` |
| Example hooks | `apps/frontend/src/hooks/workspace/` |
| Example service | `apps/frontend/src/services/workspaceService.ts` |

---

## i18n Integration

**CRITICAL: ALL user-facing text MUST use i18n** - No hardcoded strings in UI

- Use `/translation` command when adding new UI text
- Reference translation keys from the enums
- Use `useMultiLanguage` hook for all static text

```typescript
import useMultiLanguage from '@/hooks/useMultiLanguage'

const { BUTTONS, MESSAGES } = useMultiLanguage()

<ButtonWithLoader isLoading={isPending} loadingText={BUTTONS.SAVING}>
  {BUTTONS.SAVE}
  </ButtonWithLoader>
```

**Examples of text that MUST be translated:**
- Button labels (Save, Delete, Cancel, etc.)
- Toast messages (Success, Error messages)
- Alert dialog titles and descriptions
- Form labels and placeholders
- Validation messages

See `/translation` skill for adding new translation keys.

---

## File Checklist per Feature

**New domain** (e.g., `projects`):

- [ ] `services/<domain>Service.ts`
- [ ] `hooks/<domain>/queryKeys.ts`
- [ ] `hooks/<domain>/use<Domain>Queries.ts`
- [ ] `hooks/<domain>/use<Domain>Mutations.ts`
- [ ] `components/skeletons/<Domain>Skeleton.tsx`
- [ ] Add translations via `i18n` skill

**Single endpoint** (existing domain):

- [ ] Add method to service
- [ ] Add query key (if needed)
- [ ] Add hook (query or mutation) using global `queryClient`
- [ ] Add skeleton (if new UI)

---

## Pattern: Workspace mutation hooks

Key points the generator should follow:

- Import and use the **global** `queryClient` (`apps/frontend/src/lib/query/queryClient.ts`) instead of `useQueryClient`.
- Define explicit `type <Name>Variables` for mutation variables.
- Use `useMutation<ResponseType, Error, VariablesType>(...)` with correct generic types from `@backend/types/client`.
- On success, update detail cache with `queryClient.setQueryData` and invalidate any affected list queries.

---

## Rules

1. Never hand-write endpoint paths - use Api class
2. Never call APIs in components - use hooks
3. Use types from generated file - no `any`
4. Show skeleton for GET loading
5. Use `ButtonWithLoader` for mutations
6. Toast only if user explicitly requests success message
7. Invalidate queries on mutation success
8. Use `useMultiLanguage` hook for all static text (see i18n skill)
9. Use toast utilities: `showSuccessToast(message, title?)`, `showErrorToast(message, title?)`, `showToast(message, type, title?)`
10. Do not call big inline functions in JSX – extract handlers (`handleXClick`) instead.
