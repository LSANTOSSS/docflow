from html.parser import HTMLParser
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from pypdf import PdfReader

from docflow.cli import run_export


class TextCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.parts.append(data.strip())


def _docx_text(path: Path) -> str:
    document = Document(path)
    parts: list[str] = []
    for item in document.iter_inner_content():
        if isinstance(item, Paragraph):
            if item.text:
                parts.append(item.text)
        elif isinstance(item, Table):
            for row in item.rows:
                parts.extend(cell.text for cell in row.cells if cell.text)
    return "\n".join(parts)


def _html_text(path: Path) -> str:
    parser = TextCollector()
    parser.feed(path.read_text(encoding="utf-8"))
    return "\n".join(parser.parts)


def _pdf_text(path: Path) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def test_common_structure_is_preserved_across_formats(tmp_path: Path):
    source = tmp_path / "consistency.md"
    source.write_text(
        """# Consistency Document

Common paragraph.

- Bullet item

1. First ordered item
2. Second ordered item

| Field | Value |
| --- | --- |
| status | consistent |

```python
print("docflow")
```
""",
        encoding="utf-8",
    )

    outputs = {
        "docx": tmp_path / "consistency.docx",
        "html": tmp_path / "consistency.html",
        "pdf": tmp_path / "consistency.pdf",
    }
    for output in outputs.values():
        run_export(source, output)

    extracted = {
        "docx": _docx_text(outputs["docx"]),
        "html": _html_text(outputs["html"]),
        "pdf": _pdf_text(outputs["pdf"]),
    }
    expected = [
        "Consistency Document",
        "Common paragraph.",
        "Bullet item",
        "First ordered item",
        "Second ordered item",
        "Field",
        "Value",
        "status",
        "consistent",
        'print("docflow")',
    ]

    for format_name, text in extracted.items():
        for token in expected:
            assert token in text, f"{token!r} ausente em {format_name}"
        positions = [text.index(token) for token in expected]
        assert positions == sorted(positions), f"ordem estrutural divergente em {format_name}"

    assert "python" in extracted["docx"]
    assert "python" in extracted["pdf"]
    assert 'class="language-python"' in outputs["html"].read_text(encoding="utf-8")


def test_ordered_lists_keep_sequence_in_html_and_pdf(tmp_path: Path):
    source = tmp_path / "ordered.md"
    source.write_text(
        """# Ordered

1. First item
2. Second item
3. Third item
""",
        encoding="utf-8",
    )
    html_output = tmp_path / "ordered.html"
    pdf_output = tmp_path / "ordered.pdf"

    run_export(source, html_output)
    run_export(source, pdf_output)

    html = html_output.read_text(encoding="utf-8")
    pdf = _pdf_text(pdf_output)

    assert "<ol><li>First item</li><li>Second item</li><li>Third item</li></ol>" in html
    assert "1. First item" in pdf
    assert "2. Second item" in pdf
    assert "3. Third item" in pdf


def test_docx_uses_numbered_list_style_for_ordered_items(tmp_path: Path):
    source = tmp_path / "ordered.md"
    output = tmp_path / "ordered.docx"
    source.write_text("1. First item\n2. Second item\n", encoding="utf-8")

    run_export(source, output)

    document = Document(output)
    ordered = [paragraph for paragraph in document.paragraphs if paragraph.text]
    assert [paragraph.text for paragraph in ordered] == ["First item", "Second item"]
    assert all(paragraph.style.name == "List Number" for paragraph in ordered)
