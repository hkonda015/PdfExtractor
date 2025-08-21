from pathlib import Path

import pytest

from pdf_extractor.core.pipeline import run_pipeline

SAMPLE = Path("tests/data/sample.pdf")


@pytest.mark.skipif(not SAMPLE.exists(), reason="Add tests/data/sample.pdf (text PDF)")
def test_pipeline_writes_txt(tmp_path: Path) -> None:
    out_files = run_pipeline(SAMPLE, out_dir=tmp_path, overwrite=True)
    assert len(out_files) == 1
    out = out_files[0]
    assert out.exists()
    assert out.suffix == ".txt"
    assert out.read_text(encoding="utf-8") != ""
