# Semantic HTML — Accessibility Reference

> For landmark regions and heading hierarchy patterns, see `seo/references/semantic-html.md` — covers `<main>`, `<nav>`, `<header>`, `<footer>`, `<article>`, `<section>`, heading rules, lists, and `<figure>`.

---

## Element Selection — Interactive Elements

This is the accessibility-specific concern: choosing the **right HTML element** so keyboard and screen reader support is built-in.

| Intent | Use | Never use |
|--------|-----|-----------|
| Click action (no navigation) | `<button type="button">` | `<div onClick>`, `<span onClick>` |
| Navigate to URL | `<a href="...">` | `<div onClick>` with `router.push` |
| Toggle / expand | `<button aria-expanded>` | `<div onClick>` |
| Submit form | `<button type="submit">` | `<div onClick>` |
| Data table | `<table><thead><tbody><th scope>` | nested divs |
| List of items | `<ul><li>` or `<ol><li>` | `<div>` per item |

```tsx
// CORRECT
<button type="button" onClick={handleClick}>Save</button>
<a href="/items/123">View details</a>

// WRONG — no keyboard support, no screen reader role
<div onClick={handleClick}>Save</div>
<span onClick={() => router.push('/items/123')}>View details</span>
```

---

## Multiple Nav Landmarks — Use aria-label

```tsx
// Without aria-label, screen readers just say "navigation" for each
<nav aria-label="Main navigation">...</nav>
<nav aria-label="Breadcrumb">...</nav>
<nav aria-label="Pagination">...</nav>
```

---

## Accessible Tables

Always include `caption` and `scope` on header cells — these are required for screen readers to associate data with headers.

```tsx
<table>
  <caption>Monthly activity summary</caption>
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">Name</th>
      <th scope="col">Count</th>
      <th scope="col">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2026-03-28</td>
      <td>Item A</td>
      <td>3</td>
      <td>Active</td>
    </tr>
  </tbody>
</table>

// Row headers (e.g., comparison tables)
<th scope="row">Feature name</th>
```
