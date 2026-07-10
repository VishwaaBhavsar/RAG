# Terms & Conditions Page (`/terms`)

## Required Sections

| Section | Must Cover |
|---------|-----------|
| Acceptance | Using the site = agreement to terms; must stop using if they disagree |
| Service Description | What the site does; who can use it (age/geo restrictions) |
| User Responsibilities | Accurate info, account security, lawful use |
| Acceptable Use | No illegal content, no IP infringement, no scraping/hacking, no harassment |
| Intellectual Property | All content/code owned by company; user-generated content licence |
| Limitation of Liability | "As is" — no indirect/consequential damages; max liability cap |
| Third-Party Links | Company not responsible for third-party sites |
| Termination | Company may suspend for violations; users may close account |
| Governing Law | Jurisdiction and applicable law (no blanks in production) |
| Changes | How users are notified; continued use = acceptance |
| Contact | Legal/support email |

## Next.js Page Stub

```tsx
// apps/frontend/src/app/terms/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms & Conditions',
  description: 'The terms governing your use of our service.',
};

export default function TermsPage() {
  return (
    <main className="max-w-3xl mx-auto px-4 py-16 prose">
      <h1>Terms & Conditions</h1>
      <p className="text-sm text-gray-500">Effective date: [date]</p>
      {/* Populate all sections from Required Sections table above */}
    </main>
  );
}
```

## Rules
- Never leave jurisdiction blank in production
- Link from footer of every page
- If users must actively accept T&C at signup, add a separate T&C checkbox alongside the Privacy Policy checkbox
- Update effective date on every material change
