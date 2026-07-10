# Subscription & Billing Terms (SaaS)

## Terms & Conditions — Subscription section

```md
## Subscription Plans & Billing

| Topic | Rule |
|-------|------|
| Free Trial | No charge during trial; auto-converts to paid unless cancelled before trial ends |
| Auto-Renewal | Renews automatically each billing period; we charge payment method on file |
| Pricing Changes | 30 days' notice; takes effect at next renewal; continued use = acceptance |
| Cancellation | Cancel anytime from account settings; access continues until period end |
| Downgrade | Takes effect next cycle; data retained 90 days above new plan limits |
| Upgrade | Pro-rata charge for remainder of current period |
```

## Privacy Policy — Billing Data section

```md
## Subscription & Billing Data
- Collected: plan, billing cycle, payment token (not full card), invoice history, usage metrics
- Purpose: fulfil subscription, issue invoices, tax compliance
- Retention: billing records 7 years (legal obligation)
- Rights: request invoice copies at any time via [support@domain.com]

### Account Deletion
Profile data deleted within 30 days · Billing history retained 7 years · Data export (CSV/JSON) available on request before deletion
```

## Next.js Routes

```
apps/frontend/src/app/
  billing/page.tsx          ← current plan, payment method, invoice history
  billing/cancel/page.tsx   ← cancellation confirmation (checkbox + confirm button)
  account/page.tsx          ← settings, data export, delete account
```

## CancelConfirmation Skeleton

```tsx
// apps/frontend/src/components/billing/CancelConfirmation.tsx
'use client';
import { useState } from 'react';

export default function CancelConfirmation({ onConfirm }: { onConfirm: () => void }) {
  const [confirmed, setConfirmed] = useState(false);
  return (
    <div role="dialog" aria-modal="true" aria-labelledby="cancel-title">
      <h2 id="cancel-title">Cancel your subscription?</h2>
      {/* What they lose · data export note · reactivation note */}
      <label><input type="checkbox" onChange={e => setConfirmed(e.target.checked)} /> I understand my subscription ends at the billing period close</label>
      <button type="button" onClick={() => window.history.back()}>Keep my plan</button>
      <button type="button" onClick={onConfirm} disabled={!confirmed}>Confirm cancellation</button>
    </div>
  );
}
```

## Checklist
- [ ] Free trial terms state exactly when billing begins
- [ ] Auto-renewal disclosed before checkout
- [ ] Cancellation accessible from account settings
- [ ] Price change notice period stated (30 days)
- [ ] Invoice/billing history accessible to user
- [ ] Data export available before account deletion
- [ ] Billing records retention documented (7 years)
