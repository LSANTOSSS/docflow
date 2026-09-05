# Distribuição e instalação

A v0.7.0 aproxima o DocFlow de uma CLI distribuível sem publicar automaticamente o pacote em um índice público. O objetivo desta etapa é tornar o build reproduzível, validar o wheel em ambiente limpo e documentar um fluxo de instalação previsível.

## Requisitos

- Python 3.11 ou superior;
- `pip` atualizado;
- ambiente virtual recomendado para instalações locais.

## Instalação para desenvolvimento

Na raiz do repositório:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .[dev]
```

Esse modo instala o projeto de forma editável e inclui as ferramentas usadas pela suíte, build e validação de distribuição.

## Gerando o pacote

Com as dependências de desenvolvimento instaladas:

```bash
python -m build
python -m twine check dist/*
```

O build gera, em `dist/`, um source distribution e um wheel. `twine check` valida os metadados antes de qualquer tentativa de publicação.

## Instalação a partir do wheel

Para testar o mesmo artefato que seria distribuído:

```bash
python -m venv .venv-wheel
source .venv-wheel/bin/activate
python -m pip install --upgrade pip
pip install dist/*.whl
docflow --help
```

Depois da instalação, a CLI pode ser usada normalmente:

```bash
docflow validate examples/sample.md -c examples/docflow.yaml
docflow export examples/sample.md -o output/sample.docx -c examples/docflow.yaml
```

## Atualização local

Quando um novo wheel for gerado, a atualização pode ser feita no mesmo ambiente com:

```bash
pip install --upgrade dist/*.whl
```

Para desenvolvimento editável, execute novamente:

```bash
pip install -e .[dev]
```

## Verificação automatizada no CI

O workflow público executa a seguinte sequência:

1. instala as dependências de desenvolvimento;
2. executa a suíte de testes;
3. gera os artefatos DOCX, HTML, PDF e JSON de demonstração;
4. executa `python -m build`;
5. valida o conteúdo de `dist/` com `twine check`;
6. cria um ambiente virtual limpo;
7. instala o wheel produzido naquele run;
8. executa a CLI instalada e valida o exemplo público;
9. publica os artefatos documentais e de distribuição no próprio workflow.

Assim, o editable install não é usado como evidência suficiente de distribuição: o wheel precisa ser instalável e executável isoladamente.

## Publicação em índice de pacotes

A v0.7.0 prepara o DocFlow para distribuição, mas não publica automaticamente em PyPI ou outro índice. Publicação externa exige uma decisão separada sobre nome definitivo do pacote, credenciais, política de release e governança dos artefatos.
