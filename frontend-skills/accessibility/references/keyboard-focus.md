# Keyboard & Focus — Accessibility Reference

## Focus Ring — Never Remove

```css
/* WRONG — destroys keyboard accessibility */
* { outline: none; }
button:focus { outline: none; }

/* CORRECT — remove outline only for pointer, keep for keyboard */
button:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 2px; }
button:focus:not(:focus-visible) { outline: none; }
```

## Tailwind Focus Pattern

```tsx
// Use focus-visible, not focus (avoids showing ring on mouse click)
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2">
  Click me
</button>
```

## Tab Order — Natural DOM Order

```tsx
// tabIndex rules
tabIndex={0}   // ONLY to make non-interactive element focusable (rare — prefer semantic HTML)
tabIndex={-1}  // Focusable programmatically but not in tab order (e.g., modal container)
tabIndex={1+}  // NEVER — breaks natural tab sequence
```

## Focus Trapping in Modals

```tsx
// Use Dialog from @/components — it handles trap + restore
import { Dialog, DialogContent } from '@/components';

// If building custom modal
import { useEffect, useRef } from 'react';

function Modal({ isOpen, onClose, triggerRef }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    // Focus first focusable element on open
    const focusable = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    (focusable?.[0] as HTMLElement)?.focus();
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
      triggerRef.current?.focus(); // restore
    }
  };

  return (
    <div ref={modalRef} role="dialog" aria-modal="true" onKeyDown={handleKeyDown}>
      ...
      <button onClick={() => { onClose(); triggerRef.current?.focus(); }}>Close</button>
    </div>
  );
}
```

## Route Change Focus (Next.js App Router)

```tsx
// src/components/providers/RouteAnnouncer.tsx
// Announce page title on route change for screen readers
'use client';
import { usePathname } from 'next/navigation';
import { useEffect, useRef } from 'react';

export function RouteAnnouncer() {
  const pathname = usePathname();
  const ref = useRef<HTMLParagraphElement>(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.textContent = `Navigated to ${document.title}`;
    }
  }, [pathname]);

  return (
    <p
      ref={ref}
      aria-live="assertive"
      aria-atomic="true"
      className="sr-only"
    />
  );
}
```

## Keyboard Patterns by Component

| Component | Keys required |
|-----------|--------------|
| Button | `Enter`, `Space` |
| Link | `Enter` |
| Checkbox | `Space` to toggle |
| Radio group | `Arrow` keys within group |
| Dropdown/Select | `Enter` to open, `Arrow` to navigate, `Escape` to close |
| Modal/Dialog | `Escape` to close, `Tab` trapped inside |
| Tabs | `Arrow` keys to switch tabs |
| Accordion | `Enter`/`Space` to expand |
| Combobox | `Arrow` to navigate options, `Enter` to select |

## Skip Link (Add Once at Root Layout)

```tsx
// src/app/layout.tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:fixed focus:top-4 focus:left-4 focus:z-[9999] focus:px-4 focus:py-2 focus:bg-white focus:text-primary focus:rounded focus:shadow-lg"
>
  Skip to main content
</a>
```
