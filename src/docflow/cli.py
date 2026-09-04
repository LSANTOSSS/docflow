import argparse
from pathlib import Path
from docflow.config import load_config
from docflow.exporters.docx import export_docx
from docflow.parser import parse_markdown, validate_markdown
from docflow.validation import validate_structure

def build_parser():
    parser=argparse.ArgumentParser(prog="docflow",description="Automação documental a partir de Markdown.")
    subs=parser.add_subparsers(dest="command",required=True)
    export=subs.add_parser("export",help="Exporta um documento Markdown.")
    export.add_argument("source",type=Path); export.add_argument("-o","--output",type=Path,required=True); export.add_argument("-c","--config",type=Path)
    return parser
def run_export(source: Path, output: Path, config_path: Path|None=None)->Path:
    validate_markdown(source)
    if output.suffix.lower()!=".docx": raise ValueError("A saída suportada é .docx.")
    config=load_config(config_path); blocks=parse_markdown(source.read_text(encoding="utf-8"))
    validate_structure(blocks,config)
    return export_docx(blocks,output,config=config)
def main(argv=None):
    parser=build_parser(); args=parser.parse_args(argv)
    try:
        if args.command=="export":
            print(f"Documento gerado: {run_export(args.source,args.output,args.config)}"); return 0
    except (FileNotFoundError,ValueError) as exc: parser.error(str(exc))
    return 1
if __name__=="__main__": raise SystemExit(main())
