# OpenTofu for infrastructure code

TrendBoda will manage AWS and Cloudflare infrastructure with OpenTofu using HCL `.tf` files. We chose OpenTofu because it preserves the Terraform-style workflow and ecosystem familiarity while keeping the infrastructure engine open source and suitable for code review with AI.

## Consequences

- Terraform learning material remains useful, but local commands use `tofu`.
- Initial infrastructure code will cover AWS EC2, security groups, IAM, and Cloudflare DNS.
- Vercel, Neon, Grafana, OpenRouter, and Telegram setup can remain manual at first and be added to infrastructure code later if useful.
