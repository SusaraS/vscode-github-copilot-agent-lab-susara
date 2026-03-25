# 🎯 Soc Ops — Social Bingo

> **Break the ice, make connections, win at networking!**

Soc Ops is an interactive social bingo game built for in-person mixers, team events, and conferences. Find people who match the prompts on your card, mark them off, and race to get 5 in a row!

🎮 **[Play the Game](https://madebygps.github.io/vscode-github-copilot-agent-lab/)** • 📚 **[View Lab Guide](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/)**

---

## ✨ Features

- 🎲 **Randomized boards** — Every player gets a unique card arrangement
- 💾 **Auto-save progress** — Your card persists across page reloads
- 🏆 **Bingo detection** — Automatic win detection for rows, columns, and diagonals
- 🎉 **Celebration modal** — Confetti-worthy victory screen
- 📱 **Mobile-first** — Works great on phones at live events

---

## 🚀 Quick Start

### Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) package manager

### Run Locally

```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000
```

### Test

```bash
uv run pytest
```

### Lint

```bash
uv run ruff check .
uv run ruff format .
```

---

## 🎨 Customize Your Game

Edit `app/data.py` to swap in your own icebreaker prompts:

```python
questions_list: list[str] = [
    "has a pet",
    "speaks more than 2 languages",
    "your custom question here",
    # ... 24+ questions for a full board
]
```

---

## 📚 Lab Guide

Follow the hands-on workshop to build this app step-by-step with GitHub Copilot agents.

| Part | Title |
|------|-------|
| [**00**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=00-overview) | Overview & Checklist |
| [**01**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=01-setup) | Setup & Context Engineering |
| [**02**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=02-design) | Design-First Frontend |
| [**03**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=03-quiz-master) | Custom Quiz Master |
| [**04**](https://madebygps.github.io/vscode-github-copilot-agent-lab/docs/step.html?step=04-multi-agent) | Multi-Agent Development |

> 📝 Lab guides are also available in the [`.lab/`](.lab/) folder for offline reading.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Jinja2](https://jinja.palletsprojects.com/) |
| Frontend | [HTMX](https://htmx.org/) + Custom CSS utilities |
| State | Server-side sessions with signed-cookie persistence |
| Deployment | GitHub Pages via GitHub Actions |

---

## 📁 Project Structure

```
app/
├── templates/           # Jinja2 templates
│   ├── base.html
│   ├── home.html
│   └── components/      # bingo_board, bingo_modal, game_screen, start_screen
├── static/              # CSS & JS assets
├── models.py            # Game state & data models
├── game_logic.py        # Bingo detection & board generation
├── game_service.py      # Session management
├── data.py              # Question bank
└── main.py              # FastAPI routes
tests/
├── test_api.py          # API endpoint tests
└── test_game_logic.py   # Game logic unit tests
```

---

## 🚢 Deployment

Pushes to `main` automatically deploy to GitHub Pages:

```
https://{username}.github.io/{repo-name}
```

---

## 📝 License

[MIT](LICENSE) — use it for your next event!
