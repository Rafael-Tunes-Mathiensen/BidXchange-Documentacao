# Filas e rotinas em segundo plano

Cartão Trello 071. Documento alinhado ao código da branch `main` do BidXchange.

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

## 3. Rotinas agendadas

Cada rotina existe como `management command` (execução manual em ambiente
restrito) e, quando aplicável, como endpoint HTTP acionado pelo cron da Vercel.

| Rotina | Command | Endpoint | Frequência |
|---|---|---|---|
| Remover cadastros pendentes | `delete_expired_pending_accounts` | `/api/cron/delete-expired-pending-accounts/` | Diária, 03:00 UTC (`vercel.json`) |
| Reenviar e-mails pendentes e purgar antigos | `send_pending_emails [--limit N]` | `/api/cron/send-pending-emails/` | Intervalo curto (ver nota) |
| Limpar janelas de limite de autenticação | `clear_expired_authentication_limits` | — | Manual/sob demanda |

> **Nota:** o `vercel.json` agenda hoje apenas a limpeza de cadastros. O reenvio de
> e-mails precisa ser agendado em intervalo curto no ambiente de produção (cron
> externo ou plano da Vercel compatível); sem isso, só a tentativa imediata pós-commit
> ocorre e falhas de SMTP ficam pendentes.

### 3.1 Remoção de cadastros pendentes

Implementação: `accounts/services/cleanup.py`. Remove contas inativas, sem e-mail
confirmado, criadas há pelo menos **3 dias**, junto com a organização criada no
cadastro. Preserva superusuários, staff, contas verificadas, organizações
verificadas ou com mais de um vínculo, e qualquer conta com dados operacionais
associados (inclui `ProtectedError`). Cada candidato é processado em transação
própria com bloqueio de linha.

### 3.2 Reenvio de e-mails

Entrega até 50 mensagens vencidas por execução (`limit=50`) e depois purga registros
com mais de 7 dias.

### 3.3 Limites de autenticação

Remove apenas contadores (`AuthenticationRateLimit`) já expirados, sem afetar
janelas ativas.

### Segurança dos endpoints de cron

Implementação: `accounts/cron_views.py`.

- Apenas `GET`; outros métodos retornam 405.
- Exigem `Authorization: Bearer <CRON_SECRET>`, comparado com `secrets.compare_digest`.
- Sem `CRON_SECRET` configurado ou com cabeçalho incorreto, retornam **401** e nada é executado.
- `CRON_SECRET` deve ser *Sensitive* na Vercel, com pelo menos 16 caracteres.
- A Vercel envia o cron apenas em Production e pode executar após o horário nominal.

## 4. Tempo real (Django Channels)

Implementação: `bidxchange/realtime.py`, `bidxchange/consumers.py`, `config/asgi.py`.

- Rota WebSocket `ws/atualizacoes/`.
- Eventos são publicados em grupos (`user_*`, `organization_*`, `audience_*`) **somente
  após o commit**, garantindo que a alteração já esteja visível.
- Usado para avisar mudanças em recursos (ex.: cotação criada ou encerrada) e para
  encerrar conexões quando o acesso à organização é revogado.
- Controlado por `ENABLE_REALTIME`; em produção exige `REDIS_URL` (camada
  `channels_redis`, com TLS). Fora de produção usa `InMemoryChannelLayer`.
- **Não é durável:** eventos perdidos não são reenviados; a tela se atualiza ao recarregar.

## 5. Fora de escopo atual

- Não há expiração automática de cotações: o encerramento (`CLOSED_WITHOUT_WINNER`,
  `CANCELLED`) ocorre por ação de usuário.
- Não há workers, filas de mensagens externas nem painel de monitoramento de jobs.

## 6. Operação e diagnóstico

- Mensagens `failed` e `last_error` (até 255 caracteres) indicam a causa da falha
  de entrega; consulte pelo Admin ou banco, em ambiente restrito.
- Falhas de envio são registradas em log (`WARNING`) apenas com o tipo da exceção.
- Execução manual: `python manage.py send_pending_emails`,
  `python manage.py delete_expired_pending_accounts`,
  `python manage.py clear_expired_authentication_limits`.
- Conferir execuções do cron em **Vercel > Settings > Cron Jobs**.
