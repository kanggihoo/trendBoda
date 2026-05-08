# Domain-backed HTTPS with Caddy

TrendBoda will use a purchased domain, Cloudflare-managed DNS, and Caddy on EC2 to expose the backend over HTTPS. We chose this because Vercel dashboard calls, Telegram webhook support, stable links, and future subdomain separation are simpler and more reliable with a real domain than with a raw EC2 public IP.

## Consequences

- The owner must pay the small annual domain cost.
- Caddy owns TLS certificate issuance and renewal through Let's Encrypt.
- Telegram polling can be used during early development, but production can move to webhook without changing the public API shape.
