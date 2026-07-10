# chatbot-ui

Frontend for the `chatbot/` FastAPI backend. This app uses Vite + React + Tailwind and talks to the backend through a local dev proxy.

## Setup

```powershell
cd chatbot-ui
npm install
npm run dev
```

The Vite dev server proxies these requests to `http://127.0.0.1:8000`:

- `GET /health`
- `POST /chat`

So the frontend can keep using relative fetch URLs without any CORS-specific backend changes.

## Build

```powershell
npm run build
```

## Theme system

The UI does not hard-code a single visual style. On load it:

1. Calls `GET /health`
2. Reads the backend `domain`
3. Selects a hand-authored theme for:
   - `healthcare`
   - `food`
4. Falls back to a deterministic generator for every other domain name

The fallback generator hashes the domain string and turns it into a coherent palette, so a future domain such as `finance` or `legal` still looks intentional without any frontend edits.

Theme tokens are applied through CSS custom properties, and Tailwind utilities read those variables at runtime. That is what makes the shell reskin itself without rebuilds.

## Adding a new hand-designed theme

Edit `src/theme.ts` and add a new branch inside `createTheme(domain)`.

For a good result, define:

- a background treatment
- foreground and muted text colors
- panel and border colors
- an accent color
- a font pairing
- one subtle signature motif

You can keep the same app layout and only swap the theme tokens and backdrop pattern.

## Notes

- The app shows a loading state until `/health` resolves.
- Enter sends the message; `Shift+Enter` adds a newline.
- The chat view auto-scrolls to the latest message.
- Backend errors are shown inline and do not crash the UI.
