# Accessible Forms — Reference

## Label Association (Required for Every Input)

```tsx
// Method 1: htmlFor + id (preferred)
<label htmlFor="item-name">Name <span aria-hidden="true">*</span></label>
<input id="item-name" type="text" required aria-required="true" />

// Method 2: wrapping label
<label>
  Email address
  <input type="email" />
</label>

// Method 3: aria-label (icon-only, search bars)
<input type="search" aria-label="Search records" />

// Method 4: aria-labelledby (visible text elsewhere on page)
<h2 id="form-title">Form Title</h2>
<form aria-labelledby="form-title">...</form>

// WRONG — placeholder is NOT a label
<input type="text" placeholder="Full name" />  // no label = inaccessible
```

## Required Fields

```tsx
// Indicate required visually AND programmatically
<fieldset>
  <legend>Contact information <span className="text-muted-foreground text-sm">(* required)</span></legend>

  <label htmlFor="email">
    Email <span aria-hidden="true" className="text-destructive">*</span>
  </label>
  <input id="email" type="email" required aria-required="true" />
</fieldset>
```

## Validation Errors

```tsx
// Pattern: error message linked via aria-describedby
function FormField({ id, label, error, ...props }) {
  const errorId = `${id}-error`;
  return (
    <div>
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        aria-describedby={error ? errorId : undefined}
        aria-invalid={!!error}
        {...props}
      />
      {error && (
        <p id={errorId} className="text-destructive text-sm mt-1" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

## Grouping Related Inputs

```tsx
// Always use fieldset + legend for radio/checkbox groups
<fieldset>
  <legend>Notification preferences</legend>
  <label>
    <input type="checkbox" name="notify-email" /> Email
  </label>
  <label>
    <input type="checkbox" name="notify-sms" /> SMS
  </label>
</fieldset>

// Date range — group with fieldset
<fieldset>
  <legend>Date range</legend>
  <label htmlFor="start-date">From</label>
  <input id="start-date" type="date" />
  <label htmlFor="end-date">To</label>
  <input id="end-date" type="date" />
</fieldset>
```

## Select / Dropdown

```tsx
<label htmlFor="category-select">Select category</label>
<select id="category-select" aria-required="true">
  <option value="">-- Choose a category --</option>
  <option value="option-a">Option A</option>
</select>
```

## Form Submission Feedback

```tsx
// Announce success/error after form submit
const [submitStatus, setSubmitStatus] = useState('');

<form onSubmit={handleSubmit}>
  {/* fields */}
  <button type="submit">Save</button>
</form>

{/* Live region outside form */}
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {submitStatus}
</div>
```

## Checklist

- [ ] Every `<input>`, `<select>`, `<textarea>` has a `<label>` or `aria-label`
- [ ] `htmlFor` on label matches `id` on input (exact, case-sensitive)
- [ ] Required fields have `required` attribute + visual indicator
- [ ] Errors use `aria-invalid` + `aria-describedby` pointing to error message
- [ ] Radio/checkbox groups are wrapped in `<fieldset><legend>`
- [ ] No placeholder-only labels
- [ ] Submit feedback announced via `aria-live`
