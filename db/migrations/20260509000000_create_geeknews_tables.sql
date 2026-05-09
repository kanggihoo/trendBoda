-- migrate:up

CREATE TABLE geeknews_fetch_runs (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  source_name TEXT NOT NULL,
  status TEXT NOT NULL,
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  item_count INTEGER NOT NULL DEFAULT 0,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT geeknews_fetch_runs_status_check
    CHECK (status IN ('success', 'failure'))
);

CREATE INDEX geeknews_fetch_runs_source_fetched_at_idx
  ON geeknews_fetch_runs (source_name, fetched_at DESC);

CREATE TABLE geeknews_items (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  fetch_run_id BIGINT REFERENCES geeknews_fetch_runs(id) ON DELETE SET NULL,
  source_name TEXT NOT NULL,
  external_id TEXT NOT NULL,
  title TEXT NOT NULL,
  source_url TEXT NOT NULL,
  published_at TIMESTAMPTZ,
  fetched_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  CONSTRAINT geeknews_items_source_external_id_unique
    UNIQUE (source_name, external_id)
);

CREATE INDEX geeknews_items_published_at_idx
  ON geeknews_items (published_at DESC NULLS LAST, id DESC);

CREATE INDEX geeknews_items_fetched_at_idx
  ON geeknews_items (fetched_at DESC, id DESC);

-- migrate:down

DROP TABLE IF EXISTS geeknews_items;
DROP TABLE IF EXISTS geeknews_fetch_runs;
