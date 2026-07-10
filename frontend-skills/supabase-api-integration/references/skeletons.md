# Skeleton Components (TanStack Query + Supabase)

Loading skeletons that mirror actual content layout. Use with **`get-with-skeleton.md`** loading states.

**Location:** `apps/frontend/src/components/skeletons/`

Reuse an existing skeleton when one matches the domain; otherwise create one that mirrors the real layout to avoid CLS.

---

## Card list skeleton

```typescript
import { Skeleton, Card, CardContent, CardHeader } from '@/components'

export function ProjectsSkeleton({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: count }).map((_, i) => (
        <Card key={i}>
          <CardHeader className="space-y-2">
            <Skeleton className="h-5 w-2/3" />
            <Skeleton className="h-4 w-1/3" />
          </CardHeader>
          <CardContent className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-4/5" />
            <Skeleton className="h-8 w-24 mt-4" />
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

---

## Table skeleton

```typescript
import {
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components'

export function TasksTableSkeleton({ rows = 5 }: { rows?: number }) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Name</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {Array.from({ length: rows }).map((_, i) => (
          <TableRow key={i}>
            <TableCell><Skeleton className="h-4 w-32" /></TableCell>
            <TableCell><Skeleton className="h-4 w-24" /></TableCell>
            <TableCell><Skeleton className="h-8 w-20" /></TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

---

## Detail page skeleton

```typescript
import { Skeleton } from '@/components'

export function ProjectDetailSkeleton() {
  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Skeleton className="h-12 w-12 rounded-full" />
        <div className="space-y-2">
          <Skeleton className="h-6 w-48" />
          <Skeleton className="h-4 w-32" />
        </div>
      </div>
      <div className="space-y-3">
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-5/6" />
        <Skeleton className="h-4 w-3/4" />
      </div>
      <div className="flex gap-3">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>
  )
}
```

---

## Rules

- Mirror the real component layout; use varying widths (`w-1/3`, `w-2/3`, `w-full`).
- Include major blocks (titles, actions, avatars) so the shell matches the loaded UI.
- Lists/tables: accept `count` or `rows` props.

---

## Related

- **components** skill for `Skeleton`, `Card`, `Table` imports and patterns.
