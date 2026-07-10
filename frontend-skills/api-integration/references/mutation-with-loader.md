# Mutation with Button Loading

POST/PUT/PATCH mutations with loading states.

**Use `i18n` skill** for all static text via `useMultiLanguage` hook.

---

## Use Existing Component

**`ButtonWithLoader`** from `@/components`:

```typescript
const { BUTTONS } = useMultiLanguage()

<ButtonWithLoader isLoading={isPending} loadingText={BUTTONS.SAVING}>
  {BUTTONS.SAVE}
</ButtonWithLoader>
```

---

## Mutation Hook

Use the **global query client** from `apps/frontend/src/lib/query/queryClient.ts` rather than `useQueryClient`, and strongly type the mutation with response and variable types.

```typescript
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/lib/query/queryClient'
import { WorkspaceService } from '@/services/workspaceService'
import { workspaceKeys } from '@/hooks/workspace/queryKeys'
import type {
  UpdateWorkspaceBody,
  WorkspaceWithMembersResponse,
} from '@backend/types/client'

type UpdateWorkspaceVariables = {
  id: string
  body: UpdateWorkspaceBody
}

export function useUpdateWorkspaceMutation() {
  return useMutation<
    WorkspaceWithMembersResponse,
    Error,
    UpdateWorkspaceVariables
  >({
    mutationFn: ({ id, body }) => WorkspaceService.update(id, body),
    onSuccess: (data, variables) => {
      queryClient.setQueryData(workspaceKeys.detail(variables.id), data)
      queryClient.invalidateQueries({ queryKey: workspaceKeys.list() })
    },
  })
}
```

**Note:** Hook only handles cache operations. Use `useEffect` in components to handle `isSuccess`/`isError` states for toasts and UI feedback.

---

## Examples

```typescript
import { useEffect, useState } from 'react';
import useMultiLanguage from '@/hooks/useMultiLanguage';
import { showSuccessToast, showErrorToast } from '@/lib/toast';
```

### Action Button with Toast
```typescript
const { BUTTONS, MESSAGES } = useMultiLanguage()
const { mutate, isPending, isSuccess, isError, error, reset, data: responseData } = useUpdateWorkspaceMutation()

// toast only if user explicitly requests success message
useEffect(() => {
  if (isSuccess && responseData) {
    showSuccessToast(
      responseData.message || MESSAGES.UPDATE_SUCCESS_DESCRIPTION,
      MESSAGES.UPDATE_SUCCESS,
    )
    reset()
  }
}, [isSuccess, responseData, MESSAGES.UPDATE_SUCCESS, MESSAGES.UPDATE_SUCCESS_DESCRIPTION, reset])

useEffect(() => {
  if (isError && error) {
    showErrorToast(
      error.message || MESSAGES.UPDATE_FAILED_DESCRIPTION,
      MESSAGES.UPDATE_FAILED,
    )
    reset()
  }
}, [isError, error, MESSAGES.UPDATE_FAILED, MESSAGES.UPDATE_FAILED_DESCRIPTION, reset])

<ButtonWithLoader
  isLoading={isPending}
  loadingText={BUTTONS.SAVING}
  onClick={() => mutate(payload)}
>
  {BUTTONS.SAVE}
</ButtonWithLoader>
```

### Form Submit
```typescript
import { useForm } from 'react-hook-form';

const { BUTTONS, MESSAGES } = useMultiLanguage()
const { register, handleSubmit } = useForm<{ name: string }>()
const { mutate, isPending, isError, error, reset } = useUpdateWorkspaceMutation()

useEffect(() => {
  if (isError && error) {
    showErrorToast(error.message || MESSAGES.UPDATE_FAILED_DESCRIPTION, MESSAGES.UPDATE_FAILED)
    reset()
  }
}, [isError, error, MESSAGES.UPDATE_FAILED, MESSAGES.UPDATE_FAILED_DESCRIPTION, reset])

<form onSubmit={handleSubmit((formData) => mutate({ id, body: formData }))}>
  <Input {...register('name')} disabled={isPending} />
  <ButtonWithLoader type="submit" isLoading={isPending} loadingText={BUTTONS.SAVING}>
    {BUTTONS.SAVE}
  </ButtonWithLoader>
</form>
```

### Dialog (close on success)
```typescript
const { BUTTONS } = useMultiLanguage()
const [open, setOpen] = useState(false)
const { mutate, isPending, isSuccess, reset } = useCreateWorkspaceMutation()

useEffect(() => {
  if (isSuccess) {
    setOpen(false)
    reset()
  }
}, [isSuccess, reset])

<ButtonWithLoader isLoading={isPending} loadingText={BUTTONS.CREATING} onClick={() => mutate(formData)}>
  {BUTTONS.CREATE}
</ButtonWithLoader>
```

---

## Auth Pages: Inline Errors

Use inline `<Alert>` instead of toast for login/register.
