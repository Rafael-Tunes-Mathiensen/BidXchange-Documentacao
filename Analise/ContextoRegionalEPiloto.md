# Contexto regional e dimensionamento do piloto do BidXchange

O recorte inicial é **Araras (SP), código IBGE 3503307**. A análise usa estabelecimentos da educação básica para dimensionar o contexto de demanda e unidades locais de atividades econômicas selecionadas como indício de oferta. A disponibilidade para participar depende de confirmação com cada instituição e fornecedor. As fontes foram consultadas em 19 nov. 2026.

## Estabelecimentos e APMs

| Fonte e recorte | Resultado | Como interpretar |
| --- | ---: | --- |
| Inep, Censo Escolar 2025, Araras, Sinopse V2, tabela 3.2 | **91 estabelecimentos** | 65 da rede pública, dos quais 48 municipais e 17 estaduais, sem federais. Outros 26 pertenciam à rede privada, da qual 13 particulares, 9 comunitários, 1 confessional e 3 filantrópicos. O Censo conta estabelecimentos em atividade na data de referência, com ao menos uma matrícula. Exclui os que ofertam exclusivamente atividade complementar ou atendimento educacional especializado. [Sinopse da Educação Básica][inep] |
| Prefeitura de Araras, início do ano letivo em 9 fev. 2026 | **48 escolas municipais** | Retrato da rede municipal nessa data. A coincidência com o subtotal do Censo de 2025 não identifica individualmente as mesmas escolas. [Nota da Prefeitura][escolas26] |
| Decreto Municipal nº 7.998/2026, Anexo único, p. 7 do DOE nº 2.859, publicado em 2 abr. 2026 | **47 APMs listadas** | Contagem de linhas do Anexo e conferência de 47 CNPJs distintos. A lista é do PDDE Municipal (PDDEM) e não abrange todas as redes. Estar listado não comprova repasse, autonomia para contratar, disponibilidade ou adesão ao BidXchange. [Diário Oficial do Município][decreto] |

Os três números têm unidades e datas diferentes. As APMs se vinculam a escolas e a lista do PDDEM tem finalidade própria, por isso a análise não soma essas contagens nem calcula uma taxa de cobertura de APMs sem cruzamento por unidade. A participação exige confirmar quem tem competência para autorizar o piloto e a forma de registro aplicável, caso a caso. Os dados também não cobrem instituições exclusivamente de ensino superior.

**Como reproduzir.** Baixe a [Sinopse V2 em ZIP][inep-zip], atualizada em julho de 2026, e abra `Sinopse_Estatistica_da_Educação_Basica_2025_V2.xlsx`. Na aba `3.2`, filtre a coluna D pelo código `3503307`. A linha 3340, nas colunas E:J, traz 91, 65, 0, 17, 48 e 26, nessa ordem. As categorias privadas estão em K:N. O MD5 do XLSX é `07461c4fd19e120ef31945af8a3d0625`, igual ao manifesto do ZIP. Para repetir a contagem das APMs, conte as linhas preenchidas da tabela do Anexo único, da primeira à última APM, e confira a unicidade da coluna CNPJ. A pesquisa não replica identificadores das entidades.

## Categorias e oferta local

O [registro de elicitação](../Requisitos/ElicitacaoRequisitos.docx) descreve compras de materiais de consumo e serviços de manutenção de equipamentos e infraestrutura pelo lado da APM. A entrevista serve de ponto de partida para escolher categorias candidatas. A segmentação abaixo relaciona essas compras a atividades econômicas que podem atendê-las. As categorias iniciais correspondem a **Papelaria e escritório** e **Manutenção e reformas** no cadastro do produto. [Categorias do BidXchange na versão 2.0.0][seed-default] · [Revisão dos nomes][category-names] · [Categorias de fornecedores][seed-supplier]

| Categoria de compra ou serviço | Classe CNAE 2.0 do levantamento | Unidades locais no CEMPRE 2024 em Araras |
| --- | --- | ---: |
| Materiais de expediente, como papel, pastas e canetas | 47.61-0 Comércio varejista de livros, jornais, revistas e papelaria | 45 |
| Pequena manutenção predial, a depender da necessidade | 43.21-5 Instalações elétricas | 59 |
| Pequena manutenção predial, a depender da necessidade | 43.22-3 Instalações hidráulicas, de sistemas de ventilação e refrigeração | 19 |
| Material e suprimentos de informática, como opção de expansão | 47.51-2 Comércio varejista especializado de equipamentos e suprimentos de informática | 48 |
| Manutenção de equipamentos de informática, como opção de expansão | 95.11-8 Reparação e manutenção de computadores e de equipamentos periféricos | 17 |

**Como reproduzir.** Consulte a [API do IBGE para a tabela 9528 do SIDRA][cem-pre], pesquisa Cadastro Central de Empresas (CEMPRE), ano 2024, variável 706 (número de unidades locais), município 3503307 e classificação 12762 (CNAE 2.0). A tabela informa unidades locais nas classes mais amplas que os serviços e produtos do piloto. Pode haver vários estabelecimentos da mesma empresa. A contagem não mede aptidão fiscal, interesse, cobertura de entrega ou capacidade de atender uma especificação. É possível atender a partir de outro município. O levantamento não soma as classes como universo de fornecedores elegíveis. [Metadados da tabela 9528][cem-meta] · [Consulta CNAE da Concla][concla]

## Proposta de piloto

**Rodada inicial de quatro semanas em Araras, com cotações simuladas e sem contratação.** Convidar até duas instituições com representantes autorizados, usando uma necessidade simulada por categoria, em papelaria e manutenção. Organizar até seis convites a fornecedores, com até três por categoria e deduplicação de empresas. Confirmar interesse, atendimento da localidade, capacidade para o item e disponibilidade para testar. Planejar até quatro cotações, com limite de uma nova cotação por semana. O teto operacional supõe tempo para orientar cadastro, acompanhar as propostas e apoiar o encerramento. Convites, cotações e adesões efetivas devem ser registrados separadamente.

| Evidência de acompanhamento | Como registrar |
| --- | --- |
| Adesão de instituições e fornecedores | Contar convidados, cadastros concluídos e participantes que chegaram a publicar ou enviar uma proposta, por grupo e categoria. |
| Capacidade de comparar propostas | Contar propostas que atendam ao roteiro de aceite de cada cotação simulada, como preenchimento de preço e prazo e atendimento à especificação. Apurar a mediana dessas propostas por cotação e a quantidade de cotações com ao menos duas opções comparáveis. Registrar o critério antes de abrir cada rodada. |
| Registro da decisão | Contar cotações publicadas e encerradas com decisão justificada, identificando categoria e encerramentos sem seleção. Registrar a mediana do tempo entre publicação e encerramento com escolha. Informar quantas observações sustentam cada mediana. |
| Suporte | Contar pedidos de ajuda e tempo de atendimento por etapa. Registrar desistências e motivos informados, sem presumir motivo quando houver silêncio. |

**Critério para continuar.** Encerrar ao menos uma cotação com decisão registrada em cada uma das duas categorias e receber pelo menos duas propostas que satisfaçam o roteiro de aceite em ao menos duas cotações. Se houver poucos retornos, rever especificação e recrutamento antes de ampliar. O critério indica que o fluxo pôde ser observado em condições controladas. A rodada não estima taxa de adesão regional e não substitui as [metas SMART de três meses](AnaliseSmartCorrigido.docx), de 10 instituições cadastradas, 30 fornecedores ativos e 5 cotações concluídas.

Em eventual uso real com recursos do PDDEM, a instituição e a APM devem confirmar a autorização, o plano e os procedimentos do programa. O art. 20 do Decreto nº 7.998/2026 prevê **mínimo de três orçamentos**, preferencialmente de fornecedores locais. Admite pesquisa pela internet ou e-mail quando datada, identificada, assinada e preenchida com os campos do art. 16. O registro do teste de duas propostas não atende a esse rito. A declaração fiscal no BidXchange é autodeclarada. O programa exige verificações e documentação próprias antes de qualquer contratação. [Decreto Municipal nº 7.998/2026, arts. 16, 20 e 21][decreto]

[inep]: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-basica
[inep-zip]: https://download.inep.gov.br/dados_abertos/sinopses_estatisticas/sinopse_estatistica_censo_escolar_2025.zip
[escolas26]: https://www.araras.sp.gov.br/noticias/28784
[decreto]: https://araras.siscam.com.br/arquivo?Id=223240
[cem-pre]: https://servicodados.ibge.gov.br/api/v3/agregados/9528/periodos/2024/variaveis/706?localidades=N6%5B3503307%5D&classificacao=12762%5B117355,117356,117458,117467,117877%5D
[cem-meta]: https://servicodados.ibge.gov.br/api/v3/agregados/9528/metadados
[concla]: https://cnae.ibge.gov.br/
[seed-default]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783ff1d9ada526b765f3a04bc6244106cbea/bidxchange/migrations/0002_seed_default_categories.py
[category-names]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783ff1d9ada526b765f3a04bc6244106cbea/bidxchange/migrations/0004_correct_category_names.py
[seed-supplier]: https://github.com/Rafael-Tunes-Mathiensen/BidXchange/blob/1aa8783ff1d9ada526b765f3a04bc6244106cbea/bidxchange/migrations/0008_seed_supplier_categories.py
