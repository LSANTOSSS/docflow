from pathlib import Path
from typing import Any

from docflow.parser import Block


def build_validation_report(blocks: list[Block], config: dict[str, Any], source: Path | None = None) -> dict[str, Any]:
    required = config.get("structure", {}).get("required_headings") or []
    if not isinstance(required, list):
        raise ValueError("structure.required_headings deve ser uma lista.")

    headings = [block.text for block in blocks if block.kind == "heading" and block.text]
    normalized = {heading.casefold() for heading in headings}
    missing = [str(name) for name in required if str(name).casefold() not in normalized]
    counts: dict[str, int] = {}
    for block in blocks:
        counts[block.kind] = counts.get(block.kind, 0) + 1

    checks = [
        {
            "id": "required_headings",
            "status": "passed" if not missing else "failed",
            "message": (
                "Todas as seções obrigatórias estão presentes."
                if not missing
                else "Seções obrigatórias ausentes: " + ", ".join(missing) + "."
            ),
        }
    ]
    issues = [
        {
            "code": "missing_required_heading",
            "severity": "error",
            "message": f"Seção obrigatória ausente: {heading}.",
            "heading": heading,
        }
        for heading in missing
    ]

    return {
        "valid": not issues,
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
        "block_counts": counts,
    }


def validate_structure(blocks: list[Block], config: dict[str, Any]) -> None:
    report = build_validation_report(blocks, config)
    if not report["valid"]:
        raise ValueError("Seções obrigatórias ausentes: " + ", ".join(report["missing_headings"]) + ".")
