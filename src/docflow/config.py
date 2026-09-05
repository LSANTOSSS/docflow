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
        "heading": {"font": "Arial", "size": 18},
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


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path}")
    if path.suffix.lower() not in {".yaml", ".yml"}:
        raise ValueError("A configuração deve usar extensão .yaml ou .yml.")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError("A raiz da configuração YAML deve ser um objeto.")
    return data


def _normalize_extends(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise ValueError("extends deve ser um caminho ou uma lista de caminhos YAML.")


def _prepare_local_paths(data: dict[str, Any], config_path: Path) -> dict[str, Any]:
    prepared = deepcopy(data)
    template = prepared.get("template")
    if isinstance(template, dict) and template.get("path"):
        raw = Path(str(template["path"]))
        if not raw.is_absolute():
            template["path"] = str((config_path.parent / raw).resolve())
    return prepared


def _load_composed_data(path: Path, stack: tuple[Path, ...] = ()) -> dict[str, Any]:
    resolved = path.resolve()
    if resolved in stack:
        chain = " -> ".join(item.name for item in (*stack, resolved))
        raise ValueError(f"Ciclo de configuração detectado em extends: {chain}.")

    data = _read_yaml(resolved)
    extends = _normalize_extends(data.get("extends"))
    local = deepcopy(data)
    local.pop("extends", None)

    composed: dict[str, Any] = {}
    next_stack = (*stack, resolved)
    for raw_base in extends:
        base_path = Path(raw_base)
        if not base_path.is_absolute():
            base_path = resolved.parent / base_path
        composed = _merge(composed, _load_composed_data(base_path, next_stack))

    return _merge(composed, _prepare_local_paths(local, resolved))


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

    data = _load_composed_data(path)
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
    _resolve_template_path(config, path.resolve())
    return config
