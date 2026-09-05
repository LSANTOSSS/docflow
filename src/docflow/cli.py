import argparse
from pathlib import Path

from docflow import __version__
from docflow.config import load_config
from docflow.exporters.docx import export_docx
from docflow.exporters.html import export_html
from docflow.exporters.pdf import export_pdf
from docflow.parser import parse_markdown, validate_markdown
from docflow.validation import build_validation_report, validate_structure, validation_error_message

SUPPORTED_OUTPUTS = {".docx", ".html", ".pdf"}


def build_parser():
    parser = argparse.ArgumentParser(prog="docflow", description="Automação documental a partir de Markdown.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subs = parser.add_subparsers(dest="command", required=True)

    export = subs.add_parser("export", help="Exporta um documento Markdown.")
    export.add_argument("source", type=Path, help="Arquivo Markdown de origem.")
    export.add_argument("-o", "--output", type=Path, required=True, help="Destino .docx, .html ou .pdf.")
    export.add_argument("-c", "--config", type=Path, help="Arquivo YAML opcional de configuração.")

    validate = subs.add_parser("validate", help="Valida um documento Markdown e gera relatório opcional.")
    validate.add_argument("source", type=Path, help="Arquivo Markdown de origem.")
    validate.add_argument("-c", "--config", type=Path, help="Arquivo YAML opcional de configuração.")
    validate.add_argument("--report", type=Path, help="Destino opcional do relatório JSON.")
    return parser


def _load_document(source: Path, config_path: Path | None):
    validate_markdown(source)
    config = load_config(config_path)
    blocks = parse_markdown(source.read_text(encoding="utf-8"))
    return config, blocks


def run_export(source: Path, output: Path, config_path: Path | None = None) -> Path:
    suffix = output.suffix.lower()
    if suffix not in SUPPORTED_OUTPUTS:
        raise ValueError("Formato de saída não suportado. Use .docx, .html ou .pdf.")
    config, blocks = _load_document(source, config_path)
    validate_structure(blocks, config)
    if suffix == ".docx":
        return export_docx(blocks, output, config=config)
    if suffix == ".html":
        return export_html(blocks, output, config=config)
    return export_pdf(blocks, output, config=config)


def run_validation(source: Path, config_path: Path | None = None, report_path: Path | None = None) -> dict:
    config, blocks = _load_document(source, config_path)
    report = build_validation_report(blocks, config, source=source)
    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        import json
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not report["valid"]:
        raise ValueError(validation_error_message(report))
    return report


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            print(f"Documento gerado: {run_export(args.source, args.output, args.config)}")
            return 0
        if args.command == "validate":
            report = run_validation(args.source, args.config, args.report)
            print(f"Validação concluída: {'válido' if report['valid'] else 'inválido'}")
            return 0
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
