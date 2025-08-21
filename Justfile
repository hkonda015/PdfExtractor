set shell := ["powershell.exe", "-NoProfile", "-Command"]

setup:
    python -m pip install -U pip
    pip install -r requirements-all.txt
    pip install -e .
    pre-commit install

lint:
    ruff check .
    black --check .

type:
    mypy

test:
    pytest -q

format:
    ruff check . --fix
    black .

run:
    python -m pdf_extractor run

clean:
    Remove-Item -Recurse -Force .pytest_cache,.mypy_cache -ErrorAction SilentlyContinue
    Get-ChildItem -Filter "*.egg-info" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
