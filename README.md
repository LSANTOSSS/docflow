# DocFlow

**Markdown document automation with validation and multi-format delivery.**

[![CI](https://github.com/LSANTOSSS/docflow/actions/workflows/ci.yml/badge.svg)](https://github.com/LSANTOSSS/docflow/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/LSANTOSSS/docflow)](https://github.com/LSANTOSSS/docflow/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11%2B-informational)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational)](LICENSE)

O **DocFlow** é uma CLI em Python que transforma uma única fonte Markdown em documentos **DOCX, HTML e PDF**, aplicando configuração, presets e validação estrutural antes da geração dos artefatos.

Foi desenvolvido como projeto público e clean-room de portfólio para demonstrar **Python, automação documental, desenho de CLI, parsing, validação, testes e CI/CD**.

> **Release atual:** [v0.4.0 — Multi-format](https://github.com/LSANTOSSS/docflow/releases/tag/v0.4.0)

## O problema

Documentos mantidos manualmente em vários formatos tendem a divergir, exigir trabalho repetitivo e dificultar a validação antes da entrega. O DocFlow trata o Markdown como fonte e cria um fluxo reproduzível entre conteúdo, validação e publicação.

```text
Markdown
   ↓
Validação estrutural
   ↓
Parser
   ↓
Configuração / Preset
   ↓
Exportador
   ├── DOCX
   ├── HTML
   └── PDF
```

## O que a v0.4.0 entrega

- exportação DOCX, HTML e PDF;
- configuração documental via YAML;
- presets `report` e `specification`;
- suporte a DOCX-base configurável;
- validação de títulos obrigatórios;
- comando `docflow validate`;
- relatório de validação em JSON;
- sumário DOCX opcional;
- cabeçalho, rodapé, metadados e estilos configuráveis;
- tabelas, listas e blocos de código;
- testes automatizados;
- GitHub Actions com geração de artefatos de demonstração.

## Quick start

Requer Python 3.11+.

```bash
git clone https://github.com/LSANTOSSS/docflow.git
cd docflow
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Gere os três formatos a partir do mesmo Markdown:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
docflow export examples/sample.md -o output/sample.html -c examples/docflow.yaml
docflow export examples/sample.md -o output/sample.pdf -c examples/docflow.yaml
```

Valide a estrutura e gere um relatório JSON:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml --report output/validation.json
```

## Configuração

O arquivo YAML permite combinar metadados, estilos, presets e regras estruturais sem acoplar essas decisões ao conteúdo Markdown. Também é possível fornecer um DOCX-base próprio para controlar a identidade visual do documento gerado.

A exportação PDF é feita diretamente em Python com ReportLab. O exportador cobre títulos, parágrafos, listas, tabelas, blocos de código e metadados básicos, além de cabeçalho e rodapé quando configurados.

## Qualidade e pipeline

O workflow `.github/workflows/ci.yml` executa a suíte de testes e valida o fluxo público de demonstração. A pipeline gera automaticamente:

- `sample.docx`;
- `sample.html`;
- `sample.pdf`;
- `validation.json`.

A release v0.4.0 foi validada com sucesso pelo GitHub Actions antes da publicação formal.

## Evolução do projeto

| Versão | Marco |
| --- | --- |
| v0.1 | Foundation — CLI, parser, DOCX e testes |
| v0.2 | Document Styling — YAML, estilos, tabelas, código, header/footer |
| v0.3 | Templates — presets, DOCX-base, validação estrutural e sumário |
| v0.4 | Multi-format — HTML, PDF, relatório JSON e pipeline CI |

Consulte [`ROADMAP.md`](ROADMAP.md) e [`CHANGELOG.md`](CHANGELOG.md) para o histórico completo.

## Relação com o SAF

O DocFlow complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF). O SAF apresenta o lado de **análise e Engenharia de Requisitos** do portfólio; o DocFlow demonstra a transformação desse perfil em **automação, desenvolvimento, testes e tooling**.

Os projetos são independentes e públicos, mas juntos mostram um fluxo que vai da estruturação do problema à automação de entregáveis.

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações, credenciais ou artefatos de ambientes corporativos.

## Testes

```bash
pytest
```

## Licença

MIT — consulte [`LICENSE`](LICENSE).
