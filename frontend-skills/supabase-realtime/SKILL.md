---
name: supabase-realtime
description: >
  Supabase Realtime: Postgres Changes, Broadcast, Presence. Use for live DB feeds, chat,
  cursors, presence, collaborative UI. Read SKILL first; channel code in references/.
  RLS: references/rls-patterns.md. Canonical doc links: see SKILL.md § Official documentation.
---

# Supabase Realtime Skill

**Supabase Realtime** — **Broadcast** (client events), **Presence** (who’s online), **Postgres Changes** (DB replication). Supabase docs and the open-source Realtime server: **Official documentation** (below).

## Official documentation

Reference files point here instead of repeating URLs.

- **Realtime (overview):** https://supabase.com/docs/guides/realtime
- **Broadcast:** https://supabase.com/docs/guides/realtime/broadcast
- **Presence:** https://supabase.com/docs/guides/realtime/presence
- **Postgres Changes:** https://supabase.com/docs/guides/realtime/postgres-changes
- **Realtime Authorization (private channels, `realtime.messages`):** https://supabase.com/docs/guides/realtime/authorization
- **Realtime server (GitHub):** https://github.com/supabase/realtime

---

## Flow

```
Need → 1 CLASSIFY → 2 DATA + AUTH → 3 CHANNEL CODE → 4 LIFECYCLE → 5 REVIEW → 6 DELIVER
```

| # | Phase | Do |
|---|--------|-----|
| 1 | Classify | DB row events vs custom events vs presence — tree **Phase 1**. |
| 2 | Data + auth | **Postgres Changes:** add table to **`supabase_realtime`** publication + **SELECT RLS** on that table. **Broadcast/Presence (private):** policies on **`realtime.messages`** + `private: true` — **`references/rls-patterns.md`**, **Official documentation** → Authorization. |
| 3 | Channel code | `.channel().on(...).subscribe()` — patterns in **`postgres-changes.md`**, **`broadcast.md`**, **`presence.md`**, **`patterns.md`**. |
| 4 | Lifecycle | **`removeChannel`** / unsubscribe on unmount; reconnect + token refresh per **`patterns.md`**. |
| 5 | Review | Filters for narrow subscriptions; JWT for private topics; no leak via permissive RLS. |
| 6 | Deliver | Client modules / hooks; SQL policies when needed. |

---

## Phase 1 — Which feature?

```
React to INSERT/UPDATE/DELETE on a table?     → Postgres Changes (+ publication + table RLS)
Low-latency custom events between clients?    → Broadcast (optionally private + realtime.messages RLS)
Who is online / sync participant state?        → Presence (often with Broadcast)
One screen needs several?                      → Compose channels; see patterns.md
```

---

## Phase 5 — Review checklist

- [ ] Table in **`supabase_realtime`** if using Postgres Changes.
- [ ] **RLS** allows only intended rows for subscribing roles (Postgres Changes — **Official documentation**).
- [ ] **Private** Broadcast/Presence → **`realtime.messages`** policies + `config: { private: true }` (Authorization — **Official documentation**).
- [ ] **Channel cleanup** on route change / unmount.
- [ ] **`filter`** on subscriptions when rows are scoped (room, tenant).
- [ ] **INSERT/UPDATE/DELETE** handlers use `payload.new` / `payload.old` correctly.

---

## Block rules

| # | Rule |
|---|------|
| **B1** | No **private** channel without **`realtime.messages`** policies you understand — Authorization (**Official documentation**). |
| **B2** | No Postgres Changes on a table users must **not** read without matching **restrictive SELECT RLS**. |
| **B3** | Do not subscribe in a loop without **cleanup** — leaks connections. |
| **B4** | **Heavy RLS** on `realtime.messages` at scale → monitor connect latency — simplify or server-relay (Authorization — **Official documentation**). |
| **B5** | **JWT expiry:** refresh `access_token` on channel or reconnect before expiry (Authorization — **Official documentation**). |

---

## References

| File | Use for |
|------|---------|
| `references/rls-patterns.md` | Table RLS vs `realtime.messages`, private channels, `realtime.topic()` |
| `references/postgres-changes.md` | INSERT/UPDATE/DELETE subscribe, filters, hooks |
| `references/broadcast.md` | Send/receive custom events |
| `references/presence.md` | `track`, `presenceState`, sync events |
| `references/patterns.md` | Next.js, errors, reconnect, combine features |

---

## Anti-patterns

| Never | Instead |
|-------|---------|
| Publication on + **RLS off** open table | Enable RLS + least-privilege `SELECT` |
| Private channel **without** policies | Public access off + `realtime.messages` SQL |
| Missing **`removeChannel`** | `useEffect` cleanup / router leave |
| Subscribe **all rows** when app needs one room | `filter: 'col=eq.val'` |
| Trust **client-only** for secrets in payloads | Server authority + Broadcast payloads sized |

## Client setup anchor

**`createClient`:** **`../supabase-api-integration/references/workflow.md`** (Next.js singleton + **Edge Functions (Deno)**).

**`createClient` → `supabase.channel(name)` → `.on(…)` → `.subscribe()`** — use **`RealtimeListenTypes`**, **`PostgresChangeFilterEvent`**, **`PresenceListenEvent`**, **`RealtimePostgresSchema`**, and **`RealtimePostgresTable`** from **`references/patterns.md`** instead of string literals for listen kinds, Postgres filter events, and replicated schema/table names. Feature snippets: **`patterns.md`**, **`postgres-changes.md`**, **`broadcast.md`**, **`presence.md`**.

**Postgres Changes prerequisite:** add table to **`supabase_realtime`** publication (`ALTER PUBLICATION supabase_realtime ADD TABLE …` or Dashboard replication) — **`postgres-changes.md`**.
