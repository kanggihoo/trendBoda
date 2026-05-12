"use client";

import type { GeekNewsItem } from "./lib/contracts";
import { formatDate, formatOptionalDate } from "./lib/dashboard-format";
import { fetchGeekNewsItems } from "./lib/trendboda-api";
import { useRemoteResource } from "./lib/use-remote-resource";

function hasNoDeveloperTrendSignals(items: GeekNewsItem[]) {
  return items.length === 0;
}

export function GeekNewsList() {
  const items = useRemoteResource(fetchGeekNewsItems, hasNoDeveloperTrendSignals);

  if (items.status === "loading") {
    return (
      <p className="text-body-sm text-ink-subtle">Loading recent Developer Trend Source signals.</p>
    );
  }

  if (items.status === "error") {
    return <p className="text-body-sm text-ink-subtle">GeekNews items are unavailable.</p>;
  }

  if (items.status === "empty") {
    return <p className="text-body-sm text-ink-subtle">No GeekNews items fetched yet.</p>;
  }

  return <GeekNewsItemsView items={items.data} />;
}

function GeekNewsItemsView({ items }: { items: GeekNewsItem[] }) {
  return (
    <ul className="grid list-none gap-md p-0">
      {items.map((item) => (
        <GeekNewsSignalRow item={item} key={item.id} />
      ))}
    </ul>
  );
}

function GeekNewsSignalRow({ item }: { item: GeekNewsItem }) {
  return (
    <li className="grid items-center gap-md border-b border-hairline py-md sm:grid-cols-[minmax(0,1fr)_auto]">
      <div className="grid min-w-0 gap-xs">
        <a
          className="[overflow-wrap:anywhere] font-semibold text-ink no-underline hover:underline"
          href={item.source_url}
          rel="noreferrer"
          target="_blank"
        >
          {item.title}
        </a>
        <p className="max-w-[680px] text-body-sm text-ink-muted">{item.content_text}</p>
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
  );
}
