# Folder Structure (Supabase frontend)

---

## Supabase module

```
apps/frontend/src/lib/supabase/
  supabaseClient.ts           — getSupabaseClient() singleton
  database-generated.types.ts — Supabase CLI output (regenerate only)
  database.types.ts           — MergeDeep + Tables* / Enums aliases
```

**Env and imports:** `SKILL.md` → *Project paths and env*.

---

## Data + UI layout (generic)

TanStack Query, services, and skeletons stay next to feature code — same placement whether the data source is PostgREST or another HTTP API.

```
apps/frontend/src/
  lib/
    query/
      queryClient.ts          — global QueryClient

  services/
    <domain>Service.ts        — static methods; Supabase chains + .throwOnError()

  hooks/<domain>/
    queryKeys.ts              — stable key factories (all, list, detail, …)
    use<Domain>Queries.ts
    use<Domain>Mutations.ts

  components/
    skeletons/
      <Domain>Skeleton.tsx    — mirrors final layout (see skeletons.md)
```

---

## Naming

| Kind | Convention | Example |
|------|------------|---------|
| Service | `<domain>Service.ts` | `projectService.ts` |
| Query keys file | `queryKeys.ts` | — |
| Query hook | `use<Plural>Query` / `use<Thing>Query` | `useProjectsQuery` |
| Mutation hook | `use<Action><Domain>Mutation` | `useDeleteProjectMutation` |
| Skeleton | `<Domain>Skeleton.tsx` | `ProjectsSkeleton.tsx` |

---

**New-domain file list:** see **`SKILL.md`** → **File checklist** (single source of truth).

---

## Imports (Supabase)

```typescript
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'
import type { Tables, TablesInsert, TablesUpdate } from '@/lib/supabase/database.types'
import { queryClient } from '@/lib/query/queryClient'
import { ButtonWithLoader, Skeleton, DeleteButton } from '@/components'
```
