# Migration Execution Reference

How to apply the generated SQL to the connected Supabase project using the existing project infrastructure.

---

## Project Infrastructure

The project already has a complete Supabase integration with these API endpoints and hooks:

### Backend Service
```
apps/backend/src/app/supabase/supabase.service.ts
  └── SupabaseOAuthService.runMigration(projectId, query)
  └── SupabaseOAuthService.listTables(projectId)
```

### API Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/integrations/supabase/projects/migrate` | Run SQL migration |
| GET | `/api/integrations/supabase/projects/:projectId/tables` | List tables |
| GET | `/api/integrations/supabase/projects/:projectId` | List available projects |

### Frontend Hooks
```
apps/frontend/src/hooks/supabase/useSupabaseMutations.ts
  └── useRunSupabaseMigrationMutation()

apps/frontend/src/services/supabaseService.ts
  └── SupabaseService.runMigration(body)
  └── SupabaseService.listTables(projectId)
```

---

## Step 1 — Confirm Prerequisites

Before running a migration, verify the user has:
1. Connected a Supabase account (OAuth completed)
2. Selected or created a Supabase project
3. The `projectId` (AppInvento project ID, not the Supabase project ref)

---

## Step 2 — Apply the Migration

### Option A: Via Frontend (using TanStack Query hook)

```typescript
import { useRunSupabaseMigrationMutation } from '@/hooks/supabase/useSupabaseMutations';

const { mutate, isPending, error } = useRunSupabaseMigrationMutation();

mutate(
  {
    projectId: 'your-appinvento-project-id',
    query: `
      -- Full DDL SQL here
      CREATE TABLE IF NOT EXISTS public.products (
        id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
        ...
      );
    `
  },
  {
    onSuccess: (data) => {
      console.log('Migration applied:', data.rows);
      // Then call listTables to verify
    },
    onError: (err) => {
      console.error('Migration failed:', err.message);
    }
  }
);
```

### Option B: Direct API Call

```bash
POST /api/integrations/supabase/projects/migrate
Content-Type: application/json
Authorization: Bearer <jwt-token>

{
  "projectId": "your-appinvento-project-id",
  "query": "CREATE TABLE IF NOT EXISTS public.products (...)"
}
```

Response:
```json
{ "rows": [] }
```
DDL statements (CREATE TABLE, ALTER TABLE, CREATE INDEX, etc.) return empty rows — this is correct.

### Option C: Backend Service Direct Call

```typescript
// In any NestJS service that injects SupabaseOAuthService
const result = await this.supabaseOAuthService.runMigration(projectId, sql);
```

---

## Step 3 — Verify Migration

After applying, confirm tables were created:

```typescript
// Frontend
const tables = await SupabaseService.listTables(projectId);
// Expect: tables.tables contains all tables you created
```

Or via API:
```bash
GET /api/integrations/supabase/projects/:projectId/tables
```

Response:
```json
{
  "tables": [
    { "name": "products", "schema": "public", "type": "BASE TABLE" },
    { "name": "categories", "schema": "public", "type": "BASE TABLE" }
  ]
}
```

If a table is missing from the response, the migration failed silently for that table. Check the SQL for syntax errors and re-run.

---

## Error Handling

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `relation already exists` | Table exists from prior run | Use `CREATE TABLE IF NOT EXISTS` |
| `type already exists` | Enum was already created | Use `DO $$ BEGIN CREATE TYPE... EXCEPTION WHEN duplicate_object THEN NULL; END $$` |
| `column ... does not exist` | ALTER TABLE on non-existent column | Check table structure first |
| `syntax error at or near` | SQL syntax error | Review the generated SQL |
| `permission denied` | RLS blocked the query | The migration runs as service_role — should bypass RLS |
| `No connected Supabase project` | User hasn't selected a project yet | User must connect Supabase first |
| `Supabase rejected the stored access token` | OAuth token expired | User must re-connect Supabase |

### Safe Migration Pattern

Always use idempotent SQL so migrations can be re-run without errors:

```sql
-- Tables
CREATE TABLE IF NOT EXISTS public.products (...);

-- Enums
DO $$ BEGIN
  CREATE TYPE public.product_status AS ENUM ('active', 'inactive');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- Indexes
CREATE INDEX IF NOT EXISTS products_user_id_idx ON public.products(user_id);

-- Triggers (use CREATE OR REPLACE)
CREATE OR REPLACE TRIGGER handle_updated_at ...

-- RLS policies (drop and recreate to avoid conflicts)
DROP POLICY IF EXISTS "products_select_own" ON public.products;
CREATE POLICY "products_select_own" ON public.products ...
```

---

## Large Migrations — Split Strategy

If the schema is large (10+ tables), split into logical groups and apply separately:

1. **Extensions + Enums** — run first
2. **Core entities** (no FK to other app tables) — e.g., categories, tags
3. **Dependent entities** (FK to core) — e.g., products, orders
4. **Junction tables** — e.g., product_tags, order_items
5. **RLS policies** — all policies last

Verify `listTables` after each group before proceeding.

---

## Rollback

The existing `runMigration` API runs arbitrary SQL, so rollback is also a SQL migration:

```sql
-- Rollback: drop tables in reverse dependency order
DROP TABLE IF EXISTS public.post_tags CASCADE;
DROP TABLE IF EXISTS public.products CASCADE;
DROP TABLE IF EXISTS public.categories CASCADE;
DROP TYPE IF EXISTS public.product_status;
```

Always confirm with user before running destructive rollback SQL.