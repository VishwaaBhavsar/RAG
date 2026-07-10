# Row Level Security Patterns

All tables in the public schema MUST have RLS enabled. Enabled RLS with no policies = deny-all (breaks the app). Always add at least a SELECT policy.

---

## Non-Negotiable Rules

1. **Enable RLS on every table** — no exceptions
2. **Always use `(SELECT auth.uid())`** not `auth.uid()` in policies — prevents per-row re-evaluation
3. **SELECT needs USING only** — not WITH CHECK
4. **INSERT needs WITH CHECK only** — not USING
5. **UPDATE needs both USING and WITH CHECK** — and also requires a SELECT policy to work
6. **DELETE needs USING only** — not WITH CHECK
7. **Specify the role** — always `TO authenticated` or `TO anon`

---

## Pattern 1 — Owner-Only (Most Common)

User can only see and modify their own rows.

```sql
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "products_select_own" ON public.products
  FOR SELECT TO authenticated
  USING ((SELECT auth.uid()) = user_id);

CREATE POLICY "products_insert_own" ON public.products
  FOR INSERT TO authenticated
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "products_update_own" ON public.products
  FOR UPDATE TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "products_delete_own" ON public.products
  FOR DELETE TO authenticated
  USING ((SELECT auth.uid()) = user_id);
```

---

## Pattern 2 — Public Read, Owner Write

Anyone can read (e.g., blog posts, public profiles, product catalog). Only owner can write.

```sql
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Public read: anyone (including anon) can SELECT
CREATE POLICY "posts_select_public" ON public.posts
  FOR SELECT TO anon, authenticated
  USING (true);

-- Only owner can insert
CREATE POLICY "posts_insert_own" ON public.posts
  FOR INSERT TO authenticated
  WITH CHECK ((SELECT auth.uid()) = user_id);

-- Only owner can update
CREATE POLICY "posts_update_own" ON public.posts
  FOR UPDATE TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);

-- Only owner can delete
CREATE POLICY "posts_delete_own" ON public.posts
  FOR DELETE TO authenticated
  USING ((SELECT auth.uid()) = user_id);
```

---

## Pattern 3 — Published/Unpublished Content

Public can only see published content. Owner can see all their own content (including drafts).

**CRITICAL**: `posts_select_published` must include BOTH `anon` AND `authenticated`. Without it, authenticated users who don't own a post cannot see any published posts from other authors. Multiple SELECT policies are OR'd together in Postgres, so:
- Owner: matches `posts_select_own_all` → sees all own posts (draft + published)
- Non-owner authenticated: matches `posts_select_published` → sees only published posts
- Anon: matches `posts_select_published` → sees only published posts

```sql
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;

-- Owner sees all their own posts (published + draft)
CREATE POLICY "posts_select_own_all" ON public.posts
  FOR SELECT TO authenticated
  USING ((SELECT auth.uid()) = user_id);

-- Everyone (anon + authenticated non-owners) can see published posts
CREATE POLICY "posts_select_published" ON public.posts
  FOR SELECT TO anon, authenticated
  USING (status = 'published');

CREATE POLICY "posts_insert_own" ON public.posts
  FOR INSERT TO authenticated
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "posts_update_own" ON public.posts
  FOR UPDATE TO authenticated
  USING ((SELECT auth.uid()) = user_id)
  WITH CHECK ((SELECT auth.uid()) = user_id);

CREATE POLICY "posts_delete_own" ON public.posts
  FOR DELETE TO authenticated
  USING ((SELECT auth.uid()) = user_id);
```

---

## Pattern 4 — Workspace / Team Based

Rows are scoped to a workspace. Any member of the workspace can read. Only admins/owners can write.

```sql
ALTER TABLE public.projects ENABLE ROW LEVEL SECURITY;

-- Any workspace member can select
CREATE POLICY "projects_select_member" ON public.projects
  FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.workspace_members wm
      WHERE wm.workspace_id = projects.workspace_id
        AND wm.user_id = (SELECT auth.uid())
    )
  );

-- Any workspace member can insert
CREATE POLICY "projects_insert_member" ON public.projects
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.workspace_members wm
      WHERE wm.workspace_id = projects.workspace_id
        AND wm.user_id = (SELECT auth.uid())
    )
  );

-- Only admins/owners can update
CREATE POLICY "projects_update_admin" ON public.projects
  FOR UPDATE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.workspace_members wm
      WHERE wm.workspace_id = projects.workspace_id
        AND wm.user_id = (SELECT auth.uid())
        AND wm.role IN ('owner', 'admin')
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.workspace_members wm
      WHERE wm.workspace_id = projects.workspace_id
        AND wm.user_id = (SELECT auth.uid())
        AND wm.role IN ('owner', 'admin')
    )
  );

-- Only owners can delete
CREATE POLICY "projects_delete_owner" ON public.projects
  FOR DELETE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.workspace_members wm
      WHERE wm.workspace_id = projects.workspace_id
        AND wm.user_id = (SELECT auth.uid())
        AND wm.role = 'owner'
    )
  );
```

---

## Pattern 5 — Admin-Only Table (No User Access)

Internal table that only service role (backend) can access. Block all client access.

```sql
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

-- No policies = deny all client access
-- Only service_role (used by backend) bypasses RLS
-- This is correct and intentional — no policies needed
```

---

## Pattern 6 — Junction Table (Many-to-Many)

For tables like `post_tags`, `user_roles`, `product_categories`:

```sql
ALTER TABLE public.post_tags ENABLE ROW LEVEL SECURITY;

-- Read: anyone who can read the parent post can read its tags
CREATE POLICY "post_tags_select" ON public.post_tags
  FOR SELECT TO anon, authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.posts p
      WHERE p.id = post_tags.post_id
        AND (p.status = 'published' OR p.user_id = (SELECT auth.uid()))
    )
  );

-- Write: only the post owner can manage tags
CREATE POLICY "post_tags_insert_own" ON public.post_tags
  FOR INSERT TO authenticated
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM public.posts p
      WHERE p.id = post_tags.post_id
        AND p.user_id = (SELECT auth.uid())
    )
  );

CREATE POLICY "post_tags_delete_own" ON public.post_tags
  FOR DELETE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM public.posts p
      WHERE p.id = post_tags.post_id
        AND p.user_id = (SELECT auth.uid())
    )
  );
```

---

## Pattern 7 — No-Auth / Public App

Use this when the project has **no user authentication** (AUTH: NO). All operations are open to both anon and authenticated roles. No `user_id` column exists on the table.

```sql
ALTER TABLE public.todos ENABLE ROW LEVEL SECURITY;

-- Anyone (anon or authenticated) can read all rows
CREATE POLICY "todos_select_public" ON public.todos
  FOR SELECT TO anon, authenticated
  USING (true);

-- Anyone can insert
CREATE POLICY "todos_insert_public" ON public.todos
  FOR INSERT TO anon, authenticated
  WITH CHECK (true);

-- Anyone can update
CREATE POLICY "todos_update_public" ON public.todos
  FOR UPDATE TO anon, authenticated
  USING (true)
  WITH CHECK (true);

-- Anyone can delete
CREATE POLICY "todos_delete_public" ON public.todos
  FOR DELETE TO anon, authenticated
  USING (true);
```

**Rules for Pattern 7:**
- Always include all four operations (SELECT, INSERT, UPDATE, DELETE)
- Always specify `TO anon, authenticated` — never omit the role
- Never reference `auth.uid()` — there is no per-user context
- Seed data goes directly in the migration as INSERT statements (no auth.users trigger)

---

## RLS Decision Tree

```
Does the table have user-owned rows?
├── YES → Pattern 1 (owner-only) or Pattern 2 (public read)
│         └── Should unauthenticated users see any data?
│             ├── NO  → Pattern 1
│             └── YES → Pattern 2 (or Pattern 3 for published/draft)
└── NO → Does it belong to a workspace/team?
          ├── YES → Pattern 4 (workspace-based)
          └── NO  → Is it a junction/reference table?
                    ├── YES → Pattern 6 (inherit parent's access)
                    └── NO  → Is it backend-only?
                              ├── YES → Pattern 5 (no policies = deny all)
                              └── NO  → Ask user who should have access
```

---

## Performance Note

Always wrap auth functions in a subquery SELECT to prevent per-row evaluation:

```sql
-- ✅ Fast: auth.uid() evaluated once
USING ((SELECT auth.uid()) = user_id)

-- ❌ Slow at scale: auth.uid() evaluated for every row scanned
USING (auth.uid() = user_id)
```

This makes a significant difference on tables with thousands of rows.