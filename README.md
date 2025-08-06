
# OpenBot 2.0 🤖  
**Your AI gateway inside Telegram, powered by OpenRouter**

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=flat-square)](#prerequisites)
[![Version](https://img.shields.io/badge/version-2.0-blue.svg?style=flat-square)](#changelog)

---

## Table of Contents
1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Architecture](#architecture)  
4. [Prerequisites](#prerequisites)  
5. [Installation](#installation)  
6. [Configuration](#configuration)  
7. [Usage](#usage)  
8. [Command Reference](#command-reference)  
9. [Deployment Options](#deployment-options)  
10. [Troubleshooting](#troubleshooting)  
11. [Roadmap](#roadmap)  
12. [Contributing](#contributing)  
13. [Security](#security)  
14. [License](#license)  
15. [Changelog](#changelog)  

---

## Overview
**OpenBot 2.0** bridges 🌉 **Telegram** and the **75+ AI models** available on [OpenRouter](https://openrouter.ai/).  
Whether you need code review, brainstorming, translations, or simply an always‑on knowledge companion, OpenBot delivers an extensible, secure, _chat‑native_ experience.

---

## Key Features

| Category | Highlights |
| :-- | :-- |
| 🔑 **Secure Authentication** | One‑time API‑key handshake with OpenRouter; encrypted storage (AES‑256) on disk |
| 🤖 **Multi‑Model Chat** | Live switch between 75+ models (GPT‑4o, Claude 3, Command R+, etc.) |
| 🎨 **Rich Formatting** | Markdown → Telegram support: code blocks, inline images, LaTeX |
| 🧠 **Context Caching** | Per‑user conversation history with configurable token limits |
| 📊 **Activity Logging** | JSONL logs for analytics & audit; GDPR‑ready retention controls |
| 🔄 **Async Runtime** | Built with **aiohttp** & **python‑telegram‑bot v21** for maximal throughput |
| 📈 **Rate Limiting** | Prevents abuse via per‑user & global quotas |
| 🛠 **Plugin System** | Drop‑in Python modules add slash‑commands without touching core |
| 🐳 **Docker‑first** | Single‑command production deploy via Docker or Docker Compose |
| 🌍 **i18n** | UI messages in **English** & **Русский** (more coming) |

---

## Architecture

```
Telegram Client  ─┐
                  │        +---------------------+
User ↔ Bot API ↔  │  HTTP  |  OpenRouter Gateway |
                  │◀──────►| (75+ AI models)     |
                  │        +---------------------+
                  │
                  │        +---------------------+
                  └───────►|  OpenBot Core       |
                           |  • Command Router   |
                           |  • Model Manager    |
                           |  • Context Cache    |
                           |  • Plugin Loader    |
                           +---------------------+
```

- **OpenBot Core** orchestrates incoming Telegram updates, maps them to command handlers, and forwards prompts to the selected AI model.  
- **Plugin Loader** autoloads any Python script placed in `plugins/`, enabling rapid feature development (e.g., `/weather`, `/pdf`).  
- **Context Cache** uses an LRU strategy to keep conversations relevant while respecting token budgets.

---

## Prerequisites
| Requirement | Notes |
| :-- | :-- |
| **Python 3.9 – 3.12** | Async features rely on modern  `asyncio` & `typing`. |
| **Telegram Bot Token** | Create via [@BotFather](https://t.me/BotFather). |
| **OpenRouter API Key** | Sign up at <https://openrouter.ai/> → **API Keys**. |
| (Optional) **Docker ≥ 24.0** | For containerised deployment. |

---

## Installation

```bash
# 1 – Clone the repo
git clone https://github.com/rokoss21/OpenBot-2.0.git
cd OpenBot-2.0

# 2 – Create virtual env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3 – Install deps
pip install -r requirements.txt
```

---

## Configuration

All runtime settings live in **`config.py`** (or environment variables in Docker).

```python
TELEGRAM_TOKEN   = "YOUR_TELEGRAM_BOT_TOKEN"
OPENROUTER_KEY   = "YOUR_OPENROUTER_API_KEY"
DEFAULT_MODEL    = "openai/gpt-4o-mini"
MAX_HISTORY_TOKENS = 3000

# Optional
ADMIN_IDS        = [123456789]          # Telegram IDs with `/stats` etc.
RATE_LIMIT_PER_MIN = 20                 # messages
LOG_LEVEL        = "INFO"
```

> **Tip:** In production, export variables instead of hard‑coding.  
> `export TELEGRAM_TOKEN=... && python main.py`

---

## Usage

```bash
python main.py          # Local run
```

The bot responds to slash‑commands and plain messages.  
Example session:

```
User  ➜  /model anthropic/claude-3-opus
Bot   ➜  ✅ Switched to Claude 3 Opus.

User  ➜  Rewrite this paragraph with more humour.
Bot   ➜  (AI response…)
```

---

## Command Reference

| Command | Description |
| :-- | :-- |
| `/start` | Onboard user & show quick tips |
| `/api <key>` | Register or update personal OpenRouter API key |
| `/model [model_slug]` | Choose AI model; without args lists all available |
| `/context` | Toggle context saving *on/off* |
| `/help` | Full help with examples |
| `/stats` | (Admin) Show usage metrics |
| `/plugins` | List installed plugins |

---

## Deployment Options

### 🔧 Bare Metal / Systemd

1. Copy `openbot.service` to `/etc/systemd/system/`.
2. `sudo systemctl enable --now openbot`.

### 🐳 Docker Compose

```yaml
version: "3.9"
services:
  openbot:
    image: ghcr.io/your-org/openbot:2.0
    environment:
      TELEGRAM_TOKEN: ${TELEGRAM_TOKEN}
      OPENROUTER_KEY: ${OPENROUTER_KEY}
    restart: unless-stopped
```

`docker compose up -d` and you’re live.

---

## Troubleshooting

| Symptom | Fix |
| :-- | :-- |
| **Bot doesn’t start** | Verify `TELEGRAM_TOKEN` & `OPENROUTER_KEY` env vars. |
| **403 Forbidden** | Bot not added to group / token revoked. |
| **Slow responses** | Check rate limits, OpenRouter status, or switch model. |
| **High RAM usage** | Reduce `MAX_HISTORY_TOKENS` or enable `/context off`. |

> See `logs/openbot.log` for stack traces (rotate daily).

---

## Roadmap

- [ ] **Inline Mode** (query bot without opening chat)  
- [ ] **Voice → Text** via Whisper models  
- [ ] **Web Dashboard** for analytics & moderation  
- [ ] **Pay‑as‑you‑go billing hook** (Stripe)  
- [ ] **Additional locales** (ES, DE, ZH)  

Vote or propose features in [Discussions](https://github.com/<your‑org>/openbot/discussions).

---

## Contributing

We welcome PRs, issues, and plugin ideas.

1. Fork → create feature branch  
2. Run `pre-commit install` (black, isort, flake8)  
3. Submit a **draft PR** early for feedback  
4. Ensure CI passes (`pytest -q`)  

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## Security

Please report vulnerabilities via **security@yourdomain.com**.  
We follow [responsible disclosure](https://opensource.guide/security/) and aim to patch within 72 hours.

---

## License
Released under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

## Changelog

### 2.0 — 2025‑07‑26
* **Re‑architected core** for async + plugin support  
* **Multi‑model switching** in‑chat  
* **Encrypted API‑key storage**  
* **Docker images (GHCR)**  
* Docs overhaul & CI pipeline (GitHub Actions)

---

<div align="center">
  <i>Built with ❤️ & asyncio — let your Telegram fly smarter!</i>
</div>
