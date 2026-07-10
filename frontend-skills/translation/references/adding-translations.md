# Adding New Translations — Step-by-Step

Follow this flow to add a new translatable string so it stays consistent across enums and all locale files.

---

## 1. Add the key constant (enum)

**File:** `apps/frontend/src/lib/i18n/localization-enum.ts`

- Choose or add a **namespace** (e.g. `Auth`, `FormLabels`, `Buttons`, `Validation`, or a new one like `Dashboard`).
- Add a new property whose **value** is a dot-path string matching the namespace and a short identifier.

Example — adding a dashboard welcome message:

```ts
// In localizationEnum.ts, add or extend a namespace:

export const Dashboard = {
  WELCOME_TITLE: 'DASHBOARD.WELCOME_TITLE',
  STATS_LABEL: 'DASHBOARD.STATS_LABEL',
} as const;  // Always add 'as const' for type safety
```

Use UPPER_SNAKE_CASE for the property name and a dot-path like `'NAMESPACE.KEY_NAME'` for the value. This value is the **translation key** used by i18next. Always add `as const` for type safety.

---

## 2. Add the string for each locale

**Files:**
- `apps/frontend/src/lib/i18n/locals/en.ts`
- `apps/frontend/src/lib/i18n/locals/sv.ts`
(and any other locale files you have)

In each file, add the **same key** (the dot-path string) with the translated value for that language.

**en.js:**

```js
export const LangEn = {
  // ... existing keys ...
  'DASHBOARD.WELCOME_TITLE': 'Welcome to your dashboard',
  'DASHBOARD.STATS_LABEL': 'Statistics',
};
```

**sv.js:**

```js
export const LangSv = {
  // ... existing keys ...
  'DASHBOARD.WELCOME_TITLE': 'Välkommen till din instrumentpanel',
  'DASHBOARD.STATS_LABEL': 'Statistik',
};
```

Keys in all locale files must match the enum value exactly (same string, same dots).

---

## 3. Use the key in a client component

Components that use translations must be **client components** (have `'use client'` at the top) and live under the app’s `LanguageProvider`.

**Custom hook `useMultiLanguage`:**

If you want the new key exposed via the shared hook, edit:

**File:** `apps/frontend/src/hooks/useMultiLanguage.ts`

1. Import the new enum
2. Add to `MultiLanguage` interface
3. Add to the return object

```ts
import { Dashboard } from './localizationEnum';

// Add to interface
type Translated<T> = { readonly [K in keyof T]: string };

interface MultiLanguage {
  // ... existing
  readonly DASHBOARD: Translated<typeof Dashboard>;
}

// Add to return object
const useMultiLanguage = (): MultiLanguage => {
  const { t } = useTranslation();
  return {
    // ... existing
    DASHBOARD: {
      WELCOME_TITLE: t(Dashboard.WELCOME_TITLE),
      STATS_LABEL: t(Dashboard.STATS_LABEL),
    },
  };
};
```

Then in any client component:

```tsx
'use client';

import useMultiLanguage from '@/hooks/useMultiLanguage';

export function DashboardHeader() {
  const { DASHBOARD } = useMultiLanguage();
  return <h1>{DASHBOARD.WELCOME_TITLE}</h1>;
}
```

---

For adding a **new language** (e.g. German), see `references/adding-new-language.md`.

---

## Checklist

- [ ] Key added in `lib/i18n/localization-enum.ts` with `as const` assertion.
- [ ] Same key added in `lib/i18n/locals/en.ts` and `lib/i18n/locals/sv.ts`.
- [ ] `MultiLanguage` interface updated in `hooks/useMultiLanguage.ts`.
- [ ] Return object updated in `hooks/useMultiLanguage.ts`.
- [ ] Component uses `useMultiLanguage()` hook (must be `'use client'`).
