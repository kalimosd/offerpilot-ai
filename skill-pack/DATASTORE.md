# Profile Datastore

## Purpose

The profile datastore is a structured personal material library. Instead of only rewriting the few bullets already on a resume, the agent can select and assemble the most relevant bullets from a larger pool based on the target JD.

## File Format

- Use YAML for human readability and easy manual editing
- Default location: project root or any path the user specifies
- Default filename: `profile_store.yaml`
- Template: `skill-pack/templates/profile_store.yaml`

## Structure Overview

```yaml
meta:           # candidate identity and contact info
experience:     # work history with tagged bullets
projects:       # standalone projects outside of work experience
skills:         # skill inventory with proficiency and evidence
education:      # degrees and schools
certifications: # professional certifications
achievements:   # awards, recognitions, notable outcomes
```

## Field Reference

### meta

| Field      | Required | Description                              |
|------------|----------|------------------------------------------|
| name       | yes      | candidate display name                   |
| name_en    | no       | English name in `Given Name Family Name` |
| email      | no       | contact email                            |
| phone      | no       | contact phone                            |
| updated    | no       | last update date                         |

### experience[].bullets[]

| Field    | Required | Description                                              |
|----------|----------|----------------------------------------------------------|
| text     | yes      | the bullet content                                       |
| tags     | yes      | list of skill/domain tags for JD matching                |
| impact   | no       | `quantified` / `qualitative` / `context-only`            |
| variants | no       | map of alternative phrasings keyed by perspective        |

### variants

Variants let you pre-write different angles of the same achievement:

```yaml
variants:
  management: "built onboarding program, cut ramp-up time by 50%"
  technical: "wrote starter kit and internal docs, reduced first-commit time"
```

The agent picks the variant that best fits the target JD. If no variant matches better than the original `text`, use `text`.

### skills[]

| Field    | Required | Description                                    |
|----------|----------|------------------------------------------------|
| name     | yes      | skill name                                     |
| level    | no       | `familiar` / `proficient` / `expert`           |
| years    | no       | years of experience                            |
| evidence | no       | list of concrete uses tied to bullets/projects  |

### impact priority

When multiple bullets match a JD requirement equally well, prefer:

1. `quantified` — has numbers, percentages, scale
2. `qualitative` — clear outcome without hard numbers
3. `context-only` — describes responsibility without outcome

## Tagging Rules

- Use lowercase tags
- Prefer tags that align with keys in `data/skill_aliases.zh-en.json`
- A bullet can have multiple tags
- Tags enable the JD matching step; bullets without tags are deprioritized during selection

## How the Agent Uses the Datastore

1. Parse the JD to extract requirements and keywords
2. Normalize keywords using `data/skill_aliases.zh-en.json`
3. Match normalized keywords against bullet tags
4. Rank matched bullets by relevance and impact level
5. If a bullet has a matching variant for the target role type, use the variant
6. Assemble top bullets into resume sections
7. Polish phrasing per `PROMPTS.md` rules

## Quick Start

### 1. Create your datastore

```bash
cp skill-pack/templates/profile_store.yaml profile_store.yaml
```

See `skill-pack/examples/profile_store_example.yaml` for a filled-in reference.

### 2. Fill in your materials

- Write as many bullets as you can for each work experience and project
- Every bullet must have `tags` — this is how the agent matches against JDs
- Mark `impact` when possible (`quantified` > `qualitative` > `context-only`)
- Add `variants` when the same achievement can be told from different angles (e.g. management vs technical)
- Link skills to concrete evidence so the agent can back up claims

You do not need to be concise here. The datastore is your full material pool, not a finished resume. The more you put in, the more the agent can select from.

### 3. Keep it out of git

```bash
echo "profile_store.yaml" >> .git/info/exclude
```

### 4. Generate a targeted resume

Tell the agent:

> 请根据 profile_store.yaml 和这个 JD，生成一份定向简历

The agent will:

1. Parse the JD to extract requirements and keywords
2. Match keywords against your bullet tags
3. Pick the most relevant bullets, ranked by impact
4. Choose the best variant for each bullet when available
5. Assemble and polish into a targeted resume

Different JDs produce different bullet selections from the same datastore.

### 5. Maintain over time

- After finishing a project or getting a result, add a bullet to the datastore
- Focus on `text` + `tags`; formatting can be rough
- The more you accumulate, the better the agent can tailor future resumes

## When the Datastore Is Not Provided

If the user does not provide a profile datastore, the workflow falls back to the existing behavior: rewrite and optimize the source resume directly. No datastore is required.

## Privacy

- The profile datastore contains personal career details; treat it as private by default
- Do not commit it to version control unless the user explicitly asks
- The template and example files use anonymous placeholder data
