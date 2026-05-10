import { GeekNewsList } from "./geeknews-list";

const checks = [
  "GeekNews source collection",
  "OpenRouter summary usage",
  "AI cost dashboard",
  "Interactive Bot commands",
];

export default function Home() {
  return (
    <main className="grid min-h-screen gap-xl px-page-x-mobile py-xxl text-ink md:px-page-x-desktop md:py-section">
      <section className="max-w-[720px] self-end" aria-labelledby="dashboard-title">
        <p className="mb-md text-caption uppercase text-ink-subtle">Local first slice</p>
        <h1 id="dashboard-title" className="mb-lg text-display">
          TrendBoda
        </h1>
        <p className="max-w-[620px] text-body text-ink-muted">
          Developer Trend Source signals, summaries, and OpenRouter cost tracking will appear
          here as first-slice capabilities land.
        </p>
      </section>

      <section
        className="w-full max-w-[920px] self-start border-t border-hairline pt-xl"
        aria-label="First slice readiness"
      >
        <h2 className="mb-lg text-title">Dashboard Shell</h2>
        <div className="grid grid-cols-[repeat(auto-fit,minmax(220px,1fr))] gap-md">
          {checks.map((check) => (
            <div
              className="flex min-h-[56px] items-center gap-[10px] rounded-md border border-hairline bg-surface-1 px-lg py-[14px] text-body-sm text-ink"
              key={check}
            >
              <span
                className="h-[10px] w-[10px] flex-none rounded-full bg-success"
                aria-hidden="true"
              />
              <span>{check}</span>
            </div>
          ))}
        </div>
      </section>

      <section
        className="w-full max-w-[920px] self-start border-t border-hairline pt-xl"
        aria-label="Recent GeekNews items"
      >
        <h2 className="mb-lg text-title">Recent GeekNews</h2>
        <GeekNewsList />
      </section>
    </main>
  );
}
