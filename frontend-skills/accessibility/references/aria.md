# ARIA — Accessibility Reference

## Golden Rule

> Use native HTML semantics first. Add ARIA only when HTML alone cannot express the required role, state, or property.

---

## When to Use ARIA

| Situation | Solution |
|-----------|----------|
| Custom dropdown/combobox | `role="combobox"`, `aria-expanded`, `aria-controls` |
| Toggle button | `aria-pressed="true/false"` |
| Loading spinner | `role="status"`, `aria-label="Loading..."` |
| Icon-only button | `aria-label="Close dialog"` |
| Expanded/collapsed | `aria-expanded` on trigger, `aria-controls` pointing to panel |
| Required field | `aria-required="true"` (or use native `required` — prefer native) |
| Invalid field | `aria-invalid="true"` + `aria-describedby` pointing to error |
| Progress bar | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax` |

---

## Redundant ARIA — Never Add

```tsx
// WRONG — native semantics already provide these
<button role="button">          // button already has role=button
<h2 aria-level="2">             // h2 already has level 2
<input type="checkbox" role="checkbox">  // checkbox already implied
<a href="..." role="link">      // link already has role=link
<ul role="list">                // ul already has role=list (usually)
<img alt="logo" role="img">    // img already has role=img
```

---

## Common ARIA Patterns

### Toggle / Disclosure Button

```tsx
<button
  aria-expanded={isOpen}
  aria-controls="panel-id"
  onClick={() => setIsOpen(!isOpen)}
>
  {isOpen ? 'Hide details' : 'Show details'}
</button>
<div id="panel-id" hidden={!isOpen}>
  ...panel content...
</div>
```

### Icon-Only Button

```tsx
// Always add aria-label when there is no visible text
<button type="button" aria-label="Close dialog">
  <XIcon aria-hidden="true" />  {/* hide decorative icon from SR */}
</button>
```

### Tab Panel

```tsx
<div role="tablist" aria-label="Item status">
  <button role="tab" aria-selected={tab === 'unread'} aria-controls="unread-panel" id="tab-unread">
    Unread
  </button>
  <button role="tab" aria-selected={tab === 'read'} aria-controls="read-panel" id="tab-read">
    Read
  </button>
</div>
<div role="tabpanel" id="unread-panel" aria-labelledby="tab-unread" hidden={tab !== 'unread'}>
  ...
</div>
```

### Form Error Association

```tsx
<label htmlFor="item-name">Item name</label>
<input
  id="item-name"
  type="text"
  aria-describedby={error ? 'name-error' : undefined}
  aria-invalid={!!error}
/>
{error && (
  <p id="name-error" role="alert" className="text-destructive text-sm">
    {error}
  </p>
)}
```

### Loading State

```tsx
<button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? 'Saving...' : 'Save'}
</button>

// Spinner
<div role="status" aria-label="Loading items">
  <Spinner aria-hidden="true" />
</div>
```

### aria-hidden Usage

```tsx
// Hide decorative/duplicate content from screen readers
<Icon aria-hidden="true" />               // decorative icon next to text
<span aria-hidden="true">✓</span>         // visual checkmark (text handles meaning)

// NEVER hide focusable elements
// WRONG:
<button aria-hidden="true">Click</button>  // hidden but still focusable — broken
```

---

## Live Region Cheatsheet

| Scenario | Use |
|----------|-----|
| Status update (non-urgent) | `aria-live="polite"` |
| Critical error / alert | `role="alert"` (implies assertive) |
| Progress / loading message | `role="status"` (implies polite) |
| Real-time timer | `aria-live="assertive"` (use sparingly) |

```tsx
// Pattern: persistent live region that updates
const [message, setMessage] = useState('');

<div aria-live="polite" aria-atomic="true" className="sr-only">
  {message}
</div>

// Trigger: setMessage('Item updated successfully')
// Clear after delay to allow re-announcement of same message
```
