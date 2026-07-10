# Workflow (ordered)

**Hard rules:** `../SKILL.md`. **This file:** step order + minimal snippets. Skip done work.

**Out:** `@supabase/ssr`, server `route.ts` auth callback, `middleware` auth. **Data tables:** **supabase-api-integration** (auth out of scope there). **Shared client:** if both skills → `auth:{…}` from Step 2 overrides **supabase-api-integration** Step 2 “no auth config” note.

---

## Step map

| # | Deliverable |
|---|-------------|
| 1 | Env + Supabase Auth URLs (`/auth/callback`, `/reset-password`) + Google provider if needed |
| 2 | `supabaseClient.ts` + `auth:{persistSession,autoRefreshToken,detectSessionInUrl}` |
| 3 | `Routes` + `AUTH_CALLBACK='/auth/callback'` |
| 4 | `authSchemas.ts` (yup + `translate`) |
| 5 | `AuthService` — `login-and-signup.md` · `google-oauth.md` · `phone-otp.md` (Phone: `signInWithOtp` + `verifyOtp` + disabled-provider fallback) · `password-reset.md` |
| 6 | `authKeys` |
| 7 | `useSession` · `useAuthMutations` · `use*Form` · `useAuth` — `session-and-guards.md` + login/google/phone/password refs |
| 8 | `AuthProvider` in `layout` inside `QueryProvider` |
| 9 | `PublicRoute` / `PrivateRoute` layouts |
| 10 | Pages table below |

---

## 1 — Env

`NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Dashboard redirect allow list includes every app origin + paths from Step 3.

---

## 2 — Client

```ts
cachedClient = createClient<Database>(url, anonKey, {
  auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
});
```

If file missing: create with **supabase-api-integration** `workflow.md` Steps 2–3 first.

---

## 3 — Routes

```ts
export enum Routes {
  HOME = '/',
  LANDING = '/landing',
  DASHBOARD = '/dashboard',
  LOGIN = '/login',
  REGISTER = '/register',
  FORGOT_PASSWORD = '/forgot-password',
  RESET_PASSWORD = '/reset-password',
  AUTH_CALLBACK = '/auth/callback',
}
```

No string paths in UI — only `Routes.*`.

---

## 4 — Schemas

Five schemas: login, register, forgot, reset, change-password — messages `translate('VALIDATION.*')`.

---

## 5–7 — Service · `authKeys` · hooks

**Service:** `login-and-signup.md` · `google-oauth.md` · `phone-otp.md` · `password-reset.md` — always `if (error) throw error`.

**`authKeys`:**

```ts
export const authKeys = {
  all: ['auth'] as const,
  session: () => [...authKeys.all, 'session'] as const,
  user: () => [...authKeys.all, 'user'] as const,
} as const;
```

**Hooks / forms / `useAuth`:** `session-and-guards.md` + same four feature refs.

---

## 8–9 — Provider · guards

Full `AuthProvider` + guard components: **`session-and-guards.md`**.

---

## 10 — Pages

| File | Notes |
|------|--------|
| `(auth)/login` | `login-and-signup.md` |
| `(auth)/register` | + verification empty-state |
| `(auth)/forgot-password` | `password-reset.md` |
| `(auth)/reset-password` | `PASSWORD_RECOVERY` listener |
| `(auth)/phone` | Single page, two-step (phone → OTP) — `phone-otp.md` (only when SMS OTP is required) |
| `app/auth/callback` | **Not** `(auth)/` — `google-oauth.md` |

UI: **components** + **translation** + **api-integration** `mutation-with-loader.md`.

---

## Error display pattern (single source)

Use this exact pattern in all auth pages/components/hooks:

```tsx
const { ERRORS } = useMultiLanguage();

try {
  await mutation.mutateAsync(payload);
} catch (error) {
  showErrorToast(
    error instanceof Error ? error.message : ERRORS.AUTHENTICATION_FAILED,
  );
}
```

Rules:

- Use `useMultiLanguage` for fallback keys; do not hardcode fallback strings.
- Do not call `translate()` directly in components/hooks.
- Keep original Supabase `error.message` when present.
- Use flow-specific fallback keys when needed (example: `ERRORS.GOOGLE_SIGN_IN_FAILED`, `ERRORS.GOOGLE_OAUTH_DISABLED`, `ERRORS.OTP_VERIFY_FAILED`, `AUTH.PHONE_PROVIDER_DISABLED`, `ERRORS.PASSWORD_UPDATE_FAILED`).

---

## Verify

- [ ] `if (error) throw error` on every `AuthService` auth call
- [ ] Callback = `app/auth/callback/page.tsx`
- [ ] `AuthProvider` = only global `getSession` / `onAuthStateChange` (+ reset-password narrow listener)
- [ ] `replace` + `${origin}${Routes.AUTH_CALLBACK}` for redirects
- [ ] Sign-out: `removeQueries(authKeys.all)` before `signOut()`
- [ ] No `middleware` / server PKCE route
