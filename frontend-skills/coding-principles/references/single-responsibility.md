# Single Responsibility Principle (SRP)

---

## Core Concept

A "reason to change" = a responsibility = an actor/stakeholder who might request changes.

---

## Quick Identification

| Question | Multiple Responsibilities If... |
|----------|--------------------------------|
| Who requests changes? | Multiple people/teams |
| What does it do? | Need "and" to describe |
| Can I name it specifically? | Name is vague (Manager, Handler, Utils) |

---

## Naming Indicators

| Red Flag | Better |
|----------|--------|
| `UserManager` | `UserAuthenticator`, `UserRepository` |
| `DataProcessor` | `OrderValidator`, `PaymentProcessor` |
| `HelperUtils` | `DateFormatter`, `CurrencyFormatter` |

---

## Refactoring Patterns

| Violation | Pattern | Action |
|-----------|---------|--------|
| Service does CRUD + Auth + Email | Split by actor | `UserRepository`, `AuthService`, `NotificationService` |
| Component fetches + calculates + renders | Extract hooks/utils | `useUser()`, `calculateTotal()`, UI component |
| Handler validates + processes + logs | Orchestrate | Handler calls validator, service, logger |

---

## Project References

| Pattern | Reference |
|---------|-----------|
| Service layer | `services/projectService.ts`, `services/workspaceService.ts` |
| Hooks separation | `hooks/project/useProjectQueries.ts`, `hooks/project/useProjectMutations.ts` |
| Query keys | `hooks/project/queryKeys.ts` |

---

## Levels of Application

| Level | Single Responsibility Means |
|-------|----------------------------|
| Function | Does one thing, named specifically |
| Class/Module | One actor requests changes |
| File | One concept per file |
| Folder | One domain per folder |

---

## Common Violations

| Violation | Sign | Fix |
|-----------|------|-----|
| God Object | Class with 50+ methods | Split by domain |
| Feature Envy | Function knows too much about other object's internals | Move logic to that object |
| Mixed Abstraction | High-level + low-level code together | Keep consistent abstraction |

---

## Testing Impact

| SRP Compliance | Testing Experience |
|----------------|-------------------|
| Single responsibility | Simple unit tests, minimal mocks |
| Multiple responsibilities | Complex setup, many mocks, brittle tests |

**Rule:** If testing requires more than 2-3 mocks, likely violating SRP.

---

## Code Review Triggers

Flag during review if:
- Function > 50 lines
- File > 300 lines
- Class > 10 methods
- Import list > 10 items
- Name contains "And", "Or", "Manager", "Handler"

---

## Trade-offs

| Situation | Pragmatic Choice |
|-----------|-----------------|
| Startup MVP | Ship fast, refactor later |
| Tight deadline | Document tech debt, create ticket |
| Simple CRUD | Single file acceptable |
| One-off script | Don't over-engineer |

**Remember:** Perfect is enemy of shipped. Refactor when pain is real, not theoretical.

---

## Checklist

- [ ] Can name the class/function specifically (not vaguely)
- [ ] Only one actor would request changes
- [ ] Description doesn't need "and"
- [ ] Easy to test in isolation (< 3 mocks)
