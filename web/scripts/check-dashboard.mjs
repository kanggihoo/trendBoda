import { access, readFile } from "node:fs/promises";

const requiredFiles = [
  "app/fonts/PretendardVariable.woff2",
  "app/layout.tsx",
  "app/page.tsx",
  "app/ai-cost-dashboard.tsx",
  "app/globals.css",
  "components.json",
  "next.config.ts",
  "package.json",
  "pnpm-lock.yaml",
  "postcss.config.mjs",
  "tailwind.config.js",
  "tailwind.theme.json",
];

for (const file of requiredFiles) {
  await access(new URL(`../${file}`, import.meta.url));
}

try {
  await access(new URL("../package-lock.json", import.meta.url));
  throw new Error("web/package-lock.json must not exist; use pnpm-lock.yaml only.");
} catch (error) {
  if (error instanceof Error && "code" in error && error.code === "ENOENT") {
    // Expected: pnpm is the only package manager for web.
  } else {
    throw error;
  }
}

const packageJson = JSON.parse(
  await readFile(new URL("../package.json", import.meta.url), "utf8"),
);
const page = await readFile(new URL("../app/page.tsx", import.meta.url), "utf8");
const geeknewsList = await readFile(new URL("../app/geeknews-list.tsx", import.meta.url), "utf8");
const aiCostDashboard = await readFile(
  new URL("../app/ai-cost-dashboard.tsx", import.meta.url),
  "utf8",
);
const layout = await readFile(new URL("../app/layout.tsx", import.meta.url), "utf8");
const globals = await readFile(new URL("../app/globals.css", import.meta.url), "utf8");
const tailwindConfig = await readFile(new URL("../tailwind.config.js", import.meta.url), "utf8");
const tailwindTheme = await readFile(new URL("../tailwind.theme.json", import.meta.url), "utf8");

if (!packageJson.packageManager?.startsWith("pnpm@")) {
  throw new Error("web/package.json must declare a pnpm packageManager version.");
}

if (!packageJson.dependencies?.["lucide-react"]) {
  throw new Error("web/package.json must include lucide-react for dashboard icons.");
}

for (const cssImport of ["@tailwind base;", "@tailwind components;", "@tailwind utilities;"]) {
  if (!globals.includes(cssImport)) {
    throw new Error(`web/app/globals.css must include ${cssImport}`);
  }
}

if (!tailwindConfig.includes('require("./tailwind.theme.json")')) {
  throw new Error("Tailwind config must consume web/tailwind.theme.json.");
}

if (!tailwindConfig.includes("lineHeight")) {
  throw new Error("Tailwind config must restore typography line heights omitted by export.");
}

if (!tailwindTheme.includes('"primary": "#23835b"')) {
  throw new Error("Tailwind theme snapshot must include DESIGN-v2 primary color.");
}

if (!page.includes("TrendBoda")) {
  throw new Error("Dashboard shell must render TrendBoda brand text.");
}

if (!page.includes("Developer Trend Source")) {
  throw new Error("Dashboard shell must use domain language from CONTEXT.md.");
}

if (!geeknewsList.includes("/geeknews/items")) {
  throw new Error("Dashboard shell must request GeekNews items from FastAPI.");
}

if (!page.includes("AiCostDashboard")) {
  throw new Error("Dashboard shell must render the AI Cost Dashboard.");
}

for (const endpoint of ["/ai/cost/summary", "/ai/cost/requests"]) {
  if (!aiCostDashboard.includes(endpoint)) {
    throw new Error(`AI Cost Dashboard must request FastAPI endpoint: ${endpoint}`);
  }
}

if (!layout.includes("next/font/local") || !layout.includes("PretendardVariable.woff2")) {
  throw new Error("Dashboard shell must load local Pretendard through next/font/local.");
}

for (const className of ["text-display", "border-hairline", "bg-surface-1", "text-ink-subtle"]) {
  if (
    !page.includes(className) &&
    !geeknewsList.includes(className) &&
    !aiCostDashboard.includes(className)
  ) {
    throw new Error(`Dashboard shell must use Tailwind design token class: ${className}`);
  }
}

for (const stateText of [
  "Loading recent Developer Trend Source signals.",
  "GeekNews items are unavailable.",
  "No GeekNews items fetched yet.",
  "Loading OpenRouter cost telemetry.",
  "AI cost data is unavailable.",
  "No OpenRouter requests recorded yet.",
]) {
  if (!geeknewsList.includes(stateText) && !aiCostDashboard.includes(stateText)) {
    throw new Error(`Dashboard shell must cover state text: ${stateText}`);
  }
}

if (!geeknewsList.includes("Published") || !geeknewsList.includes("Fetched")) {
  throw new Error("Dashboard shell must show both publish time and fetch time.");
}

if (!geeknewsList.includes("summary?.summary")) {
  throw new Error("Dashboard shell must show stored GeekNews summaries when present.");
}

for (const dashboardText of [
  "Monthly budget",
  "Latency",
  "Error status",
  "By date",
  "By model",
  "By feature",
  "Recent requests",
]) {
  if (!aiCostDashboard.includes(dashboardText)) {
    throw new Error(`AI Cost Dashboard must cover product text: ${dashboardText}`);
  }
}
