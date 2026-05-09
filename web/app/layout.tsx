import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TrendBoda",
  description: "Personal briefing system for source signals",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
