# Column Types Reference

Mapping from frontend input types and data concepts to the correct PostgreSQL/Supabase column type.

---

## Core Type Decision Table

| Frontend Input / Data Concept | PostgreSQL Type | Notes |
|-------------------------------|-----------------|-------|
| Short text (name, title, label) | `text` | Never `varchar(n)` |
| Long text (description, body, notes) | `text` | Same type, no limit needed |
| Email address | `text` | Add CHECK if strict validation needed |
| Phone number | `text` | Store as-is, formatting is FE concern |
| URL / slug / path | `text` | Add UNIQUE if needed |
| Integer count (qty, views, retries) | `integer` | Range: -2B to +2B |
| Large integer (user count, IDs from external) | `bigint` | Range: -9 quintillion to +9 quintillion |
| Small integer (rating 1-5, month 1-12) | `smallint` | Range: -32768 to 32767 |
| Price / money / financial amount | `numeric(10,2)` | NEVER float/real — rounding errors |
| Percentage (0.00 to 100.00) | `numeric(5,2)` | |
| Latitude / Longitude | `numeric(9,6)` | 6 decimal places = ~0.1m precision |
| True/false toggle or checkbox | `boolean` | DEFAULT false NOT NULL |
| Date only (birthday, due date) | `date` | No time component |
| Date + time | `timestamptz` | Always timezone-aware |
| Duration in seconds | `integer` | Store seconds, format in FE |
| File upload (image, document, video) | `text` | Store Supabase Storage path/URL |
| Color picker | `text` | Store hex string (#RRGGBB) |
| Fixed dropdown (status, role, type) | `text` + CHECK | Or enum if values never change |
| FK to another table (relation) | `uuid REFERENCES` | Store the ID, NOT the display label |
| Multi-select / tags (simple) | `text[]` | Array of strings |
| Multi-select / tags (with relations) | Junction table | Separate table with two FK columns |
| JSON / dynamic object | `jsonb` | Only for truly variable structure |
| JSON array of objects | `jsonb` | E.g., line items on an order |
| IP address | `inet` | PostgreSQL native IP type |
| UUID string from external system | `text` | Don't use uuid type if format varies |
| Order / sort position | `integer` | For manual drag-and-drop ordering |

---

## Money / Numeric Precision

**Always use `numeric` for money, never `float` or `real`:**

```sql
-- ✅ Correct — exact decimal storage
price           numeric(10,2),   -- up to 99,999,999.99
discount_amount numeric(10,2),
tax_rate        numeric(5,4),    -- e.g. 0.0825 = 8.25%

-- ❌ Wrong — floating point rounding errors will corrupt financial data
price    float,
price    real,
price    double precision
```

`numeric(precision, scale)`:
- `precision` = total significant digits
- `scale` = digits after decimal point
- `numeric(10,2)` = up to 8 digits before decimal, 2 after → max 99,999,999.99

---

## Text vs VARCHAR

**Always use `text`. Never use `varchar(n)` unless the length limit is a real business constraint:**

```sql
-- ✅ Correct
name        text NOT NULL,
email       text NOT NULL,
description text,

-- ❌ Avoid — arbitrary limits cause truncation bugs and migrations later
name        varchar(255),
email       varchar(100),
```

PostgreSQL stores `text` and `varchar` identically. The only benefit of `varchar(n)` is enforcing a real constraint (e.g., a country code must be exactly 2 chars: `char(2)`).

---

## Enums vs Text + CHECK

**Use `text` + CHECK for most "status" / "type" fields:**

```sql
-- ✅ Preferred — easy to add new values later
status text CHECK (status IN ('draft', 'published', 'archived')) DEFAULT 'draft' NOT NULL,
role   text CHECK (role IN ('owner', 'admin', 'member', 'viewer')) DEFAULT 'member' NOT NULL,
```

**Use PostgreSQL ENUM only when:**
- Values are truly fixed and will never need removal
- Performance of joins matters (enum compresses better)

```sql
-- ✅ OK for truly stable enums
CREATE TYPE public.payment_method AS ENUM ('card', 'bank_transfer', 'crypto');

-- ⚠️ Remember: you can ADD enum values but CANNOT remove them
ALTER TYPE public.payment_method ADD VALUE 'paypal';
-- ALTER TYPE ... DROP VALUE doesn't exist — you'd need to recreate the type
```

**Never use enum for values that might expand or be user-defined.**

---

## Arrays

For multi-select fields where relations don't matter:

```sql
-- Simple string tags
tags        text[]    DEFAULT '{}' NOT NULL,

-- Multiple file URLs
image_urls  text[]    DEFAULT '{}' NOT NULL,

-- Querying arrays
SELECT * FROM products WHERE 'red' = ANY(tags);
SELECT * FROM products WHERE tags @> ARRAY['red', 'large'];  -- contains both
```

**Use junction table instead when:**
- You need to query all products with a tag AND all tags for a product efficiently
- You need metadata on the relationship (e.g., display order, added_by)
- The related items are first-class entities (e.g., user-created tags with descriptions)

---

## JSONB

Use `jsonb` for truly variable or unknown structure:

```sql
-- ✅ Good uses for jsonb
webhook_payload  jsonb,                     -- external API response, unknown shape
metadata         jsonb DEFAULT '{}',        -- extensible extra attributes
settings         jsonb DEFAULT '{}',        -- user preferences, key-value
line_items       jsonb DEFAULT '[]',        -- embedded sub-objects (denormalized)

-- ❌ Bad uses for jsonb — use proper columns instead
-- jsonb for: name, price, color — these are known structured fields
```

Querying jsonb:
```sql
SELECT * FROM orders WHERE metadata->>'source' = 'mobile';
SELECT * FROM orders WHERE (metadata->>'amount')::numeric > 100;
```

---

## Boolean Columns

```sql
-- Always NOT NULL with DEFAULT false (or true if semantically appropriate)
is_available   boolean DEFAULT true  NOT NULL,
is_featured    boolean DEFAULT false NOT NULL,
is_verified    boolean DEFAULT false NOT NULL,
email_verified boolean DEFAULT false NOT NULL,
```

Never store booleans as `text` ('yes'/'no'), `integer` (0/1), or nullable boolean.

---

## Timestamps

```sql
-- ✅ Always use timestamptz
published_at  timestamptz,              -- nullable: NULL means not yet published
expires_at    timestamptz,              -- nullable: NULL means no expiry
scheduled_at  timestamptz NOT NULL,

-- ❌ Never use timestamp (no timezone = UTC assumption = timezone bugs)
published_at  timestamp,
```

Storing current time:
```sql
DEFAULT now()          -- equivalent to CURRENT_TIMESTAMP
```

---

## File/Image Storage

When frontend has file upload, store the Supabase Storage path:

```sql
-- Store the storage path (not the full URL — URLs can change if bucket/domain changes)
avatar_path     text,    -- e.g. "avatars/user-uuid/profile.jpg"
thumbnail_path  text,    -- e.g. "products/product-uuid/thumb.jpg"
document_path   text,    -- e.g. "documents/user-uuid/contract.pdf"

-- OR store the full public URL if bucket is public and URL is stable
avatar_url      text,
thumbnail_url   text,
```

---

## Foreign Keys

For every FK reference:

```sql
-- Reference to auth.users (Supabase managed)
user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,

-- Reference to your own tables
category_id uuid REFERENCES public.categories(id) ON DELETE SET NULL,
parent_id   uuid REFERENCES public.comments(id)   ON DELETE CASCADE,

-- ON DELETE behavior decision:
-- CASCADE   → delete child when parent deleted (e.g. user's posts deleted when user deleted)
-- SET NULL  → keep child, nullify FK (e.g. keep product when category deleted)
-- RESTRICT  → block parent delete if children exist (use sparingly — causes confusing errors)
-- SET DEFAULT → set FK to default value (rare)
```

---

## Indexes

See `references/schema-conventions.md` — Indexes section for the canonical rules.

**Summary**: Every table gets exactly **1 default index** (`user_id` for user-owned, `created_at DESC` for public). Never add composite indexes, never index booleans/enums/status columns, never add a second index unless the requirement explicitly calls for it. Index naming: `idx_[table]_[col]`.