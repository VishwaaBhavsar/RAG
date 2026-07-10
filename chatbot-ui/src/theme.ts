import type { CSSProperties } from "react";
import type { ThemeDetails, ThemeTokenSet } from "./types";

type Palette = Pick<
  ThemeTokenSet,
  | "background"
  | "foreground"
  | "muted"
  | "mutedForeground"
  | "panel"
  | "panelForeground"
  | "border"
  | "accent"
  | "accentForeground"
  | "bubbleUser"
  | "bubbleAssistant"
  | "shadow"
  | "success"
  | "warning"
  | "danger"
  | "fontDisplay"
  | "fontBody"
  | "signature"
  | "signatureOpacity"
  | "backdrop"
>;

const healthcare: Palette = {
  background: "#eef6fb",
  foreground: "#0c1e2d",
  muted: "#dceaf3",
  mutedForeground: "#557188",
  panel: "rgba(255,255,255,0.8)",
  panelForeground: "#0c1e2d",
  border: "rgba(71,103,128,0.18)",
  accent: "#1b7ea6",
  accentForeground: "#f5fbff",
  bubbleUser: "linear-gradient(135deg, #1b7ea6, #175f92)",
  bubbleAssistant: "rgba(255,255,255,0.86)",
  shadow: "rgba(8, 35, 55, 0.18)",
  success: "#1f8a70",
  warning: "#af7a12",
  danger: "#b43c4a",
  fontDisplay:
    '"Segoe UI Semibold", "Trebuchet MS", "Avenir Next", "Helvetica Neue", sans-serif',
  fontBody: '"Aptos", "Gill Sans", "Trebuchet MS", sans-serif',
  signature: "health",
  signatureOpacity: "0.42",
  backdrop:
    "radial-gradient(circle at 20% 20%, rgba(27,126,166,0.18), transparent 28%), radial-gradient(circle at 80% 10%, rgba(31,138,112,0.14), transparent 26%), linear-gradient(180deg, rgba(255,255,255,0.65), rgba(238,246,251,0.92))"
};

const food: Palette = {
  background: "#fff6ea",
  foreground: "#352113",
  muted: "#f7e4c7",
  mutedForeground: "#7b5b42",
  panel: "rgba(255,249,241,0.82)",
  panelForeground: "#352113",
  border: "rgba(150,96,42,0.18)",
  accent: "#b85b22",
  accentForeground: "#fffaf4",
  bubbleUser: "linear-gradient(135deg, #b85b22, #8f5f18)",
  bubbleAssistant: "rgba(255,251,245,0.9)",
  shadow: "rgba(92, 47, 11, 0.18)",
  success: "#2f7d53",
  warning: "#b76b13",
  danger: "#ad3d2f",
  fontDisplay:
    '"Palatino Linotype", "Book Antiqua", "Iowan Old Style", Georgia, serif',
  fontBody: '"Avenir Next", "Trebuchet MS", "Gill Sans", sans-serif',
  signature: "food",
  signatureOpacity: "0.38",
  backdrop:
    "radial-gradient(circle at 15% 15%, rgba(184,91,34,0.16), transparent 24%), radial-gradient(circle at 82% 16%, rgba(181,127,28,0.14), transparent 28%), linear-gradient(180deg, rgba(255,250,244,0.62), rgba(255,246,234,0.95))"
};

function hashDomain(domain: string): number {
  let hash = 0;
  for (let index = 0; index < domain.length; index += 1) {
    hash = (hash * 31 + domain.charCodeAt(index)) >>> 0;
  }
  return hash;
}

function titleCase(domain: string): string {
  return domain
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\s+/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function hsl(hue: number, saturation: number, lightness: number): string {
  return `hsl(${Math.round(hue)} ${Math.round(saturation)}% ${Math.round(lightness)}%)`;
}

function buildFallback(domain: string): Palette {
  const hash = hashDomain(domain || "domain");
  const hue = hash % 360;
  const accentHue = (hue + 24 + (hash % 17)) % 360;
  const surfaceHue = (hue + 8) % 360;
  const isLight = (hash & 1) === 0;
  const bodyHue = (hue + 195) % 360;
  const bgLightness = isLight ? 96 : 12;
  const fgLightness = isLight ? 15 : 92;

  return {
    background: hsl(surfaceHue, 28, bgLightness),
    foreground: hsl(bodyHue, 22, fgLightness),
    muted: hsl(hue, 22, isLight ? 91 : 22),
    mutedForeground: hsl(bodyHue, 14, isLight ? 38 : 72),
    panel: isLight ? "rgba(255,255,255,0.82)" : "rgba(12,16,23,0.82)",
    panelForeground: hsl(bodyHue, 18, fgLightness),
    border: hsl(hue, 18, isLight ? 82 : 30),
    accent: hsl(accentHue, 72, isLight ? 38 : 62),
    accentForeground: isLight ? "#fffaf4" : "#0e1116",
    bubbleUser: `linear-gradient(135deg, ${hsl(accentHue, 68, isLight ? 42 : 60)}, ${hsl(
      hue,
      62,
      isLight ? 33 : 52
    )})`,
    bubbleAssistant: isLight ? "rgba(255,255,255,0.88)" : "rgba(17,23,31,0.86)",
    shadow: isLight ? "rgba(8, 14, 24, 0.14)" : "rgba(0, 0, 0, 0.42)",
    success: hsl((hue + 145) % 360, 52, isLight ? 34 : 63),
    warning: hsl((hue + 36) % 360, 76, isLight ? 42 : 65),
    danger: hsl((hue + 340) % 360, 68, isLight ? 44 : 63),
    fontDisplay: '"Palatino Linotype", "Book Antiqua", "Georgia", serif',
    fontBody: '"Avenir Next", "Trebuchet MS", "Gill Sans", sans-serif',
    signature: "fallback",
    signatureOpacity: "0.32",
    backdrop:
      "radial-gradient(circle at 18% 18%, rgba(255,255,255,0.38), transparent 18%), radial-gradient(circle at 80% 24%, rgba(255,255,255,0.16), transparent 21%), linear-gradient(180deg, rgba(255,255,255,0.35), rgba(255,255,255,0.1))"
  };
}

function buildSignature(domain: string): ThemeDetails["signature"] {
  if (domain === "healthcare") {
    return "health";
  }
  if (domain === "food") {
    return "food";
  }
  return "fallback";
}

export function createTheme(domain: string): ThemeDetails {
  const normalized = (domain || "domain").trim().toLowerCase();
  const base =
    normalized === "healthcare"
      ? healthcare
      : normalized === "food"
        ? food
        : buildFallback(normalized);

  const displayName = titleCase(normalized);
  const tagline =
    normalized === "healthcare"
      ? "Calm, clinically minded guidance for health questions."
      : normalized === "food"
        ? "Warm, useful help for cooking, ingredients, and meals."
        : `A domain-tuned space for ${displayName.toLowerCase()} questions.`;

  return {
    domain: normalized,
    displayName,
    tagline,
    domainLabel: `${displayName} mode`,
    ...base,
    signature: buildSignature(normalized)
  };
}

export function themeVars(theme: ThemeDetails): CSSProperties {
  return {
    ["--background" as never]: theme.background,
    ["--foreground" as never]: theme.foreground,
    ["--muted" as never]: theme.muted,
    ["--muted-foreground" as never]: theme.mutedForeground,
    ["--panel" as never]: theme.panel,
    ["--panel-foreground" as never]: theme.panelForeground,
    ["--border" as never]: theme.border,
    ["--accent" as never]: theme.accent,
    ["--accent-foreground" as never]: theme.accentForeground,
    ["--bubble-user" as never]: theme.bubbleUser,
    ["--bubble-assistant" as never]: theme.bubbleAssistant,
    ["--shadow" as never]: theme.shadow,
    ["--success" as never]: theme.success,
    ["--warning" as never]: theme.warning,
    ["--danger" as never]: theme.danger,
    ["--font-display" as never]: theme.fontDisplay,
    ["--font-body" as never]: theme.fontBody,
    ["--signature-opacity" as never]: theme.signatureOpacity,
    ["--backdrop" as never]: theme.backdrop
  } as CSSProperties;
}