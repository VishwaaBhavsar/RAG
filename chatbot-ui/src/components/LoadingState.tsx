import { Sparkles } from "lucide-react";

export function LoadingState() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-6 text-foreground">
      <div className="max-w-sm rounded-[1.75rem] border border-border bg-panel px-6 py-7 text-center shadow-glow">
        <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-accent/10 text-accent">
          <Sparkles className="h-5 w-5 animate-pulse" />
        </div>
        <p className="font-display text-xl">Resolving domain theme</p>
        <p className="mt-2 text-sm text-muted-foreground">
          Fetching the backend configuration so the interface can match the active domain.
        </p>
      </div>
    </div>
  );
}
