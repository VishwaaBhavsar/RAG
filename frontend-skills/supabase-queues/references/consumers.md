# Consumers — Reading and Processing Messages

**RLS + client reads:** `rls-patterns.md`. **Producers:** `producers.md`. **Recipes:** `use-case.md`. Official docs: `../SKILL.md` → **Official documentation** (Queues API).

**Patterns:** `read(q, vt, qty)` hides rows for `vt` seconds → **`delete`** (gone) or **`archive`** (moves to `pgmq.a_<q>`). **`pop`** = read+delete atomically (no VT retry). **VT** must exceed worst-case handler time (`../SKILL.md` B2).

---

## SQL (`pgmq` schema)

Replace `my_queue` with your queue name.

```sql
-- Read + delete (at-most-once after success)
SELECT * FROM pgmq.read('my_queue', 30, 5);
SELECT pgmq.delete('my_queue', <msg_id>);

-- Read + archive (audit trail)
SELECT * FROM pgmq.read('my_queue', 60, 1);
SELECT pgmq.archive('my_queue', <msg_id>);
-- SELECT * FROM pgmq.a_my_queue ORDER BY archived_at DESC LIMIT 50;

-- Pop (idempotent work only — no automatic retry)
SELECT * FROM pgmq.pop('my_queue');
```

**`pgmq_public` (Data API / supabase-js):** Supabase wraps queue ops in **`pgmq_public`** (not raw `pgmq`) when **Expose Queues via PostgREST** is on — Quickstart + Queues API in `../SKILL.md` → **Official documentation**. RPC names match SQL intent; **`read`** args per docs are **`queue_name`**, **`sleep_seconds`** (visibility timeout), **`n`** (batch size).

---

## Edge worker (skeleton)

**`service_role`** + **`pgmq_public`** RPCs (requires **Expose Queues via PostgREST** in project settings). Loop: `read` → handle `msg.message` json → `archive` or `delete`; on throw, skip ack so the message becomes visible again after the visibility window. Alternative: run **`pgmq.*` SQL** via a direct Postgres client (pooler) if you intentionally keep the Data API path off.

Instantiate **`createClient` from `@supabase/supabase-js`** once per **`../../supabase-api-integration/references/workflow.md`** → **Edge Functions (Deno)** (`SUPABASE_SERVICE_ROLE_KEY`). Do not duplicate import/env wiring in queue reference docs.

```ts
Deno.serve(async () => {
  const { data: rows, error } = await supabase.schema('pgmq_public').rpc('read', {
    queue_name: 'my_queue',
    sleep_seconds: 90,
    n: 10,
  })
  if (error) return new Response(error.message, { status: 500 })

  for (const msg of rows ?? []) {
    try {
      await processPayload(msg.message) // your I/O
      await supabase.schema('pgmq_public').rpc('archive', {
        queue_name: 'my_queue',
        message_id: msg.msg_id,
      })
    } catch {
      /* omit archive/delete → retry after vt */
    }
  }
  return new Response('ok')
})

async function processPayload(_payload: unknown) {
  /* implement */
}
```

---

## Polling + backoff (optional)

If empty queue: sleep and increase delay (cap e.g. 30s); reset delay when messages arrive.

```ts
let delayMs = 1000
while (true) {
  const { data } = await supabase.schema('pgmq_public').rpc('read', {
    queue_name: 'my_queue',
    sleep_seconds: 60,
    n: 5,
  })
  if (!data?.length) {
    await new Promise((r) => setTimeout(r, delayMs))
    delayMs = Math.min(delayMs * 2, 30_000)
  } else {
    delayMs = 1000
    /* process + ack */
  }
}
```

---

## Retry cap + DLQ

`read_ct` increases each time a message is read. If `read_ct > N`, **`send`** payload to `<queue>_dead` (or similar) + **`archive`** original so it stops retrying.

```sql
SELECT pgmq.create('my_queue_dead');
-- SELECT msg_id, message FROM pgmq.q_my_queue_dead ORDER BY enqueued_at DESC LIMIT 50;
```

```ts
const MAX = 3
for (const msg of rows ?? []) {
  if (msg.read_ct > MAX) {
    await supabase.schema('pgmq_public').rpc('send', {
      queue_name: 'my_queue_dead',
      message: { ...msg.message, _from: msg.msg_id },
    })
    await supabase.schema('pgmq_public').rpc('archive', {
      queue_name: 'my_queue',
      message_id: msg.msg_id,
    })
    continue
  }
  try {
    await processPayload(msg.message)
    await supabase.schema('pgmq_public').rpc('archive', {
      queue_name: 'my_queue',
      message_id: msg.msg_id,
    })
  } catch { /* rely on VT */ }
}
```

Monitor DLQ depth in app metrics or a scheduled check — no need for trigger boilerplate unless you require DB-side alerts.
