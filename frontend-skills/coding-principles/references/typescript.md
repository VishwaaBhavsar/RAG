# TypeScript Standards

Enterprise-level TypeScript coding standards for type safety and maintainability.

---

## 1. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interface | PascalCase, noun | `User`, `ProjectSettings` |
| Type alias | PascalCase | `UserId`, `ApiResponse` |
| Enum | PascalCase, singular | `ProjectStatus`, `EditorTabId` |
| Enum values | UPPER_SNAKE_CASE | `EditorTabId.PREVIEW` |
| Generic | Single uppercase or descriptive | `T`, `TData`, `TError` |
| Props interface | `ComponentNameProps` | `ButtonProps`, `ProjectCardProps` |

---

## 2. Use Enums for Conditional Rendering

When rendering content conditionally based on identifiers (tabs, views, modes, status), always use enums instead of hardcoded strings.

**Location:** `types/` folder

**Reference:** `types/editor.ts` (EditorTabId enum), `app/(private)/editor/page.tsx` (usage)

| Use Case | Example |
|----------|---------|
| Tab identifiers | `EditorTabId.PREVIEW`, `EditorTabId.SETTINGS` |
| View modes | `ViewMode.GRID`, `ViewMode.LIST` |
| Status values | `ProjectStatus.DRAFT`, `ProjectStatus.PUBLISHED` |
| Step identifiers | `WizardStep.INFO`, `WizardStep.REVIEW` |

---

## 3. Strict Type Annotations

| Rule | Avoid | Prefer |
|------|-------|--------|
| No `any` | `any` | `unknown`, specific type, or generic `<T>` |
| Explicit types | Implicit `any` | Explicit type annotation |
| Type narrowing | Type assertions `as` | Type guards |
| Return types | Implicit return | Explicit return type annotation |

---

## 4. Utility Types

Use built-in utility types to reduce boilerplate.

| Utility | Usage |
|---------|-------|
| `Partial<T>` | All properties optional (updates, patches) |
| `Required<T>` | All properties required |
| `Pick<T, K>` | Select specific properties |
| `Omit<T, K>` | Exclude specific properties |
| `Record<K, V>` | Dictionary/map types |
| `ReturnType<T>` | Extract function return type |
| `Parameters<T>` | Extract function parameters |

---

## 5. Interface vs Type

| Use | When |
|-----|------|
| `interface` | Object shapes, extensible contracts, class implementations |
| `type` | Unions, intersections, primitives, tuples, mapped types |

---

## 6. Readonly and Immutability

| Pattern | Usage |
|---------|-------|
| `readonly` | Object properties that shouldn't change |
| `as const` | Literal types for constants and enums |
| `ReadonlyArray<T>` | Arrays that shouldn't be mutated |
| `Readonly<T>` | Make all properties readonly |

---

## 7. Nullability

| Pattern | Usage |
|---------|-------|
| Optional chaining `?.` | Safe property access |
| Nullish coalescing `??` | Default values (prefer over `\|\|`) |
| Non-null assertion `!` | Avoid unless absolutely certain |
| Optional property `?:` | Properties that may not exist |

---

## 8. Type Guards

Use type guards for runtime type checking and narrowing.

| Pattern | Usage |
|---------|-------|
| `typeof` | Primitive checks |
| `instanceof` | Class instance checks |
| `in` operator | Property existence |
| Custom guard | `function isUser(x): x is User` |

---

## 9. Discriminated Unions

Use discriminated unions for type-safe conditional logic with exhaustive checks.

**Reference:** `services/projectService.ts` (ConversationStreamChunk type)

| Pattern | Usage |
|---------|-------|
| Discriminant property | `type: 'success' \| 'error'` |
| Exhaustive check | `never` type in default case |

---

## 10. Function Types

| Pattern | Usage |
|---------|-------|
| Arrow function type | `type Handler = (e: Event) => void` |
| Async function | `type AsyncFn = () => Promise<Data>` |
| Callback with generics | `type Callback<T> = (data: T) => void` |
| Overloads | Multiple signatures for same function |

---

## 11. Generic Constraints

Use constraints to ensure type safety in generics.

| Pattern | Usage |
|---------|-------|
| `extends` | `<T extends BaseType>` |
| Multiple constraints | `<T extends A & B>` |
| Default type | `<T = DefaultType>` |

**Reference:** `hooks/workspace/useWorkspaceMutations.ts` (mutation generics)

---

## 12. Export Patterns

| Pattern | Usage |
|---------|-------|
| Named exports | Prefer for most exports |
| Barrel exports | `index.ts` for public API |
| Type-only exports | `export type { }` for types |
| Type-only imports | `import type { }` for types |

---

## 13. File Organization

```
types/
├── editor.ts       # EditorTabId enum
├── project.ts      # Project-related types
├── workspace.ts    # Workspace-related types
└── common.ts       # Shared utility types
```

---

## Checklist

**Type Safety:**
- [ ] No `any` types (use `unknown` or generics)
- [ ] Explicit return types on functions
- [ ] Type guards for runtime checks
- [ ] Exhaustive checks with `never` in switches

**Consistency:**
- [ ] Follow naming conventions (PascalCase for types)
- [ ] Props interface named `ComponentNameProps`
- [ ] Enums for conditional identifiers (tabs, modes, status)

**Immutability:**
- [ ] `readonly` for immutable properties
- [ ] `as const` for constant objects
- [ ] `Readonly<T>` for frozen objects

**Best Practices:**
- [ ] Use utility types (Partial, Pick, Omit)
- [ ] Discriminated unions for variant types
- [ ] Type-only imports where applicable
- [ ] Generic constraints for type safety
