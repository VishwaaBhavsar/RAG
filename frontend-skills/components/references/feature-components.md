# Feature Components

> Domain-specific components organized by feature area.

## Billing (`billing/`)

| Component | File | Description |
|-----------|------|-------------|
| `CurrentPlanCard` | `billing/CurrentPlanCard.tsx` | Displays current subscription plan |
| `FeatureItem` | `billing/FeatureItem.tsx` | Single feature in plan comparison |
| `InvoiceItem` | `billing/InvoiceItem.tsx` | Invoice line item |
| `PaymentMethodCard` | `billing/PaymentMethodCard.tsx` | Payment method display |
| `PlanCard` | `billing/PlanCard.tsx` | Pricing plan card |
| `UsageProgressBar` | `billing/UsageProgressBar.tsx` | Usage meter with progress |

```tsx
import { CurrentPlanCard, PlanCard, UsageProgressBar } from '@/components';
```

---

## Projects (`projects/`)

| Component | File | Description |
|-----------|------|-------------|
| `ProjectCard` | `projects/ProjectCard.tsx` | Project card with thumbnail and status |

```tsx
import { ProjectCard, type Project, type ProjectCardProps } from '@/components';
```

---

## Team (`team/`)

| Component | File | Description |
|-----------|------|-------------|
| `MemberItem` | `team/MemberItem.tsx` | Team member row with actions |
| `PendingInviteItem` | `team/PendingInviteItem.tsx` | Pending invitation row |
| `InviteMemberForm` | `team/InviteMemberForm.tsx` | Form to invite new members |

```tsx
import { MemberItem, PendingInviteItem, InviteMemberForm } from '@/components';
```

---

## Notifications (`notifications/`)

| Component | File | Description |
|-----------|------|-------------|
| `NotificationItem` | `notifications/NotificationItem.tsx` | Single notification display |

```tsx
import { NotificationItem } from '@/components';
```

---

## Usage (`usage/`)

| Component | File | Description |
|-----------|------|-------------|
| `UsageStatCard` | `usage/UsageStatCard.tsx` | Usage statistic card |

```tsx
import { UsageStatCard } from '@/components';
```

---

## Settings (`settings/`)

| Component | File | Description |
|-----------|------|-------------|
| `NotificationSettingItem` | `settings/NotificationSettingItem.tsx` | Notification preference toggle |
| `WorkspaceSettingsForm` | `settings/WorkspaceSettingsForm.tsx` | Workspace settings form |

```tsx
import { NotificationSettingItem, WorkspaceSettingsForm } from '@/components';
```

---

## Editor (`editor/`)

| Component | File | Description |
|-----------|------|-------------|
| `MessageItem` | `editor/components/MessageItem.tsx` | Chat/editor message |

```tsx
import { MessageItem } from '@/components';
```

---

## Landing (`landing/`)

| Component | File | Description |
|-----------|------|-------------|
| `CTASection` | `landing/CTASection.tsx` | Call-to-action section |
| `FeaturesSection` | `landing/FeaturesSection.tsx` | Features showcase |
| `Footer` | `landing/Footer.tsx` | Landing page footer |
| `HeroSection` | `landing/HeroSection.tsx` | Hero banner |
| `Navigation` | `landing/Navigation.tsx` | Landing navigation |

```tsx
import { HeroSection, FeaturesSection, CTASection, Footer, Navigation } from '@/components';
```
