# Service Layer (`storage.ts`)

Place at `apps/frontend/src/lib/supabase/storage.ts`. **Hooks:** `references/hooks.md`.

---

## Imports + types (copy-paste)

```typescript
import type { SupabaseClient } from '@supabase/supabase-js';
import type { TransformOptions } from '@supabase/storage-js';

export type { TransformOptions };

export interface UploadOptions {
  cacheControl?: string; // default '3600'
  upsert?: boolean; // updateFile forces true
  contentType?: string; // set explicitly for non-standard MIME types
}

export interface ListOptions {
  limit?: number;
  offset?: number;
  sortBy?: { column: string; order: 'asc' | 'desc' };
  search?: string;
}

export interface SignedUrlOptions {
  download?: boolean | string;
  transform?: TransformOptions;
}
```

---

## Contract (every function)

- **First argument** is always `supabase: SupabaseClient` — hooks obtain it via `getSupabaseClient()`; **never** call `getSupabaseClient()` inside this module.
- **Returns:** pass through the SDK’s `{ data, error }` **without throwing** (except where noted below `fileExists` wraps `exists`).
- **No bucket management** in app code (create/delete bucket — agent/MCP only).

**Passthrough shell** — most exports are one line after `from(bucket)`:

```typescript
export async function example(
  supabase: SupabaseClient,
  bucket: string /* …other params */,
) {
  return supabase.storage.from(bucket)/* chain from table below */;
}
```

**Sync exception:** `getPublicUrl` — not `async`, returns SDK return value directly.

---

## Passthrough functions — signature + `from(bucket)` chain

Use **`supabase.storage.from(bucket)`** then the chain in the last column.

| Export | Parameters after `supabase`, `bucket` | Chain |
|--------|----------------------------------------|-------|
| `uploadFile` | `path`, `file`, `options?` | `.upload(path, file, options)` |
| `createSignedUploadUrl` | `path`, `upsert = false` | `.createSignedUploadUrl(path, { upsert })` |
| `uploadToSignedUrl` | `path`, `token`, `file`, `options?` (`Pick<UploadOptions,'contentType'>`) | `.uploadToSignedUrl(path, token, file, options)` |
| `createSignedUrl` | `path`, `expiresIn`, `options?` | `.createSignedUrl(path, expiresIn, options)` |
| `createSignedUrls` | `paths`, `expiresIn`, `options?` | `.createSignedUrls(paths, expiresIn, options)` |
| `removeFiles` | `paths` | `.remove(paths)` |
| `listFiles` | `folder?`, `options?` | `.listV2(folder, options)` |
| `moveFile` | `fromPath`, `toPath` | `.move(fromPath, toPath)` |
| `copyFile` | `fromPath`, `toPath` | `.copy(fromPath, toPath)` |
| `getFileInfo` | `path` | `.info(path)` |

Example assembled export:

```typescript
export async function listFiles(
  supabase: SupabaseClient,
  bucket: string,
  folder?: string,
  options?: ListOptions,
) {
  return supabase.storage.from(bucket).listV2(folder, options);
}
```

---

## Non-passthrough — copy these bodies exactly

**`updateFile`** — forces `upsert: true`:

```typescript
export async function updateFile(
  supabase: SupabaseClient,
  bucket: string,
  path: string,
  file: File | Blob | ArrayBuffer,
  options?: UploadOptions,
) {
  return supabase.storage.from(bucket).update(path, file, { ...options, upsert: true });
}
```

**`getPublicUrl`** — synchronous; optional image transform:

```typescript
export function getPublicUrl(
  supabase: SupabaseClient,
  bucket: string,
  path: string,
  transform?: TransformOptions,
) {
  return supabase.storage.from(bucket).getPublicUrl(
    path,
    transform ? { transform } : undefined,
  );
}
```

**`downloadFile`** — optional transform:

```typescript
export async function downloadFile(
  supabase: SupabaseClient,
  bucket: string,
  path: string,
  transform?: TransformOptions,
) {
  return supabase.storage.from(bucket).download(
    path,
    transform ? { transform } : undefined,
  );
}
```

**`downloadAsBase64`** — uses SDK `.toBase64()` (browser/Node); do not use FileReader-based conversion:

```typescript
export async function downloadAsBase64(
  supabase: SupabaseClient,
  bucket: string,
  path: string,
) {
  return supabase.storage.from(bucket).toBase64(path);
}
```

**`fileExists`** — normalizes `exists`; surfaces SDK `error`:

```typescript
export async function fileExists(
  supabase: SupabaseClient,
  bucket: string,
  path: string,
): Promise<{ exists: boolean; error: unknown }> {
  const { data, error } = await supabase.storage.from(bucket).exists(path);
  return { exists: data === true, error };
}
```

---

## When to use which check

| Method | Use when |
|--------|----------|
| `fileExists(supabase, bucket, path)` | Boolean check only — no download |
| `getFileInfo(supabase, bucket, path)` | Need metadata (size, MIME, created_at) |
| `listFiles(supabase, bucket, folder)` | Browse folder contents with pagination |

**Do not** use `.download()` to check existence — it downloads the full file unnecessarily.
