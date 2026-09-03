# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega, começando por **DOCX**.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## Estado atual

A v0.1.0 estabeleceu o fluxo funcional de Markdown até DOCX. A v0.2.0 está em desenvolvimento e adiciona configuração documental sem quebrar o uso básico da versão anterior.

```text
Markdown
   ↓
Validação
   ↓
Parser estrutural
   ↓
Configuração YAML (opcional)
   ↓
Exportador DOCX
   ↓
Documento gerado
```

### Suporte atual

- títulos Markdown (`#` a `######`);
- parágrafos;
- listas não ordenadas e ordenadas;
- blocos de código cercados por ```;
- validação de arquivo de entrada;
- CLI `docflow export`;
- configuração YAML opcional;
- metadados DOCX (`title`, `author`, `subject`, `keywords`);
- fonte e tamanho do corpo configuráveis;
- fonte de títulos e de código configurável;
- testes automatizados.

## Instalação local

Requer Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Uso

Compatível com a v0.1.0:

```bash
docflow export examples/sample.md -o output/sample.docx
```

Com configuração:

```bash
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```

Consulte `examples/docflow.yaml` para um exemplo de metadados e estilos.

## Testes

```bash
pytest
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

A v0.2.0 continuará com tabelas Markdown, melhor tratamento de código e cabeçalho/rodapé.

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
