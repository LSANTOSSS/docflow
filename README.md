# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos DOCX configuráveis e reproduzíveis.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## v0.3.0 — Templates

A v0.3.0 consolida uma camada de templates sobre a fundação de parsing e estilização das versões anteriores:

```text
Markdown
   ↓
Validação estrutural
   ↓
Parser
   ↓
Preset + YAML + DOCX-base
   ↓
Exportador DOCX
   ↓
Sumário opcional
   ↓
Documento final
```

### Suporte atual

- títulos Markdown (`#` a `######`);
- parágrafos e listas;
- tabelas Markdown;
- blocos de código com linguagem opcional;
- metadados, estilos, cabeçalho e rodapé;
- configuração YAML;
- DOCX-base configurável;
- presets `report` e `specification`;
- validação de títulos obrigatórios;
- sumário DOCX opcional;
- CLI `docflow export`;
- testes automatizados.

## Instalação local

Requer Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Uso

Sem configuração:

```bash
docflow export examples/sample.md -o output/sample.docx
```

Com preset e configuração YAML:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```

Exemplo de configuração:

```yaml
document:
  title: Documento DocFlow
  author: Lucas da Silva Santos
  header: DocFlow Portfolio
  footer: v0.3.0
  toc: true

template:
  preset: report
```

O preset `report` exige os títulos `Resumo` e `Resultados`. O preset `specification` exige `Objetivo`, `Requisitos` e `Critérios de Aceite`. Valores definidos no YAML podem sobrescrever configurações herdadas do preset.

Para usar um DOCX-base próprio, informe um caminho relativo ao YAML ou absoluto:

```yaml
template:
  path: templates/reference.docx
```

O arquivo precisa existir e usar extensão `.docx`. O DocFlow abre esse documento como base e preserva seus estilos e elementos existentes antes de acrescentar o conteúdo Markdown.

### Sumário

Com `document.toc: true`, o DocFlow inclui um campo de sumário baseado nos níveis de título 1 a 3. O campo é compatível com processadores DOCX que atualizam campos; quando necessário, abra o documento e atualize o sumário no editor.

## Testes

```bash
pytest
```

## Estrutura

```text
docflow/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── ROADMAP.md
├── AGENTS.md
├── pyproject.toml
├── src/
│   └── docflow/
│       ├── cli.py
│       ├── config.py
│       ├── parser.py
│       ├── presets.py
│       ├── validation.py
│       └── exporters/
│           └── docx.py
├── tests/
└── examples/
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A próxima etapa prevista é a v0.4.0 — Multi-format, com PDF, HTML, pipeline de publicação e relatório de validação.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
