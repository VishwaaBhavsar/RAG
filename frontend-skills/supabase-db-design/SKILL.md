---
name: supabase-db-design
description: Designs Supabase PostgreSQL database schemas from user requirements. Enforces a strict frontend-to-database field contract so no form field is ever silently dropped from the schema. Generates DDL SQL with RLS policies, indexes, and triggers, then writes the migration file to supabase/migrations/.
---

# Supabase DB Design Skill

Design and apply Supabase database schemas that perfectly match what the frontend collects and displays. The #1 rule: **every frontend field must have a DB column — no silent drops**.

---

## Flow

```
User Requirement (natural language OR existing FE code path)
        │
        ▼
┌─────────────────────────┐
│  1. EXTRACT FE FIELDS   │  ← Read all fields from forms, displays, filters
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  2. BUILD FIELD         │  ← Map every FE field → DB column, flag unmapped
│     CONTRACT TABLE      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  3. DESIGN SCHEMA       │  ← Tables, types, constraints, relationships
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  4. GENERATE SQL        │  ← Full DDL: tables, RLS, indexes, triggers
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  5. REVIEW (auto)       │  ← Log contract + summary, no user confirmation
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  6. WRITE MIGRATION     │  ← Write SQL to supabase/migrations/<ts>_<name>.sql
└─────────────────────────┘
```

---

## Phase 1 — Extract Frontend Fields

**Two entry points:**

### A. User describes requirements in natural language
Extract every field the user mentions the frontend will collect, display, filter, or sort. Include:
- Form inputs (text, number, select, checkbox, date, file)
- Display fields shown in lists/cards/detail pages
- Filter/sort fields
- Computed-but-stored fields (e.g. slug derived from title)

### B. Existing frontend code exists
Read the relevant frontend files to extract fields:
```
- Forms: look for name="...", register("..."), field.name, zodSchema fields
- API calls: look at request body shape sent to backend
- Types/interfaces: look at TypeScript types the component uses
- Display: look at what fields are accessed (e.g. product.size, order.status)
```

**Document every field found. Miss nothing.**

### C. Identify seed data (mandatory for all entry points)

Seed data must always be identified — either by scanning existing files or by inferring from the requirement.

**If existing frontend code is present** — scan for hardcoded data:
- Arrays of objects: `const tasks = [{ id: 1, title: '...', ... }]`
- `mockData`, `INITIAL_DATA`, `DEFAULT_ITEMS`, `SAMPLE_*` constants
- Data files: `data.ts`, `constants.ts`, `mock.ts`, `fixtures.ts`
- Inline JSX rendering fixed items from a hardcoded array
- Extract every row found → use as seed data in the migration

**If NO frontend code exists yet (fresh generation)** — infer seed data from the requirement:
- For every non-user-owned table: generate 4–6 realistic sample rows matching the app domain (e.g. for a recipe app → 5 sample recipes; for an e-commerce app → 6 sample categories + 8–10 products)
- For every user-owned table with an auth flow: generate 3–5 representative sample rows that will be seeded per-user via the `auth.users` trigger (e.g. for a todo app → 3 sample todos covering different priorities)
- Use realistic, domain-appropriate content — not "Sample Item 1", "Test Row 2"

**Document in Migration Summary:**
- Source: `[file path + variable name]` if scanned, or `[inferred from requirement]` if fresh generation
- Row count per table

---

## Phase 2 — Build the Field Contract Table

Before writing any SQL, produce this table for every entity:

```
FIELD CONTRACT: [EntityName]
─────────────────────────────────────────────────────────────────────
FE Field Name    │ Source          │ DB Column       │ Type     │ Status
─────────────────┼─────────────────┼─────────────────┼──────────┼────────
name             │ form input      │ name            │ text     │ ✅ MAPPED
price            │ form input      │ price           │ numeric  │ ✅ MAPPED
size             │ form select     │ size            │ text     │ ✅ MAPPED
color            │ form input      │ color           │ text     │ ✅ MAPPED
category_id      │ dropdown (FK)   │ category_id     │ uuid     │ ✅ MAPPED
thumbnail_url    │ file upload     │ thumbnail_url   │ text     │ ✅ MAPPED
─────────────────────────────────────────────────────────────────────
SYSTEM COLUMNS (auto-managed, not from FE):
id               │ auto            │ id              │ uuid     │ ✅ AUTO
created_at       │ auto            │ created_at      │ timestamptz│ ✅ AUTO
updated_at       │ auto            │ updated_at      │ timestamptz│ ✅ AUTO
user_id          │ auth.uid()      │ user_id         │ uuid     │ ✅ AUTO
─────────────────────────────────────────────────────────────────────
```

**BLOCK RULE 1 — Unmapped FE fields**: If any FE field shows ❌ UNMAPPED — stop, resolve it before generating SQL.

**BLOCK RULE 2 — Orphan DB columns**: If you plan a DB column that has no corresponding FE field — stop, show it as ⚠️ ORPHAN, and ask the user whether to include it. Do NOT silently add "bonus" columns like `excerpt`, `description`, `notes`, or `metadata` just because they seem useful. Only add what the FE explicitly collects or displays.

**BLOCK RULE 3 — Column name mismatch**: If a DB column name differs from the FE field name (beyond acceptable suffixes like `_id` for FK or `_url` for file uploads) — flag it as ⚠️ NAME CHANGE and confirm with the user before generating SQL. Never silently rename `thumbnail_url` → `cover_image_url` or `is_published` → `status`.

---

## Phase 3 — Design Schema

### Auth Context Decision (resolve this FIRST — it changes everything)

Check the instructions you received for the AUTH flag:

| Flag | user_id column | RLS pattern | Seed data |
|------|---------------|-------------|-----------|
| **AUTH: YES** | Add `user_id uuid REFERENCES auth.users(id) NOT NULL` to user-owned tables | Pattern 1 (owner-only) | Via auth.users trigger |
| **AUTH: NO** | **DO NOT add user_id to any table** | Pattern 7 (public full access — see rls-patterns.md) | Direct INSERT statements |

**If AUTH: NO — these are absolute rules, no exceptions:**
- No `user_id` column anywhere
- No policies that reference `auth.uid()`
- No `auth.users` triggers for seed data
- Every table gets Pattern 7 RLS (full anon + authenticated read/write)
- All seed data goes directly in the migration as INSERT statements

Apply rules from `references/schema-conventions.md`:
- UUID primary keys using `gen_random_uuid()`
- `created_at` and `updated_at` on every table
- `user_id uuid REFERENCES auth.users(id)` for ownership — **only when AUTH: YES**
- Snake_case column names matching the FE field names (or explicit aliases)
- Correct type mapping (see `references/column-types.md`)
- RLS plan per table (see `references/rls-patterns.md`)
- Indexes: **always add exactly 1 default index per table** (`user_id` for user-owned tables, `created_at DESC` for public tables). Only add more if the requirement explicitly mentions filtering or sorting on a specific high-cardinality column. Never index booleans, enums, status fields, composite columns, or UNIQUE columns. See `references/schema-conventions.md` Indexes section.
- Relationships via FK with explicit ON DELETE behavior (see `references/relationship-patterns.md`)

### Type Mapping from FE Input Type → DB Column Type

| FE Input / Data               | DB Type          | Notes                              |
|-------------------------------|------------------|------------------------------------|
| text input                    | `text`           | Never use `varchar(n)` unless constraint is real |
| number (integer, count, qty)  | `integer`        |                                    |
| number (price, amount, weight)| `numeric(10,2)`  | Never use float for money          |
| boolean / checkbox            | `boolean`        | Default `false`                    |
| date only                     | `date`           |                                    |
| datetime / timestamp          | `timestamptz`    | Always timezone-aware              |
| select (fixed options)        | `text` + CHECK   | Or custom enum if values are stable|
| multi-select / tags           | `text[]`         | Or junction table if relations matter |
| file upload URL               | `text`           | Store Supabase Storage path        |
| JSON / dynamic object         | `jsonb`          | Only for truly variable structure  |
| FK reference to another table | `uuid REFERENCES`|                                    |
| email                         | `text`           | Add CHECK (email ~* '^[^@]+@[^@]+$') |
| phone                         | `text`           |                                    |
| slug / URL-safe string        | `text UNIQUE`    |                                    |
| color hex                     | `text`           | Add CHECK (color ~* '^#[0-9a-f]{6}$') if needed |
| rating / score                | `smallint`       | Add CHECK (rating BETWEEN 1 AND 5) |
| large text / description      | `text`           |                                    |

---

## Phase 4 — Generate SQL

### File naming

Save the migration at:
```
supabase/migrations/<YYYYMMDDHHmmss>_<snake_case_description>.sql
```

Example: `supabase/migrations/20260505123051_create_blog_schema.sql`

Use the current UTC timestamp for `<YYYYMMDDHHmmss>`. The description should be lowercase snake_case (e.g. `create_products_schema`, `add_orders_table`).

### SQL structure

Follow the **bolt.new migration format**. Produce a single SQL file in this exact structure:

```sql
/*
  # <Feature Name> Schema

  1. New Tables
    - `table_name` - brief description (key columns)
    - `table_name` - brief description

  2. Security
    - RLS enabled on all tables
    - brief description of access patterns
*/

-- Enum (only when values are stable — skip for dynamic values, use text+CHECK instead)
-- Wrap in DO block so migration is idempotent (safe to re-run)
DO $$ BEGIN
  CREATE TYPE [enum_name] AS ENUM ('value1', 'value2', 'value3');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

-- [Table description]
CREATE TABLE IF NOT EXISTS [table_name] (
  id            uuid         PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid         REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  category_id   uuid         REFERENCES categories(id) ON DELETE SET NULL,

  name          text         NOT NULL,
  price         numeric(10,2) NOT NULL,
  thumbnail_url text,
  is_featured   boolean      DEFAULT false NOT NULL,

  created_at    timestamptz  DEFAULT now(),
  updated_at    timestamptz  DEFAULT now()
);

ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;

-- For user-owned tables (has user_id): always use owner-only SELECT (Pattern 1)
-- For public/shared tables (no user_id, e.g. categories, tags): use USING (true) TO anon, authenticated
CREATE POLICY "Users can read own [table_name]"
  ON [table_name] FOR SELECT
  TO authenticated
  USING ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can insert own [table_name]"
  ON [table_name] FOR INSERT
  TO authenticated
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can update own [table_name]"
  ON [table_name] FOR UPDATE
  TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "Users can delete own [table_name]"
  ON [table_name] FOR DELETE
  TO authenticated
  USING ((SELECT auth.uid()) = user_id);

-- Default index (1 per table — more only if requirement explicitly needs it)
CREATE INDEX IF NOT EXISTS idx_[table]_created_at ON [table_name] (created_at DESC);

-- updated_at trigger — ALWAYS name the function handle_updated_at(), NEVER moddatetime()
-- (moddatetime conflicts with the Supabase built-in extension of the same name)
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON [table_name];
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON [table_name]
  FOR EACH ROW
  EXECUTE FUNCTION handle_updated_at();

-- Seed data (only when requirement implies demo or initial lookup data)
INSERT INTO [table_name] (col1, col2) VALUES
  ('value1', 'value2')
ON CONFLICT (slug) DO NOTHING;
```

### Seed Data (Static → Dynamic Migration)

**Rule: if Phase 1C found static/hardcoded data, it MUST appear as INSERT statements in this migration.**

This is the handoff from static to dynamic: after the migration runs, the frontend reads from the DB — the hardcoded array is no longer the source of truth.

**Pattern A — tables with a `slug` or other UNIQUE column (preferred):**
```sql
-- Seed [table_name] — migrated from static frontend data
INSERT INTO [table_name] (col1, col2, col3) VALUES
  ('value1', 'value2', 'value3'),
  ('value4', 'value5', 'value6')
ON CONFLICT (slug) DO NOTHING;
```

**Pattern B — tables without a UNIQUE column (use WHERE NOT EXISTS per row):**
```sql
INSERT INTO [table_name] (col1, col2, col3)
SELECT 'value1', 'value2', 'value3'
WHERE NOT EXISTS (SELECT 1 FROM [table_name] WHERE col1 = 'value1');
```

**Pattern C — user-owned tables (todos, notes, items owned by auth.uid()):**
User-owned rows **cannot** be seeded in a migration (no `auth.uid()` available at migration time). Always apply this pattern — whether seed rows came from scanning existing files or were inferred from the requirement. What to do depends on whether the project has auth:

- **Project has signup/signin flow** → seed at runtime on first signup. After a new user is created, insert the default rows for that user. Implement this as a Supabase Database Function triggered on `auth.users` insert:
```sql
-- Seed default [table_name] rows for every new user
CREATE OR REPLACE FUNCTION public.seed_default_[table_name]_for_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.[table_name] (user_id, col1, col2, col3) VALUES
    (NEW.id, 'value1', 'value2', 'value3'),
    (NEW.id, 'value4', 'value5', 'value6');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created_seed_[table_name]
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.seed_default_[table_name]_for_new_user();
```
  Add this trigger function to the **same migration file**, after the table DDL and policies. Document in the Migration Summary as: `Static data: user-owned — seeded via auth.users trigger on signup`

- **Project has NO signup/signin flow** → skip entirely. Do NOT add a trigger, do NOT attempt to seed user-owned data. Document in the Migration Summary as: `Static data: user-owned — skipped (no auth flow in project)`

**Seed data rules:**
- Always place seed INSERTs at the bottom of the migration, after all DDL and policies
- Always use `ON CONFLICT ... DO NOTHING` or `WHERE NOT EXISTS` — migrations must be idempotent
- Seed all rows from the static frontend source — do not trim or sample
- If an image URL is referenced in the static data, keep it as-is (do not change URLs)
- Add a comment `-- Seed [entity] — migrated from static frontend data` above each seed block

**Format rules (bolt.new style):**
- Start with `/* # Title \n\n 1. New Tables \n 2. Security */` block comment header
- Policy names are human-readable double-quoted strings: `"Anyone can read products"`, `"Users can insert own orders"`
- Write CREATE POLICY directly — no DO blocks around policies
- No `public.` schema prefix — Supabase sets `search_path = public`
- No `CREATE EXTENSION` — Supabase projects have all required extensions pre-installed
- One short `-- comment` above each table, no section banners (`-- ===...===`, `-- ---...---`)

**Code rules:**
- Every column from the Field Contract Table must appear in the DDL
- Tables use `CREATE TABLE IF NOT EXISTS`
- Enums: wrap in a DO block for idempotency so the migration can be safely re-run:
  ```sql
  DO $$ BEGIN
    CREATE TYPE [enum_name] AS ENUM ('value1', 'value2');
  EXCEPTION WHEN duplicate_object THEN NULL;
  END $$;
  ```
- Always `(SELECT auth.uid())` not `auth.uid()` in policies (performance)
- Always specify `TO anon, authenticated` or `TO authenticated` on every policy — never omit the role

---

## Phase 5 — Review (automated — no user confirmation needed)

Log the following before writing the file:

1. **Field Contract Table** (Phase 2 output) — confirm all fields mapped
2. **Migration Summary**:

```
MIGRATION SUMMARY
─────────────────────────────────────
Tables to create:    [list]
Enums to create:     [list]
Indexes to add:      [count]
RLS policies:        [count]
─────────────────────────────────────
FE fields covered:   [n/n] ✅
Orphan DB columns:   [n] ⚠️
─────────────────────────────────────
Static data found:   [yes/no]
  Source:            [file path + variable name, or "none"]
  Non-user-owned:    [seeded directly in migration — n rows]
  User-owned:        [trigger on auth.users (has auth) | skipped (no auth)]
─────────────────────────────────────
```

Do NOT ask the user for confirmation — proceed directly to Phase 6.

---

## Phase 6 — Write Migration File

Write the generated SQL to the project's `supabase/migrations/` directory.

### Steps

1. Get the current UTC timestamp:
   ```bash
   date -u +%Y%m%d%H%M%S
   ```

2. Create the directory if it does not exist:
   ```bash
   mkdir -p supabase/migrations
   ```

3. Write the complete DDL SQL using the Write tool to:
   ```
   supabase/migrations/<YYYYMMDDHHmmss>_<snake_case_description>.sql
   ```
   Example: `supabase/migrations/20260506143022_create_blog_schema.sql`

4. Log: "Migration written to supabase/migrations/<filename>.sql"

**Do NOT** apply the migration to any live database. File creation is the only output of this phase.

---

## References

| File | Topic |
|------|-------|
| `references/schema-conventions.md` | Naming, UUID, timestamps, column ordering |
| `references/column-types.md` | FE input type → PostgreSQL type mapping |
| `references/rls-patterns.md` | All RLS policy patterns (owner, public, team, admin) |
| `references/relationship-patterns.md` | FKs, junction tables, self-referential, cascade rules |
| `references/field-contract.md` | Field contract rules and validation checklist |
| `references/migration-execution.md` | API endpoints, hooks, error handling |

---

## Anti-Patterns — Never Do These

| Anti-pattern | Why | Instead |
|---|---|---|
| DB column not in Field Contract | FE field silently dropped, data lost | Map every FE field first |
| Adding "bonus" columns not in FE | Orphan columns cause confusion, unmaintained | Only add what FE explicitly collects |
| Silently renaming FE field → different DB column | API breaks (e.g. `thumbnail_url` sent but DB has `cover_image_url`) | Keep names aligned or confirm rename |
| `posts_select_published TO anon` only | Authenticated non-owners can't see published posts | Include `authenticated` too: `TO anon, authenticated` |
| `varchar(255)` | Arbitrary limit, no benefit in Postgres | Use `text` |
| `float` / `real` for money | Floating point rounding errors | Use `numeric(10,2)` |
| `timestamp` (no tz) | Timezone bugs | Use `timestamptz` |
| No RLS | Any anon key can read/write all data | Always enable RLS |
| RLS without policies | Enables RLS = deny-all (breaks the app) | Always add at least SELECT policy |
| `auth.uid()` in policy without SELECT | Evaluated per-row, slow at scale | Use `(SELECT auth.uid())` |
| Enum for dynamic values | Can't remove enum values safely | Use `text` + CHECK constraint |
| Adding any index by default | Wastes space, slows writes — indexes must be earned | Default is zero indexes; only add when requirement explicitly needs it |
| Static frontend data not seeded | Frontend stays hardcoded, DB is empty, dynamic fetch returns nothing | Scan for static arrays in Phase 1C and seed them in the migration |
| Seeding user-owned rows directly in migration | No `auth.uid()` at migration time — INSERT will fail | If project has auth: add an `auth.users` trigger in the same migration. If no auth: skip entirely |
| Seed without idempotency guard | Re-running migration creates duplicate rows | Always use `ON CONFLICT DO NOTHING` or `WHERE NOT EXISTS` |
| Index on boolean / flag column | Only 2 values — Postgres seq scans faster | Never index `is_completed`, `is_active`, `is_featured` |
| Composite index `(user_id, anything)` | Rarely needed; plain `user_id` index covers most cases | Never add composite indexes unless requirement explicitly demands it |
| Index on every FK column | Wastes space; rarely-queried FKs don't benefit | Only index FKs actually used in WHERE/JOIN per the requirement |
| Index on UNIQUE column | UNIQUE already creates an implicit index | Remove the redundant CREATE INDEX |
| Index on low-cardinality enum/status | Postgres ignores it, does seq scan instead | Skip `status`, `priority`, `role` columns entirely |
| `ON DELETE RESTRICT` by default | Prevents deletes, causes confusing errors | Choose cascade or set-null explicitly |
| `USING (true)` SELECT on user-owned table | Exposes every user's rows to all authenticated users | Use `USING ((SELECT auth.uid()) = user_id)` for any table with a `user_id` column |
| Adding `user_id` when AUTH: NO | Column references auth.users which has no rows — INSERTs fail, anon users are blocked | When AUTH: NO, omit user_id entirely and use Pattern 7 (public full access) |
| `supabase.auth.getUser()` in frontend hook when AUTH: NO | Returns null — throws "Not authenticated" — nothing works | When AUTH: NO, remove all auth checks from hooks; the anon key handles access |
| auth.users seed trigger when AUTH: NO | Trigger never fires (no users sign up) — data never seeded | When AUTH: NO, seed directly with INSERT statements in the migration |
| `CREATE FUNCTION moddatetime()` | Conflicts with Supabase's built-in `moddatetime` extension, causing confusing behavior | Always name the updated_at trigger function `handle_updated_at()` |
| Providing `id` in seed INSERTs | Hardcoded UUIDs cause conflicts on re-run and look ugly in the DB | Omit `id` — `DEFAULT gen_random_uuid()` generates it automatically |