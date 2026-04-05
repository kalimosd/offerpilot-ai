# Skill-First Repository Notes

## Status

OfferPilot has completed its shift from a CLI-first repository to a skill-first repository.

The repository no longer exposes a product-level CLI entry point. The recommended and supported way to use OfferPilot is through `skill-pack/` and its agent adapters.

## Primary Surface

The main product surface is now:

- `skill-pack/README.md`
- `skill-pack/WORKFLOW.md`
- `skill-pack/JD_MATCHING.md`
- `skill-pack/INPUTS.md`
- `skill-pack/OUTPUTS.md`
- `skill-pack/PROMPTS.md`
- `skill-pack/examples/`
- `skill-pack/adapters/`
- `skill-pack/scripts/`

## Role of the Python Code

The legacy `offerpilot/` package has now been removed.

Helper implementation now lives under `skill-pack/scripts/` when it is still useful to the workflow, such as:

- text extraction
- PDF rendering
- lightweight validation

New product capabilities should land in `skill-pack/` first and should follow the shared workflow documents rather than introducing a parallel Python product layer.

## Packaging Guidance

`pyproject.toml` remains in the repository for Python dependency management and local module organization.

It should not be treated as a sign that OfferPilot is still a CLI product.

## Test Guidance

The current tests under `tests/` validate helper scripts that still matter to the workflow.

They are useful as implementation checks, but they are not the primary expression of OfferPilot's value. The primary value lives in the shared workflow docs, prompts, examples, and adapters inside `skill-pack/`.

## Publishing Guidance

If this repository is later split into a standalone distributable artifact, `skill-pack/` should remain the main package and the adapter directories should stay thin wrappers over the shared workflow docs.
