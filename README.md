# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega configuráveis e reproduzíveis.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## Versão estável

A versão estável atual é a **v0.3.0 — Templates**, com DOCX configurável, presets, validação estrutural e sumário opcional.

A **v0.4.0 — Multi-format** está em desenvolvimento. A primeira rodada adiciona exportação HTML e relatório de validação, preservando a exportação DOCX existente.

## Fluxo

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
   └── HTML
```

## Instalação local

Requer Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Exportação

DOCX:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```

HTML:

```bash
docflow export examples/sample.md -o output/sample.html -c examples/docflow.yaml
```

## Validação e relatório

A v0.4.0 introduz um comando dedicado de validação:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml
```

Para persistir o resultado em JSON:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml --report output/validation.json
```

O relatório registra se o documento é válido, títulos encontrados, títulos obrigatórios ausentes e contagem dos blocos estruturais reconhecidos pelo parser.

## Recursos disponíveis

- títulos Markdown (`#` a `######`);
- parágrafos e listas;
- tabelas Markdown;
- blocos de código com linguagem opcional;
- metadados, estilos, cabeçalho e rodapé no DOCX;
- configuração YAML;
- DOCX-base configurável;
- presets `report` e `specification`;
- validação de títulos obrigatórios;
- sumário DOCX opcional;
- exportação DOCX e HTML;
- relatório JSON de validação;
- testes automatizados.

## Testes

```bash
pytest
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A próxima rodada da v0.4.0 prevê **PDF + pipeline de publicação + fechamento da versão**.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
