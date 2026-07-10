# Folder Structure (Supabase Storage)

---

## Storage module files

```
apps/frontend/src/
  lib/
    supabase/
      supabaseClient.ts           — shared getSupabaseClient() singleton (reuse existing)
      storage.ts                  — all storage service functions (named exports)

  hooks/
    useSupabaseStorage.ts         — storageKeys + all useQuery/useMutation hooks
```

Two files only. No class, no separate folder per domain.

---

## Naming

| Kind | Convention | Example |
|------|------------|---------|
| Service file | `storage.ts` | — |
| Service functions | camelCase verbs | `uploadFile`, `listFiles`, `getPublicUrl` |
| Hooks file | `useSupabaseStorage.ts` | — |
| Query hooks | `use<Action><Noun>` | `useListFiles`, `useSignedUrl`, `useDownloadFile` |
| Mutation hooks | `use<Action><Noun>` | `useUploadFile`, `useDeleteFiles`, `useMoveFile` |
| Query keys | `storageKeys` object | `storageKeys.files(bucket, folder)` |

---

## Imports

```typescript
// In hooks file
import { getSupabaseClient } from '@/lib/supabase/supabaseClient';
import {
  uploadFile,
  listFiles,
  getPublicUrl,
  type UploadOptions,
  type ListOptions,
} from '@/lib/supabase/storage';

// In components
import {
  useUploadFile,
  useListFiles,
  usePublicUrl,
  useDeleteFiles,
} from '@/hooks/useSupabaseStorage';
```

---

## What does NOT go in storage.ts

- No `getSupabaseClient()` calls — client is injected as a parameter.
- No React hooks.
- No TanStack Query imports.
- No cache invalidation logic.

## What does NOT go in useSupabaseStorage.ts

- No direct `supabase.storage.*` calls — delegate to service functions.
- No JSX.
- No business logic — hooks are thin wrappers around services + TanStack Query.

---

## Relationship to supabase-api-integration

| Concern | File | Skill |
|---------|------|-------|
| Table queries, inserts, updates | `services/<domain>Service.ts` | supabase-api-integration |
| Storage uploads, downloads, URLs | `lib/supabase/storage.ts` | supabase-storage (this) |
| Both share | `lib/supabase/supabaseClient.ts` | Either — create once |
