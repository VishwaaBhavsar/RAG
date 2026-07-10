# Folder Structure

Where API-related files belong.

---

## Structure

```
libs/types/src/lib/client/
  index.ts                    ← Generated types (READ ONLY)

apps/frontend/src/
  lib/
    axios/
      apiClient.ts            ← Api instance + interceptors
    query/
      queryClient.ts          ← QueryClient config

  services/
    <domain>Service.ts        ← API wrapper methods

  hooks/<domain>/
    queryKeys.ts              ← Query key factory
    use<Domain>Queries.ts     ← useQuery hooks
    use<Domain>Mutations.ts   ← useMutation hooks

  components/
    ui/
      ButtonWithLoader.tsx    ← Button with loading state
      Skeleton.tsx            ← Skeleton primitive
      AlertDialog.tsx         ← Confirmation dialog
    skeletons/
      <Domain>Skeleton.tsx    ← Domain-specific skeletons
```

---

## Naming

| Type | Convention | Example |
|------|-----------|---------|
| Service | `<domain>Service.ts` | `workspaceService.ts` |
| Query keys | `queryKeys.ts` | - |
| Query hook | `use<Domain>Query` | `useWorkspaceQuery` |
| Mutation hook | `use<Action><Domain>Mutation` | `useDeleteWorkspaceMutation` |
| Skeleton | `<Domain>Skeleton.tsx` | `WorkspacesSkeleton.tsx` |

---

## Checklist: New Domain

- [ ] `services/<domain>Service.ts`
- [ ] `hooks/<domain>/queryKeys.ts`
- [ ] `hooks/<domain>/use<Domain>Queries.ts`
- [ ] `hooks/<domain>/use<Domain>Mutations.ts`
- [ ] `components/skeletons/<Domain>Skeleton.tsx`

---

## Imports

```typescript
// Types from generated file
import type { WorkspaceResponse } from '@backend/types/client'

// Internal
import { apiClient } from '@/lib/axios/apiClient'
import { ButtonWithLoader, Skeleton } from '@/components'
```
