---
version: alpha
name: TrendBoda Dashboard
description: Operational dashboard for scanning Sources, Signals, and AI Cost data.
colors:
  canvas: "#F7F8F5"
  surface-1: "#FFFFFF"
  surface-2: "#F1F4EF"
  surface-3: "#E8EEE5"
  surface-4: "#DDE6DB"
  hairline: "#D9E0D6"
  hairline-strong: "#B9C6B4"
  ink: "#17201A"
  ink-muted: "#445147"
  ink-subtle: "#637067"
  ink-tertiary: "#8B968E"
  primary: "#23835B"
  primary-hover: "#1C6F4D"
  primary-active: "#155C40"
  primary-soft-light: "#E4F4EC"
  primary-soft-dark: "#183528"
  focus-ring: "#2EA66F"
  on-primary: "#FFFFFF"
  success: "#2F7D4F"
  warning: "#B7791F"
  danger: "#C2413D"
  info: "#3867D6"
  stale: "#667085"
  urgent: "#B42318"
  market-up: "#17803D"
  market-down: "#B42318"
  market-neutral: "#667085"
  chart-1: "#23835B"
  chart-2: "#3867D6"
  chart-3: "#B7791F"
  chart-4: "#637067"
  dark-canvas: "#0F1412"
  dark-surface-1: "#171D1A"
  dark-surface-2: "#1F2723"
  dark-surface-3: "#28312D"
  dark-surface-4: "#323D37"
  dark-hairline: "#303A35"
  dark-hairline-strong: "#4A574F"
  dark-ink: "#F1F4EF"
  dark-ink-muted: "#C7D0C5"
  dark-ink-subtle: "#9AA69D"
  dark-ink-tertiary: "#758078"
  dark-primary: "#2EA66F"
  dark-primary-hover: "#38B87C"
  dark-primary-active: "#259B63"
  dark-focus-ring: "#38B87C"
  dark-on-primary: "#FFFFFF"
  dark-success: "#3DA567"
  dark-warning: "#D49B2A"
  dark-danger: "#E05551"
  dark-info: "#5B8AF0"
  dark-stale: "#8895A4"
  dark-urgent: "#D94A42"
  dark-market-up: "#3DA567"
  dark-market-down: "#D94A42"
  dark-market-neutral: "#8895A4"
typography:
  display:
    fontFamily: Pretendard
    fontSize: 32px
    fontWeight: 700
    lineHeight: 1.15
  title-lg:
    fontFamily: Pretendard
    fontSize: 24px
    fontWeight: 700
    lineHeight: 1.25
  title:
    fontFamily: Pretendard
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.35
  body:
    fontFamily: Pretendard
    fontSize: 15px
    fontWeight: 400
    lineHeight: 1.55
  body-sm:
    fontFamily: Pretendard
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: Pretendard
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
    letterSpacing: 0.02em
  button:
    fontFamily: Pretendard
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0.01em
  metric:
    fontFamily: Pretendard
    fontSize: 28px
    fontWeight: 700
    lineHeight: 1.1
  mono:
    fontFamily: ui-monospace
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.45
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  xxl: 32px
  section: 40px
  page-x-desktop: 32px
  page-x-mobile: 16px
  row-y: 10px
  panel-padding: 16px
  panel-padding-lg: 24px
rounded:
  xs: 4px
  sm: 6px
  md: 8px
  lg: 10px
  xl: 12px
  pill: 9999px
  full: 9999px
components:
  button-primary:
    rounded: "{rounded.md}"
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  button-primary-active:
    backgroundColor: "{colors.primary-active}"
  button-secondary:
    rounded: "{rounded.md}"
    backgroundColor: "{colors.surface-1}"
    textColor: "{colors.ink}"
    borderColor: "{colors.hairline}"
  button-ghost:
    rounded: "{rounded.md}"
    textColor: "{colors.ink-muted}"
  button-ghost-hover:
    backgroundColor: "{colors.surface-2}"
  status-badge:
    rounded: "{rounded.pill}"
    typography: "{typography.caption}"
    padding: "{spacing.sm}"
  dashboard-panel:
    rounded: "{rounded.xl}"
    backgroundColor: "{colors.surface-1}"
    padding: "{spacing.panel-padding}"
  signal-row:
    rounded: "{rounded.lg}"
    backgroundColor: "{colors.surface-1}"
    height: 44px
  metric-card:
    rounded: "{rounded.xl}"
    backgroundColor: "{colors.surface-1}"
    typography: "{typography.metric}"
  text-input:
    rounded: "{rounded.md}"
    backgroundColor: "{colors.surface-1}"
    height: 44px
    padding: "{spacing.md}"
  table-row:
    height: 44px
  table-row-hover:
    backgroundColor: "{colors.surface-2}"
  top-nav:
    backgroundColor: "{colors.surface-1}"
    padding: "{spacing.page-x-desktop}"
  sidebar:
    backgroundColor: "{colors.surface-2}"
    padding: "{spacing.lg}"
  footer:
    backgroundColor: "{colors.canvas}"
    padding: "{spacing.xl}"
  progress-bar:
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.surface-3}"
  progress-indicator:
    rounded: "{rounded.pill}"
    backgroundColor: "{colors.primary}"
  summary-box:
    rounded: "{rounded.lg}"
    backgroundColor: "{colors.primary-soft-light}"
    padding: "{spacing.panel-padding-lg}"
  summary-box-dark:
    backgroundColor: "{colors.primary-soft-dark}"
  skeleton:
    rounded: "{rounded.md}"
    backgroundColor: "{colors.surface-2}"
---

# Design System: TrendBoda Dashboard

## Overview

TrendBoda is a light-first, dense operational dashboard for one Owner who scans Sources, Signals, Routine Briefings, Urgent Alerts, Watchlist context, Price Snapshots, and AI Cost Dashboard data. The interface should feel **precise, quiet, operational, readable, and developer-oriented**.

The strongest reference is Linear's precision: clean hierarchy, scarce accent color, compact controls, hairline borders, and surface-based depth. TrendBoda should not copy Linear's dark marketing canvas, lavender brand, hero-scale typography, or product-screenshot-led marketing rhythm. The dashboard is a working surface, not a landing page.

Light mode is the default identity. Dark mode is supported as a readable charcoal dashboard, not a near-black premium marketing theme. Both modes use the same surface ladder and component hierarchy.

## Colors

The palette is rooted in high-contrast neutrals with a single, evocative accent color used sparingly.

- **Canvas (#F7F8F5):** Cool Paper Canvas. Default page background. Soft enough for daily reading without feeling beige or editorial.
- **Surface-1 (#FFFFFF):** White Work Surface. Primary panels, cards, tables, and controls.
- **Surface-2 (#F1F4EF):** Pale Operational Surface. Hovered rows, secondary panels, and low-emphasis grouped areas.
- **Hairline (#D9E0D6):** Soft Gray-Green Hairline. Default borders and dividers.
- **Ink (#17201A):** Primary Ink. Headlines and primary body text.
- **Brand Primary (#23835B):** Developer Emerald. Primary actions, selected navigation, focused important links, and active tabs. Use sparingly.
- **Semantic Success (#2F7D4F):** Success Green. Used when source fetched, summary complete, budget healthy.
- **Semantic Urgent (#B42318):** Urgent Red. Exceptional Signal that should not wait for a Routine Briefing.
- **Data Visualization:** A set of precise, muted colors for AI cost charts and graphs.
  - **Chart 1 (#23835B):** Primary Emerald (Base metric)
  - **Chart 2 (#3867D6):** Info Blue (Secondary metric)
  - **Chart 3 (#B7791F):** Amber (Tertiary metric)
  - **Chart 4 (#637067):** Subtle Gray (Other/Remaining)

### Dark Mode (Charcoal Dashboard)

- **Readable Charcoal Canvas (#0F1412):** Default dark background. Reduces glare without becoming pure black.
- **Charcoal Work Surface (#171D1A):** Primary dark panels and cards.
- **Lifted Charcoal Surface (#1F2723):** Hovered rows and secondary panels.
- **Deep Charcoal Surface (#28312D):** Grouped controls and selected neutral surfaces.
- **Highest Charcoal Surface (#323D37):** Rare high-emphasis neutral backgrounds.
- **Dark Hairline (#303A35):** Default dark borders and dividers.
- **Strong Dark Hairline (#4A574F):** Strong dark separators and focus-adjacent borders.
- **Dark Primary Ink (#F1F4EF):** Headlines and primary body text in dark mode.
- **Dark Muted Ink (#C7D0C5):** Secondary body text and descriptions in dark mode.
- **Dark Subtle Ink (#9AA69D):** Metadata, timestamps, labels, and helper text.
- **Dark Tertiary Ink (#758078):** Disabled labels and low-priority hints.
- **Dark Developer Emerald (#2EA66F):** Lighter primary for actions, active tabs, and focus states. Maintains visual prominence against charcoal surfaces.
- **Dark Semantic Colors:** Success (#3DA567), Warning (#D49B2A), Danger (#E05551), Info (#5B8AF0), Stale (#8895A4), and Urgent (#D94A42) are lightened for readability on dark surfaces. Market movement colors follow the same adjustment.

## Typography

Use Pretendard as the single sans-serif voice for Korean and English dashboard text. Display and body typography should feel like one system. Use a monospace stack only for request IDs, model names, code-like tokens, cost tokens, timestamps where alignment matters, and compact technical metadata.

- **Display & Titles:** Set in Pretendard Semi-Bold and Bold for major dashboard section headings and panel headings.
- **Body:** Pretendard Regular at 15px (default) or 14px (dense rows) ensures contemporary professionalism and long-form readability.
- **Mono:** Monospace stack (13px) for technical tokens and metadata.

Do not use hero-scale headings, viewport-scaled type, or negative letter-spacing. The dashboard should prioritize scan speed and Korean readability over marketing drama.

## Layout

The layout follows a medium-high density structure: repeated rows are compact, while page-level layout keeps enough space to prevent visual noise.

- A strict 4px base spacing system is used.
- Page padding: 32px on desktop, 16px on mobile.
- Dashboard section gap: 24px to 40px depending on hierarchy.
- Panel padding: 16px by default, 20px for dense but important panels, 24px only for large summaries.
- List and table rows: 44px to 56px height. Touch targets are at least 40px (growing to 44px on mobile).
- The canvas should act as background structure, not decoration. Sections should be unframed layouts or dashboard panels.

## Elevation & Depth

Depth is achieved through **Tonal Layers** (a surface ladder) and **Hairline Borders**, not drop shadows.

- **Flat:** No shadow, no border. Page text, nav labels, simple metadata.
- **Level 1:** `surface-1` with 1px hairline border. Default panel, card, table wrapper.
- **Level 2:** `surface-2` with 1px hairline border. Hovered cards, selected neutral containers.
- **Level 3:** `surface-3` with stronger hairline border. Menus, dropdowns, focused grouped controls.
- **Overlay:** Soft shadow over overlay scrim. Dialogs and blocking inspection surfaces.

## Shapes

The shape language utilizes precise, restrained rounding.

- **xs (4px) & sm (6px):** Small badges, inline tags, and compact labels.
- **md (8px):** Buttons, inputs, selects, and compact controls. Subtly rounded corners.
- **lg (10px):** Repeated item cards and rows.
- **xl (12px):** Large dashboard panels and metric cards. Cards should not exceed 12px radius.
- **pill (9999px):** Status badges and segmented controls only.

## Components

- **Buttons**:
  - **Primary**: Developer Emerald background, white text, 8px corners. Used only for the main command in a region.
  - **Secondary**: Surface background, primary ink, hairline border.
  - **Ghost**: Transparent background, muted ink, subtle surface hover.
- **Cards and Panels**:
  - **Dashboard panel**: Surface-1 background, hairline border, 12px corners.
  - **Metric card**: Surface-1 background, hairline border, 12px corners, metric typography.
- **Inputs and Forms**:
  - Surface backgrounds, hairline borders, 8px corners, and 44px mobile touch targets. Focus uses the Focus Emerald ring.
- **Top Nav**:
  - Top navigation bar. Uses `surface-1` background with a bottom `hairline` border to separate it from the main content canvas. Maintains page-level horizontal padding.
- **Sidebar**:
  - Left-side vertical navigation. Uses `surface-2` background to create a subtle hierarchy difference from the main `surface-1` work area. Separated by a right `hairline` border.
- **Footer**:
  - Bottom area for supplementary information. Uses `canvas` background to recede visually and blend with the page edge. Text should be `ink-subtle`.
- **Status Badges**:
  - Compact and pill-shaped. Uses state colors only for state meaning (success, warning, error, stale, urgent).
- **Budget Progress**:
  - **Track (Background):** Surface-3, pill-shaped.
  - **Indicator:** Primary Emerald by default. Switches to Warning Amber near limits, and Danger Red when exceeded.
- **AI Summary Box**:
  - Distinctive panel for OpenRouter-generated summaries. Uses `primary-soft-light` background to subtly differentiate AI content from standard fetched data, with 10px corners and generous padding.
- **Skeleton Loader**:
  - Uses `surface-2` background with 8px corners. Muted and quiet, providing structure before data (like GeekNews items or Cost metrics) loads.

## Do's and Don'ts

- **Do** use light mode as the default dashboard identity.
- **Do** support readable charcoal dark mode with equivalent hierarchy.
- **Do** use Developer Emerald sparingly for action, focus, selected nav, and active tabs.
- **Do** separate operational state colors from market movement colors.
- **Don't** copy Linear's near-black marketing canvas or lavender brand.
- **Don't** create a landing-page hero for dashboard work.
- **Don't** use oversized display type, viewport-scaled font sizes, or negative letter-spacing.
- **Don't** use gradients, glow, blurred orbs, or decorative spotlights.
- **Don't** nest cards inside cards.
- **Don't** mix pill-shaped buttons with standard 8px buttons except for segmented controls or badges.
