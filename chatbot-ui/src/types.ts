export type HealthResponse = {
  status: string;
  domain: string;
  provider: string;
};

export type ChatResponse = {
  response: string;
  on_topic: boolean;
};

export type ThemeTokenSet = {
  displayName: string;
  tagline: string;
  domainLabel: string;
  fontDisplay: string;
  fontBody: string;
  background: string;
  foreground: string;
  muted: string;
  mutedForeground: string;
  panel: string;
  panelForeground: string;
  border: string;
  accent: string;
  accentForeground: string;
  bubbleUser: string;
  bubbleAssistant: string;
  shadow: string;
  success: string;
  warning: string;
  danger: string;
  signature: "health" | "food" | "fallback";
  signatureOpacity: string;
  backdrop: string;
};

export type ThemeDetails = ThemeTokenSet & {
  domain: string;
};

export type MessageRole = "assistant" | "user" | "error";

export type Message = {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: string;
  loading?: boolean;
  onTopic?: boolean;
};
