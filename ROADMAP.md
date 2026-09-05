# Roadmap — DocFlow

O roadmap organiza a evolução do DocFlow até a primeira versão estável da CLI. Cada milestone deve preservar compatibilidade com o fluxo público existente, incluir testes e manter a documentação alinhada ao comportamento real da ferramenta.

## v0.1.0 — Foundation

- [x] CLI em Python
- [x] Validação de entrada
- [x] Parser estrutural de Markdown
- [x] Exportação DOCX
- [x] Testes
- [x] Exemplo público

## v0.2.0 — Document Styling

- [x] estilos configuráveis;
- [x] metadados do documento;
- [x] tabelas Markdown;
- [x] melhor tratamento de código;
- [x] cabeçalho e rodapé;
- [x] configuração por arquivo YAML.

## v0.3.0 — Templates

- [x] template DOCX de referência;
- [x] presets de documentos;
- [x] validação de estrutura;
- [x] sumário.

## v0.4.0 — Multi-format

- [x] PDF;
- [x] HTML;
- [x] pipeline de publicação;
- [x] relatório de validação.

### Entregas da v0.4.0

- [x] exportação DOCX, HTML e PDF pela mesma CLI;
- [x] comando `docflow validate`;
- [x] relatório JSON opcional de validação;
- [x] geração PDF direta em Python com ReportLab;
- [x] workflow de CI com testes e geração dos três formatos;
- [x] artefatos de exemplo publicados pelo pipeline;
- [x] exemplo público compatível com o preset `report`.

## v0.5.0 — Quality & Validation

**Objetivo:** fortalecer a qualidade dos artefatos existentes antes de ampliar a biblioteca e a distribuição da ferramenta.

- [x] melhorar a fidelidade visual entre DOCX, HTML e PDF;
- [x] definir um conjunto comum de estruturas que devem manter comportamento equivalente entre exportadores;
- [x] ampliar as validações estruturais;
- [x] enriquecer o relatório JSON com resultados acionáveis;
- [x] adicionar testes de regressão para os três formatos;
- [x] documentar diferenças intencionais entre exportadores.

### Critério de saída

A mesma entrada de demonstração deve poder ser validada e exportada para DOCX, HTML e PDF com estrutura previsível, testes automatizados e diferenças conhecidas documentadas.

## v0.6.0 — Template Library

**Objetivo:** ampliar a reutilização do DocFlow sem acoplar conteúdo a um único modelo documental.

- [x] adicionar novos presets de documentos;
- [x] evoluir a composição e reutilização de configurações;
- [x] ampliar exemplos públicos de templates;
- [x] validar requisitos estruturais específicos por preset;
- [x] documentar criação e customização de templates.

### Critério de saída

O usuário deve conseguir selecionar ou adaptar modelos para diferentes tipos de documento mantendo o Markdown como fonte principal.

## v0.7.0 — Distribution

**Objetivo:** tornar a instalação e o consumo da CLI mais próximos de uma ferramenta distribuível.

- [x] revisar metadados e estrutura de empacotamento Python;
- [x] validar instalação em ambiente limpo;
- [x] definir fluxo de build do pacote;
- [x] automatizar verificações de distribuição no CI;
- [x] documentar instalação, atualização e execução da CLI.

### Critério de saída

O DocFlow deve possuir um pacote reproduzível, instalável em ambiente limpo e validado automaticamente antes de uma publicação.

## v1.0.0 — Stable CLI

**Objetivo:** encerrar o ciclo inicial com uma interface pública estável e uma experiência completa de uso.

- [ ] revisar e estabilizar comandos e opções públicas da CLI;
- [ ] consolidar tratamento de erros e mensagens ao usuário;
- [ ] executar testes end-to-end do fluxo validar → exportar;
- [ ] revisar README, exemplos, changelog e documentação de uso;
- [ ] definir política básica de compatibilidade para versões 1.x;
- [ ] publicar a primeira release estável.

### Critério de saída

Um novo usuário deve conseguir instalar, configurar, validar e exportar documentos utilizando apenas a documentação pública, com CI verde e comportamento da CLI coberto por testes.

## Princípios de evolução

- uma única fonte Markdown deve continuar atendendo todos os formatos suportados;
- diferenças entre exportadores devem ser intencionais e documentadas;
- nenhuma milestone é concluída sem testes automatizados correspondentes;
- exemplos públicos devem permanecer executáveis pelo pipeline;
- novas funcionalidades não devem comprometer o caráter clean-room e independente do projeto.
