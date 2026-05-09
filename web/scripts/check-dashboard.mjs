import { access, readFile } from "node:fs/promises";

const requiredFiles = ["app/layout.tsx", "app/page.tsx", "app/globals.css", "next.config.ts"];

for (const file of requiredFiles) {
  await access(new URL(`../${file}`, import.meta.url));
}

const page = await readFile(new URL("../app/page.tsx", import.meta.url), "utf8");
const geeknewsList = await readFile(new URL("../app/geeknews-list.tsx", import.meta.url), "utf8");

if (!page.includes("TrendBoda")) {
  throw new Error("Dashboard shell must render TrendBoda brand text.");
}

if (!page.includes("Developer Trend Source")) {
  throw new Error("Dashboard shell must use domain language from CONTEXT.md.");
}

if (!geeknewsList.includes("/geeknews/items")) {
  throw new Error("Dashboard shell must request GeekNews items from FastAPI.");
}

for (const stateText of [
  "Loading recent Developer Trend Source signals.",
  "GeekNews items are unavailable.",
  "No GeekNews items fetched yet.",
]) {
  if (!geeknewsList.includes(stateText)) {
    throw new Error(`Dashboard shell must cover state text: ${stateText}`);
  }
}

if (!geeknewsList.includes("Published") || !geeknewsList.includes("Fetched")) {
  throw new Error("Dashboard shell must show both publish time and fetch time.");
}
