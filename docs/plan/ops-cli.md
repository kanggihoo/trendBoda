# Ops CLI

TrendBoda may include a Rust command-line tool for local and cloud operations after the first slice is working.

## Goal

Provide one terminal entry point for inspecting, diagnosing, deploying, and controlling TrendBoda operations without relying on cloud provider GUIs.

## MVP-Late Commands

- `trendboda doctor`: check API, DB, Telegram, OpenRouter, and provider connectivity
- `trendboda status`: show API, worker, bot, and scheduler status
- `trendboda costs`: show OpenRouter cost summary
- `trendboda logs`: show recent backend logs

## Cloud Commands

- `trendboda ssh`: connect to the EC2 host
- `trendboda deploy`: deploy backend services
- `trendboda restart api`: restart the API process
- `trendboda restart worker`: restart worker processes
- `trendboda migrate`: run dbmate migrations

## Rules

- Prefer API calls for read-only inspection.
- Use SSH only for cloud operations that cannot be handled through the API.
- Require confirmation for destructive or disruptive actions.
- Keep secrets in environment variables, local config, or a secure secret store, not command arguments.
