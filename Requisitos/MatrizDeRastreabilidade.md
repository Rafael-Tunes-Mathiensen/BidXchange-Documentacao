# Matriz de rastreabilidade do BidXchange

O catálogo e os fluxos partem da documentação na revisão `59ae22d`. A [versão 2.0.0][base] é a referência histórica do produto. O código e os cenários apontados nesta matriz usam a revisão [`34853e0`][current] da `develop`, que acrescentou testes dedicados. As referências ao código e aos logs exigem acesso ao repositório do projeto.

Consulte os [requisitos funcionais](RequisitosFuncionais.docx), os [requisitos não funcionais](RequisitosNaoFuncionais.docx), o [registro de elicitação](ElicitacaoRequisitos.docx), os [fluxos de eventos](../CasosDeUso/FluxoDeEventosBxcCompleto.docx), a [monografia](../Monografia/Monografia_BidXchange.docx) e as [fichas dos casos de teste](../CasosDeTeste/CasosDeTeste.docx).

## Critérios de situação

| Critério | Evidência mínima |
| --- | --- |
| Implementado integralmente | O comportamento previsto está disponível para o ator correto na revisão indicada, com as condições e restrições do catálogo. |
| Implementado parcialmente | Uma parte utilizável está disponível. A matriz identifica a parte ausente do escopo documentado. |
| Pendente | O fluxo principal definido no requisito está indisponível ao ator previsto, ou a função prevista ainda não foi implementada. |
| Observado | Comportamento existente que ainda carece de requisito correspondente no catálogo. Consulte o inventário do Apêndice I. |
| Testado | Há cenário, revisão e resultado identificáveis. O resultado vale para as condições verificadas, inclusive quando o teste confirma uma ausência esperada. |
| Demonstrado | Há registro do percurso apresentado, com identificação da tela, do cenário e da versão quando disponível. Capturas isoladas demonstram somente o estado mostrado. |
| Validado por usuário | Há participante ou perfil, procedimento, critério de aceitação e resultado registrados. As entrevistas de elicitação documentam necessidades, sem estabelecer aceitação das funcionalidades. |
| Medido em operação | Há indicador, método, ambiente, período ou amostra e resultado observados em operação. Metas sem apuração ficam sem medição. |

A coluna **Situação técnica** trata da implementação. As demais evidências se aplicam por cenário e podem coexistir. A coluna de verificação distingue testes identificados de inspeções e passos a executar. Não foi localizada evidência suficiente de validação do fluxo completo por usuário ou de medição em operação. A [monografia](../Monografia/Monografia_BidXchange.docx) apresenta telas e a trilha técnica do percurso de cotação, envio, comparação e seleção.

## Requisitos funcionais

| ID | Requisito | Caso de uso | Situação técnica | Evidência de código | Teste ou verificação |
| --- | --- | --- | --- | --- | --- |
| RF01 | Cadastro de instituição ou fornecedor | CU06 | Implementado integralmente | [Formulário][signup-form] e [registro][registration]. Fornecedor deve informar categoria ativa ou marcar **Outros**. | [Criação e confirmação de e-mail][signup-test], [categoria obrigatória][category-signup-test] e [endereço normalizado][address-test]. |
| RF02 | Autenticação por e-mail | CU07 | Implementado integralmente | [Login com limitação de tentativas][login] e [rotas de autenticação][account-urls]. | [Redirecionamento por perfil][login-test] e [limitação após falhas de autenticação][login-limit-test]. |
| RF03 | Criação e publicação de cotação | CU12 | Implementado integralmente | [Formulário de cotação][quote-form] e [serviço de criação][quote-create]. | [Publicação][quote-create-test], [rascunho][quote-draft-test] e [prazo mínimo][quote-form-test]. |
| RF04 | Edição de cotação | CU13 | Implementado parcialmente | [Busca do rascunho editável][quote-draft] e [serviço de atualização][quote-update]. | [Edição de rascunho][quote-update-test]. A edição de cotação já publicada permanece pendente. |
| RF05 | Consulta de cotações | CU11 | Implementado parcialmente | [Listagem e acesso por organização][quote-list]. | [Listagem isolada da instituição][rf05-test] e [paginação][quote-list-test]. O histórico integral previsto na origem permanece pendente. |
| RF06 | Visualização de cotações disponíveis | CU11 | Implementado integralmente | [Listagem de cotações abertas no prazo][quote-list]. | [Teste dedicado de oportunidades abertas, no prazo e de instituições ativas][rf06-test]. |
| RF07 | Envio e atualização de proposta | CU09 | Implementado parcialmente | [Formulário][proposal-form] e [submissão transacional][submit]. | [Valor e histórico][submit-test] e [revalidação após bloqueio][revalidation-test]. [Filtro fiscal na comparação][invoice-test]. O envio aceita Sim ou Não. A confirmação positiva exigida no [requisito de origem][rf-origem] não é condição obrigatória de envio. O filtro opera sobre a declaração e a validade do documento fiscal não é verificada. |
| RF08 | Comparação de propostas | CU16 | Implementado integralmente | [Comparador][compare] e [ranking e elegibilidade][rank]. | [Uso dos critérios salvos][rank-test] e [teto de valor][max-amount-test]. A recomendação apoia a escolha humana. |
| RF09 | Consulta de propostas próprias | CU08 | Implementado parcialmente | [Listagem e acesso ao detalhe][proposal-list]. | [Teste dedicado de propostas próprias e versões atuais][rf09-test] e [paginação][proposal-list-test]. A consulta individual de propostas concorrentes permanece sujeita à definição de escopo. |
| RF10 | Seleção da proposta vencedora | CU15 | Implementado integralmente | [Confirmação da seleção][selection-view] e [serviço de decisão][selection]. | [Jornada de seleção e conversa][flow-test] e [revalidação concorrente][selection-test]. |
| RF11 | Encerramento manual sem escolha | CU14 | Implementado integralmente | [Ação de encerramento][close-view] e [serviço][close-service]. | [Testes dedicados][rf11-test] cobrem encerramento com auditoria, bloqueio de novos envios, rascunho cancelado e restrições por papel ou organização. |
| RF12 | Encerramento automático da cotação | — | Pendente | [Janela de recebimento][quote-window] e [seleção por estado][selection]. Ao vencer o prazo, a cotação pode continuar em estado aberto. | [Bloqueio de novo envio vencido][expired-test]. A transição automática após 30 dias, prevista na origem, ainda precisa de implementação e teste. |
| RF13 | Ativação e desativação de contas | CU02 | Pendente | [Cadastro dos modelos no Django Admin][admin-registry] e [rotas efetivas][root-urls]. | [Ausência da rota para visitante, usuário comum e staff][admin-route-test]. A interface web para mudar o estado da conta continua pendente. |
| RF14 | Registro de chamado de suporte | CU19 | Implementado parcialmente | [Área autenticada de suporte][support-view] e [criação de chamado][support-create]. | [Acesso autenticado][support-auth-test], [pedido de categoria][category-request-test] e [rollback do chamado][support-atomic-test]. O anexo opcional permanece pendente na criação. |
| RF15 | Gestão de chamados de suporte | CU23 | Implementado integralmente | [Fila e resposta administrativa][support-admin]. | [Resposta registrada e enviada][support-answer-test] e [análise de nova categoria][category-approve-test]. |
| RF16 | Registro de avaliação de fornecedor | CU17 | Implementado integralmente | [Formulário de avaliação][ratings] e [gravação da avaliação][review-save]. | [Testes dedicados][rf16-test] cobrem registro e edição, rejeição de nota fora de 1 a 5, papel sem permissão e cotação sem vencedora. |
| RF17 | Consulta de avaliações recebidas | CU18 | Pendente | [View com ramo de fornecedor][ratings] e [rotas do fornecedor][supplier-urls] sem entrada para avaliações. | Inspeção de rotas. Teste positivo da consulta do fornecedor pendente até a jornada estar disponível. |
| RF18 | Gestão de membros da organização | CU20 | Implementado integralmente | [Gestão da equipe][team] e [aceite de convite][account-urls]. | [Convite e aceite][team-test] e [restrição por papel][team-denied-test]. O código também oferece gestão de equipes de fornecedores. |
| RF19 | Votação interna sobre propostas | CU24 | Implementado parcialmente | [Criação, participantes e voto][poll-service]. | [Votação na jornada integrada][flow-test] e [opções distintas][poll-test]. A priorização de cotações como finalidade própria ainda depende de definição. |
| RF20 | Gestão de fornecedores favoritos | CU21 | Implementado integralmente | [Inclusão e remoção][favorites-service] e [consulta de favoritos][favorites-list]. | [Inclusão e acesso por perfil][rf20-test], [remoção registrada em auditoria][favorite-test] e [isolamento por instituição][favorite-isolation-test]. |
| RF21 | Geração de relatórios administrativos | CU03 | Implementado parcialmente | [Indicadores administrativos calculados na consulta][report]. O indicador de cotações abertas conta pelo estado, incluindo as vencidas ainda abertas. | [Teste dedicado dos indicadores atuais][rf21-test]. Geração de relatórios por filtros segue pendente. |
| RF22 | Consulta de relatórios anteriores | CU04 | Pendente | [Rotas administrativas][product-urls] e [consulta de indicadores atuais][report]. | Inspeção da rota e do serviço. Recuperação de relatório persistido a validar quando houver implementação. |
| RF23 | Exportação de relatórios | CU05 | Pendente | [Rotas administrativas][product-urls]. | Inspeção das rotas. Formato, geração e teste de download ainda dependem de definição. |
| RF24 | Consulta administrativa de usuários | CU01 | Pendente | [Cadastros internos][admin-registry], [rotas raiz][root-urls] e [rotas administrativas][product-urls]. | [Ausência do Django Admin pela web][admin-route-test]. Busca e histórico unificado pela interface seguem pendentes. |
| RF25 | Conversar após a seleção | CU25 | Implementado integralmente | [Abertura da conversa na seleção][selection] e [acesso e envio de mensagens][chat]. | [Envio e notificação à contraparte][chat-test] e [bloqueio de outra organização][chat-isolation-test]. |
| RF26 | Consultar e gerenciar notificações | CU26 | Implementado integralmente | [Caixa de notificações e ações de leitura][notifications] e [escopo por usuário e organização ativa][notification-scope]. | [Leitura por POST][notification-test], [isolamento][notification-isolation-test] e [paginação e escopo][notification-list-test]. |
| RF27 | Recuperação e alteração de senha | CU27 | Implementado integralmente | [Rotas de redefinição e troca][account-urls]. | [Envio, resposta neutra e limite no reset][reset-test]. [Testes dedicados de troca com senha atual][rf27-test]. |
| RF28 | Perfil da organização | CU28 | Implementado integralmente | [Consulta e edição de perfil][profile]. | [Campos somente leitura para membros sem papel de proprietário][profile-test] e [edição de endereço][profile-address-test]. |
| RF29 | Categorias de atuação do fornecedor | CU29 | Implementado integralmente | [Cadastro][signup-form], [perfil][profile] (categoria ativa ou opção **Outros**) e [gestão administrativa do pedido][support-admin]. | [Categorias no cadastro e perfil][supplier-category-test] e [pedido e decisão da equipe][category-approve-test]. |
| RF30 | Preenchimento de endereço por CEP | CU06 | Implementado integralmente | [Rota de consulta por CEP][account-urls] e [formulário][signup-form]. | [Resposta normalizada e preenchimento manual no caso de falha][cep-test]. Os cenários usam resposta simulada do serviço. |
| RF31 | Troca de organização ativa | CU30 | Implementado integralmente | [Ação de troca da organização ativa][switch]. | [Troca e persistência entre páginas][switch-test]. |

## Requisitos não funcionais

Os casos de uso desta seção indicam jornadas úteis para verificar o requisito. Requisitos transversais podem atingir outras jornadas.

| ID | Requisito | Jornadas relacionadas | Estado ou evidência | Teste ou verificação |
| --- | --- | --- | --- | --- |
| RNF01 | Atualizar proposta em até 1 segundo | CU09, CU16, CU26 | Sem medição. O código [notifica a instituição][submit] e [publica após o commit][realtime]. | [Testes de WebSocket][realtime-test] e [atualização de interface][realtime-ui-test] cobrem mecanismos. Medir do commit até a atualização visível com o ambiente e o transporte registrados. |
| RNF02 | Avisar sobre nova cotação em até 30 segundos | CU11, CU12, CU13 | Sem medição. [Criação publicada][quote-create] e [publicação de rascunho][quote-update] emitem evento para fornecedores quando habilitado. | [Publicação após commit][quote-event-test]. Medir a entrega na interface. O fluxo observado de publicação não envia e-mail. |
| RNF03 | Armazenar senhas com PBKDF2 SHA-256 e sal | CU06, CU07 | Uso da [API de senha no cadastro][registration] e da [redefinição do Django][account-urls]. | [Armazenamento com hash][password-test] e [teste dedicado PBKDF2 com sal][rnf03-test]. Conferir o identificador do algoritmo após cadastro e redefinição em ambiente controlado. |
| RNF04 | Rastrear interações relevantes | CU09, CU12, CU14, CU15, CU24 | Parcial. [Serviço de auditoria][audit] registra eventos selecionados. | [Auditoria da seleção na jornada][flow-test] e [rollback do envio][proposal-atomic-test]. Consolidar o catálogo de eventos que devem ser auditados. |
| RNF05 | Manter disponibilidade mensal de 99,9% | Transversal | Sem medição. Há [endpoint de saúde][health]. | [Resposta do endpoint][health-test]. Apurar série de monitoramento externo e janela de indisponibilidade mensal. |
| RNF06 | Adaptar a interface a diferentes larguras | CU06, CU09, CU12, CU16 | Estilos responsivos presentes. Cobertura integral de navegador, dispositivo e jornada a verificar. | [Assistente de proposta][proposal-ui-test] e [estrutura de estilos][bootstrap]. Executar matriz de larguras, navegadores e interações. |
| RNF07 | Executar backup horário redundante e reter por 30 dias | Transversal | Sem evidência operacional. O [guia de banco][database] orienta definir e testar a rotina no provedor. | Conferir agendamento, retenção, redundância e restauração com evidência do ambiente aplicável. |
| RNF08 | Manter o processamento financeiro externo | CU09, CU15, CU25 | Condições comerciais, seleção e conversa registradas. O [escopo do produto][product] e o [formulário da proposta][proposal-form] descrevem a jornada observada. | [Jornada de cotação a conversa][flow-test] e inspeção das rotas e integrações da revisão. |

### Configuração de tempo real

Para RNF01 e RNF02, a [configuração versionada][settings] habilita o tempo real por padrão em desenvolvimento. Em Preview e Production, a opção vem desabilitada por padrão. Com a opção ligada e sem `REDIS_URL`, o código seleciona a camada em memória. A revisão local de 8 nov. registrou uma diferença em relação às restrições descritas no [guia de implantação][deploy]. A configuração em operação e as latências continuam a verificar. Consulte os [requisitos não funcionais](RequisitosNaoFuncionais.docx) e a [viabilidade técnica](../Viabilidades/ViabilidadeTecnica.docx).

## Correspondência com o histórico

| Identificador na documentação anterior | Referência no catálogo atual |
| --- | --- |
| CU09 Participar de cotação e CU09 Enviar proposta | CU09 Enviar ou atualizar proposta, vinculado ao RF07. O RF08 corresponde à comparação. |
| CU12 Abrir cotação | CU12 Criar ou publicar cotação. |
| Segunda ocorrência de CU12 para edição de cotação | CU13 Editar rascunho de cotação. A edição de cotação publicada permanece como lacuna do RF04. |
| CU10 | Sem registro identificado. O [fluxo histórico de eventos][fluxo-historico] contém dois títulos CU09 e nenhum CU10. O identificador foi preservado como lacuna do histórico. |
| CU21 Favoritar fornecedor e CU22 Desfavoritar fornecedor | CU21 Gerenciar fornecedores favoritos. |
| CU03 Geração de relatórios | CU03 Consultar indicadores. Relatórios com filtros permanecem no escopo pretendido do RF21. |
| Chat e notificações registrados como comportamentos associados | RF25/CU25 e RF26/CU26 documentam jornadas próprias da versão analisada. |

Os rótulos históricos estão no [commit de origem][historico]. Aprovações institucionais permanecem dependentes dos registros da instituição.

## Evidências de execução

- [Harness CI #289][ci289], em 3 nov. 2026, revisão `1aa8783`. O workflow passou com 327 testes Django por versão de Python e 67 testes JavaScript.
- [Harness CI #293][ci293], em 11 nov. 2026, revisão `34853e0`. O workflow passou com 348 testes Django por versão de Python e 67 testes JavaScript. Os cenários dedicados de RF11 e RF16 pertencem a esta revisão.

O [registro de evidências do gate](EvidenciasGateTestes.md) detalha ambientes, resultados e logs das duas execuções. O registro histórico do cartão 068 relata uma execução local de `quick` e `full` em 8 nov. 2026, na revisão `1aa8783`, com Django 6.1.1 e PostgreSQL 18 isolado, com 327 testes Django e 67 JavaScript no perfil completo.

Os resultados são técnicos e limitados às verificações executadas. O RF07 cobre persistência e histórico da proposta e o filtro fiscal no ranking, com a confirmação positiva no envio ainda parcial. A ausência das telas de RF13, RF17 e RF24 faz parte das lacunas da versão. O percurso principal é executável sob as condições testadas. Teste em navegador real, cobertura percentual, desempenho e validação por usuário do percurso como um todo seguem sem evidência nesses gates.

[current]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/commit/34853e0be3e2a69a70e77c2596657f6cd548a64d
[ci289]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701
[ci293]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343
[settings]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/config/settings.py#L166
[deploy]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/docs/VERCEL_DEPLOY.md
[historico]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange-Documentacao/tree/a40888869eeb
[rf-origem]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange-Documentacao/blob/a40888869eeb/Requisitos/RequisitosFuncionais.docx
[supplier-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/supplier_urls.py
[rf05-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L24
[rf06-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L52
[rf09-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L96
[rf11-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L133
[rf16-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L207
[rf21-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L274
[rf27-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L300
[rf20-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L342
[rnf03-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_requirements_coverage.py#L375
[invoice-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_decision_criteria.py#L144
[reset-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_transactional_emails.py#L21
[profile]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/profile.py
[profile-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/account/test_team_management.py#L288
[profile-address-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_addresses.py#L62
[supplier-category-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_supplier_categories.py
[cep-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_addresses.py#L109
[switch]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/account.py#L11
[switch-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/account/test_team_management.py#L155
[base]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/commit/1aa8783ff1d9ada526b765f3a04bc6244106cbea
[signup-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/forms.py#L167
[registration]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/services/registration.py
[signup-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_signup.py#L63
[category-signup-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_supplier_categories.py#L56
[address-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_addresses.py#L19
[login]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/auth_views.py#L44
[account-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/urls.py
[login-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_dashboard.py#L176
[login-limit-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_login_security.py#L21
[quote-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/forms/quotes.py
[quote-create]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/quotes.py#L35
[quote-create-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_wizard.py#L238
[quote-draft-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_wizard.py#L361
[quote-form-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_forms.py#L41
[quote-draft]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/quotes.py#L122
[quote-update]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/quotes.py#L66
[quote-update-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_wizard.py#L413
[quote-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/quotes.py#L39
[quote-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_pagination.py#L107
[expired-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_views.py#L452
[proposal-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/forms/proposals.py
[submit]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/proposals.py#L284
[submit-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_views.py#L115
[revalidation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_service_transactions.py#L237
[compare]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/proposals.py#L218
[rank]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/proposals.py#L136
[rank-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_decision_criteria.py#L150
[max-amount-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_decision_criteria.py#L166
[proposal-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/proposals.py#L27
[proposal-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_pagination.py#L132
[selection-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/proposals.py#L349
[selection]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/proposals.py#L344
[flow-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/proposals/test_flow.py#L169
[selection-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_service_transactions.py#L159
[close-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/quotes.py#L385
[close-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/quotes.py#L106
[quote-window]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/models/quotes.py#L147
[admin-registry]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/admin.py
[root-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/config/urls.py
[admin-route-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_views.py#L57
[support-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/core.py#L105
[support-create]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/core.py#L37
[support-auth-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_views.py#L185
[category-request-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_category_requests.py#L76
[support-atomic-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_service_workflows.py#L18
[support-admin]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/system_admin.py
[support-answer-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_category_requests.py#L270
[category-approve-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_category_requests.py#L138
[ratings]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/proposal_review.py
[review-save]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/proposals.py#L442
[team]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/team.py
[team-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/account/test_team_management.py#L357
[team-denied-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/account/test_team_management.py#L240
[poll-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/quotes.py#L183
[poll-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_poll_options.py#L180
[favorites-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/quotes.py#L140
[favorites-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/quotes.py#L22
[favorite-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_engagement_views.py#L125
[favorite-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/quotes/test_engagement_views.py#L160
[report]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/core.py#L181
[product-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/urls.py#L57
[chat]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/chat.py
[chat-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/chat/test_views.py#L103
[chat-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/chat/test_views.py#L149
[notifications]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/views/core.py#L38
[notification-scope]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/selectors/core.py#L141
[notification-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_notification_read.py#L80
[notification-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_notification_read.py#L92
[notification-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_pagination.py#L148
[realtime]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/realtime.py
[realtime-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_realtime.py
[realtime-ui-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/js/realtime.test.cjs
[quote-event-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_service_transactions.py#L302
[password-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/tests/test_models.py#L29
[audit]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/services/audit.py
[proposal-atomic-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/test_service_transactions.py#L216
[health]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/accounts/public_views.py#L90
[health-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/core/test_views.py#L136
[proposal-ui-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/bidxchange/tests/js/proposal_wizard.test.cjs
[bootstrap]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/frontend/ui/bootstrap.scss
[database]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/docs/DATABASE.md
[product]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0/PRODUCT.md
[fluxo-historico]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange-Documentacao/blob/b925515eebb8bfd529b9396a6bafe03f3f0e6261/CasosDeUso/FluxoDeEventosBxcCompleto.docx
