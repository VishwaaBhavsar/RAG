# Producers — Sending Messages to Queues

## Table of Contents
1. [Send from client JS (pgmq_public)](#client-js)
2. [Send from server/Edge Function (pgmq)](#server)
3. [Send on DB trigger (automatic enqueue)](#trigger)
4. [Batch send](#batch)
5. [Delayed / scheduled send](#delayed)

---

## 1. Send from Client JS via pgmq_public {#client-js}

Requires PostgREST exposure enabled + RLS on `pgmq.q_*` + grants — **`references/rls-patterns.md`**. **Browser client:** `getSupabaseClient()` / **`../../supabase-api-integration/references/workflow.md`** Step 2.

```ts
// const supabase = getSupabaseClient()

// Single message
const { data: msgId, error } = await supabase
  .schema('pgmq_public')
  .rpc('send', {
    queue_name: 'notifications',
    message: {
      userId: 'user-123',
      type: 'NEW_MESSAGE',
      payload: { from: 'Alice', text: 'Hey!' }
    },
    sleep_seconds: 0 // available immediately
  })
```

---

## 2. Send from Server / Edge Function {#server}

Use `service_role` key for unrestricted access to `pgmq` schema directly. **Client wiring:** **`../../supabase-api-integration/references/workflow.md`** → **Edge Functions (Deno)** — do not duplicate `createClient` / import lines here.

```ts
// supabase/functions/enqueue-welcome/index.ts
Deno.serve(async (req) => {
  const { userId, email } = await req.json()

  const { data } = await supabase.rpc('pgmq_send', {
    queue_name: 'email_jobs',
    msg: { to: email, template: 'welcome', userId }
  })

  return new Response(JSON.stringify({ messageId: data }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

---

## 3. Auto-Enqueue on DB Trigger {#trigger}

Automatically enqueue a job whenever a row is inserted/updated.

```sql
-- Function: enqueue a welcome email whenever a new user is created
CREATE OR REPLACE FUNCTION enqueue_welcome_email()
RETURNS TRIGGER AS $$
BEGIN
  PERFORM pgmq.send(
    'email_jobs',
    jsonb_build_object(
      'to',       NEW.email,
      'subject',  'Welcome to our app!',
      'template', 'welcome',
      'userId',   NEW.id
    )
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger on user creation
CREATE TRIGGER on_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION enqueue_welcome_email();
```

---

## 4. Batch Send {#batch}

```sql
-- Send multiple messages at once
SELECT pgmq.send_batch(
  'notifications',
  ARRAY[
    '{"userId":"1","type":"REMINDER"}'::jsonb,
    '{"userId":"2","type":"REMINDER"}'::jsonb,
    '{"userId":"3","type":"REMINDER"}'::jsonb
  ]
);
```

```ts
// JS batch via pgmq_public
const { data } = await supabase
  .schema('pgmq_public')
  .rpc('send_batch', {
    queue_name: 'notifications',
    messages: [
      { userId: '1', type: 'REMINDER' },
      { userId: '2', type: 'REMINDER' }
    ]
  })
```

---

## 5. Delayed / Scheduled Send {#delayed}

```sql
-- Send a message that becomes visible in 1 hour
SELECT pgmq.send(
  'email_jobs',
  '{"to":"user@example.com","template":"follow_up"}',
  delay := 3600  -- seconds
);
```

```ts
// JS: delay 30 minutes
await supabase.schema('pgmq_public').rpc('send', {
  queue_name: 'email_jobs',
  message: { to: 'user@example.com', template: 'follow_up' },
  sleep_seconds: 1800 // 30 minutes
})
```

**Use case:** Send a "you left items in your cart" email 30 minutes after abandonment.
If the user checks out before 30 minutes, delete the message from the queue.