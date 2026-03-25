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

## Code Conventions

- snake_case, type hints on all signatures, `Final` for constants
- Imports sorted by ruff (stdlib → third-party → local)
- Frozen Pydantic `BaseModel` for immutable data; minimal logic in templates
- API tests use `httpx.AsyncClient` with `ASGITransport`
