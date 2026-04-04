import unittest

from offerpilot.cover import build_cover_letter_prompt


class CoverPromptTests(unittest.TestCase):
    def test_english_cover_prompt_mentions_english_output(self) -> None:
        prompt = build_cover_letter_prompt("resume", "job", target_language="en")

        self.assertIn("polished professional English", prompt)

    def test_same_language_cover_prompt_mentions_source_materials(self) -> None:
        prompt = build_cover_letter_prompt("resume", "job", target_language="same")

        self.assertIn("same language as the source materials", prompt)


if __name__ == "__main__":
    unittest.main()
