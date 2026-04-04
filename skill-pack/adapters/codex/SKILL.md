---
name: offerpilot-codex-adapter
description: Use the OfferPilot skill pack for resume optimization, job-targeted rewrites, and cover-letter workflows in Codex-style repository agents. Use when local files such as resumes or job descriptions need to be transformed into stronger application materials.
---

# Codex Adapter

This adapter points Codex-style agents to the shared OfferPilot workflow.

## Read Order

1. `../../README.md`
2. `../../WORKFLOW.md`
3. `../../INPUTS.md`
4. `../../PROMPTS.md`
5. `../../OUTPUTS.md`

## Operating Rules

- use the original resume when available
- do not invent facts or metrics
- treat private source files as sensitive
- verify English name ordering for Chinese resumes when needed
- if a `.pdf` or `.docx` source cannot be read natively, run `python3 skill-pack/scripts/extract_text.py "path/to/file"` and continue from the extracted text

## Optional Scripts

- `python3 skill-pack/scripts/extract_text.py "path/to/file"` is required when native `.pdf` or `.docx` reading is unavailable
- use files under `../../scripts/` for validation when extra checks add value
