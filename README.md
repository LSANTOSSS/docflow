# DocFlow

**Document automation from Markdown, built as a clean-room portfolio project.**

O DocFlow é uma CLI em Python para transformar documentos Markdown em artefatos de entrega, começando por **DOCX**.

Este projeto complementa o [SAF — System Analysis Framework](https://github.com/LSANTOSSS/SAF): enquanto o SAF demonstra análise e Engenharia de Requisitos, o DocFlow demonstra **automação, desenvolvimento, testes e tooling**.

## v0.3.0 — em desenvolvimento

A v0.3.0 introduz a camada de templates e estrutura documental sem quebrar o fluxo simples das versões anteriores.

Na primeira rodada desta versão, o DocFlow passa a oferecer:

- presets públicos de documento (`report` e `specification`);
- validação de seções obrigatórias;
- suporte a um arquivo DOCX-base informado por configuração;
- resolução de caminhos de template relativa ao arquivo YAML;
- possibilidade de sobrescrever valores herdados de um preset;
- compatibilidade com exportação sem configuração.

O template DOCX de referência versionado e o sumário ficam para a segunda rodada da v0.3.0.

## Uso básico

```bash
docflow export examples/sample.md -o output/sample.docx
```

## Configuração com preset

```yaml
template:
  preset: report

document:
  title: Relatório de Exemplo

styles:
  body:
    size: 12
```

O preset `report` exige uma seção `Resumo`. O preset `specification` exige as seções `Objetivo` e `Requisitos`.

## Configuração com DOCX-base

```yaml
template:
  path: reference.docx
```

Caminhos relativos são resolvidos a partir do diretório do arquivo YAML. O arquivo informado deve existir e usar a extensão `.docx`.

Também é possível combinar preset e template:

```yaml
template:
  preset: specification
  path: reference.docx
```

## Validação estrutural

A configuração também aceita regras explícitas:

```yaml
structure:
  required_headings:
    - Resumo
    - Conclusão
```

Os títulos são comparados sem diferenciar maiúsculas de minúsculas. Se uma seção obrigatória estiver ausente, a exportação é interrompida com uma mensagem clara.

## Suporte acumulado

- títulos Markdown (`#` a `######`);
- parágrafos;
- listas ordenadas e não ordenadas;
- tabelas Markdown;
- blocos de código com linguagem opcional;
- metadados DOCX;
- estilos configuráveis;
- cabeçalho e rodapé;
- configuração YAML;
- presets;
- validação estrutural;
- DOCX-base configurável;
- CLI `docflow export`;
- testes automatizados.

## Instalação local

Requer Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Testes

```bash
pytest
```

## Segurança e origem

O DocFlow é desenvolvido de forma independente para o portfólio pessoal. Não copia código, templates, caminhos, configurações ou artefatos de ambientes corporativos.

## Roadmap

Consulte [`ROADMAP.md`](ROADMAP.md).

## Licença

MIT.
