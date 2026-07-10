---
name: supabase-queues
description: >
  Supabase Queues (pgmq): durable FIFO messages, visibility timeouts, producers/consumers,
  Edge workers, retries. Use for background jobs, webhooks, delayed work. Read SKILL first;
  SQL/JS patterns in references/. RLS + PostgREST exposure: references/rls-patterns.md.
  Canonical doc links: see SKILL.md § Official documentation.
---

# Supabase Queues Skill

**Supabase Queues** = Postgres-native durable queues on **pgmq** (GitHub link in **Official documentation** below) — guaranteed delivery, **exactly-once within a visibility window**, optional archive. Supabase product docs: **Official documentation** (below).

**Postgres:** enable `pgmq` on **15.6.1.143+** (see **Official documentation** → Quickstart); older hosts may lack the module.

## Official documentation

Reference files point here instead of repeating URLs.

- **pgmq (extension):** https://github.com/tembo-io/pgmq
- **Supabase Queues (overview):** https://supabase.com/docs/guides/queues
- **Queues API (`pgmq_public`):** https://supabase.com/docs/guides/queues/api
- **Quickstart (version, expose + RLS):** https://supabase.com/docs/guides/queues/quickstart

---

## Flow

```
Need → 1 CLASSIFY → 2 ACCESS MODEL → 3 PRODUCER → 4 CONSUMER → 5 REVIEW → 6 DELIVER
```

| # | Phase | Do |
|---|--------|-----|
| 1 | Classify | Basic vs unlogged vs partitioned (**Coming Soon** in Quickstart); FIFO, no priority — see **Official documentation** (overview + Quickstart). |
| 2 | Access model | **Server-only** → `pgmq.*` + service role / DB. **Browser/anon/auth client** → expose via Data API + **`pgmq_public`** + **RLS on `pgmq.q_*`** → **`references/rls-patterns.md`**. |
| 3 | Producer | `pgmq.send` / `send_batch`, delay (`sleep_seconds`), triggers — **`references/producers.md`**. |
| 4 | Consumer | `read` + `archive`/`delete`, `pop`, VT > max work time, DLQ — **`references/consumers.md`**. |
| 5 | Review | VT, idempotency, archive vs delete, no stuck messages, RLS if exposed, no service_role in client. |
| 6 | Deliver | SQL migrations / Edge code as requested; verify queue depth + worker logs. |

---

## Phase 1 — Classify & access

```
Durability?
├── Default durable workload     → Basic queue (logged)
├── Speed > durability          → Unlogged queue
└── Huge scale / partitions       → Partitioned (**Coming Soon** — Quickstart in **Official documentation**)

Who calls send/read?
├── Server / Edge / SQL only     → pgmq schema (no client RLS path required)
└── Client via Supabase JS       → pgmq_public RPCs + RLS on pgmq.q_<name> (rls-patterns.md)
```

---

## Phase 5 — Review checklist

- [ ] Queue type matches durability need.
- [ ] **Visibility timeout** > worst-case processing time (Queues overview — **Official documentation**).
- [ ] Consumer **archives or deletes** (or intentional pop); no infinite hidden messages.
- [ ] If **PostgREST exposed**: RLS on **`pgmq.q_*`**, grants aligned to RPC matrix — **`references/rls-patterns.md`**.
- [ ] **service_role** only server-side (Quickstart — **Official documentation**).
- [ ] Retry / DLQ story for poison messages — **`references/consumers.md`**.

---

## Block rules

| # | Rule |
|---|------|
| **B1** | Never ship **service_role** to browsers or public repos. |
| **B2** | **VT shorter than work** → duplicate processing / thrash — size VT to handler + I/O. |
| **B3** | Expose queues to Data API **without** RLS on `pgmq.q_*` → **stop** until policies exist (**`rls-patterns.md`**). |
| **B4** | Do not `pop` lossy paths for work that **must** survive retries unless explicitly idempotent. |
| **B5** | Payloads: no PII you cannot justify; validate shape before enqueue. |

---

## References

| File | Use for |
|------|---------|
| `references/rls-patterns.md` | PostgREST expose, RLS on `pgmq.q_*`, `pgmq_public` grants |
| `references/producers.md` | send, batch, delay, triggers, client vs server |
| `references/consumers.md` | read/archive/delete/pop, Edge worker, backoff, DLQ |
| `references/use-case.md` | Welcome email, payments, webhooks, cleanup, audit recipes |

---

## Anti-patterns

| Never | Instead |
|-------|---------|
| Client dequeue with **bypass** role | `anon`/`authenticated` + RLS + least privilege RPCs |
| **No ack** after successful work | `archive` or `delete` (or deliberate pop) |
| **Unbounded** queue growth | Monitor depth, DLQ, consumer autoscaling |
| Same **message processed forever** | DLQ / max `read_ct` handling — `consumers.md` |
| RLS **`USING (true)`** on exposed queues | Tenant-scoped checks on `message` / ownership |
| Secrets in **message JSON** logged everywhere | References / vault patterns in producers |

## API anchor

**`@supabase/supabase-js` `createClient`:** canonical patterns in **`../supabase-api-integration/references/workflow.md`** (Step 2 + Edge Functions) — queue reference snippets assume `supabase` is wired there; do not duplicate imports.

`CREATE EXTENSION IF NOT EXISTS pgmq;` · `SELECT pgmq.create('queue_name');` — **`use-case.md`** / **`producers.md`**. SQL: `SELECT pgmq.send('queue', '{"k":"v"}'::jsonb);` · `SELECT * FROM pgmq.read('queue', vt_seconds, qty);` · Data API (`pgmq_public`): **`send`**, **`read`**, **`pop`**, **`archive`**, **`delete`**, **`send_batch`** — use **`sleep_seconds` / `n`** on **`read`** per **Official documentation** → Queues API; details in **`producers.md`** / **`consumers.md`**.
