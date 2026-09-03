from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Block:
    kind: str
    text: str
    level: int | None = None


_ORDERED = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_UNORDERED = re.compile(r"^\s*[-*+]\s+(.*)$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def validate_markdown(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    if not path.is_file():
        raise ValueError(f"A entrada precisa ser um arquivo: {path}")
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("A entrada precisa ser um arquivo Markdown (.md ou .markdown).")
    if not path.read_text(encoding="utf-8").strip():
        raise ValueError("O arquivo Markdown está vazio.")


def parse_markdown(text: str) -> list[Block]:
    blocks: list[Block] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block("paragraph", " ".join(part.strip() for part in paragraph)))
            paragraph = []

    for raw in text.splitlines():
        line = raw.rstrip()

        if line.strip().startswith("```"):
            if in_code:
                blocks.append(Block("code", "\n".join(code)))
                code = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue

        if in_code:
            code.append(raw)
            continue

        if not line.strip():
            flush_paragraph()
            continue

        heading = _HEADING.match(line)
        if heading:
            flush_paragraph()
            blocks.append(Block("heading", heading.group(2).strip(), len(heading.group(1))))
            continue

        unordered = _UNORDERED.match(line)
        if unordered:
            flush_paragraph()
            blocks.append(Block("unordered_list", unordered.group(1).strip()))
            continue

        ordered = _ORDERED.match(line)
        if ordered:
            flush_paragraph()
            blocks.append(Block("ordered_list", ordered.group(1).strip()))
            continue

        paragraph.append(line)

    flush_paragraph()
    if in_code:
        blocks.append(Block("code", "\n".join(code)))

    return blocks
