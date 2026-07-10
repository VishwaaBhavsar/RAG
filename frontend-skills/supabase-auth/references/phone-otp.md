# Phone OTP (SMS sign-in / sign-up)

**Scope:** Browser `signInWithOtp` + `verifyOtp` on one page — not WhatsApp, voice OTP, MFA, or native SMS retriever APIs.

Auto sign-up is on by default (`shouldCreateUser: true`): one flow for new and returning numbers. No separate phone-signup page.

---

## Flow (5 steps, single page `/phone`)

1. User enters E.164 phone (`+<country><number>`) → `signInWithOtp({ phone, options: { shouldCreateUser: true } })` → Supabase sends SMS via the dashboard-configured provider.
2. UI switches to OTP on the **same page** (no route change). 6-digit code arrives.
3. User enters code → `verifyOtp({ phone, token, type: 'sms' })`.
4. On success, Supabase returns `{ session, user }` synchronously → `onAuthStateChange` → cache updates via `AuthProvider`.
5. `replace(Routes.DASHBOARD)`.

No `redirectTo` or `?code=` exchange — phone OTP never leaves the app (no auth callback page).

---

## Service · hook

```ts
import { getSupabaseClient } from '@/lib/supabase/supabaseClient';
import type { AuthResponse } from '@supabase/supabase-js';

export type RequestPhoneOtpInput = { phone: string };
export type VerifyPhoneOtpInput = { phone: string; token: string };

// AuthService
static async signInWithPhoneOtp(input: RequestPhoneOtpInput): Promise<void> {
  const { error } = await getSupabaseClient().auth.signInWithOtp({
    phone: input.phone,
    options: { shouldCreateUser: true },
  });
  if (error) throw error;
}

static async verifyPhoneOtp(
  input: VerifyPhoneOtpInput,
): Promise<AuthResponse['data']> {
  const { data, error } = await getSupabaseClient().auth.verifyOtp({
    phone: input.phone,
    token: input.token,
    type: 'sms',
  });
  if (error) throw error;
  return data;
}
```

```ts
import { useMutation } from '@tanstack/react-query';
import { queryClient } from '@/lib/query/queryClient';
import {
  AuthService,
  type RequestPhoneOtpInput,
  type VerifyPhoneOtpInput,
} from '@/services/authService';
import { authKeys } from './queryKeys';
import type { AuthResponse } from '@supabase/supabase-js';

type AuthData = AuthResponse['data'];

export function useRequestPhoneOtpMutation() {
  return useMutation<void, Error, RequestPhoneOtpInput>({
    mutationFn: AuthService.signInWithPhoneOtp,
  });
}

export function useVerifyPhoneOtpMutation() {
  return useMutation<AuthData, Error, VerifyPhoneOtpInput>({
    mutationFn: AuthService.verifyPhoneOtp,
    onSuccess: (d) => {
      queryClient.setQueryData(authKeys.session(), d.session);
      queryClient.setQueryData(authKeys.user(), d.user);
    },
  });
}
```

`phone` MUST be E.164 (e.g. `+14155552671`). `verifyOtp` returns a session synchronously on success (unlike OAuth). `AuthProvider` `onAuthStateChange` still fires — mutation `onSuccess` is optimistic UX only.

Request/verify error handling: follow the **single-source pattern** in `workflow.md` → **Error display pattern (single source)**. In the phone-page **`catch`**, if the error indicates Phone provider is disabled (`Unsupported phone provider`, `phone_provider_disabled`, etc.), open **`PhoneProviderDisabledDialog`** (next section) — never the raw Supabase string or a full-page JSON error. Use `ERRORS.OTP_VERIFY_FAILED` as verify-step fallback key.

`isPending` on both steps (no double-submit; Supabase rate-limits `signInWithOtp`). On verify success, `router.replace(Routes.DASHBOARD)`.

---

## Phone page

**Path:** `apps/frontend/src/app/(auth)/phone/page.tsx`. `Routes.PHONE_LOGIN = '/phone'`.

Two-step UI on one page: phone input → OTP. Forms/schemas: same **yup** + `translate('VALIDATION.*')` pattern as `login-and-signup.md` (E.164 phone; 6-digit OTP). Optional `usePhoneOtpForm` for `step` + separate `phoneForm` / `otpForm`.

Use `InputOTP` from `components/ui/InputOtp.tsx`. Mask the number on the OTP step; **Change number** resets OTP and returns to step 1. Optional **Resend code** only with client throttle ≥ 30s; surface Supabase rate-limit errors verbatim — do **not** auto-retry. Optional auto-submit when 6 digits are entered.

---

## Disabled provider · `PhoneProviderDisabledDialog`

Without a UI **`catch`**, a disabled Phone provider surfaces **`Unsupported phone provider`** (or similar). **`PhoneProviderDisabledDialog`** replaces that with setup guidance.

**Dialog:** `AlertDialog`; i18n body mirrors **Where to configure** (enable Phone in Supabase, pick SMS provider, add valid credentials, OTP length 6, smoke-test a real number). Optional dashboard link from `NEXT_PUBLIC_SUPABASE_URL` → `https://supabase.com/dashboard/project/<ref>/auth/providers`.

**Phone page / button:** `try { await requestOtp.mutateAsync(…); } catch` → disabled-provider → `setDialogOpen(true)`; else toast per **`workflow.md`**. Raise `AlertDialog` z-index above Sonner if toasts are used.

---

## Where to configure

| Layer | Action |
|--------|--------|
| **Supabase Dashboard** | Auth → Providers → Phone → enable. Choose SMS provider (Twilio, MessageBird, Vonage, Textlocal, etc.) and fill its API credentials. Set OTP length to 6, expiry ≤ 600s. Auth → URLs: no extra entries needed for phone OTP. |
| **SMS provider** | Provision sender ID / Twilio number. Verify country-code restrictions (Twilio Geo Permissions). Smoke-test with one real number before shipping. |

---

## Optional

**Phone change for existing email user:** `updateUser({ phone })` then `verifyOtp({ phone, token, type: 'phone_change' })`.

**Login page link:** `<Link href={Routes.PHONE_LOGIN}>` next to the Google button on `(auth)/login/page.tsx`.

Add fallback keys via **translation** skill, e.g. `AUTH.PHONE_PROVIDER_DISABLED` (dialog title/body), `ERRORS.OTP_VERIFY_FAILED`, and `VALIDATION.PHONE_*` / `VALIDATION.OTP_*`.
