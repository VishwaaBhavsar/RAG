# Cookie Policy (Detailed)

Extends `gdpr-consent-management.md`. Use when project has analytics, marketing pixels, or third-party embeds.

## Cookie Categories

| Category | Consent Required | Examples |
|----------|-----------------|---------|
| Strictly Necessary | No | Session ID, CSRF token, auth cookie, consent preference |
| Functional | Yes | Language preference, theme, saved form data |
| Analytics | Yes | Google Analytics (`_ga`), Mixpanel, PostHog |
| Marketing | Yes | Facebook Pixel, Google Ads, LinkedIn Insight |
| Third-party embeds | Yes | YouTube, Intercom, Drift, Typeform |

## Cookie Policy Page — `/cookies`

```tsx
// apps/frontend/src/app/cookies/page.tsx
export const metadata = { title: 'Cookie Policy', description: 'How we use cookies and tracking technologies.' };

export default function CookiePolicyPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Cookie Policy</h1>
      {/* Sections: What are cookies · Cookies we use (CookieTable) ·
          Managing cookies (/privacy-controls link) · Third-party cookies (link each provider policy) */}
      <CookieTable />
    </main>
  );
}
```

## CookieTable Component

```tsx
// apps/frontend/src/components/privacy/CookieTable.tsx
const cookies = [
  { name: 'consent',   category: 'Strictly Necessary', purpose: 'Stores consent preference',          duration: '1 year',  party: 'First-party' },
  { name: '__session', category: 'Strictly Necessary', purpose: 'Maintains authenticated session',     duration: 'Session', party: 'First-party' },
  { name: '_ga, _ga_*',category: 'Analytics',          purpose: 'Google Analytics — page views/behaviour', duration: '2 years', party: 'Third-party (Google)' },
  // add all cookies the site sets
];

export default function CookieTable() {
  return (
    <div className="overflow-x-auto">
      <table>
        <thead><tr><th>Name</th><th>Category</th><th>Purpose</th><th>Duration</th><th>Party</th></tr></thead>
        <tbody>{cookies.map(c => <tr key={c.name}><td><code>{c.name}</code></td><td>{c.category}</td><td>{c.purpose}</td><td>{c.duration}</td><td>{c.party}</td></tr>)}</tbody>
      </table>
    </div>
  );
}
```

## Granular Consent Utilities

```ts
// Extend consent.ts when category-level consent is needed
interface GranularConsent { functional: boolean; analytics: boolean; marketing: boolean; }

export const setGranularConsent = (s: GranularConsent): void =>
  localStorage.setItem('consent_granular', JSON.stringify({ ...s, necessary: true }));

export const getGranularConsent = (): (GranularConsent & { necessary: true }) | null => {
  const raw = localStorage.getItem('consent_granular');
  return raw ? JSON.parse(raw) : null;
};
```

## Footer
```tsx
{ label: 'Cookie Policy', href: '/cookies' },
```

## Checklist
- [ ] `/cookies` page with CookieTable listing every cookie the site sets
- [ ] Cookie banner links to Cookie Policy
- [ ] "Manage Cookies" link in footer or Privacy Controls
- [ ] Third-party providers listed with links to their privacy policies
- [ ] Cookie preferences re-askable from Privacy Controls page
