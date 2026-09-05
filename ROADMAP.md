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

## v0.5.0 — Quality & Validation

- [x] melhorar a fidelidade visual entre DOCX, HTML e PDF;
- [x] definir um conjunto comum de estruturas que devem manter comportamento equivalente entre exportadores;
- [x] ampliar as validações estruturais;
- [x] enriquecer o relatório JSON com resultados acionáveis;
- [x] adicionar testes de regressão para os três formatos;
- [x] documentar diferenças intencionais entre exportadores.

## v0.6.0 — Template Library

- [x] adicionar novos presets de documentos;
- [x] evoluir a composição e reutilização de configurações;
- [x] ampliar exemplos públicos de templates;
- [x] validar requisitos estruturais específicos por preset;
- [x] documentar criação e customização de templates.

## v0.7.0 — Distribution

- [x] revisar metadados e estrutura de empacotamento Python;
- [x] validar instalação em ambiente limpo;
- [x] definir fluxo de build do pacote;
- [x] automatizar verificações de distribuição no CI;
- [x] documentar instalação, atualização e execução da CLI.

## v1.0.0 — Stable CLI

**Objetivo:** encerrar o ciclo inicial com uma interface pública estável e uma experiência completa de uso.

- [x] revisar e estabilizar comandos e opções públicas da CLI;
- [x] consolidar tratamento de erros e mensagens ao usuário;
- [x] executar testes end-to-end do fluxo validar → exportar;
- [x] revisar README, exemplos, changelog e documentação de uso;
- [x] definir política básica de compatibilidade para versões 1.x;
- [ ] publicar a primeira GitHub Release estável.

### Critério de saída funcional

Um novo usuário deve conseguir instalar, configurar, validar e exportar documentos utilizando apenas a documentação pública, com CI verde e comportamento da CLI coberto por testes. A publicação da GitHub Release é o único passo externo ao código quando a conexão disponível não expõe escrita de Tag/Release.

## Estado após v1.0.0

A linha inicial do roadmap está funcionalmente concluída. Evoluções futuras devem entrar como manutenção compatível 1.x ou como uma nova major quando exigirem quebra deliberada da interface pública.

## Princípios de evolução

- uma única fonte Markdown deve continuar atendendo todos os formatos suportados;
- diferenças entre exportadores devem ser intencionais e documentadas;
- nenhuma milestone funcional é concluída sem testes automatizados correspondentes;
- exemplos públicos devem permanecer executáveis pelo pipeline;
- novas funcionalidades não devem comprometer o caráter clean-room e independente do projeto.
