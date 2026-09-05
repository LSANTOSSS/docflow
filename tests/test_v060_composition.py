from pathlib import Path

import pytest
from docx import Document

from docflow.config import load_config


def test_config_can_extend_single_base(tmp_path: Path):
    base = tmp_path / "base.yaml"
    child = tmp_path / "child.yaml"
    base.write_text(
        "template:\n  preset: report\ndocument:\n  author: Shared Author\nstyles:\n  body:\n    font: Times New Roman\n",
        encoding="utf-8",
    )
    child.write_text(
        "extends: base.yaml\ndocument:\n  title: Child Document\nstyles:\n  body:\n    size: 12\n",
        encoding="utf-8",
    )

    config = load_config(child)

    assert config["template"]["preset"] == "report"
    assert config["document"]["author"] == "Shared Author"
    assert config["document"]["title"] == "Child Document"
    assert config["styles"]["body"] == {"font": "Times New Roman", "size": 12}
    assert config["structure"]["required_headings"] == ["Resumo"]


def test_config_can_extend_multiple_bases_in_order(tmp_path: Path):
    first = tmp_path / "first.yaml"
    second = tmp_path / "second.yaml"
    child = tmp_path / "child.yaml"
    first.write_text("document:\n  author: First\n  footer: Shared footer\n", encoding="utf-8")
    second.write_text("document:\n  author: Second\nstyles:\n  body:\n    size: 12\n", encoding="utf-8")
    child.write_text(
        "extends:\n  - first.yaml\n  - second.yaml\ndocument:\n  author: Child\n",
        encoding="utf-8",
    )

    config = load_config(child)

    assert config["document"]["author"] == "Child"
    assert config["document"]["footer"] == "Shared footer"
    assert config["styles"]["body"]["size"] == 12


def test_relative_template_path_is_resolved_from_declaring_base(tmp_path: Path):
    shared = tmp_path / "shared"
    shared.mkdir()
    template = shared / "reference.docx"
    Document().save(template)
    base = shared / "base.yaml"
    child = tmp_path / "child.yaml"
    base.write_text("template:\n  path: reference.docx\n", encoding="utf-8")
    child.write_text("extends: shared/base.yaml\n", encoding="utf-8")

    config = load_config(child)

    assert config["template"]["path"] == str(template.resolve())


def test_config_extends_cycle_is_rejected(tmp_path: Path):
    first = tmp_path / "first.yaml"
    second = tmp_path / "second.yaml"
    first.write_text("extends: second.yaml\n", encoding="utf-8")
    second.write_text("extends: first.yaml\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Ciclo de configuração detectado"):
        load_config(first)


def test_config_extends_requires_path_or_list(tmp_path: Path):
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text("extends:\n  base: shared.yaml\n", encoding="utf-8")

    with pytest.raises(ValueError, match="extends deve ser um caminho ou uma lista"):
        load_config(config_path)
