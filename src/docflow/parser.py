from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Block:
    kind: str
    text: str = ""
    level: int | None = None
    rows: tuple[tuple[str, ...], ...] = ()
    language: str | None = None


_ORDERED = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_UNORDERED = re.compile(r"^\s*[-*+]\s+(.*)$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_TABLE_SEPARATOR_CELL = re.compile(r"^:?-{3,}:?$")


def validate_markdown(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    if not path.is_file():
        raise ValueError(f"A entrada precisa ser um arquivo: {path}")
    if path.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError("A entrada precisa ser um arquivo Markdown (.md ou .markdown).")
    if not path.read_text(encoding="utf-8").strip():
        raise ValueError("O arquivo Markdown está vazio.")


def _split_table_row(line: str) -> tuple[str, ...]:
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return tuple(cell.strip() for cell in value.split("|"))


def _is_table_separator(line: str) -> bool:
    cells = _split_table_row(line)
    return bool(cells) and all(_TABLE_SEPARATOR_CELL.fullmatch(cell) for cell in cells)


def parse_markdown(text: str) -> list[Block]:
    blocks: list[Block] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False
    code_language: str | None = None
    lines = text.splitlines()
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block("paragraph", " ".join(part.strip() for part in paragraph)))
            paragraph = []

    while index < len(lines):
        raw = lines[index]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                blocks.append(Block("code", "\n".join(code), language=code_language))
                code = []
                code_language = None
                in_code = False
            else:
                flush_paragraph()
                code_language = stripped[3:].strip() or None
                in_code = True
            index += 1
            continue

        if in_code:
            code.append(raw)
            index += 1
            continue

        if not stripped:
            flush_paragraph()
            index += 1
            continue

        if (
            "|" in line
            and index + 1 < len(lines)
            and "|" in lines[index + 1]
            and _is_table_separator(lines[index + 1])
        ):
            flush_paragraph()
            header = _split_table_row(line)
            rows = [header]
            index += 2
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip() or "|" not in candidate:
                    break
                row = _split_table_row(candidate)
                if len(row) != len(header):
                    break
                rows.append(row)
                index += 1
            blocks.append(Block("table", rows=tuple(rows)))
            continue

        heading = _HEADING.match(line)
        if heading:
            flush_paragraph()
            blocks.append(Block("heading", heading.group(2).strip(), len(heading.group(1))))
            index += 1
            continue

        unordered = _UNORDERED.match(line)
        if unordered:
            flush_paragraph()
            blocks.append(Block("unordered_list", unordered.group(1).strip()))
            index += 1
            continue

        ordered = _ORDERED.match(line)
        if ordered:
            flush_paragraph()
            blocks.append(Block("ordered_list", ordered.group(1).strip()))
            index += 1
            continue

        paragraph.append(line)
        index += 1

    flush_paragraph()
    if in_code:
        blocks.append(Block("code", "\n".join(code), language=code_language))

    return blocks
