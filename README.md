# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega, começando por **DOCX**.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## Objetivo da v0.2.0

A v0.2.0 amplia a fundação da CLI com configuração e apresentação documental:

```text
Markdown
   ↓
Validação
   ↓
Parser estrutural
   ↓
Configuração YAML
   ↓
Exportador DOCX
   ↓
Documento estilizado
```

### Suporte atual

- títulos Markdown (`#` a `######`);
- parágrafos;
- listas não ordenadas;
- listas ordenadas;
- tabelas Markdown no formato com linha separadora;
- blocos de código cercados por ```, com identificação opcional da linguagem;
- validação de arquivo de entrada;
- saída `.docx` configurável;
- metadados DOCX;
- estilos de corpo, títulos e código;
- cabeçalho e rodapé;
- configuração opcional via YAML;
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

Com configuração YAML:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```

Ou:

```bash
python -m docflow.cli export examples/sample.md -o output/sample.docx
```

## Configuração YAML

Exemplo:

```yaml
document:
  title: Documento DocFlow
  author: Lucas da Silva Santos
  header: DocFlow Portfolio
  footer: v0.2.0

styles:
  body:
    font: Arial
    size: 11
  heading:
    font: Arial
  code:
    font: Courier New
    size: 9
```

Todos os campos são opcionais. Sem arquivo YAML, o DocFlow utiliza valores padrão e preserva o fluxo simples da v0.1.0.

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
│       └── exporters/
│           └── docx.py
├── tests/
└── examples/
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A evolução prevista inclui templates DOCX, presets, sumário, PDF, HTML e pipeline de publicação.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
