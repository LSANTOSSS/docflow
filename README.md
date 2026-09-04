# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega configuráveis, validáveis e reproduzíveis.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## v0.4.0 — Multi-format

A v0.4.0 fecha o primeiro ciclo multi-format do projeto. A mesma fonte Markdown pode ser validada e exportada para **DOCX, HTML ou PDF**.

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

PDF:

```bash
docflow export examples/sample.md -o output/sample.pdf -c examples/docflow.yaml
```

A exportação PDF é gerada diretamente em Python com ReportLab. O exportador cobre títulos, parágrafos, listas, tabelas, blocos de código e metadados básicos, além de cabeçalho e rodapé quando configurados.

## Validação e relatório

```bash
docflow validate examples/sample.md -c examples/docflow.yaml
```

Para persistir o resultado em JSON:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml --report output/validation.json
```

O relatório registra validade estrutural, títulos encontrados, seções obrigatórias ausentes e contagem dos blocos reconhecidos pelo parser.

## Pipeline

O workflow em `.github/workflows/ci.yml` executa a suíte de testes e gera automaticamente quatro artefatos de demonstração:

- `sample.docx`;
- `sample.html`;
- `sample.pdf`;
- `validation.json`.

Isso mantém o exemplo público verificável e demonstra o pipeline multi-format sem depender de ambiente corporativo.

## Recursos disponíveis

- títulos Markdown (`#` a `######`);
- parágrafos e listas;
- tabelas Markdown;
- blocos de código com linguagem opcional;
- metadados e estilos configuráveis;
- cabeçalho e rodapé;
- configuração YAML;
- DOCX-base configurável;
- presets `report` e `specification`;
- validação de títulos obrigatórios;
- sumário DOCX opcional;
- exportação DOCX, HTML e PDF;
- relatório JSON de validação;
- CI com geração de artefatos;
- testes automatizados.

## Testes

```bash
pytest
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A v0.4.0 conclui o roadmap funcional inicial. Próximas evoluções podem aprofundar fidelidade visual entre formatos, distribuição empacotada, templates adicionais e novas validações.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
