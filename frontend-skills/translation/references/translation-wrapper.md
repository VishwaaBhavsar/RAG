# Translation Wrapper for Non-React Code

## Overview

For **non-React code** (utility files, services, plain TypeScript files), we use the `translate()` wrapper function instead of directly importing `i18next`. This maintains **separation of concerns** and reduces coupling to the i18n library.

---

## When to Use

Use the `translate()` function when:
- ✅ Working in **non-React files** (utilities, services, config files)
- ✅ Cannot use React hooks (`useMultiLanguage`, `useTranslation`)
- ✅ Need translations in plain JavaScript/TypeScript functions
- ✅ Writing library-agnostic code

**Do NOT use** `translate()` in:
- ❌ React components (use `useMultiLanguage` hook instead)
- ❌ Custom React hooks (use `useTranslation` or `useMultiLanguage`)

---

## Architecture

### Translation Wrapper Location

```
apps/frontend/src/lib/i18n/translate.ts
```

### Implementation

```typescript
import { getI18n } from 'react-i18next';

/**
 * Get translated string by key (for use outside React components)
 * Use useMultiLanguage hook inside React components instead
 */
export const translate = (key: string): string => {
  const i18n = getI18n();
  return i18n.t(key);
};
```

---

## Benefits

### 1. **Single Point of Change**
Only `translate.ts` imports the i18n library directly. If you switch from `react-i18next` to another library (e.g., `react-intl`, `lingui`), you only update this one file.

### 2. **Reduced Surface Area**
Minimizes the number of files that depend on the specific i18n implementation.

### 3. **Better Separation of Concerns**
Business logic doesn't know or care what i18n library is being used.

### 4. **Easier Testing**
Mock the `translate` function instead of the entire i18n library.

---

## Usage Examples

### ✅ Correct: Using the Wrapper

```typescript
// ✅ apps/frontend/src/lib/query/queryClient.ts
import { translate } from '@/lib/i18n/translate';
import { ToastMessages } from '@/lib/i18n/localization-enum';

const defaultErrorMessage = translate(ToastMessages.ERROR_DEFAULT_MESSAGE);
showErrorToast(errorMessage, translate(ToastMessages.ERROR_DEFAULT_RETRY));
```

### ❌ Incorrect: Direct i18next Import

```typescript
// ❌ DON'T DO THIS - Tight coupling to i18next
import i18next from 'i18next';
import { ToastMessages } from '@/lib/i18n/localization-enum';

const defaultErrorMessage = i18next.t(ToastMessages.ERROR_DEFAULT_MESSAGE);
```

### ✅ Correct: React Component

```typescript
// ✅ In React components, use useMultiLanguage hook
import useMultiLanguage from '@/hooks/useMultiLanguage';

export function MyComponent() {
  const { TOAST_MESSAGES } = useMultiLanguage();

  return <div>{TOAST_MESSAGES.ERROR_DEFAULT_MESSAGE}</div>;
}
```

---

## Common Use Cases

### 1. Query Client / API Layer

```typescript
// apps/frontend/src/lib/query/queryClient.ts
import { translate } from '@/lib/i18n/translate';
import { ToastMessages } from '@/lib/i18n/localization-enum';

export function createAuthMutation() {
  return useMutation({
    onError: (error: Error) => {
      const defaultErrorMessage = translate(ToastMessages.ERROR_DEFAULT_MESSAGE);
      showErrorToast(error.message || defaultErrorMessage);
    },
  });
}
```

### 2. Utility Functions

```typescript
// apps/frontend/src/lib/utils/validation.ts
import { translate } from '@/lib/i18n/translate';
import { Validation } from '@/lib/i18n/localization-enum';

export function validateEmail(email: string): string | null {
  if (!email) {
    return translate(Validation.EMAIL_REQUIRED);
  }
  // ... more validation
}
```

### 3. Service Layer

```typescript
// apps/frontend/src/services/storage.service.ts
import { translate } from '@/lib/i18n/translate';
import { ErrorMessages } from '@/lib/i18n/localization-enum';

export class StorageService {
  save(key: string, value: any) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      throw new Error(translate(ErrorMessages.STORAGE_FAILED));
    }
  }
}
```

---

## Decision Tree

```
Need translation?
│
├─ In React Component?
│  └─ YES → Use useMultiLanguage() hook
│
└─ In non-React code?
   └─ YES → Use translate() function
```

---

## Rules

1. **NEVER** import `i18next` directly in application code
2. **ALWAYS** use `translate()` for non-React code
3. **ALWAYS** use `useMultiLanguage()` for React components
4. **NEVER** use `translate()` in React components (use the hook instead)
5. All translation keys must be defined in `localization-enum.ts`

---

## Switching i18n Libraries

If you ever need to switch from `react-i18next` to another library, you only need to:

1. Update `translate.ts` implementation
2. Update `useMultiLanguage.ts` hook
3. No changes needed in your application code!

**Example: Switching to react-intl**

```typescript
// Before (react-i18next):
import { getI18n } from 'react-i18next';

export const translate = (key: string): string => {
  const i18n = getI18n();
  return i18n.t(key);
};

// After (react-intl):
import { createIntl, createIntlCache } from 'react-intl';
import messages from './messages';

const cache = createIntlCache();
const intl = createIntl({ locale: 'en', messages }, cache);

export const translate = (key: string): string => {
  return intl.formatMessage({ id: key });
};
```

All your application code remains unchanged! ✅

---

## Related Files

- `apps/frontend/src/lib/i18n/translate.ts` - Translation wrapper implementation
- `apps/frontend/src/hooks/useMultiLanguage.ts` - React hook for components
- `apps/frontend/src/lib/i18n/localization-enum.ts` - Translation key constants
