from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle

from docflow.parser import Block

_FONT_MAP = {
    "Arial": "Helvetica",
    "Calibri": "Helvetica",
    "Times New Roman": "Times-Roman",
    "Courier New": "Courier",
    "Consolas": "Courier",
}


def _pdf_font(name: str | None, fallback: str) -> str:
    if not name:
        return fallback
    return _FONT_MAP.get(str(name), fallback)


def _heading_size(base_size: float, level: int) -> float:
    return max(base_size - (level - 1) * 1.3, 12.0)


def _styles(config: dict[str, Any]):
    styles_cfg = config.get("styles", {})
    body_cfg = styles_cfg.get("body", {})
    heading_cfg = styles_cfg.get("heading", {})
    code_cfg = styles_cfg.get("code", {})
    sample = getSampleStyleSheet()

    body_font = _pdf_font(body_cfg.get("font"), "Helvetica")
    body_size = float(body_cfg.get("size") or 11)
    heading_font = _pdf_font(heading_cfg.get("font"), body_font)
    heading_base_size = float(heading_cfg.get("size") or 18)
    code_font = _pdf_font(code_cfg.get("font"), "Courier")
    code_size = float(code_cfg.get("size") or 9)

    body = ParagraphStyle(
        "DocFlowBody",
        parent=sample["BodyText"],
        fontName=body_font,
        fontSize=body_size,
        leading=body_size * 1.4,
        spaceAfter=4,
    )
    headings = {}
    for level in range(1, 7):
        level_size = _heading_size(heading_base_size, level)
        headings[level] = ParagraphStyle(
            f"DocFlowHeading{level}",
            parent=sample["Heading1"],
            fontName=heading_font,
            fontSize=level_size,
            leading=level_size * 1.2,
            spaceBefore=8,
            spaceAfter=4,
        )
    code = ParagraphStyle(
        "DocFlowCode",
        parent=sample["Code"],
        fontName=code_font,
        fontSize=code_size,
        leading=code_size * 1.25,
        spaceAfter=6,
    )
    return body, headings, code, body_font


def _page_decorator(config: dict[str, Any], font_name: str):
    metadata = config.get("document", {})
    header = str(metadata.get("header") or "")
    footer = str(metadata.get("footer") or "")

    def decorate(canvas, document):
        canvas.saveState()
        canvas.setFont(font_name, 8)
        if header:
            canvas.drawString(document.leftMargin, A4[1] - 12 * mm, header)
        if footer:
            canvas.drawString(document.leftMargin, 10 * mm, footer)
        canvas.restoreState()

    return decorate


def export_pdf(blocks: list[Block], output: Path, config: dict[str, Any]) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = config.get("document", {})
    body, headings, code, body_font = _styles(config)
    story = []
    ordered_index = 0

    for block in blocks:
        if block.kind == "ordered_list":
            ordered_index += 1
            story.append(Paragraph(f"{ordered_index}. {escape(block.text)}", body))
            continue

        ordered_index = 0
        if block.kind == "heading":
            level = min(max(block.level or 1, 1), 6)
            story.append(Paragraph(escape(block.text), headings[level]))
        elif block.kind == "unordered_list":
            story.append(Paragraph(f"• {escape(block.text)}", body))
        elif block.kind == "code":
            prefix = f"{block.language}\n" if block.language else ""
            story.append(Preformatted(escape(prefix + block.text), code))
        elif block.kind == "table" and block.rows:
            data = [[Paragraph(escape(cell), body) for cell in row] for row in block.rows]
            table = Table(data, repeatRows=1)
            table.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("FONTNAME", (0, 0), (-1, 0), body_font),
                    ]
                )
            )
            story.extend([table, Spacer(1, 6)])
        else:
            story.append(Paragraph(escape(block.text), body))

    document = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        title=str(metadata.get("title") or ""),
        author=str(metadata.get("author") or ""),
        subject=str(metadata.get("subject") or ""),
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    decorate = _page_decorator(config, body_font)
    document.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return output
