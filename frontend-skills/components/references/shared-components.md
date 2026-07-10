# Shared Components

> Root-level reusable components in `apps/frontend/src/components/`
>
> **Note:** These components can be modified based on project requirements (unlike `components/ui/` shadcn primitives which should remain unchanged).

## Layout Components

| Component | File | Description |
|-----------|------|-------------|
| `DashboardLayout` | `DashboardLayout.tsx` | Dashboard layout structure |
| `DashboardContent` | `DashboardContent.tsx` | Dashboard content wrapper |

```tsx
import DashboardLayout from '@/components/DashboardLayout';
```

---

## Auth Components

| Component | File | Description |
|-----------|------|-------------|
| `PrivateRoute` | `PrivateRoute.tsx` | Auth route guard |
| `PublicRoute` | `PublicRoute.tsx` | Public route guard |

---

## Navigation

| Component | File | Description |
|-----------|------|-------------|
| `NavLink` | `NavLink.tsx` | Navigation link |
| `DropdownMenuItems` | `DropdownMenuItems.tsx` | Reusable dropdown items |

```tsx
import { DropdownMenuItems, type DropdownMenuItemConfig } from '@/components';
```

---

## Form Helpers

| Component | File | Description |
|-----------|------|-------------|
| `FormError` | `FormError.tsx` | Form error message display |
| `SelectBox` | `form/SelectBox.tsx` | Custom select dropdown |

```tsx
import { FormError } from '@/components';
import { SelectBox } from '@/components/form/SelectBox';
```

---

## State Components

| Component | File | Description |
|-----------|------|-------------|
| `EmptyState` | `ui/EmptyState.tsx` | Empty state display |
| `LoadingState` | `ui/LoadingState.tsx` | Loading state display |
| `ErrorState` | `ui/ErrorState.tsx` | Error state display |

```tsx
import { EmptyState, LoadingState, ErrorState } from '@/components';
```

---

## Providers

| Component | File | Description |
|-----------|------|-------------|
| `QueryProvider` | `providers/QueryProvider.tsx` | TanStack Query provider |
| `LanguageProvider` | `providers/LanguageProvider.tsx` | i18n language context |
| `CookieProvider` | `providers/CookieProvider.tsx` | Cookie/language persistence |
| `GoogleOAuthProvider` | `providers/GoogleOAuthProvider.tsx` | Google OAuth context |
