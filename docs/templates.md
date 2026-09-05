# Biblioteca de templates

A v0.6.0 amplia os presets públicos do DocFlow sem acoplar o conteúdo Markdown a um único modelo documental. O preset fornece uma base reutilizável de metadados, estilos e regras estruturais; o arquivo YAML continua podendo sobrescrever valores específicos do documento.

## Presets disponíveis

| Preset | Uso sugerido | Seções obrigatórias |
| --- | --- | --- |
| `report` | relatório geral | `Resumo` |
| `specification` | especificação funcional/técnica | `Objetivo`, `Requisitos` |
| `meeting-notes` | ata ou registro de reunião | `Participantes`, `Decisões`, `Próximos passos` |
| `decision-record` | registro de decisão | `Contexto`, `Decisão`, `Consequências` |

Os presets `meeting-notes` e `decision-record` também habilitam validações para um único H1, títulos únicos e hierarquia sem saltos de nível.

## Selecionando um preset

```yaml
template:
  preset: meeting-notes
```

O mesmo arquivo pode customizar qualquer valor herdado:

```yaml
template:
  preset: meeting-notes

styles:
  body:
    size: 12

document:
  author: Example Author
```

A composição segue a precedência atual do DocFlow: configuração padrão → preset → valores informados no YAML. Assim, um preset funciona como base e o documento preserva liberdade para customização local.

## Criando um documento a partir de um preset

1. escolha o preset mais próximo do tipo de documento;
2. crie o Markdown mantendo as seções exigidas pelo preset;
3. crie um YAML com `template.preset` e somente os overrides necessários;
4. execute `docflow validate` antes da exportação;
5. exporte a mesma fonte para DOCX, HTML ou PDF.

Exemplos públicos estão disponíveis em `examples/meeting-notes.*` e `examples/decision-record.*`.

## Customização e limites

Presets definem defaults reutilizáveis, não conteúdo. O Markdown continua sendo a fonte principal e nenhum preset injeta texto de domínio no documento. Quando uma estrutura precisar de regras diferentes, prefira sobrescrever a configuração no YAML em vez de duplicar conteúdo entre documentos.

Nesta primeira rodada da v0.6.0, a reutilização acontece por herança de um único preset com overrides locais. Composição entre múltiplos arquivos de configuração permanece como evolução separada da milestone.
