# Domain Docs

How engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This is a single-context repo.

- `CONTEXT.md`: project domain language and resolved terminology
- `docs/adr/`: architecture decision records
- `docs/plan/`: implementation plans and sequencing notes

## Before Exploring, Read These

- Read `CONTEXT.md` before naming domain concepts or proposing behavior.
- Read relevant ADRs in `docs/adr/` before changing architecture, integration patterns, deployment, data access, AI usage, or provider strategy.
- Read relevant plans in `docs/plan/` before turning planned work into issues or implementation tasks.

If any of these files do not exist, proceed silently. The producer skill creates them lazily when terms or decisions get resolved.

## Use the Glossary's Vocabulary

When output names a domain concept in an issue title, refactor proposal, hypothesis, test name, or implementation plan, use the term as defined in `CONTEXT.md`. Do not drift to synonyms the glossary explicitly avoids.

If the concept needed is not in the glossary yet, either the work is using language outside the project domain or the glossary has a real gap. Note the gap for `grill-with-docs`.

## Flag ADR Conflicts

If output contradicts an existing ADR, surface it explicitly rather than silently overriding it.
