from copy import deepcopy
from typing import Any

PRESETS: dict[str, dict[str, Any]] = {
    "report": {
        "document": {"subject": "Relatório gerado com DocFlow"},
        "styles": {"body": {"font": "Calibri", "size": 11}, "heading": {"font": "Calibri"}, "code": {"font": "Consolas", "size": 9}},
        "structure": {"required_headings": ["Resumo"]},
    },
    "specification": {
        "document": {"subject": "Especificação gerada com DocFlow"},
        "styles": {"body": {"font": "Arial", "size": 11}, "heading": {"font": "Arial"}, "code": {"font": "Consolas", "size": 9}},
        "structure": {"required_headings": ["Objetivo", "Requisitos"]},
    },
}
def get_preset(name: str) -> dict[str, Any]:
    try: return deepcopy(PRESETS[name])
    except KeyError as exc:
        raise ValueError(f"Preset desconhecido: {name}. Presets disponíveis: {', '.join(sorted(PRESETS))}.") from exc
