# Supabase Mutations with Button Loading

INSERT/UPDATE: services use **`getSupabaseClient()`** and PostgREST chains per **`SKILL.md`** (**.throwOnError()`, `.select()` before `.single()`, global `queryClient`**).

**Copy:** **`useMultiLanguage`** (**translation** skill). **Buttons:** **`ButtonWithLoader`** from **`@/components`** (**components** skill).

---

## Service examples

```typescript
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'
import type { Tables, TablesInsert, TablesUpdate } from '@/lib/supabase/database.types'

type ProjectRow = Tables<'projects'>

export class ProjectService {
  static async create(input: TablesInsert<'projects'>) {
    const { data } = await getSupabaseClient()
      .from('projects')
      .insert(input)
      .select('id, workspace_id, name')
      .single()
      .throwOnError()
    return data as ProjectRow
  }

  static async update(id: string, patch: TablesUpdate<'projects'>) {
    const { data } = await getSupabaseClient()
      .from('projects')
      .update(patch)
      .eq('id', id)
      .select('id, workspace_id, name')
      .single()
      .throwOnError()
    return data as ProjectRow
  }
}
```

**DELETE:** no `.select()` on the chain → **`delete-with-confirmation.md`**.

---

## Mutation hook

Hooks own cache updates only; use **`useEffect`** in components for toasts / dialog close / navigation.

```typescript
import { queryClient } from '@/lib/query/queryClient'

type CreateProjectVariables = { workspaceId: string; name: string }

export function useCreateProjectMutation() {
  return useMutation<ProjectRow, Error, CreateProjectVariables>({
    mutationFn: ({ workspaceId, name }) =>
      ProjectService.create({ workspace_id: workspaceId, name }),
    onSuccess: (created) => {
      queryClient.invalidateQueries({
        queryKey: projectKeys.list(created.workspace_id),
      })
      queryClient.setQueryData(projectKeys.detail(created.id), created)
    },
  })
}
```

---

## ButtonWithLoader

```typescript
const { BUTTONS } = useMultiLanguage()

<ButtonWithLoader isLoading={isPending} loadingText={BUTTONS.SAVING}>
  {BUTTONS.SAVE}
</ButtonWithLoader>
```

---

## Action button + toast (product asks for success feedback)

Toast only when the product expects it; map errors to **`MESSAGES.*`** / **`ERRORS.*`**.

```typescript
import { useEffect } from 'react'
import useMultiLanguage from '@/hooks/useMultiLanguage'
import { showSuccessToast, showErrorToast } from '@/lib/toast'

const { BUTTONS, MESSAGES } = useMultiLanguage()
const { mutate, isPending, isSuccess, isError, error, reset, data: responseData } =
  useUpdateProjectMutation()

useEffect(() => {
  if (isSuccess && responseData) {
    showSuccessToast(
      responseData.message ?? MESSAGES.UPDATE_SUCCESS_DESCRIPTION,
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

---

## Form submit

```typescript
import { useForm } from 'react-hook-form'

const { BUTTONS, MESSAGES } = useMultiLanguage()
const { register, handleSubmit } = useForm<{ name: string }>()
const { mutate, isPending, isError, error, reset } = useUpdateProjectMutation()

useEffect(() => {
  if (isError && error) {
    showErrorToast(error.message || MESSAGES.UPDATE_FAILED_DESCRIPTION, MESSAGES.UPDATE_FAILED)
    reset()
  }
}, [isError, error, MESSAGES.UPDATE_FAILED, MESSAGES.UPDATE_FAILED_DESCRIPTION, reset])

<form onSubmit={handleSubmit((formData) => mutate({ id, patch: formData }))}>
  <Input {...register('name')} disabled={isPending} />
  <ButtonWithLoader type="submit" isLoading={isPending} loadingText={BUTTONS.SAVING}>
    {BUTTONS.SAVE}
  </ButtonWithLoader>
</form>
```

---

## Dialog (close on success)

```typescript
import { useEffect, useState } from 'react'

const { BUTTONS } = useMultiLanguage()
const [open, setOpen] = useState(false)
const { mutate, isPending, isSuccess, reset } = useCreateProjectMutation()

useEffect(() => {
  if (isSuccess) {
    setOpen(false)
    reset()
  }
}, [isSuccess, reset])

<ButtonWithLoader
  isLoading={isPending}
  loadingText={BUTTONS.CREATING}
  onClick={() => mutate(formData)}
>
  {BUTTONS.CREATE}
</ButtonWithLoader>
```

---

## Auth-style pages

Prefer inline **`<Alert>`** for login/register errors instead of toasts.
