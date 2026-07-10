# DRY Principle (Don't Repeat Yourself)

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."

---

## Core Concept

DRY is about **knowledge**, not just code. Applies to: business logic, schemas, config, validation.

---

## Types of Duplication

| Type | Example | Fix |
|------|---------|-----|
| Code | Same calculation in 2 functions | Extract function |
| Knowledge | Magic number `18` scattered | Extract constant `LEGAL_AGE` |
| Data | Same regex in multiple files | Single `PATTERNS.EMAIL` constant |
| Structural | Similar type definitions | Compose with `&` or utility types |

---

## Extraction Patterns

| Pattern | When to Use | Project Reference |
|---------|-------------|-------------------|
| Extract Function | Same logic repeated | `services/*Service.ts` |
| Extract Constant | Magic numbers/strings | `constants/*.ts` |
| Extract Component | Same UI structure | `components/ui/*.tsx` |
| Extract Hook | Same state/effect logic | `hooks/*/*.ts` |
| Extract Type | Same shape repeated | `types/*.ts` |

---

## Project References

| Pattern | Reference |
|---------|-----------|
| Shared constants | `constants/routes.ts`, `constants/config.ts` |
| Reusable hooks | `hooks/workspace/useWorkspaceQueries.ts` |
| Shared types | `types/editor.ts`, `types/workspace.ts` |
| UI components | `components/ui/DeleteButton.tsx` |
| Validation | `lib/i18n/localization-enum.ts` (single source for keys) |

---

## When NOT to DRY

| Situation | Why |
|-----------|-----|
| Accidental similarity | Code looks same but represents different business rules |
| Premature abstraction | Wait for pattern to emerge (Rule of 3) |
| Wrong abstraction | Bad abstraction worse than duplication |
| Coupling concerns | DRY creates unwanted dependency between modules |

---

## Rule of Three

| Occurrence | Action |
|------------|--------|
| 1st time | Just write it |
| 2nd time | Note the duplication |
| 3rd time | Extract it |

---

## Trade-offs

| Situation | Pragmatic Choice |
|-----------|-----------------|
| 2 similar but different domains | Keep separate (avoid coupling) |
| Shared code across microservices | Duplicate > shared library complexity |
| Tight deadline | Ship, create refactor ticket |
| Uncertain requirements | Wait for pattern to stabilize |

**Remember:** Wrong abstraction is worse than duplication. When in doubt, duplicate.

---

## Technical Debt Impact

| Duplication Level | Debt Impact |
|-------------------|-------------|
| 2 copies | Low - note it |
| 3-5 copies | Medium - plan refactor |
| 5+ copies | High - immediate action |

---

## Checklist

- [ ] No magic numbers/strings (use constants)
- [ ] No copy-pasted logic (extract functions)
- [ ] No repeated types (compose or use utilities)
- [ ] Single source for validation rules
- [ ] Centralized configuration
- [ ] Duplication documented if intentional
