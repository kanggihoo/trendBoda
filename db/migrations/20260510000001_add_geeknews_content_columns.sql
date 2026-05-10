-- migrate:up

ALTER TABLE geeknews_items
  ADD COLUMN content_raw_html TEXT NOT NULL DEFAULT '',
  ADD COLUMN content_text TEXT NOT NULL DEFAULT '';

-- migrate:down

ALTER TABLE geeknews_items
  DROP COLUMN IF EXISTS content_text,
  DROP COLUMN IF EXISTS content_raw_html;
