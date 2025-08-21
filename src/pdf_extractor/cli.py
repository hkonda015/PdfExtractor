from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from loguru import logger
from rich import print as rprint
from rich.console import Console
from rich.progress import Progress

from pdf_extractor.core.pipeline import run_pipeline
from pdf_extractor.settings import settings

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Extract text from PDFs and write .txt files to out_dir.",
)
console = Console()


def _validate_path(p: Path) -> Path:
    if not p.exists():
        raise typer.BadParameter(f"Path does not exist: {p}")
    return p


@app.command("run")
def run(
    # NOTE: defaults belong to the function parameters (after the annotation),
    #       not inside typer.Argument/Option metadata.
    input_path: Annotated[Path, typer.Argument(help="Path to a PDF file OR a folder of PDFs")],
    out_dir: Annotated[Path, typer.Option(help="Output dir for extracted .txt files")] = Path(
        "data/out"
    ),
    pattern: Annotated[
        str, typer.Option(help="Glob pattern when input_path is a folder")
    ] = "*.pdf",
    recursive: Annotated[
        bool, typer.Option(help="Recurse into subfolders if input_path is a folder")
    ] = False,
    overwrite: Annotated[bool, typer.Option(help="Overwrite existing .txt files")] = False,
    log_level: Annotated[
        str | None,
        typer.Option(help="Override LOG_LEVEL from .env (e.g., DEBUG, INFO, WARNING)"),
    ] = None,
) -> None:
    """
    Extract text from PDFs and write .txt files to out_dir.
    """
    # Configure logging
    level = (log_level or settings.log_level or "INFO").upper()
    logger.remove()
    logger.add(lambda m: rprint(m, end=""), level=level)
    logger.info(f"Timeout: {settings.timeout}s  Base URL: {settings.base_url or '-'}")

    input_path = _validate_path(input_path)

    # Expand target list
    if input_path.is_file():
        paths = [input_path]
    else:
        paths = list(input_path.rglob(pattern) if recursive else input_path.glob(pattern))

    if not paths:
        rprint("[yellow]No matching PDFs found.[/yellow]")
        raise typer.Exit(code=0)

    written: list[Path] = []
    if len(paths) == 1:
        written = run_pipeline(
            input_path=paths[0],
            out_dir=out_dir,
            pattern=pattern,
            recursive=recursive,
            overwrite=overwrite,
        )
    else:
        with Progress(console=console) as progress:
            task = progress.add_task("Extracting", total=len(paths))
            for p in paths:
                run_pipeline(input_path=p, out_dir=out_dir, overwrite=overwrite)
                written.append(Path(out_dir) / f"{p.stem}.txt")
                progress.advance(task)

    rprint(
        f"[bold green]Done[/bold green]. Wrote {len(written)} file(s) to [cyan]{out_dir}[/cyan]."
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
