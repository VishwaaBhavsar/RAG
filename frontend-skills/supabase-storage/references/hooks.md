# Hooks (`useSupabaseStorage.ts`)

Place at `apps/frontend/src/hooks/useSupabaseStorage.ts`.

**Rules:** Same mandatory patterns as `../SKILL.md` (no `.throwOnError()` on storage, explicit `if (error) throw error` in hooks, `enabled` guards incl. `!!session` for auth-scoped buckets). **Service:** `references/service-layer.md`. **Blob previews:** `useDownloadFile` returns a `Blob` — create/revoke Object URLs in `useEffect`, never in `queryFn`.

---

## Imports + `storageKeys` (copy-paste)

```typescript
export const storageKeys = {
  all: ['storage'] as const,
  files: (bucket: string, folder?: string, options?: ListOptions) =>
    ['storage', 'files', bucket, folder, options] as const,
  fileInfo: (bucket: string, path: string) => ['storage', 'info', bucket, path] as const,
  fileExists: (bucket: string, path: string) => ['storage', 'exists', bucket, path] as const,
  signedUrl: (bucket: string, path: string, expiresIn: number) =>
    ['storage', 'signedUrl', bucket, path, expiresIn] as const,
  signedUrls: (bucket: string, paths: string[], expiresIn: number) =>
    ['storage', 'signedUrls', bucket, paths, expiresIn] as const,
  download: (bucket: string, path: string) => ['storage', 'download', bucket, path] as const,
  downloadBase64: (bucket: string, path: string) =>
    ['storage', 'downloadBase64', bucket, path] as const,
};
```

---

## Hook shell (wrap every `queryFn` / `mutationFn` below)

**Queries** — inside each hook: `const supabase = getSupabaseClient();` then:

```typescript
return useQuery({
  queryKey: /* see per-hook table */,
  queryFn: async () => { /* see per-hook section */ },
  enabled: /* see per-hook table */,
  // useSignedUrl / useSignedUrls only:
  // staleTime: Math.max(0, expiresIn - 60) * 1000,
  // gcTime: expiresIn * 1000,
});
```

**Mutations** — inside each hook: `const supabase = getSupabaseClient();` `const queryClient = useQueryClient();` then:

```typescript
return useMutation({
  mutationFn: async /* vars */ => { /* see per-hook section */ },
  onSuccess: /* useUpdateFile differs; all others invalidate storageKeys.files(bucket) only */,
});
```

**Default mutation `onSuccess`** (upload, delete, move, copy):

```typescript
onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: storageKeys.files(bucket) });
},
```

**`usePublicUrl`** — no `useQuery`. Sync body only (see below).

---

## Per-hook: `queryKey`, `enabled`, and fn body

| Hook | `queryKey` | `enabled` |
|------|------------|-----------|
| `useListFiles(bucket, folder?, options?)` | `storageKeys.files(bucket, folder, options)` | `!!bucket` |
| `useFileInfo(bucket, path)` | `storageKeys.fileInfo(bucket, path)` | `!!bucket && !!path` |
| `useFileExists(bucket, path)` | `storageKeys.fileExists(bucket, path)` | `!!bucket && !!path` |
| `useSignedUrl(bucket, path, expiresIn, options?)` | `storageKeys.signedUrl(bucket, path, expiresIn)` | `!!bucket && !!path && expiresIn > 0` |
| `useSignedUrls(bucket, paths, expiresIn, options?)` | `storageKeys.signedUrls(bucket, paths, expiresIn)` | `!!bucket && paths.length > 0 && expiresIn > 0` |
| `useDownloadFile(bucket, path, transform?)` | `storageKeys.download(bucket, path)` | `!!bucket && !!path` |
| `useDownloadBase64(bucket, path)` | `storageKeys.downloadBase64(bucket, path)` | `!!bucket && !!path` |

### `queryFn` bodies

**`useListFiles`**

```typescript
async () => {
  const { data, error } = await listFiles(supabase, bucket, folder, options);
  if (error) throw error;
  return data;
}
```

**`useFileInfo`**

```typescript
async () => {
  const { data, error } = await getFileInfo(supabase, bucket, path);
  if (error) throw error;
  return data;
}
```

**`useFileExists`**

```typescript
async () => {
  const { exists, error } = await fileExists(supabase, bucket, path);
  if (error) throw error;
  return exists;
}
```

**`useSignedUrl`** — add `staleTime` / `gcTime` on `useQuery` (see shell).

```typescript
async () => {
  const { data, error } = await createSignedUrl(supabase, bucket, path, expiresIn, options);
  if (error) throw error;
  return data?.signedUrl ?? null;
}
```

**`useSignedUrls`** — add `staleTime` / `gcTime` on `useQuery` (see shell).

```typescript
async () => {
  const { data, error } = await createSignedUrls(supabase, bucket, paths, expiresIn, options);
  if (error) throw error;
  return data;
}
```

**`useDownloadFile`**

```typescript
async () => {
  const { data, error } = await downloadFile(supabase, bucket, path, transform);
  if (error) throw error;
  return data ?? null;
}
```

**`useDownloadBase64`**

```typescript
async () => {
  const { data, error } = await downloadAsBase64(supabase, bucket, path);
  if (error) throw error;
  return data;
}
```

**`usePublicUrl(bucket, path, transform?)`** — sync; **not** a `queryFn`:

```typescript
const supabase = getSupabaseClient();
if (!bucket || !path) return null;
return getPublicUrl(supabase, bucket, path, transform).data.publicUrl;
```

---

## Per-hook: mutations — `mutationFn` + `onSuccess`

Use **`useMutation` generics** where helpful, e.g. upload/update:

`useMutation<{ id: string; path: string; fullPath: string }, Error, { path: string; file: File | Blob | ArrayBuffer; options?: UploadOptions }>`

| Hook | Variables | `onSuccess` |
|------|-----------|-------------|
| `useUploadFile(bucket)` | `{ path, file, options? }` | default (`storageKeys.files(bucket)`) |
| `useUpdateFile(bucket)` | `{ path, file, options? }` | see below |
| `useDeleteFiles(bucket)` | `paths: string[]` | default |
| `useMoveFile(bucket)` | `{ from, to }` | default |
| `useCopyFile(bucket)` | `{ from, to }` | default |

**`useUploadFile` — `mutationFn`**

```typescript
async ({ path, file, options }) => {
  const { data, error } = await uploadFile(supabase, bucket, path, file, options);
  if (error) throw error;
  return data!;
}
```

**`useUpdateFile` — `mutationFn`**

```typescript
async ({ path, file, options }) => {
  const { data, error } = await updateFile(supabase, bucket, path, file, options);
  if (error) throw error;
  return data!;
}
```

**`useUpdateFile` — `onSuccess`** (replaces default)

```typescript
onSuccess: (_data, { path }) => {
  queryClient.invalidateQueries({ queryKey: storageKeys.files(bucket) });
  queryClient.invalidateQueries({ queryKey: storageKeys.fileInfo(bucket, path) });
  queryClient.invalidateQueries({ queryKey: storageKeys.download(bucket, path) });
  queryClient.invalidateQueries({ queryKey: storageKeys.downloadBase64(bucket, path) });
},
```

**`useDeleteFiles` — `mutationFn`**

```typescript
async (paths) => {
  const { data, error } = await removeFiles(supabase, bucket, paths);
  if (error) throw error;
  return data;
}
```

**`useMoveFile` — `mutationFn`**

```typescript
async ({ from, to }) => {
  const { data, error } = await moveFile(supabase, bucket, from, to);
  if (error) throw error;
  return data;
}
```

**`useCopyFile` — `mutationFn`**

```typescript
async ({ from, to }) => {
  const { data, error } = await copyFile(supabase, bucket, from, to);
  if (error) throw error;
  return data;
}
```

---

## Quick reference

| Hook | Kind | Returns / notes |
|------|------|-----------------|
| `useListFiles` | query | `.listV2` data |
| `useFileInfo` | query | metadata |
| `useFileExists` | query | `boolean` |
| `usePublicUrl` | sync | `string \| null` |
| `useSignedUrl` | query | signed URL \| null + URL TTL cache options |
| `useSignedUrls` | query | SDK array + URL TTL cache options |
| `useDownloadFile` | query | `Blob \| null` |
| `useDownloadBase64` | query | base64 string |
| `useUploadFile` | mutation | invalidates list |
| `useUpdateFile` | mutation | invalidates list + path-scoped queries |
| `useDeleteFiles` | mutation | invalidates list |
| `useMoveFile` | mutation | invalidates list |
| `useCopyFile` | mutation | invalidates list |
