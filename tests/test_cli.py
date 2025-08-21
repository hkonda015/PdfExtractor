import subprocess
import sys
from pathlib import Path

import pytest


def test_cli_help() -> None:
    cmd = [sys.executable, "-m", "pdf_extractor", "--help"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    assert "Extract text from PDFs" in res.stdout


SAMPLE = Path("tests/data/sample.pdf")


@pytest.mark.skipif(not SAMPLE.exists(), reason="Add tests/data/sample.pdf (text PDF)")
def test_cli_run(tmp_path: Path) -> None:
    cmd = [
        sys.executable,
        "-m",
        "pdf_extractor",
        str(SAMPLE),
        "--out-dir",
        str(tmp_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0
    out = tmp_path / (SAMPLE.stem + ".txt")
    assert out.exists()
    assert out.read_text(encoding="utf-8") != ""
