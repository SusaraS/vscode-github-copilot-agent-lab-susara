# Copilot Workspace Instructions

## Mandatory Development Checklist

Run these in order before every commit:

```bash
uv run ruff check .                               # 1. Lint — must pass with no errors
uv run uvicorn app.main:app --reload --port 8000  # 2. Build — server must start cleanly
uv run pytest                                     # 3. Test — all tests must pass
```

> No unused imports, no type errors, no skipped tests.

## Project Overview

**Soc Ops** is a Social Bingo web app for in-person mixers (FastAPI + Jinja2 + HTMX). Players mark a 5×5 board by finding people matching prompts; 5 in a row wins.

## Architecture

```
app/
├── main.py          # Routes & HTMX partial-HTML endpoints
├── game_service.py  # GameSession dataclass + in-memory session store
├── game_logic.py    # Board generation, toggle, bingo detection
├── models.py        # Pydantic models: GameState, BingoSquareData, BingoLine
├── data.py          # QUESTIONS list + FREE_SPACE constant
├── templates/       # base.html, home.html, components/
└── static/css/app.css  # Custom utility classes (Tailwind-like)
tests/
├── test_api.py         # httpx integration tests
└── test_game_logic.py  # Unit tests
```

## Key Patterns

- **HTMX partials**: routes return the smallest HTML fragment; never full pages
- **Immutable board**: `BingoSquareData` is frozen; functions return new lists, never mutate
- **Sessions**: `GameSession` dataclass in `_sessions` dict, keyed by signed-cookie UUID
- **State machine**: `GameState` flows `START → PLAYING → BINGO`; check state before acting

## Styling

Use only the custom utilities in `app/static/css/app.css`. No external CSS libraries.

Key classes: `.flex`, `.grid`, `.grid-cols-5`, `.items-center`, `.justify-center`, `.p-1`–`.p-6`, `.gap-1`, `.mx-auto`, `.bg-accent`, `.bg-marked`, `.rounded-lg`, `.shadow-xl`, `.transition-all`

Add new utilities to `app.css` following existing patterns.

## Design Guide (Cyberpunk Neon)

- **Visual direction**: dark futuristic base with neon cyan/pink/lime accents and high legibility.
- **Theme tokens**: use CSS variables in `:root` (`--cyber-bg`, `--cyber-bg-soft`, `--neon-cyan`, `--neon-pink`, `--neon-lime`, `--text-soft`, `--text-muted`).
- **Primary surfaces**: use `bg-cyber-dark`, `neon-panel`, and `neon-bar` for page/background/card/header structure.
- **Interactive elements**: use `btn-neon` for primary CTAs and `chip-btn` for secondary controls.
- **Bingo board states**:
	- idle: `square-idle`
	- marked: `square-marked`
	- winning: `square-winning`
	- free-space emphasis: `square-free`
- **Hover/motion rules**: keep motion smooth and subtle with `hover:lift`, `hover:lift-sm`, `hover:glow-cyan`, `hover:glow-pink`, and low-motion entry (`animate-neon-pop`).
- **Text emphasis**: use `text-neon-cyan`, `text-neon-pink`, `text-neon-soft`, and glow helpers (`text-glow-cyan`, `text-glow-pink`) for hierarchy.
- **Accessibility guardrail**: preserve contrast and avoid heavy glow on dense text blocks.
- **Do not**: add inline styles, import external CSS frameworks, or break HTMX swap roots (`#game-container`).

## Code Conventions

- snake_case, type hints on all signatures, `Final` for constants
- Imports sorted by ruff (stdlib → third-party → local)
- Frozen Pydantic `BaseModel` for immutable data; minimal logic in templates
- API tests use `httpx.AsyncClient` with `ASGITransport`
