const designTheme = require("./tailwind.theme.json");

/** @type {import("tailwindcss").Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}"],
  theme: {
    ...designTheme.theme,
    extend: {
      ...designTheme.theme.extend,
      fontFamily: {
        ...designTheme.theme.extend.fontFamily,
        sans: ["var(--font-pretendard)", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "Monaco", "Consolas", "monospace"],
      },
      fontSize: {
        ...designTheme.theme.extend.fontSize,
        display: ["32px", { fontWeight: "700", lineHeight: "1.15" }],
        "title-lg": ["24px", { fontWeight: "700", lineHeight: "1.25" }],
        title: ["18px", { fontWeight: "600", lineHeight: "1.35" }],
        body: ["15px", { fontWeight: "400", lineHeight: "1.55" }],
        "body-sm": ["14px", { fontWeight: "400", lineHeight: "1.5" }],
        caption: ["12px", { fontWeight: "500", letterSpacing: "0.02em", lineHeight: "1.4" }],
        button: ["14px", { fontWeight: "600", letterSpacing: "0.01em", lineHeight: "1.2" }],
        metric: ["28px", { fontWeight: "700", lineHeight: "1.1" }],
        mono: ["13px", { fontWeight: "400", lineHeight: "1.45" }],
      },
    },
  },
};
