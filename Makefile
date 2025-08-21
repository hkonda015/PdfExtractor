.PHONY: setup lint type test format run clean

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
	rm -rf .pytest_cache .mypy_cache build dist *.egg-info
