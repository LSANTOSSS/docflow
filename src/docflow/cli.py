from __future__ import annotations

import argparse
from pathlib import Path

from docflow.exporters.docx import export_docx
from docflow.parser import parse_markdown, validate_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="docflow",
        description="Automação documental a partir de Markdown.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export = subparsers.add_parser("export", help="Exporta um documento Markdown.")
    export.add_argument("source", type=Path, help="Arquivo Markdown de entrada.")
    export.add_argument("-o", "--output", type=Path, required=True, help="Arquivo DOCX de saída.")

    return parser


def run_export(source: Path, output: Path) -> Path:
    validate_markdown(source)
    if output.suffix.lower() != ".docx":
        raise ValueError("Na v0.1.0, a saída suportada é .docx.")

    text = source.read_text(encoding="utf-8")
    blocks = parse_markdown(text)
    return export_docx(blocks, output)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "export":
            output = run_export(args.source, args.output)
            print(f"Documento gerado: {output}")
            return 0
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
