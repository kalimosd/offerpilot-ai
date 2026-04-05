---
name: offerpilot-cursor-adapter
description: Use the OfferPilot skill pack for resume optimization, China-first JD fit diagnosis, job-targeted resume rewrites, and cover letters in Cursor or other repository-local coding agents. Use when the user asks to improve resumes, analyze fit to a job description, tailor resumes to a job description, or create cover letters from local files.
---

# Cursor Adapter

This adapter is a thin wrapper over the platform-agnostic OfferPilot skill pack.

## Read Order

1. `../../README.md`
2. `../../WORKFLOW.md`
3. if the task is China-first JD matching, read `../../JD_MATCHING.md`
4. `../../INPUTS.md`
5. `../../PROMPTS.md`
6. `../../OUTPUTS.md`

## When To Use

- resume optimization
- China-first JD fit diagnosis
- targeted resume rewriting
- cover letter generation
- multilingual application material cleanup

## Cursor-Specific Notes

- prefer local repository files as inputs
- treat generated drafts as drafts, not as the source of truth
- if a source file is `.pdf` or `.docx` and native reading is unreliable, run `python3 skill-pack/scripts/extract_text.py "path/to/file"` before drafting
- use `python3 skill-pack/scripts/validate_inputs.py ...` and `python3 skill-pack/scripts/validate_outputs.py ...` as optional validation checks
