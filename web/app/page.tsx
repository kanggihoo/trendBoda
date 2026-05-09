import { GeekNewsList } from "./geeknews-list";

const checks = [
  "GeekNews source collection",
  "OpenRouter summary usage",
  "AI cost dashboard",
  "Interactive Bot commands",
];

export default function Home() {
  return (
    <main className="shell">
      <section className="intro" aria-labelledby="dashboard-title">
        <p className="eyebrow">Local first slice</p>
        <h1 id="dashboard-title">TrendBoda</h1>
        <p className="summary">
          Developer Trend Source signals, summaries, and OpenRouter cost tracking will appear
          here as first-slice capabilities land.
        </p>
      </section>

      <section className="panel" aria-label="First slice readiness">
        <h2>Dashboard Shell</h2>
        <div className="status-grid">
          {checks.map((check) => (
            <div className="status-item" key={check}>
              <span className="dot" aria-hidden="true" />
              <span>{check}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="panel" aria-label="Recent GeekNews items">
        <h2>Recent GeekNews</h2>
        <GeekNewsList />
      </section>
    </main>
  );
}
