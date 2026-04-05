---
name: offerpilot-claude-code-adapter
description: Use the OfferPilot skill pack for resume optimization, China-first JD fit diagnosis, targeted resumes, and cover letters in Claude Code style repository agents. Use when the user wants structured job-application outputs or JD fit analysis from local resume and job-description files.
---

# Claude Code Adapter

This adapter provides the minimum platform-specific bridge to the shared OfferPilot workflow.

## Read Order

1. `../../README.md`
2. `../../WORKFLOW.md`
3. if the task is China-first JD matching, read `../../JD_MATCHING.md`
4. `../../INPUTS.md`
5. `../../PROMPTS.md`
6. `../../OUTPUTS.md`

## Agent Behavior

- start from the original resume source
- keep outputs compact and factual
- ask for missing job descriptions only when task type requires them
- if a `.pdf` or `.docx` source cannot be read reliably, run `python3 skill-pack/scripts/extract_text.py "path/to/file"` first
- use validation scripts only when the extra check adds value
