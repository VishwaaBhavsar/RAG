# Language Switcher Dropdown

The `LanguageSwitcher` component allows users to change the application language. It is already set up and integrated.

---

## Quick Reference

| File | Purpose |
|------|---------|
| `components/LanguageSwitcher.tsx` | Dropdown component (exported from `@/components`) |
| `lib/i18n/translate.ts` | `changeLanguage(lang)` — switches language + persists to cookie |
| `lib/i18n/language-list.ts` | `LanguageList` — available locales with native names |
| `lib/i18n/index.ts` | i18next configuration |

---

## Usage

Import from the barrel export:

```tsx
import { LanguageSwitcher } from '@/components';

// Add to nav/header:
<LanguageSwitcher />
```

---

## Verify Integration

If the language switcher is missing from a layout, add it:

1. Import: `import { LanguageSwitcher } from '@/components';`
2. Place in nav/header area
3. Ensure parent component has `'use client'`

---

## How It Works

The component uses:
- `useState` — tracks current language for UI reactivity
- `changeLanguage()` — handles i18next switch + cookie persistence
- `LanguageList` — provides available languages with native names

---

## Checklist (for new layouts)

- [ ] Imported `LanguageSwitcher` from `@/components`
- [ ] Placed in visible nav/header area
- [ ] Parent is a client component (`'use client'`)
