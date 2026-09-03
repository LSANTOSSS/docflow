from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "document": {
        "title": None,
        "author": None,
        "subject": None,
        "keywords": None,
    },
    "styles": {
        "body": {"font": "Arial", "size": 11},
        "heading": {"font": "Arial"},
        "code": {"font": "Courier New", "size": 9},
    },
}


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(path: Path | None = None) -> dict[str, Any]:
    if path is None:
        return deepcopy(DEFAULT_CONFIG)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")
    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("A configuração deve usar extensão .yaml ou .yml.")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("A raiz da configuração YAML deve ser um objeto.")
    return _merge(DEFAULT_CONFIG, data)
