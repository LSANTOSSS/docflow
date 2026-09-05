# Changelog

## [1.0.0] — Stable CLI

- Interface pública da CLI consolidada em `docflow validate` e `docflow export`.
- Novo `docflow --version`.
- Mensagens e ajuda da CLI revisadas para os formatos e opções suportados.
- Fluxo end-to-end `validate → export` coberto para DOCX, HTML e PDF.
- README, roadmap e documentação revisados para o estado estável.
- Política de compatibilidade da linha 1.x documentada.
- Versão do pacote e `__version__` consolidadas em 1.0.0.
- Pipeline de distribuição preserva build, `twine check` e instalação limpa do wheel antes de aceitar o artefato.

## [0.7.0] — Distribution

- Metadados de empacotamento Python revisados.
- Build reproduzível de wheel e source distribution com `python -m build`.
- Validação de metadados com `twine check`.
- Instalação do wheel em ambiente virtual limpo no CI.
- Execução da CLI instalada a partir do artefato produzido.
- Artefatos de distribuição publicados pelo GitHub Actions.
- Guia público de instalação, atualização e build em `docs/distribution.md`.

## [0.6.0] — Template Library

- Novos presets públicos `meeting-notes` e `decision-record`.
- Requisitos estruturais específicos por preset.
- Exemplos públicos para os novos modelos.
- Composição e reutilização de configurações YAML com `extends`.
- Herança simples e múltipla com precedência determinística.
- Resolução de caminhos relativos pelo arquivo que os declara e proteção contra ciclos.
- Guia de criação e customização em `docs/templates.md`.

## [0.5.0] — Quality & Validation

- Fidelidade visual aprimorada entre DOCX, HTML e PDF.
- Conjunto comum de estruturas com comportamento equivalente entre exportadores.
- Validações estruturais ampliadas.
- Relatório JSON enriquecido com resultados acionáveis.
- Testes de regressão cobrindo os três formatos.
- Diferenças intencionais entre exportadores documentadas.
- Configuração tipográfica compartilhada para corpo, títulos e blocos de código.
- Escala previsível de títulos H1–H6, respeitando as limitações próprias de cada formato.

## [0.4.0] — Multi-format

- Exportação HTML a partir da mesma estrutura Markdown usada pelo DOCX.
- Exportação PDF direta em Python com ReportLab.
- Novo comando `docflow validate`.
- Relatório JSON opcional com títulos, seções ausentes e contagem de blocos.
- CLI unificada para `.docx`, `.html` e `.pdf`.
- Workflow de GitHub Actions com testes e geração de artefatos de exemplo.
- Exemplo público atualizado e compatível com o preset `report`.
- Cobertura de testes ampliada para HTML, PDF e validação.

## [0.3.0] — Templates

- Suporte a DOCX-base configurável.
- Presets públicos `report` e `specification`.
- Validação estrutural por títulos obrigatórios.
- Caminho de template relativo ao arquivo YAML.
- Sumário DOCX opcional via campo `document.toc`.
- Exemplo público de configuração para v0.3.0.
- Cobertura de testes ampliada para templates e sumário.

## [0.2.0] — Document Styling

- Configuração opcional por arquivo YAML.
- Metadados DOCX configuráveis.
- Estilos configuráveis para corpo, títulos e código.
- Suporte a tabelas Markdown.
- Blocos de código com identificação opcional da linguagem.
- Cabeçalho e rodapé configuráveis.
- Cobertura de testes ampliada.

## [0.1.0] — Foundation

- CLI inicial `docflow export`.
- Validação de arquivos Markdown.
- Parser estrutural para títulos, parágrafos, listas e blocos de código.
- Exportação para DOCX.
- Testes automatizados.
- Exemplo de documento.
- Fundação de governança e roadmap do projeto.
