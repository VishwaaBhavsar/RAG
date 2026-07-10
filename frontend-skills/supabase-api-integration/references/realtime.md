# Supabase Realtime

Subscribe only where live updates are worth the complexity. **Shared client:** `getSupabaseClient()` — never a second browser client.

**PostgREST** calls use **`SKILL.md`** error rules; realtime channels handle events separately — invalidate or **`setQueryData`** in callbacks.

---

## Conventions

- Subscriptions live in hooks/providers, not inlined in large page JSX.
- Name channels by domain + context (`projects:<workspaceId>`).
- **`removeChannel`** (or equivalent) in `useEffect` cleanup.

---

## Hook example

```typescript
import { useEffect } from 'react'
import { getSupabaseClient } from '@/lib/supabase/supabaseClient'
import { queryClient } from '@/lib/query/queryClient'
import { projectKeys } from './queryKeys'

export function useProjectsRealtime(workspaceId: string | undefined) {
  useEffect(() => {
    if (!workspaceId) return

    const supabase = getSupabaseClient()
    const channel = supabase
      .channel(`projects:${workspaceId}`)
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'projects',
          filter: `workspace_id=eq.${workspaceId}`,
        },
        () => {
          queryClient.invalidateQueries({ queryKey: projectKeys.list(workspaceId) })
        },
      )
      .subscribe()

    return () => {
      void supabase.removeChannel(channel)
    }
  }, [workspaceId])
}
```
