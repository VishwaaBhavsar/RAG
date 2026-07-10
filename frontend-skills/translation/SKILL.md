---
name: translation (i18n)
description: Adds and manages UI text translations using react-i18next. Use this skill when adding any user-facing string to a component or page — labels, buttons, headings, placeholders, or error messages — to ensure they go through the project's i18n system with key enums and per-locale files under lib/i18n/locals instead of being hardcoded.
---

# i18n — Adding and Using Translations

This skill describes the project's i18n flow and how to add new translations. The stack is **i18next** + **react-i18next** with a **key-constant + per-locale files** pattern.

---

## When to use this skill

- Add a new translation string or key
- Add a new language (locale)
- Change or fix copy in en or sv (or other locales)
- Understand where translation keys and values live
- Use `useMultiLanguage` hook in client components
- Use `translate()` function in non-React code (utilities, services)
- Add a language switcher dropdown to the layout

---

## Reference

| File | Read when |
|------|-----------|
| `references/adding-translations.md` | Adding a new translation key |
| `references/translation-wrapper.md` | Using translations in non-React code (utilities, services) |
| `references/adding-new-language.md` | Adding a new language (locale) |
| `references/language-switcher-dropdown.md` | Adding language switcher dropdown to layout |

---

## Key Files

| File | Purpose |
|------|---------|
| `lib/i18n/localization-enum.ts` | Key constants with `as const` (Auth, Buttons, FormLabels, etc.) |
| `@/hooks/useMultiLanguage.ts` | Type-safe hook for React components with `Translated<T>` utility type |
| `lib/i18n/translate.ts` | Translation wrapper for non-React code (utilities, services) |

---


## Rules

1. **React components** - use `useMultiLanguage()` hook, never `t()` directly
2. **Non-React code** - use `translate()` function from `@/lib/i18n/translate`, never import `i18next` directly
3. **Add to all 4 places** - enum (with `as const`), locale files, `MultiLanguage` interface, hook return
4. **Never hardcode strings** - use translation keys
5. **Keys must match exactly** - dot-path in enum = key in locale files
6. **Client-only** - components using translations need `'use client'`
7. **New locale** - add `lib/i18n/locals/<locale>.ts`, register in `language-list.ts`
8. **Language switcher required** - `DashboardLayout.tsx` and `landing/Navigation.tsx` MUST include `<LanguageSwitcher />` from `@/components`
9. **Separation of concerns** - only `translate.ts` and `useMultiLanguage.ts` should import i18n libraries directly
