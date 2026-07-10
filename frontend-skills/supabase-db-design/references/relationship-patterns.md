# Relationship Patterns

How to model common data relationships in Supabase PostgreSQL.

---

## One-to-Many (Most Common)

One user has many products. One category has many posts.

```sql
-- Parent table
CREATE TABLE IF NOT EXISTS public.categories (
  id         uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id    uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name       text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Child table — FK points to parent
CREATE TABLE IF NOT EXISTS public.products (
  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id     uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  category_id uuid REFERENCES public.categories(id) ON DELETE SET NULL,  -- keep product if category deleted
  name        text NOT NULL,
  price       numeric(10,2) NOT NULL,
  created_at  timestamptz DEFAULT now() NOT NULL,
  updated_at  timestamptz DEFAULT now() NOT NULL
);

-- Always index the FK column on the child
CREATE INDEX products_category_id_idx ON public.products(category_id);
```

### ON DELETE behavior choice:
| Behavior | When to use |
|----------|------------|
| `CASCADE` | Deleting parent should delete children (e.g. user deleted → delete their posts) |
| `SET NULL` | Keep child but clear the reference (e.g. delete category → keep products, category_id = NULL) |
| `RESTRICT` | Block parent delete if children exist — use sparingly, causes confusing errors |
| `SET DEFAULT` | Rare — set FK to a default "uncategorized" ID |

---

## Many-to-Many (Junction Table)

Posts can have many tags. Tags can belong to many posts.

```sql
-- Entity A
CREATE TABLE IF NOT EXISTS public.tags (
  id         uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id    uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  name       text NOT NULL,
  slug       text NOT NULL UNIQUE,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

-- Entity B (already exists: posts)

-- Junction table
CREATE TABLE IF NOT EXISTS public.post_tags (
  post_id    uuid REFERENCES public.posts(id) ON DELETE CASCADE NOT NULL,
  tag_id     uuid REFERENCES public.tags(id)  ON DELETE CASCADE NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  PRIMARY KEY (post_id, tag_id)  -- composite PK prevents duplicates
);

-- Indexes both FKs (composite PK already covers post_id; add tag_id for reverse lookup)
CREATE INDEX post_tags_tag_id_idx ON public.post_tags(tag_id);
```

**No `id` column on junction table** — composite primary key is the right approach here.

---

## Self-Referential (Nested / Hierarchical)

Comments with replies. Categories with subcategories. Org chart.

```sql
CREATE TABLE IF NOT EXISTS public.comments (
  id         uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id    uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  post_id    uuid REFERENCES public.posts(id) ON DELETE CASCADE NOT NULL,
  -- Self-reference: NULL = top-level comment, UUID = reply to parent
  parent_id  uuid REFERENCES public.comments(id) ON DELETE CASCADE,
  content    text NOT NULL,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);

CREATE INDEX comments_post_id_idx    ON public.comments(post_id);
CREATE INDEX comments_parent_id_idx  ON public.comments(parent_id);
CREATE INDEX comments_user_id_idx    ON public.comments(user_id);
```

Query top-level comments and their replies:
```sql
-- Top-level comments for a post
SELECT * FROM public.comments WHERE post_id = $1 AND parent_id IS NULL ORDER BY created_at;

-- Replies to a comment
SELECT * FROM public.comments WHERE parent_id = $1 ORDER BY created_at;
```

---

## One-to-One (Profile Pattern)

A user has exactly one profile. Reference `auth.users` from a `profiles` table.

```sql
CREATE TABLE IF NOT EXISTS public.profiles (
  -- id = auth.users.id — same UUID, not generated separately
  id         uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name text,
  last_name  text,
  bio        text,
  avatar_url text,
  created_at timestamptz DEFAULT now() NOT NULL,
  updated_at timestamptz DEFAULT now() NOT NULL
);
```

Auto-create profile on user signup via trigger:
```sql
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id)
  VALUES (new.id);
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

## Relationship Checklist

Before finalizing the schema:

- [ ] Every FK column has a corresponding index
- [ ] ON DELETE behavior is explicitly chosen (not accidentally RESTRICT)
- [ ] Junction tables have composite PK (not separate `id`)
- [ ] Self-referential columns are nullable (top-level rows have NULL parent)
- [ ] Parent tables are created before child tables in the SQL (or use deferred constraints)
- [ ] One-to-one relationships use the parent's ID as the child's PK

---

## Foreign Key Order in SQL

Parent tables must be defined BEFORE child tables that reference them.

```sql
-- ✅ Correct order
CREATE TABLE public.categories (...);   -- parent
CREATE TABLE public.products (...);     -- child references categories

-- ❌ Wrong order — FK reference will fail
CREATE TABLE public.products (...    category_id REFERENCES public.categories(id) ...);
CREATE TABLE public.categories (...);   -- categories doesn't exist yet!
```

When in doubt, structure SQL in this order:
1. Lookup / reference tables (no FKs)
2. Core entities (FK to auth.users only)
3. Child entities (FK to core entities)
4. Junction tables (FK to both sides)