import type { CSSProperties } from "react";
import { AlertTriangle, Bot, User } from "lucide-react";
import type { Message, ThemeDetails } from "../types";
import { cn } from "../lib/utils";

type Props = {
  message: Message;
  theme: ThemeDetails;
};

export function ChatMessage({ message, theme }: Props) {
  const isUser = message.role === "user";
  const isError = message.role === "error";
  const outlineColor = isUser ? "var(--accent)" : "var(--border)";

  const bubbleStyle = isUser
    ? ({
        background: "var(--bubble-user)",
        boxShadow: "0 18px 40px var(--shadow), inset 0 0 0 1px color-mix(in srgb, var(--accent) 24%, transparent)"
      } as CSSProperties)
    : ({
        background: "var(--bubble-assistant)",
        boxShadow: "0 18px 40px var(--shadow), inset 0 0 0 1px color-mix(in srgb, var(--border) 70%, transparent)"
      } as CSSProperties);

  return (
    <article
      className={cn(
        "group flex gap-3 md:gap-4",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      {!isUser ? (
        <div
          className={cn(
            "mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border shadow-sm",
            isError
              ? "border-[color:var(--danger)] text-[color:var(--danger)]"
              : "border-[color:var(--border)] bg-[color:var(--panel)] text-[color:var(--accent)]"
          )}
          style={
            isError
              ? { backgroundColor: "color-mix(in srgb, var(--danger) 10%, transparent)" }
              : undefined
          }
        >
          {isError ? <AlertTriangle className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
        </div>
      ) : null}
      <div className={cn("max-w-[92%] md:max-w-[75%]", isUser && "items-end")}>
        <div
          className={cn("rounded-[1.35rem] px-4 py-3 text-sm leading-6", isUser ? "text-accent-foreground" : "text-panel-foreground")}
          style={bubbleStyle}
        >
          <p className="whitespace-pre-wrap break-words">{message.content}</p>
          {message.loading ? (
            <div className="mt-2 flex items-center gap-1.5" aria-label="Assistant is typing">
              <span className="typing-dot" />
              <span className="typing-dot [animation-delay:120ms]" />
              <span className="typing-dot [animation-delay:240ms]" />
            </div>
          ) : null}
        </div>
        <div
          className={cn(
            "mt-2 flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-muted-foreground",
            isUser && "justify-end"
          )}
        >
          {isUser ? <User className="h-3.5 w-3.5" /> : <Bot className="h-3.5 w-3.5" />}
          <span>{message.timestamp}</span>
          {!isUser && message.onTopic !== undefined ? (
            <span
              className={cn(
                "rounded-full px-2 py-0.5",
                message.onTopic
                  ? "text-[color:var(--success)]"
                  : "text-[color:var(--warning)]"
              )}
              style={{
                backgroundColor: message.onTopic
                  ? "color-mix(in srgb, var(--success) 10%, transparent)"
                  : "color-mix(in srgb, var(--warning) 10%, transparent)",
                boxShadow: message.onTopic
                  ? "inset 0 0 0 1px color-mix(in srgb, var(--success) 20%, transparent)"
                  : "inset 0 0 0 1px color-mix(in srgb, var(--warning) 20%, transparent)"
              }}
            >
              {message.onTopic ? "Domain aware" : "Domain redirect"}
            </span>
          ) : null}
        </div>
      </div>
      {isUser ? (
        <div
          className="mt-1 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border text-[color:var(--accent)] shadow-sm"
          style={{
            borderColor: "color-mix(in srgb, var(--accent) 25%, transparent)",
            backgroundColor: "color-mix(in srgb, var(--accent) 12%, transparent)"
          }}
        >
          <User className="h-4 w-4" />
        </div>
      ) : null}
    </article>
  );
}