# Adding a New Language (Locale)

Follow these steps to add a new language (e.g. German, French) to the frontend i18n setup. The new locale will use the same translation keys as existing locales; you provide the translated values.

---

## 1. Create a new locale file

**Path:** `apps/frontend/src/lib/i18n/locals/<locale>.ts`
Example for German: `locals/de.ts`

- Export an object (e.g. `LangDe`) with the **same keys** as in `en.ts` and `sv.ts`.
- Values are the translated strings for the new language.

Example skeleton for `de.ts`:

```js
export const LangDe = {
  // Copy the same keys from en.ts and replace values with German translations
  'AUTH.WELCOME_BACK': 'Willkommen zurück',
  'AUTH.SIGN_IN_TO_ACCOUNT': 'Melden Sie sich in Ihrem Konto an, um fortzufahren',
  // ... every key from en.ts / sv.ts with German values
};
```

Ensure every key present in `en.ts` (and `sv.ts`) exists in the new file so no keys are missing at runtime.

---

## 2. Register the locale in the language list

**File:** `apps/frontend/src/lib/i18n/language-list.ts`

- **Import** the new locale object:
  `import { LangDe } from './locals/de';`

- Add an entry to **LanguageList** (for UI display, e.g. language switcher):
  `de: { name: 'German', nativeName: 'Deutsch' }`

- Add to **LanguageResources**:
  `de: { translation: LangDe }`

Example after adding German:

```js
import { LangDe } from './locals/de';

// Add to LanguageList
// ... existing LanguageList entries
de: { name: 'German', nativeName: 'Deutsch' },

// Add to LanguageResources
// ... existing LanguageResources entries
de: { translation: LangDe },
```

---

## 3. Cookie and language detector

- Language is persisted via `CookieProvider` at `apps/frontend/src/components/providers/CookieProvider.tsx`.
- The browser language detector in `apps/frontend/src/lib/i18n/index.ts` will recognize the new locale if you use the same locale code (e.g. `de`) as the cookie value and in `LanguageResources`.

No code changes are required in `lib/i18n/index.ts` when adding a new locale; only the new locale file and `language-list.ts` need to be updated.

---

## Checklist

- [ ] New file created under `lib/i18n/locals/<locale>.ts` with all keys from existing locales.
- [ ] `language-list.ts` updated: import, `LanguageList` entry, and `LanguageResources` entry.
