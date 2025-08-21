from pathlib import Path

import pytest

from pdf_extractor.adapters.pdf_reader import extract_text

SAMPLE = Path("tests/data/sample.pdf")


@pytest.mark.skipif(not SAMPLE.exists(), reason="Add tests/data/sample.pdf (text PDF)")
def test_extract_text_returns_text() -> None:
    text = extract_text(SAMPLE)
    assert isinstance(text, str)
    assert len(text) > 0
