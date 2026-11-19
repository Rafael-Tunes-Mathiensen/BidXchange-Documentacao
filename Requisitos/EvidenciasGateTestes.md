# Evidências do gate de testes do BidXchange

O workflow **Harness CI** executou as verificações de backend e frontend abaixo em pushes para `develop`. Cada resultado pertence ao commit indicado. Os testes Django foram repetidos nas três versões de Python de cada execução.

| Execução | Data | Commit | Duração total | Resultado |
| --- | --- | --- | --- | --- |
| [Harness CI #289](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701) | 3 nov. 2026 | [`1aa8783ff1d9ada526b765f3a04bc6244106cbea`](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/commit/1aa8783ff1d9ada526b765f3a04bc6244106cbea) | 2 min 36 s | Aprovado |
| [Harness CI #293](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343) | 11 nov. 2026 | [`34853e0be3e2a69a70e77c2596657f6cd548a64d`](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/commit/34853e0be3e2a69a70e77c2596657f6cd548a64d) | 3 min 15 s | Aprovado |

## Logs e resultados

| Job | Execução #289 | Execução #293 |
| --- | --- | --- |
| Frontend | [67 testes JavaScript aprovados](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701/job/125920818327) | [67 testes JavaScript aprovados](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343/job/130856786635) |
| Backend Python 3.12 | [Python 3.12.15, 327 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701/job/125920818757) | [Python 3.12.16, 348 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343/job/130856786921) |
| Backend Python 3.13 | [Python 3.13.17, 327 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701/job/125920818526) | [Python 3.13.18, 348 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343/job/130856786939) |
| Backend Python 3.14 | [Python 3.14.9, 327 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701/job/125920818717) | [Python 3.14.10, 348 testes Django e 5 do harness](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343/job/130856787097) |
| Resultado agregado | [harness/required aprovado](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/41637066701/job/125922001805) | [harness/required aprovado](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/actions/runs/43119721343/job/130858117724) |

O frontend verificou distribuição Bootstrap, estilos, sintaxe JavaScript e os testes do comando `npm run test:ui`. O backend verificou configuração Django, migrations e coleta de estáticos em simulação, lint e formatação Ruff, testes do harness e a suíte Django. Os totais Django incluem testes de unidade e integração, sem subtotais separados nos logs.

## Ambiente

| Item | Execução #289 | Execução #293 |
| --- | --- | --- |
| Runner hospedado | Ubuntu 26.04, imagem 20261025.179.1, runner 2.338.2 (logs de frontend e backend 3.14) | Ubuntu 26.04, imagem 20261101.186.1, runner 2.338.2 |
| Frontend | Node.js 24.15.0 e Python 3.14.9 | Node.js 24.15.0 e Python 3.14.10 |
| Django | 6.1.1 conferido no job Python 3.14 | 6.1.1 |
| Imagem PostgreSQL nos jobs de backend | `postgres:18-alpine` | `postgres:18-alpine` |
| Digest da imagem PostgreSQL | `sha256:10a5c69a83035ab5239f5620d708520e8b28f5aa1f2b20143e6024532edadfb5` | `sha256:9ba53c7d41ea093baf5c1ba635ba5434c4f979880527d49bb7d9237d3193085b` |

O digest identifica a imagem do serviço PostgreSQL. A versão da imagem do runner identifica o ambiente hospedado. O resumo das duas execuções não lista artefatos anexos. Os links dos jobs apontam aos logs disponíveis no GitHub Actions. O arquivo `.github/workflows/django.yml` de cada commit descreve o CI. [Workflow de #289](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783ff1d9ada526b765f3a04bc6244106cbea/.github/workflows/django.yml) · [Workflow de #293](https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/34853e0be3e2a69a70e77c2596657f6cd548a64d/.github/workflows/django.yml)

## Limites da evidência

As execuções verificaram unitários e integração automatizada. Não há evidência nesses jobs de testes ponta a ponta em navegador real, percentual de cobertura, testes de carga ou desempenho, nem validação com usuários. Os registros de execução local da monografia têm procedência própria.
