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


def export_docx(blocks: list[Block], output: Path, config: dict[str, Any] | None = None) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = Document()
    config = config or {
        "document": {},
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
            paragraph = document.add_paragraph()
            run = paragraph.add_run(block.text)
            run.font.name = code_style["font"]
            run.font.size = Pt(float(code_style["size"]))
        else:
            document.add_paragraph(block.text)

    document.save(output)
    return output
