# CCPA — Do Not Sell

## /do-not-sell Page

```tsx
'use client';
import { useEffect, useState } from 'react';

const OPT_OUT_KEY = 'ccpa_do_not_sell';

export default function DoNotSellPage() {
  const [optedOut, setOptedOut] = useState(false);

  useEffect(() => {
    if (navigator.globalPrivacyControl) setCCPAOptOut(true); // honour GPC
    setOptedOut(localStorage.getItem(OPT_OUT_KEY) === 'true');
  }, []);

  const handleOptOut = () => { localStorage.setItem(OPT_OUT_KEY, 'true'); setOptedOut(true); };
  const handleOptIn  = () => { localStorage.removeItem(OPT_OUT_KEY); setOptedOut(false); };

  return (
    <main className="max-w-2xl mx-auto px-4 py-16">
      <h1 className="text-3xl font-bold mb-6">Do Not Sell My Personal Information</h1>
      <p className="mb-4">Under CCPA, California residents may opt out of the sale of their personal information.</p>

      {optedOut ? (
        <div>
          <p className="text-green-700 font-semibold mb-4">✓ You have opted out.</p>
          <button onClick={handleOptIn} className="text-sm underline text-gray-500">Opt back in</button>
        </div>
      ) : (
        <button onClick={handleOptOut} className="bg-black text-white px-6 py-3 rounded hover:bg-gray-800">
          Do Not Sell My Personal Information
        </button>
      )}

      <section className="mt-12 text-sm text-gray-600">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Data we collect</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Identifiers (name, email, IP address)</li>
          <li>Usage data (pages visited, time on site)</li>
          <li>Device and browser information</li>
          <li>Cookie and tracking data</li>
        </ul>
        <h2 className="text-lg font-semibold text-gray-900 mt-6 mb-2">Your rights</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Right to know what personal information is collected</li>
          <li>Right to opt out of the sale of personal information</li>
          <li>Right to delete personal information</li>
          <li>Right to non-discrimination for exercising rights</li>
        </ul>
      </section>
    </main>
  );
}
```

## Utilities

```ts
// apps/frontend/src/lib/ccpa.ts
export const CCPA_OPT_OUT_KEY = 'ccpa_do_not_sell';

export const hasCCPAOptedOut = (): boolean =>
  typeof window !== 'undefined' && localStorage.getItem(CCPA_OPT_OUT_KEY) === 'true';

export const setCCPAOptOut = (value: boolean): void => {
  if (typeof window === 'undefined') return;
  value ? localStorage.setItem(CCPA_OPT_OUT_KEY, 'true') : localStorage.removeItem(CCPA_OPT_OUT_KEY);
};

// Analytics gate — use before loading any tracking script
export const canLoadAnalytics = (): boolean => {
  const gdprAccepted = localStorage.getItem('gdpr_consent') === 'accepted';
  return gdprAccepted && !hasCCPAOptedOut();
};
```

## Rules
- Link "Do Not Sell My Info" in footer of every page
- Honour `navigator.globalPrivacyControl` automatically on page load
- Persist opt-out server-side via API call for cross-device coverage
