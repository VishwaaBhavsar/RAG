# Email/password sign-in & sign-up

**Rules:** `../SKILL.md`. Mutations UX: **api-integration** `mutation-with-loader.md`. Schemas: **translation** skill; mirror `apps/frontend/src/lib/validations/authSchemas.ts`.

---

## `AuthService` (`services/authService.ts`)

```ts
import { getSupabaseClient } from '@/lib/supabase/supabaseClient';
import { Routes } from '@/constants/routes';
import type { AuthResponse } from '@supabase/supabase-js';

export type SignInInput = { email: string; password: string };
export type SignUpInput = { email: string; password: string; name: string };

export class AuthService {
  static async signIn(input: SignInInput): Promise<AuthResponse['data']> {
    const { data, error } = await getSupabaseClient().auth.signInWithPassword(input);
    if (error) throw error;
    return data;
  }

  static async signUp(input: SignUpInput): Promise<AuthResponse['data']> {
    const { data, error } = await getSupabaseClient().auth.signUp({
      email: input.email,
      password: input.password,
      options: {
        emailRedirectTo: `${window.location.origin}${Routes.AUTH_CALLBACK}`,
        data: { name: input.name },
      },
    });
    if (error) throw error;
    return data;
  }

  static async signOut(): Promise<void> {
    const { error } = await getSupabaseClient().auth.signOut();
    if (error) throw error;
  }
}
```

- `emailRedirectTo` must be allowed in Supabase **Auth → URL Configuration**.
- `signUp` → often `data.session === null` until email confirm → UI: “check email”, no redirect.

---

## Mutations (`hooks/auth/useAuthMutations.ts`)

```ts
import { useMutation } from '@tanstack/react-query';
import { queryClient } from '@/lib/query/queryClient';
import { AuthService, type SignInInput, type SignUpInput } from '@/services/authService';
import { authKeys } from './queryKeys';
import type { AuthResponse } from '@supabase/supabase-js';

type AuthData = AuthResponse['data'];

export function useSignInMutation() {
  return useMutation<AuthData, Error, SignInInput>({
    mutationFn: AuthService.signIn,
    onSuccess: (d) => {
      queryClient.setQueryData(authKeys.session(), d.session);
      queryClient.setQueryData(authKeys.user(), d.user);
    },
  });
}

export function useSignUpMutation() {
  return useMutation<AuthData, Error, SignUpInput>({ mutationFn: AuthService.signUp });
}

export function useSignOutMutation() {
  return useMutation<void, Error, void>({
    mutationFn: AuthService.signOut,
    onSuccess: () => queryClient.removeQueries({ queryKey: authKeys.all }),
  });
}
```

`AuthProvider` still syncs via `onAuthStateChange` — `onSuccess` on sign-in is optimistic UX only.

---

## Forms

`useForm` + `yupResolver(loginSchema)` · `defaultValues { email:'', password:'' }`. **Register:** `registerSchema`, `{ name, email, password }`.

---

## Pages (`app/(auth)/…`)

| Route | Pattern |
|--------|---------|
| **login** | `useLoginForm` → `useSignInMutation` → `try/catch` (show original error, fallback from `useMultiLanguage`) · `replace(DASHBOARD)` on success · `GoogleSignInButton` · links `FORGOT_PASSWORD` / `REGISTER` |
| **register** | `useRegisterForm` → `useSignUpMutation` · if `!data.session` show verification UI else `replace(DASHBOARD)` |

Login shape: `Input` email · `PasswordInput` · `ButtonWithLoader` loading=`signIn.isPending` · i18n via `useMultiLanguage`.

```tsx
// register onSubmit core
const data = await signUp.mutateAsync(values);
if (!data.session) setVerificationSent(true);
else router.replace(Routes.DASHBOARD);
```

Verification link lands on `Routes.AUTH_CALLBACK` → `app/auth/callback/page.tsx` (`google-oauth.md`).

---

## Notes

- Errors: throw from service; for UI catch blocks use the **single-source pattern** in `workflow.md` → **Error display pattern (single source)** with `ERRORS.AUTHENTICATION_FAILED` fallback.
- Skeleton while `AuthProvider` hydrates: **api-integration** `skeletons.md`.
- Template may lack `PasswordInput` — **components** skill / add wrapper.

Add `ERRORS.AUTHENTICATION_FAILED` to locale files via **translation** skill.
