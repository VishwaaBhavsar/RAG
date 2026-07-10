# Supabase SELECT with Skeleton Loading

SELECT: **`queryFn`** calls service static methods only; services use PostgREST + **`.throwOnError()`** per **`SKILL.md`**.

**Copy:** **`useMultiLanguage`**. **Skeleton layouts:** **`references/skeletons.md`**. **Mutation + buttons:** **`references/mutation-with-loader.md`**.

---

## Flow

```
Initial load → skeleton
Ready → content
Error → translated message/state
Empty → empty state
Background refetch → keep content (optional subtle indicator)
```

---

## Joins and nested selects

Typing: **`QueryData<typeof query>`** on the unawaited builder — **`workflow.md`** Step 3b.

---

## Service example (list)

```typescript
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'
import type { Tables } from '@/lib/supabase/database.types'

type TaskRow = Tables<'tasks'>

export class TaskService {
  static async list(projectId: string) {
    const { data } = await getSupabaseClient()
      .from('tasks')
      .select('id, title, status')
      .eq('project_id', projectId)
      .throwOnError()
    return (data ?? []) as TaskRow[]
  }
}
```

---

## Query hook

```typescript
export function useTasksQuery(projectId: string | undefined) {
  return useQuery({
    queryKey: projectId ? taskKeys.list(projectId) : taskKeys.all,
    queryFn: () => TaskService.list(projectId!),
    enabled: !!projectId,
  })
}
```

---

## Page/component

```typescript
import useMultiLanguage from '@/hooks/useMultiLanguage'

const { data, isLoading, isError, error } = useTasksQuery(projectId)
const { ERRORS, COMMON } = useMultiLanguage()

if (isLoading) return <TasksSkeleton />
if (isError) return <div className="text-destructive">{ERRORS?.FETCH_FAILED ?? error.message}</div>
if (!data?.length) return <EmptyState message={COMMON?.NO_DATA} />

return <TaskList tasks={data} />
```

---

## Skeleton while refetching after mutation

After a create/update, some screens show skeleton when the list **`isFetching`** so users do not flash stale rows.

```typescript
const { data, isLoading, isFetching } = useTasksQuery(projectId)
const createMutation = useCreateTaskMutation()

if (isLoading || (createMutation.isSuccess && isFetching)) {
  return <TasksSkeleton />
}
```

---

## Toasts and forms

**`ButtonWithLoader`**, **`useEffect`** after **`isSuccess`/`isError`**, and dialog flows: **`references/mutation-with-loader.md`**.
