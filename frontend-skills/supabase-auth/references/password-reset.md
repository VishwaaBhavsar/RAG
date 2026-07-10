# Password reset & change

**Rules:** `../SKILL.md`. Mutations UX: **api-integration** `mutation-with-loader.md`.

---

## Flows

| Flow | UI | Service |
|------|-----|-----------|
| **Forgot** | `(auth)/forgot-password` | `resetPasswordForEmail(email, { redirectTo: origin+RESET_PASSWORD })` |
| **Reset** | `(auth)/reset-password` | After `PASSWORD_RECOVERY` event → `updateUser({ password })` |
| **Change** | settings (logged in) | `signInWithPassword` (current) then `updateUser({ password })` — no `verifyPassword` in Supabase |

Forgot: **same success UI** whether email exists (anti-enumeration).

---

## `AuthService` additions

```ts
static async resetPasswordForEmail(email: string): Promise<void> {
  const { error } = await getSupabaseClient().auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}${Routes.RESET_PASSWORD}`,
  });
  if (error) throw error;
}

static async updatePassword(newPassword: string): Promise<void> {
  const { error } = await getSupabaseClient().auth.updateUser({ password: newPassword });
  if (error) throw error;
}

static async changePassword(input: {
  email: string;
  currentPassword: string;
  newPassword: string;
}): Promise<void> {
  const { error: e1 } = await getSupabaseClient().auth.signInWithPassword({
    email: input.email,
    password: input.currentPassword,
  });
  if (e1) throw e1;
  const { error } = await getSupabaseClient().auth.updateUser({ password: input.newPassword });
  if (error) throw error;
}
```

`RESET_PASSWORD` path on Supabase redirect allow list.

---

## Mutations

```ts
useMutation<void, Error, { email: string }>({ mutationFn: ({ email }) => AuthService.resetPasswordForEmail(email) });
useMutation<void, Error, { newPassword: string }>({ mutationFn: ({ newPassword }) => AuthService.updatePassword(newPassword) });
useMutation<void, Error, { email: string; currentPassword: string; newPassword: string }>({
  mutationFn: AuthService.changePassword,
});
```

---

## Reset page (narrow listener)

`getSupabaseClient().auth.onAuthStateChange` in **one** `useEffect` on reset page only — `if (event === 'PASSWORD_RECOVERY') setReady(true)`; unsubscribe on unmount. Timeout → invalid link UI if never ready.

Submit → `updatePassword` → toast → `replace(LOGIN)` (fresh session). On catch, use the **single-source pattern** in `workflow.md` → **Error display pattern (single source)** with `ERRORS.PASSWORD_UPDATE_FAILED`.

---

## Forgot / change pages

- **Forgot:** email field · `try/catch` · on success always show “check email” (same copy for unknown email).
- **Change:** `useChangePasswordForm` · `user.email` + current + new · `useChangePasswordMutation` · show original error on catch with `useMultiLanguage` fallback key.

Full JSX patterns: same as login (`login-and-signup.md`) — `PasswordInput` × n + `ButtonWithLoader`.

---

## Notes

- Server password policy: Supabase dashboard + mirror in yup.
- Add fallback keys via **translation** skill: `ERRORS.PASSWORD_UPDATE_FAILED` (and any flow-specific variants you use).
