# Documento de Exemplo

## Resumo

Este documento demonstra a versão pública do DocFlow e o fluxo multi-format da v0.4.0.

## Objetivos

- usar Markdown como fonte;
- validar a estrutura;
- exportar para DOCX, HTML e PDF;
- manter o processo reproduzível.

## Recursos da v0.4.0

| Recurso | Estado |
| --- | --- |
| Estilos YAML | Suportado |
| Tabelas | Suportado |
| Cabeçalho e rodapé | Suportado |
| HTML | Suportado |
| PDF | Suportado |
| Relatório de validação | Suportado |

## Exemplo de código

```python
print("DocFlow v0.4.0")
```

## Exemplo de comando

```bash
docflow export examples/sample.md -o output/sample.pdf -c examples/docflow.yaml
```
