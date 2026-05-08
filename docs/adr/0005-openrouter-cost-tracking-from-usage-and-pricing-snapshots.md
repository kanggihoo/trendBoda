# OpenRouter cost tracking from usage and pricing snapshots

TrendBoda will track OpenRouter usage by recording response token usage, model, feature, latency, status, and an estimated cost calculated from a local pricing table snapshot at request time. We chose this because model pricing can change over time, so historical dashboard numbers should remain stable even if future pricing data changes.

## Consequences

- Every AI request must write an AI usage record, including failed requests when possible.
- Cost values are estimates until reconciled with OpenRouter billing exports or APIs.
- Pricing metadata used for a request must be stored with that request, not only referenced globally.
