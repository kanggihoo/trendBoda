-- migrate:up

CREATE TABLE geeknews_summaries (
  item_id BIGINT PRIMARY KEY REFERENCES geeknews_items(id) ON DELETE CASCADE,
  summary TEXT NOT NULL,
  model TEXT NOT NULL,
  generated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ai_usage_records (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  feature TEXT NOT NULL,
  status TEXT NOT NULL,
  requested_models TEXT[] NOT NULL,
  actual_model TEXT,
  prompt_tokens INTEGER,
  completion_tokens INTEGER,
  total_tokens INTEGER,
  estimated_cost_usd NUMERIC(18, 12),
  latency_ms INTEGER NOT NULL,
  pricing_source TEXT,
  pricing_snapshot JSONB,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT ai_usage_records_status_check
    CHECK (status IN ('success', 'failure'))
);

CREATE INDEX ai_usage_records_feature_created_at_idx
  ON ai_usage_records (feature, created_at DESC);

CREATE INDEX ai_usage_records_actual_model_created_at_idx
  ON ai_usage_records (actual_model, created_at DESC);

-- migrate:down

DROP TABLE IF EXISTS ai_usage_records;
DROP TABLE IF EXISTS geeknews_summaries;
