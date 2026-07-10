# Realtime Patterns — React, Next.js (client-only)

RLS / private channels: **`references/rls-patterns.md`**.

## Shared types

Colocate in e.g. `lib/realtime-types.ts`.

```ts
export type Message = { id: string; room_id: string; created_at: string; body?: string }

/** `.subscribe((status) => …)` string literals */
export enum ChannelStatus {
  Connecting = 'CONNECTING',
  Subscribed = 'SUBSCRIBED',
  ChannelError = 'CHANNEL_ERROR',
  TimedOut = 'TIMED_OUT',
  Closed = 'CLOSED',
}

/** First argument to `channel.on()` */
export enum RealtimeListenTypes {
  PostgresChanges = 'postgres_changes',
  Broadcast = 'broadcast',
  Presence = 'presence',
}

/** `postgres_changes` subscription `filter.event` */
export enum PostgresChangeFilterEvent {
  Insert = 'INSERT',
  Update = 'UPDATE',
  Delete = 'DELETE',
  All = '*',
}

/** Postgres schema for `postgres_changes` filter — extend for replicated tables outside `public` */
export enum RealtimePostgresSchema {
  Public = 'public',
}

/** Replicated tables referenced in this project’s Realtime snippets — extend with your app tables */
export enum RealtimePostgresTable {
  Messages = 'messages',
  Orders = 'orders',
  Inventory = 'inventory',
  Alerts = 'alerts',
  Documents = 'documents',
}

/** `presence` subscription `filter.event` */
export enum PresenceListenEvent {
  Sync = 'sync',
  Join = 'join',
  Leave = 'leave',
}

export const CHANNEL_STATUS_BADGE: Record<ChannelStatus, string> = {
  [ChannelStatus.Subscribed]: 'bg-green-500',
  [ChannelStatus.Connecting]: 'bg-yellow-500',
  [ChannelStatus.ChannelError]: 'bg-red-500',
  [ChannelStatus.TimedOut]: 'bg-orange-500',
  [ChannelStatus.Closed]: 'bg-gray-500',
}
```

---

## Next.js App Router (no server Supabase)

`page.tsx` only forwards `roomId`; the browser client loads history and subscribes.

```tsx
// app/chat/[roomId]/page.tsx
import { ChatClient } from './ChatClient'

export default function ChatPage({ params }: { params: { roomId: string } }) {
  return <ChatClient roomId={params.roomId} />
}
```

```tsx
// app/chat/[roomId]/ChatClient.tsx
'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import {
  ChannelStatus,
  CHANNEL_STATUS_BADGE,
  PostgresChangeFilterEvent,
  RealtimeListenTypes,
  RealtimePostgresSchema,
  RealtimePostgresTable,
  type Message,
} from '@/lib/realtime-types'

function StatusDot({ status }: { status: ChannelStatus }) {
  return <span className={`h-2 w-2 rounded-full ${CHANNEL_STATUS_BADGE[status]}`} title={status} />
}

export function ChatClient({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [status, setStatus] = useState(ChannelStatus.Connecting)

  useEffect(() => {
    void supabase
      .from(RealtimePostgresTable.Messages)
      .select('*')
      .eq('room_id', roomId)
      .order('created_at', { ascending: true })
      .limit(50)
      .then(({ data }) => setMessages((data as Message[]) ?? []))

    const channel = supabase
      .channel(`chat:${roomId}`)
      .on(
        RealtimeListenTypes.PostgresChanges,
        {
          event: PostgresChangeFilterEvent.Insert,
          schema: RealtimePostgresSchema.Public,
          table: RealtimePostgresTable.Messages,
          filter: `room_id=eq.${roomId}`,
        },
        (payload) => setMessages((prev) => [...prev, payload.new as Message])
      )
      .subscribe((newStatus) => {
        setStatus(newStatus as ChannelStatus)
        if (newStatus === ChannelStatus.ChannelError) console.error('Realtime error — will retry')
      })

    return () => {
      void supabase.removeChannel(channel)
    }
  }, [roomId])

  return (
    <>
      <StatusDot status={status} />
      <MessageList messages={messages} />
    </>
  )
}
```

---

## Reconnect gap-fill

After **`SUBSCRIBED`**, refetch rows with `created_at` greater than a **`useRef`** cursor and merge into state (covers rows missed while disconnected). Update the ref after each gap query. **Do not** call `.subscribe` twice — extend the same callback you use for `setStatus` / errors:

```tsx
const lastEventAt = useRef(new Date().toISOString())

// inside your existing .subscribe((newStatus) => { … })
if (newStatus === ChannelStatus.Subscribed) {
  void supabase
    .from('messages')
    .select('*')
    .gt('created_at', lastEventAt.current)
    .then(({ data }) => {
      if (data?.length) setMessages((prev) => [...prev, ...(data as Message[])])
      lastEventAt.current = new Date().toISOString()
    })
}
```

---

## One channel: Postgres + broadcast + presence

```ts
import { ChannelStatus, PostgresChangeFilterEvent, PresenceListenEvent, RealtimeListenTypes, RealtimePostgresSchema, RealtimePostgresTable } from '@/lib/realtime-types'

const channel = supabase.channel(`collab:${docId}`)

channel
  .on(
    RealtimeListenTypes.PostgresChanges,
    { event: PostgresChangeFilterEvent.Update, schema: RealtimePostgresSchema.Public, table: RealtimePostgresTable.Documents, filter: `id=eq.${docId}` },
    (p) => applyRemoteSave(p.new)
  )
  .on(RealtimeListenTypes.Broadcast, { event: 'op' }, ({ payload }) => applyOperation(payload))
  .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Sync }, () => {
    setCollaborators(Object.values(channel.presenceState()).flat())
  })
  .subscribe(async (status) => {
    if (status === ChannelStatus.Subscribed) await channel.track({ userId: me.id, name: me.name, color: me.color })
  })
```

**Checklist:** assert **`SUBSCRIBED`** before timing-sensitive sends; same-region ~**500ms** expectation; `payload.new` matches schema; **`removeChannel`** per test; exercise **anon vs authenticated** for RLS.
