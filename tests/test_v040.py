from pathlib import Path

import pytest

from docflow.cli import run_export, run_validation


def test_export_html(tmp_path: Path):
    source = tmp_path / "sample.md"
    output = tmp_path / "sample.html"
    source.write_text(
        """# Documento

Texto <seguro>.

| Campo | Valor |
| --- | --- |
| versão | 0.4.0 |

```python
print("docflow")
```
""",
        encoding="utf-8",
    )

    generated = run_export(source, output)
    content = output.read_text(encoding="utf-8")

    assert generated == output
    assert "<!doctype html>" in content
    assert "<h1>Documento</h1>" in content
    assert "Texto &lt;seguro&gt;." in content
    assert "<table>" in content
    assert 'class="language-python"' in content


def test_export_pdf(tmp_path: Path):
    source = tmp_path / "sample.md"
    output = tmp_path / "sample.pdf"
    config = tmp_path / "docflow.yaml"
    source.write_text(
        """# Documento

Texto de teste.

| Campo | Valor |
| --- | --- |
| versão | 0.4.0 |

```python
print("docflow")
```
""",
        encoding="utf-8",
    )
    config.write_text(
        "document:\n  title: PDF público\n  author: Lucas da Silva Santos\n  header: DocFlow\n  footer: v0.4.0\n",
        encoding="utf-8",
    )

    generated = run_export(source, output, config)

    assert generated == output
    assert output.exists()
    assert output.stat().st_size > 1000
    assert output.read_bytes().startswith(b"%PDF")


def test_validation_report_is_written(tmp_path: Path):
    source = tmp_path / "report.md"
    config = tmp_path / "docflow.yaml"
    report = tmp_path / "validation.json"
    source.write_text("# Resumo\n\nTexto.\n", encoding="utf-8")
    config.write_text("template:\n  preset: report\n", encoding="utf-8")

    result = run_validation(source, config, report)

    assert result["valid"] is True
    assert result["summary"] == {"checks": 1, "passed": 1, "failed": 0, "issues": 0}
    assert result["checks"][0]["status"] == "passed"
    assert result["issues"] == []
    assert result["block_counts"]["heading"] == 1
    assert report.exists()
    assert '"valid": true' in report.read_text(encoding="utf-8")


def test_invalid_validation_report_is_actionable_and_written(tmp_path: Path):
    source = tmp_path / "report.md"
    config = tmp_path / "docflow.yaml"
    report = tmp_path / "validation.json"
    source.write_text("# Introdução\n\nTexto.\n", encoding="utf-8")
    config.write_text("template:\n  preset: report\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Resumo"):
        run_validation(source, config, report)

    content = report.read_text(encoding="utf-8")
    assert '"valid": false' in content
    assert '"failed": 1' in content
    assert '"code": "missing_required_heading"' in content
    assert '"heading": "Resumo"' in content
