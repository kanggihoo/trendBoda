---
name: TrendBoda Dashboard
version: 0.1.0
status: draft
project:
  product: TrendBoda
  surface: web dashboard
  audience: Owner
  purpose: Scan Sources, Signals, Routine Briefings, Urgent Alerts, Watchlist context, Price Snapshots, and AI Cost Dashboard data.
principles:
  default_mode: light
  supported_modes:
    - light
    - dark
  density: medium-high
  aesthetic:
    - precise
    - quiet
    - operational
    - readable
    - developer-oriented
  references:
    primary: Linear precision and surface hierarchy
    structural: IBM Carbon dashboard clarity
    reading: Mintlify readable panels
    state: Sentry monitoring status clarity
  avoid:
    - marketing hero layouts
    - decorative gradients
    - nested cards
    - broad brand imitation
    - oversized display typography
tokens:
  colors:
    light:
      canvas: "#f7f8f5"
      surface-1: "#ffffff"
      surface-2: "#f1f4ef"
      surface-3: "#e8eee5"
      surface-4: "#dde6db"
      hairline: "#d9e0d6"
      hairline-strong: "#b9c6b4"
      ink: "#17201a"
      ink-muted: "#445147"
      ink-subtle: "#637067"
      ink-tertiary: "#8b968e"
      overlay: "rgba(15, 20, 18, 0.56)"
    dark:
      canvas: "#0f1412"
      surface-1: "#171d1a"
      surface-2: "#1f2723"
      surface-3: "#28312d"
      surface-4: "#323d37"
      hairline: "#303a35"
      hairline-strong: "#4a574f"
      ink: "#f1f4ef"
      ink-muted: "#c7d0c5"
      ink-subtle: "#9aa69d"
      ink-tertiary: "#758078"
      overlay: "rgba(0, 0, 0, 0.64)"
    brand:
      primary: "#23835b"
      primary-hover: "#1c6f4d"
      primary-active: "#155c40"
      primary-soft-light: "#e4f4ec"
      primary-soft-dark: "#183528"
      focus-ring: "#2ea66f"
      on-primary: "#ffffff"
    semantic:
      success: "#2f7d4f"
      warning: "#b7791f"
      danger: "#c2413d"
      info: "#3867d6"
      stale: "#667085"
      urgent: "#b42318"
    market:
      up: "#17803d"
      down: "#b42318"
      neutral: "#667085"
  typography:
    family:
      sans: "Pretendard, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
      mono: "ui-monospace, SFMono-Regular, SF Mono, Menlo, Monaco, Consolas, monospace"
    scale:
      display:
        size: "32px"
        line_height: "1.15"
        weight: 700
        letter_spacing: "0"
      title-lg:
        size: "24px"
        line_height: "1.25"
        weight: 700
        letter_spacing: "0"
      title:
        size: "18px"
        line_height: "1.35"
        weight: 600
        letter_spacing: "0"
      body:
        size: "15px"
        line_height: "1.55"
        weight: 400
        letter_spacing: "0"
      body-sm:
        size: "14px"
        line_height: "1.5"
        weight: 400
        letter_spacing: "0"
      caption:
        size: "12px"
        line_height: "1.4"
        weight: 500
        letter_spacing: "0"
      button:
        size: "14px"
        line_height: "1.2"
        weight: 600
        letter_spacing: "0"
      metric:
        size: "28px"
        line_height: "1.1"
        weight: 700
        letter_spacing: "0"
      mono:
        size: "13px"
        line_height: "1.45"
        weight: 400
        letter_spacing: "0"
  spacing:
    base: "4px"
    xs: "4px"
    sm: "8px"
    md: "12px"
    lg: "16px"
    xl: "24px"
    xxl: "32px"
    section: "40px"
    page-x-desktop: "32px"
    page-x-mobile: "16px"
    row-y: "10px"
    panel-padding: "16px"
  radius:
    xs: "4px"
    sm: "6px"
    md: "8px"
    lg: "10px"
    xl: "12px"
    pill: "9999px"
    full: "9999px"
  elevation:
    flat:
      shadow: "none"
      border: "none"
    level-1:
      background: "surface-1"
      border: "1px solid hairline"
      shadow: "none"
    level-2:
      background: "surface-2"
      border: "1px solid hairline"
      shadow: "none"
    level-3:
      background: "surface-3"
      border: "1px solid hairline-strong"
      shadow: "none"
    overlay:
      shadow: "0 16px 40px rgba(15, 20, 18, 0.14)"
components:
  button-primary:
    radius: md
    background: primary
    text: on-primary
    hover: primary-hover
    active: primary-active
    focus: focus-ring
  button-secondary:
    radius: md
    background: surface-1
    text: ink
    border: hairline
  button-ghost:
    radius: md
    background: transparent
    text: ink-muted
    hover_background: surface-2
  status-badge:
    radius: pill
    typography: caption
    padding: "2px 8px"
  dashboard-panel:
    radius: xl
    background: surface-1
    border: hairline
    padding: panel-padding
  signal-row:
    radius: lg
    min_height: "44px"
    background: transparent
    border: "bottom hairline"
  metric-card:
    radius: xl
    background: surface-1
    border: hairline
    typography: metric
  text-input:
    radius: md
    background: surface-1
    border: hairline
    focus: focus-ring
  table:
    row_height: "44px"
    border: hairline
    header_typography: caption
states:
  loading:
    treatment: skeleton first, muted text fallback
  empty:
    treatment: muted panel with one clear next action
  ready:
    treatment: default content without required badge
  success:
    token: success
    meaning: source fetched, summary complete, budget healthy
  warning:
    token: warning
    meaning: budget nearing limit, source delayed, review useful
  error:
    token: danger
    meaning: fetch failed, API unavailable, action failed
  disabled:
    token: ink-tertiary
    meaning: unavailable or inactive action
  stale:
    token: stale
    meaning: data is old but not failed
  urgent:
    token: urgent
    meaning: exceptional Signal that should not wait for Routine Briefing
  market-up:
    token: market.up
    meaning: price movement only
  market-down:
    token: market.down
    meaning: price movement only
  market-neutral:
    token: market.neutral
    meaning: price movement only
implementation:
  framework: Next.js
  styling: Tailwind CSS
  primitives: shadcn/ui
  icons: lucide-react
  first_allowed_shadcn:
    - Button
    - Card
    - Badge
    - Tabs
    - Table
    - Input
    - Select
    - DropdownMenu
    - Dialog
    - Tooltip
    - Skeleton
    - Alert
---

# Design System: TrendBoda Dashboard

## 1. Visual Theme & Atmosphere

TrendBoda is a light-first, dense operational dashboard for one Owner who scans Sources, Signals, Routine Briefings, Urgent Alerts, Watchlist context, Price Snapshots, and AI Cost Dashboard data. The interface should feel precise, quiet, readable, and developer-oriented.

The strongest reference is Linear's precision: clean hierarchy, scarce accent color, compact controls, hairline borders, and surface-based depth. TrendBoda should not copy Linear's dark marketing canvas, lavender brand, hero-scale typography, or product-screenshot-led marketing rhythm. The dashboard is a working surface, not a landing page.

Light mode is the default identity. Dark mode is supported as a readable charcoal dashboard, not a near-black premium marketing theme. Both modes use the same surface ladder and component hierarchy.

## 2. Color Palette & Roles

### Light Mode

- **Cool Paper Canvas** (`#f7f8f5`): Default page background. Soft enough for daily reading without feeling beige or editorial.
- **White Work Surface** (`#ffffff`): Primary panels, cards, tables, and controls.
- **Pale Operational Surface** (`#f1f4ef`): Hovered rows, secondary panels, and low-emphasis grouped areas.
- **Muted Lift Surface** (`#e8eee5`): Deeper grouped controls, selected neutral surfaces, and subtle nested structure.
- **Deep Lift Surface** (`#dde6db`): Rare high-emphasis neutral backgrounds.
- **Soft Gray-Green Hairline** (`#d9e0d6`): Default borders and dividers.
- **Strong Gray-Green Hairline** (`#b9c6b4`): Focus-adjacent borders, table header separators, and stronger panel edges.
- **Primary Ink** (`#17201a`): Headlines and primary body text.
- **Muted Ink** (`#445147`): Secondary body text and descriptions.
- **Subtle Ink** (`#637067`): Metadata, timestamps, labels, and helper text.
- **Tertiary Ink** (`#8b968e`): Disabled labels and low-priority hints.

### Dark Mode

- **Readable Charcoal Canvas** (`#0f1412`): Default dark background. It should reduce glare without becoming pure black.
- **Charcoal Work Surface** (`#171d1a`): Primary dark panels and cards.
- **Lifted Charcoal Surface** (`#1f2723`): Hovered rows and secondary panels.
- **Deep Charcoal Surface** (`#28312d`): Grouped controls and selected neutral surfaces.
- **Highest Charcoal Surface** (`#323d37`): Rare high-emphasis neutral backgrounds.
- **Dark Hairline** (`#303a35`): Default dark borders and dividers.
- **Strong Dark Hairline** (`#4a574f`): Strong dark separators and focus-adjacent borders.
- **Dark Primary Ink** (`#f1f4ef`): Headlines and primary body text.
- **Dark Muted Ink** (`#c7d0c5`): Secondary body text and descriptions.
- **Dark Subtle Ink** (`#9aa69d`): Metadata, timestamps, labels, and helper text.
- **Dark Tertiary Ink** (`#758078`): Disabled labels and low-priority hints.

### Brand, Semantic, and Market Colors

- **Developer Emerald** (`#23835b`): Primary actions, selected navigation, focused important links, and active tabs. Use sparingly.
- **Developer Emerald Hover** (`#1c6f4d`): Hovered primary action.
- **Developer Emerald Active** (`#155c40`): Pressed primary action.
- **Soft Emerald Light** (`#e4f4ec`): Light-mode selected background or subtle primary tint.
- **Soft Emerald Dark** (`#183528`): Dark-mode selected background or subtle primary tint.
- **Focus Emerald** (`#2ea66f`): Focus ring and keyboard-visible focus state.
- **Success Green** (`#2f7d4f`): Source fetched, summary complete, budget healthy.
- **Warning Amber** (`#b7791f`): Budget nearing limit, Source delayed, review recommended.
- **Danger Red** (`#c2413d`): Fetch failed, API unavailable, destructive action, or failed operation.
- **Info Blue** (`#3867d6`): Neutral informational notices.
- **Stale Gray** (`#667085`): Old data that is not failed.
- **Urgent Red** (`#b42318`): Exceptional Signal that should not wait for a Routine Briefing.
- **Market Up Green** (`#17803d`), **Market Down Red** (`#b42318`), **Market Neutral Gray** (`#667085`): Price movement only. Do not reuse these for generic success or failure.

## 3. Typography Rules

Use Pretendard as the single sans-serif voice for Korean and English dashboard text. Display and body typography should feel like one system. Use a monospace stack only for request IDs, model names, code-like tokens, cost tokens, timestamps where alignment matters, and compact technical metadata.

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---:|---:|---:|---:|---|
| `display` | 32px | 700 | 1.15 | 0 | Page title only |
| `title-lg` | 24px | 700 | 1.25 | 0 | Major dashboard section headings |
| `title` | 18px | 600 | 1.35 | 0 | Panel headings and card titles |
| `body` | 15px | 400 | 1.55 | 0 | Default text |
| `body-sm` | 14px | 400 | 1.5 | 0 | Dense rows, secondary text |
| `caption` | 12px | 500 | 1.4 | 0 | Labels, timestamps, badges, metadata |
| `button` | 14px | 600 | 1.2 | 0 | Button labels and compact commands |
| `metric` | 28px | 700 | 1.1 | 0 | Cost, count, and status metrics |
| `mono` | 13px | 400 | 1.45 | 0 | Technical tokens |

Do not use hero-scale headings, viewport-scaled type, or negative letter-spacing. The dashboard should prioritize scan speed and Korean readability over marketing drama.

## 4. Layout Principles

Use a 4px base spacing system. TrendBoda should feel medium-high density: repeated rows are compact, while page-level layout keeps enough space to prevent visual noise.

- Page padding: 32px on desktop, 16px on mobile.
- Dashboard section gap: 24px to 40px depending on hierarchy.
- Panel padding: 16px by default, 20px for dense but important panels, 24px only for large summaries.
- List and table rows: 44px to 56px height.
- Row vertical padding: 10px to 12px.
- Touch targets: at least 40px, growing to 44px on mobile.
- Use grid and table layouts for comparison, not decorative card clusters.
- Avoid large empty hero areas. The first viewport should show useful dashboard content.

The canvas should act as background structure, not decoration. Sections should be unframed layouts or dashboard panels, not floating marketing bands.

## 5. Elevation & Depth

Depth comes from a surface ladder and hairline borders, not drop shadows.

| Level | Treatment | Use |
|---|---|---|
| Flat | No shadow, no border | Page text, nav labels, simple metadata |
| Level 1 | `surface-1` with 1px hairline | Default panel, card, table wrapper |
| Level 2 | `surface-2` with 1px hairline | Hovered cards, selected neutral containers |
| Level 3 | `surface-3` with stronger hairline | Menus, dropdowns, focused grouped controls |
| Overlay | Soft shadow over overlay scrim | Dialogs and blocking inspection surfaces |

Avoid decorative glow, spotlight cards, glassmorphism, blurred orbs, and atmospheric gradients. Dark mode should use the same ladder with readable charcoal values.

## 6. Shapes

TrendBoda uses precise, restrained rounding.

| Token | Value | Use |
|---|---:|---|
| `xs` | 4px | Small badges and tiny chips |
| `sm` | 6px | Inline tags and compact labels |
| `md` | 8px | Buttons, inputs, selects, compact controls |
| `lg` | 10px | Repeated item cards and rows |
| `xl` | 12px | Large dashboard panels and metric cards |
| `pill` | 9999px | Status badges and segmented controls only |
| `full` | 9999px | Avatars, dots, and circular indicators |

Cards should not exceed 12px radius. Buttons should normally use 8px corners, not pill shapes. Status badges may be pill-shaped because their role is compact state recognition.

## 7. Component Styling

### Buttons

- **Primary button**: Developer Emerald background, white text, 8px corners, compact 14px label. Use only for the main command in a region.
- **Secondary button**: Surface background, primary ink, 1px hairline border. Use for supporting actions.
- **Ghost button**: Transparent background, muted ink, subtle surface hover. Use for toolbar and row actions.
- **Icon button**: Use lucide-react icons. Add accessible labels and tooltips when icon meaning is not obvious.

### Cards and Panels

- **Dashboard panel**: Surface-1 background, 1px hairline, 12px corners, 16px padding.
- **Metric card**: Surface-1 background, 1px hairline, 12px corners, metric typography. Use for cost, count, latency, error, and budget summaries.
- **Signal row**: Compact row with bottom hairline or subtle hover surface. Prefer list rhythm over isolated cards for repeated Signals.
- **Nested cards**: Avoid. If hierarchy is needed inside a panel, use table rows, dividers, inset groups, or typographic hierarchy.

### Inputs and Forms

Inputs use surface backgrounds, hairline borders, 8px corners, and 44px mobile touch targets. Focus uses the Focus Emerald ring. Error text uses Danger Red, but only after the field or action has failed validation.

### Status Badges

Badges are compact and pill-shaped. Use state colors only for state meaning:

- `success`: completed Source check, summary complete, budget healthy.
- `warning`: delayed Source, nearing budget limit, review recommended.
- `error`: failed fetch, unavailable API, failed action.
- `stale`: old data that may still be usable.
- `urgent`: exceptional Signal requiring immediate attention.

Do not use `success` for market price increase. Use `market-up` and `market-down` only for price movement.

### Tables and Lists

Tables and lists are first-class dashboard surfaces. Headers use caption typography and subtle ink. Rows should support hover, selected, stale, warning, and error states without changing row height. Numeric columns should align for comparison.

### Dialogs and Overlays

Dialogs are for destructive confirmation, detail inspection, or focused settings. Use overlay scrim plus soft shadow. Keep dialog content utilitarian and avoid marketing-style cards inside dialogs.

## 8. State Model

Every data surface should have explicit states:

- **Loading**: Skeleton first, muted text fallback when skeleton is not useful.
- **Empty**: Muted panel with one clear next action or explanation.
- **Ready**: Default content, no badge required.
- **Success**: Completed operational event.
- **Warning**: Needs attention but not failed.
- **Error**: Failed operation or unavailable dependency.
- **Disabled**: Action exists but cannot be used now.
- **Stale**: Data is old but not failed.
- **Urgent**: Exceptional Signal that should not wait for the next Routine Briefing.

Urgent is not the same as error. Stale is not the same as warning. Success is not the same as market-up.

## 9. Implementation Guidance

Use Tailwind CSS for application styling and shadcn/ui for shared primitives. This file is the design contract; it does not require Tailwind config generation in this first draft.

Allowed first shadcn/ui primitives:

- Button
- Card
- Badge
- Tabs
- Table
- Input
- Select
- DropdownMenu
- Dialog
- Tooltip
- Skeleton
- Alert

Use lucide-react for icons. Prefer icons for compact controls when a standard symbol exists. Add tooltip and accessible label for icon-only actions.

Keep `web/app/globals.css` minimal. Prefer Tailwind utility composition and shadcn/ui theming over broad custom CSS. Do not introduce broad component abstractions before patterns repeat.

## 10. Do's and Don'ts

### Do

- Use light mode as the default dashboard identity.
- Support readable charcoal dark mode with equivalent hierarchy.
- Use Developer Emerald sparingly for action, focus, selected nav, and active tabs.
- Use surface ladder plus hairline borders for hierarchy.
- Keep rows, tables, and panels dense enough for repeated daily scanning.
- Keep Pretendard as the dashboard typeface.
- Separate operational state colors from market movement colors.
- Prefer quiet, scannable UI over expressive decoration.

### Don't

- Do not copy Linear's near-black marketing canvas or lavender brand.
- Do not create a landing-page hero for dashboard work.
- Do not use oversized display type, viewport-scaled font sizes, or negative letter-spacing.
- Do not use gradients, glow, blurred orbs, or decorative spotlights.
- Do not nest cards inside cards.
- Do not use pill-shaped buttons except segmented controls or status badges.
- Do not use green success styling for market price movement.
- Do not create broad component abstractions before the dashboard has repeated patterns.

## 11. Responsive Behavior

- Desktop: 32px page padding, dense multi-column dashboard grids where useful.
- Tablet: Reduce grids predictably; keep panels readable and avoid cramped side-by-side tables.
- Mobile: 16px page padding, single-column panels, 44px touch targets, no horizontal overflow.
- Tables with many columns should become horizontally scrollable or switch to stacked rows only when comparison is not the main task.
- Text must never overlap controls or truncate critical Signal titles unless an explicit expanded view exists.

## 12. Iteration Guide

1. Start from mode, surface level, and density before styling a component.
2. Choose the component's state model before choosing color.
3. Use primary color only when the Owner can act or identify the active view.
4. Use semantic colors only when state meaning is present.
5. Use market tokens only for Price Snapshot and market movement.
6. Add new component variants to this file before repeating them across screens.
7. Run `npx @google/design.md lint DESIGN.md` when the project starts relying on export or lint tooling.

## Known Gaps

- Tailwind theme export is intentionally deferred.
- Current web CSS may not yet match these tokens.
- Dark mode support is documented here but not necessarily implemented.
- Final dashboard navigation and AI Cost Dashboard layouts may add component variants later.
