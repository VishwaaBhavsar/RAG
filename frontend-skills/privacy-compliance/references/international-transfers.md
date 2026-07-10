# International Data Transfers

Use when EU/UK/Swiss user data is processed outside those jurisdictions (US servers, US SaaS tools, etc.).

## Legal Bases for Transfer

| Mechanism | When to Use | Status (2025) |
|-----------|------------|---------------|
| **EU-US Data Privacy Framework (DPF)** | US recipient certified under DPF | Valid (replaces Privacy Shield) |
| **Standard Contractual Clauses (SCCs)** | Any third country transfer | Valid — use 2021 EU SCCs |
| **UK IDTA** | UK → third country | Valid (use alongside or instead of EU SCCs) |
| **Adequacy Decision** | UK, Japan, Canada, Israel, etc. | Country-specific |
| **Binding Corporate Rules (BCRs)** | Intra-group, large multinationals | Complex, long approval |

## Privacy Policy — International Transfers section

```md
## International Data Transfers
Your data may be transferred to countries outside the EEA/UK/Switzerland (including the US).
Safeguards in place:
- **EU-US DPF:** Where US providers are DPF-certified (list: https://www.dataprivacyframework.gov/)
- **SCCs:** 2021 EU Standard Contractual Clauses (Module 2/3) for non-DPF transfers
- **UK IDTA:** For UK-originating transfers where SCCs are insufficient
To request a copy of specific safeguards, email [privacy@domain.com].
```

## Transfer Records (internal — not public)

| Recipient | Country | Data | Mechanism |
|-----------|---------|------|-----------|
| AWS | US | Hosted app data | SCCs (Module 2) + DPF certified |
| Stripe | US | Billing name/address, last 4 | DPF certified |
| SendGrid | US | Email address, name | SCCs (Module 2) |
| _(add all processors)_ | | | |

## SCCs — Module Reference

| Module | Transfer type |
|--------|--------------|
| 1 | Controller → Controller |
| 2 | Controller → Processor *(most common for SaaS)* |
| 3 | Processor → Processor |
| 4 | Processor → Controller |

SCCs text: https://commission.europa.eu/publications/standard-contractual-clauses-scc_en  
UK IDTA: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/

## Checklist
- [ ] International Transfers section in Privacy Policy
- [ ] Transfer mechanism identified for each third country
- [ ] US processors: check DPF list; if not certified, execute SCCs
- [ ] UK transfers: use IDTA or UK addendum to EU SCCs
- [ ] Transfer Impact Assessments documented internally
- [ ] Sub-processor list reflects countries of processing
- [ ] Privacy contact for safeguard requests documented
