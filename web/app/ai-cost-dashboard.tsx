"use client";

import { useEffect, useState } from "react";

type CostGroup = {
  date?: string;
  model?: string;
  feature?: string;
  estimated_cost_usd: string;
  request_count: number;
  average_latency_ms: number | null;
  failure_count: number;
};

type CostSummary = {
  totals: {
    estimated_cost_usd: string;
    request_count: number;
    success_count: number;
    failure_count: number;
    average_latency_ms: number | null;
  };
  by_date: CostGroup[];
  by_model: CostGroup[];
  by_feature: CostGroup[];
  budget: {
    monthly_budget_usd: string;
    estimated_monthly_cost_usd: string;
    percent_used: string;
  };
};

type UsageRequest = {
  id: number;
  feature: string;
  status: "success" | "failure";
  requested_models: string[];
  actual_model: string | null;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  estimated_cost_usd: string;
  latency_ms: number;
  pricing_source: string | null;
  error_message: string | null;
  created_at: string;
};

type UsageRequestsResponse = {
  requests: UsageRequest[];
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export function AiCostDashboard() {
  const [summary, setSummary] = useState<CostSummary | null>(null);
  const [requests, setRequests] = useState<UsageRequest[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "empty" | "error">("loading");

  useEffect(() => {
    let ignore = false;

    async function loadCostTelemetry() {
      try {
        const [summaryResponse, requestsResponse] = await Promise.all([
          fetch(`${apiBaseUrl}/ai/cost/summary`),
          fetch(`${apiBaseUrl}/ai/cost/requests?limit=25`),
        ]);
        if (!summaryResponse.ok || !requestsResponse.ok) {
          throw new Error("AI cost API unavailable");
        }
        const summaryPayload = (await summaryResponse.json()) as CostSummary;
        const requestsPayload = (await requestsResponse.json()) as UsageRequestsResponse;
        if (ignore) {
          return;
        }
        setSummary(summaryPayload);
        setRequests(requestsPayload.requests);
        setStatus(summaryPayload.totals.request_count > 0 ? "ready" : "empty");
      } catch {
        if (!ignore) {
          setStatus("error");
        }
      }
    }

    void loadCostTelemetry();
    return () => {
      ignore = true;
    };
  }, []);

  if (status === "loading") {
    return <p className="text-body-sm text-ink-subtle">Loading OpenRouter cost telemetry.</p>;
  }

  if (status === "error") {
    return <p className="text-body-sm text-ink-subtle">AI cost data is unavailable.</p>;
  }

  if (status === "empty" || summary === null) {
    return <p className="text-body-sm text-ink-subtle">No OpenRouter requests recorded yet.</p>;
  }

  const budgetPercent = clamp(Number(summary.budget.percent_used), 0, 100);

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

function formatUsd(value: string) {
  return `$${Number(value).toFixed(4)}`;
}

function formatLatency(value: number | null) {
  return value === null ? "n/a" : `${value}ms`;
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(Number.isFinite(value) ? value : min, min), max);
}
