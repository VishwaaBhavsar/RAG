# UI Primitives

> Base shadcn/ui components in `apps/frontend/src/components/ui/`
> **Do not modify directly** - create wrappers if needed.

## Buttons

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Button` | `@/components` | `ui/Button.tsx` | Button with variants (default, destructive, outline, secondary, ghost, link) |
| `ButtonWithIcon` | `@/components` | `ui/ButtonWithIcon.tsx` | Button with leading icon |
| `ButtonWithLoader` | `@/components` | `ui/ButtonWithLoader.tsx` | Button with loading spinner |
| `DeleteButton` | `@/components` | `ui/DeleteButton.tsx` | Delete with confirmation |
| `Toggle` | `@/components` | `ui/Toggle.tsx` | Toggle button |
| `ToggleGroup` | `@/components` | `ui/ToggleGroup.tsx` | Grouped toggles |

## Form Inputs

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Input` | `@/components` | `ui/Input.tsx` | Text input |
| `Textarea` | `@/components` | `ui/Textarea.tsx` | Multi-line input |
| `Select` | `@/components` | `ui/Select.tsx` | Dropdown select |
| `Checkbox` | `@/components` | `ui/Checkbox.tsx` | Checkbox input |
| `RadioGroup` | `@/components` | `ui/RadioGroup.tsx` | Radio buttons |
| `Switch` | `@/components` | `ui/Switch.tsx` | Toggle switch |
| `Slider` | `@/components` | `ui/Slider.tsx` | Range slider |
| `Calendar` | `@/components` | `ui/Calendar.tsx` | Date picker calendar |
| `InputOtp` | `@/components` | `ui/InputOtp.tsx` | OTP input |
| `Label` | `@/components` | `ui/Label.tsx` | Form label |
| `Form` | `@/components` | `ui/Form.tsx` | React Hook Form wrapper |

## Layout

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter` | `@/components` | `ui/Card.tsx` | Card container |
| `Tabs, TabsList, TabsTrigger, TabsContent` | `@/components` | `ui/Tabs.tsx` | Tabbed interface |
| `Accordion` | `@/components` | `ui/Accordion.tsx` | Collapsible sections |
| `Separator` | `@/components` | `ui/Separator.tsx` | Visual divider |
| `ScrollArea` | `@/components` | `ui/ScrollArea.tsx` | Custom scrollbar |
| `Resizable` | `@/components` | `ui/Resizable.tsx` | Resizable panels |
| `AspectRatio` | `@/components` | `ui/AspectRatio.tsx` | Maintain aspect ratio |
| `Collapsible` | `@/components` | `ui/Collapsible.tsx` | Collapsible container |

## Navigation

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Sidebar` | `@/components` | `ui/Sidebar.tsx` | App sidebar |
| `NavigationMenu` | `@/components` | `ui/NavigationMenu.tsx` | Navigation with dropdowns |
| `Breadcrumb` | `@/components` | `ui/Breadcrumb.tsx` | Navigation breadcrumbs |
| `Pagination` | `@/components` | `ui/Pagination.tsx` | Page navigation |
| `Menubar` | `@/components` | `ui/Menubar.tsx` | Horizontal menubar |

## Overlay & Dialog

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter` | `@/components` | `ui/Dialog.tsx` | Modal dialog |
| `AlertDialog` | `@/components` | `ui/AlertDialog.tsx` | Confirmation prompts |
| `Sheet` | `@/components` | `ui/Sheet.tsx` | Slide-out panel |
| `Drawer` | `@/components` | `ui/Drawer.tsx` | Mobile drawer |
| `Popover` | `@/components` | `ui/Popover.tsx` | Floating popover |
| `Tooltip` | `@/components` | `ui/Tooltip.tsx` | Hover tooltip |
| `HoverCard` | `@/components` | `ui/HoverCard.tsx` | Card on hover |
| `DropdownMenu` | `@/components` | `ui/DropdownMenu.tsx` | Dropdown menu |
| `ContextMenu` | `@/components` | `ui/ContextMenu.tsx` | Right-click menu |
| `Command` | `@/components` | `ui/Command.tsx` | Command palette |

## Feedback & Status

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Alert` | `@/components` | `ui/Alert.tsx` | Alert messages |
| `Badge` | `@/components` | `ui/Badge.tsx` | Labels/status badges |
| `Progress` | `@/components` | `ui/Progress.tsx` | Progress bar |
| `Skeleton` | `@/components` | `ui/Skeleton.tsx` | Loading skeleton |
| `Toaster` | `@/components` | `ui/Toaster.tsx` | Toast container |
| `SonnerToaster, sonnerToast` | `@/components` | `ui/Sonner.tsx` | Sonner toast |

## Display

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `Avatar, AvatarImage, AvatarFallback` | `@/components` | `ui/Avatar.tsx` | User avatars |
| `Table, TableHeader, TableBody, TableRow, TableHead, TableCell` | `@/components` | `ui/Table.tsx` | Table components |
| `Carousel` | `@/components` | `ui/Carousel.tsx` | Image/content carousel |
| `Chart` | `@/components` | `ui/Chart.tsx` | Charts (Recharts) |

## State Components

| Component | Import | File | Description |
|-----------|--------|------|-------------|
| `LoadingState` | `@/components` | `ui/LoadingState.tsx` | Loading state display |
| `ErrorState` | `@/components` | `ui/ErrorState.tsx` | Error state display |
| `EmptyState` | `@/components` | `ui/EmptyState.tsx` | Empty state display |
| `SuccessState` | `@/components` | `ui/SuccessState.tsx` | Success state display |
