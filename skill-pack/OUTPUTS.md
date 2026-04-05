# Outputs

## Output Categories

OfferPilot supports three main output types:

- resume diagnosis
- optimized resume
- job-targeted resume
- jd-fit diagnosis
- cover letter

## Resume Diagnosis Expectations

- identifies strengths that are already supported by the source
- identifies gaps relative to either general job-readiness or a target job
- calls out risks without inventing problems
- suggests the highest-value rewrite priorities before generation

## JD-Fit Diagnosis Expectations

- explains how well the resume matches the target JD
- separates matched, partial, and missing signals
- prioritizes practical rewrite actions over abstract commentary
- uses a score only as supporting context, not as the sole conclusion
- avoids `ATS score` framing for China-first outputs unless explicitly requested

## Language Options

- `same`: keep the source language unless the source is mixed and the user asked for cleanup
- `zh`: produce professional Simplified Chinese
- `en`: produce polished English for job applications

## Resume Output Expectations

- clear sectioning
- concise bullet points
- stronger action-oriented phrasing
- no fabricated facts
- no inflated metrics
- compact, interview-ready tone

## Targeted Resume Expectations

- emphasizes experience relevant to the target role
- incorporates job-description language naturally
- reorders emphasis without changing the underlying facts

## Cover Letter Expectations

- reflects the job description
- stays grounded in the candidate's real background
- avoids generic filler
- keeps the tone professional and direct

## English Name Check

When the source resume is Chinese and the output is English:

- verify the English name order
- default to `Given Name + Family Name`
- keep the user-provided spelling if one exists

Example:

- `中文名` -> `<Given Name> <Family Name>`

## Final Review Checklist

- [ ] name is correct
- [ ] dates are correct
- [ ] titles and employer names are correct
- [ ] content matches the intended task
- [ ] language matches the request
- [ ] fit conclusions are supported by resume and JD evidence
- [ ] rewrite suggestions are concrete and truthful
- [ ] nothing confidential is accidentally included in publishable artifacts
