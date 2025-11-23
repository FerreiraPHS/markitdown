#!/usr/bin/env python3
"""
Conversor simples: varre a pasta uploads e gera markdown em results usando MarkItDown.
Sem filas, OpenAI ou banco; focado em uso local.
"""

from pathlib import Path
from typing import Iterable, Tuple

from markitdown import MarkItDown

SUPPORTED_EXTS = {".pdf", ".docx", ".txt", ".md", ".rtf", ".html"}


def iter_input_files(upload_dir: Path) -> Iterable[Path]:
    """Yield arquivos suportados da pasta de upload."""
    for path in upload_dir.glob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
            yield path


def convert_file(md: MarkItDown, src: Path, dest: Path) -> None:
    """Converte um arquivo com MarkItDown e grava markdown."""
    print(f"[convert] {src.name}")
    result = md.convert(str(src))
    if not result or not result.text_content:
        raise ValueError("MarkItDown nao retornou conteudo")
    dest.write_text(result.text_content, encoding="utf-8")
    print(f"[ok] -> {dest}")


def watch(upload_dir: Path, results_dir: Path) -> None:
    """
    Processa todos os arquivos suportados e encerra quando nao ha mais trabalho.
    Registra falhas para evitar loops infinitos em casos de erro.
    """
    md = MarkItDown()
    processed: set[Tuple[Path, Path]] = set()
    failed: set[Tuple[Path, Path]] = set()

    upload_dir.mkdir(exist_ok=True, parents=True)
    results_dir.mkdir(exist_ok=True, parents=True)

    print(f"[start] Monitorando {upload_dir.resolve()}")
    print(f"[start] Gravando resultados em {results_dir.resolve()}")

    while True:
        pending: list[Tuple[Path, Path, Tuple[Path, Path]]] = []
        for src in iter_input_files(upload_dir):
            dest = results_dir / f"{src.stem}.md"
            key = (src.resolve(), dest.resolve())
            if key in processed or key in failed:
                continue
            pending.append((src, dest, key))

        if not pending:
            if failed:
                print(
                    f"[done] Nenhum novo arquivo. {len(failed)} conversao(oes) falhou/falharam; corrija e rode novamente."
                )
            else:
                print("[done] Nenhum novo arquivo para converter. Encerrando.")
            break

        for src, dest, key in pending:
            try:
                convert_file(md, src, dest)
                processed.add(key)
            except KeyboardInterrupt:
                print("\n[stop] Encerrado pelo usuario")
                return
            except Exception as exc:
                print(f"[error] {src.name}: {exc}")
                failed.add(key)


if __name__ == "__main__":
    base = Path(__file__).resolve().parent
    watch(upload_dir=base / "../../uploads", results_dir=base / "../../results")
