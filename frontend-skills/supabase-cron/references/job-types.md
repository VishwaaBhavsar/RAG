# Cron Job Types — Patterns

**Entry:** `../SKILL.md` (flow, B1–B5, anti-patterns). **Recipes** (digest, cleanup, matview, subscriptions, …): **`use-case.md`**. **Schedules / GMT / `N seconds`:** **`syntax.md`**. Official docs: `../SKILL.md` → **Official documentation**.

---

## 1. SQL snippet

Shape: `SELECT cron.schedule('name', 'schedule', $$ … $$);` — command is raw SQL. Keep DML **bounded** (windows, `LIMIT`); unbounded deletes → **`../SKILL.md` B2**.

```sql
SELECT cron.schedule('weekly-cleanup', '0 3 * * 6',
  $$DELETE FROM logs WHERE created_at < now() - interval '90 days'$$);
```

Multi-step cleanup, audit archive, soft-delete purge → **`use-case.md`** §2. `REFRESH MATERIALIZED VIEW` → **`use-case.md`** §4. Do **not** lean on scheduled **`VACUUM`** on hosted Supabase → **`../SKILL.md` B5**.

---

## 2. Database function

Put logic in PL/pgSQL (unit-test / reuse), then schedule **`SELECT fn()`** or **`CALL proc()`**.

```sql
SELECT cron.schedule('tick', '* * * * *', 'SELECT process_pending_notifications()');
```

Full function bodies (subscriptions, birthday, health, …) → **`use-case.md`** §§3, 6, 8.

---

## 3. HTTP / Edge (`pg_net`)

**B1:** no keys in repo SQL — Vault (e.g. `service_role_key`) + `vault.decrypted_secrets`. Enable **`pg_net`** (Dashboard → Database → Extensions). Always set **`timeout_milliseconds`**. For **`'30 seconds'`** and other sub-minute strings → version gate in **`syntax.md`**.

```sql
CREATE EXTENSION IF NOT EXISTS pg_net;

SELECT cron.schedule('edge-worker', '* * * * *', $$
  SELECT net.http_post(
    url := 'https://YOUR_PROJECT.supabase.co/functions/v1/email-worker',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'service_role_key')
    ),
    body := '{}'::jsonb,
    timeout_milliseconds := 25000
  );
$$);
```

**Same** `headers` / Vault pattern for other URLs or schedules (e.g. `'30 seconds'`): only change `url`, `body`, schedule. Alternate real URLs → **`use-case.md`** §§1, 5. Do **not** use `current_setting('app.service_role_key')` for secrets in examples you ship.

---

## 4. Cron → queue

Cron **enqueues**; heavy work runs in workers (limits in **`../SKILL.md`** intro).

```sql
SELECT cron.schedule('enqueue-hourly', '0 * * * *',
  $$SELECT pgmq.send('report_jobs', jsonb_build_object('type', 'hourly_summary', 'requestedAt', now()))$$);
```

`pgmq` payload patterns → **`use-case.md`** §7. Consumer / worker code → **Queues skill** (not duplicated here).
