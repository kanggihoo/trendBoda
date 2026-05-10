"use client";

import { useEffect, useState } from "react";

type GeekNewsItem = {
  id: number;
  title: string;
  source_url: string;
  published_at: string | null;
  fetched_at: string;
  summary: GeekNewsSummary | null;
};

type GeekNewsResponse = {
  items: GeekNewsItem[];
};

type GeekNewsSummary = {
  item_id: number;
  summary: string;
  model: string;
  generated_at: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export function GeekNewsList() {
  const [items, setItems] = useState<GeekNewsItem[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "empty" | "error">("loading");

  useEffect(() => {
    let ignore = false;

    async function loadItems() {
      try {
        const response = await fetch(`${apiBaseUrl}/geeknews/items`);
        if (!response.ok) {
          throw new Error(`FastAPI returned ${response.status}`);
        }
        const payload = (await response.json()) as GeekNewsResponse;
        if (ignore) {
          return;
        }
        setItems(payload.items);
        setStatus(payload.items.length > 0 ? "ready" : "empty");
      } catch {
        if (!ignore) {
          setStatus("error");
        }
      }
    }

    void loadItems();
    return () => {
      ignore = true;
    };
  }, []);

  if (status === "loading") {
    return (
      <p className="text-body-sm text-ink-subtle">Loading recent Developer Trend Source signals.</p>
    );
  }

  if (status === "error") {
    return <p className="text-body-sm text-ink-subtle">GeekNews items are unavailable.</p>;
  }

  if (status === "empty") {
    return <p className="text-body-sm text-ink-subtle">No GeekNews items fetched yet.</p>;
  }

  return (
    <ul className="grid list-none gap-md p-0">
      {items.map((item) => (
        <li
          className="grid items-center gap-md border-b border-hairline py-md sm:grid-cols-[minmax(0,1fr)_auto]"
          key={item.id}
        >
          <div className="grid min-w-0 gap-xs">
            <a
              className="[overflow-wrap:anywhere] font-semibold text-ink no-underline hover:underline"
              href={item.source_url}
              rel="noreferrer"
              target="_blank"
            >
              {item.title}
            </a>
            {item.summary?.summary ? (
              <p className="max-w-[680px] text-body-sm text-ink-muted">
                {item.summary.summary}
              </p>
            ) : null}
          </div>
          <div
            className="grid gap-xs text-left sm:justify-items-end sm:text-right"
            aria-label={`${item.title} timeline`}
          >
            <span className="text-caption text-ink-subtle sm:whitespace-nowrap">
              Published {formatOptionalDate(item.published_at)}
            </span>
            <span className="text-caption text-ink-subtle sm:whitespace-nowrap">
              Fetched {formatDate(item.fetched_at)}
            </span>
          </div>
        </li>
      ))}
    </ul>
  );
}

function formatOptionalDate(value: string | null) {
  return value ? formatDate(value) : "Unknown";
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}
