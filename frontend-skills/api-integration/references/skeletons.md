# Skeleton Components

Loading skeletons that mirror actual content layout.

---

## Finding Existing Skeletons

**Location:** `apps/frontend/src/components/skeletons/`

```bash
# Check for existing skeletons
ls apps/frontend/src/components/skeletons/
```

Use existing skeleton if available. If not, create one that mirrors the real component layout.

---

## Creating Skeletons

The skeleton must **mirror the layout** of the actual content to prevent layout shifts.

### Card List Skeleton

```typescript
// apps/frontend/src/components/skeletons/WorkspacesSkeleton.tsx
import { Skeleton, Card, CardContent, CardHeader } from '@/components'

export function WorkspacesSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: count }).map((_, i) => (
        <Card key={i}>
          <CardHeader className="space-y-2">
            <Skeleton className="h-5 w-2/3" />  {/* Title */}
            <Skeleton className="h-4 w-1/3" />  {/* Subtitle */}
          </CardHeader>
          <CardContent className="space-y-2">
            <Skeleton className="h-4 w-full" />   {/* Description line 1 */}
            <Skeleton className="h-4 w-4/5" />    {/* Description line 2 */}
            <Skeleton className="h-8 w-24 mt-4" /> {/* Action button */}
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

### Table Skeleton

```typescript
// apps/frontend/src/components/skeletons/UsersTableSkeleton.tsx
import {
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components'

export function UsersTableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Email</TableHead>
          <TableHead>Role</TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Array.from({ length: rows }).map((_, i) => (
          <TableRow key={i}>
            <TableCell><Skeleton className="h-4 w-32" /></TableCell>
            <TableCell><Skeleton className="h-4 w-48" /></TableCell>
            <TableCell><Skeleton className="h-4 w-16" /></TableCell>
            <TableCell><Skeleton className="h-8 w-20" /></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### Detail Page Skeleton

```typescript
// apps/frontend/src/components/skeletons/WorkspaceDetailSkeleton.tsx
import { Skeleton } from '@/components'

export function WorkspaceDetailSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Skeleton className="h-12 w-12 rounded-full" /> {/* Avatar */}
        <div className="space-y-2">
          <Skeleton className="h-6 w-48" />  {/* Name */}
          <Skeleton className="h-4 w-32" />  {/* Subtitle */}
        </div>
      </div>

      {/* Body */}
      <div className="space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-3/4" />
      </div>

      {/* Actions */}
      <div className="flex gap-3">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>
  )
}
```

---

## Key Rules

- Mirror the real component's layout exactly
- Use varying widths (`w-1/3`, `w-2/3`, `w-full`) for natural look
- Include all major elements (titles, buttons, avatars)
- Accept `count` or `rows` prop for lists/tables
