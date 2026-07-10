# Workflow (ordered)

**Hard rules:** `../SKILL.md`. **This file:** step order + minimal snippets. Skip steps already done for your app.

**Out:** PostgREST table queries (**supabase-api-integration**), Auth (**supabase-auth**), server-side SSR storage.

---

## Step map

| # | Deliverable |
|---|-------------|
| 1 | Env + bucket setup |
| 2 | Shared Supabase client (reuse if exists) |
| 3 | `storage.ts` service layer |
| 4 | `useSupabaseStorage.ts` hooks + `storageKeys` |
| 5 | RLS policies on bucket |
| 6 | UI — upload, list, URL display |
| 7 | Verify checklist |

---

## 1 — Env + Bucket setup

Required env vars:
```
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

**Bucket creation is handled by the agent via MCP** (`mcp__supabase__apply_migration`). Never instruct the user to use the dashboard. Generated frontend code must **never** call `createBucket` or any bucket management function.

### Create bucket (MCP)
```sql
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES ('avatars', 'avatars', false, 5242880, ARRAY['image/jpeg','image/png','image/webp'])
ON CONFLICT (id) DO NOTHING;
```

### Update bucket (MCP)
```sql
UPDATE storage.buckets
SET public = false, file_size_limit = 10485760,
    allowed_mime_types = ARRAY['image/jpeg','image/png','image/webp','image/gif']
WHERE id = 'avatars';
```

### Delete bucket (MCP)
```sql
DELETE FROM storage.objects WHERE bucket_id = 'avatars';
DELETE FROM storage.buckets WHERE id = 'avatars';
```

### Bucket config reference

| Field | Type | Notes |
|-------|------|-------|
| `public` | boolean | `true` → `getPublicUrl`; `false` → signed URLs required |
| `file_size_limit` | integer (bytes) | `5242880` = 5 MB, `10485760` = 10 MB |
| `allowed_mime_types` | text[] | `NULL` = allow all |

---

## 2 — Shared Supabase Client

Reuse `apps/frontend/src/lib/supabase/supabaseClient.ts` with `getSupabaseClient()`. If missing, implement it from **supabase-api-integration** `references/workflow.md` **Step 2** only (do not duplicate that `createClient` block in this skill). Storage uses the same client as PostgREST — no separate storage client.

---

## 3 — Service Layer (`storage.ts`)

Service layer: **`references/service-layer.md`** — copy **Imports + types**, follow **Contract** and the passthrough **table** (assemble each export), then paste **Non-passthrough** bodies as-is.

Key patterns: all functions accept `supabase: SupabaseClient` as first arg · all async return raw `{ data, error }` · `getPublicUrl` is synchronous · no bucket management functions.

---

## 4 — Hooks (`useSupabaseStorage.ts`)

Hooks file: **`references/hooks.md`** — copy **Imports + `storageKeys`**, follow **Hook shell**, then wire each export using **Per-hook** `queryKey` / `enabled` / `queryFn`, **mutations** `mutationFn` / `onSuccess`, and **`usePublicUrl`** sync body.

Key patterns: `storageKeys` factory covers all cache shapes · every `useQuery` has `enabled` guard · every mutation `onSuccess` invalidates relevant `storageKeys.*` · `usePublicUrl` is synchronous.

---

## 5 — RLS Policies

Complete policy SQL: **`references/rls-policies.md`**.

Minimum for authenticated user uploads:
```sql
CREATE POLICY "Users can upload own files" ON storage.objects FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users can read own files" ON storage.objects FOR SELECT TO authenticated
USING (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);
```

---

## 6 — UI Integration

### Upload
```tsx
'use client';
import { useUploadFile } from '@/hooks/useSupabaseStorage';

export function AvatarUpload({ userId }: { userId: string }) {
  const upload = useUploadFile('avatars');
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    upload.mutate({ path: `${userId}/${file.name}`, file,
      options: { contentType: file.type, cacheControl: '3600', upsert: true } });
  };
  return (
    <div>
      <input type="file" accept="image/*" onChange={handleChange} />
      {upload.isPending && <span>Uploading…</span>}
      {upload.isError && <span>{upload.error?.message}</span>}
    </div>
  );
}
```

### Public URL display
```tsx
'use client';
import { usePublicUrl } from '@/hooks/useSupabaseStorage';

export function Avatar({ userId, filename }: { userId: string; filename: string }) {
  const url = usePublicUrl('avatars', `${userId}/${filename}`, { width: 100, height: 100 });
  if (!url) return null;
  return <img src={url} alt="Avatar" width={100} height={100} />;
}
```

### Private bucket (Blob → Object URL)
`useDownloadFile` returns a `Blob`. Create/revoke the Object URL in `useEffect` — never inside `queryFn` (see `hooks.md` *Returns / notes*).

---

## 7 — Verify checklist

- [ ] No `.throwOnError()` on any storage call
- [ ] No bucket management functions in generated code
- [ ] `getSupabaseClient()` called in hooks only — never in service functions or components
- [ ] Every `useQuery` has `enabled` guard
- [ ] Every mutation `onSuccess` invalidates `storageKeys.*`
- [ ] `usePublicUrl` is synchronous (no `useQuery`)
- [ ] RLS policies set on bucket
- [ ] **Auth-protected buckets:** `!!session` added to query `enabled`; `mutate()` guarded with session check
- [ ] `contentType` + `cacheControl` set on uploads
- [ ] User-facing strings in translation keys
