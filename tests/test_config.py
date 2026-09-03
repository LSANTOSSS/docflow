from pathlib import Path

import pytest

from docflow.config import load_config


def test_load_config_merges_defaults(tmp_path: Path):
    path = tmp_path / "docflow.yaml"
    path.write_text("styles:\n  body:\n    size: 12\n", encoding="utf-8")

    config = load_config(path)

    assert config["styles"]["body"]["size"] == 12
    assert config["styles"]["body"]["font"] == "Arial"
    assert config["styles"]["code"]["font"] == "Courier New"


def test_load_config_rejects_non_mapping_yaml(tmp_path: Path):
    path = tmp_path / "docflow.yaml"
    path.write_text("- item\n", encoding="utf-8")

    with pytest.raises(ValueError, match="raiz"):
        load_config(path)
