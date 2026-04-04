def build_cover_letter_prompt(
    resume_text: str,
    job_text: str,
    target_language: str = "same",
) -> str:
    language_instruction = _build_language_instruction(target_language)

    return f"""
You are an expert career writing assistant for international students and entry-level job seekers.

Write a tailored cover letter based on the resume and job description below.

Requirements:
- Keep the tone professional, confident, and concise
- Make the letter specific to the job description
- Highlight relevant experience and transferable strengths from the resume
- Do not invent fake experience, fake metrics, or fake technologies
- Keep the letter sharp and submission-ready
- Avoid generic AI-sounding phrases and unnecessary fluff
- Use clear business English for a non-native speaker audience
- Show clear alignment between the candidate's background and the role
- Avoid repeating the same idea across paragraphs

Language:
- {language_instruction}

Output format:
- 3 to 5 short paragraphs
- No bullet points
- No explanation before or after the letter
- Start with "Dear Hiring Manager,"
- End with a professional closing
- Keep the total length around 220 to 320 words
- Do not use placeholders like [Company Name]

Resume:
{resume_text}

Job Description:
{job_text}
""".strip()


def _build_language_instruction(target_language: str) -> str:
    if target_language == "en":
        return "Write the entire cover letter in polished professional English."

    if target_language == "zh":
        return "Write the entire cover letter in concise professional Simplified Chinese."

    return "Keep the cover letter in the same language as the source materials."
