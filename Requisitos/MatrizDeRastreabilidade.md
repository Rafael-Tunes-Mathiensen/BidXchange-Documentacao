# Matriz de rastreabilidade do BidXchange

Esta matriz relaciona os requisitos acadêmicos e os casos de uso ao código e às verificações da versão 2.0.0. A base técnica é a revisão [`1aa8783ff1d9`][base] da `develop`, com o mesmo conteúdo da tag [`v2.0.0`][release]. As referências ao código e aos testes exigem acesso ao repositório do projeto.

Consulte os [requisitos funcionais](RequisitosFuncionais.docx), os [requisitos não funcionais](RequisitosNaoFuncionais.docx), a [elicitação](ElicitacaoRequisitos.docx), os [fluxos de eventos](../CasosDeUso/FluxoDeEventosBxcCompleto.docx) e o [diagrama](../CasosDeUso/DiagramaCasosDeUso.pdf).

## Como interpretar

- **Atendido** indica que o comportamento descrito corresponde à implementação inspecionada.
- **Parcial** indica que parte do escopo histórico ainda depende de implementação, validação ou decisão.
- **Pendente** indica que a funcionalidade pretendida carece de implementação disponível no escopo indicado. Um teste que demonstra a ausência do fluxo é evidência da pendência.
- **Observado** identifica funcionalidades da versão analisada incorporadas ao catálogo nesta revisão. RF25 e RF26 carecem de prioridade histórica registrada.
- **Sem medição** indica uma meta de qualidade que precisa de evidência operacional. Os testes citados cobrem aspectos específicos de cada requisito.

## Requisitos funcionais

| ID | Requisito | Caso de uso | Estado | Evidência de código | Teste ou verificação |
| --- | --- | --- | --- | --- | --- |
| RF01 | Cadastro de instituição ou fornecedor | CU06 | Atendido | [Formulário][signup-form] e [registro][registration]. Fornecedor deve informar categoria ativa ou marcar **Outros**. | [Criação e confirmação de e-mail][signup-test], [categoria obrigatória][category-signup-test] e [endereço normalizado][address-test]. |
| RF02 | Autenticação por e-mail | CU07 | Atendido | [Login com limitação de tentativas][login] e [rotas de autenticação][account-urls]. | [Redirecionamento por perfil][login-test] e [limitação após falhas de autenticação][login-limit-test]. |
| RF03 | Criação e publicação de cotação | CU12 | Atendido | [Formulário de cotação][quote-form] e [serviço de criação][quote-create]. | [Publicação][quote-create-test], [rascunho][quote-draft-test] e [prazo mínimo][quote-form-test]. |
| RF04 | Edição de cotação | CU13 | Parcial | [Busca do rascunho editável][quote-draft] e [serviço de atualização][quote-update]. | [Edição de rascunho][quote-update-test]. A edição de cotação já publicada permanece pendente. |
| RF05 | Consulta de cotações | CU11 | Parcial | [Listagem e acesso por organização][quote-list]. | [Paginação de cotações][quote-list-test]. O histórico integral previsto na origem permanece pendente. |
| RF06 | Visualização de cotações disponíveis | CU11 | Atendido | [Listagem de cotações abertas no prazo][quote-list]. | Conferir a listagem como fornecedor com cotações abertas, vencidas, encerradas, em rascunho e de instituição inativa. O [teste de envio vencido][expired-test] cobre a restrição na jornada de proposta. |
| RF07 | Envio e atualização de proposta | CU09 | Parcial | [Formulário][proposal-form] e [submissão transacional][submit]. | [Valor e histórico][submit-test] e [revalidação após bloqueio][revalidation-test]. Exigência positiva e verificação da validade fiscal permanecem pendentes no escopo histórico. |
| RF08 | Comparação de propostas | CU16 | Atendido | [Comparador][compare] e [ranking e elegibilidade][rank]. | [Uso dos critérios salvos][rank-test] e [teto de valor][max-amount-test]. A recomendação apoia a escolha humana. |
| RF09 | Consulta de propostas próprias | CU08 | Parcial | [Listagem e acesso ao detalhe][proposal-list]. | [Permissões e paginação][proposal-list-test]. A consulta individual de propostas concorrentes permanece sujeita à definição de escopo. |
| RF10 | Seleção da proposta vencedora | CU15 | Atendido | [Confirmação da seleção][selection-view] e [serviço de decisão][selection]. | [Jornada de seleção e conversa][flow-test] e [revalidação concorrente][selection-test]. |
| RF11 | Encerramento manual sem escolha | CU14 | Atendido | [Ação de encerramento][close-view] e [serviço][close-service]. | Roteiro manual sugerido. Encerrar cotação aberta com papel autorizado e conferir estado sem vencedora. Em rascunho, conferir cancelamento. |
| RF12 | Encerramento automático da cotação | — | Pendente | [Janela de recebimento][quote-window] e [seleção por estado][selection]. Ao vencer o prazo, a cotação pode continuar em estado aberto. | [Bloqueio de novo envio vencido][expired-test]. A transição automática após 30 dias, prevista na origem, ainda precisa de implementação e teste. |
| RF13 | Ativação e desativação de contas | CU02 | Pendente | [Cadastro dos modelos no Django Admin][admin-registry] e [rotas efetivas][root-urls]. | [Ausência da rota administrativa inclusive para superusuário][admin-route-test]. A interface web para mudar o estado da conta continua pendente. |
| RF14 | Registro de chamado de suporte | CU19 | Parcial | [Área autenticada de suporte][support-view] e [criação de chamado][support-create]. | [Acesso autenticado][support-auth-test], [pedido de categoria][category-request-test] e [rollback do chamado][support-atomic-test]. O anexo opcional permanece pendente na criação. |
| RF15 | Gestão de chamados de suporte | CU23 | Atendido | [Fila e resposta administrativa][support-admin]. | [Resposta registrada e enviada][support-answer-test] e [análise de nova categoria][category-approve-test]. |
| RF16 | Registro de avaliação de fornecedor | CU17 | Atendido | [Formulário de avaliação][ratings] e [gravação da avaliação][review-save]. | Roteiro manual sugerido. Avaliar cotação com vencedora, atualizar a nota e conferir a rejeição de notas fora de 1 a 5. |
| RF17 | Consulta de avaliações recebidas | CU18 | Parcial | [Listagem de avaliações por perfil][ratings]. | Roteiro manual sugerido. Abrir avaliações como fornecedor e conferir cotação, nota, data e isolamento. Comentários e média nessa tela permanecem pendentes. |
| RF18 | Gestão de membros da organização | CU20 | Atendido | [Gestão da equipe][team] e [aceite de convite][account-urls]. | [Convite e aceite][team-test] e [restrição por papel][team-denied-test]. O código também oferece gestão de equipes de fornecedores. |
| RF19 | Votação interna sobre propostas | CU24 | Parcial | [Criação, participantes e voto][poll-service]. | [Votação na jornada integrada][flow-test] e [opções distintas][poll-test]. A priorização de cotações como finalidade própria ainda depende de definição. |
| RF20 | Gestão de fornecedores favoritos | CU21 | Atendido | [Inclusão e remoção][favorites-service] e [consulta de favoritos][favorites-list]. | [Remoção registrada em auditoria][favorite-test] e [isolamento por instituição][favorite-isolation-test]. |
| RF21 | Geração de relatórios administrativos | CU03 | Parcial | [Indicadores administrativos calculados na consulta][report]. O indicador de cotações abertas conta pelo estado, incluindo as vencidas ainda abertas. | Roteiro manual sugerido. Abrir indicadores como equipe autorizada e comparar com a base de teste. A geração por filtros permanece pendente. |
| RF22 | Consulta de relatórios anteriores | CU04 | Pendente | [Rotas administrativas][product-urls] e [consulta de indicadores atuais][report]. | Inspeção da rota e do serviço. Recuperação de relatório persistido a validar quando houver implementação. |
| RF23 | Exportação de relatórios | CU05 | Pendente | [Rotas administrativas][product-urls]. | Inspeção das rotas. Formato, geração e teste de download ainda dependem de definição. |
| RF24 | Consulta administrativa de usuários | CU01 | Pendente | [Cadastros internos][admin-registry], [rotas raiz][root-urls] e [rotas administrativas][product-urls]. | [Ausência do Django Admin pela web][admin-route-test]. Busca e histórico unificado pela interface seguem pendentes. |
| RF25 | Conversar após a seleção | CU25 | Observado | [Abertura da conversa na seleção][selection] e [acesso e envio de mensagens][chat]. | [Envio e notificação à contraparte][chat-test] e [bloqueio de outra organização][chat-isolation-test]. |
| RF26 | Consultar e gerenciar notificações | CU26 | Observado | [Caixa de notificações e ações de leitura][notifications] e [escopo por usuário e organização ativa][notification-scope]. | [Leitura por POST][notification-test], [isolamento][notification-isolation-test] e [paginação e escopo][notification-list-test]. |

## Requisitos não funcionais

Os casos de uso desta seção indicam jornadas úteis para verificar o requisito. Requisitos transversais podem atingir outras jornadas.

| ID | Requisito | Jornadas relacionadas | Estado ou evidência | Teste ou verificação |
| --- | --- | --- | --- | --- |
| RNF01 | Atualizar proposta em até 1 segundo | CU09, CU16, CU26 | Sem medição. O código [notifica a instituição][submit] e [publica após o commit][realtime]. | [Testes de WebSocket][realtime-test] e [atualização de interface][realtime-ui-test] cobrem mecanismos. Medir do commit até a atualização visível com o ambiente e o transporte registrados. |
| RNF02 | Avisar sobre nova cotação em até 30 segundos | CU11, CU12, CU13 | Sem medição. [Criação publicada][quote-create] e [publicação de rascunho][quote-update] emitem evento para fornecedores quando habilitado. | [Publicação após commit][quote-event-test]. Medir a entrega na interface. O fluxo observado de publicação não envia e-mail. |
| RNF03 | Armazenar senhas com PBKDF2 SHA-256 e sal | CU06, CU07 | Uso da [API de senha no cadastro][registration] e da [redefinição do Django][account-urls]. | [Armazenamento com hash][password-test]. Conferir o identificador do algoritmo após cadastro e redefinição em ambiente controlado. |
| RNF04 | Rastrear interações relevantes | CU09, CU12, CU14, CU15, CU24 | Parcial. [Serviço de auditoria][audit] registra eventos selecionados. | [Auditoria da seleção na jornada][flow-test] e [rollback do envio][proposal-atomic-test]. Consolidar o catálogo de eventos que devem ser auditados. |
| RNF05 | Manter disponibilidade mensal de 99,9% | Transversal | Sem medição. Há [endpoint de saúde][health]. | [Resposta do endpoint][health-test]. Apurar série de monitoramento externo e janela de indisponibilidade mensal. |
| RNF06 | Adaptar a interface a diferentes larguras | CU06, CU09, CU12, CU16 | Estilos responsivos presentes. Cobertura integral de navegador, dispositivo e jornada a verificar. | [Assistente de proposta][proposal-ui-test] e [estrutura de estilos][bootstrap]. Executar matriz de larguras, navegadores e interações. |
| RNF07 | Executar backup horário redundante e reter por 30 dias | Transversal | Sem evidência operacional. O [guia de banco][database] orienta definir e testar a rotina no provedor. | Conferir agendamento, retenção, redundância e restauração com evidência do ambiente aplicável. |
| RNF08 | Manter o processamento financeiro externo | CU09, CU15, CU25 | Condições comerciais, seleção e conversa registradas. O [escopo do produto][product] e o [formulário da proposta][proposal-form] descrevem a jornada observada. | [Jornada de cotação a conversa][flow-test] e inspeção das rotas e integrações da revisão. |

Para RNF01 e RNF02, a [configuração versionada][settings] permite habilitar o tempo real em Preview e Production com camada em memória se `REDIS_URL` estiver ausente. Em desenvolvimento, o recurso vem habilitado por padrão. Essas regras divergem de afirmações no [guia de implantação][deploy] e no [guia de desenvolvimento][development]. A configuração efetiva de uma implantação e as latências permanecem a verificar.

## Correspondência com o histórico

| Identificador na documentação anterior | Referência nesta revisão |
| --- | --- |
| CU09 Participar de cotação e CU09 Enviar proposta | CU09 Enviar ou atualizar proposta. A referência a RF08 para envio, usada no fluxo legado, corresponde ao RF07 do catálogo. O RF08 do catálogo permanece associado à comparação. |
| CU12 Abrir cotação | CU12 Criar ou publicar cotação. |
| Segunda ocorrência de CU12 para edição de cotação | CU13 Editar rascunho de cotação, com a edição pós-publicação mantida como pendência no RF04. |
| CU21 Favoritar fornecedor e CU22 Desfavoritar fornecedor | CU21 Gerenciar fornecedores favoritos. |
| CU03 Geração de relatórios | CU03 Consultar indicadores. O escopo de relatórios filtrados continua registrado no RF21. |
| Chat e notificações registrados como comportamentos associados | RF25/CU25 e RF26/CU26 documentam jornadas próprias da versão analisada. |

A correspondência acima registra o histórico disponível no [commit de origem][historico] e nos fluxos revisados. Aprovações e devolutivas citadas no Teams dependem de consulta ao registro institucional.

## Reprodução da validação

Na revisão técnica indicada, os perfis `quick` e `full` do [verificador do projeto][harness] foram executados em 8 nov. 2026 com Django 6.1.1 e PostgreSQL 18 isolado. O perfil completo aprovou 327 testes Django e 67 testes JavaScript. Os roteiros manuais e as medições operacionais da matriz continuam identificados separadamente.

[base]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/commit/1aa8783ff1d9ada526b765f3a04bc6244106cbea
[release]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/tree/v2.0.0
[historico]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange-Documenta-o/tree/a40888869eeb
[signup-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/forms.py#L167
[registration]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/services/registration.py
[signup-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/tests/test_signup.py#L63
[category-signup-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/tests/test_supplier_categories.py#L56
[address-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/tests/test_addresses.py#L19
[login]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/auth_views.py#L44
[account-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/urls.py
[login-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_dashboard.py#L176
[login-limit-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/tests/test_login_security.py#L21
[quote-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/forms/quotes.py
[quote-create]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/quotes.py#L35
[quote-create-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_wizard.py#L238
[quote-draft-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_wizard.py#L361
[quote-form-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_forms.py#L41
[quote-draft]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/quotes.py#L122
[quote-update]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/quotes.py#L66
[quote-update-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_wizard.py#L413
[quote-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/quotes.py#L39
[quote-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_pagination.py#L107
[expired-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/proposals/test_views.py#L452
[proposal-form]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/forms/proposals.py
[submit]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/proposals.py#L284
[submit-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/proposals/test_views.py#L115
[revalidation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_service_transactions.py#L237
[compare]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/proposals.py#L218
[rank]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/proposals.py#L136
[rank-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/proposals/test_decision_criteria.py#L150
[max-amount-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/proposals/test_decision_criteria.py#L166
[proposal-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/proposals.py#L27
[proposal-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_pagination.py#L132
[selection-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/proposals.py#L349
[selection]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/proposals.py#L344
[flow-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/proposals/test_flow.py#L169
[selection-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_service_transactions.py#L159
[close-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/quotes.py#L385
[close-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/quotes.py#L106
[quote-window]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/models/quotes.py#L147
[admin-registry]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/admin.py
[root-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/config/urls.py
[admin-route-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_views.py#L57
[support-view]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/core.py#L105
[support-create]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/core.py#L37
[support-auth-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_views.py#L185
[category-request-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_category_requests.py#L76
[support-atomic-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_service_workflows.py#L18
[support-admin]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/system_admin.py
[support-answer-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_category_requests.py#L270
[category-approve-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_category_requests.py#L138
[ratings]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/proposal_review.py
[review-save]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/proposals.py#L442
[team]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/team.py
[team-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/account/test_team_management.py#L357
[team-denied-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/account/test_team_management.py#L240
[poll-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/quotes.py#L183
[poll-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_poll_options.py#L180
[favorites-service]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/quotes.py#L140
[favorites-list]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/quotes.py#L22
[favorite-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_engagement_views.py#L125
[favorite-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/quotes/test_engagement_views.py#L160
[report]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/core.py#L181
[product-urls]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/urls.py#L57
[chat]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/chat.py
[chat-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/chat/test_views.py#L103
[chat-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/chat/test_views.py#L149
[notifications]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/views/core.py#L38
[notification-scope]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/selectors/core.py#L141
[notification-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_notification_read.py#L80
[notification-isolation-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_notification_read.py#L92
[notification-list-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_pagination.py#L148
[realtime]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/realtime.py
[realtime-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_realtime.py
[realtime-ui-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/js/realtime.test.cjs
[quote-event-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_service_transactions.py#L302
[password-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/tests/test_models.py#L29
[audit]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/services/audit.py
[proposal-atomic-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/test_service_transactions.py#L216
[health]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/accounts/public_views.py#L90
[health-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/core/test_views.py#L136
[proposal-ui-test]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/bidxchange/tests/js/proposal_wizard.test.cjs
[bootstrap]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/frontend/ui/bootstrap.scss
[database]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/docs/DATABASE.md
[product]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/PRODUCT.md
[settings]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/config/settings.py#L166
[deploy]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/docs/VERCEL_DEPLOY.md
[development]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/docs/DEVELOPMENT.md
[harness]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783/.agents/README.md#verificação
