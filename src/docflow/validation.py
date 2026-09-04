from pathlib import Path
from typing import Any

from docflow.parser import Block


def _rule_enabled(structure: dict[str, Any], name: str) -> bool:
    value = structure.get(name, False)
    if not isinstance(value, bool):
        raise ValueError(f"structure.{name} deve ser true ou false.")
    return value


def _validation_error(report: dict[str, Any]) -> str:
    messages = [str(issue["message"]) for issue in report.get("issues", []) if issue.get("severity") == "error"]
    return "Validação estrutural falhou: " + " ".join(messages)


def build_validation_report(blocks: list[Block], config: dict[str, Any], source: Path | None = None) -> dict[str, Any]:
    structure = config.get("structure", {}) or {}
    if not isinstance(structure, dict):
        raise ValueError("A seção structure da configuração deve ser um objeto.")

    required = structure.get("required_headings") or []
    if not isinstance(required, list):
        raise ValueError("structure.required_headings deve ser uma lista.")

    heading_blocks = [block for block in blocks if block.kind == "heading" and block.text]
    headings = [block.text for block in heading_blocks]
    normalized = {heading.casefold() for heading in headings}
    missing = [str(name) for name in required if str(name).casefold() not in normalized]

    counts: dict[str, int] = {}
    for block in blocks:
        counts[block.kind] = counts.get(block.kind, 0) + 1

    checks: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    checks.append(
        {
            "id": "required_headings",
            "status": "passed" if not missing else "failed",
            "message": (
                "Todas as seções obrigatórias estão presentes."
                if not missing
                else "Seções obrigatórias ausentes: " + ", ".join(missing) + "."
            ),
        }
    )
    issues.extend(
        {
            "code": "missing_required_heading",
            "severity": "error",
            "message": f"Seção obrigatória ausente: {heading}.",
            "heading": heading,
        }
        for heading in missing
    )

    duplicate_headings: list[str] = []
    if _rule_enabled(structure, "unique_headings"):
        seen: set[str] = set()
        duplicate_keys: set[str] = set()
        for heading in headings:
            key = heading.casefold()
            if key in seen and key not in duplicate_keys:
                duplicate_headings.append(heading)
                duplicate_keys.add(key)
            seen.add(key)
        checks.append(
            {
                "id": "unique_headings",
                "status": "passed" if not duplicate_headings else "failed",
                "message": (
                    "Os títulos são únicos."
                    if not duplicate_headings
                    else "Títulos duplicados: " + ", ".join(duplicate_headings) + "."
                ),
            }
        )
        issues.extend(
            {
                "code": "duplicate_heading",
                "severity": "error",
                "message": f"Título duplicado: {heading}.",
                "heading": heading,
            }
            for heading in duplicate_headings
        )

    h1_count = sum((block.level or 1) == 1 for block in heading_blocks)
    if _rule_enabled(structure, "single_h1"):
        checks.append(
            {
                "id": "single_h1",
                "status": "passed" if h1_count == 1 else "failed",
                "message": (
                    "O documento possui exatamente um título H1."
                    if h1_count == 1
                    else f"Esperado exatamente um H1; encontrados {h1_count}."
                ),
            }
        )
        if h1_count != 1:
            issues.append(
                {
                    "code": "invalid_h1_count",
                    "severity": "error",
                    "message": f"Esperado exatamente um H1; encontrados {h1_count}.",
                    "count": h1_count,
                }
            )

    heading_level_skips: list[dict[str, Any]] = []
    if _rule_enabled(structure, "no_heading_level_skips"):
        previous = None
        for block in heading_blocks:
            level = block.level or 1
            if previous is not None and level > previous + 1:
                heading_level_skips.append(
                    {
                        "heading": block.text,
                        "previous_level": previous,
                        "level": level,
                    }
                )
            previous = level
        checks.append(
            {
                "id": "no_heading_level_skips",
                "status": "passed" if not heading_level_skips else "failed",
                "message": (
                    "A hierarquia de títulos não possui saltos de nível."
                    if not heading_level_skips
                    else f"Encontrados {len(heading_level_skips)} salto(s) na hierarquia de títulos."
                ),
            }
        )
        issues.extend(
            {
                "code": "heading_level_skip",
                "severity": "error",
                "message": (
                    f"Salto de nível antes de '{item['heading']}': "
                    f"H{item['previous_level']} → H{item['level']}."
                ),
                **item,
            }
            for item in heading_level_skips
        )

    return {
        "valid": not any(issue.get("severity") == "error" for issue in issues),
        "source": str(source) if source else None,
        "summary": {
            "checks": len(checks),
            "passed": sum(check["status"] == "passed" for check in checks),
            "failed": sum(check["status"] == "failed" for check in checks),
            "issues": len(issues),
        },
        "checks": checks,
        "issues": issues,
        "required_headings": [str(name) for name in required],
        "headings": headings,
        "missing_headings": missing,
        "duplicate_headings": duplicate_headings,
        "h1_count": h1_count,
        "heading_level_skips": heading_level_skips,
        "block_counts": counts,
    }


def validate_structure(blocks: list[Block], config: dict[str, Any]) -> None:
    report = build_validation_report(blocks, config)
    if not report["valid"]:
        raise ValueError(_validation_error(report))


def validation_error_message(report: dict[str, Any]) -> str:
    return _validation_error(report)
