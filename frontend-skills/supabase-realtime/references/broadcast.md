# Broadcast — Reference

Ephemeral client↔client messages (no Postgres write). Fits chat, cursors, typing, game ticks.
**Auth / private topics:** `references/rls-patterns.md` · Authorization (`../SKILL.md` → **Official documentation**).

---

## Shared types & event enum

```ts
// lib/broadcast-events.ts
export const BroadcastEvent = {
  Message:   'message',
  Cursor:    'cursor',
  Typing:    'typing',
  GameEvent: 'game_event',
} as const
export type BroadcastEvent = typeof BroadcastEvent[keyof typeof BroadcastEvent]

// lib/broadcast-types.ts
export interface ChatMessagePayload { id: string; userId: string; text: string; timestamp: string }
export interface CursorPayload      { userId: string; x: number; y: number; color: string }
export interface TypingPayload      { userId: string; isTyping: boolean }
export type GameEventType         = 'move' | 'attack' | 'collect'
export interface GameEventPayload  { type: GameEventType; playerId: string; data: Record<string, unknown> }
```

**Listen kind:** use `RealtimeListenTypes.Broadcast` (and siblings for Postgres/Presence) from `@/lib/realtime-types` — see **`patterns.md`** Shared types.

---

## API rules (apply to every pattern)

| Rule | Detail |
|------|--------|
| **Topic naming** | `scope:id:entity` — e.g. `room:${id}:messages`, `game:${id}:moves`, `user:${id}:notifications` |
| **Who receives** | Default: **others only**. Add `config: { broadcast: { self: true } }` for sender to receive own events |
| **Private channels** | Add `config: { private: true }` for production. Requires RLS on `realtime.messages` |
| **Send timing** | Before **`ChannelStatus.Subscribed`** → HTTP; after → WebSocket. Guard with `.subscribe((s) => { if (s === ChannelStatus.Subscribed) send() })` — import from **`patterns.md`** Shared types. |
| **Rate limit** | Default **10 msg/sec (≥100ms)**. Set `realtime: { params: { eventsPerSecond: 20 } }` to unlock 50ms |

Listen / send shape (same for all events):
```ts
import { BroadcastEvent } from '@/lib/broadcast-events'
import { RealtimeListenTypes } from '@/lib/realtime-types'

channel
  .on(RealtimeListenTypes.Broadcast, { event: BroadcastEvent.X }, ({ payload }: { payload: XPayload }) => handle(payload))
  .subscribe()

await channel.send({ type: 'broadcast', event: BroadcastEvent.X, payload })
```

---

## Recipes

| Pattern   | Topic                          | Event                       | Key config |
|-----------|--------------------------------|-----------------------------|------------|
| Live chat | `room:${roomId}:messages`      | `BroadcastEvent.Message`    | `self: true`; cleanup `removeChannel` |
| Cursors   | `room:${docId}:cursors`        | `BroadcastEvent.Cursor`     | Throttle ≥100ms; 50ms only if `eventsPerSecond: 20` |
| Typing    | `room:${roomId}:messages`      | `BroadcastEvent.Typing`     | `true` on input, `false` after 2s idle |
| Game sync | `game:${roomId}:moves`         | `BroadcastEvent.GameEvent`  | No extra config — default skips sender |

---

## Live chat (React — full example)

```tsx
import { useEffect, useRef, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { BroadcastEvent } from '@/lib/broadcast-events'
import type { ChatMessagePayload } from '@/lib/broadcast-types'
import { RealtimeListenTypes } from '@/lib/realtime-types'

export function LiveChat({ roomId, userId }: { roomId: string; userId: string }) {
  const [messages, setMessages] = useState<ChatMessagePayload[]>([])
  const [input, setInput]       = useState('')
  const channelRef = useRef<ReturnType<typeof supabase.channel> | null>(null)

  useEffect(() => {
    const ch = supabase.channel(`room:${roomId}:messages`, {
      config: { private: true, broadcast: { self: true } },
    })
    ch.on(RealtimeListenTypes.Broadcast, { event: BroadcastEvent.Message },
      ({ payload }: { payload: ChatMessagePayload }) => setMessages((p) => [...p, payload])
    ).subscribe()
    channelRef.current = ch
    return () => { supabase.removeChannel(ch) }
  }, [roomId])

  const send = async () => {
    if (!input.trim() || !channelRef.current) return
    await channelRef.current.send({
      type: 'broadcast', event: BroadcastEvent.Message,
      payload: { id: crypto.randomUUID(), userId, text: input, timestamp: new Date().toISOString() } satisfies ChatMessagePayload,
    })
    setInput('')
  }

  return (
    <div>
      <div>{messages.map((m) => <div key={m.id}><strong>{m.userId}:</strong> {m.text}</div>)}</div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button type="button" onClick={send}>Send</button>
    </div>
  )
}
```

---

## Cursors / Typing / Game (minimal snippets)

```ts
import { BroadcastEvent } from '@/lib/broadcast-events'
import type { CursorPayload, TypingPayload, GameEventPayload } from '@/lib/broadcast-types'
import { RealtimeListenTypes } from '@/lib/realtime-types'

// — Cursors: throttle ≥100ms (default limit); 50ms only with eventsPerSecond: 20
const cursors: Record<string, CursorPayload> = {}
let tCursor: ReturnType<typeof setTimeout>
document.addEventListener('mousemove', (e) => {
  clearTimeout(tCursor)
  tCursor = setTimeout(() => channel.send({
    type: 'broadcast', event: BroadcastEvent.Cursor,
    payload: { x: e.clientX, y: e.clientY, userId: myId, color: myColor } satisfies CursorPayload,
  }), 100)
})
channel.on(RealtimeListenTypes.Broadcast, { event: BroadcastEvent.Cursor },
  ({ payload }: { payload: CursorPayload }) => { cursors[payload.userId] = payload; renderCursors(cursors) }
).subscribe()

// — Typing: true on input, false after 2s quiet
let tTyping: ReturnType<typeof setTimeout>
inputEl.addEventListener('input', () => {
  channel.send({ type: 'broadcast', event: BroadcastEvent.Typing, payload: { userId: myId, isTyping: true } satisfies TypingPayload })
  clearTimeout(tTyping)
  tTyping = setTimeout(() =>
    channel.send({ type: 'broadcast', event: BroadcastEvent.Typing, payload: { userId: myId, isTyping: false } satisfies TypingPayload })
  , 2000)
})
channel.on(RealtimeListenTypes.Broadcast, { event: BroadcastEvent.Typing }, ({ payload }: { payload: TypingPayload }) =>
  setTypingUsers((p) => payload.isTyping ? [...new Set([...p, payload.userId])] : p.filter((id) => id !== payload.userId))
)

// — Game: default already skips sender, no config needed
const gameCh = supabase.channel(`game:${roomId}:moves`)
gameCh.on(RealtimeListenTypes.Broadcast, { event: BroadcastEvent.GameEvent },
  ({ payload }: { payload: GameEventPayload }) => applyGameEvent(payload)
).subscribe()
const emitGameEvent = (e: GameEventPayload) =>
  gameCh.send({ type: 'broadcast', event: BroadcastEvent.GameEvent, payload: e })
```