from pathlib import Path
from typing import Any
from docx import Document
from docx.shared import Pt
from docflow.parser import Block

def _apply_document_config(document: Document, config: dict[str, Any]) -> None:
    metadata=config["document"]; properties=document.core_properties
    for field in ("title","author","subject","keywords"):
        value=metadata.get(field)
        if value: setattr(properties,field,str(value))
    styles=config["styles"]; body=styles["body"]; normal=document.styles["Normal"]
    normal.font.name=body["font"]; normal.font.size=Pt(float(body["size"]))
    for level in range(1,7): document.styles[f"Heading {level}"].font.name=styles["heading"]["font"]
    for section in document.sections:
        if metadata.get("header"): section.header.paragraphs[0].text=str(metadata["header"])
        if metadata.get("footer"): section.footer.paragraphs[0].text=str(metadata["footer"])

def _add_code_block(document, block, code_style):
    p=document.add_paragraph(); p.paragraph_format.space_before=Pt(3); p.paragraph_format.space_after=Pt(3)
    if block.language:
        label=p.add_run(f"{block.language}\n"); label.bold=True; label.font.name=code_style["font"]; label.font.size=Pt(float(code_style["size"]))
    run=p.add_run(block.text); run.font.name=code_style["font"]; run.font.size=Pt(float(code_style["size"]))

def _add_table(document, block):
    if not block.rows: return
    table=document.add_table(rows=len(block.rows),cols=len(block.rows[0])); table.style="Table Grid"
    for ri,row in enumerate(block.rows):
        for ci,value in enumerate(row):
            cell=table.cell(ri,ci); cell.text=value
            if ri==0:
                for run in cell.paragraphs[0].runs: run.bold=True

def _create_document(config):
    template_path=config.get("template",{}).get("path")
    return Document(str(template_path)) if template_path else Document()

def export_docx(blocks: list[Block], output: Path, config: dict[str, Any] | None=None) -> Path:
    output.parent.mkdir(parents=True,exist_ok=True)
    if config is None:
        from docflow.config import DEFAULT_CONFIG
        config=DEFAULT_CONFIG
    document=_create_document(config); _apply_document_config(document,config)
    code_style=config["styles"]["code"]
    for block in blocks:
        if block.kind=="heading": document.add_heading(block.text,level=block.level or 1)
        elif block.kind=="unordered_list": document.add_paragraph(block.text,style="List Bullet")
        elif block.kind=="ordered_list": document.add_paragraph(block.text,style="List Number")
        elif block.kind=="code": _add_code_block(document,block,code_style)
        elif block.kind=="table": _add_table(document,block)
        else: document.add_paragraph(block.text)
    document.save(output); return output
