from pathlib import Path

import pytest

from docflow.config import load_config
from docflow.parser import parse_markdown
from docflow.presets import get_preset
from docflow.validation import validate_structure


def test_template_library_exposes_new_presets():
    meeting = get_preset("meeting-notes")
    decision = get_preset("decision-record")

    assert meeting["structure"]["required_headings"] == ["Participantes", "Decisões", "Próximos passos"]
    assert decision["structure"]["required_headings"] == ["Contexto", "Decisão", "Consequências"]
    assert meeting["structure"]["single_h1"] is True
    assert decision["structure"]["unique_headings"] is True


def test_new_preset_can_be_overridden_without_mutating_library(tmp_path: Path):
    config_path = tmp_path / "docflow.yaml"
    config_path.write_text(
        "template:\n  preset: meeting-notes\nstyles:\n  body:\n    size: 12\n",
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config["styles"]["body"]["font"] == "Calibri"
    assert config["styles"]["body"]["size"] == 12
    assert get_preset("meeting-notes")["styles"]["body"]["size"] == 11


def test_new_presets_enforce_their_structure():
    meeting = get_preset("meeting-notes")
    decision = get_preset("decision-record")

    validate_structure(
        parse_markdown(
            "# Reunião\n\n## Participantes\n\nTime.\n\n## Decisões\n\nDecisão.\n\n## Próximos passos\n\nAção.\n"
        ),
        meeting,
    )
    validate_structure(
        parse_markdown(
            "# ADR\n\n## Contexto\n\nContexto.\n\n## Decisão\n\nDecisão.\n\n## Consequências\n\nEfeito.\n"
        ),
        decision,
    )

    with pytest.raises(ValueError, match="Próximos passos"):
        validate_structure(parse_markdown("# Reunião\n\n## Participantes\n\nTime.\n\n## Decisões\n\nDecisão.\n"), meeting)


def test_public_v060_examples_match_their_presets():
    root = Path(__file__).resolve().parents[1]
    cases = [
        (root / "examples" / "meeting-notes.md", root / "examples" / "meeting-notes.yaml"),
        (root / "examples" / "decision-record.md", root / "examples" / "decision-record.yaml"),
    ]

    for source, config_path in cases:
        config = load_config(config_path)
        blocks = parse_markdown(source.read_text(encoding="utf-8"))
        validate_structure(blocks, config)
