# End-to-End API Integration Workflow (All Steps Required)

Step-by-step guide for integrating any new API endpoint.

---

## Step 1: Find Endpoint in Generated Types

```bash
grep -n "projects\." libs/types/src/lib/client/index.ts
```

Identify: method signature, request body type, response type.

---

## Step 2: Add Service Method

```typescript
// apps/frontend/src/services/projectService.ts
import { apiClient } from '@/lib/axios/apiClient'
import type { ProjectResponse } from '@backend/types/client'

export class ProjectService {
  static async list(): Promise<ProjectResponse[]> {
    return (await apiClient.projects.list()).data
  }

  static async getById(id: string) {
    return (await apiClient.projects.getById(id)).data
  }

  static async create(body: CreateProjectBody) {
    return (await apiClient.projects.create(body)).data
  }

  static async delete(id: string) {
    return (await apiClient.projects.delete(id)).data
  }
}
```

---

## Step 3: Define Query Keys

```typescript
// apps/frontend/src/hooks/project/queryKeys.ts
export const projectKeys = {
  all: ['projects'] as const,
  list: () => [...projectKeys.all, 'list'] as const,
  detail: (id: string) => [...projectKeys.all, 'detail', id] as const,
} as const
```

---

## Step 4: Create Hooks

**Queries (GET):**
```typescript
// apps/frontend/src/hooks/project/useProjectQueries.ts
export function useProjectsQuery() {
  return useQuery({
    queryKey: projectKeys.list(),
    queryFn: ProjectService.list,
  })
}
```

**Mutations (POST/PUT/DELETE):**
```typescript
// apps/frontend/src/hooks/project/useProjectMutations.ts
import { queryClient } from '@/lib/query/queryClient'
import { showSuccessToast, showErrorToast } from '@/lib/toast'

export function useCreateProjectMutation() {
  return useMutation({
    mutationFn: ProjectService.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: projectKeys.list() })
      queryClient.setQueryData(projectKeys.detail(data.id), data)
      // Only show toast if user explicitly requests success message
    },
    onError: (error) => {
      showErrorToast(error.message || 'Failed to create project')
    },
  })
}
```

---

## Step 5: Create Skeleton

```typescript
// apps/frontend/src/components/skeletons/ProjectsSkeleton.tsx
export function ProjectsSkeleton() {
  return (
    <div className="grid gap-4">
      {[1, 2, 3].map((i) => (
    <Card key={i}>
    <Skeleton className="h-5 w-2/3" />
    <Skeleton className="h-4 w-1/3" />
      </Card>
  ))}
  </div>
)
}
```

---

## Step 6: Add Translations (REQUIRED)

**All static text must use `useMultiLanguage` hook.** Use the `translation` skill to add new keys.

```typescript
// In your page/component
import useMultiLanguage from '@/hooks/useMultiLanguage'

const { BUTTONS, MESSAGES, LABELS } = useMultiLanguage()

// Use translation keys instead of hardcoded strings:
<ButtonWithLoader isLoading={isPending} loadingText={BUTTONS.SAVING}>
  {BUTTONS.SAVE}
  </ButtonWithLoader>

  <h1>{LABELS.WORKSPACES}</h1>
  <p>{MESSAGES.NO_WORKSPACES}</p>
```

Common keys to add for a new feature:
- Page title / section headers
- Button labels (Save, Cancel, Delete, Create, etc.)
- Empty states, error messages
- Form labels and placeholders
- Toast messages

---

## Step 7: Wire Up in Page

```typescript
import useMultiLanguage from '@/hooks/useMultiLanguage'
import { showSuccessToast, showErrorToast } from '@/lib/toast'

export default function ProjectsPage() {
  const { data, isLoading, isError } = useProjectsQuery()
  const { LABELS, MESSAGES } = useMultiLanguage()
  const createProject = useCreateProjectMutation()

  const handleCreate = async () => {
    try {
      const newProject = await createProject.mutateAsync({ name: 'New Project' })
      showSuccessToast(MESSAGES.PROJECT_CREATED)
    } catch (error) {
      // Error toast shown in mutation hook
    }
  }

  if (isLoading) return <ProjectsSkeleton />
  if (isError) return <p>{MESSAGES.LOAD_ERROR}</p>
  if (!data?.length) return <p>{MESSAGES.NO_PROJECTS}</p>

  return (
    <>
      <h1>{LABELS.PROJECTS}</h1>
  {data.map((p) => <ProjectCard key={p.id} project={p} />)}
  </>
  )
  }
```

---

## Checklist

- [ ] Grep types file for endpoint
- [ ] Add service method
- [ ] Add query keys
- [ ] Add query/mutation hook
- [ ] Create skeleton
- [ ] **Add translations via `translation` skill**
- [ ] Wire up in page with `useMultiLanguage`
