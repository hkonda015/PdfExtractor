from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from loguru import logger

from pdf_extractor.adapters.pdf_reader import extract_text
from pdf_extractor.utils.fs import ensure_dirs


def _iter_pdf_paths(root: Path, pattern: str, recursive: bool) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() == ".pdf":
            yield root
        return
    if recursive:
        yield from root.rglob(pattern)
    else:
        yield from root.glob(pattern)


def run_pipeline(
    input_path: str | Path,
    out_dir: str | Path = "data/out",
    *,
    pattern: str = "*.pdf",
    recursive: bool = False,
    overwrite: bool = False,
) -> list[Path]:
    """
    Process a single PDF file or a directory of PDFs.
    - Creates out_dir if missing.
    - Extracts text via adapters.pdf_reader.extract_text
    - Writes <name>.txt into out_dir
    Returns list of written file paths.
    """
    ensure_dirs(out_dir)
    out_base = Path(out_dir)
    src = Path(input_path)

    written: list[Path] = []
    for pdf in _iter_pdf_paths(src, pattern=pattern, recursive=recursive):
        target = out_base / f"{pdf.stem}.txt"
        if target.exists() and not overwrite:
            logger.info(f"Skip (exists): {target}")
            continue

        text = extract_text(pdf)
        if not text:
            logger.warning(f"No text extracted: {pdf} (scanned image? consider OCR)")
            # still create an empty file so the run is traceable
            target.write_text("", encoding="utf-8")
            written.append(target)
            continue

        target.write_text(text, encoding="utf-8")
        logger.info(f"Wrote: {target}")
        written.append(target)

    if not written:
        logger.warning("No files processed/written.")
    return written
