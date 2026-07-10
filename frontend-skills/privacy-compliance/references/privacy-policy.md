# Privacy Policy Page (`/privacy-policy`)

## Required Sections

| Section | Must Cover |
|---------|-----------|
| Introduction | Company name, contact email, effective date |
| Data Collected | Identity, contact, usage, technical, transaction data |
| How Collected | Forms, cookies/analytics, third-party APIs |
| Purpose & Legal Basis | Table: purpose → legal basis (consent / contract / legal obligation / legitimate interest) |
| Third-Party Sharing | List vendors (e.g. Stripe, GA), purpose, confirm not sold |
| Retention Periods | Table: data type → period (accounts 3yr, transactions 7yr, analytics 1yr) |
| User Rights (GDPR) | Access, erasure, rectification, portability, objection, restriction — 30-day response |
| CCPA Rights | Right to know, delete, opt-out → link to `/do-not-sell`; non-discrimination statement |
| Cookies | Categories (necessary/analytics/marketing), how to manage |
| Security | HTTPS/TLS in transit, encrypted storage at rest |
| International Transfers | EEA transfers → Standard Contractual Clauses |
| Policy Changes | How users are notified; effective date updated |
| Contact / DPO | Data controller email, DPO if applicable, supervisory authority right |

## Next.js Page Stub

```tsx
// apps/frontend/src/app/privacy-policy/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'How we collect, use, and protect your personal data.',
};

export default function PrivacyPolicyPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Privacy Policy</h1>
      <p className="text-sm text-gray-500">Effective date: [date]</p>
      {/* Populate all sections from Required Sections table above */}
    </main>
  );
}
```

## Rules
- Link from every consent checkbox, cookie banner, and footer
- Update effective date on every material change
- Re-obtain consent if changes affect how data is processed
