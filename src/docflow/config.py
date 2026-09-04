from copy import deepcopy
from pathlib import Path
from typing import Any
import yaml
from docflow.presets import get_preset

DEFAULT_CONFIG: dict[str, Any] = {
    "document": {
        "title": None,
        "author": None,
        "subject": None,
        "keywords": None,
        "header": None,
        "footer": None,
        "toc": False,
    },
    "styles": {
        "body": {"font": "Arial", "size": 11},
        "heading": {"font": "Arial"},
        "code": {"font": "Courier New", "size": 9},
    },
    "template": {"path": None, "preset": None},
    "structure": {
        "required_headings": [],
        "unique_headings": False,
        "single_h1": False,
        "no_heading_level_skips": False,
    },
}


def _merge(base, override):
    result = deepcopy(base)
    for key, value in override.items():
        result[key] = _merge(result[key], value) if isinstance(value, dict) and isinstance(result.get(key), dict) else value
    return result


def _resolve_template_path(config, config_path: Path):
    raw = config["template"].get("path")
    if not raw:
        return
    template = Path(str(raw))
    if not template.is_absolute():
        template = (config_path.parent / template).resolve()
    if template.suffix.lower() != ".docx":
        raise ValueError("O template de referência precisa ser um arquivo .docx.")
    if not template.exists() or not template.is_file():
        raise FileNotFoundError(f"Template DOCX não encontrado: {template}")
    config["template"]["path"] = str(template)


def load_config(path: Path | None = None):
    if path is None:
        return deepcopy(DEFAULT_CONFIG)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")
    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("A configuração deve usar extensão .yaml ou .yml.")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("A raiz da configuração YAML deve ser um objeto.")
    template = data.get("template") or {}
    if not isinstance(template, dict):
        raise ValueError("A seção template da configuração deve ser um objeto.")
    structure = data.get("structure") or {}
    if not isinstance(structure, dict):
        raise ValueError("A seção structure da configuração deve ser um objeto.")

    config = deepcopy(DEFAULT_CONFIG)
    preset = template.get("preset")
    if preset:
        config = _merge(config, get_preset(str(preset)))
    config = _merge(config, data)
    _resolve_template_path(config, path)
    return config
