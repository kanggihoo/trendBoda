"use client";

import type { CostGroup, CostSummary, UsageRequest } from "./lib/contracts";
import { clampPercent, formatDate, formatLatency, formatUsd } from "./lib/dashboard-format";
import { type AiCostTelemetry, fetchAiCostTelemetry } from "./lib/trendboda-api";
import { useRemoteResource } from "./lib/use-remote-resource";

function hasNoAiCostRequests(telemetry: AiCostTelemetry) {
  return telemetry.summary.totals.request_count === 0;
}

export function AiCostDashboard() {
  const telemetry = useRemoteResource(fetchAiCostTelemetry, hasNoAiCostRequests);

  if (telemetry.status === "loading") {
    return <p className="text-body-sm text-ink-subtle">Loading OpenRouter cost telemetry.</p>;
  }

  if (telemetry.status === "error") {
    return <p className="text-body-sm text-ink-subtle">AI cost data is unavailable.</p>;
  }

  if (telemetry.status === "empty") {
    return <p className="text-body-sm text-ink-subtle">No OpenRouter requests recorded yet.</p>;
  }

  return (
    <AiCostDashboardView
      requests={telemetry.data.requests}
      summary={telemetry.data.summary}
    />
  );
}

function AiCostDashboardView({
  requests,
  summary,
}: {
  requests: UsageRequest[];
  summary: CostSummary;
}) {
  const budgetPercent = clampPercent(summary.budget.percent_used);

  return (
    <div className="grid gap-lg">
      <div className="grid grid-cols-[repeat(auto-fit,minmax(180px,1fr))] gap-md">
        <MetricCard label="Estimated cost" value={formatUsd(summary.totals.estimated_cost_usd)} />
        <MetricCard label="Requests" value={String(summary.totals.request_count)} />
        <MetricCard label="Latency" value={formatLatency(summary.totals.average_latency_ms)} />
        <MetricCard label="Error status" value={`${summary.totals.failure_count} failed`} />
      </div>

      <section className="rounded-xl border border-hairline bg-surface-1 p-lg">
        <div className="mb-md flex items-center justify-between gap-md">
          <div>
            <h3 className="text-title">Monthly budget</h3>
            <p className="text-body-sm text-ink-muted">
              {formatUsd(summary.budget.estimated_monthly_cost_usd)} of{" "}
              {formatUsd(summary.budget.monthly_budget_usd)} used
            </p>
          </div>
          <span className="font-mono text-[13px] text-ink-muted">
            {summary.budget.percent_used}%
          </span>
        </div>
        <div className="h-[10px] overflow-hidden rounded-pill bg-surface-3">
          <div
            className="h-full rounded-pill bg-primary transition-[width]"
            style={{ width: `${budgetPercent}%` }}
          />
        </div>
      </section>

      <div className="grid gap-md xl:grid-cols-3">
        <GroupingPanel groups={summary.by_date} title="By date" valueKey="date" />
        <GroupingPanel groups={summary.by_model} title="By model" valueKey="model" />
        <GroupingPanel groups={summary.by_feature} title="By feature" valueKey="feature" />
      </div>

      <RecentRequestsPanel requests={requests} />
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <section className="rounded-xl border border-hairline bg-surface-1 p-lg">
      <p className="mb-sm text-caption uppercase text-ink-subtle">{label}</p>
      <p className="font-mono text-[24px] font-semibold leading-none text-ink">{value}</p>
    </section>
  );
}

function GroupingPanel({
  groups,
  title,
  valueKey,
}: {
  groups: CostGroup[];
  title: string;
  valueKey: "date" | "model" | "feature";
}) {
  return (
    <section className="rounded-xl border border-hairline bg-surface-1 p-lg">
      <h3 className="mb-md text-title">{title}</h3>
      <div className="grid gap-sm">
        {groups.map((group) => (
          <div className="grid gap-xs border-t border-hairline py-sm first:border-t-0" key={group[valueKey]}>
            <div className="flex items-center justify-between gap-md">
              <span className="truncate font-mono text-[13px] text-ink">{group[valueKey]}</span>
              <span className="font-mono text-[13px] text-ink">{formatUsd(group.estimated_cost_usd)}</span>
            </div>
            <p className="text-caption text-ink-subtle">
              {group.request_count} requests · {formatLatency(group.average_latency_ms)} ·{" "}
              {group.failure_count} failures
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}

function RecentRequestsPanel({ requests }: { requests: UsageRequest[] }) {
  return (
    <section className="rounded-xl border border-hairline bg-surface-1 p-lg">
      <div className="mb-md flex items-center justify-between gap-md">
        <h3 className="text-title">Recent requests</h3>
        <span className="text-caption uppercase text-ink-subtle">OpenRouter local records</span>
      </div>
      <div className="grid gap-xs">
        {requests.map((request) => (
          <article
            className="grid gap-sm border-t border-hairline py-md first:border-t-0 md:grid-cols-[minmax(0,1fr)_auto]"
            key={request.id}
          >
            <div className="min-w-0">
              <p className="truncate font-mono text-[13px] text-ink">
                #{request.id} {request.feature} · {request.actual_model ?? "unknown model"}
              </p>
              <p className="text-body-sm text-ink-muted">
                {formatUsd(request.estimated_cost_usd)} · {request.latency_ms}ms ·{" "}
                {request.total_tokens ?? 0} tokens
              </p>
              {request.error_message ? (
                <p className="text-body-sm text-danger">{request.error_message}</p>
              ) : null}
            </div>
            <div className="grid gap-xs text-left md:justify-items-end md:text-right">
              <StatusBadge status={request.status} />
              <time className="text-caption text-ink-subtle">{formatDate(request.created_at)}</time>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function StatusBadge({ status }: { status: UsageRequest["status"] }) {
  const className =
    status === "success"
      ? "border-success/30 bg-primary-soft-light text-success"
      : "border-danger/30 bg-surface-2 text-danger";
  return (
    <span className={`rounded-pill border px-sm py-xs text-caption uppercase ${className}`}>
      {status}
    </span>
  );
}
