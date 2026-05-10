# AI model routing through feature config

TrendBoda will route AI requests through explicit `AIModel` and `AIFeature` enums with feature-level primary and fallback model configuration. We chose this so model changes are intentional, dashboard grouping stays stable, and OpenRouter model strings can still be overridden by environment configuration without scattering vendor model names through application code.

## Consequences

- AI features must declare which route they use instead of calling arbitrary models directly.
- Each AI usage record stores the actual OpenRouter model string used for the request.
- Fallback behavior is configured per feature and sent to OpenRouter as an ordered `models` list when the provider supports managed fallback.
- A managed fallback request is recorded as one AI usage record; the successful response model or final error represents the request outcome.
