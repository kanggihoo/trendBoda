Status: ready-for-agent

# Render Dashboard Price Snapshot Table

## Parent

.scratch/us-price-snapshot-dashboard/PRD.md

## What to build

Add a Next.js dashboard view for the fixed Watchlist Price Snapshots. The view should use the backend Watchlist Price Snapshot endpoint, render dense table-like rows on desktop, render compact stacked rows on mobile, show market movement states, and let the Owner manually refresh without adding auto-refresh behavior.

## Acceptance criteria

- [ ] The dashboard fetches Price Snapshots from the backend Watchlist endpoint.
- [ ] Desktop layout uses compact table-like rows for Watchlist comparison.
- [ ] Mobile layout uses compact stacked rows while preserving the same scan order.
- [ ] Rows display symbol, name, exchange, currency, current price, previous close, change, change percent, day open, day high, day low, freshness, and last updated time where available.
- [ ] Market movement uses existing market-up, market-down, and market-neutral design tokens.
- [ ] Stale fallback data is visibly marked as stale.
- [ ] The dashboard includes a manual refresh control.
- [ ] The dashboard does not auto-refresh in the MVP.
- [ ] Loading, unavailable, empty, ready, and stale states are handled without layout jumps or overlapping text.
- [ ] The implementation follows the existing dashboard design contract and does not introduce a broad generic DataTable abstraction unless repeated table behavior already exists.
- [ ] Web tests or existing supported checks cover ready rows, stale freshness display, market movement styling, and manual refresh behavior where practical.

## Blocked by

- .scratch/us-price-snapshot-dashboard/issues/02-add-fixed-watchlist-price-snapshot-api.md
