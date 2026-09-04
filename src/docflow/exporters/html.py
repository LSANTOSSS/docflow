from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from docflow.parser import Block


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


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
    body_style = config.get("styles", {}).get("body", {})
    font = str(body_style.get("font") or "Arial")
    size = float(body_style.get("size") or 11)

    parts: list[str] = []
    for block in blocks:
        if block.kind == "heading":
            level = min(max(block.level or 1, 1), 6)
            parts.append(f"<h{level}>{_escape(block.text)}</h{level}>")
        elif block.kind == "unordered_list":
            parts.append(f"<ul><li>{_escape(block.text)}</li></ul>")
        elif block.kind == "ordered_list":
            parts.append(f"<ol><li>{_escape(block.text)}</li></ol>")
        elif block.kind == "code":
            language = f' class="language-{_escape(block.language)}"' if block.language else ""
            parts.append(f"<pre><code{language}>{_escape(block.text)}</code></pre>")
        elif block.kind == "table":
            parts.append(_table_html(block))
        else:
            parts.append(f"<p>{_escape(block.text)}</p>")

    author_meta = f'<meta name="author" content="{_escape(author)}">' if author else ""
    content = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_escape(title)}</title>
{author_meta}
<style>
body {{ font-family: {font}, sans-serif; font-size: {size}pt; line-height: 1.5; max-width: 960px; margin: 2rem auto; padding: 0 1rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid currentColor; padding: .4rem; text-align: left; }}
pre {{ overflow-x: auto; padding: .75rem; border: 1px solid currentColor; }}
</style>
</head>
<body>
{chr(10).join(parts)}
</body>
</html>
"""
    output.write_text(content, encoding="utf-8")
    return output
