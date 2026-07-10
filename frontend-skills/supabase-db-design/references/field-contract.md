# Field Contract Reference

The field contract is the mandatory bridge between frontend requirements and the database schema. It guarantees that no field the user interacts with is ever silently dropped from the database.

---

## Why This Exists

**The silent drop problem**: A frontend form collects `name`, `price`, `size`, `color`. The developer writes a schema with `name`, `price`, `color` — forgetting `size`. The form submits successfully (no error), but `size` is never stored. The user's data is silently lost on every save.

This happens because:
- SQL INSERT ignores unknown fields (no error thrown)
- The app appears to work during development
- The bug only surfaces when someone queries for size-based data that doesn't exist

**The field contract prevents this** by forcing an explicit mapping of every FE field before any SQL is written.

---

## Contract Table Format

For every entity/table, produce this table:

```
FIELD CONTRACT: products
─────────────────────────────────────────────────────────────────────────────
FE Field Name    │ FE Source               │ DB Column       │ DB Type      │ Status
─────────────────┼─────────────────────────┼─────────────────┼──────────────┼────────
name             │ form input (text)        │ name            │ text         │ ✅ MAPPED
price            │ form input (number)      │ price           │ numeric(10,2)│ ✅ MAPPED
size             │ form select (XS/S/M/L/XL)│ size            │ text+CHECK   │ ✅ MAPPED
color            │ form input (text)        │ color           │ text         │ ✅ MAPPED
category         │ dropdown (FK)            │ category_id     │ uuid         │ ✅ MAPPED
thumbnail        │ file upload              │ thumbnail_url   │ text         │ ✅ MAPPED
is_available     │ toggle/checkbox          │ is_available    │ boolean      │ ✅ MAPPED
description      │ textarea                 │ description     │ text         │ ✅ MAPPED
─────────────────┴─────────────────────────┴─────────────────┴──────────────┴────────
SYSTEM COLUMNS:
id               │ auto-generated           │ id              │ uuid         │ ✅ AUTO
user_id          │ auth.uid() on insert     │ user_id         │ uuid         │ ✅ AUTO
created_at       │ auto-generated           │ created_at      │ timestamptz  │ ✅ AUTO
updated_at       │ trigger-maintained       │ updated_at      │ timestamptz  │ ✅ AUTO
─────────────────────────────────────────────────────────────────────────────
COVERAGE: 8/8 FE fields mapped ✅
```

---

## Status Codes

| Status | Meaning | Action Required |
|--------|---------|-----------------|
| ✅ MAPPED | FE field has a matching DB column | None — proceed |
| ✅ AUTO | System column, not from FE input | None — auto-handled |
| ❌ UNMAPPED | FE field has NO DB column | **BLOCK** — must resolve before SQL |
| ⚠️ ORPHAN | DB column has no FE field | Ask if intentional — explain why |
| ⚠️ TYPE MISMATCH | FE sends string but DB column is integer | **BLOCK** — fix type before SQL |

---

## Validation Rules (apply before generating SQL)

### Rule 1 — Every FE field must be MAPPED or AUTO
```
FOR EACH field in frontend_fields:
  IF field.status == UNMAPPED:
    STOP — ask: "Where should [field] be stored? Add column or intentionally omit?"
```

### Rule 2 — DB column name must match FE field name exactly (unless explicitly aliased)
```
IF db_column_name != fe_field_name:
  BLOCK — show the mismatch in the contract table as ⚠️ NAME CHANGE
  Ask: "FE uses [fe_name] but I'm mapping to [db_name] because [reason]. Confirm?"
  Only proceed after user confirms the rename.

Examples of common valid aliases (must still be confirmed):
  - FE "thumbnail" (file upload) → DB "thumbnail_url" (adds _url suffix for clarity) ✅ acceptable
  - FE "is_published" (boolean) → DB "status" (text enum) ⚠️ NAME CHANGE — must confirm
  - FE "category" (dropdown) → DB "category_id" (adds _id suffix for FK) ✅ acceptable

Do NOT silently rename fe_field → different db column (e.g. "thumbnail_url" → "cover_image_url").
```

### Rule 3 — No extra DB columns without FE justification (ORPHAN BLOCK)
```
IF db_column has no corresponding FE field:
  BLOCK — do NOT add the column without asking
  Show it as ⚠️ ORPHAN in the contract table
  Ask: "I see no FE field for [column]. Is this intentional (e.g. admin-only, server-computed)?"
  Only add it after user confirms with a reason.

This applies to ALL columns — even "obviously useful" ones like excerpt, description, notes.
Never assume a column is needed. Only add what the FE explicitly collects or displays.
```

### Rule 4 — FK dropdowns must store the ID, not the label
```
IF fe_field is a dropdown/select that references another entity:
  DB column = [entity]_id (uuid FK) NOT the display name
  Example: "category" dropdown → category_id uuid REFERENCES categories(id)
```

### Rule 5 — File upload fields store the path/URL, not the file
```
IF fe_field is a file upload:
  DB column = [fe_field_name]_url (text) — keep FE field name as base, append _url
  Store the Supabase Storage object path
  Example: FE "thumbnail" → DB "thumbnail_url" (NOT "cover_image_url" or "image_path")
```

### Rule 6 — Multi-select fields need special handling
```
IF fe_field is multi-select or tags:
  OPTION A: text[] array column (simple, no relations needed)
  OPTION B: junction table (if you need to query/filter by selection)
  Ask user which is needed based on their query requirements
```

### Rule 7 — Computed/derived fields
```
IF fe_field is computed from other fields (e.g. slug from title):
  INCLUDE as DB column (store computed value, don't re-derive)
  Add trigger or note that app must compute before insert
```

### Rule 8 — Display-only fields from joins
```
IF fe_field shows related data (e.g. "author name" on a post):
  NOT a column on this table — it comes from JOIN
  Mark as ✅ JOINED: author_name comes from users.name via user_id FK
```

---

## Extracting Fields from Frontend Code

When reading existing frontend files, look for these patterns:

### React Hook Form
```typescript
// Every register() call is a field
const { register } = useForm();
<input {...register("name")} />       // → field: name
<input {...register("price")} />      // → field: price
<input {...register("size")} />       // → field: size  ← don't miss this!
```

### Zod Schema
```typescript
const schema = z.object({
  name: z.string(),       // → field: name
  price: z.number(),      // → field: price
  size: z.string(),       // → field: size  ← match this to DB column
  color: z.string(),      // → field: color
});
```

### TypeScript Interface/Type
```typescript
interface ProductFormData {
  name: string;       // → field: name
  price: number;      // → field: price
  size: string;       // → field: size
  color: string;      // → field: color
}
```

### API Request Body
```typescript
await api.post('/products', {
  name: form.name,
  price: form.price,
  size: form.size,    // → field: size — DB must have this column
  color: form.color,
});
```

### Display Template
```tsx
// Fields accessed in templates are read from DB — they must exist
<p>{product.name}</p>
<p>{product.price}</p>
<p>{product.size}</p>   // → if this renders, DB must have size column
<p>{product.color}</p>
```

---

## Common Mistakes to Catch

| Mistake | Example | Detection |
|---------|---------|-----------|
| Missing select field | FE has `size` select, DB has no `size` column | Contract shows ❌ UNMAPPED |
| Storing label not ID | FE sends `category: "Electronics"`, DB has `category text` | Should be `category_id uuid` |
| Missing boolean | FE has `is_featured` toggle, DB has no column | Contract shows ❌ UNMAPPED |
| Missing optional field | FE has optional `discount_price`, dev skips it "for now" | Must be in DB even if nullable |
| Wrong numeric type | FE sends `4.99`, DB column is `integer` | Contract shows ⚠️ TYPE MISMATCH |
| Forgot array field | FE has multi-tag selector, DB has no `tags` column | Contract shows ❌ UNMAPPED |

---

## Sign-off Checklist

Before writing SQL, verify:

- [ ] All FE form inputs have a DB column
- [ ] All FE display fields either have a DB column or are marked as JOINED
- [ ] All FE filter/sort fields have a DB column AND an index
- [ ] All FK dropdowns store the `_id` UUID, not the display label
- [ ] All file upload fields use the FE field name as base + `_url` suffix (e.g. `thumbnail_url`)
- [ ] All multi-select fields have either `text[]` or a junction table
- [ ] No UNMAPPED or TYPE MISMATCH statuses remain
- [ ] Every DB column name matches the FE field name exactly (or rename is confirmed by user)
- [ ] Zero orphan columns — every DB column traces to a FE field or an explicit user approval
- [ ] No "bonus" columns added without user request (excerpt, description, notes, etc.)