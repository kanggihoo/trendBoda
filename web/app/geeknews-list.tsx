"use client";

import { useEffect, useState } from "react";

type GeekNewsItem = {
  id: number;
  title: string;
  source_url: string;
  published_at: string | null;
  fetched_at: string;
};

type GeekNewsResponse = {
  items: GeekNewsItem[];
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
    return <p className="muted">Loading recent Developer Trend Source signals.</p>;
  }

  if (status === "error") {
    return <p className="muted">GeekNews items are unavailable.</p>;
  }

  if (status === "empty") {
    return <p className="muted">No GeekNews items fetched yet.</p>;
  }

  return (
    <ul className="signal-list">
      {items.map((item) => (
        <li key={item.id}>
          <a href={item.source_url} rel="noreferrer" target="_blank">
            {item.title}
          </a>
          <span>{formatDate(item.published_at ?? item.fetched_at)}</span>
        </li>
      ))}
    </ul>
  );
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}
