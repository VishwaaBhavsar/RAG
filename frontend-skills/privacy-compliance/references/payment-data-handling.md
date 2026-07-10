# Payment Data Handling

## Privacy Policy — Payment Data section

```md
## Payment Information
We use [Stripe / PayPal] to process payments. We do not store card numbers, CVV, or credentials.
- Collected: billing name/address, last 4 digits of card, transaction IDs, order history
- Processor privacy policy: https://stripe.com/privacy
- Retention: order/transaction records retained 7 years (tax compliance)
```

## Terms & Conditions — Payments & Billing section

```md
## Payments & Billing
Payments processed by [Stripe / PayPal]. Prices in [USD/GBP] exclude applicable taxes.
Failed payments may suspend access; we will notify by email and retry. You are responsible for taxes in your jurisdiction.
```

## Refund Policy — `/refund-policy`

```tsx
// apps/frontend/src/app/refund-policy/page.tsx
export const metadata = { title: 'Refund Policy' };

export default function RefundPolicyPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Refund Policy</h1>
      {/* Sections: Digital Products (final on download, 14-day tech issue window)
                   Subscriptions (cancel anytime, no pro-rata, end of billing period)
                   Physical Goods (30-day return, original packaging, customer pays shipping)
                   How to Request (email support@domain.com with order ID, 2 business days) */}
    </main>
  );
}
```

## PCI DSS Notes

| Requirement | Implementation |
|-------------|---------------|
| No card data on server | Use Stripe.js / hosted fields — card never hits your server |
| HTTPS | Enforce `Strict-Transport-Security` header |
| Tokenisation | Store only processor token (e.g. `pm_xxx`), never raw card data |
| Audit logs | Log payment events (intent created/succeeded/failed) — never log card details |
| Breach notification | Notify processor + users within 72 h (GDPR obligation) |

## Footer
```tsx
{ label: 'Refund Policy', href: '/refund-policy' },
```

## Checklist
- [ ] Payment processor privacy policy linked in Privacy Policy
- [ ] No raw card data stored or logged
- [ ] `/refund-policy` page exists
- [ ] Billing section in Terms & Conditions
- [ ] HTTPS enforced (HSTS header)
- [ ] Transaction records retained 7 years
