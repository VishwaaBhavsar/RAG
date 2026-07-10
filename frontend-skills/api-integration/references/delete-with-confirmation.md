# DELETE with Confirmation Dialog

Delete actions with AlertDialog confirmation and loading states.

> **Note:** This is the **default pattern** for delete operations. If the user specifies different requirements (e.g., inline delete, no confirmation, custom dialog), follow the user's requirements instead.

---

## Default Pattern

```
User clicks delete → Confirmation dialog opens
User clicks "Cancel" → Dialog closes, nothing happens
User clicks "Confirm" → Button disabled + spinner + API call
├── Success → Toast success, dialog closes, item removed from UI
└── Error → Toast error, button re-enables, dialog stays open
```

---

## Delete Mutation Hook

Create a mutation hook for the delete operation:

```typescript
// apps/frontend/src/hooks/workspace/useWorkspaceMutations.ts
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/lib/query/queryClient'
import { WorkspaceService } from '@/services/workspaceService'
import { workspaceKeys } from './queryKeys'

export function useDeleteWorkspaceMutation() {
  return useMutation({
    mutationFn: (id: string) => WorkspaceService.delete(id),
    onSuccess: (_, deletedId) => {
      queryClient.invalidateQueries({ queryKey: workspaceKeys.list() })
      queryClient.removeQueries({ queryKey: workspaceKeys.detail(deletedId) })
    },
  })
}
```

---

## Generic DeleteButton Component (Recommended)

Use the reusable `DeleteButton` component for standard delete operations:

```typescript
import { DeleteButton } from '@/components';
import useMultiLanguage from '@/hooks/useMultiLanguage';
import { useDeleteWorkspaceMutation } from '@/hooks/workspace/useWorkspaceMutations';
import { showSuccessToast, showErrorToast } from '@/lib/toast';

// Example: Full-featured DeleteButton usage

const deleteWorkspaceMutation = useDeleteWorkspaceMutation();
const { PROJECT, BUTTONS, MESSAGES } = useMultiLanguage();

<DeleteButton
  // Required props
  deleteMutation={deleteWorkspaceMutation}
  deletePayload={workspace.id}               // Can be id, array of ids, or object

  // Custom i18n text (optional - defaults to DELETE_DIALOG.* translations)
  dialogTitle={PROJECT.DELETE_TITLE}         // e.g., "Delete Project?" or omit for default "Are you sure you want to delete?"
  dialogDescription={PROJECT.DELETE_DESCRIPTION} // e.g., "All project data will be lost." or omit for default
  confirmText={PROJECT.REMOVE}               // e.g., "Remove" or omit for default "Delete"
  cancelText={BUTTONS.CANCEL}                // Omit for default "Cancel"
  loadingText={PROJECT.REMOVING}             // e.g., "Removing..." or omit for default "Deleting..."

  // Button styling (optional)
  variant="destructive"                      // "destructive" | "ghost" | "outline" | etc.
  size="sm"                                  // "sm" | "icon" | "default" | "lg"
  className="ml-2"

  // Custom trigger content (optional - defaults to Trash2 icon)
  // children={<Trash2 className="h-4 w-4 text-red-500" />}

  // Callbacks
  onSuccess={(response) => {
    showSuccessToast(
      response?.message || MESSAGES.DELETE_SUCCESS_DESCRIPTION,
      MESSAGES.DELETE_SUCCESS,
    );
    router.push('/dashboard');
  }}
  onError={(error) => showErrorToast(
    error.message || MESSAGES.DELETE_FAILED_DESCRIPTION,
    MESSAGES.DELETE_FAILED,
  )}
/>

```

### DeleteButton Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `deleteMutation` | `{ mutate: (data: T) => void, isPending, isSuccess, isError, error, data, reset }` | required | Full mutation result from useMutation hook |
| `deletePayload` | `T` (generic) | required | Data to pass to mutation (id, array, object, etc.) |
| `dialogTitle` | `string` | i18n "Are you sure you want to delete?" | Custom dialog title (e.g., PROJECT.DELETE_TITLE) |
| `dialogDescription` | `string` | i18n "This action cannot be undone." | Custom dialog description |
| `confirmText` | `string` | i18n "Delete" | Custom confirm button text |
| `cancelText` | `string` | i18n "Cancel" | Custom cancel button text |
| `loadingText` | `string` | i18n "Deleting..." | Custom loading text |
| `variant` | `ButtonProps['variant']` | `"destructive"` | Trigger button variant |
| `size` | `ButtonProps['size']` | `"sm"` | Trigger button size |
| `className` | `string` | - | Trigger button className |
| `children` | `ReactNode` | `<Trash2 />` | Custom trigger content |
| `onSuccess` | `(response: R) => void` | - | Callback triggered via useEffect when isSuccess |
| `onError` | `(error: Error) => void` | - | Callback triggered via useEffect when isError |

---

## Use Existing Components

Import from barrel export:
```typescript
import { DeleteButton, AlertDialog, ButtonWithLoader } from '@/components';
```

- **`DeleteButton`** — recommended for standard delete operations
- **`AlertDialog`** — for custom confirmation dialogs
- **`ButtonWithLoader`** — for submit buttons with loading state

---

## Custom Scenarios

For custom delete scenarios not covered by the props above, follow the same pattern as the `DeleteButton` component at `apps/frontend/src/components/ui/DeleteButton.tsx`.

---

## Key Points

- Prefer `DeleteButton` component for standard delete operations
- Use `AlertDialog` (not Dialog) for destructive actions
- Disable Cancel button during `isPending`
- Uses `useEffect` with `isSuccess`/`isError` states (not callbacks in mutate)
- Calls `reset()` after handling success/error to allow retry
- Close dialog only on success, keep open on error (button re-enables)
