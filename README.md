# PDF Extractor (CLI)



Extract **text from PDFs** and write `.txt` files to an output folder.
Small, reliable, and Windows-friendly — with strict typing, linting, and pre-commit hooks.

> ⚠️ This tool extracts embedded text. For **scanned** (image-only) PDFs, you’ll need OCR (see **Roadmap**).

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration (.env)](#configuration-env)
- [Project Structure](#project-structure)
- [Development](#development)
- [Type Checking & Tests](#type-checking--tests)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- ✅ **Single file or folder** input (`--pattern`, `--recursive`)
- ✅ **Safe overwrites** (`--overwrite` required to replace outputs)
- ✅ **Rich logging** (`--log-level DEBUG|INFO|...`)
- ✅ **.env support** (`BASE_URL`, `API_KEY`, `TIMEOUT`, `LOG_LEVEL`)
- ✅ **Pre-commit**: Ruff (lint/format) + mypy (type checking)
- ✅ **Typed codebase** (Python 3.11)

---

## Requirements

- Python **3.11+**
- Windows, macOS, or Linux
- (Optional) Git, pipx/Conda

---

## Quick Start

### 1) Clone & create a virtual environment

**Windows (PowerShell)**
```powershell
git clone https://github.com/<your-user>/PdfExtractor.git
cd PdfExtractor
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
