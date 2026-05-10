import type {
  CostSummary,
  GeekNewsItem,
  GeekNewsResponse,
  UsageRequest,
  UsageRequestsResponse,
} from "./contracts";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type AiCostTelemetry = {
  summary: CostSummary;
  requests: UsageRequest[];
};

export async function fetchAiCostTelemetry(): Promise<AiCostTelemetry> {
  const [summary, requests] = await Promise.all([
    fetchJson<CostSummary>("/ai/cost/summary"),
    fetchJson<UsageRequestsResponse>("/ai/cost/requests?limit=25"),
  ]);
  return { summary, requests: requests.requests };
}

export async function fetchGeekNewsItems(): Promise<GeekNewsItem[]> {
  const payload = await fetchJson<GeekNewsResponse>("/geeknews/items");
  return payload.items;
}

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);
  if (!response.ok) {
    throw new Error(`TrendBoda API unavailable: ${response.status}`);
  }
  return (await response.json()) as T;
}
