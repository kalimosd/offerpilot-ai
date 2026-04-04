#!/usr/bin/env python3
"""Extract plain text from OfferPilot source files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}
UNSUPPORTED_EXTENSIONS = {".doc"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract readable text from .txt, .md, .pdf, or .docx source files."
    )
    parser.add_argument("path", help="Source file to extract text from.")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional file path to save the extracted text.",
    )
    return parser


def load_text_from_file(path: str) -> str:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return file_path.read_text(encoding="utf-8").strip()
    if suffix == ".pdf":
        return _load_pdf_text(file_path)
    if suffix == ".docx":
        return _load_docx_text(file_path)
    if suffix in UNSUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Format {suffix} is not supported. "
            "Please export the file as .docx, .pdf, .txt, or .md."
        )

    raise ValueError(
        f"Unsupported file format: {suffix or '[no extension]'}. "
        "Please use .txt, .md, .pdf, or .docx."
    )


def _load_pdf_text(file_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: pypdf. Install project dependencies before reading PDFs."
        ) from exc

    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(page.strip() for page in pages if page.strip()).strip()
    if text:
        return text

    raise ValueError(
        "Could not extract readable text from the PDF. "
        "Please use a text-based PDF or convert it to .txt/.md."
    )


def _load_docx_text(file_path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency: python-docx. Install project dependencies before reading DOCX files."
        ) from exc

    document = Document(str(file_path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    text = "\n".join(paragraph for paragraph in paragraphs if paragraph).strip()
    if text:
        return text

    raise ValueError(
        "Could not extract readable text from the DOCX file. "
        "Please check the file content and try again."
    )


def main() -> int:
    args = build_parser().parse_args()

    try:
        text = load_text_from_file(args.path)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
        print(f"OK: extracted text saved to {output_path}")
        return 0

    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
