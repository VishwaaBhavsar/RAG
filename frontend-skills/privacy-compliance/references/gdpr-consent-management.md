# GDPR — Consent Management

## CookieBanner (Next.js)

```tsx
'use client';
import { useEffect, useState } from 'react';

const CONSENT_KEY = 'gdpr_consent';

export default function CookieBanner() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem(CONSENT_KEY)) setVisible(true);
  }, []);

  const accept = () => { localStorage.setItem(CONSENT_KEY, 'accepted'); setVisible(false); loadAnalytics(); };
  const reject = () => { localStorage.setItem(CONSENT_KEY, 'rejected'); setVisible(false); };

  if (!visible) return null;

  return (
    <div role="dialog" aria-labelledby="cb-title" className="fixed bottom-0 inset-x-0 bg-white border-t shadow-lg p-4 z-50">
      <p id="cb-title" className="font-semibold mb-1">We use cookies</p>
      <p className="text-sm text-gray-600 mb-3">
        See our <a href="/privacy-policy" className="underline">Privacy Policy</a> and{' '}
        <a href="/privacy-policy#cookies" className="underline">Cookie Policy</a>.
      </p>
      <div className="flex gap-3">
        <button onClick={accept} className="bg-black text-white px-4 py-2 rounded text-sm">Accept All</button>
        <button onClick={reject} className="border px-4 py-2 rounded text-sm">Reject All</button>
      </div>
      <p className="text-xs text-gray-400 mt-2">
        California residents: <a href="/do-not-sell" className="underline">Do Not Sell My Info</a>
      </p>
    </div>
  );
}

function loadAnalytics() {
  // inject analytics script only after consent
}
```

## ConsentCheckbox (all forms)

```tsx
import { forwardRef } from 'react';

const ConsentCheckbox = forwardRef<HTMLInputElement, { error?: string }>(({ error, ...props }, ref) => (
  <div>
    <label className="flex items-start gap-2 text-sm cursor-pointer">
      <input ref={ref} type="checkbox" className="mt-0.5 shrink-0" {...props} />
      <span>
        I agree to the{' '}
        <a href="/privacy-policy" target="_blank" rel="noopener noreferrer" className="underline text-blue-600">
          Privacy Policy
        </a>{' '}
        and consent to my data being processed.
      </span>
    </label>
    {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
  </div>
));
ConsentCheckbox.displayName = 'ConsentCheckbox';
export default ConsentCheckbox;

// react-hook-form usage:
// <ConsentCheckbox
//   {...register('consent', { required: 'You must agree to the Privacy Policy' })}
//   error={errors.consent?.message as string}
// />
```

## Rules
- Never pre-check the checkbox — always opt-in
- Track `version` so policy changes can trigger re-consent
- Store `ipAddress` + `userAgent` as proof of consent
