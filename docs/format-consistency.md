# Consistência entre formatos

A partir da v0.5.0, o DocFlow trata a representação estrutural produzida pelo parser como contrato comum para DOCX, HTML e PDF. A milestone também alinha a tipografia configurável básica para reduzir diferenças visuais evitáveis entre os exportadores.

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

## Fidelidade visual comum

Os estilos configuráveis abaixo passam a ter interpretação equivalente nos três exportadores:

- `styles.body.font` e `styles.body.size` definem a tipografia do corpo;
- `styles.heading.font` define a família dos títulos;
- `styles.heading.size` define o tamanho-base do H1, com redução progressiva e previsível até H6;
- `styles.code.font` e `styles.code.size` definem a tipografia dos blocos de código.

O valor padrão de `styles.heading.size` é `18`. A escala de títulos reduz 1,3 pt por nível e respeita piso de 12 pt. Essa regra é aplicada por DOCX, HTML e PDF.

A fidelidade buscada é de **hierarquia, tipografia configurada e estrutura**, não de renderização pixel a pixel. Word, navegadores e ReportLab possuem mecanismos de layout distintos.

## Diferenças intencionais

- **DOCX:** usa estilos nativos do Word para títulos e listas. A numeração de listas ordenadas é responsabilidade do estilo `List Number`.
- **HTML:** listas consecutivas são agrupadas em um único `<ul>` ou `<ol>`, permitindo que o navegador mantenha a sequência e a semântica HTML.
- **PDF:** listas são materializadas diretamente no conteúdo. Itens ordenados recebem numeração sequencial dentro de cada bloco consecutivo de lista.
- **Fontes no PDF:** famílias configuradas são mapeadas para fontes base equivalentes do ReportLab quando necessário; por exemplo, Arial/Calibri → Helvetica e Times New Roman → Times-Roman.
- **Código:** DOCX e PDF podem exibir a linguagem como rótulo textual; HTML a representa também pela classe `language-*`.
- **Metadados, cabeçalho e rodapé:** a representação depende das capacidades nativas de cada formato e não faz parte da equivalência visual exata.
- **Sumário:** o DOCX pode usar campo de TOC atualizável pelo editor. Não há exigência de mecanismo idêntico nos demais formatos nesta milestone.
- **Paginação e quebras:** continuam específicas de cada mecanismo de renderização.

## Regra de evolução

Qualquer alteração em um exportador que mude a preservação de títulos, parágrafos, listas, código, tabelas ou a interpretação da tipografia comum deve manter os testes de consistência entre formatos verdes. Diferenças novas e intencionais precisam ser documentadas aqui.
