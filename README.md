# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega, começando por **DOCX**.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## Objetivo da v0.1.0

A primeira versão entrega um fluxo mínimo, mas funcional:

```text
Markdown
   ↓
Validação
   ↓
Parser estrutural
   ↓
Exportador DOCX
   ↓
Documento gerado
```

### Suporte inicial

- títulos Markdown (`#` a `######`);
- parágrafos;
- listas não ordenadas;
- listas ordenadas;
- blocos de código cercados por ```;
- validação de arquivo de entrada;
- saída `.docx` configurável;
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

```bash
docflow export examples/sample.md -o output/sample.docx
```

Ou:

```bash
python -m docflow.cli export examples/sample.md -o output/sample.docx
```

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
│       ├── parser.py
│       └── exporters/
│           └── docx.py
├── tests/
└── examples/
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A evolução prevista inclui estilos configuráveis, metadados, tabelas, imagens, templates DOCX, PDF, validações adicionais e pipeline de publicação.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
