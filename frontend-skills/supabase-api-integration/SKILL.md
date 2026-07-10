---
name: supabase-api-integration
description: Integrates frontend features with Supabase PostgREST and Realtime via @supabase/supabase-js, TanStack Query v5, and shared service static methods. Use this skill when adding any Supabase table query, mutation, or realtime listener — not Supabase Auth. Storage uploads/downloads use the same client with manual error checks (see SKILL.md Storage). Covers service layer, query key factories, global queryClient, skeletons, confirmations, and mandatory .throwOnError() on PostgREST builder chains where available.
---

# Supabase API Integration

Thin **service** wrappers call `getSupabaseClient()`; hooks use TanStack Query; the data layer is Supabase instead of a hand-rolled HTTP client.

**Read this file first for every rule.** Use `references/workflow.md` for the ordered implementation path; use other `references/` files only for task-specific snippets (SELECT, mutations, DELETE, realtime, folder tree, skeletons).

---

## References

| File | Use when |
|------|----------|
| `references/workflow.md` | Ordered steps (types, MergeDeep, `QueryData` / `QueryResult` / `QueryError`, services, keys, hooks, checklist) |
| `references/get-with-skeleton.md` | SELECT queries, loading/error/empty UI |
| `references/mutation-with-loader.md` | INSERT/UPDATE service + mutation hooks, ButtonWithLoader, toasts, dialogs |
| `references/delete-with-confirmation.md` | DELETE service shape, DeleteButton, cache invalidation |
| `references/realtime.md` | `postgres_changes` subscriptions |
| `references/folder-structure.md` | `lib/supabase/` + services/hooks/skeletons layout |
| `references/skeletons.md` | Card, table, detail skeleton patterns |

Storage bucket calls: **SKILL.md** → *Storage (buckets)* (same skill; no separate reference file).

**Shared UI primitives** (`ButtonWithLoader`, `DeleteButton`, `Skeleton`, `AlertDialog`): **components** skill and `references/mutation-with-loader.md` / `references/delete-with-confirmation.md`.

---

## Key components (import from `@/components`)

| Component | Use for |
|-----------|---------|
| `ButtonWithLoader` | Mutations: `isLoading` + `loadingText` |
| `Skeleton` | Placeholders inside domain skeletons |
| `DeleteButton` | Standard destructive action with confirmation |
| `AlertDialog` | Custom destructive confirmation flows |

---

## Project paths and env

| What | Where |
|------|--------|
| Client factory | `apps/frontend/src/lib/supabase/supabaseClient.ts` → `getSupabaseClient()` |
| Generated schema types | `apps/frontend/src/lib/supabase/database-generated.types.ts` (regenerate via CLI; do not hand-edit) |
| Overrides + aliases | `apps/frontend/src/lib/supabase/database.types.ts` (`MergeDeep`, `Tables`, `TablesInsert`, `TablesUpdate`, `Enums`) |
| Global query client | `apps/frontend/src/lib/query/queryClient.ts` |
| Toasts | `apps/frontend/src/lib/toast` |
| Env (browser) | `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` — never expose service-role keys |

`services/`, `hooks/<domain>/`, and `components/skeletons/`: **`references/folder-structure.md`**.

Import: `@/lib/supabase/supabaseClient`, `@/lib/supabase/database.types`.

Join and nested-select typing: **`QueryData`** (see workflow Step 3b). **`QueryResult`** / **`QueryError`** — only when you need explicit types for PostgREST result or error payloads (workflow Step 3b).

---

## Mandatory patterns (single source)

### PostgREST errors

On every **`.from()`** chain (and any builder that exposes it), append **`.throwOnError()`** as the **last** call **before `await`**, so failed responses **reject** instead of `{ error }` on success path. Do not pair that chain with redundant `const { error } = …` checks.

**RPC**, **Storage**, or APIs **without** `.throwOnError()` — use `const { data, error } = await …` and **`if (error) throw error`** (or normalize to `Error`).

Typed mutations: **`useMutation<ResponseType, Error, VariablesType>(...)`**.

Never swallow Supabase errors in services for flows the UI must reflect.

### Storage (buckets)

Use **`getSupabaseClient().storage`** in services (not in components). The Storage API does **not** use the same `.from().throwOnError()` chain as PostgREST — use **`const { data, error } = await …`** and **`if (error) throw error`**. Example: `storage.from(bucket).upload(path, file)` / `download(path)` / `remove([path])`; align bucket policies with the anon key.

### Row multiplicity

| Method | Use when |
|--------|----------|
| `.single()` | Exactly one row required; errors on 0 or many rows |
| `.maybeSingle()` | At most one row; `null` data for 0 rows; still use `.throwOnError()` for transport/RLS failures |

### Service return contract (PostgREST)

| Operation | Chain ends with | Return |
|-----------|-----------------|--------|
| List | `.select(...).throwOnError()` | Typed array (normalize `null` to `[]` if needed) |
| Detail | `.select(...).eq(...).single().throwOnError()` | One row |
| CREATE | `.insert(...).select(...).single().throwOnError()` | Created row — **`.select(...)` before `.single()`** or `data` is `null` |
| UPDATE | `.update(...).eq(...).select(...).single().throwOnError()` | Updated row only; select only needed columns |
| DELETE | `.delete().eq(...).throwOnError()` — **no `.select()`** | `{ id }` for callers to invalidate caches |

### Layering and queries

- Do not run `getSupabaseClient()` or `.from()` in components; **`queryFn` / `mutationFn` call service static methods only**.
- Use **`enabled`** when the key depends on optional route params or IDs.
- Keep **`.select(...)`** minimal for payload size and tighter types.

### Hooks and cache

- Import the **global** `queryClient` from `@/lib/query/queryClient` in hook modules unless a scoped provider forces `useQueryClient()`.
- On success: **`invalidateQueries`**, **`setQueryData`** for detail caches, **`removeQueries`** when deleting (`delete-with-confirmation.md`).

### Types

- **`strictNullChecks: true`** for `MergeDeep` correctness.
- JSON column shapes and view nullability: one exported `Database` via **`MergeDeep`** (see workflow Step 3).
- **`->`** for typed JSON projection; **`->>`** is always string — do not use `->>` when you need a typed object.
- Joins / nested selects: derive types with **`QueryData<typeof query>`** on the **unawaited** builder (workflow Step 3b). For one-off fixes without editing `database.types.ts`, use **`.overrideTypes<T>()`** (still end with `.throwOnError()` when on a PostgREST chain).

### i18n

All user-visible strings: **`useMultiLanguage`** (**translation** skill). PostgREST errors are often English; map to **`MESSAGES.*`** at the UI.

---

## File checklist

**Once per app**

- [ ] `apps/frontend/src/lib/supabase/` with `supabaseClient.ts`, `database-generated.types.ts`, `database.types.ts`
- [ ] `getSupabaseClient()` + `createClient<Database>`

**New domain**

- [ ] `services/<domain>Service.ts`
- [ ] `hooks/<domain>/queryKeys.ts`
- [ ] `hooks/<domain>/use<Domain>Queries.ts` / `use<Domain>Mutations.ts`
- [ ] `components/skeletons/<Domain>Skeleton.tsx`
- [ ] Translations per **translation** skill

**Extend existing domain**

- [ ] Service methods — every `.from()` path ends with `.throwOnError()` (or explicit throw for non-builder APIs)
- [ ] Keys and hooks wired to global `queryClient`
