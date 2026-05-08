# AI only for interpretation and summarization

TrendBoda will use AI only when it needs interpretation, summarization, or cross-source reasoning, not for deterministic data display such as current prices, status checks, or raw source listings. This keeps OpenRouter cost predictable and avoids low-confidence explanations when the system lacks supporting news, disclosure, or market context.

## Consequences

- Price snapshots and status views must be generated without AI.
- AI answers must be grounded in fetched source data and include links where available.
- Model routing should prefer cheaper models for routine summaries and stronger models for market questions or investment analysis.
