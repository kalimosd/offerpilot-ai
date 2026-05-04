# OfferPilot AI

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

OfferPilot is a local-first AI career agent for resume rewriting, JD evaluation, job discovery, and application tracking.

It is designed around one rule: use the candidate's real experience. No invented projects, no fake metrics, no made-up contact details.

[中文说明](./README_zh.md)

![OfferPilot Web UI](docs/web-ui-screenshot.png)

## What This Project Is

OfferPilot has three entry points:

- **Agent CLI**: the main interface. Ask in natural language and the LangGraph agent routes the task.
- **Web UI**: a local chat, tracker, and outputs dashboard.
- **Skill Pack**: portable workflow documents and helper scripts for Cursor, Claude Code, Codex, and similar coding agents.

The agent now uses explicit intent routing:

- General career tasks go through the normal ReAct tool loop.
- Pipeline requests run a deterministic scan, rank, and report workflow.
- Batch evaluation requests load local JD files and score them with a low-temperature LLM call.

## What You Can Do

- Improve a general-purpose resume without fabricating experience.
- Rewrite a resume for a specific JD.
- Analyze JD fit and identify gaps.
- Batch-evaluate multiple JDs in `jds/`.
- Scan job portals and generate ranked recommendations.
- Track applications from `discovered` to `applied`, `interviewing`, `offer`, `rejected`, or `ghosted`.
- Generate cover letters, LinkedIn outreach messages, mock interview prep, and product research notes.
- Export Markdown outputs to styled PDFs.

## Requirements

- Python 3.10+
- Node.js 18+ if you want to run the Web UI
- An LLM API key, such as DeepSeek, Anthropic, Google, or OpenAI
- Optional but recommended: Playwright Chromium for PDF rendering and browser-based scraping

## Installation

```bash
git clone https://github.com/kalimosd/offerpilot-ai.git
cd offerpilot-ai

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
python -m playwright install chromium
```

If you only want to run the agent without tests, `pip install -e .` is enough. The `dev` extra installs `pytest`.

## LLM Configuration

Create a local `.env` file in the repository root. This file should not be committed.

```bash
touch .env
```

Use one of the following configurations.

### DeepSeek

```bash
OFFERPILOT_MODEL=deepseek-chat
OFFERPILOT_API_KEY=your-deepseek-key
OFFERPILOT_BASE_URL=https://api.deepseek.com
```

### Claude

```bash
OFFERPILOT_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=your-anthropic-key
```

### Gemini

```bash
OFFERPILOT_MODEL=gemini-2.0-flash
GOOGLE_API_KEY=your-google-key
```

### OpenAI

```bash
OFFERPILOT_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-key
```

Optional temperature override:

```bash
OFFERPILOT_TEMPERATURE=0.3
```

OfferPilot also has task defaults in code: `0.3` for general agent work, `0.1` for precise evaluation, and `0.7` for creative writing.

## Prepare Your Data

Create a personal profile store:

```bash
cp skill-pack/templates/profile_store.yaml profile_store.yaml
```

Edit `profile_store.yaml` with your real background:

- `meta`: name, email, phone, update date
- `experience`: work history and bullets
- `projects`: personal, open-source, school, or side projects
- `skills`: skills with evidence
- `education`, `certifications`, `achievements`

Put job descriptions under `jds/`:

```bash
mkdir -p jds outputs/resumes outputs/pipeline outputs/interview outputs/research outputs/misc
```

Example:

```text
jds/
  anthropic-ai-agent-engineer.md
  meituan-algorithm-engineer.md
```

Private local files such as `profile_store.yaml`, `jds/`, `outputs/`, and `data/` are intended to stay out of git.

## Run The Agent

Single-shot mode:

```bash
python -m offerpilot.agent "analyze the fit between jds/anthropic-ai-agent-engineer.md and profile_store.yaml"
python -m offerpilot.agent "batch evaluate all JDs in jds/"
python -m offerpilot.agent "run pipeline, scan last 7 days, recommend top 10"
python -m offerpilot.agent "check which applications need follow-up"
```

Interactive mode:

```bash
python -m offerpilot.agent
```

Then type requests such as:

```text
optimize my resume using profile_store.yaml
rewrite my resume for jds/anthropic-ai-agent-engineer.md
export the latest resume to PDF
exit
```

You can also use the installed console script:

```bash
offerpilot-agent "batch evaluate all JDs in jds/"
```

## Web UI

The Web UI has a FastAPI backend and a Next.js frontend.

Install backend and frontend dependencies:

```bash
source .venv/bin/activate
pip install -r web/api/requirements.txt

cd web/frontend
npm install
cd ../..
```

Start both services:

```bash
./start.sh
```

Open:

```text
http://localhost:3000
```

Manual startup:

```bash
# Terminal 1
source .venv/bin/activate
uvicorn web.api.main:app --port 8000

# Terminal 2
cd web/frontend
npm run dev -- --port 3000
```

## Skill Pack Mode

Use `skill-pack/` when you want a portable workflow for an AI coding agent rather than the built-in OfferPilot agent.

Recommended reading order:

1. `skill-pack/WORKFLOW.md`
2. `skill-pack/INPUTS.md`
3. `skill-pack/JD_MATCHING.md` for China-first JD matching
4. `skill-pack/PROMPTS.md`
5. `skill-pack/OUTPUTS.md`
6. `skill-pack/scripts/README.md` when local helpers are needed
7. `skill-pack/adapters/` for Cursor, Claude Code, or Codex wrappers

Useful helper scripts:

```bash
python skill-pack/scripts/validate_inputs.py profile_store.yaml jds/example.md
python skill-pack/scripts/extract_text.py resume.pdf
python skill-pack/scripts/render_pdf.py outputs/resumes/resume.md outputs/resumes/resume.pdf
python skill-pack/scripts/validate_outputs.py outputs/resumes/resume.md
```

The Agent CLI exposes `validate_inputs` and `validate_outputs` as tools, so validation can also happen inside agent workflows.

## Pipeline Workflow

The pipeline is for job discovery and recommendation:

1. Scan configured job portals.
2. Load recent entries from `data/scan-history.tsv`.
3. Score jobs using portal config, profile tags, and bilingual skill aliases.
4. Deduplicate and rank candidates.
5. Write a Markdown report to `outputs/pipeline/pipeline_recommendations.md`.

Example:

```bash
python -m offerpilot.agent "run pipeline, scan last 14 days, recommend top 20 domestic jobs"
```

## Development

Run tests:

```bash
source .venv/bin/activate
python -m pytest
```

Quick graph compile smoke test:

```bash
python - <<'PY'
from unittest.mock import Mock, patch
from offerpilot.graph import build_graph

with patch("offerpilot.graph.get_llm") as get_llm:
    llm = Mock()
    llm.bind_tools.return_value.invoke.return_value = "ok"
    get_llm.return_value = llm
    print(type(build_graph()).__name__)
PY
```

Expected output:

```text
CompiledStateGraph
```

## Project Structure

```text
.
├── offerpilot/
│   ├── agent.py            # CLI entry
│   ├── graph.py            # LangGraph routing and workflows
│   ├── intent.py           # Intent classification
│   ├── llm.py              # Multi-provider LLM initialization
│   ├── script_loader.py    # Legacy script module loader
│   ├── state.py            # Graph state
│   └── tools.py            # Agent tools
├── skill-pack/             # Portable workflow docs, adapters, scripts, data
├── web/
│   ├── api/                # FastAPI backend
│   └── frontend/           # Next.js frontend
├── tests/                  # Unit and integration tests
├── outputs/                # Generated local outputs
├── jds/                    # Local job descriptions
├── data/                   # Tracker and scan history
└── profile_store.yaml      # Local personal profile store
```

## License

MIT
