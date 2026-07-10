---
name: supabase-cron
description: >
  Generate Supabase Cron (pg_cron) jobs: SQL, DB functions, HTTP/pg_net (Edge Functions), queues.
  Use for recurring work in Postgres — cleanup, digests, sync, scheduled triggers. Covers syntax,
  Vault secrets, safety, and ops. Read this file first; patterns live in references/.
---

# Supabase Cron Skill

**Supabase Cron** = scheduled work in Postgres via `pg_cron` (link in **Official documentation**). Jobs: `cron.job`; runs: `cron.job_run_details`. Create via SQL or **Integrations → Cron**.

**Limits (Supabase):** at most **8 jobs running concurrently**; each job should finish within **10 minutes** — split with batches, queues, or Edge Functions if heavier (see **Official documentation** → Supabase Cron).

## Official documentation

Reference files point here instead of repeating URLs.

- **Supabase Cron:** https://supabase.com/docs/guides/cron
- **pg_cron (extension):** https://github.com/citusdata/pg_cron

---

## Flow

```
Need → 1 CLASSIFY → 2 SCHEDULE (GMT) → 3 COMMAND → 4 SAFETY → 5 REVIEW → 6 DELIVER SQL + verify
```

| # | Phase | Do |
|---|--------|-----|
| 1 | Classify | One primary path: SQL snippet vs `SELECT fn()` vs `pg_net` HTTP vs `pgmq.send` → worker (tree under **Phase 1**). |
| 2 | Schedule | Default **GMT**; 5-field cron or `'N seconds'` only if version allows → `references/syntax.md`. |
| 3 | Command | Bounded + idempotent; **`pg_net`**: always `timeout_milliseconds`; secrets → **Vault** only → `references/job-types.md`. |
| 4 | Safety | Concurrency/runtime caps; no casual `VACUUM` / `pg_terminate_backend` / long locks without explicit sign-off. |
| 5 | Review | Auto — no user confirm for routine jobs. **Block** on dangerous cluster ops or ambiguous multi-tenant effects. |
| 6 | Deliver | `cron.schedule` / `cron.unschedule`; one-line GMT meaning; verify via `references/management.md`. Migrations only if the repo already uses `supabase/migrations/`. |

---

## Phase 1 — Classify

```
SQL in DB?        → command = raw SQL / $$ … $$
Postgres fn?      → command = 'SELECT my_fn()' or CALL …
Edge / HTTP URL?  → command = $$ SELECT net.http_post(...) $$  (pg_net)
Background worker?  → SQL + pgmq.send (see Queues skill)
```

API shape (all variants): `SELECT cron.schedule('jobname', 'schedule', 'command');` — full SQL in **`references/job-types.md`** §1–4.

---

## Phase 5 — Review checklist

Confirm: (1) job type fits tree, (2) schedule + **GMT** stated, (3) no `auth.uid()` in cron unless intentional inside a locked-down `SECURITY DEFINER` path, (4) **no secret literals**, (5) **`pg_net`** enabled if HTTP used, (6) **`jobname`** unique (duplicates overwrite).

---

## Block rules

| # | Rule |
|---|------|
| **B1** | No plaintext service role / API keys — Vault or project secrets; placeholders only. |
| **B2** | No unbounded `DELETE`/`UPDATE` without windows/`LIMIT` unless user accepts full purge risk. |
| **B3** | Vague local time (“9 AM”) → **assume GMT** and state it. |
| **B4** | `'N seconds'` only after **`references/syntax.md`** version gate; else 5-field cron. |
| **B5** | `VACUUM` / terminate backends / heavy maintenance → stop, warn; prefer autovacuum / support. |

---

## References (patterns + recipes + ops)

| File | Use for |
|------|---------|
| `references/syntax.md` | Cron fields, GMT, `N seconds`, natural language, validation |
| `references/job-types.md` | **Canonical `cron.schedule` examples** — SQL, function, HTTP+Vault, queues |
| `references/use-case.md` | End-to-end recipes (digest, cleanup, sync, …) |
| `references/management.md` | List/pause/`unschedule`, `cron.job_run_details`, failures |

---

## Anti-patterns

| Never | Instead |
|-------|---------|
| Secret literals in SQL | Vault / secrets (`job-types.md`) |
| Unbounded DML on big tables | Windows, `LIMIT`, batches |
| Many heavy jobs same tick | Stagger; queue |
| `auth.uid()` in raw cron | No JWT in cron — Edge fn or guarded DB fn |
| Duplicate `jobname` | `unschedule` then `schedule` |
| `pg_net` without timeout | Always set `timeout_milliseconds` |
| Sub-minute schedule blind | Check `syntax.md` version |
| Casual `VACUUM` / backend kill | Autovacuum / support |
| “9 AM” without saying GMT | Label GMT; note local conversion |
| Long synchronous HTTP in cron | Edge + queue / chunk SQL |