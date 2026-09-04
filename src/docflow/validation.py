from typing import Any
from docflow.parser import Block

def validate_structure(blocks: list[Block], config: dict[str, Any]) -> None:
    required=config.get("structure",{}).get("required_headings") or []
    if not isinstance(required,list): raise ValueError("structure.required_headings deve ser uma lista.")
    headings={b.text.casefold() for b in blocks if b.kind=="heading" and b.text}
    missing=[str(name) for name in required if str(name).casefold() not in headings]
    if missing: raise ValueError("Seções obrigatórias ausentes: "+", ".join(missing)+".")
