# End-to-End Supabase Integration Workflow

**Contracts and mandatory rules:** `SKILL.md` only. Follow steps in order; skip steps already done for your app.

**Out of scope:** Supabase Auth. Anon-key client only — align **RLS** and policies.

**Architecture:** Service static methods wrap **`getSupabaseClient()`**; hooks use TanStack Query v5 and the **global** **`queryClient`**; UI uses skeletons, translated errors, and confirmed deletes per `references/*.md`.

---

## Step 1: Confirm Data Contract

- Table/view, columns, constraints.
- Who may read/write with the anon key (RLS / policies).
- UI shape — map `snake_case` columns to typed domain shapes when useful.

---

## Step 2: Shared Supabase Client

One lazy singleton at `apps/frontend/src/lib/supabase/supabaseClient.ts`. **Do not** add custom session/auth config here beyond `createClient(url, anonKey)` for this pattern.

```typescript
import { createClient, type SupabaseClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

let cachedClient: SupabaseClient<Database> | null = null

export function getSupabaseClient() {
  if (cachedClient) return cachedClient
  cachedClient = createClient<Database>(supabaseUrl, supabaseAnonKey)
  return cachedClient
}
```

### Edge Functions (Deno) {#edge-functions}

Use the **same** package everywhere: `import { createClient } from '@supabase/supabase-js'` (Supabase Edge Functions resolve it via the project lockfile).

**Anon key + caller JWT** (RLS as the signed-in user; forward the browser `Authorization` header):

```typescript
import { createClient } from '@supabase/supabase-js'

Deno.serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )
  // e.g. await supabase.auth.getUser()
})
```

Other skills should **link here** instead of duplicating `createClient` / import lines.

---

## Step 3: Generate and Compose Database Types

Required before services:

1. `npx supabase gen types typescript --project-id "$PROJECT_REF" --schema public > apps/frontend/src/lib/supabase/database-generated.types.ts`
2. `database.types.ts`: re-export `Json`; **`MergeDeep<DatabaseGenerated, { public: { Tables: …, Views?: … } }>`** — one exported `Database`; export `Tables`, `TablesInsert`, `TablesUpdate`, `Enums`.

| File | Role |
|------|------|
| `database-generated.types.ts` | CLI output |
| `database.types.ts` | `Json`, `Database`, helper aliases |
| `supabaseClient.ts` | `createClient<Database>(...)` only |

**MergeDeep**

- **a)** Override JSON/JSONB column types so selectors return typed objects instead of `Json`.
- **b)** Optional **`Views`** branch in the **same** `MergeDeep` to fix nullable PKs etc. on views.

```typescript
// database.types.ts
import { MergeDeep } from 'type-fest'
import { Database as DatabaseGenerated } from './database-generated.types'

export { Json } from './database-generated.types'

type ProjectSettingsJson = {
  notifications: { email: boolean; push: boolean }
  defaultView: 'list' | 'board'
}

export type Database = MergeDeep<
  DatabaseGenerated,
  {
    public: {
      Tables: {
        projects: {
          Row: { settings: ProjectSettingsJson | null }
          Insert: { settings?: ProjectSettingsJson | null }
          Update: { settings?: ProjectSettingsJson | null }
        }
      }
      Views: {
        projects_view: {
          Row: { id: number }
        }
      }
    }
  }
>

type PublicSchema = Database['public']
export type Tables<T extends keyof PublicSchema['Tables']> = PublicSchema['Tables'][T]['Row']
export type TablesInsert<T extends keyof PublicSchema['Tables']> = PublicSchema['Tables'][T]['Insert']
export type TablesUpdate<T extends keyof PublicSchema['Tables']> = PublicSchema['Tables'][T]['Update']
export type Enums<T extends keyof PublicSchema['Enums']> = PublicSchema['Enums'][T]
```

**Selectors:** **`->`** = typed JSON; **`->>** = string only.

---

## Step 3b: Typing Joins and Nested Selects (`QueryData` / `QueryResult` / `QueryError` / `overrideTypes`)

Derive types from the **unawaited** builder — avoid hand-written nested PostgREST interfaces.

```typescript
import { QueryData } from '@supabase/supabase-js'
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'

const countriesWithCitiesQuery = getSupabaseClient()
  .from('countries')
  .select('id, name, cities(id, name)')

type CountriesWithCities = QueryData<typeof countriesWithCitiesQuery>

const { data } = await countriesWithCitiesQuery.throwOnError()
const result = data as CountriesWithCities
```

Use **`QueryResult`** on the **Promise-returning chain** (the value you **`await`**, including `.throwOnError()`), when you need the full resolved **`{ data, error }`** shape. Use **`QueryError`** for **`PostgrestError`** (e.g. **`catch`** after reject, or **`error`** from **`{ data, error }`** when not using `.throwOnError()`). Most list/detail UI only needs **`QueryData`**.

```typescript
import type { QueryResult, QueryError } from '@supabase/supabase-js'
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'

const projectsPromise = getSupabaseClient()
  .from('projects')
  .select('id, name')
  .throwOnError()

type ProjectsResolved = QueryResult<typeof projectsPromise>

async function logProjects(): Promise<void> {
  const res: ProjectsResolved = await projectsPromise
  void res.data
  void res.error
}

function logRejectedPostgrest(err: unknown) {
  if (err && typeof err === 'object' && 'message' in err) {
    console.error((err as QueryError).message)
  }
}
```

**One-off type tweaks** without editing `database.types.ts`:

```typescript
const { data } = await getSupabaseClient()
  .from('projects')
  .select()
  .overrideTypes<Array<{ id: string }>>()
  .throwOnError()

const { data: row } = await getSupabaseClient()
  .from('projects')
  .select()
  .single()
  .overrideTypes<{ id: string }>()
  .throwOnError()
```

---

## Step 4: Service Methods

Use `getSupabaseClient()` for all data access. **Return shapes and `.throwOnError()` rules:** `SKILL.md` → *Mandatory patterns*.

Minimal list/read pattern (one method per domain is enough to anchor the rest):

```typescript
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'

export class ProjectService {
  static async listByWorkspace(workspaceId: string) {
    const { data } = await getSupabaseClient()
      .from('projects')
      .select('id, name')
      .eq('workspace_id', workspaceId)
      .throwOnError()
    return data
  }
}
```

**CREATE / UPDATE** (insert/update chains, `.select()` before `.single()`, cache-aware mutations): **`references/mutation-with-loader.md`**. **DELETE** (no `.select()` on chain, return `{ id }`, `DeleteButton`): **`references/delete-with-confirmation.md`**.

**RPC / Storage:** manual `if (error) throw` when `.throwOnError()` is not on the chain (`SKILL.md`).

---

## Step 5: Query Keys

Stable factories: **`all`**, scoped **`list`**, **`detail`**, plus any filters the UI caches.

```typescript
export const projectKeys = {
  all: ['projects'] as const,
  list: (workspaceId: string) => [...projectKeys.all, 'list', workspaceId] as const,
  detail: (id: string) => [...projectKeys.all, 'detail', id] as const,
} as const
```

Rules:

- Arrays are readonly tuples; include serializable params in order.
- **`all`** is the broad prefix for invalidating every project query.
- Add segments (e.g. `'infinite'`, filter hashes) only when the screen needs distinct cache rows.

---

## Step 6: Hooks

Global `queryClient` from `@/lib/query/queryClient`. **Mutation generics, `useMutation`, `invalidateQueries` / `setQueryData`, ButtonWithLoader, toasts:** **`references/mutation-with-loader.md`**.

Query hooks: **`enabled`** when the key depends on optional route params or IDs; **`queryFn`** calls the service only.

```typescript
export function useProjectsQuery(workspaceId: string | undefined) {
  return useQuery({
    queryKey: workspaceId ? projectKeys.list(workspaceId) : projectKeys.all,
    queryFn: () => ProjectService.listByWorkspace(workspaceId!),
    enabled: !!workspaceId,
  })
}
```

Prefer **`queryClient`** from the module singleton; use **`useQueryClient()`** only when scope must follow a custom provider.

Optional **`onError`** in hooks sparingly — usually handle user-visible errors in components with **`useEffect`** so you can **`reset()`** the mutation (`mutation-with-loader.md`).

---

## Step 7: UI States

Loading → **`references/skeletons.md`**. Error → translated UX. Empty → dedicated empty state. Thin handlers — **`get-with-skeleton.md`**.

---

## Step 8: Optional Realtime

See **`realtime.md`** — invalidate or patch cache in handlers; unsubscribe on cleanup.

---

## Verification checklist

- [ ] `SKILL.md` mandatory patterns satisfied (especially `.throwOnError()` on all `.from()` chains)
- [ ] Types: one `MergeDeep` `Database`, `QueryData` / `overrideTypes` where joins need typing; `QueryResult` / `QueryError` only if needed (Step 3b)
- [ ] Keys stable; hooks use global `queryClient`
- [ ] Skeleton, error, empty, i18n
- [ ] Realtime unsubscribed if used
