from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.shared import Pt

from docflow.parser import Block


def export_docx(blocks: list[Block], output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    document = Document()

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
            run.font.name = "Courier New"
            run.font.size = Pt(9)
        else:
            document.add_paragraph(block.text)

    document.save(output)
    return output
