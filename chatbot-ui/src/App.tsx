import { MessageSquareText, RefreshCw, Send, Stethoscope, UtensilsCrossed } from "lucide-react";
import { type KeyboardEvent, useEffect, useRef, useState } from "react";
import { fetchHealth, sendChat } from "./api";
import { Button } from "./components/ui/button";
import { ChatMessage } from "./components/ChatMessage";
import { DomainBackdrop, ThemeChip } from "./components/DomainBackdrop";
import { LoadingState } from "./components/LoadingState";
import { createTheme, themeVars } from "./theme";
import type { ChatResponse, HealthResponse, Message, ThemeDetails } from "./types";
import { cn } from "./lib/utils";

function formatNow(): string {
  return new Date().toLocaleTimeString([], {
    hour: "numeric",
    minute: "2-digit"
  });
}

function makeId(): string {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function introText(theme: ThemeDetails): string {
  if (theme.domain === "healthcare") {
    return "Ask about symptoms, wellness, prevention, or when to seek medical care.";
  }
  if (theme.domain === "food") {
    return "Ask about ingredients, substitutions, cooking methods, meal planning, or food safety.";
  }
  return `Ask anything that fits the ${theme.displayName.toLowerCase()} domain.`;
}

function domainIcon(theme: ThemeDetails) {
  if (theme.domain === "healthcare") return <Stethoscope className="h-4 w-4" />;
  if (theme.domain === "food") return <UtensilsCrossed className="h-4 w-4" />;
  return <MessageSquareText className="h-4 w-4" />;
}

function useReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduced(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);

  return reduced;
}

export default function App() {
  const [bootState, setBootState] = useState<
    | { status: "loading" }
    | { status: "error"; error: string }
    | { status: "ready"; health: HealthResponse; theme: ThemeDetails }
  >({ status: "loading" });
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);
  const listRef = useRef<HTMLDivElement | null>(null);
  const reducedMotion = useReducedMotion();

  useEffect(() => {
    let alive = true;

    async function load() {
      setBootState({ status: "loading" });
      try {
        const health = await fetchHealth();
        if (!alive) {
          return;
        }

        const theme = createTheme(health.domain);
        document.documentElement.style.setProperty("color-scheme", "light");
        document.title = `${theme.displayName} Chat`;
        setBootState({ status: "ready", health, theme });
        setMessages([
          {
            id: makeId(),
            role: "assistant",
            content: `${theme.displayName} is live. ${introText(theme)}`,
            timestamp: formatNow()
          }
        ]);
      } catch (exception) {
        const message =
          exception instanceof Error
            ? exception.message
            : "Unable to load the backend health check.";
        if (alive) {
          setBootState({ status: "error", error: message });
        }
      }
    }

    load();
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTo({
        top: listRef.current.scrollHeight,
        behavior: reducedMotion ? "auto" : "smooth"
      });
    }
  }, [messages, isSending, reducedMotion]);

  async function handleSend() {
    if (bootState.status !== "ready" || isSending) {
      return;
    }

    const message = draft.trim();
    if (!message) {
      return;
    }

    setError(null);
    setDraft("");
    setIsSending(true);

    const placeholderId = makeId();
    setMessages((current) => [
      ...current,
      {
        id: makeId(),
        role: "user",
        content: message,
        timestamp: formatNow()
      },
      {
        id: placeholderId,
        role: "assistant",
        content: "Thinking...",
        timestamp: formatNow(),
        loading: true
      }
    ]);

    try {
      const response: ChatResponse = await sendChat(message);
      setMessages((current) =>
        current.map((entry) =>
          entry.id === placeholderId
            ? {
                id: placeholderId,
                role: "assistant",
                content: response.response,
                timestamp: formatNow(),
                onTopic: response.on_topic
              }
            : entry
        )
      );
    } catch (exception) {
      const messageText =
        exception instanceof Error
          ? exception.message
          : "Unable to send the message right now.";
      setMessages((current) =>
        current.map((entry) =>
          entry.id === placeholderId
            ? {
                id: placeholderId,
                role: "error",
                content: `Request failed. ${messageText}`,
                timestamp: formatNow()
              }
            : entry
        )
      );
      setError(messageText);
    } finally {
      setIsSending(false);
    }
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSend();
    }
  }

  if (bootState.status === "loading") {
    return <LoadingState />;
  }

  if (bootState.status === "error") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background px-6 text-foreground">
        <div className="max-w-lg rounded-[2rem] border border-border bg-panel p-6 shadow-glow">
          <div
            className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl text-[color:var(--danger)]"
            style={{ backgroundColor: "color-mix(in srgb, var(--danger) 10%, transparent)" }}
          >
            <RefreshCw className="h-5 w-5" />
          </div>
          <p className="font-display text-2xl">Could not load the chat theme</p>
          <p className="mt-2 text-sm text-muted-foreground">{bootState.error}</p>
          <Button className="mt-5" onClick={() => window.location.reload()}>
            Retry
          </Button>
        </div>
      </div>
    );
  }

  const theme = bootState.theme;
  const style = themeVars(theme);

  return (
    <div
      className="relative min-h-screen overflow-hidden bg-background text-foreground"
      style={style}
    >
      <DomainBackdrop theme={theme} />
      <main className="relative mx-auto flex min-h-screen w-full max-w-7xl flex-col gap-6 px-4 py-4 md:px-6 md:py-6 lg:px-8">
        <header className="grid gap-4 lg:grid-cols-[minmax(0,360px)_minmax(0,1fr)] lg:items-end">
          <section className="relative overflow-hidden rounded-[2rem] border border-border bg-panel p-5 shadow-glow backdrop-blur-xl md:p-6">
            <div className="absolute inset-0 opacity-70 [background:linear-gradient(135deg,rgba(255,255,255,0.28),transparent_55%)]" />
            <div className="relative flex items-start justify-between gap-4">
              <div>
                <ThemeChip label={bootState.health.domain} />
                <h1 className="mt-4 font-display text-3xl leading-none md:text-4xl">
                  {theme.displayName}
                </h1>
                <p className="mt-3 max-w-sm text-sm leading-6 text-muted-foreground">
                  {theme.tagline}
                </p>
              </div>
              <div
                className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border text-accent opacity-90"
                style={{
                  borderColor: "color-mix(in srgb, var(--accent) 18%, transparent)",
                  backgroundColor: "color-mix(in srgb, var(--accent) 8%, transparent)"
                }}
              >
                {domainIcon(theme)}
              </div>
            </div>
            <div className="relative mt-5 flex flex-wrap gap-2 text-xs text-muted-foreground">
              <span className="inline-flex items-center rounded-full border border-border bg-background px-3 py-1 opacity-90">
                Backend: {bootState.health.provider}
              </span>
              <span className="inline-flex items-center rounded-full border border-border bg-background px-3 py-1 opacity-90">
                {bootState.health.status.toUpperCase()}
              </span>
              <span className="inline-flex items-center rounded-full border border-border bg-background px-3 py-1 opacity-90">
                Domain locked
              </span>
            </div>
          </section>
          <section className="grid gap-4 md:grid-cols-3">
            <div className="rounded-[1.5rem] border border-border bg-panel p-4 shadow-glow backdrop-blur-xl">
              <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Session
              </p>
              <p className="mt-2 font-display text-xl">Live conversation</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                Enter to send. Shift+Enter adds a line break.
              </p>
            </div>
            <div className="rounded-[1.5rem] border border-border bg-panel p-4 shadow-glow backdrop-blur-xl">
              <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Theme
              </p>
              <p className="mt-2 font-display text-xl">{theme.domainLabel}</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                The UI palette, background, and accent language are derived from
                the backend&apos;s active domain.
              </p>
            </div>
            <div className="rounded-[1.5rem] border border-border bg-panel p-4 shadow-glow backdrop-blur-xl">
              <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Response mode
              </p>
              <p className="mt-2 font-display text-xl">Guarded by design</p>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">
                The backend keeps replies confined to the configured subject matter.
              </p>
            </div>
          </section>
        </header>

        <section className="grid flex-1 gap-5 lg:grid-cols-[minmax(0,300px)_minmax(0,1fr)]">
          <aside className="relative overflow-hidden rounded-[2rem] border border-border bg-panel p-5 shadow-glow backdrop-blur-xl md:p-6">
            <div className="absolute inset-0 opacity-50 [background:linear-gradient(180deg,rgba(255,255,255,0.22),transparent_40%)]" />
            <div className="relative">
              <p className="text-xs uppercase tracking-[0.28em] text-muted-foreground">
                {theme.displayName} space
              </p>
              <div className="mt-3 flex items-center gap-3">
                <div
                  className="flex h-10 w-10 items-center justify-center rounded-2xl text-accent"
                  style={{ backgroundColor: "color-mix(in srgb, var(--accent) 12%, transparent)" }}
                >
                  {domainIcon(theme)}
                </div>
                <div>
                  <p className="font-display text-2xl">{theme.domainLabel}</p>
                  <p className="text-sm text-muted-foreground">{theme.tagline}</p>
                </div>
              </div>
              <div className="mt-5 space-y-3 rounded-[1.5rem] border border-border bg-background p-4 opacity-90">
                <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                  Quick notes
                </p>
                <ul className="space-y-2 text-sm leading-6 text-panel-foreground">
                  <li>- Theming resolves from the backend on first paint.</li>
                  <li>- The dev server proxies `/health` and `/chat` to port 8000.</li>
                  <li>- Domain-specific styling falls back deterministically.</li>
                </ul>
              </div>
              <div className="mt-5 rounded-[1.5rem] border border-border bg-background p-4 opacity-90">
                <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">
                  Today&apos;s shape
                </p>
                <p className="mt-2 text-sm leading-6 text-panel-foreground">
                  {theme.domain === "healthcare"
                    ? "Clinical, calm, and legible."
                    : theme.domain === "food"
                      ? "Warm, editorial, and appetite-forward."
                      : "Composable, colored by the active domain."}
                </p>
              </div>
            </div>
          </aside>

          <section className="flex min-h-[70vh] flex-col overflow-hidden rounded-[2rem] border border-border bg-panel shadow-glow backdrop-blur-xl">
            <div
              ref={listRef}
              className="flex-1 space-y-4 overflow-y-auto px-4 py-4 sm:px-6 sm:py-6"
            >
              {messages.map((message) => (
                <ChatMessage key={message.id} message={message} theme={theme} />
              ))}
            </div>

            <div className="border-t border-border bg-background px-4 py-4 opacity-95 sm:px-6">
              {error ? (
                <div
                  className="mb-3 rounded-2xl border px-4 py-3 text-sm text-[color:var(--danger)]"
                  style={{
                    borderColor: "color-mix(in srgb, var(--danger) 20%, transparent)",
                    backgroundColor: "color-mix(in srgb, var(--danger) 8%, transparent)"
                  }}
                >
                  {error}
                </div>
              ) : null}
              <label className="mb-2 block text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Message
              </label>
              <div className="flex flex-col gap-3 md:flex-row md:items-end">
                <textarea
                  aria-label="Message"
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a question..."
                  rows={4}
                  className={cn(
                    "min-h-28 flex-1 resize-none rounded-[1.4rem] border border-border bg-panel px-4 py-3 text-sm leading-6 text-foreground shadow-sm shadow-[color:var(--shadow)] outline-none transition placeholder:text-muted-foreground focus-visible:ring-2 focus-visible:ring-accent focus-visible:ring-offset-2 focus-visible:ring-offset-background motion-reduce:transition-none"
                  )}
                />
                <Button
                  className="md:w-40"
                  onClick={() => void handleSend()}
                  disabled={isSending || draft.trim().length === 0}
                >
                  {isSending ? (
                    <>
                      <RefreshCw className="h-4 w-4 animate-spin" />
                      Sending
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4" />
                      Send
                    </>
                  )}
                </Button>
              </div>
              <div className="mt-3 flex items-center justify-between gap-3 text-xs text-muted-foreground">
                <span>
                  {isSending
                    ? "Waiting for the backend response..."
                    : "Keyboard friendly. Focus rings stay visible."}
                </span>
                <span>{messages.length} messages</span>
              </div>
            </div>
          </section>
        </section>
      </main>
    </div>
  );
}