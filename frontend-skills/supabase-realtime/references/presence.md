# Presence — Full Reference

Track and synchronize user state across clients. Shows who is online,
what they're doing, and cleans up automatically on disconnect.
**Private channels + auth:** `references/rls-patterns.md` · Authorization (`../SKILL.md` → **Official documentation**).

## Table of Contents
1. [Basic online tracking](#basic)
2. [Avatar stack component](#avatars)
3. [Document collaborators](#doc)
4. [Presence + Auth](#auth)

---

## 1. Basic Online Tracking {#basic}

```ts
import { ChannelStatus, PresenceListenEvent, RealtimeListenTypes } from '@/lib/realtime-types'

interface UserPresence {
  userId: string
  username: string
  avatar_url?: string
  online_at: string
}

const channel = supabase.channel('room:online-users')

// Listen for presence changes
channel
  .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Sync }, () => {
    // Full state after any join/leave
    const state = channel.presenceState<UserPresence>()
    const users = Object.values(state).flat()
    setOnlineUsers(users)
  })
  .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Join }, ({ newPresences }) => {
    console.log('Joined:', newPresences)
  })
  .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Leave }, ({ leftPresences }) => {
    console.log('Left:', leftPresences)
  })
  .subscribe(async (status) => {
    if (status === ChannelStatus.Subscribed) {
      // Announce yourself
      await channel.track({
        userId: currentUser.id,
        username: currentUser.name,
        avatar_url: currentUser.avatar,
        online_at: new Date().toISOString()
      })
    }
  })
```

---

## 2. Avatar Stack Component {#avatars}

```tsx
// components/OnlineAvatars.tsx
import Image from 'next/image'
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'
import { ChannelStatus, PresenceListenEvent, RealtimeListenTypes } from '@/lib/realtime-types'

interface Presence { userId: string; username: string; avatar_url: string }

export function OnlineAvatars({
  roomId,
  currentUser
}: {
  roomId: string
  currentUser: { id: string; name: string; avatar_url: string }
}) {
  const [online, setOnline] = useState<Presence[]>([])

  useEffect(() => {
    const channel = supabase.channel(`room:${roomId}`)

    channel
      .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Sync }, () => {
        const state = channel.presenceState<Presence>()
        setOnline(Object.values(state).flat())
      })
      .subscribe(async (status) => {
        if (status === ChannelStatus.Subscribed) {
          await channel.track({
            userId: currentUser.id,
            username: currentUser.name,
            avatar_url: currentUser.avatar_url
          })
        }
      })

    return () => { supabase.removeChannel(channel) }
  }, [roomId, currentUser])

  return (
    <div className="flex -space-x-2">
      {online.slice(0, 5).map((user) => (
        <Image
          key={user.userId}
          src={user.avatar_url}
          alt={user.username}
          title={user.username}
          width={32}
          height={32}
          className="h-8 w-8 rounded-full border-2 border-white"
        />
      ))}
      {online.length > 5 && (
        <span className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-xs">
          +{online.length - 5}
        </span>
      )}
    </div>
  )
}
```

Allow remote avatar hosts in **`next.config.js`** (`images.remotePatterns`) when `avatar_url` is not same-origin.

---

## 3. Document Collaborators — Track What Each User Is Editing {#doc}

```ts
import { ChannelStatus, PresenceListenEvent, RealtimeListenTypes } from '@/lib/realtime-types'

interface DocPresence {
  userId: string
  username: string
  color: string
  cursor?: { line: number; col: number }
  viewing_section?: string
}

const docChannel = supabase.channel(`doc:${docId}`)

docChannel
  .on(RealtimeListenTypes.Presence, { event: PresenceListenEvent.Sync }, () => {
    const collaborators = Object.values(
      docChannel.presenceState<DocPresence>()
    ).flat()
    renderCollaboratorCursors(collaborators)
  })
  .subscribe(async (status) => {
    if (status === ChannelStatus.Subscribed) {
      await docChannel.track({
        userId: me.id,
        username: me.name,
        color: assignColor(me.id), // deterministic color from userId
        viewing_section: 'introduction'
      })
    }
  })

// Update presence when user moves cursor
editor.on('cursorActivity', async () => {
  await docChannel.track({
    ...myPresence,
    cursor: { line: editor.getCursor().line, col: editor.getCursor().ch }
  })
})
```

---

## 4. Presence + Auth (Server-side validation) {#auth}

For sensitive presence data, validate via a Supabase Edge Function before tracking. **Wire `createClient` from `@supabase/supabase-js`** (anon key + forwarded `Authorization`) in **`../../supabase-api-integration/references/workflow.md`** → **Edge Functions (Deno)** — do not duplicate import/setup in this doc.

```ts
// `supabase` from `@supabase/supabase-js` — full Edge setup:
// ../../supabase-api-integration/references/workflow.md (#edge-functions)
const {
  data: { user },
} = await supabase.auth.getUser()
if (!user) return new Response('Unauthorized', { status: 401 })

return new Response(JSON.stringify({ userId: user.id, verified: true }))
```

```ts
// Client: fetch token, then track
const { data } = await supabase.functions.invoke('presence-token')
if (data?.verified) {
  await channel.track({ userId: data.userId, ...otherPresenceData })
}
```