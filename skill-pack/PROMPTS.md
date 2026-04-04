# Prompts

Use these prompt rules regardless of the AI platform.

## Shared Constraints

- preserve the candidate's real experience and intent
- do not invent fake jobs, fake metrics, or fake credentials
- improve clarity, structure, and credibility
- keep outputs concise and usable for applications
- avoid commentary such as `Improved Version`

## Resume Optimization Prompt Shape

Use a prompt that asks the model to:

- rewrite the resume for job applications
- improve bullet quality
- preserve facts
- remove filler
- keep the output clean and sectioned

## Targeted Resume Prompt Shape

Use a prompt that asks the model to:

- tailor the resume toward the provided job description
- surface matching skills and responsibilities
- emphasize the most relevant experience first
- stay truthful to the source

## Cover Letter Prompt Shape

Use a prompt that asks the model to:

- connect the resume to the job description
- explain relevant fit using real experiences
- keep the letter concise
- avoid generic enthusiasm without evidence

## Name Handling Prompt Rules

For English outputs:

- preserve the candidate name accurately
- if the source name is Chinese, use pinyin unless the user gave a preferred spelling
- format the English name as `Given Name + Family Name`
- do not create a western nickname

## Suggested Validation Questions

After generation, ask:

- does every bullet map back to a real source fact?
- is the name correct?
- did the output keep the requested language?
- did the model overstate impact beyond the source?
