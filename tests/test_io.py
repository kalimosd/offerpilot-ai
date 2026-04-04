import tempfile
import unittest
from pathlib import Path

from offerpilot.io import load_text_from_file, save_text_to_file


class IoTests(unittest.TestCase):
    def test_load_text_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "resume.txt"
            file_path.write_text("hello world\n", encoding="utf-8")

            result = load_text_from_file(str(file_path))

            self.assertEqual(result, "hello world")

    def test_save_text_to_file_creates_parents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "nested" / "output.md"

            saved_path = save_text_to_file(str(file_path), "content")

            self.assertEqual(saved_path.read_text(encoding="utf-8"), "content")

    def test_unsupported_doc_extension(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "resume.doc"
            file_path.write_text("binary-ish", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_text_from_file(str(file_path))


if __name__ == "__main__":
    unittest.main()
