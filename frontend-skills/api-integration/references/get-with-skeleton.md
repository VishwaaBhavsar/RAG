# GET API with Skeleton Loading

Fetching data with skeleton loading states.

---

## The Pattern

```
Initial Load → Show Skeleton
Data Ready → Show Content
Error → Show Error Message
Empty → Show Empty State
Background Refetch → Keep showing content (optional subtle indicator)
```

---

## Skeleton Component

See `references/skeletons.md` for skeleton patterns (Card, Table, Detail).

---

## Query Hook

```typescript
export function useWorkspaceListQuery() {
  return useQuery({
    queryKey: workspaceKeys.list(),
    queryFn: WorkspaceService.listForUser,
  })
}

export function useWorkspaceDetailQuery(id: string | undefined) {
  return useQuery({
    queryKey: workspaceKeys.detail(id!),
    queryFn: () => WorkspaceService.getById(id!),
    enabled: !!id,  // Only fetch when ID exists
  })
}
```

---

## Page Pattern

```typescript
import useMultiLanguage from '@/hooks/useMultiLanguage';

export default function WorkspacesPage() {
  const { data, isLoading, isError, error } = useWorkspaceListQuery()
  const { COMMON, ERRORS } = useMultiLanguage()

  if (isLoading) return <WorkspacesSkeleton />
  if (isError) return <div className="text-destructive">{ERRORS?.FETCH_FAILED || error.message}</div>
  if (!data?.length) return <EmptyState message={COMMON?.NO_DATA} />

  return (
    <div className="grid gap-4">
      {data.map((item) => <WorkspaceCard key={item.id} workspace={item} />)}
    </div>
  )
}
```

---

## After Mutation: Show Skeleton While Refetching

```typescript
const { data, isLoading, isFetching } = useWorkspaceListQuery()
const createMutation = useCreateWorkspaceMutation()

// Show skeleton on initial load OR after successful mutation
if (isLoading || (createMutation.isSuccess && isFetching)) {
  return <WorkspacesSkeleton />
}
```
