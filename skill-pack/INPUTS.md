# Inputs

## Supported Source Types

- `.txt`
- `.md`
- `.pdf`
- `.docx`

Legacy `.doc` is not supported.

## Agent File-Reading Rule

- If the agent can read `.txt` or `.md` directly, use the file content as-is
- If the agent cannot reliably read `.pdf` or `.docx`, run `python3 skill-pack/scripts/extract_text.py "path/to/file"`
- After extraction, treat the extracted text as the working copy for the rest of the workflow

## Input Priority

Use inputs in this order:

1. original source resume from the user
2. original source job description
3. previously generated drafts only as supporting reference

## Source Selection Rules

- Never assume the newest generated resume is the best source of truth
- If the user reports an older generated version is wrong, stop using it as input
- If both PDF and Markdown versions of the same original resume exist, prefer the cleaner text source when content fidelity is preserved

## Sensitive Input Rules

- treat source resumes as private by default
- do not commit private resumes to git unless the user explicitly asks
- if a private file was accidentally committed, explain the difference between deleting the latest file and rewriting history

## Targeting Inputs

For job-targeted resumes and cover letters, capture:

- job title
- company name if known
- job description text
- target language
- any user-specified emphasis

## Name Inputs

If the candidate name appears in Chinese and English output is requested:

- use the user's preferred romanization if provided
- otherwise default to pinyin with `Given Name + Family Name`
- do not invent a westernized first name
