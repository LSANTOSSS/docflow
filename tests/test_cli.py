from pathlib import Path

from docflow.cli import run_export


def test_export_creates_docx(tmp_path: Path):
    source = tmp_path / "sample.md"
    output = tmp_path / "sample.docx"
    source.write_text("# Documento\n\nConteúdo de teste.\n", encoding="utf-8")

    generated = run_export(source, output)

    assert generated == output
    assert output.exists()
    assert output.stat().st_size > 0
