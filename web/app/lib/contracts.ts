export type GeekNewsSummary = {
  item_id: number;
  summary: string;
  model: string;
  generated_at: string;
};

export type GeekNewsItem = {
  id: number;
  title: string;
  source_url: string;
  published_at: string | null;
  fetched_at: string;
  summary: GeekNewsSummary | null;
};

export type GeekNewsResponse = {
  items: GeekNewsItem[];
};

export type CostGroup = {
  date?: string;
  model?: string;
  feature?: string;
  estimated_cost_usd: string;
  request_count: number;
  average_latency_ms: number | null;
  failure_count: number;
};

export type CostSummary = {
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

export type UsageRequest = {
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

export type UsageRequestsResponse = {
  requests: UsageRequest[];
};
