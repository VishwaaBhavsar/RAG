# Postgres Changes — Full Reference

Listen to INSERT, UPDATE, DELETE on any Postgres table via Supabase Realtime.

**Typed channel events:** use `RealtimeListenTypes.PostgresChanges`, `PostgresChangeFilterEvent`, **`RealtimePostgresSchema`**, and **`RealtimePostgresTable`** from `@/lib/realtime-types` — definitions in **`patterns.md`** (Shared types). Avoid raw `'postgres_changes'` / `'INSERT'` / `'public'` / table name literals in app code.

## Table of Contents
1. [Subscribe to INSERT](#insert)
2. [Subscribe to UPDATE](#update)
3. [Subscribe to DELETE](#delete)
4. [Filter by column value](#filter)
5. [Multiple tables on one channel](#multi)
6. [React hook pattern](#react)
7. [RLS & security](#security)

---

## 1. INSERT {#insert}

**Use case:** New chat message, new order, new notification.

```ts
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'

supabase
  .channel('inserts')
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Insert,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Messages,
    },
    (payload) => {
      // payload.new = the newly inserted row
      setMessages((prev) => [...prev, payload.new as Message])
    }
  )
  .subscribe()
```

---

## 2. UPDATE {#update}

**Use case:** Order status changed, profile updated, collaborative field edit.

```ts
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'

supabase
  .channel('updates')
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Update,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Orders,
    },
    (payload) => {
      // payload.new = updated row, payload.old = previous row
      setOrders((prev) =>
        prev.map((o) => (o.id === payload.new.id ? payload.new : o))
      )
    }
  )
  .subscribe()
```

---

## 3. DELETE {#delete}

**Use case:** Deleted message, removed collaborator, expired session cleanup.

```ts
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'

supabase
  .channel('deletes')
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Delete,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Messages,
    },
    (payload) => {
      // payload.old = the deleted row (only id is guaranteed without REPLICA IDENTITY FULL)
      setMessages((prev) => prev.filter((m) => m.id !== payload.old.id))
    }
  )
  .subscribe()
```

> **Note:** To receive full old row data on DELETE, run:
> ```sql
> ALTER TABLE messages REPLICA IDENTITY FULL;
> ```
>
> **RLS + `DELETE`:** Postgres does not apply `SELECT` RLS to the deleted row when building `old`. With RLS enabled and `REPLICA IDENTITY FULL`, Realtime still sends **only primary key columns** in `payload.old` for deletes — plan UI/state updates accordingly (Postgres Changes — **Official documentation** — `../SKILL.md`).

---

## 4. Filter by column value {#filter}

Subscribe only to rows matching a condition — reduces noise and improves security.

```ts
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'

// Only listen to messages in room '123'
supabase
  .channel('room-123-messages')
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Insert,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Messages,
      filter: 'room_id=eq.123',
    },
    (payload) => setMessages((prev) => [...prev, payload.new])
  )
  .subscribe()
```

Supported filter operators: `eq`, `neq`, `lt`, `lte`, `gt`, `gte`, `in` (the **`in`** filter is capped at **100** values per Postgres Changes — **Official documentation** — `../SKILL.md`).

---

## 5. Multiple tables on one channel {#multi}

```ts
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'

supabase
  .channel('dashboard')
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Insert,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Orders,
    },
    handleOrder
  )
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Update,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Inventory,
    },
    handleStock
  )
  .on(
    RealtimeListenTypes.PostgresChanges,
    {
      event: PostgresChangeFilterEvent.Insert,
      schema: RealtimePostgresSchema.Public,
      table: RealtimePostgresTable.Alerts,
    },
    handleAlert
  )
  .subscribe()
```

---

## 6. React Hook Pattern {#react}

Add new tables to **`RealtimePostgresTable`** in `lib/realtime-types.ts` before using this hook with them.

```tsx
// hooks/useRealtimeTable.ts
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import {
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
} from '@/lib/realtime-types'
import { RealtimePostgresChangesPayload } from '@supabase/supabase-js'

export function useRealtimeTable<T extends { id: string }>(
  table: RealtimePostgresTable,
  initialData: T[] = []
) {
  const [rows, setRows] = useState<T[]>(initialData)

  useEffect(() => {
    const channel = supabase
      .channel(`realtime-${table}`)
      .on(
        RealtimeListenTypes.PostgresChanges,
        { event: PostgresChangeFilterEvent.All, schema: RealtimePostgresSchema.Public, table },
        (payload: RealtimePostgresChangesPayload<T>) => {
          if (payload.eventType === PostgresChangeFilterEvent.Insert) {
            setRows((prev) => [...prev, payload.new])
          } else if (payload.eventType === PostgresChangeFilterEvent.Update) {
            setRows((prev) =>
              prev.map((r) => (r.id === payload.new.id ? payload.new : r))
            )
          } else if (payload.eventType === PostgresChangeFilterEvent.Delete) {
            setRows((prev) => prev.filter((r) => r.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [table])

  return rows
}

// Usage
const messages = useRealtimeTable<Message>(RealtimePostgresTable.Messages, initialMessages)
```

---

## 7. RLS & Security {#security}

**Table RLS:** Realtime only delivers Postgres Changes for rows the subscriber role **may `SELECT`**. Add normal `SELECT` policies on the replicated table — no extra realtime-specific table policy.

```sql
CREATE POLICY "Users see own messages realtime"
  ON messages FOR SELECT
  USING ((SELECT auth.uid()) = user_id);
```

**Broadcast / Presence (private channels):** policies on **`realtime.messages`**, `realtime.topic()`, `extension` — see **`references/rls-patterns.md`** and Authorization (**Official documentation** — `../SKILL.md`).

**Important:** If a user cannot `SELECT` a row, they will not receive its change events.