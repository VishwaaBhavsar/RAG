---
name: privacy-compliance
description: >
  Trigger when building any website, web app, landing page, dashboard, SaaS, portfolio,
  or e-commerce site. Also trigger for GDPR/CCPA compliance, consent management, privacy
  policies, or terms and conditions — even without explicit mention.
---

# Privacy Compliance — GDPR + CCPA + Privacy Policy + T&C

Auto-integrate all compliance below on every website build.
Skip only for: purely backend CLI, mobile, or desktop app with zero web-facing component.

## Mandatory (deliver all 8, always)

| # | Requirement | Ref |
|---|-------------|-----|
| 1 | **GDPR Cookie Banner** — opt-in before any tracking loads; Accept All / Reject All | `gdpr-consent-management.md` |
| 2 | **CCPA Do Not Sell** — `/do-not-sell` page; honour GPC signal | `ccpa-do-not-sell.md` |
| 3 | **Privacy Policy** `/privacy-policy` — data collected, legal basis, user rights, CCPA section | `privacy-policy.md` |
| 4 | **Terms & Conditions** `/terms` — acceptable use, liability, governing law | `terms-and-conditions.md` |
| 5 | **Consent Checkbox** on every form — unchecked by default, links to Privacy Policy | `gdpr-consent-management.md` |
| 6 | **Privacy Controls UI** — withdraw GDPR consent, CCPA opt-out; accessible from footer | `nextjs-implementation.md` |
| 7 | **Footer** on every page — Privacy Policy · Terms · Do Not Sell My Info | `nextjs-implementation.md` |
| 8 | **Analytics Gate** — load only after GDPR accept; skip if CCPA opted out | `ccpa-do-not-sell.md` |

## Conditional (load reference when trigger matches)

| Trigger | Reference | Adds |
|---------|-----------|------|
| Payments (Stripe, PayPal, checkout) | `payment-data-handling.md` | Refund Policy page, billing T&C, PCI DSS |
| SaaS / subscriptions / free trial | `subscription-terms.md` | Auto-renewal, cancellation flow, billing retention |
| Analytics pixels / embeds beyond necessary | `cookie-policy.md` | Cookie inventory table, `/cookies` page, granular consent |
| Children's audience / educational | `coppa-compliance.md` | Age gate, parental consent, UK Children's Code |
| B2B — customers process their users' data | `data-processing-agreement.md` | DPA page, sub-processor list, TOMs |
| UGC / API / messaging platform | `acceptable-use-policy.md` | AUP page, prohibited categories, abuse reporting |
| EU/UK users + US/non-EEA hosting or tools | `international-transfers.md` | SCCs, DPF, IDTA, transfer records |

## Reference Index

| File | Covers |
|------|--------|
| `gdpr-consent-management.md` | CookieBanner, ConsentCheckbox, consent rules |
| `ccpa-do-not-sell.md` | Opt-out page, GPC signal, analytics gate |
| `privacy-policy.md` | Required sections + page stub |
| `terms-and-conditions.md` | Required sections + page stub |
| `nextjs-implementation.md` | PrivacyControls, Footer, root layout |
| `compliance-checklist.md` | Full GDPR + CCPA + legal pages checklist |
| `payment-data-handling.md` | PCI DSS, refund policy, billing T&C |
| `cookie-policy.md` | Cookie table, `/cookies` page, granular consent |
| `subscription-terms.md` | SaaS billing, cancellation, data export |
| `coppa-compliance.md` | Under-13 protections, age gate, UK Children's Code |
| `data-processing-agreement.md` | B2B DPA, sub-processor list, TOMs |
| `acceptable-use-policy.md` | AUP, prohibited categories, moderation |
| `international-transfers.md` | SCCs, EU-US DPF, UK IDTA, TIA |
