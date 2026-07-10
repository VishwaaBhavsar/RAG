---
name: coding-principles
description: Enforces clean code standards for this project — naming conventions, TypeScript strict mode, DRY, KISS, single responsibility, and file/folder structure. Use this skill when writing any new TypeScript or React code, creating files, writing hooks, utilities, or services, or when the code needs to follow project conventions.
---

# Coding Principles

> Fundamental principles for writing clean, maintainable, and scalable code.

---

## Quick Reference

| Principle | Key Idea | When to Apply |
|-----------|----------|---------------|
| **DRY** | Don't Repeat Yourself | Duplicated logic, copy-pasted code |
| **KISS** | Keep It Simple | Over-engineered solutions |
| **Separation of Concerns** | Divide by responsibility | Mixed business/UI/data logic |
| **Single Responsibility** | One reason to change | Classes/functions doing too much |

---

## References

| Principle | Reference File |
|-----------|---------------|
| **DRY** | [references/dry.md](references/dry.md) |
| **Single Responsibility** | [references/single-responsibility.md](references/single-responsibility.md) |
| **TypeScript** | [references/typescript.md](references/typescript.md) |

---

## DRY (Don't Repeat Yourself)

Every piece of knowledge should have a single, unambiguous representation.

**See:** [references/dry.md](references/dry.md)

---

## KISS (Keep It Simple, Stupid)

Prefer simple solutions over complex ones.

**Signs of violation:**
- Factory for a single implementation
- Abstraction with one concrete type
- Generics where none needed

---

## Separation of Concerns

Divide program into distinct sections, each addressing a separate concern.

**Project structure:**
```
app/
├── components/     # UI rendering
├── hooks/          # State and behavior
├── services/       # Business logic
├── types/          # TypeScript types and enums
└── utils/          # Pure utilities
```

---

## Single Responsibility Principle

A class/function should have only one reason to change.

**See:** [references/single-responsibility.md](references/single-responsibility.md)

---

## TypeScript Standards

Enterprise-level TypeScript coding standards.

**See:** [references/typescript.md](references/typescript.md)

---

## Applying Principles

### When Reviewing Code

1. **Spot duplication** → Extract shared logic (DRY)
2. **Check complexity** → Simplify if over-engineered (KISS)
3. **Count responsibilities** → Split if doing too much (SRP)
4. **Check responsibilities** → Separate if mixed concerns

### When Refactoring

| Smell | Principle Violated | Action |
|-------|-------------------|--------|
| Copy-pasted code | DRY | Extract shared logic |
| Over-engineered | KISS | Simplify, inline |
| God class/function | Single Responsibility | Split by responsibility |
| Spaghetti code | Separation of Concerns | Layer architecture |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description |
|--------------|-------------|
| Premature Optimization | Don't optimize before measuring |
| Cargo Cult Programming | Don't copy patterns without understanding |
| Golden Hammer | Don't use same solution for every problem |

---

## Summary

1. **DRY**: Extract duplication, but don't force wrong abstractions
2. **KISS**: Simplest solution that works
3. **Separation of Concerns**: Organize by responsibility
4. **Single Responsibility**: One job per unit, clear boundaries
5. **TypeScript**: Follow strict typing standards (see references/typescript.md)

