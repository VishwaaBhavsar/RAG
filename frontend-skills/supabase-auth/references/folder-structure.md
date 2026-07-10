# Folder tree

**Root:** `apps/frontend/src/`. Baseline: vibe template under `templates/project-templates/frontend-template/files/apps/frontend/src/`.

**Invariant:** OAuth/email callback = **`app/auth/callback/page.tsx`** (not under `(auth)/`) — `SKILL.md` + `session-and-guards.md`.

```
lib/supabase/supabaseClient.ts    # + auth:{persistSession,autoRefreshToken,detectSessionInUrl}
lib/supabase/googleAuthErrors.ts  # when Google OAuth: disabled-provider normalization + authorize URL gate
lib/supabase/database.types.ts    # if using supabase-api-integration
lib/validations/authSchemas.ts    # + phoneSchema + verifyOtpSchema (phone OTP only)
services/authService.ts
hooks/auth/queryKeys.ts | useSession.ts | useAuthMutations.ts | use*Form.ts (×5, + usePhoneOtpForm if phone OTP)
hooks/useAuth.ts
contexts/AuthProvider.tsx
components/auth/PublicRoute.tsx | PrivateRoute.tsx | GoogleSignInButton.tsx | PhoneProviderDisabledDialog.tsx
components/ui/InputOtp.tsx        # reused for the 6-digit code on (auth)/phone (phone OTP only)
types/authFormTypes.ts
constants/routes.ts               # + LOGIN REGISTER FORGOT_PASSWORD RESET_PASSWORD AUTH_CALLBACK=/auth/callback (+ PHONE_LOGIN=/phone if phone OTP)
app/layout.tsx                    # QueryProvider > AuthProvider > …
app/auth/callback/page.tsx
app/(auth)/layout.tsx             # PublicRoute
app/(auth)/login|register|forgot-password|reset-password/page.tsx
app/(auth)/phone/page.tsx         # single page, two-step (phone → OTP) — phone OTP only
app/(private)/layout.tsx          # PrivateRoute + dashboard/…
```

**Parity:** `supabase-api-integration` + **api-integration** skeletons/mutation UX. **translation** + **components** for copy/UI.

**See also:**
- `../../supabase-api-integration/references/folder-structure.md` — shared Supabase module layout (`lib/supabase/*`) and domain service/hook parity.
- `../../next-best-practices/file-conventions.md` — Next.js App Router file conventions (`page.tsx`, `layout.tsx`, route groups).
