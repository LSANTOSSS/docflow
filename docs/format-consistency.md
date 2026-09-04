# Consistência entre formatos

A partir da v0.5.0, o DocFlow trata a representação estrutural produzida pelo parser como contrato comum para DOCX, HTML e PDF.

## Estruturas cobertas pelo contrato

Os três exportadores devem preservar, na mesma ordem semântica:

- títulos de níveis 1 a 6;
- parágrafos;
- itens de listas não ordenadas;
- itens de listas ordenadas;
- blocos de código e sua linguagem quando informada;
- tabelas, incluindo cabeçalho e células;
- conteúdo textual principal.

A regressão automatizada exporta a mesma fonte Markdown para os três formatos, lê os artefatos gerados e verifica presença e ordem do conteúdo estrutural comum.

## Diferenças intencionais

Os formatos não precisam ser visualmente idênticos. O contrato exige equivalência estrutural e conteúdo previsível, respeitando as características de cada destino.

- **DOCX:** usa estilos nativos do Word para títulos e listas. A numeração de listas ordenadas é responsabilidade do estilo `List Number`.
- **HTML:** listas consecutivas são agrupadas em um único `<ul>` ou `<ol>`, permitindo que o navegador mantenha a sequência e a semântica HTML.
- **PDF:** listas são materializadas diretamente no conteúdo. Itens ordenados recebem numeração sequencial dentro de cada bloco consecutivo de lista.
- **Código:** DOCX e PDF podem exibir a linguagem como rótulo textual; HTML a representa também pela classe `language-*`.
- **Metadados, cabeçalho e rodapé:** a representação depende das capacidades nativas de cada formato e não faz parte da equivalência visual exata.
- **Sumário:** o DOCX pode usar campo de TOC atualizável pelo editor. Não há exigência de mecanismo idêntico nos demais formatos nesta milestone.

## Regra de evolução

Qualquer alteração em um exportador que mude a preservação de títulos, parágrafos, listas, código ou tabelas deve manter os testes de consistência entre formatos verdes. Diferenças novas e intencionais precisam ser documentadas aqui.
