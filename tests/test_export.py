import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

from offerpilot.export import (
    _extract_heading_text,
    _get_style_config,
    _parse_markdown_blocks,
    _render_blocks_to_html,
    _sanitize_pdf_text,
    _strip_markdown_inline,
    render_markdown_to_pdf,
)


def _write_fake_pdf(path: Path, marker: bytes = b"%PDF-1.4\n") -> None:
    path.write_bytes(marker + b"fake pdf body\n")


class ExportTests(unittest.TestCase):
    def test_extract_heading_text_supports_level_three_headings(self) -> None:
        self.assertEqual(_extract_heading_text("### **Education**"), "Education")

    def test_strip_markdown_inline_removes_emphasis_markers(self) -> None:
        text = "**Company** | *Role* | 2024-07 - Present"

        cleaned = _strip_markdown_inline(text)

        self.assertEqual(cleaned, "Company | Role | 2024-07 - Present")

    def test_sanitize_pdf_text_replaces_unsupported_unicode_punctuation(self) -> None:
        text = "content‑side data – time‑series"

        sanitized = _sanitize_pdf_text(text)

        self.assertEqual(sanitized, "content-side data - time-series")

    def test_parse_markdown_blocks_captures_resume_structure(self) -> None:
        markdown = "# Candidate Example\nPhone: 123\n\n## Experience\n- Built tooling\n**Key Project**\n"

        blocks = _parse_markdown_blocks(markdown)

        self.assertEqual(
            [(block.kind, block.level, block.text) for block in blocks],
            [
                ("heading", 1, "Candidate Example"),
                ("meta", 0, "Phone: 123"),
                ("blank", 0, ""),
                ("heading", 2, "Experience"),
                ("bullet", 0, "Built tooling"),
                ("emphasis", 0, "Key Project"),
            ],
        )

    def test_render_blocks_to_html_builds_browser_friendly_markup(self) -> None:
        markdown = (
            "# 候选人示例\n"
            "Phone: 123\n"
            "## Experience\n"
            "- 使用 **Perfetto** / *Systrace* 分析\n"
        )
        blocks = _parse_markdown_blocks(markdown)

        html = _render_blocks_to_html(
            blocks,
            style_config=_get_style_config("classic", "resume"),
            document_type="resume",
            style="classic",
        )

        self.assertIn('class="document style-classic type-resume"', html)
        self.assertIn("<h1 class=\"name\">候选人示例</h1>", html)
        self.assertIn("<p class=\"meta\">Phone: 123</p>", html)
        self.assertIn("<ul class=\"bullet-list\">", html)
        self.assertIn("<strong>Perfetto</strong>", html)
        self.assertIn("<em>Systrace</em>", html)
        self.assertIn("font-kerning: normal;", html)
        self.assertIn("PingFang SC", html)

    def test_render_markdown_to_pdf_prefers_browser_renderer(self) -> None:
        markdown = "# Candidate Example\nPhone: 123\n\n## Experience\n- Built tooling\n"

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "resume.pdf"

            def fake_browser_renderer(html: str, path: Path) -> None:
                self.assertIn("OfferPilot PDF Export", html)
                _write_fake_pdf(path, marker=b"%PDF-browser\n")

            with patch(
                "offerpilot.export._render_html_to_pdf_with_playwright",
                side_effect=fake_browser_renderer,
            ) as browser_renderer, patch(
                "offerpilot.export._render_markdown_to_pdf_with_reportlab"
            ) as fallback_renderer:
                saved_path = render_markdown_to_pdf(markdown, str(output_path))

            self.assertTrue(saved_path.exists())
            self.assertIn(b"%PDF-browser", saved_path.read_bytes())
            browser_renderer.assert_called_once()
            fallback_renderer.assert_not_called()

    def test_render_markdown_to_pdf_falls_back_when_browser_render_fails(self) -> None:
        markdown = "# Candidate Example\nPhone: 123\n\n## Experience\n- Built tooling\n"

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "resume.pdf"

            def fake_fallback_renderer(
                markdown_text: str,
                target_path: Path,
                *,
                document_type: str,
                style: str,
            ) -> None:
                self.assertEqual(document_type, "cover_letter")
                self.assertEqual(style, "ats")
                self.assertIn("Candidate Example", markdown_text)
                _write_fake_pdf(target_path, marker=b"%PDF-fallback\n")

            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                with patch(
                    "offerpilot.export._render_html_to_pdf_with_playwright",
                    side_effect=RuntimeError("Chromium missing"),
                ) as browser_renderer, patch(
                    "offerpilot.export._render_markdown_to_pdf_with_reportlab",
                    side_effect=fake_fallback_renderer,
                ) as fallback_renderer:
                    saved_path = render_markdown_to_pdf(
                        markdown,
                        str(output_path),
                        document_type="cover_letter",
                        style="ats",
                    )

            self.assertTrue(saved_path.exists())
            self.assertIn(b"%PDF-fallback", saved_path.read_bytes())
            browser_renderer.assert_called_once()
            fallback_renderer.assert_called_once()
            self.assertTrue(
                any("falling back to ReportLab" in str(warning.message) for warning in caught)
            )


if __name__ == "__main__":
    unittest.main()
