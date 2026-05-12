Status: ready-for-agent

# Add Price Snapshot Cache And Stale Fallback

## Parent

.scratch/us-price-snapshot-dashboard/PRD.md

## What to build

Add a small Price Snapshot cache interface and an application-scoped in-process TTL implementation. The Price Snapshot service should decide per dashboard request and per symbol whether to return fresh cached data, call Finnhub for missing or expired data, or return stale cached quote data when Finnhub is temporarily unavailable or rate-limited.

## Acceptance criteria

- [ ] Price Snapshot caching is accessed through a narrow cache interface rather than direct service-owned dictionaries.
- [ ] The MVP cache implementation is in-process and application-scoped.
- [ ] Quote data is fresh for 60 seconds.
- [ ] Quote data remains eligible for stale fallback for up to five minutes.
- [ ] Profile data is cached for 24 hours.
- [ ] US market holiday data is cached for 24 hours or until the next local market-calendar refresh boundary.
- [ ] Repeated dashboard requests within the quote TTL use cached quote data instead of calling Finnhub again.
- [ ] Expired quote data triggers a Finnhub refresh when provider rate limits and failures are not present.
- [ ] Finnhub temporary failures or rate limits return stale quote data when a valid stale entry exists.
- [ ] Expired stale quote data is not returned as a successful Price Snapshot.
- [ ] The cache design can later be replaced by Redis without changing provider, service, API, or dashboard contracts.
- [ ] Service and cache tests use a controlled clock and cover fresh cache, expired cache, stale fallback, missing cache, and provider failure behavior.

## Blocked by

- .scratch/us-price-snapshot-dashboard/issues/02-add-fixed-watchlist-price-snapshot-api.md
