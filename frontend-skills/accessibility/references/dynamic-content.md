# Dynamic Content — Accessibility Reference

## aria-live Regions

```tsx
// Mount live region ONCE — update content to trigger announcement
// DO NOT mount/unmount the region itself — SR misses it

// Polite — waits for user to finish current action (most common)
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {statusMessage}
</div>

// Assertive — interrupts user immediately (use sparingly: errors only)
<div aria-live="assertive" aria-atomic="true" className="sr-only">
  {criticalError}
</div>

// role="status" — shorthand for aria-live="polite" + aria-atomic="true"
<div role="status" className="sr-only">{loadingStatus}</div>

// role="alert" — shorthand for aria-live="assertive" + aria-atomic="true"
<div role="alert">{errorMessage}</div>
```

## Re-announcing the Same Message

```tsx
// Problem: setting same text twice doesn't re-announce
// Solution: clear then set with a tick delay

const announce = useCallback((msg: string) => {
  setAnnouncement('');
  setTimeout(() => setAnnouncement(msg), 50);
}, []);

<div aria-live="polite" className="sr-only">{announcement}</div>
```

## Toast / Notification Pattern

```tsx
// Toasts must be announced — place live region in root layout
// src/app/layout.tsx

<div id="toast-announcer" aria-live="polite" aria-atomic="true" className="sr-only" />

// In toast utility — inject text into announcer
export function showSuccessToast(message: string) {
  const el = document.getElementById('toast-announcer');
  if (el) { el.textContent = ''; setTimeout(() => { el.textContent = message; }, 50); }
  // ... show visual toast
}
```

## Async Data Loading

```tsx
// Announce when data finishes loading
const { data, isLoading } = useItems();

<div role="status" aria-live="polite" className="sr-only">
  {isLoading ? 'Loading...' : `${data?.length ?? 0} items loaded`}
</div>
```

## Infinite Scroll / Pagination

```tsx
// Announce new items loaded
const [announcement, setAnnouncement] = useState('');

const loadMore = async () => {
  await fetchNextPage();
  setAnnouncement(`Loaded ${newItems.length} more items. Showing ${total} total.`);
};

<div aria-live="polite" className="sr-only">{announcement}</div>
<button onClick={loadMore}>Load more</button>
```

## Filter / Search Results

```tsx
// Announce result count after filter changes
const [resultAnnouncement, setResultAnnouncement] = useState('');

useEffect(() => {
  if (!isLoading) {
    setResultAnnouncement(`${filteredItems.length} results found`);
  }
}, [filteredItems.length, isLoading]);

<div role="status" aria-live="polite" className="sr-only">
  {resultAnnouncement}
</div>
```

## SPA Route Announcements

```tsx
// src/components/providers/RouteAnnouncer.tsx
'use client';
import { usePathname } from 'next/navigation';
import { useEffect, useRef } from 'react';

export function RouteAnnouncer() {
  const pathname = usePathname();
  const ref = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    // Short delay to let new page render its <title>
    const timer = setTimeout(() => {
      if (ref.current) ref.current.textContent = document.title;
    }, 100);
    return () => clearTimeout(timer);
  }, [pathname]);

  return <p ref={ref} aria-live="assertive" aria-atomic="true" className="sr-only" />;
}
```

## Checklist

- [ ] All status updates (save, delete, filter, load) have `aria-live` announcement
- [ ] Live region is mounted once — content updated, not region itself
- [ ] Toasts/notifications are announced via live region
- [ ] Route changes announce new page title
- [ ] Infinite scroll announces newly loaded count
- [ ] Same-message re-announcement uses clear + delay pattern
