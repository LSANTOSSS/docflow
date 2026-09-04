from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from docflow.parser import Block


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _heading_size(base_size: float, level: int) -> float:
    return max(base_size - (level - 1) * 1.3, 12.0)


def _table_html(block: Block) -> str:
    if not block.rows:
        return ""
    header, *body = block.rows
    head = "".join(f"<th>{_escape(cell)}</th>" for cell in header)
    rows = "".join(
        "<tr>" + "".join(f"<td>{_escape(cell)}</td>" for cell in row) + "</tr>"
        for row in body
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"


def export_html(blocks: list[Block], output: Path, config: dict[str, Any]) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = config.get("document", {})
    title = str(metadata.get("title") or "DocFlow Document")
    author = str(metadata.get("author") or "")
    styles = config.get("styles", {})
    body_style = styles.get("body", {})
    heading_style = styles.get("heading", {})
    code_style = styles.get("code", {})
    font = str(body_style.get("font") or "Arial")
    size = float(body_style.get("size") or 11)
    heading_font = str(heading_style.get("font") or font)
    heading_size = float(heading_style.get("size") or 18)
    code_font = str(code_style.get("font") or "Courier New")
    code_size = float(code_style.get("size") or 9)

    parts: list[str] = []
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if block.kind in {"unordered_list", "ordered_list"}:
            kind = block.kind
            tag = "ul" if kind == "unordered_list" else "ol"
            items: list[str] = []
            while index < len(blocks) and blocks[index].kind == kind:
                items.append(f"<li>{_escape(blocks[index].text)}</li>")
                index += 1
            parts.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        if block.kind == "heading":
            level = min(max(block.level or 1, 1), 6)
            parts.append(f"<h{level}>{_escape(block.text)}</h{level}>")
        elif block.kind == "code":
            language = f' class="language-{_escape(block.language)}"' if block.language else ""
            parts.append(f"<pre><code{language}>{_escape(block.text)}</code></pre>")
        elif block.kind == "table":
            parts.append(_table_html(block))
        else:
            parts.append(f"<p>{_escape(block.text)}</p>")
        index += 1

    heading_rules = "\n".join(
        f"h{level} {{ font-family: {heading_font}, sans-serif; font-size: {_heading_size(heading_size, level):g}pt; line-height: 1.2; margin: .8em 0 .35em; }}"
        for level in range(1, 7)
    )
    author_meta = f'<meta name="author" content="{_escape(author)}">' if author else ""
    content = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_escape(title)}</title>
{author_meta}
<style>
body {{ font-family: {font}, sans-serif; font-size: {size:g}pt; line-height: 1.4; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
{heading_rules}
table {{ border-collapse: collapse; width: 100%; margin: .5rem 0; }}
th, td {{ border: 1px solid currentColor; padding: .4rem; text-align: left; vertical-align: top; }}
pre {{ overflow-x: auto; padding: .75rem; border: 1px solid currentColor; font-family: {code_font}, monospace; font-size: {code_size:g}pt; line-height: 1.25; }}
</style>
</head>
<body>
{chr(10).join(parts)}
</body>
</html>
"""
    output.write_text(content, encoding="utf-8")
    return output
