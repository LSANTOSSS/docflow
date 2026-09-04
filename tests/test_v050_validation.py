import json
from pathlib import Path

import pytest

from docflow.cli import run_export, run_validation


def _strict_config(path: Path) -> None:
    path.write_text(
        """structure:
  unique_headings: true
  single_h1: true
  no_heading_level_skips: true
""",
        encoding="utf-8",
    )


def test_strict_structural_validation_passes_for_well_formed_document(tmp_path: Path):
    source = tmp_path / "valid.md"
    config = tmp_path / "docflow.yaml"
    source.write_text(
        """# Document

## Overview

Text.

### Details

More text.
""",
        encoding="utf-8",
    )
    _strict_config(config)

    report = run_validation(source, config)

    assert report["valid"] is True
    assert report["summary"] == {"checks": 4, "passed": 4, "failed": 0, "issues": 0}
    assert report["h1_count"] == 1
    assert report["duplicate_headings"] == []
    assert report["heading_level_skips"] == []


def test_strict_structural_validation_reports_multiple_actionable_issues(tmp_path: Path):
    source = tmp_path / "invalid.md"
    config = tmp_path / "docflow.yaml"
    report_path = tmp_path / "validation.json"
    source.write_text(
        """# Document

# Other title

## Section

## Section

#### Deep detail
""",
        encoding="utf-8",
    )
    _strict_config(config)

    with pytest.raises(ValueError, match="Validação estrutural falhou"):
        run_validation(source, config, report_path)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    codes = {issue["code"] for issue in report["issues"]}

    assert report["valid"] is False
    assert report["summary"]["failed"] == 3
    assert report["h1_count"] == 2
    assert report["duplicate_headings"] == ["Section"]
    assert report["heading_level_skips"] == [
        {"heading": "Deep detail", "previous_level": 2, "level": 4}
    ]
    assert codes == {"duplicate_heading", "invalid_h1_count", "heading_level_skip"}


def test_export_is_blocked_when_enabled_structure_rule_fails(tmp_path: Path):
    source = tmp_path / "invalid.md"
    config = tmp_path / "docflow.yaml"
    output = tmp_path / "invalid.html"
    source.write_text("# Title\n\n# Second title\n", encoding="utf-8")
    config.write_text("structure:\n  single_h1: true\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Esperado exatamente um H1"):
        run_export(source, output, config)

    assert not output.exists()


def test_structure_rules_must_be_boolean(tmp_path: Path):
    source = tmp_path / "document.md"
    config = tmp_path / "docflow.yaml"
    source.write_text("# Title\n", encoding="utf-8")
    config.write_text("structure:\n  unique_headings: yes-please\n", encoding="utf-8")

    with pytest.raises(ValueError, match="structure.unique_headings deve ser true ou false"):
        run_validation(source, config)
