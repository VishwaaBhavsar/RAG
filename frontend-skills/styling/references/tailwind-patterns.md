# Tailwind Patterns

> Common layout and responsive patterns.
> **References:** [Tailwind CSS](https://tailwindcss.com/) | [Utility Classes Docs](https://tailwindcss.com/docs/styling-with-utility-classes)

---

## Layout Patterns

```tsx
// Responsive card grid
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  {items.map(item => <Card key={item.id} />)}
</div>

// Sidebar layout
<div className="flex">
  <aside className="w-64 shrink-0" />
  <main className="flex-1 min-w-0" />
</div>

// Flex patterns
<div className="flex items-center justify-between" />  // Space between
<div className="flex items-center justify-center" />   // Centered
<div className="flex items-center gap-3" />            // With gap
<div className="flex flex-col gap-4" />                // Column
```

---

## Centering content

Ways to center content with utility classes:

| Goal | Classes | Use when |
|------|---------|----------|
| **Flex: both axes** | `flex items-center justify-center` | Center a child in a flex parent (horizontal + vertical) |
| **Flex: column** | `flex flex-col items-center justify-center` | Stack vertically, center horizontally |
| **Grid** | `grid place-items-center` | Center single item in both axes; no flex needed |
| **Grid (content)** | `grid place-content-center` | Center grid content as a block |
| **Block + horizontal** | `mx-auto` | Center a block horizontally (element needs width, e.g. `w-full` or `max-w-*`) |
| **Text** | `text-center` | Center inline/text content |
| **Container** | Parent of `.container`: `flex items-center justify-center` (required) | Required when wrapper has a `.container` child so content centers |

```tsx
// flex: flex items-center justify-center
// grid: grid place-items-center
// block: mx-auto max-w-4xl
// text: text-center
```

### Container centering (required when using `.container`)

When using `.container` inside a wrapper, the wrapper does not center the container by itself. **Always** add `flex items-center justify-center` to the wrapper so content is centered.

**Rule:** Every element (`<section>`, `<nav>`, `<footer>`, `<header>`, `<div>`) that has a `.container` child must have `flex items-center justify-center`.

```tsx
<section className="py-24 flex items-center justify-center">
  <div className="container">...</div>
</section>
```

---

## Responsive Design

### Breakpoints

| Breakpoint | Min Width | Usage |
|------------|-----------|-------|
| `sm:` | 640px | Small devices (phones landscape) |
| `md:` | 768px | Medium devices (tablets) |
| `lg:` | 1024px | Large devices (laptops) |
| `xl:` | 1280px | Extra large (desktops) |
| `2xl:` | 1536px | Wide screens |

### Responsive Classes

| Category | Classes | Description |
|----------|---------|-------------|
| **Display** | `hidden`, `block`, `inline`, `flex`, `grid` | Control element visibility/type |
| **Flex Direction** | `flex-row`, `flex-col`, `flex-row-reverse` | Main axis direction |
| **Flex Wrap** | `flex-wrap`, `flex-nowrap` | Allow items to wrap |
| **Flex Grow/Shrink** | `flex-1`, `flex-auto`, `flex-none`, `shrink-0` | Item sizing behavior |
| **Grid Columns** | `grid-cols-1`, `grid-cols-2`, `grid-cols-3`, `grid-cols-4` | Number of columns |
| **Gap** | `gap-2`, `gap-4`, `gap-6`, `gap-x-4`, `gap-y-2` | Spacing between items |
| **Justify** | `justify-start`, `justify-center`, `justify-between`, `justify-end` | Main axis alignment |
| **Align** | `items-start`, `items-center`, `items-end`, `items-stretch` | Cross axis alignment |
| **Width** | `w-full`, `w-1/2`, `w-auto`, `min-w-0`, `max-w-md` | Element width |
| **Padding** | `p-4`, `px-6`, `py-2`, `pt-4`, `pb-0` | Internal spacing |
| **Margin** | `m-4`, `mx-auto`, `my-2`, `mt-4`, `mb-0` | External spacing |

### Mobile-first pattern

Base styles = mobile; add breakpoint prefixes for larger screens. Do not use desktop-first.

```tsx
// CORRECT: Mobile-first (base = mobile, add prefixes for larger)
<h1 className="text-2xl md:text-4xl lg:text-6xl">Title</h1>
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
<div className="px-4 md:px-6 lg:px-8">
<div className="hidden lg:block">  // Show only on desktop
<div className="lg:hidden">        // Hide on desktop

// WRONG: Desktop-first (don't do this)
<h1 className="text-6xl sm:text-4xl xs:text-2xl">
```

### Common responsive patterns

```tsx
// Hide on mobile, show on desktop
<div className="hidden md:block" />
<div className="hidden md:flex">Desktop nav</div>
<div className="md:hidden">Mobile menu</div>

// Stack on mobile, row on desktop
<div className="flex flex-col md:flex-row gap-4" />

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" />
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6 lg:gap-8">

// Typography scaling
<h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold">

// Padding/spacing
<section className="py-12 md:py-16 lg:py-24 px-4 md:px-6">

// Button sizing
<Button className="w-full sm:w-auto">
```

### Flex row overflow

Single-line rows (headers/toolbars): **`flex-1 min-w-0`** on the main area, **`truncate`** on long text, **`shrink-0`** on icons; avoid **`w-full`** unless inside **`flex-1 min-w-0`**. **`flex-wrap`**: use for chips/filters; avoid for single-line toolbars.

```tsx
<div className="flex items-center gap-2 min-w-0">
  <div className="flex-1 min-w-0">
    <Button className="w-full min-w-0 justify-start">
      <span className="truncate">Title…</span>
    </Button>
  </div>
  <Button size="icon" className="shrink-0" aria-label="Close" />
</div>

// Generic overflow helpers
<p className="line-clamp-2">{description}</p>
<ScrollArea className="h-[300px]">...</ScrollArea>
```

### Collapsible sidebar (mobile off-canvas)

Use off-canvas on small screens, and a static sidebar on desktop.

```tsx
<aside
  className={cn(
    'w-64 shrink-0 border-r',
    'fixed inset-y-0 left-0 md:static',
    'transition-transform duration-200 ease-out md:translate-x-0',
    isOpen ? 'translate-x-0' : '-translate-x-full',
  )}
/>
```

---

## Empty/Loading States

```tsx
<div className="flex flex-col items-center justify-center gap-4 p-8 text-center">
  <div className="size-12 rounded-full bg-muted flex items-center justify-center">
    <Icon className="size-6 text-muted-foreground" />
  </div>
  <h3 className="text-lg font-semibold">No items</h3>
  <p className="text-sm text-muted-foreground max-w-md">Message</p>
</div>
```

---

## Z-Index Layers

| Layer | Z-Index | Usage |
|-------|---------|-------|
| Dropdown | `z-10` | Menus, popovers |
| Sticky | `z-20` | Sticky headers |
| Overlay | `z-30` | Overlay backgrounds |
| Modal | `z-40` | Dialogs, sheets |
| Toast | `z-50` | Notifications |

> shadcn/ui components handle z-index internally.
