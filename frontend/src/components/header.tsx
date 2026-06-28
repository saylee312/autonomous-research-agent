import { Link, useRouterState } from "@tanstack/react-router";
import { Moon, Sun, Sparkles } from "lucide-react";
import { useTheme } from "@/hooks/use-theme";
import { cn } from "@/lib/utils";

const nav = [
  { to: "/", label: "Chat" },
  { to: "/research", label: "Research" },
  { to: "/documents", label: "RAG" },
];

export function Header() {
  const { theme, toggle } = useTheme();
  const pathname = useRouterState({ select: (s) => s.location.pathname });

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="grid size-9 place-items-center rounded-md bg-primary text-primary-foreground shadow-sm transition-transform group-hover:scale-105">
            <Sparkles className="size-4" strokeWidth={2.5} />
          </div>
          <div className="leading-tight">
            <div className="font-display text-[15px] font-bold tracking-tight">RESEARCH<span className="text-primary">.</span>AGENT</div>
          </div>
        </Link>

        <nav className="hidden md:flex items-center gap-1 rounded-full border border-border bg-card p-1">
          {nav.map((n) => {
            const active = n.to === "/" ? pathname === "/" : pathname.startsWith(n.to);
            return (
              <Link
                key={n.to}
                to={n.to}
                className={cn(
                  "px-4 py-1.5 text-sm font-medium rounded-full transition-colors",
                  active
                    ? "bg-primary text-primary-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {n.label}
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <button
            onClick={toggle}
            aria-label="Toggle theme"
            className="grid size-9 place-items-center rounded-full border border-border bg-card text-foreground transition-colors hover:bg-accent"
          >
            {theme === "dark" ? <Sun className="size-4" /> : <Moon className="size-4" />}
          </button>
        </div>
      </div>
      <div className="md:hidden border-t border-border">
        <div className="mx-auto flex max-w-7xl gap-1 overflow-x-auto px-4 py-2">
          {nav.map((n) => {
            const active = n.to === "/" ? pathname === "/" : pathname.startsWith(n.to);
            return (
              <Link
                key={n.to}
                to={n.to}
                className={cn(
                  "px-3 py-1.5 text-sm rounded-full whitespace-nowrap",
                  active ? "bg-primary text-primary-foreground" : "text-muted-foreground"
                )}
              >
                {n.label}
              </Link>
            );
          })}
        </div>
      </div>
    </header>
  );
}
