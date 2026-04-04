import unittest

from offerpilot.resume import build_resume_optimization_prompt


class ResumePromptTests(unittest.TestCase):
    def test_english_prompt_mentions_english_output(self) -> None:
        prompt = build_resume_optimization_prompt("sample", target_language="en")

        self.assertIn("polished English", prompt)
        self.assertIn("Given Name + Family Name order", prompt)

    def test_prompt_requires_preserving_name_accuracy(self) -> None:
        prompt = build_resume_optimization_prompt("sample", target_language="en")

        self.assertIn("Preserve the candidate's legal name exactly", prompt)
        self.assertIn("transliterate to pinyin", prompt)
        self.assertIn("first character as the family name", prompt)
        self.assertIn("surname usually comes first in Chinese but should appear last in English", prompt)

    def test_same_language_prompt_mentions_source_language(self) -> None:
        prompt = build_resume_optimization_prompt("sample", target_language="same")

        self.assertIn("same language as the source content", prompt)

    def test_ats_prompt_mentions_ats_friendly_style(self) -> None:
        prompt = build_resume_optimization_prompt("sample", style="ats")

        self.assertIn("ATS-friendly formatting", prompt)

    def test_job_targeting_prompt_mentions_job_alignment(self) -> None:
        prompt = build_resume_optimization_prompt(
            "sample",
            job_text="Need Android development and performance optimization experience.",
        )

        self.assertIn("Tailor the resume toward the provided job description", prompt)
        self.assertIn("Target Job Description:", prompt)

    def test_job_targeting_prompt_mentions_job_alignment(self) -> None:
        prompt = build_resume_optimization_prompt(
            "sample",
            job_text="Need Android development and performance optimization experience.",
        )

        self.assertIn("Tailor the resume toward the provided job description", prompt)
        self.assertIn("Target Job Description:", prompt)


if __name__ == "__main__":
    unittest.main()
