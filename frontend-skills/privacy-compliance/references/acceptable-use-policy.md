# Acceptable Use Policy (AUP)

## AUP Page — `/acceptable-use`

```tsx
// apps/frontend/src/app/acceptable-use/page.tsx
export const metadata = { title: 'Acceptable Use Policy', description: 'Rules governing use of our platform.' };

export default function AcceptableUsePolicyPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Acceptable Use Policy</h1>
      <p>Violations may result in immediate account suspension or termination.</p>
      {/* Populate prohibited categories from table below */}
      {/* Sections: Prohibited Activities · Content Standards · Reporting · Enforcement */}
    </main>
  );
}
```

## Prohibited Categories

| Category | Prohibited |
|----------|-----------|
| Illegal content | Law violations, IP infringement, defamation, CSAM (zero tolerance — reported to authorities) |
| Harassment | Bullying, threats, hate speech, doxxing, impersonation |
| Security abuse | Unauthorised access, malware distribution, DoS attacks, vulnerability scanning without permission, excess scraping |
| Spam | Unsolicited bulk email/messages, phishing, CAN-SPAM/CASL violations |
| Platform abuse | Multiple accounts to evade bans, unauthorised resale, rate-limit abuse, crypto mining on infrastructure |

## Terms & Conditions — reference AUP

```md
## Acceptable Use
Your use is subject to our [Acceptable Use Policy](/acceptable-use), incorporated by reference. By using our services you agree to comply.
```

## Content Moderation

| Type | Approach |
|------|---------|
| CSAM | Zero-tolerance; PhotoDNA hash matching if images allowed |
| Spam | Rate-limit message APIs; SpamAssassin or equivalent |
| DMCA | Register DMCA agent + counter-notice process |
| User reports | In-app report button with categories |
| Appeals | Mechanism for disputing account suspension |

## Footer
```tsx
{ label: 'Acceptable Use', href: '/acceptable-use' },
```

## Checklist
- [ ] `/acceptable-use` page with all prohibited categories
- [ ] AUP referenced in Terms & Conditions
- [ ] Abuse reporting contact (abuse@domain.com or in-app)
- [ ] CSAM zero-tolerance statement
- [ ] Enforcement rights clearly stated
- [ ] DMCA process if UGC includes files/media
