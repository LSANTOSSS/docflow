from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document
from docx.shared import Pt

from docflow.parser import Block


def _apply_document_config(document: Document, config: dict[str, Any]) -> None:
    metadata = config["document"]
    properties = document.core_properties
    for field in ("title", "author", "subject", "keywords"):
        value = metadata.get(field)
        if value:
            setattr(properties, field, str(value))

    styles = config["styles"]
    body = styles["body"]
    normal = document.styles["Normal"]
    normal.font.name = body["font"]
    normal.font.size = Pt(float(body["size"]))

    heading_font = styles["heading"]["font"]
    for level in range(1, 7):
        document.styles[f"Heading {level}"].font.name = heading_font

    header_text = metadata.get("header")
    footer_text = metadata.get("footer")
    for section in document.sections:
        if header_text:
            section.header.paragraphs[0].text = str(header_text)
        if footer_text:
            section.footer.paragraphs[0].text = str(footer_text)


def _add_code_block(document: Document, block: Block, code_style: dict[str, Any]) -> None:
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(3)
    if block.language:
        label = paragraph.add_run(f"{block.language}\n")
        label.bold = True
        label.font.name = code_style["font"]
        label.font.size = Pt(float(code_style["size"]))
    run = paragraph.add_run(block.text)
    run.font.name = code_style["font"]
    run.font.size = Pt(float(code_style["size"]))


def _add_table(document: Document, block: Block) -> None:
    if not block.rows:
        return
    table = document.add_table(rows=len(block.rows), cols=len(block.rows[0]))
    table.style = "Table Grid"
    for row_index, row in enumerate(block.rows):
        for column_index, value in enumerate(row):
            cell = table.cell(row_index, column_index)
            cell.text = value
            if row_index == 0:
                for run in cell.paragraphs[0].runs:
                    run.bold = True


def export_docx(blocks: list[Block], output: Path, config: dict[str, Any] | None = None) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    config = config or {
        "document": {
            "title": None,
            "author": None,
            "subject": None,
            "keywords": None,
            "header": None,
            "footer": None,
        },
        "styles": {
            "body": {"font": "Arial", "size": 11},
            "heading": {"font": "Arial"},
            "code": {"font": "Courier New", "size": 9},
        },
    }
    _apply_document_config(document, config)

    code_style = config["styles"]["code"]
    for block in blocks:
        if block.kind == "heading":
            document.add_heading(block.text, level=block.level or 1)
        elif block.kind == "unordered_list":
            document.add_paragraph(block.text, style="List Bullet")
        elif block.kind == "ordered_list":
            document.add_paragraph(block.text, style="List Number")
        elif block.kind == "code":
            _add_code_block(document, block, code_style)
        elif block.kind == "table":
            _add_table(document, block)
        else:
            document.add_paragraph(block.text)

    document.save(output)
    return output
