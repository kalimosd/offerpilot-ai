# Migration to Skill-First

## Why This Repository Changed

OfferPilot started as a CLI-first project for resume optimization and cover letters.

The repository is moving toward a skill-first structure so that:

- people can download and reuse the workflow without depending on one local CLI
- the core value lives in prompts, rules, and workflows rather than a single runtime
- multiple repository-based AI agents can use the same skill pack

## New Primary Surface

The primary product surface is now:

- `skill-pack/README.md`
- `skill-pack/WORKFLOW.md`
- `skill-pack/INPUTS.md`
- `skill-pack/OUTPUTS.md`
- `skill-pack/PROMPTS.md`
- `skill-pack/adapters/`

## Current Role of the Python Code

The code under `offerpilot/` still exists, but it should be treated as a legacy compatibility layer rather than the center of the project.

Relevant legacy files:

- `offerpilot/cli.py`
- `offerpilot/resume.py`
- `offerpilot/cover.py`
- `offerpilot/export.py`
- `pyproject.toml`

The current PDF export path in `offerpilot/export.py` now prefers HTML/CSS rendered through Playwright + Chromium, with a temporary ReportLab fallback kept for compatibility while the browser-based path stabilizes.

## Current Role of Tests

The current tests under `tests/` mostly validate the legacy Python implementation. They may still be useful while the compatibility layer remains, but they are no longer the main expression of repository value.

## Planned Cleanup Path

Short term:

- keep the legacy CLI runnable
- keep tests for the legacy layer
- move new documentation and platform guidance into `skill-pack/`
- document that browser-based PDF export requires `playwright install chromium`

Later:

- decide whether to archive or remove `offerpilot/`
- decide whether to keep `pyproject.toml` only for helper scripts or remove packaging entirely
- decide whether `tests/` should focus on script validation rather than CLI behavior

## Publishing Guidance

If this repository is later split into a standalone product, `skill-pack/` should become the main distributable artifact and the adapter directories should remain thin wrappers over the shared workflow docs.
