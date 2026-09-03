from pathlib import Path

from docx import Document

from docflow.cli import run_export


def test_export_creates_docx(tmp_path: Path):
    source = tmp_path / "sample.md"
    output = tmp_path / "sample.docx"
    source.write_text("# Documento\n\nConteúdo de teste.\n", encoding="utf-8")

    generated = run_export(source, output)

    assert generated == output
    assert output.exists()
    assert output.stat().st_size > 0


def test_export_uses_yaml_metadata_and_styles(tmp_path: Path):
    source = tmp_path / "sample.md"
    config = tmp_path / "docflow.yaml"
    output = tmp_path / "sample.docx"
    source.write_text("# Documento\n\nConteúdo.\n", encoding="utf-8")
    config.write_text(
        """document:
  title: Documento configurado
  author: Autor de teste
styles:
  body:
    font: Aptos
    size: 12
  heading:
    font: Aptos Display
""",
        encoding="utf-8",
    )

    run_export(source, output, config)
    document = Document(output)

    assert document.core_properties.title == "Documento configurado"
    assert document.core_properties.author == "Autor de teste"
    assert document.styles["Normal"].font.name == "Aptos"
    assert document.styles["Normal"].font.size.pt == 12
    assert document.styles["Heading 1"].font.name == "Aptos Display"
