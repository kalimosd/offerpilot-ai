---
name: offerpilot-claude-code-adapter
description: Use the OfferPilot skill pack for resume optimization, targeted resumes, and cover letters in Claude Code style repository agents. Use when the user wants structured job-application outputs from local resume and job-description files.
---

# Claude Code Adapter

This adapter provides the minimum platform-specific bridge to the shared OfferPilot workflow.

## Read Order

1. `../../README.md`
2. `../../WORKFLOW.md`
3. `../../INPUTS.md`
4. `../../PROMPTS.md`
5. `../../OUTPUTS.md`

## Agent Behavior

- start from the original resume source
- keep outputs compact and factual
- ask for missing job descriptions only when task type requires them
- if a `.pdf` or `.docx` source cannot be read reliably, run `python3 skill-pack/scripts/extract_text.py "path/to/file"` first
- use validation scripts only when the extra check adds value
