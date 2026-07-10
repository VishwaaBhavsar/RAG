# Supabase DELETE with Confirmation

Default pattern: confirm before destructive work; **`DeleteButton`** from **`@/components`** handles dialog, loading, and **`isPending`** on cancel.

**Service contract** (no `.select()` on DELETE, return **`{ id }`**): **`SKILL.md`** → *Service return contract*.

If the user specifies a different UX (inline delete, no dialog), follow the product spec instead of this default.

---

## Flow

```
User clicks delete → confirmation dialog opens
Cancel → dialog closes
Confirm → pending state → Supabase delete
├── Success → optional toast; close dialog; invalidate/remove cache
└── Error → toast or inline message; dialog can stay open; retry after reset()
```

---

## Service

```typescript
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'

export class ProjectService {
  static async delete(id: string) {
    await getSupabaseClient().from('projects').delete().eq('id', id).throwOnError()
    return { id }
  }
}
```

---

## Delete mutation hook

```typescript
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/lib/query/queryClient'
import { ProjectService } from '@/services/projectService'
import { projectKeys } from '@/hooks/projects/queryKeys'

export function useDeleteProjectMutation() {
  return useMutation({
    mutationFn: (id: string) => ProjectService.delete(id),
    onSuccess: (_, deletedId) => {
      queryClient.invalidateQueries({ queryKey: projectKeys.all })
      queryClient.removeQueries({ queryKey: projectKeys.detail(deletedId) })
    },
  })
}
```

---

## DeleteButton (recommended)

```typescript
import { DeleteButton } from '@/components'
import useMultiLanguage from '@/hooks/useMultiLanguage'
import { useDeleteProjectMutation } from '@/hooks/projects/useProjectMutations'
import { showSuccessToast, showErrorToast } from '@/lib/toast'

const deleteProjectMutation = useDeleteProjectMutation()
const { PROJECT, BUTTONS, MESSAGES } = useMultiLanguage()

<DeleteButton
  deleteMutation={deleteProjectMutation}
  deletePayload={project.id}
  dialogTitle={PROJECT.DELETE_TITLE}
  dialogDescription={PROJECT.DELETE_DESCRIPTION}
  confirmText={PROJECT.REMOVE}
  cancelText={BUTTONS.CANCEL}
  loadingText={PROJECT.REMOVING}
  variant="destructive"
  size="sm"
  onSuccess={() => {
    showSuccessToast(
      MESSAGES.DELETE_SUCCESS_DESCRIPTION,
      MESSAGES.DELETE_SUCCESS,
    )
  }}
  onError={(err) =>
    showErrorToast(
      err.message || MESSAGES.DELETE_FAILED_DESCRIPTION,
      MESSAGES.DELETE_FAILED,
    )
  }
/>
```

### Props (summary)

| Prop | Role |
|------|------|
| `deleteMutation` | Full `useMutation` result |
| `deletePayload` | Argument to `mutationFn` (often `id`) |
| `dialogTitle` / `dialogDescription` / `confirmText` / `cancelText` / `loadingText` | i18n strings |
| `onSuccess` / `onError` | Usually toasts; implement with `useEffect` inside `DeleteButton` pattern |

Full prop list: read **`apps/frontend/src/components/ui/DeleteButton.tsx`** if behavior must diverge.

---

## Custom dialog

Use **`AlertDialog`** (not **`Dialog`**) for destructive actions. Disable cancel while **`isPending`**. After handling success or error in **`useEffect`**, call **`reset()`** on the mutation so the same control can retry.

---

## Imports

```typescript
import { DeleteButton, AlertDialog, ButtonWithLoader } from '@/components'
```
