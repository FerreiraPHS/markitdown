#!/usr/bin/env python3
"""Worker simples: observa uploads/ e gera markdown em results/ usando MarkItDown."""

from pathlib import Path

from convert_watch import watch


def main() -> None:
    base = Path(__file__).resolve().parent
    watch(upload_dir=base / "../../uploads", results_dir=base / "../../results")


if __name__ == "__main__":
    main()
