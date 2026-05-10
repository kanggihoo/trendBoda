# OpenRouter cost tracking from usage and pricing snapshots

TrendBoda will track OpenRouter usage by recording response token usage, model, feature, latency, status, and an estimated cost calculated from a pricing snapshot at request time. Pricing should come from OpenRouter's `/api/v1/models` metadata cached for roughly one day, with local fallback pricing only when the metadata endpoint is unavailable. We chose this because model pricing can change over time, so historical dashboard numbers should remain stable even if future pricing data changes.

## Consequences

- Every AI request must write an AI usage record, including failed requests when possible.
- Cost values are estimates until reconciled with OpenRouter billing exports or APIs.
- Pricing metadata used for a request must be stored with that request, not only referenced globally.
- OpenRouter pricing metadata lookup failure must not block summarization; the request can proceed with fallback pricing or unavailable estimated cost.
- OpenRouter management endpoints such as `/api/v1/credits` and `/api/v1/activity` may be used for audit/reconciliation with a separate management key, not the normal inference key.
