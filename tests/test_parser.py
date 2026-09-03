from pathlib import Path

import pytest

from docflow.parser import parse_markdown, validate_markdown


def test_parse_supported_blocks():
    blocks = parse_markdown(
        """# Título

Texto de exemplo.

- item
1. primeiro

```python
print('ok')
```
"""
    )

    assert [block.kind for block in blocks] == [
        "heading",
        "paragraph",
        "unordered_list",
        "ordered_list",
        "code",
    ]
    assert blocks[0].level == 1
    assert "print('ok')" in blocks[-1].text


def test_validate_rejects_empty_markdown(tmp_path: Path):
    source = tmp_path / "empty.md"
    source.write_text("\n", encoding="utf-8")

    with pytest.raises(ValueError, match="vazio"):
        validate_markdown(source)
