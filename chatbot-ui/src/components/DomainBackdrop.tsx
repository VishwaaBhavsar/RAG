import type { CSSProperties } from "react";
import type { ThemeDetails } from "../types";
import { cn } from "../lib/utils";

type Props = {
  theme: ThemeDetails;
};

export function DomainBackdrop({ theme }: Props) {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0" style={{ background: theme.backdrop }} />
      {theme.signature === "health" ? (
        <div className="absolute inset-0 opacity-60">
          <div className="health-grid absolute inset-0" />
          <div className="health-scan absolute left-0 right-0 top-1/3 h-px bg-[color:var(--accent)] motion-safe:animate-scan" />
          <div
            className="absolute left-[8%] top-[16%] h-32 w-32 rounded-full border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 40%, transparent)" }}
          />
          <div
            className="absolute right-[9%] bottom-[14%] h-44 w-44 rounded-full border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 35%, transparent)" }}
          />
        </div>
      ) : theme.signature === "food" ? (
        <div className="absolute inset-0 opacity-60">
          <div className="food-rings absolute left-[4%] top-[8%] h-72 w-72 rounded-full" />
          <div className="food-grain absolute inset-0" />
          <div
            className="absolute right-[10%] top-[18%] h-36 w-36 rotate-[-11deg] rounded-[32px] border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 35%, transparent)" }}
          />
          <div
            className="absolute bottom-[10%] left-[12%] h-24 w-24 rounded-full border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 40%, transparent)" }}
          />
        </div>
      ) : (
        <div className="absolute inset-0 opacity-55">
          <div className="fallback-orbits absolute inset-0" />
          <div
            className="absolute left-[10%] top-[12%] h-40 w-40 rounded-full border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 35%, transparent)" }}
          />
          <div
            className="absolute right-[8%] bottom-[12%] h-56 w-56 rounded-full border border-[color:var(--border)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--panel) 25%, transparent)" }}
          />
        </div>
      )}
      <div className="absolute inset-0 bg-[linear-gradient(180deg,transparent,rgba(255,255,255,0.18))]" />
    </div>
  );
}

export function ThemeChip({
  label,
  tone = "accent"
}: {
  label: string;
  tone?: "accent" | "muted";
}) {
  const accentStyle: CSSProperties | undefined =
    tone === "accent"
      ? {
          backgroundColor: "color-mix(in srgb, var(--accent) 12%, transparent)",
          boxShadow: "inset 0 0 0 1px color-mix(in srgb, var(--accent) 20%, transparent)"
        }
      : undefined;

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.28em]",
        tone === "accent"
          ? "text-accent"
          : "bg-panel text-muted-foreground border border-border"
      )}
      style={accentStyle}
    >
      {label}
    </span>
  );
}