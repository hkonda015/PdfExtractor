from __future__ import annotations

from pathlib import Path

import pdfplumber


def extract_text(pdf_path: str | Path) -> str:
    """
    Extract text from a text-based PDF.
    Returns a normalized string (LF newlines). If no text is found, returns "".
    """
    p = Path(pdf_path)
    if not p.exists():
        raise FileNotFoundError(p)

    text_parts: list[str] = []
    try:
        with pdfplumber.open(p) as pdf:
            for page in pdf.pages:
                # page.extract_text() returns None on some pages; guard with or ""
                page_text = page.extract_text() or ""
                text_parts.append(page_text)
    except Exception as exc:  # pragma: no cover (depends on specific PDFs)
        # Caller (pipeline) will decide how to handle/log this, we keep simple here.
        raise RuntimeError(f"Failed to read PDF: {p}") from exc

    # Normalize line endings to LF
    return ("\n".join(text_parts)).replace("\r\n", "\n").replace("\r", "\n").strip()
