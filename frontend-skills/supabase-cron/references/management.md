# Cron Management — Ops

**Authoritative guardrails:** `../SKILL.md` (anti-patterns, B1–B5, phase 6). **Schedule / GMT:** `syntax.md`. **Job shapes:** `job-types.md`. **Recipes:** `use-case.md`. Official docs: `../SKILL.md` → **Official documentation**.

---

## Lifecycle

- **Create:** `SELECT cron.schedule('jobname', 'schedule', 'command');` — returns job id.
- **Name:** unique, case-sensitive; **duplicate name overwrites** silently.
- **Change command/schedule:** `SELECT cron.unschedule('jobname');` then `schedule` again (name not truly editable).
- **By id:** `SELECT cron.unschedule(42);`
- **Pause / resume:** `UPDATE cron.job SET active = false WHERE jobname = 'x';` — `true` to resume.

```sql
SELECT cron.unschedule('old-job');
SELECT cron.schedule('old-job', '0 */2 * * *', 'SELECT updated_function()');
```

---

## Inventory

```sql
SELECT jobid, jobname, schedule, command, active FROM cron.job ORDER BY jobname;
```

---

## Run history (`cron.job_run_details`)

Template: join `cron.job` for `jobname`, filter/order as needed.

```sql
SELECT j.jobname, jrd.status, jrd.return_message, jrd.start_time, jrd.end_time,
       EXTRACT(EPOCH FROM (jrd.end_time - jrd.start_time)) AS duration_s
FROM cron.job_run_details jrd
JOIN cron.job j ON j.jobid = jrd.jobid
WHERE j.jobname = 'my-job'
ORDER BY jrd.start_time DESC
LIMIT 20;
```

**Variants (same join, adjust `WHERE`):** `jrd.status = 'failed' AND jrd.start_time > now() - interval '24 hours'` — last failures; `… start_time > now() - interval '7 days'` + `GROUP BY j.jobname` + `AVG(duration_s)` — regression check.

---

## Optional: alert on failure

Requires `system_alerts` (or swap table). Fires on each `job_run_details` insert.

```sql
CREATE OR REPLACE FUNCTION alert_on_cron_failure() RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  IF NEW.status = 'failed' THEN
    INSERT INTO system_alerts (type, message, created_at)
    VALUES ('CRON_FAILURE', format('job %s: %s', NEW.jobid, NEW.return_message), now());
  END IF;
  RETURN NEW;
END; $$;
CREATE TRIGGER cron_failure_alert AFTER INSERT ON cron.job_run_details
  FOR EACH ROW EXECUTE FUNCTION alert_on_cron_failure();
```

---

## Dashboard

**Integrations → Cron:** create job (natural language + SQL / function / HTTP), per-job **History**, **Active** toggle.

---

## Ops-only pitfalls

| Symptom | Check |
|---------|--------|
| Never runs | `cron.job.active`, schedule typo, job exists |
| “Wrong time” | GMT vs local — **`syntax.md`** / **`../SKILL.md` B3** |
| HTTP hangs / 5xx | `timeout_milliseconds`, Edge logs; heavy work → queue (**`job-types.md`** §4) |
| Silent overwrite | Duplicate `jobname` — **`../SKILL.md`** anti-patterns |
