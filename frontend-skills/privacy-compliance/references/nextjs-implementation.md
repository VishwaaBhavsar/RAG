# Next.js — Privacy Components

Generic, portable. Do not tie to any specific project structure.

## PrivacyControls (manage/withdraw consent)

```tsx
// apps/frontend/src/components/privacy/PrivacyControls.tsx
'use client';
import { useEffect, useState } from 'react';

const GDPR_KEY = 'gdpr_consent';
const CCPA_KEY = 'ccpa_do_not_sell';

export default function PrivacyControls() {
  const [gdpr, setGdpr] = useState<string | null>(null);
  const [ccpa, setCcpa] = useState(false);

  useEffect(() => {
    setGdpr(localStorage.getItem(GDPR_KEY));
    setCcpa(localStorage.getItem(CCPA_KEY) === 'true');
  }, []);

  const updateGdpr = (v: 'accepted' | 'rejected') => { localStorage.setItem(GDPR_KEY, v); setGdpr(v); };
  const updateCcpa = (v: boolean) => { v ? localStorage.setItem(CCPA_KEY, 'true') : localStorage.removeItem(CCPA_KEY); setCcpa(v); };

  return (
    <div className="max-w-lg space-y-6">
      <div>
        <h2 className="font-semibold mb-1">Cookie Consent (GDPR)</h2>
        <p className="text-sm text-gray-600 mb-3">Status: <strong>{gdpr ?? 'Not set'}</strong></p>
        <div className="flex gap-3">
          <button onClick={() => updateGdpr('accepted')} className="bg-black text-white px-4 py-2 rounded text-sm">Accept</button>
          <button onClick={() => updateGdpr('rejected')} className="border px-4 py-2 rounded text-sm">Reject</button>
        </div>
      </div>
      <div>
        <h2 className="font-semibold mb-1">Data Selling (CCPA)</h2>
        <p className="text-sm text-gray-600 mb-3">Status: <strong>{ccpa ? 'Opted out' : 'Not opted out'}</strong></p>
        <button onClick={() => updateCcpa(!ccpa)} className="border px-4 py-2 rounded text-sm">
          {ccpa ? 'Opt back in' : 'Do Not Sell My Info'}
        </button>
      </div>
    </div>
  );
}
```

## Footer

```tsx
// apps/frontend/src/components/privacy/Footer.tsx
export default function Footer() {
  return (
    <footer className="border-t border-gray-200 mt-auto py-6 px-4">
      <div className="max-w-6xl mx-auto flex flex-wrap gap-4 text-sm text-gray-500">
        <span>© {new Date().getFullYear()} Your Company</span>
        <a href="/privacy-policy" className="hover:underline">Privacy Policy</a>
        <a href="/terms" className="hover:underline">Terms & Conditions</a>
        <a href="/do-not-sell" className="hover:underline">Do Not Sell My Info</a>
      </div>
    </footer>
  );
}
```

## Root Layout

```tsx
// apps/frontend/src/app/layout.tsx
import CookieBanner from '@/components/privacy/CookieBanner';
import Footer from '@/components/privacy/Footer';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex flex-col min-h-screen">
        <main className="flex-1">{children}</main>
        <Footer />
        <CookieBanner />
      </body>
    </html>
  );
}
```

## Rules
- `CookieBanner` must be in root layout — never page-level
- `ConsentCheckbox` in every generated form — never pre-checked
- Analytics injected only inside `loadAnalytics()` called post-consent
- `/privacy-policy`, `/terms`, `/do-not-sell` pages must be generated for every website
