# JD-Fit Diagnosis Example

## Task

Analyze how well a resume matches a target job description for a China-first hiring context.

## Inputs

- original resume
- target job description
- target language, usually `zh`

## Workflow

1. extract the JD's core requirements
2. find direct evidence in the resume
3. label each requirement as matched, partially matched, or missing
4. explain the biggest fit gaps in practical hiring language
5. provide concrete rewrite suggestions and sample phrasing

## Expected Output

- a clear `岗位匹配结论`
- a supporting `综合匹配度`
- matched and missing requirements
- relevance analysis tied to actual experience
- concrete rewrite priorities in Simplified Chinese
