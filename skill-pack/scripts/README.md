# Scripts

These scripts are optional helpers for the OfferPilot skill pack.

They support the workflow, but they are not the source of truth. The source of truth still lives in the documents under `skill-pack/`.

## Included Scripts

### `extract_text.py`

Use when the source resume or JD is a `.pdf` or `.docx` file and the agent cannot read it reliably.

Example:

```bash
python3 skill-pack/scripts/extract_text.py "resume.pdf" --output "resume.txt"
```

### `render_pdf.py`

Use when the workflow already produced a reviewed Markdown-like deliverable and you want a local PDF export.

Example:

```bash
python3 skill-pack/scripts/render_pdf.py "resume.md" "resume.pdf" --document-type resume --style classic
```

### `validate_inputs.py`

Use for a quick sanity check before running a workflow, especially when there is a risk that the chosen file is already a generated artifact instead of the original source.

Example:

```bash
python3 skill-pack/scripts/validate_inputs.py "resume.md" "job.md"
```

### `validate_outputs.py`

Use for lightweight output checks after generation, such as filename plausibility or optional English name formatting checks.

Example:

```bash
python3 skill-pack/scripts/validate_outputs.py "targeted_resume.md" --english-name "GivenName FamilyName"
```

## Usage Rules

- Prefer direct file reading when the agent can handle the source natively
- Use these scripts only when they add reliability or convenience
- Review Markdown-like output before exporting to PDF
- Keep new helper logic in `skill-pack/scripts/` rather than introducing a parallel product layer
