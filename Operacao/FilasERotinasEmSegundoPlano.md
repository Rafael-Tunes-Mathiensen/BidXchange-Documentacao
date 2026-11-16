# Filas e rotinas em segundo plano

Cartão Trello 071. Documento alinhado ao código da branch `main` do BidXchange.

**Como ler este documento.** Cada afirmação pertence a uma de três camadas:

- **Código**: o que os módulos Python implementam.
- **Configuração versionada**: o que está em arquivos do repositório (`vercel.json`, `settings.py`).
- **Implantação real**: o que de fato roda em produção. **Esta camada não é
  demonstrável pelo repositório** e só pode ser confirmada no painel da Vercel e
  nos logs do ambiente. Nenhuma afirmação sobre produção é presumida aqui.

## 1. Visão geral

O BidXchange **não usa um broker de filas dedicado** (Celery, RQ ou similar) nem
workers permanentes. O trabalho em segundo plano usa três mecanismos simples,
compatíveis com a hospedagem serverless na Vercel:

| Mecanismo | Finalidade | Persistência |
|---|---|---|
| Fila durável `EmailOutbox` | Envio de e-mails transacionais com retentativas | Banco de dados |
| Rotinas agendadas (cron HTTP e `management commands`) | Limpezas e reenvio da fila | Não se aplica |
| Eventos em tempo real (Django Channels + Redis) | Atualizar telas abertas | Não durável |

## 2. Fila de e-mails (`EmailOutbox`)

Implementação: `accounts/services/outbox.py`, modelo `EmailOutbox` em `accounts/models.py`.

### Fluxo

1. A operação de origem (cadastro, recuperação de senha, convite, aviso de equipe)
   chama `enqueue_email()`, que grava a mensagem na **mesma transação** da operação.
   Se a transação for desfeita, o e-mail não existe.
2. Após o commit (`transaction.on_commit`), tenta-se a entrega imediata da mensagem.
3. Se o SMTP falhar, a operação do usuário **não é desfeita**: a mensagem permanece
   pendente e é reenviada pela rotina periódica.
4. A rotina `deliver_pending_emails` reserva mensagens vencidas, envia e atualiza o estado.

### Estados

| Estado | Significado |
|---|---|
| `pending` | Aguardando envio ou nova tentativa |
| `sent` | Enviado; assunto preservado, corpo apagado |
| `failed` | Excedeu o máximo de tentativas; corpo apagado |

### Regras de robustez

- **Concorrência:** a reserva usa `select_for_update(skip_locked=True)` e um
  arrendamento (`locked_until`), evitando envio simultâneo da mesma mensagem.
- **Retentativas:** recuo exponencial de `30s × 2^tentativas`, limitado a 1 hora.
- **Semântica:** entrega *pelo menos uma vez*. O `Message-ID` (`<id>@bidxchange`)
  é o mesmo nas retentativas, permitindo deduplicação pelo destinatário.
- **Privacidade:** o corpo (que pode conter links de uso único) é apagado após
  sucesso ou falha definitiva.
- **Retenção:** registros `sent` e `failed` são removidos após 7 dias
  (`purge_finished_emails`).
- **Timeout:** `EMAIL_TIMEOUT` finito impede que o SMTP prenda a requisição.

### Variáveis de ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `EMAIL_TIMEOUT` | 10 | Timeout do SMTP, em segundos |
| `EMAIL_OUTBOX_MAX_ATTEMPTS` | 6 | Tentativas antes de marcar como `failed` |
| `EMAIL_OUTBOX_LEASE_SECONDS` | 120 | Duração da reserva de uma mensagem |

## 3. Matriz de rotinas

| Rotina | Executor (código) | Gatilho | Frequência | Proteção | Falhas | Evidência do ambiente |
|---|---|---|---|---|---|---|
| Entrega imediata de e-mail | `deliver_pending_emails(limit=1)` dentro do processo web | `transaction.on_commit` após `enqueue_email` | A cada e-mail enfileirado | Roda dentro de requisição já autenticada | Exceção é registrada e a mensagem fica `pending` com recuo | Código apenas |
| Reenvio de e-mails pendentes | Comando `send_pending_emails` ou endpoint `GET /api/cron/send-pending-emails/` (até 50 por execução, depois purga) | **Nenhum gatilho versionado.** Exige scheduler externo ou execução manual | Não definida no repositório; a documentação recomenda intervalo curto | Endpoint: `Authorization: Bearer <CRON_SECRET>` com `compare_digest`; apenas `GET`; 401 sem segredo | Falha por mensagem: recuo de 30s×2^n (máx. 1h); após 6 tentativas vira `failed` | **Não confirmada.** Verificar no painel da Vercel e em scheduler externo |
| Remoção de cadastros pendentes | Comando `delete_expired_pending_accounts` ou `GET /api/cron/delete-expired-pending-accounts/` | Cron da Vercel em `vercel.json` | Diária, `0 3 * * *` (UTC) | Mesmo `CRON_SECRET` Bearer; só GET | Candidato com dado inesperado ou `ProtectedError` é ignorado; cada conta em transação própria | Agendamento **versionado**; execução real **não confirmada** (ver Settings > Cron Jobs) |
| Limpeza de limites de autenticação | Comando `clear_expired_authentication_limits` | Manual | Sem agendamento | Execução em ambiente restrito | Sem retentativa | Sem endpoint nem cron; nenhuma execução esperada |
| Encerramento automático de cotações | **Não existe** | Não há | Não há | Não se aplica | Não se aplica | Ver seção 5 |

### 3.1 Quem consome a outbox

Consomem a `EmailOutbox` apenas: (1) o callback pós-commit no processo web, para a
mensagem recém-criada; e (2) `deliver_pending_emails` chamado por
`send_pending_emails` ou pelo endpoint de cron. Não há worker residente. Portanto,
**sem scheduler externo apontando para o comando ou endpoint, mensagens cuja
primeira tentativa falhou permanecem `pending` indefinidamente.** No repositório
não há GitHub Actions (`django.yml` e `auto-author-assign.yml` não têm `schedule`),
nem `compose.yaml` com cron, nem outro arquivo que agende esse reenvio.

### 3.2 Remoção de cadastros pendentes

Implementação: `accounts/services/cleanup.py`. Remove contas inativas, sem e-mail
confirmado, criadas há pelo menos 3 dias, junto com a organização criada no
cadastro. Preserva superusuários, staff, contas verificadas, organizações
verificadas ou com mais de um vínculo e qualquer conta com dados operacionais.

### 3.3 Segurança dos endpoints de cron

Implementação: `accounts/cron_views.py`. Apenas `GET` (outros métodos: 405).
Exigem `Authorization: Bearer <CRON_SECRET>`; sem segredo configurado ou com
cabeçalho incorreto respondem 401 e nada é executado. O valor do segredo nunca
deve aparecer em capturas, logs ou documentação; use variável *Sensitive* na Vercel.

## 4. Tempo real (Django Channels)

Implementação: `bidxchange/realtime.py`, `bidxchange/consumers.py`, `config/asgi.py`.
Eventos são publicados em grupos somente após o commit, via `channels_redis`
(`REDIS_URL`; `InMemoryChannelLayer` fora de produção), e controlados por
`ENABLE_REALTIME`. Não é fila durável: eventos perdidos não são reenviados. Não
executa rotina periódica.

## 5. Encerramento de cotações: não há automação

Verificação no código:

- `close_quote` (`bidxchange/services/quotes.py`) é a **única** transição para
  `CLOSED_WITHOUT_WINNER` ou `CANCELLED` e é chamada por ação de usuário.
- Nenhum command, endpoint de cron, tarefa ou sinal altera o status de cotações
  quando `closes_at` é atingido; `vercel.json` não agenda nada com esse fim.
- Após `closes_at`, a cotação deixa de aceitar propostas apenas porque
  `Quote.is_accepting_proposals` compara `closes_at` com o horário atual na leitura.
  O campo `status` **continua `OPEN`** até alguém encerrar manualmente.

Conclusão: **o sistema não encerra cotações automaticamente**. Ele bloqueia novas
propostas depois do prazo, mas não muda o status nem notifica. Qualquer afirmação
contrária exigiria uma rotina que não existe no repositório.

## 6. Situação da implantação real

| Pergunta | Resposta com evidência |
|---|---|
| O cron diário de contas pendentes está ativo em produção? | **A confirmar.** Está no `vercel.json`; conferir em Vercel > Settings > Cron Jobs e nos logs |
| Existe scheduler externo para `send-pending-emails`? | **Sem evidência no repositório.** Confirmar com o responsável pelo deploy; se não houver, declarar que o reenvio não está implantado |
| Existe worker residente? | **Não.** Nenhum código ou configuração de worker (hospedagem serverless) |
| `CRON_SECRET` está configurado em Production? | **A confirmar**, sem registrar o valor. Sem ele os endpoints respondem 401 |

Pendência para fechar o cartão: registrar a confirmação (data, responsável e
captura sem segredos) das linhas marcadas "A confirmar".

## 7. Operação e diagnóstico

- `EmailOutbox.status`, `attempts` e `last_error` (até 255 caracteres) indicam a
  causa de falhas; consulte em ambiente restrito.
- Falhas de envio geram log `WARNING` apenas com o tipo da exceção.
- Execução manual: `python manage.py send_pending_emails`,
  `python manage.py delete_expired_pending_accounts`,
  `python manage.py clear_expired_authentication_limits`.
