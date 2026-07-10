# Cron Syntax Reference

Companion to `../SKILL.md` (B3–B4, Flow phase 2). **Sub-minute / `'N seconds'`:** confirm Postgres version in this file before relying on it. Official docs: `../SKILL.md` → **Official documentation**.

## Standard 5-field cron syntax

```
┌─────────── minute (0–59)
│ ┌───────── hour (0–23, GMT)
│ │ ┌─────── day of month (1–31)
│ │ │ ┌───── month (1–12)
│ │ │ │ ┌─── day of week (0–7, 0=Sun, 7=Sun)
│ │ │ │ │
* * * * *
```

## Common Patterns

| Schedule | Cron expression |
|----------|----------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every hour | `0 * * * *` |
| Every 4 hours | `0 */4 * * *` |
| Every day at midnight | `0 0 * * *` |
| Every day at 9 AM | `0 9 * * *` |
| Every Monday at 8 AM | `0 8 * * 1` |
| Every weekday at 6 PM | `0 18 * * 1-5` |
| Every Saturday at 3:30 AM | `30 3 * * 6` |
| First day of month at 2 AM | `0 2 1 * *` |
| Every 30 seconds | `30 seconds` |
| Every 10 seconds | `10 seconds` |

## Second-Level Precision (PG ≥ 15.1.1.61)

```sql
-- Every 30 seconds
SELECT cron.schedule('fast-job', '30 seconds', 'SELECT check_queue()');

-- Every 10 seconds
SELECT cron.schedule('very-fast', '10 seconds', 'SELECT heartbeat()');
```

## Natural Language (also supported)

```sql
-- These all work in Supabase Cron (Dashboard and SQL)
'every 5 minutes'
'every hour'
'every day at 3am'
'every monday at 9am'
```

## Timezone Handling

All cron schedules run in **GMT (UTC)**. Convert your desired local time:

| Your timezone | You want 9 AM local | Use GMT |
|--------------|--------------------|----|
| IST (UTC+5:30) | 9:00 AM IST | `30 3 * * *` (3:30 AM GMT) |
| EST (UTC-5) | 9:00 AM EST | `0 14 * * *` (2:00 PM GMT) |
| PST (UTC-8) | 9:00 AM PST | `0 17 * * *` (5:00 PM GMT) |

```sql
-- Example: Run at 9:00 AM IST every weekday
SELECT cron.schedule(
  'morning-digest-ist',
  '30 3 * * 1-5',  -- 3:30 AM GMT = 9:00 AM IST
  'SELECT send_morning_digest()'
);
```

## Verify your expression

Use https://crontab.guru to visually verify cron expressions before deploying.