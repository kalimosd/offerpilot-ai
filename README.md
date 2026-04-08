# OfferPilot AI

AI job assistant that turns weak applications into interview-ready ones.

Built fast as a practical AI product experiment, OfferPilot tackles a real problem: strong candidates often undersell themselves with generic resumes, weak positioning, and cover letters that sound the same. It helps turn raw experience into sharper, role-specific application materials that are more likely to earn interviews.

## Quick Example

Use OfferPilot as a repository-local skill pack:

1. Prepare `resume.md` or `resume.pdf`
2. Prepare `job.md` for the target role
3. Open `skill-pack/README.md`
4. Run the workflow through Cursor, a Codex-style agent, or Claude Code
5. Generate a stronger resume, tailored rewrite, JD-fit analysis, or cover letter

Typical flow:

1. Start with a base resume and an optional job description.
2. Let the agent follow the `skill-pack` workflow and prompt rules.
3. Review the generated Markdown output.
4. Export it when the content is ready.

## Example Output

**Before**

```text
- Responsible for Android development and worked with different teams.
- Helped fix bugs and improve app performance.
```

**After**

```text
- Improved Android system stability and performance by diagnosing rendering, memory, and ANR issues with Perfetto and Systrace, then driving fixes across platform teams.
- Owned delivery for recent-tasks features, coordinating engineering stakeholders to ship on schedule and close cross-team issues faster.
```

These outputs are meant to be directly usable with minimal editing.

## Why This Project

Many international students and early-career candidates do strong work but present it weakly.

Their resumes are often too generic, their cover letters feel interchangeable, and their most relevant experience gets buried. OfferPilot focuses on outcomes: clearer positioning, stronger materials, and better odds of getting interviews.

## Features

- **Resume optimization**: Tightens wording, removes filler, and strengthens bullet points without inventing facts.
- **Job-targeted rewriting**: Rewrites and reorders content around a specific job description.
- **Cover letter generation**: Produces concise, tailored letters grounded in real experience.
- **Profile datastore support**: Pulls the most relevant experience from a structured data source.
- **JD fit analysis**: Identifies match signals, gaps, and rewrite priorities.
- **Job discovery**: Scans career portals and search engines to find relevant openings automatically.
- **Local workflow tooling**: Supports text extraction, validation, PDF export with photo embedding, and portal scanning.

## Tech Stack

- Python
- LLM-powered rewriting and analysis
- Modular skill-pack architecture
- YAML-based profile datastore
- Playwright-based PDF export and portal scanning

## Project Structure

- **main**: The `skill-pack/` directory, which contains the core workflow for resume optimization, targeted rewriting, JD-fit analysis, cover letters, examples, adapters, and scripts.
- **profile-datastore**: The structured experience store in `profile_store.yaml`, used to generate more targeted and higher-quality outputs from a richer source of truth.

```text
.
├── README.md
├── profile_store.yaml
├── portals_cn.yml
├── skill-pack/
│   ├── README.md
│   ├── WORKFLOW.md
│   ├── DATASTORE.md
│   ├── JD_MATCHING.md
│   ├── INPUTS.md
│   ├── OUTPUTS.md
│   ├── PROMPTS.md
│   ├── adapters/
│   │   ├── claude-code/
│   │   ├── codex/
│   │   └── cursor/
│   ├── examples/
│   │   ├── resume-optimization.md
│   │   ├── targeted-resume.md
│   │   ├── cover-letter.md
│   │   └── profile_store_example.yaml
│   ├── data/
│   │   └── skill_aliases.zh-en.json
│   └── scripts/
│       ├── extract_text.py
│       ├── render_pdf.py
│       ├── scan_portals.py
│       ├── validate_inputs.py
│       └── validate_outputs.py
├── jds/                  # (gitignored) saved JDs from scans
├── data/                 # (gitignored) scan history and pipeline
└── tests/
    └── test_export.py
```

## Advanced Usage

Extract text from PDF or DOCX when the agent cannot read the source reliably:

```bash
python3 skill-pack/scripts/extract_text.py "resume.pdf" --output "resume.txt"
```

Export a reviewed draft to PDF:

```bash
python3 skill-pack/scripts/render_pdf.py "resume.md" "resume.pdf" --document-type resume --style classic
```

Export with a photo embedded in the header:

```bash
python3 skill-pack/scripts/render_pdf.py "resume.md" "resume.pdf" --style standard_cn --photo "photo.jpg"
```

Scan career portals for matching job listings:

```bash
# Full scan (CN APIs + Greenhouse + web search)
python3 skill-pack/scripts/scan_portals.py

# Only Chinese company APIs (Meituan, Kuaishou, Didi)
python3 skill-pack/scripts/scan_portals.py --cn-only

# Only Greenhouse API (international companies)
python3 skill-pack/scripts/scan_portals.py --greenhouse-only

# Only web search (DuckDuckGo, covers 20+ companies)
python3 skill-pack/scripts/scan_portals.py --search-only

# Preview without writing files
python3 skill-pack/scripts/scan_portals.py --dry-run
```

Matched jobs are saved to `jds/` with full JD content and application links. Scan history is tracked in `data/scan-history.tsv` for deduplication.

## Roadmap

- RAG-based job search and resume knowledge system
- Interview simulation and feedback
- Better datastore retrieval and ranking
- Agent-driven application workflows
- Resume versioning and targeting automation

## Contributing / Feedback

Feedback, issues, and pull requests are welcome.

If you want to improve the workflow, test the output quality, or suggest product directions, open an issue or start a discussion.
