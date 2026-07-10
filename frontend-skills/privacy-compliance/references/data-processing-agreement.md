# Data Processing Agreement (DPA)

## GDPR Role Distinction

| Role | Definition | Example |
|------|-----------|---------|
| **Data Controller** | Decides why/how data is processed | Your B2B customer |
| **Data Processor** | Processes data on controller's behalf | Your SaaS product |
| **Sub-processor** | Processor engaged by the processor | AWS, Stripe, SendGrid |

As a SaaS provider you are typically a **data processor** for customers' data (GDPR Art. 28).

## DPA Page — `/dpa`

```tsx
// apps/frontend/src/app/dpa/page.tsx
export const metadata = { title: 'Data Processing Agreement', description: 'GDPR Article 28 DPA for enterprise customers.' };

export default function DPAPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Data Processing Agreement</h1>
      {/* Required sections:
          1. Definitions  2. Processing Instructions  3. Confidentiality
          4. Security (TOMs — see table below)  5. Sub-processors (link /sub-processors)
          6. Data Subject Rights assistance  7. Security Incidents (48h notify controller)
          8. Data Deletion / Return  9. Audits  10. International Transfers (SCCs)
      */}
      <p>To execute a DPA contact <a href="mailto:legal@domain.com">legal@domain.com</a>.</p>
    </main>
  );
}
```

## Sub-Processor List — `/sub-processors`

```tsx
// apps/frontend/src/app/sub-processors/page.tsx
const subProcessors = [
  { name: 'Amazon Web Services', purpose: 'Cloud hosting',        location: 'US / EU', link: 'https://aws.amazon.com/privacy/' },
  { name: 'Stripe',              purpose: 'Payment processing',   location: 'US',      link: 'https://stripe.com/privacy' },
  { name: 'SendGrid (Twilio)',   purpose: 'Transactional email',  location: 'US',      link: 'https://www.twilio.com/legal/privacy' },
  // add all sub-processors
];

export default function SubProcessorsPage() {
  return (
    <main className="max-w-4xl mx-auto px-4 py-16">
      <h1>Sub-Processor List</h1>
      <p>New sub-processors notified with 30 days advance notice.</p>
      <table>
        <thead><tr><th>Name</th><th>Purpose</th><th>Location</th><th>Privacy Policy</th></tr></thead>
        <tbody>{subProcessors.map(sp => <tr key={sp.name}><td>{sp.name}</td><td>{sp.purpose}</td><td>{sp.location}</td><td><a href={sp.link} target="_blank" rel="noopener noreferrer">View</a></td></tr>)}</tbody>
      </table>
    </main>
  );
}
```

## Privacy Policy — Business Customers section

```md
## Business Customers (B2B)
We act as a data processor under GDPR Art. 28 for business customers who process their users' data through our platform.
We process such data only per your documented instructions and our [Data Processing Agreement](/dpa).
Enterprise DPA: contact [legal@domain.com].
```

## Technical & Organisational Measures (TOMs)

| Measure | Implementation |
|---------|---------------|
| Encryption at rest | AES-256 (AWS KMS) |
| Encryption in transit | TLS 1.2+ |
| Access control | RBAC, MFA required for staff |
| Pen testing | Annual third-party |
| Incident response | Documented; 48 h notification to controllers |
| Backups | Daily, 30-day retention, encrypted |
| Pseudonymisation | PII separated from analytics data |

## Footer
```tsx
{ label: 'DPA',            href: '/dpa'            },
{ label: 'Sub-processors', href: '/sub-processors' },
```

## Checklist
- [ ] `/dpa` page with all 10 required sections
- [ ] `/sub-processors` list page
- [ ] Sub-processor change notification mechanism (email/changelog)
- [ ] TOMs documented in DPA or `/security` page
- [ ] Privacy Policy has B2B processor section
- [ ] Legal contact for DPA execution documented
- [ ] 48-hour breach notification obligation noted
