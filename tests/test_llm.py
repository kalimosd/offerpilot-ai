import unittest

from offerpilot.llm import _normalize_text_output


class LlmTests(unittest.TestCase):
    def test_normalize_plain_text(self) -> None:
        self.assertEqual(_normalize_text_output(" hello "), "hello")

    def test_normalize_code_fence(self) -> None:
        text = "```markdown\n# Title\n\nBody\n```"
        self.assertEqual(_normalize_text_output(text), "# Title\n\nBody")


if __name__ == "__main__":
    unittest.main()
