# RLS Policies for Supabase Storage

Storage uses `storage.objects` and `storage.buckets` tables for RLS. RLS is enabled by default on new buckets.

**Bucket SQL (create/update/delete): see `workflow.md` Step 1.**

**Key functions:**

| Function | Returns |
|----------|---------|
| `storage.foldername(name)` | Array of path segments — `[1]` = first folder |
| `storage.filename(name)` | Filename without folders |
| `auth.uid()` | Current authenticated user's UUID |
| `auth.role()` | `'anon'` or `'authenticated'` |

**Browser client:** `getSupabaseClient()` / lazy `createClient(url, anonKey)` for the anon key lives only in **supabase-api-integration** `references/workflow.md` **Step 2**. Do not paste that singleton here.

---

## Pattern 1 — Authenticated owner (private bucket)

Path convention: `${user.id}/${filename}` — enforce at app layer too.

```sql
CREATE POLICY "Users upload own files" ON storage.objects FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users read own files" ON storage.objects FOR SELECT TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users update own files" ON storage.objects FOR UPDATE TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text)
WITH CHECK (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);

CREATE POLICY "Users delete own files" ON storage.objects FOR DELETE TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);
```

---

## Pattern 2 — Public bucket (read-only by anon)

```sql
CREATE POLICY "Public read access" ON storage.objects FOR SELECT TO anon, authenticated
USING (bucket_id = 'public-assets');

CREATE POLICY "Authenticated upload only" ON storage.objects FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'public-assets');
```

Or: set `public: true` on the bucket to bypass RLS for SELECT — still add INSERT/DELETE policies to restrict writes.

---

## Pattern 3 — Shared team folder (workspace-scoped)

Path convention: `{workspace_id}/{filename}`

```sql
CREATE POLICY "Workspace members can upload" ON storage.objects FOR INSERT TO authenticated
WITH CHECK (
  bucket_id = 'workspace-files'
  AND EXISTS (
    SELECT 1 FROM workspace_members
    WHERE workspace_id = (storage.foldername(name))[1]::uuid AND user_id = auth.uid()
  )
);

CREATE POLICY "Workspace members can read" ON storage.objects FOR SELECT TO authenticated
USING (
  bucket_id = 'workspace-files'
  AND EXISTS (
    SELECT 1 FROM workspace_members
    WHERE workspace_id = (storage.foldername(name))[1]::uuid AND user_id = auth.uid()
  )
);

CREATE POLICY "Workspace members can delete" ON storage.objects FOR DELETE TO authenticated
USING (
  bucket_id = 'workspace-files'
  AND EXISTS (
    SELECT 1 FROM workspace_members
    WHERE workspace_id = (storage.foldername(name))[1]::uuid AND user_id = auth.uid()
  )
);
```

---

## Signed upload URL pattern (secure client upload)

Use when you want server-side validation before allowing upload.

**Browser / anon client** — After the API returns `{ path, token }`, call `uploadToSignedUrl` with the same **`getSupabaseClient()`** from **supabase-api-integration** `references/workflow.md` **Step 2** (lazy singleton + `createClient<Database>(url, anonKey)` — see that file’s code block; do not duplicate it here).

**Server-only admin client** — `createSignedUploadUrl` must use the **service role** key, not the anon key from Step 2. Add `apps/frontend/src/lib/supabase/supabaseAdmin.ts`: mirror the **lazy singleton** in **supabase-api-integration** `references/workflow.md` **Step 2** (same `createClient` / cache pattern as that code block), but pass `process.env.SUPABASE_SERVICE_ROLE_KEY` as the second argument instead of `NEXT_PUBLIC_SUPABASE_ANON_KEY`. **Never** import this module from `'use client'`.

```typescript
// app/api/upload-token/route.ts
import { supabaseAdmin } from '@/lib/supabase/supabaseAdmin';

export async function POST(req: Request) {
  const { userId, filename } = await req.json();
  const { data, error } = await supabaseAdmin.storage
    .from('private-uploads')
    .createSignedUploadUrl(`${userId}/${filename}`, { upsert: false });
  if (error) return Response.json({ error: error.message }, { status: 500 });
  return Response.json({ path: data.path, token: data.token });
}

// Client: fetch token then uploadToSignedUrl(getSupabaseClient(), bucket, path, token, file)
```

---

## Checklist

- [ ] RLS enabled on bucket (default for new buckets)
- [ ] INSERT policy restricts uploads to user's own folder
- [ ] SELECT policy restricts reads to user's own files (or public policy if open)
- [ ] DELETE policy restricts deletes to user's own files
- [ ] UPDATE policy if using `updateFile` / overwrite
- [ ] Path convention enforced in app layer (`${user.id}/${filename}`)
- [ ] Bucket `public` flag matches intended visibility
- [ ] `fileSizeLimit` + `allowedMimeTypes` set in bucket config
