# Google OAuth (browser PKCE)

**Scope:** Browser PKCE only — not One-Tap, native Google SDKs, or `signInWithIdToken`.

## Layout

| Concern | Path |
|--------|------|
| Client + `detectSessionInUrl` | `lib/supabase/supabaseClient.ts` |
| Disabled OAuth detection + redirect helper | `lib/supabase/googleAuthErrors.ts` |
| `signInWithOAuth` orchestration | `services/authService.ts` |
| Google mutation | `hooks/auth/useAuthMutations.ts` — colocate `useGoogleSignInMutation` with other auth mutations |
| Button | `components/auth/GoogleSignInButton.tsx` |
| Post-OAuth / email `?code=` | `app/auth/callback/page.tsx` · `Routes.AUTH_CALLBACK = '/auth/callback'` |

---

## Flow (end-to-end)

1. `signInWithOAuth({ provider: 'google', options: { skipBrowserRedirect: true, redirectTo, … } })` → `{ data, error }` only (no browser navigation).
2. **Errors:** if **`isSupabaseGoogleProviderDisabledError(error)`** → `throw new SupabaseGoogleProviderDisabledError()`; else rethrow.
3. **URL:** if `data.url` exists → **`await continueGoogleOAuthFromAuthorizeUrl(data.url)`** (never `assign(data.url)` alone). Preflight with `skip_http_redirect=true`, `fetch` + `redirect: 'manual'` + anon headers; on 4xx/5xx or readable disabled JSON → throw disabled; on 2xx/3xx proving Google → `assign` external URL; on CORS/opaque probe → fall back to `assign(data.url)` so enabled Google still works.
4. Google → Supabase `…/auth/v1/callback` → your `redirectTo` with `?code=` (or OAuth error query/hash) → callback page → `useSession` → `replace(DASHBOARD|LOGIN)`.

Same `?code=` path for **email verification** links.

---

## `AuthService` · mutation

```ts
import { getSupabaseClient } from '@/lib/supabase/supabaseClient';
import { Routes } from '@/constants/routes';
import {
  continueGoogleOAuthFromAuthorizeUrl,
  isSupabaseGoogleProviderDisabledError,
  SupabaseGoogleProviderDisabledError,
} from '@/lib/supabase/googleAuthErrors';

// AuthService — only place that calls signInWithOAuth for Google
static async signInWithGoogle(): Promise<void> {
  const { data, error } = await getSupabaseClient().auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}${Routes.AUTH_CALLBACK}`,
      skipBrowserRedirect: true,
    },
  });
  if (error) {
    if (isSupabaseGoogleProviderDisabledError(error)) {
      throw new SupabaseGoogleProviderDisabledError();
    }
    throw error;
  }
  if (!data.url) {
    throw new Error('Google sign-in did not return a redirect URL.');
  }
  await continueGoogleOAuthFromAuthorizeUrl(data.url);
}
```

```ts
import { useMutation } from '@tanstack/react-query';
import { AuthService } from '@/services/authService';

export function useGoogleSignInMutation() {
  return useMutation<void, Error, void>({ mutationFn: () => AuthService.signInWithGoogle() });
}
```

Button: `isPending` before redirect; no mutation `onSuccess`. On **`SupabaseGoogleProviderDisabledError`**, show **`ERRORS.GOOGLE_OAUTH_DISABLED`** via i18n — not raw Supabase strings. Other failures: **`ERRORS.GOOGLE_SIGN_IN_FAILED`**. `GoogleIcon`: `components/icons/` if missing.

---

## `lib/supabase/googleAuthErrors.ts` — OAuth disabled (one module)

**Goal:** centralize **(a)** classifying provider-off failures and **(b)** browser redirection to the OAuth URL returned by Supabase without exposing raw `/auth/v1/authorize` JSON to the user.

**Classification — one public check, no duplication:**

- **`AuthService` and UI only call `isSupabaseGoogleProviderDisabledError(error)`** — never re-check `error.message`, field names, or substring lists outside this file.
- Implement that function **inside `googleAuthErrors.ts` only** (private normalizer + provider-disabled rules). Supabase errors vary by shape and often embed JSON in a single string, so **static checks on named fields alone are brittle**; keep all parsing and matching in this module — do not copy logic into `AuthService` or UI.

**Exports (stable surface):**

| Export | Role |
|--------|------|
| `isSupabaseGoogleProviderDisabledError` | `true` when the error means OAuth provider disabled / unsupported / misconfigured |
| `SupabaseGoogleProviderDisabledError` | Domain error for Google UI branch; message: `Google OAuth is disabled. Please enable it in Supabase with valid credentials.` |
| `continueGoogleOAuthFromAuthorizeUrl(url: string): Promise<void>` | Preflight authorize URL (`skip_http_redirect=true`, `fetch`, `redirect: 'manual'`, anon headers). Throw disabled on 4xx/5xx or provider-off body; `assign` Google URL on success; on inconclusive probe, `assign(url)`. Also classify disabled in `signInWithOAuth` `error` and on callback query/hash params. |

**UI:** catch `SupabaseGoogleProviderDisabledError` once → toast / alert / `AlertDialog` with **`ERRORS.GOOGLE_OAUTH_DISABLED`** only — no raw Supabase strings, no auto-retry.

---

## Callback page

**Path:** `apps/frontend/src/app/auth/callback/page.tsx` — outside `(auth)/`.

```tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from '@/hooks/auth/useSession';
import { Routes } from '@/constants/routes';
import useMultiLanguage from '@/hooks/useMultiLanguage';

export default function AuthCallbackPage() {
  const router = useRouter();
  const { session, isLoading } = useSession();
  const { AUTH } = useMultiLanguage();

  useEffect(() => {
    if (isLoading) return;
    // Map OAuth error query/hash (e.g. validation_failed, provider not enabled) via googleAuthErrors — never show raw Supabase JSON.
    router.replace(session ? Routes.DASHBOARD : Routes.LOGIN);
  }, [session, isLoading, router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <p className="text-muted-foreground">{AUTH.SIGNING_YOU_IN}</p>
    </div>
  );
}
```

---

## Where to configure

| Layer | Action |
|--------|--------|
| **Supabase Dashboard** | Auth → Providers → Google (Client ID + Secret). Auth → URLs: Site URL + redirect allow list includes `*/auth/callback`, `*/reset-password`. |
| **Google Cloud** | OAuth consent + scopes `openid`, `email`, `profile`. **Authorized JavaScript origins** = app origins. **Authorized redirect URIs** = `https://<project-ref>.supabase.co/auth/v1/callback`. |
