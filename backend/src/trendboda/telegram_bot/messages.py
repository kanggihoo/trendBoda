from collections.abc import Mapping
from typing import cast

from trendboda.telegram_bot.types import GeekNewsTelegramItem


def format_geeknews_message(items: list[GeekNewsTelegramItem]) -> str:
    if not items:
        return "No recent Developer Trend Source signals."

    lines = ["Recent Developer Trend Source signals"]
    for index, item in enumerate(items, start=1):
        lines.append(f"{index}. {item.title}")
        if item.summary is not None:
            lines.append(item.summary)
        lines.append(item.source_url)
    return "\n".join(lines)


def format_cost_message(summary: Mapping[str, object], *, monthly_budget_usd: str) -> str:
    totals = dict_or_none(summary.get("totals")) or {}
    budget = dict_or_none(summary.get("budget")) or {}
    return "\n".join(
        [
            "OpenRouter cost",
            (
                f"Total: ${totals.get('estimated_cost_usd', '0')} across "
                f"{totals.get('request_count', 0)} requests"
            ),
            (
                f"Month: ${budget.get('estimated_monthly_cost_usd', '0')} / "
                f"${budget.get('monthly_budget_usd', monthly_budget_usd)} "
                f"({budget.get('percent_used', '0')}%)"
            ),
            f"Failures: {totals.get('failure_count', 0)}",
        ]
    )


def dict_or_none(value: object) -> dict[str, object] | None:
    if not isinstance(value, dict):
        return None
    return cast(dict[str, object], value)
