# Compatibilidade da linha 1.x

A v1.0.0 estabelece a primeira interface pública estável do DocFlow.

## Superfície pública estável

Durante a linha 1.x, o projeto pretende preservar sem quebra deliberada:

- o executável `docflow`;
- os comandos `docflow validate` e `docflow export`;
- as opções públicas `-c/--config`, `-o/--output` e `--report`;
- os formatos de saída DOCX, HTML e PDF;
- os presets públicos existentes;
- a semântica de `extends` nos arquivos YAML;
- os campos já publicados no relatório JSON de validação.

Mudanças compatíveis podem adicionar novos comandos, opções, presets, validações opcionais, campos de relatório e capacidades de exportação.

## Mudanças incompatíveis

Uma alteração que remova, renomeie ou mude de forma incompatível uma interface pública acima deve ser reservada para uma nova versão major. Correções de bugs podem ajustar comportamentos que contradigam a documentação, desde que o motivo seja registrado no changelog.

## Dependências e formatos externos

A política não promete renderização pixel a pixel idêntica entre Word, navegador e PDF. As diferenças intencionais entre exportadores continuam documentadas em `docs/format-consistency.md`.

A compatibilidade também não transforma detalhes internos de módulos Python em API pública. A interface suportada para uso externo é a CLI e seus arquivos de configuração documentados.

## Ciclo de manutenção

Versões 1.x devem manter testes automatizados, build de distribuição, validação do wheel em ambiente limpo e atualização do changelog. Antes de uma publicação, o CI precisa permanecer verde.
