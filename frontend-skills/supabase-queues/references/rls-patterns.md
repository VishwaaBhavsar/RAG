# Queues — RLS & API exposure

**Official docs:** `../SKILL.md` → **Official documentation**. **Skill entry:** same file (block rules, flow).

---

## When this applies

- **Server-only (`pgmq` schema):** consumers use Postgres or **service_role** Edge Functions — no PostgREST on queue tables. You still follow least privilege in code; RLS on `pgmq.q_*` is **not** forced by this path alone.
- **Client / anon / authenticated via Data API:** enable **Expose Queues via PostgREST** → Supabase exposes **`pgmq_public`** wrappers. Then you **must** enable **RLS** on every underlying queue table `pgmq.q_*` you expose, and add policies — per Quickstart in **Official documentation** (`../SKILL.md`).

---

## `pgmq_public` function → table permissions

Grant matching privileges on the **queue table** for each role that may call the RPC (Dashboard **Queue Settings** manages this). Reference matrix from Quickstart in **Official documentation** (`../SKILL.md`):

| Operation (RPC) | Queue table needs |
|-------------------|-------------------|
| `send`, `send_batch` | `SELECT`, `INSERT` |
| `read`, `pop` | `SELECT`, `UPDATE` |
| `archive`, `delete` | `SELECT`, `DELETE` |

**Never** expose **`postgres`** or **`service_role`** keys in the browser — Queues overview in **Official documentation** (`../SKILL.md`) / platform guidance.

---

## Enable RLS on `pgmq.q_<queue_name>`

1. `ALTER TABLE pgmq.q_my_queue ENABLE ROW LEVEL SECURITY;`
2. Policies for **who may insert** (enqueue), **select/update** (read / visibility timeout), **delete** (ack / pop path) — match your product rules (tenant id in `message` jsonb, user id, role, etc.).

**Illustrative** policies (adjust column / JSON paths to your payload contract):

```sql
-- Example: only authenticated users enqueue jobs tagged with their user id
CREATE POLICY "enqueue_own_user_jobs"
  ON pgmq.q_email_jobs FOR INSERT TO authenticated
  WITH CHECK ((message->>'userId')::uuid = (SELECT auth.uid()));

-- Example: users may only read (claim) rows for their user id in payload
CREATE POLICY "read_own_jobs"
  ON pgmq.q_email_jobs FOR SELECT TO authenticated
  USING ((message->>'userId')::uuid = (SELECT auth.uid()));

CREATE POLICY "update_own_jobs_vt"
  ON pgmq.q_email_jobs FOR UPDATE TO authenticated
  USING ((message->>'userId')::uuid = (SELECT auth.uid()))
  WITH CHECK ((message->>'userId')::uuid = (SELECT auth.uid()));
```

**Prefer** narrow policies over `USING (true)` for client-visible queues. If only **trusted servers** should dequeue, keep reads on **`pgmq`** + **service_role** and do **not** expose dequeue RPCs to `anon`.

---

## Anti-patterns (queues + RLS)

| Avoid | Why |
|-------|-----|
| Expose PostgREST queues with **RLS off** on `pgmq.q_*` | Quickstart (`../SKILL.md` → **Official documentation**) requires RLS when exposed |
| `service_role` in frontend | Full bypass of RLS |
| Policies that ignore **message shape** | Any client could enqueue arbitrary payloads for others |
| **Visibility timeout** shorter than worst-case handler time | Poison retry loops — align with `../SKILL.md` / `consumers.md` |

---

## See also

- **`producers.md`** — client `pgmq_public.send`, triggers, batch/delayed send.
- **`consumers.md`** — `read` / `archive` / `delete` / `pop`, workers, DLQ.
- **`use-case.md`** — end-to-end recipes (welcome email, retries, webhooks, …).
