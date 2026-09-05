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

A precedência básica continua sendo: configuração padrão → preset → valores informados no YAML.

## Reutilizando configurações com `extends`

Um arquivo pode herdar de outro YAML e declarar apenas as diferenças locais:

```yaml
extends: template-base.yaml

document:
  title: Monthly Report

styles:
  body:
    size: 12
```

O arquivo-base pode concentrar decisões compartilhadas:

```yaml
template:
  preset: report

document:
  author: Example Team
  footer: Internal Example

styles:
  body:
    font: Times New Roman
```

Também é possível compor múltiplas bases:

```yaml
extends:
  - organization.yaml
  - report-style.yaml
```

A ordem de precedência é determinística: defaults → preset final → bases na ordem declarada → arquivo atual. Em conflitos entre bases, a base listada por último vence; o arquivo atual sempre possui a última palavra.

Caminhos relativos em `extends` são resolvidos a partir do YAML que os declara. O mesmo vale para `template.path`, de modo que um arquivo-base pode manter seu próprio DOCX de referência sem depender da localização do arquivo filho.

A composição é recursiva, mas ciclos são rejeitados explicitamente. Assim, `base-a.yaml → base-b.yaml → base-a.yaml` falha antes da exportação.

## Criando um documento a partir de um preset

1. escolha o preset mais próximo do tipo de documento;
2. crie o Markdown mantendo as seções exigidas pelo preset;
3. reutilize uma base com `extends` quando houver configuração comum;
4. mantenha no YAML do documento somente os overrides necessários;
5. execute `docflow validate` antes da exportação;
6. exporte a mesma fonte para DOCX, HTML ou PDF.

Exemplos públicos estão disponíveis em `examples/meeting-notes.*`, `examples/decision-record.*`, `examples/template-base.yaml` e `examples/report-derived.yaml`.

## Customização e limites

Presets e arquivos-base definem defaults reutilizáveis, não conteúdo. O Markdown continua sendo a fonte principal e nenhuma composição injeta texto de domínio no documento.

Use presets para representar tipos documentais, `extends` para compartilhar configuração entre documentos e overrides locais para exceções específicas. Essa separação evita duplicação de YAML sem transformar o DocFlow em um sistema de templates de conteúdo.
