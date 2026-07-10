# COPPA Compliance (Children's Privacy)

## Legal Requirements

| Regulation | Age Threshold | Key Requirement |
|-----------|--------------|----------------|
| COPPA (US) | Under 13 | Verifiable parental consent before collecting any personal data |
| GDPR (EU) | Under 16 (member states may lower to 13) | Parental/guardian consent for data processing |
| UK GDPR | Under 13 | Age-appropriate design code (Children's Code) |
| PIPEDA (Canada) | Under 13 | Parental consent for sensitive data |

## Privacy Policy — Children's Privacy section

```md
## Children's Privacy
Our services are not directed to children under 13 (or 16 in EU/UK). We do not knowingly collect data from children under these ages.
Parents/guardians who believe their child has provided data without consent should contact [privacy@domain.com] — we will delete it within 30 days.
```

## Terms & Conditions — Age Requirements section

```md
## Age Requirements
You must be at least 13 (or 16 in the EU) to use our services. Users aged 13–18 must have parental permission and their parent must agree to these Terms.
```

## AgeVerification Component

```tsx
// apps/frontend/src/components/auth/AgeVerification.tsx
'use client';
import { useState } from 'react';

export default function AgeVerification({ minAge = 13, onVerified, onFailed }: {
  minAge?: number; onVerified: () => void; onFailed: () => void;
}) {
  const [dob, setDob] = useState('');
  const verify = () => {
    const age = Math.floor((Date.now() - new Date(dob).getTime()) / (365.25 * 24 * 60 * 60 * 1000));
    age >= minAge ? onVerified() : onFailed();
  };
  return (
    <div role="dialog" aria-labelledby="age-gate-title" aria-modal="true">
      <h2 id="age-gate-title">Age Verification</h2>
      <label htmlFor="dob">Date of birth</label>
      <input id="dob" type="date" value={dob} onChange={e => setDob(e.target.value)}
        max={new Date().toISOString().split('T')[0]} aria-required="true" />
      <button type="button" onClick={verify} disabled={!dob}>Verify age</button>
      <p className="text-sm">We do not store your date of birth — check is local only.</p>
    </div>
  );
}
```

## Parental Consent Page — `/parental-consent`

Only needed when service is directed AT children. Fields: parent name + email, child name + age, data summary, explicit consent checkbox, submit (sends email verification to parent).

## UK Children's Code (Age-Appropriate Design)

| Requirement | Implementation |
|-------------|---------------|
| Best interests | Default settings must be privacy-protective |
| Data minimisation | Collect only what is strictly necessary |
| No profiling | Do not profile children for marketing |
| No nudge techniques | No dark patterns pressuring children |
| Parental controls | Tools for parents to manage child's data |
| Geolocation off by default | Never default to sharing location |
| No targeted advertising | Children's data must not be used for ads |

## Checklist
- [ ] Children's Privacy section in Privacy Policy
- [ ] Age restriction in Terms & Conditions
- [ ] Age gate on registration if service may attract minors
- [ ] No targeted advertising to users identified as minors
- [ ] No profiling or behavioural tracking of minors
- [ ] Parental consent page if service is directed at children
- [ ] Data deletion process for underage accounts
- [ ] UK Children's Code requirements if UK audience includes minors
