# Queues — Use Case Recipes

**`pgmq_public`** via PostgREST needs **RLS on `pgmq.q_*`** — see **`references/rls-patterns.md`**.

## Shared pattern

| Role | How |
|------|-----|
| **Enqueue (SQL)** | `PERFORM pgmq.send('queue_name', jsonb_build_object(...));` from triggers / `SECURITY DEFINER` functions |
| **Enqueue (client/Edge)** | `supabase.schema('pgmq_public').rpc('send', { queue_name, message, sleep_seconds? })` |
| **Worker** | Read batch → process → **`archive`** on success; on failure use visibility timeout redelivery or cap **`read_ct`** and dead-letter / log |

```sql
-- Minimal trigger enqueue (welcome, fan-out, cleanup patterns)
PERFORM pgmq.send('my_queue', jsonb_build_object('kind', 'JOB', 'id', NEW.id));
```

```ts
// Minimal worker loop (same shape for email, webhooks, notifications, cleanup)
for (const m of await readQueue('my_queue', vtSeconds, batchSize)) {
  try {
    await handle(m.message)
    await archiveMessage('my_queue', m.msg_id)
  } catch {
    /* let VT expire for retry, or branch on m.read_ct for give-up */
  }
}
```

## Use cases

1. [Welcome email on signup](#1-welcome-email-on-signup)
2. [Retry failed payments](#2-retry-failed-payments)
3. [Notification fan-out](#3-notification-fan-out)
4. [Cart abandonment (delayed + cancel)](#4-cart-abandonment-delayed--cancel)
5. [Webhook delivery + retry](#5-webhook-delivery--retry)
6. [Cleanup expired rows](#6-cleanup-expired-rows)
7. [Audit from archives](#7-audit-from-archives)

---

## 1. Welcome email on signup

**Flow:** `auth.users` (or profile) **AFTER INSERT** trigger → `pgmq.send('email_jobs', { type: 'WELCOME', to, userId })` → Cron/Edge worker sends template → archive.

Use `SECURITY DEFINER` only where needed; keep payload minimal (no secrets in JSON).

---

## 2. Retry failed payments

**Flow:** On failure, **`send`** with **`sleep_seconds`** from a backoff list (e.g. 60 → 300 → 900 → 3600). Worker retries the charge; archive on success; at max attempts notify ops and archive (or `send` to a `*_dead` queue).

---

## 3. Notification fan-out

**Flow:** New post / event → trigger loops recipients (or batches IDs) → one `send` per unit of work (user + payload). Worker delivers push / in-app / SMS as needed, then archives. For huge fan-out, consider batching one message with an array and splitting in the worker.

---

## 4. Cart abandonment (delayed + cancel)

**Flow:** On cart activity, **`send`** with `sleep_seconds: 1800` (or your window). Store returned **`msg_id`** per user (small side table). On checkout, **`delete`** that message from the queue so the worker never sees it. Worker sends the reminder only for messages still present.

---

## 5. Webhook delivery + retry

**Flow:** `send('webhooks', { endpoint, payload })`. Worker `POST` with short timeout; archive on 2xx; non-2xx or network error → rely on VT / redelivery; after N attempts archive and optionally **`send`** to `webhooks_dead` with error text for inspection.

---

## 6. Cleanup expired rows

**Flow:** **Cron** (see supabase-cron skill) calls a function that **`pgmq.send`** several `cleanup_jobs` messages (`task`, `olderThan`, etc.). Worker runs bounded deletes or maintenance in order; avoids long transactions in the Cron job itself.

```sql
CREATE OR REPLACE FUNCTION enqueue_cleanup() RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  PERFORM pgmq.send('cleanup_jobs', jsonb_build_object('task','DELETE_EXPIRED_SESSIONS','olderThan', now() - interval '30 days'));
  PERFORM pgmq.send('cleanup_jobs', jsonb_build_object('task','DELETE_SOFT_DELETED','olderThan', now() - interval '7 days'));
END;
$$;
```

---

## 7. Audit from archives

Processed messages live in **`pgmq.a_<queue_name>`**. Query `message`, `enqueued_at`, `archived_at` for retention / compliance.

```sql
SELECT msg_id,
       message->>'userId' AS user_id,
       message->>'action' AS action,
       enqueued_at,
       archived_at
FROM pgmq.a_audit_log
WHERE archived_at > now() - interval '30 days'
ORDER BY archived_at DESC;
```
