# Documento de Exemplo

Este documento demonstra a versão pública do DocFlow.

## Objetivos

- usar Markdown como fonte;
- validar a entrada;
- exportar para DOCX;
- manter o processo reproduzível.

## Recursos da v0.2.0

| Recurso | Estado |
| --- | --- |
| Estilos YAML | Suportado |
| Tabelas | Suportado |
| Cabeçalho e rodapé | Suportado |

## Exemplo de código

```python
print("DocFlow v0.2.0")
```

## Exemplo de comando

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```
