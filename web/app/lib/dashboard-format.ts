export function formatUsd(value: string) {
  return `$${Number(value).toFixed(4)}`;
}

export function formatLatency(value: number | null) {
  return value === null ? "n/a" : `${value}ms`;
}

export function formatOptionalDate(value: string | null) {
  return value ? formatDate(value) : "Unknown";
}

export function formatDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

export function clampPercent(value: string) {
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) {
    return 0;
  }
  return Math.min(Math.max(numericValue, 0), 100);
}
