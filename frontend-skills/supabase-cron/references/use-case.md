# Cron Use Cases — Real-World Recipes

Companion to `../SKILL.md`. **HTTP:** Vault secret `service_role_key` + `net.http_post` + `timeout_milliseconds` — canonical pattern **`references/job-types.md`** §3. Official docs: `../SKILL.md` → **Official documentation**.

**Index:** [1 digest](#digest) · [2 cleanup](#cleanup) · [3 subscriptions](#subscriptions) · [4 matview](#matview) · [5 api-sync](#api-sync) · [6 birthday](#birthday) · [7 reports](#reports) · [8 health](#health)

## 1. Daily Digest Email {#digest}

Weekday **8 AM GMT** (`0 8 * * 1-5` = 1:30 PM IST). Edge Function `send-digest`: `digest_enabled` users → activity summary → email (e.g. Resend).

```sql
SELECT cron.schedule('daily-digest', '0 8 * * 1-5', $$
  SELECT net.http_post(
    url := 'https://PROJECT.supabase.co/functions/v1/send-digest',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'service_role_key')
    ),
    body := jsonb_build_object('date', current_date, 'type', 'daily'),
    timeout_milliseconds := 25000
  );
$$);
```

## 2. Cleanup Expired Records {#cleanup}

```sql
SELECT cron.schedule('cleanup-sessions', '0 * * * *',
  $$DELETE FROM sessions WHERE expires_at < now()$$);

SELECT cron.schedule('purge-soft-deleted', '0 3 * * *', $$
  DELETE FROM posts WHERE deleted_at < now() - interval '30 days';
  DELETE FROM comments WHERE deleted_at < now() - interval '30 days';
  DELETE FROM user_files WHERE deleted_at < now() - interval '30 days';
$$);

SELECT cron.schedule('archive-audit-logs', '0 1 1 * *', $$
  INSERT INTO audit_logs_archive SELECT * FROM audit_logs WHERE created_at < now() - interval '90 days';
  DELETE FROM audit_logs WHERE created_at < now() - interval '90 days';
$$);
```

## 3. Subscription Expiry Checker {#subscriptions}

Fn: mark `expired`; enqueue `SUBSCRIPTION_EXPIRING` for 7-day window (deduped). Cron **8 AM daily**.

```sql
CREATE OR REPLACE FUNCTION check_subscription_expiry() RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  UPDATE subscriptions SET status = 'expired' WHERE status = 'active' AND expires_at < now();
  INSERT INTO notification_queue (user_id, type, data)
  SELECT user_id, 'SUBSCRIPTION_EXPIRING', jsonb_build_object('expires_at', expires_at)
  FROM subscriptions
  WHERE status = 'active' AND expires_at BETWEEN now() AND now() + interval '7 days'
    AND NOT EXISTS (
      SELECT 1 FROM notification_queue nq
      WHERE nq.user_id = subscriptions.user_id AND nq.type = 'SUBSCRIPTION_EXPIRING'
        AND nq.created_at > now() - interval '7 days'
    );
END;
$$;

SELECT cron.schedule('check-subscriptions', '0 8 * * *', 'SELECT check_subscription_expiry()');
```

## 4. Materialized View Refresh {#matview}

```sql
CREATE MATERIALIZED VIEW dashboard_metrics AS
SELECT date_trunc('day', created_at) AS day, COUNT(*) AS new_users, SUM(amount) AS revenue
FROM orders GROUP BY 1;

SELECT cron.schedule('refresh-dashboard', '*/30 * * * *',
  'REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_metrics');
```

## 5. External API Sync {#api-sync}

Same Vault **`Authorization`** header pattern as **§1**; Edge Function `sync-crm`. **Every 4h** GMT.

```sql
SELECT cron.schedule('sync-crm-contacts', '0 */4 * * *', $$
  SELECT net.http_post(
    url := 'https://PROJECT.supabase.co/functions/v1/sync-crm',
    headers := jsonb_build_object(
      'Authorization', 'Bearer ' || (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE name = 'service_role_key')
    ),
    body := jsonb_build_object('source', 'hubspot', 'full_sync', false),
    timeout_milliseconds := 60000
  );
$$);
```

## 6. Birthday / Anniversary Notifications {#birthday}

Fn: enqueue `BIRTHDAY` for users whose month/day matches today. Cron **7 AM GMT**.

```sql
CREATE OR REPLACE FUNCTION send_birthday_notifications() RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO email_queue (user_id, template, data)
  SELECT id, 'BIRTHDAY', jsonb_build_object('name', full_name, 'birthday', date_of_birth)
  FROM users
  WHERE EXTRACT(MONTH FROM date_of_birth) = EXTRACT(MONTH FROM now())
    AND EXTRACT(DAY FROM date_of_birth) = EXTRACT(DAY FROM now());
END;
$$;

SELECT cron.schedule('birthday-emails', '0 7 * * *', 'SELECT send_birthday_notifications()');
```

## 7. Scheduled Report Generation {#reports}

Heavy work → **`pgmq.send`** (worker consumes separately). **Monday 6 AM GMT**.

```sql
SELECT cron.schedule('weekly-report', '0 6 * * 1', $$
  SELECT pgmq.send(
    'report_jobs',
    jsonb_build_object(
      'type', 'WEEKLY_SUMMARY',
      'week', date_trunc('week', now() - interval '7 days'),
      'recipients', (SELECT array_agg(email) FROM users WHERE role = 'admin')
    )
  );
$$);
```

## 8. Database Health Monitoring {#health}

```sql
CREATE OR REPLACE FUNCTION log_db_health() RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  INSERT INTO db_health_log (checked_at, metric, value) VALUES
    (now(), 'table_count', (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public')),
    (now(), 'total_connections', (SELECT COUNT(*) FROM pg_stat_activity)),
    (now(), 'idle_connections', (SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'idle'));
END;
$$;

SELECT cron.schedule('db-health-check', '0 * * * *', 'SELECT log_db_health()');
```
