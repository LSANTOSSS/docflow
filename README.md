# DocFlow

**Markdown document automation with validation, templates and multi-format delivery.**

[![CI](https://github.com/LSANTOSSS/docflow/actions/workflows/ci.yml/badge.svg)](https://github.com/LSANTOSSS/docflow/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/LSANTOSSS/docflow)](https://github.com/LSANTOSSS/docflow/releases/latest)
[![Python](https://img.shields.io/badge/Python-3.11%2B-informational)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-informational)](LICENSE)

O **DocFlow** é uma CLI em Python que transforma uma única fonte Markdown em documentos **DOCX, HTML e PDF**, aplicando configuração, presets, composição de YAML e validação estrutural antes da geração dos artefatos.

Foi desenvolvido como projeto público e clean-room de portfólio para demonstrar **Python, automação documental, desenho de CLI, parsing, validação, testes, empacotamento e CI/CD**.

> **Stable CLI:** v1.0.0

## O problema

Documentos mantidos manualmente em vários formatos tendem a divergir, exigir trabalho repetitivo e dificultar a validação antes da entrega. O DocFlow trata o Markdown como fonte e cria um fluxo reproduzível entre conteúdo, validação e publicação.

```text
Markdown
   ↓
Validação estrutural
   ↓
Parser
   ↓
Configuração / Preset / extends
   ↓
Exportador
   ├── DOCX
   ├── HTML
   └── PDF
```

## O que a v1.0.0 entrega

- CLI estável com `docflow validate` e `docflow export`;
- `docflow --version`;
- exportação DOCX, HTML e PDF pela mesma fonte Markdown;
- configuração documental via YAML;
- presets `report`, `specification`, `meeting-notes` e `decision-record`;
- composição de configurações com `extends`;
- suporte a DOCX-base configurável;
- validações estruturais opcionais e específicas por preset;
- relatório JSON com resultados acionáveis;
- consistência estrutural e tipográfica entre exportadores;
- cabeçalho, rodapé, metadados, estilos, tabelas, listas e blocos de código;
- testes de regressão multi-formato e fluxo E2E `validate → export`;
- build de wheel/sdist, `twine check` e instalação limpa do wheel no CI;
- política de compatibilidade para a linha 1.x.

## Instalação para desenvolvimento

Requer Python 3.11+.

```bash
git clone https://github.com/LSANTOSSS/docflow.git
cd docflow
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Consulte [`docs/distribution.md`](docs/distribution.md) para build e instalação do pacote gerado.

## Uso

Confira a versão:

```bash
docflow --version
```

Valide a estrutura e gere um relatório JSON:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml --report output/validation.json
```

Gere os três formatos a partir do mesmo Markdown:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
docflow export examples/sample.md -o output/sample.html -c examples/docflow.yaml
docflow export examples/sample.md -o output/sample.pdf -c examples/docflow.yaml
```

## Templates e configuração

O YAML permite combinar metadados, estilos, presets e regras estruturais sem acoplar essas decisões ao conteúdo. A v0.6 adicionou uma biblioteca pública de templates e composição com `extends`, permitindo reutilizar bases de configuração e manter overrides locais.

Consulte [`docs/templates.md`](docs/templates.md) para presets, customização e herança de configurações. As diferenças intencionais entre os exportadores estão em [`docs/format-consistency.md`](docs/format-consistency.md), e as regras de validação em [`docs/validation.md`](docs/validation.md).

## Qualidade e distribuição

O workflow `.github/workflows/ci.yml` executa testes, o fluxo público de demonstração, build de distribuição e validação de instalação limpa. A pipeline gera:

- `sample.docx`;
- `sample.html`;
- `sample.pdf`;
- `validation.json`;
- wheel e source distribution em `dist/`.

O wheel produzido pelo próprio CI é instalado em um ambiente virtual separado e a CLI instalada é executada antes de o build ser considerado válido.

## Compatibilidade 1.x

A interface pública estável inclui os comandos `validate` e `export`, suas opções documentadas, os formatos DOCX/HTML/PDF, os presets publicados, `extends` e os campos já expostos no relatório JSON. Mudanças incompatíveis ficam reservadas para uma nova versão major.

Consulte [`docs/compatibility.md`](docs/compatibility.md).

## Evolução do projeto

| Versão | Marco |
| --- | --- |
| v0.1 | Foundation — CLI, parser, DOCX e testes |
| v0.2 | Document Styling — YAML, estilos, tabelas, código, header/footer |
| v0.3 | Templates — presets, DOCX-base, validação estrutural e sumário |
| v0.4 | Multi-format — HTML, PDF, relatório JSON e pipeline CI |
| v0.5 | Quality & Validation — consistência multi-formato, validações e regressão |
| v0.6 | Template Library — novos presets e composição de configurações |
| v0.7 | Distribution — build, wheel, metadados e instalação limpa |
| v1.0 | Stable CLI — interface pública, E2E e política de compatibilidade |

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
