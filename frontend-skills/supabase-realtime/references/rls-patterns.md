# Realtime — RLS & authorization

**Official docs:** `../SKILL.md` → **Official documentation**. **Skill entry:** same file (flow, block rules).

---

## Two different RLS surfaces

| Surface | What it controls |
|---------|------------------|
| **Your data tables** (`public.*`, etc.) | **Postgres Changes:** clients only receive change events for rows the subscriber role **may SELECT** (Postgres Changes guide in **Official documentation** — `../SKILL.md` — plus RLS on those tables). |
| **`realtime.messages`** | **Broadcast** + **Presence** on **private** channels: policies gate who may **read** / **insert** messages for a channel topic (Authorization — **Official documentation**). |

---

## Postgres Changes + table RLS

- Add table to **`supabase_realtime`** publication (`ALTER PUBLICATION supabase_realtime ADD TABLE …` or Dashboard replication).
- **`SELECT`** policies (and other rules) on the replicated table determine which changes each user receives — no separate “realtime policy” on the table beyond normal RLS.
- Use **filters** in the client subscription to limit traffic (`filter: 'room_id=eq.x'`).
- **Private vs public** channel config still applies to the channel; data visibility is still bounded by **table RLS**.

More examples: **`postgres-changes.md`** §7.

---

## Broadcast & Presence → `realtime.messages`

Private channels: `supabase.channel('topic', { config: { private: true } })` and disable **Allow public access** in Realtime settings (Authorization — **Official documentation** — `../SKILL.md`) when enforcing auth.

Policies are on **`realtime.messages`** (validated at join; Realtime runs a probe query and rolls it back — Authorization — **Official documentation**):

| Helper / column | Use |
|-----------------|-----|
| `(SELECT realtime.topic())` | Channel topic string the client is joining |
| `realtime.messages.extension` | `'broadcast'` and/or `'presence'` |
| `(SELECT auth.uid())` | Owner checks |
| `(current_setting('request.jwt.claims', true))::json` | JWT claims (e.g. email) |

**Read** (receive broadcasts / presence sync) → `FOR SELECT` on `realtime.messages` with `USING (…)` matching topic + extension.

**Write** (send broadcast / track presence) → `FOR INSERT` on `realtime.messages` with `WITH CHECK (…)` same idea.

**Example pattern** (membership table `rooms_users` with `user_id`, `room_topic`): allow `SELECT` on `realtime.messages` when `exists (select 1 from rooms_users where user_id = (select auth.uid()) and room_topic = (select realtime.topic()) and realtime.messages.extension in ('broadcast'))` — mirror for `INSERT` / `presence` / combined `IN ('broadcast','presence')` per Authorization (**Official documentation**).

---

## Operational notes

- **Policy complexity** increases connect latency and join failures — keep policies tight (Authorization — **Official documentation**).
- **JWT refresh:** access is cached for the connection; refresh via Realtime **`access_token`** message or reconnect when roles change.
- **Scale:** for very high-volume Postgres Changes, consider a denormalized “feed” table, server-side relay + **Broadcast**, or filters — Postgres Changes scaling notes in **Official documentation** (`../SKILL.md`).

---

## See also

- **`broadcast.md`**, **`presence.md`** — client send/receive APIs.
- **`postgres-changes.md`** — subscribe filters, hooks, table RLS primer.
- **`patterns.md`** — Next.js / cleanup / combined channels.
