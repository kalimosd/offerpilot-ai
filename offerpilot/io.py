from pathlib import Path

from docx import Document
from pypdf import PdfReader


SUPPORTED_TEXT_EXTENSIONS = {".txt", ".md", ".pdf", ".docx"}
UNSUPPORTED_EXTENSIONS = {".doc"}


def load_text_from_file(path: str) -> str:
    """Load text from supported file formats."""
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


def save_text_to_file(path: str, content: str) -> Path:
    """Save generated text to a file, creating parent folders if needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def _load_pdf_text(file_path: Path) -> str:
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
    document = Document(str(file_path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    text = "\n".join(paragraph for paragraph in paragraphs if paragraph).strip()
    if text:
        return text

    raise ValueError(
        "Could not extract readable text from the DOCX file. "
        "Please check the file content and try again."
    )
