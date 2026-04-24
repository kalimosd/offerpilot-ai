import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "OfferPilot",
  description: "AI-powered career assistant",
};

function Nav() {
  const links = [
    { href: "/", label: "Chat", icon: "💬" },
    { href: "/tracker", label: "Tracker", icon: "📋" },
    { href: "/outputs", label: "Outputs", icon: "📁" },
  ];
  return (
    <nav className="w-16 border-r border-zinc-200 flex flex-col items-center py-6 gap-6 bg-white">
      <div className="text-lg font-bold">OP</div>
      {links.map((l) => (
        <Link
          key={l.href}
          href={l.href}
          className="flex flex-col items-center gap-1 text-xs text-zinc-500 hover:text-zinc-900 transition-colors"
        >
          <span className="text-xl">{l.icon}</span>
          {l.label}
        </Link>
      ))}
    </nav>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh">
      <body className="antialiased">
        <div className="flex h-screen">
          <Nav />
          <main className="flex-1 overflow-hidden">{children}</main>
        </div>
      </body>
    </html>
  );
}
