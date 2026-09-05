from pathlib import Path
import subprocess
import sys


def _run(*args: str):
    return subprocess.run(
        [sys.executable, "-m", "docflow.cli", *args],
        text=True,
        capture_output=True,
        check=False,
    )


def test_cli_version_is_stable():
    result = _run("--version")
    assert result.returncode == 0
    assert result.stdout.strip() == "docflow 1.0.0"


def test_end_to_end_validate_then_export_all_formats(tmp_path: Path):
    source = tmp_path / "document.md"
    config = tmp_path / "docflow.yaml"
    report = tmp_path / "validation.json"

    source.write_text(
        "# Documento\n\n## Resumo\n\nConteúdo estável para o fluxo E2E.\n",
        encoding="utf-8",
    )
    config.write_text("template:\n  preset: report\n", encoding="utf-8")

    validation = _run("validate", str(source), "-c", str(config), "--report", str(report))
    assert validation.returncode == 0, validation.stderr
    assert "Validação concluída: válido" in validation.stdout
    assert report.exists()

    for suffix in (".docx", ".html", ".pdf"):
        output = tmp_path / f"document{suffix}"
        export = _run("export", str(source), "-o", str(output), "-c", str(config))
        assert export.returncode == 0, export.stderr
        assert output.exists() and output.stat().st_size > 0


def test_cli_error_message_for_unsupported_output(tmp_path: Path):
    source = tmp_path / "document.md"
    source.write_text("# Documento\n", encoding="utf-8")
    result = _run("export", str(source), "-o", str(tmp_path / "document.txt"))
    assert result.returncode == 2
    assert "Formato de saída não suportado. Use .docx, .html ou .pdf." in result.stderr
