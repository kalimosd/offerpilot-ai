# OfferPilot AI

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

This is the **OfferPilot Skill Pack branch**.

The primary entry point is `skill-pack/`. This branch provides portable career workflow documents, rules, templates, data files, and local helper scripts for AI coding agents such as Cursor, Claude Code, and Codex.

If you want the runnable LangGraph Agent, CLI, or Web UI, use the `offerpilot-agent` branch instead.

[中文](./README.md)

## Who This Branch Is For

Use this branch when you want an AI coding agent to follow structured workflows for:

- resume diagnosis and optimization
- targeted resume rewrites for a specific JD
- JD fit analysis and 10-dimension structured evaluation
- cover letters and LinkedIn outreach
- mock interview preparation
- product research before interviews
- local text extraction, PDF rendering, and input/output validation

## How To Start

1. Open `skill-pack/README.md`
2. Follow the Start Order
3. Read the workflow document for your task:
   - `JD_MATCHING.md`
   - `EVALUATION.md`
   - `MOCK_INTERVIEW.md`
   - `PRODUCT_RESEARCH.md`
   - `TRACKER.md`
   - `OUTREACH.md`
4. Check `skill-pack/scripts/README.md` when local scripts are needed
5. Check `skill-pack/adapters/` if your AI agent supports repo-local skill wrappers

## What Is Included

```text
skill-pack/
├── README.md              # Skill Pack entry point
├── WORKFLOW.md            # General workflow
├── INPUTS.md              # Input selection and privacy rules
├── OUTPUTS.md             # Output formats and quality checks
├── PROMPTS.md             # Reusable prompt constraints
├── DATASTORE.md           # profile_store.yaml schema
├── JD_MATCHING.md         # JD fit analysis
├── EVALUATION.md          # 10-dimension structured evaluation
├── MOCK_INTERVIEW.md      # Mock interview workflow
├── PRODUCT_RESEARCH.md    # Product research workflow
├── TRACKER.md             # Application tracking
├── OUTREACH.md            # LinkedIn outreach
├── templates/             # Local templates
├── data/                  # Skill aliases and supporting data
├── examples/              # Examples
├── scripts/               # Local helper scripts
└── adapters/              # Cursor / Claude Code / Codex wrappers
```

## Local Helper Scripts

These scripts are optional helpers. They do not require the runnable Agent.

```bash
python skill-pack/scripts/validate_inputs.py profile_store.yaml jds/example.md
python skill-pack/scripts/extract_text.py resume.pdf
python skill-pack/scripts/render_pdf.py outputs/resumes/resume.md outputs/resumes/resume.pdf
python skill-pack/scripts/validate_outputs.py outputs/resumes/resume.md
```

## Relationship To The Agent Branch

OfferPilot ships in two forms:

- `offerpilot-skill`: workflow layer / portable skill pack
- `offerpilot-agent`: runnable Agent / CLI / Web UI

Think of `offerpilot-skill` as the method and rule layer. The `offerpilot-agent` branch consumes that layer and adds runtime automation.

This branch may still contain some historical runtime files, but they are not the primary entry point.

## License

MIT
