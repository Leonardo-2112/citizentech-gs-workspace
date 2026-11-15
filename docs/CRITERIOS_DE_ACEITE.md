# Critérios de aceite — GS 2026/2 (extraídos do PDF oficial)

> **Fonte:** `1TDS Fevereiro - Global Solution 2026-2.pdf` (FIAP, Graduação, 1º ano ADS, turmas de fevereiro — tema **CitizenTech**).
> **Data de extração:** 15/11/2026.
> **Em caso de dúvida, vale o PDF.**
>
> Convenções deste arquivo:
> - Texto entre aspas ou em listas é reprodução fiel (ou quase literal) do PDF.
> - **⚠ Exemplo/placeholder do PDF:** trechos que no PDF aparecem como `[ex.: ...]` — são exemplos/modelos dos professores, não regra definitiva.
> - **⚠ Divergência no PDF:** pontos em que o próprio PDF se contradiz. Confirmar com o professor.

---

## Regras gerais

### O que está em jogo
- 15 dias: do kickoff (04/11) à entrega (19/11).
- **60% da nota do semestre.**
- 6 disciplinas, **uma única solução**. "O grupo propõe uma solução para o tema CitizenTech. Essa mesma solução é a base das entregas de todas as disciplinas."
- "Entrega no Portal FIAP: 19/11, até 23h55. **Sem prorrogação.**"

### Agenda
| Data | Evento | Detalhe |
|---|---|---|
| 04/11 | Kickoff | Live de abertura e conteúdo para os alunos |
| 13/11 | Cadastro dos grupos | Prazo final para cadastrar os grupos |
| 19/11 | Entrega | No Portal FIAP, até 23h55 |
| 23 a 27/11 | Apresentações | Período de apresentações dos grupos de forma presencial |
| até 30/11 | Correção | Correção dos professores |

### Critérios gerais da proposta ("Uma boa proposta deixa claro")
- [ ] 01 Quem é o cidadão beneficiado
- [ ] 02 Qual problema será resolvido
- [ ] 03 Como a solução vai funcionar
- [ ] 04 Quais tecnologias serão usadas
- [ ] 05 Quem participa do ecossistema
- [ ] 06 Como o impacto será medido e ampliado
- [ ] "Simples, segura, inclusiva e acessível: protege dados, respeita diferenças e continua útil mesmo fora do cenário ideal de infraestrutura e conectividade."
- [ ] **Conexão com os ODS da ONU:** "Cada projeto deve identificar os ODS aos quais está conectado e explicar de que forma contribui para suas metas." ODS listados: 2 (Fome zero e agricultura sustentável), 3 (Saúde e bem-estar), 4 (Educação de qualidade), 9 (Indústria, inovação e infraestrutura), 10 (Redução das desigualdades), 11 (Cidades e comunidades sustentáveis), 13 (Ação contra a mudança global do clima) — Agenda 2030 da ONU.

### Grupo e cadastro
- [ ] Desafio feito individualmente ou em grupo de **até 5 integrantes — sem exceções**.
- [ ] Grupos podem reunir alunos de turmas e turnos diferentes.
- [ ] Separar RM, nome completo e turma de cada integrante.
- [ ] Preencher o formulário até **13/11** ("1TDS - Cadastro Grupos Global Solution 2º Semestre 2026 – Preencher o formulário"; o link está no PDF).
- [ ] "Grupos não cadastrados no prazo não aparecem no portal de entrega."

### Formato de entrega
- [ ] Prazo: **19/11/2026, até 23h55**, na área de trabalhos do Portal do Aluno.
- [ ] Cada disciplina aparece como uma entrega separada na lista de trabalhos; repetir o processo para todas as entregas da GS.
- [ ] Passo a passo: (01) acessar www2.fiap.com.br com RM e senha; (02) em Aulas, clicar em "Entrega de Trabalhos"; (03) escolher um trabalho da Global Solution; (04) anexar o arquivo do projeto, conferindo grupo, data de vencimento e descrição; (05) conferir o arquivo anexado (fica registrado na entrega).

### .txt de identificação
- [ ] "Um .txt em cada .zip — com RM, nome completo e turma de cada integrante do grupo."
- ⚠ **Divergência no PDF:** algumas disciplinas pedem identificação de outro jeito (BD: "capa com nomes, RM e turma" e ".zip somente com o PDF e o .sql"; Java: "README.md ou .txt na raiz"; Eng. Software: entrega é **um único PDF**, sem .zip). Na dúvida, incluir o .txt em todo .zip e confirmar com o professor.

### Uso de IA generativa
| Permitido | Não permitido | Como declarar |
|---|---|---|
| [ex.: apoio para pesquisa, revisão de texto, explicação de erros] | [ex.: entregar código ou texto gerado sem entender e sem revisar] | [ex.: seção no README listando as ferramentas usadas e para quê] |

- ⚠ **Exemplo/placeholder do PDF:** as três colunas desse slide estão preenchidas só com `[ex.: ...]` — os professores não substituíram o modelo. Tratar como orientação, não como regra fechada.
- Regra concreta existente: em **Software Engineering and Business Model** o "Registro do uso de IA" é **obrigatório e vale 10 pts** (ver seção da disciplina). Em **Eng. Software / UX**, o protótipo pode ser feito "inclusive com IA".

### Apresentação
- [ ] **23 a 27/11, presencial**, durante a aula presencial da disciplina.
- [ ] Vale **30% da nota da disciplina**. "Cada professor mostra nos slides da disciplina o que o grupo precisa apresentar."
- Quem apresenta: "Todos os integrantes (Pode ser definido pelo professor)".
- Escala dos grupos: organização realizada pelo professor.
- O que levar: alinhar com o professor da disciplina.

### Premiação
- O grupo vencedor leva shape e camisetas exclusivas.
- 01 Avaliação: além das notas, os grupos são avaliados por uma comissão de professores.
- 02 Elegibilidade: **nota igual ou maior que 90 em todas as disciplinas e no vídeo pitch de Software Engineering and Business Model**.
- 03 Escolha: professores e coordenação analisam os grupos elegíveis e escolhem um único vencedor.

### Suporte
- Professores disponíveis para dúvidas durante as aulas, presencial e remota.
- Não haverá chamada durante a GS.

---

## 1. IA & Chatbot (Artificial Intelligence & Chatbot)

### Objetivo / detalhes da entrega
- **Objetivo:** com base no desafio CitizenTech, construir pelo menos 2 modelos de IA que envolvam Regressão, Classificação e/ou Agrupamento.
- **Integração:** criar uma API REST com (Flask, FastAPI etc) para que os modelos preditivos possam ser usados por outros sistemas.
- **Conexão com a solução:** os modelos devem resolver um problema real da solução do grupo: prever, classificar ou segmentar dados das pessoas que ela atende.
- **Pipeline esperado:** Análise exploratória → preparação dos dados → treinamento → avaliação de desempenho → exportação do modelo → API.
- **Tecnologias:** Python, Jupyter Notebook (.ipynb), bibliotecas de Machine Learning, serialização com .pickle/.joblib e Flask.
- **Atenção:** arquivo corrompido ou faltando zera o item correspondente.
- ⚠ **Divergência no PDF:** os detalhes dizem "Flask, FastAPI etc", mas o requisito 06, a pontuação e as entregas dizem **Flask**. Usar Flask é o caminho seguro.

### Requisitos
- [ ] 01 Construir no mínimo 2 modelos de IA envolvendo Regressão, Classificação e/ou Agrupamento
- [ ] 02 Usar dados coerentes com o problema da solução CitizenTech (.csv, .xlsx ou similar)
- [ ] 03 Desenvolver o pipeline de ML em notebooks .ipynb: análise exploratória, treinamento e avaliação
- [ ] 04 Avaliar o desempenho dos modelos com métricas adequadas a cada tipo de problema
- [ ] 05 Exportar os modelos pré-treinados (.pickle, .joblib ou similar)
- [ ] 06 Disponibilizar os modelos em uma API REST com Flask, pronta para integração com outros sistemas

### Pontuação da entrega
| Critério | Pontos |
|---|---|
| 01 Dados utilizados para treinar os modelos (.csv, .xlsx ou similar) | 10 |
| 02 Notebooks .ipynb: análise exploratória, treinamento e avaliação de desempenho | 60 |
| 03 Modelos pré-treinados (.pickle, .joblib ou similar) | 10 |
| 04 Código da API REST em Flask (.py) e integração | 20 |
| **Total** | **100** |

### O que tira pontos
| Penalidade | Efeito |
|---|---|
| 01 Entrega fora do prazo (19/11, 23h55) ou fora do Portal do Aluno | Nota zero |
| 02 Arquivo corrompido ou faltando algum arquivo no .zip | Item zerado |
| 03 Solução sem relação com o tema CitizenTech | Até −50 pts |
| 04 Menos de 2 modelos ou modelos fora de regressão, classificação e/ou agrupamento | Até −30 pts |
| 05 API Flask que não executa ou não consome os modelos pré-treinados | Até −20 pts |

"Atenção: caso o arquivo entregue esteja corrompido ou falte algum arquivo, o item será zerado."

### Entregáveis e formato do .zip
- [ ] Dados utilizados no treinamento dos modelos (.csv, .xlsx ou similar)
- [ ] Notebooks .ipynb com o pipeline de ML: análise exploratória, treinamento e avaliação
- [ ] Modelos pré-treinados (.pickle, .joblib ou similar)
- [ ] Código da API REST em Flask (.py) com a integração dos modelos
- [ ] Arquivo .txt com nomes dos integrantes e eventuais explicações adicionais
- **Formato:** [ex.: um .zip com o código-fonte e o .txt de identificação do grupo]
  - ⚠ **Exemplo/placeholder do PDF:** o formato está só como `[ex.: ...]`.

### Apresentação presencial (vale 30% da nota — 23 a 27/11, na aula da disciplina)
| Critério | Pontos |
|---|---|
| 01 Problema CitizenTech escolhido e como a IA ajuda a resolvê-lo | 15 |
| 02 Dados e análise exploratória: origem, tratamento e principais insights | 15 |
| 03 Escolha dos modelos (regressão, classificação e/ou agrupamento) e justificativa | 20 |
| 04 Métricas de avaliação e interpretação dos resultados | 20 |
| 05 Demonstração ao vivo da API Flask consumindo os modelos treinados | 20 |
| 06 Domínio técnico: todos os integrantes respondem às perguntas | 10 |
| **Total** | **100** |

---

## 2. Banco de Dados (Building Relational Database)

### Objetivo / detalhes da entrega
- Utilizar **Oracle SQL Developer** e **Oracle Data Modeler**, promovendo a modelagem relacional da solução CitizenTech e a implementação do banco em SQL. O ambiente vai armazenar, organizar e consultar as informações da solução, **além de servir de base de dados para as demais disciplinas da GS**. O modelo e o script devem estar alinhados ao problema escolhido pelo grupo e ao que as outras frentes vão precisar consultar.
- Objetivo: entregar um banco relacional completo, com **modelo conceitual, modelo lógico, modelo relacional e dicionário de dados**. Seguir o conteúdo do semestre: criação das tabelas com chave primária, chave estrangeira, NOT NULL, UNIQUE e CHECK; inclusão de 50 registros; atualização e exclusão com WHERE; e 10 consultas variadas, com filtro, cálculo, funções de agregação, HAVING, subconsulta, INNER JOIN, LEFT JOIN e RIGHT JOIN.
- "O grupo envia um único arquivo compactado com o PDF, as capturas da execução e o script SQL."
- ⚠ **Divergência no PDF (quantidade de registros):** detalhes, pontuação e entregas falam em **50 registros / 50 INSERTs**; o requisito 05 (slide 1/3) fala em **60 registros no total**. Fazer **60** atende os dois.
- ⚠ **Divergência no PDF (conteúdo do .zip):** os detalhes e a lista de entregas incluem as **capturas de tela**, mas o formato diz ".zip **somente** com o PDF e o .sql". Interpretação segura: colocar as capturas **dentro do PDF** (e/ou confirmar com o professor).

### Requisitos

**Requisitos 1/3 — estrutura**
- [ ] 01 Mínimo de 6 tabelas, já contando a tabela associativa do N:N.
- [ ] 02 Dois relacionamentos 1:N e um relacionamento N:N com tabela associativa.
- [ ] 03 Chave primária em toda tabela e chave estrangeira em todo relacionamento.
- [ ] 04 Pelo menos um NOT NULL, um UNIQUE e um CHECK com uma regra da solução.
- [ ] 05 60 registros no total, espalhados de modo que toda tabela tenha registro. (⚠ ver divergência 50 × 60 acima)
- [ ] 06 Pelo menos um UPDATE e um DELETE, ambos com WHERE. Sem WHERE não é aceito.

**Requisitos 2/3 — levantamento e modelagem**
- [ ] 01 Levantamento: problema, público, objetivo, atores, dados, perguntas do banco e ODS.
- [ ] 02 Texto da própria solução. Um levantamento genérico, válido para qualquer tema, não atende.
- [ ] 03 Três desenhos no Data Modeler: conceitual, lógico e relacional. Um não substitui o outro.
- [ ] 04 Dicionário: tabela, coluna, tipo, tamanho, nulo, chave, restrição e o que a coluna significa.
- [ ] 05 Modelo sem atributo multivalorado nem grupo repetido. Nomes sem espaço e sem acento.
- [ ] 06 CREATE TABLE no Oracle, na ordem das chaves estrangeiras, com comentário em cada tabela.

**Requisitos 3/3 — consultas**
- [ ] 01 São 10 consultas numeradas. Cada uma responde uma pergunta da solução CitizenTech.
- [ ] 02 No conjunto: WHERE, ORDER BY e cálculo no SELECT, não apenas função de agregação.
- [ ] 03 Funções COUNT, SUM, AVG, MAX e MIN, com GROUP BY, e pelo menos uma consulta com HAVING.
- [ ] 04 Pelo menos uma subconsulta (SUBSELECT).
- [ ] 05 Pelo menos uma consulta com INNER JOIN, uma com LEFT JOIN e uma com RIGHT JOIN.
- [ ] 06 Uma consulta pode reunir mais de um recurso. *(observação/permissão, não exigência)*

### Pontuação da entrega (Portal — 70% da nota)
| Critério | Pontos |
|---|---|
| 01 Levantamento de requisitos: problema, público, dados, perguntas e ODS escolhido | 10 |
| 02 DER: modelo conceitual, entidades, atributos, relacionamentos e cardinalidades | 10 |
| 03 Dicionário, modelo lógico e relacional, com chaves e tabela associativa | 15 |
| 04 Script no Oracle: tabelas, PK, FK, NOT NULL, UNIQUE, CHECK | 15 |
| 05 CRUD: 50 registros em todas as tabelas, um UPDATE e um DELETE com WHERE | 15 |
| 06 Consultas SQL: filtro, cálculo, agregação com GROUP BY e HAVING, e subconsulta | 15 |
| 07 Uso de Junção de tabelas: INNER JOIN, LEFT JOIN e RIGHT JOIN (pelo menos 1 exemplo de cada) | 15 |
| 08 Organização: PDF e .sql, três modelos, capturas de tela e consultas numeradas | 5 |
| **Total** | **100** |

### O que tira pontos
| Penalidade | Efeito |
|---|---|
| 01 Entrega fora do prazo (19/11/2026, até 23h55) ou fora do Portal do Aluno | Nota zero |
| 02 Arquivo corrompido ou incompleto | Item zerado |
| 03 Solução sem relação com o tema CitizenTech | Até −50 pts |
| 04 Consulta incompleta ou que não executa | Até −10 pontos por consulta |
| 05 Ausência do Modelo Conceitual, Lógico ou do Dicionário de Dados | Até −10 pontos por ausência |

### Entregáveis e formato do .zip
- [ ] PDF: levantamento, três modelos do Data Modeler, dicionário e enunciado das 10 consultas.
- [ ] Arquivo .sql, **nesta ordem**: tabelas, 50 INSERTs, 10 consultas numeradas, UPDATE e DELETE.
- [ ] Capturas de tela da execução no Oracle: tabelas, INSERTs, consultas, UPDATE e DELETE.
- [ ] **Formato:** "Um .zip somente com o PDF e o .sql. Capa com nomes, RM e turma. 19/11/2026, até 23h55, sem prorrogação."
- ⚠ Ver divergências acima (50 × 60 registros; capturas × "somente PDF e .sql"; .txt de identificação da regra geral × "capa").

### Apresentação presencial (vale 30% da nota — 23 a 27/11, na aula da disciplina)
| Critério | Pontos |
|---|---|
| 01 Problema CitizenTech, público beneficiado e papel do banco | 15 |
| 02 Modelos conceitual, lógico e relacional, e o dicionário de dados | 15 |
| 03 Criação das tabelas em execução no Oracle | 15 |
| 04 CRUD em execução: inclusão, atualização e exclusão | 15 |
| 05 Consultas de filtro, agregação e subconsulta | 20 |
| 06 INNER JOIN, LEFT JOIN, RIGHT JOIN e respostas de qualquer integrante | 20 |
| **Total** | **100** |

---

## 3. Python (Computational Thinking Using Python)

### Objetivo / detalhes da entrega
- **Objetivo:** desenvolver uma aplicação em Python relacionada ao tema da Global Solution, aplicando os conceitos e as tecnologias estudadas na disciplina. "Escolham funcionalidades específicas e coerentes ao tema proposto, evitando soluções muito genéricas (como por exemplo, cadastro de usuários)."
- **Entrega 1 — Desenvolvimento da Solução:** arquivos de código fonte em Python (.py): scripts estruturados, comentados e prontos para execução.
- **Entrega 2 — Documentação e Guia de Execução (pdf):** descrição do problema, escopo do projeto, lógica de programação aplicada e resultados esperados. Se necessário, instruções de configuração do ambiente, instalação de dependências e comandos para rodar o programa.

### Requisitos

**01 — Código fonte em Python (50 pontos)**
- [ ] Menus (5,0) — Estrutura de menus e submenus com as principais funcionalidades do sistema.
- [ ] Interação com usuário (4,0) — Entrada de dados com utilização adequada de variáveis e Saída de dados utilizando f-strings.
- [ ] Estruturas de decisão (6,0) — Aplicar adequadamente as estruturas match-case e if-elif-else.
- [ ] Estruturas de repetição (6,0) — Aplicar adequadamente as estruturas while e for.
- [ ] Sequências (8,0) — Utilizar estruturas sequenciais como Listas, Tuplas, Strings, Dicionários, Sets para armazenar e manipular dados.
- [ ] Funções (6,0) — Uso adequado de funções, passagem de parâmetros e retorno.
- [ ] Persistência (4,0) — Armazenar informações de forma permanente em Arquivos (.txt, .csv ou .json) ou em Banco de Dados Oracle.
- [ ] Usabilidade (6,0) — Garantir uma boa usabilidade apresentando mensagens claras e objetivas que auxiliem o usuário na utilização do sistema.
- [ ] Organização do código fonte e Comentários (5,0) — Organização geral do código fonte e nomenclatura adequada de variáveis e utilização de comentários para esclarecer a lógica ou escolhas de implementação.

**02 — Documentação (20 pontos)**
- [ ] Capa (3,5) — Indicar RM e nome dos integrantes do grupo.
- [ ] Sumário (3,5) — Índice indicando as seções do documento e paginação.
- [ ] Descritivo (10,0) — Descrição completa do projeto, incluindo objetivos, justificativa e descrição das funcionalidades implementadas.
- [ ] Formatação (3,0) — Formatação e organização geral do documento.

**Proibições (derivadas de "O que tira pontos")**
- [ ] **NÃO** usar Classes / Orientação a Objetos (nota zero).
- [ ] **NÃO** usar List Comprehension (−15 pts por ocorrência).

### Pontuação da entrega
| Critério | Pontos |
|---|---|
| 01 Código Fonte | 50 |
| 02 Documentação | 20 |
| 03 Apresentação | 30 |
| **Total** | **100** |

### O que tira pontos
| Penalidade | Efeito |
|---|---|
| 01 Entrega fora do prazo ou fora do Portal do Aluno | −25 pts |
| 02 Arquivo corrompido, incompleto ou sem o .txt de identificação | −25 pts |
| 03 Solução sem relação com o tema CitizenTech | −100 pts (nota zero) |
| 04 Utilização de Classes e Orientação a Objetos | −100 pts (nota zero) |
| 05 Uso de List Comprehension | −15 pts (por ocorrência) |
| 06 Ausência na apresentação presencial | −30 pts (referente à apresentação) |

### Entregáveis e formato do .zip
- [ ] Um único arquivo compactado em formato .ZIP contendo:
  - [ ] Código fonte em Python (arquivos .py)
  - [ ] Arquivo em formato PDF com a documentação do projeto
  - [ ] .txt de identificação (não está na lista de entregas, mas a ausência tira −25 pts — ver penalidade 02)

### Apresentação presencial (vale 30% da nota / 30 pts — 23 a 27/11, na aula da disciplina)
| Critério | Pontos |
|---|---|
| 01 Apresentação da equipe, da solução proposta e da responsabilidade da aplicação dentro do contexto geral do projeto | 5 |
| 02 Apresentação da estrutura do código, com as devidas abstrações, módulos e eventuais dependências | 5 |
| 03 Explicação das principais funções/procedimentos que compõem o projeto, e seus parâmetros de entrada e retorno | 5 |
| 04 Explicação e justificativa para o uso das estruturas de dados e o fluxo da informação processada | 5 |
| 05 Domínio técnico de cada integrante do grupo e respostas às perguntas do professor | 10 |
| **Total** | **30** |

---

## 4. Java (Domain Driven Design Using Java)

### Objetivo / detalhes da entrega
- "Construam o back-end da solução CitizenTech do grupo: uma API RESTful em Java com Spring Boot, que guarda os dados no Oracle da FIAP, fica publicada na internet e é consumida pelo front-end do grupo."
- **O domínio:** entidades e regras saem do problema que o grupo escolheu. "Nada de CRUD genérico de usuário e produto: a API fala a língua do cidadão atendido."
- **A API:** Spring Boot com DAO em JDBC, DTOs com validação, exceções tratadas num handler global e CORS liberado para o front.
- **No ar:** deploy da API com Docker no Render.

**Arquitetura esperada:** Front-end (rodando local ou publicado) —HTTP + JSON, com CORS→ API Spring Boot (em Docker, publicada no Render) —JDBC / DataSource→ Oracle FIAP (tabelas e sequences do grupo).

**Dentro da API — um pacote por responsabilidade:**
| Pacote | Responsabilidade |
|---|---|
| `model` | entidades do domínio |
| `dao` | acesso ao banco com JDBC |
| `dto` | entrada e saída da API |
| `controller` | rotas REST e status HTTP |
| `exception` | erros do domínio |
| `handler` | JSON de erro padronizado |
| `config` | CORS |

**O padrão dos endpoints (exemplo):**
| Método | Rota (exemplo) | Sucesso | Erros esperados |
|---|---|---|---|
| POST | /ocorrencias | 201 + Location | 400 · 409 |
| GET | /ocorrencias | 200 | — |
| GET | /ocorrencias/{id} | 200 | 404 |
| PUT | /ocorrencias/{id} | 200 | 400 · 404 · 409 |
| DELETE | /ocorrencias/{id} | 204 | 404 · 409 |
| GET | /ocorrencias/{id}/atualizacoes | 200 | 404 |
| POST | /ocorrencias/{id}/atualizacoes | 201 + Location | 400 · 404 |

"Troquem 'ocorrências' pelos recursos do domínio do grupo. 409 = regra de negócio violada ou remoção de registro com filhos. Método não suportado: 405. Erro inesperado: 500 com mensagem genérica." (⚠ as rotas são **exemplo** do PDF.)

### Requisitos

**Domínio e persistência**
- [ ] 01 Modelagem do domínio — No mínimo 3 entidades tiradas do problema do grupo, com pelo menos um relacionamento 1:N entre elas.
- [ ] 02 Banco Oracle — Tabelas no Oracle da FIAP no padrão da disciplina: `tb_nome`, colunas `cd_`, `nm_`, `ds_`, `dt_`… e sequence `sq_tb_nome`, com a chave estrangeira do 1:N.
- [ ] 03 DAO com JDBC — Um DAO por entidade, com o DataSource recebido pelo construtor e PreparedStatement. JPA, Hibernate e Spring Data não são aceitos.
- [ ] 04 CRUD completo — Cadastrar, listar, buscar por id, atualizar e remover para cada entidade, mais as rotas aninhadas do relacionamento 1:N.
- [ ] 05 DTOs — DTOs de entrada e de saída: a API nunca recebe nem devolve o model direto. Conversão com ModelMapper.
- [ ] 06 Regra de negócio — Pelo menos uma regra do domínio além do CRUD (ex.: não agendar num horário já ocupado), com exceção própria. *(o "ex." é exemplo do PDF)*

**Contrato HTTP e publicação**
- [ ] 07 Validações — Bean Validation nos DTOs de entrada (@NotBlank, @Size, @Email, @Positive, @Future…), ativada com @Valid no controller.
- [ ] 08 Tratamento de exceções — Exceções próprias e um @RestControllerAdvice que devolve todo erro num JSON padronizado, sem stack trace nem detalhes do SQL.
- [ ] 09 Status HTTP corretos — 201 com Location no cadastro, 200, 204, 400, 404, 405 e 409, cada um no caso certo.
- [ ] 10 CORS — Liberar o CORS na API para que o front consiga chamar os endpoints.
- [ ] 11 Deploy — Dockerfile multi-stage e API publicada no Render.
- [ ] 12 Integração com o front — O front-end do grupo lista e cadastra dados chamando a API. Não precisa estar publicado.

### Pontuação da entrega (vale 70 pts — entrega 70 + apresentação 30 = 100 pts)
| Critério | Pontos |
|---|---|
| 01 Modelagem do domínio, relacionamento 1:N e script SQL | 5 |
| 02 DAO com JDBC e CRUD completo funcionando | 15 |
| 03 DTOs e validações com Bean Validation | 10 |
| 04 Controllers, rotas e status HTTP corretos | 10 |
| 05 Exceções próprias, handler global e regra de negócio | 10 |
| 06 CORS e integração com o front do grupo | 5 |
| 07 Deploy no Render funcionando | 5 |
| 08 Documentação técnica em PDF | 10 |
| **Total da entrega** | **70** |

### O que tira pontos
| Penalidade | Efeito |
|---|---|
| 01 Entrega fora do prazo ou fora do Portal do Aluno | Nota zero |
| 02 .zip corrompido, vazio ou sem o código-fonte do projeto | Nota zero |
| 03 Código copiado de outro grupo ou de projeto pronto | Nota zero |
| 04 Solução sem relação com o tema CitizenTech | −30 pts |
| 05 Persistência com JPA, Hibernate ou Spring Data no lugar do JDBC | −20 pts |
| 06 API fora do ar ou link quebrado no momento da correção | −10 pts |
| 07 Usuário ou senha do banco no código entregue | −10 pts |
| 08 Erro devolvido como página HTML ou com stack trace e SQL | −5 pts |

"Os descontos valem sobre a nota final da disciplina (100 pts), se somam, e a nota mínima é zero."

### Entregáveis e formato do .zip
- [ ] O projeto Spring Boot completo, com o Dockerfile (**sem a pasta target**)
- [ ] O script SQL de criação das tabelas e sequences
- [ ] A documentação técnica em PDF (conteúdo abaixo)
- [ ] Um README.md ou .txt na raiz, com integrantes e RM, como rodar o projeto, a URL da API no Render e o link do vídeo
- [ ] **Formato:** um único .zip enviado na entrega de DDD do Portal do Aluno.
- [ ] **Vídeo:** até 5 minutos, no YouTube não listado: o front do grupo funcionando integrado à API e a explicação do sistema.

**O que vai na documentação (PDF):**
- [ ] 01 Capa e links — Integrantes com RM e os links da API e do vídeo
- [ ] 02 A solução — O problema do cidadão, quem usa a solução e o que a API resolve
- [ ] 03 Diagrama de classes — Os models com atributos, tipos e o relacionamento entre eles
- [ ] 04 Modelo do banco — DER com tabelas, chaves primárias e a chave estrangeira do 1:N
- [ ] 05 Endpoints — Método, rota, status e um exemplo de JSON de entrada e de saída
- [ ] 06 Estrutura — Os pacotes do projeto e a responsabilidade de cada um
- [ ] 07 Regras e validações — A regra de negócio e as validações de cada DTO de entrada
- [ ] 08 Deploy — Como a API foi publicada e os nomes das variáveis de ambiente, sem os valores

### Apresentação presencial (vale 30 pts — 23 a 27/11, na aula da disciplina)
| Critério | Pontos |
|---|---|
| 01 Demonstração da API publicada pelo Insomnia ou Postman, com o CRUD funcionando | 8 |
| 02 Erros ao vivo: um cadastro inválido (400) e um id que não existe (404) | 4 |
| 03 Arquitetura: o caminho de uma requisição do controller ao banco, passando por DTO e DAO | 6 |
| 04 Domínio: as entidades, o relacionamento 1:N e a regra de negócio | 4 |
| 05 Perguntas do professor sobre o código, respondidas por qualquer integrante | 8 |
| **Total da apresentação** | **30** |

"Nota final da disciplina: entrega (70 pts) + apresentação (30 pts) = 100 pts."

---

## 5. Front-end (Front-End Design Engineering)

### Objetivo / detalhes da entrega
- Utilizar **REACT + VITE + TYPESCRIPT**, com arquitetura modular e aplicação **SPA**. Integração de APIs alinhada ao backend que consuma o endpoint desenvolvido em Domain Driven Design Using Java. Experiência coesa e responsiva em todos os dispositivos, com foco em acessibilidade e usabilidade. Usar **GITHUB** para versionamento.

**1. Objetivo**
- Construir — Aplicação SPA funcional com componentes reutilizáveis, rotas e tipagem TypeScript.
- Integrar — Consultar e alterar dados reais por meio de endpoints da API REST Java.
- Adaptar — Interface com Tailwind CSS responsiva para mobile, tablet e desktop.
- Validar — Formulários com validações, estados de carregamento e mensagens claras.
- Publicar — Aplicação na Vercel, API Java remota e código no GitHub.
- Documentar — README completo, vídeo no YouTube e demonstração oral do projeto.

**2. Tecnologias e execução**
- Obrigatórias — React, Vite, TypeScript, Tailwind CSS.
- Arquitetura — Separar componentes, páginas, serviços e tipos em arquivos organizados.
- Requisições — Usar **Fetch API** para chamadas HTTP. **Axios e outras bibliotecas de requisição não estão autorizadas.**
- Execução local — A aplicação deve iniciar com os comandos de instalação e execução descritos no README.
- Código próprio — Não substituir a implementação exigida por templates prontos ou frameworks alternativos.

**3. Páginas e responsividade** (título no PDF: "PÁGINAS E RESPONVIDADE")
- Institucionais — Home, Integrantes, Sobre, FAQ e Contato: cinco rotas acessíveis.
- Solução — No mínimo duas páginas adicionais, distintas, dedicadas à solução do desafio.
- Integrantes — Criação de rotas estáticas e pelo menos uma rota com parâmetro.
- Rotas — Formulários com validações, estados de carregamento e mensagens claras.
- Telas — Mobile 390 × 844; tablet 768 × 1024; desktop 1440 × 900 px.
- Integridade — Sem rolagem horizontal indevida, cortes ou sobreposições nas resoluções avaliadas.
- ⚠ No PDF os rótulos "Integrantes" e "Rotas" parecem trocados em relação ao texto (reproduzidos como estão).

**4. API Java, deploy e vídeo**
- API obrigatória — API REST de Domain Driven Design Using Java publicada em URL remota.
- GET — Ao menos uma consulta real, exibindo dados da API na interface.
- Escrita — Ao menos uma operação real de POST, PUT, PATCH ou DELETE.
- Vercel — Frontend publicado e acessível; rotas e integração devem funcionar na versão remota.
- YouTube — Vídeo público ou não listado, com duração máxima de **três minutos**, mostrando aplicação e API.
- Sem simulações — Mocks e APIs genéricas não substituem a integração obrigatória com a API Java.

**5. GitHub, README e entrega**
- GitHub — Repositório público; mínimo de **cinco commits por integrante e quinze no total**.
- README — Título, objetivo, tecnologias, estrutura, integrantes, execução, GitHub, Vercel, API, YouTube e contato.
- Arquivo — Um ZIP de **até 50 MB** com código-fonte, configurações, recursos e README; **não incluir node_modules**.
- Portal — Somente o representante envia o ZIP no Portal do Aluno, dentro do prazo.
- Outros canais — E-mail, Teams ou link isolado não substituem a submissão obrigatória no Portal.

### Requisitos

**01 — Construção do projeto (10,0)**
- [ ] React + Vite (2,0) — Configuração React com Vite e scripts válidos no package.json.
- [ ] TypeScript (2,0) — Código próprio da aplicação em arquivos .ts e .tsx.
- [ ] Estrutura de pastas (2,0) — Pastas de componentes, páginas, serviços e tipos, ou equivalentes.
- [ ] Tipagem (2,0) — Tipos ou interfaces aplicados a props, estados e dados principais.
- [ ] Execução local (2,0) — npm install e npm run dev iniciam a aplicação sem erro impeditivo.

**02 — Componentização, páginas e rotas (10,0)**
- [ ] Componentes reutilizáveis (2,0) — Ao menos dois componentes próprios reaproveitados em duas ou mais partes.
- [ ] Separação de responsabilidades (2,0) — Páginas, componentes e serviços mantidos em arquivos específicos.
- [ ] Páginas obrigatórias (2,0) — Cinco páginas institucionais e duas páginas adicionais da solução.
- [ ] Rotas estáticas e dinâmica (2,0) — Criação de rotas fixas e ao menos uma rota com parâmetro.
- [ ] Navegação funcional (2,0) — Menus e links corretos; acesso direto às rotas sem erros.

**03 — Tailwind CSS e responsividade (8,0)**
- [ ] Tailwind CSS (2,0) — Configuração correta e classes utilitárias como estilização principal.
- [ ] Mobile (1,5) — Interface funcional em 390 × 844 px.
- [ ] Tablet (1,5) — Interface funcional em 768 × 1024 px.
- [ ] Desktop (1,5) — Interface funcional em 1440 × 900 px.
- [ ] Integridade do layout (1,5) — Sem cortes, sobreposições ou rolagem horizontal indevida.

**04 — Integração com API Java (18,0)**
- [ ] API remota (3,0) — API Java acessível em URL pública, indicada no README.
- [ ] Consulta GET (3,0) — Buscar dados reais e apresentá-los na interface.
- [ ] Operação de escrita (4,0) — Executar ao menos uma operação POST, PUT, PATCH ou DELETE.
- [ ] Camada de serviços (2,0) — Requisições organizadas em funções ou arquivos de serviço.
- [ ] Tratamento de estados (3,0) — Mostrar loading, erro de requisição e ausência de dados.
- [ ] Tipagem de respostas (3,0) — Utilizar tipos/interfaces TypeScript para dados da API.

**05 — Formulários e experiência do usuário (7,0)**
- [ ] Formulário estruturado (1,5) — Campos identificados e adequados à finalidade do projeto.
- [ ] Validação (1,5) — Campos obrigatórios e formatos verificados antes de processar.
- [ ] Mensagens (1,5) — Exibir erro de preenchimento e confirmação de sucesso.
- [ ] Feedback da API (1,5) — Indicar resultado ou falha das operações remotas.
- [ ] Usabilidade (1,0) — Campos legíveis, botões claros e fluxo compreensível.

**06 — Deploy na Vercel (7,0)**
- [ ] Publicação (2,0) — Frontend disponível em URL pública da Vercel.
- [ ] URL no README (1,0) — Link correto da aplicação publicada no documento.
- [ ] Carregamento (2,0) — Aplicação abre sem erros que impeçam o uso.
- [ ] Rotas e API (2,0) — Navegação e integração funcionam no ambiente publicado.

**07 — GitHub, README e vídeo (10,0)**
- [ ] Repositório público (1,0) — GitHub acessível com a versão final do projeto.
- [ ] Histórico de commits (2,0) — Cinco commits por integrante e ao menos quinze no total.
- [ ] README — identificação (2,0) — Título, objetivo, tecnologias, pastas e dados dos integrantes.
- [ ] README — execução e links (2,0) — Comandos e URLs de GitHub, Vercel, API e YouTube.
- [ ] Vídeo no YouTube (3,0) — Vídeo de até três minutos com funcionalidades e integração API.

### Pontuação da entrega
| Critério | Pontos |
|---|---|
| 01 [Construção do Projeto] | 10,0 |
| 02 [Componentização, Páginas e Rotas] | 10,0 |
| 03 [Tailwind, CSS e Responsividade] | 8,0 |
| 04 [Integração com API Java] | 18,0 |
| 05 [Formulários e Experiência do Usuário] | 7,0 |
| 06 [Deploy na Vercel] | 7,0 |
| 07 [Github, Readme e Vídeo] | 10,0 |
| 08 [Apresentação presencial] | 30,0 |
| **Total** | **100,0** |

(Os nomes aparecem entre colchetes no próprio PDF; aqui não são exemplos, são os nomes reais dos critérios.)

### O que tira pontos
"Penalidades relacionadas ao formato de entrega e à possibilidade de executar e corrigir o projeto."

| Penalidade | Efeito |
|---|---|
| 01 Arquivo .ZIP maior que 50 MB — o arquivo compactado ultrapassa o limite máximo de 50 MB | −2,0 pontos |
| 02 Pasta node_modules incluída — deverá ser instalada por meio do gerenciador de pacotes | −3,0 pontos |
| 03 Arquivos essenciais ausentes — a entrega não contém arquivos indispensáveis para abrir ou executar o projeto | −10,0 pontos |
| 04 Uso de biblioteca de requisições não autorizada — Axios ou outra biblioteca HTTP em substituição à Fetch API | −10,0 pontos |
| 05 Entrega sem o arquivo ZIP obrigatório — apenas links externos, sem anexar o ZIP no Portal do Aluno | Nota 0 |
| 06 Uso de template pronto — template, tema ou projeto pronto como base substancial da entrega | Nota 0 |
| 07 Uso de tecnologia proibida — substituição de React + Vite por outro framework ou estrutura, como Angular, Vue, Next.js ou Create React App | Nota 0 |
| 08 Projeto incompatível com a proposta — não é aplicação própria em React + Vite + TypeScript ou não corresponde ao desafio | Nota 0 |
| 09 Plágio ou trabalho substancialmente idêntico — cópia integral ou substancial de outro grupo ou fonte | Nota 0 + ocorrência |

### Entregáveis e formato do .zip
- [ ] Um único arquivo compactado (.ZIP), até 50 MB, sem node_modules, contendo:
  - [ ] Arquivos do projeto, organizados corretamente, incluindo: Páginas HTML; Estilos CSS; Pasta /assets com imagens, ícones e mídias (se houver)
  - [ ] Arquivo de documentação README.md, obrigatoriamente contendo todos os itens do **item 7: GitHub, README e vídeo**
- [ ] Entrega **exclusivamente pelo Portal do Aluno**, na área da disciplina, anexando o .ZIP no prazo. "NÃO SERÃO ACEITAS ENTREGAS POR E-MAIL, MICROSOFT TEAMS OU QUALQUER OUTRO MEIO DE COMUNICAÇÃO!!"
- [ ] Somente o representante envia o ZIP.
- [ ] .txt de identificação (regra geral: "um .txt em cada .zip").
- ⚠ O slide de entregas fala em "Páginas HTML" e "Estilos CSS", herança aparente de um modelo HTML/CSS; a stack exigida é React + Vite + TypeScript + Tailwind.

### Apresentação presencial (vale 30% da nota / 30 pts — 23 a 27/11, na aula da disciplina)
"Todos os integrantes deverão participar efetivamente da apresentação."

| Critério | Pontos |
|---|---|
| Apresentação do problema e contexto — explicar objetivamente qual problema foi identificado, seu contexto e relevância | 3,0 |
| Explicação da solução desenvolvida — informações organizadas, sequência lógica entre problema, solução, demonstração e técnica | 3,0 |
| Demonstração das páginas e navegação — páginas obrigatórias, páginas da solução, menu e navegação | 3,0 |
| Demonstração da responsividade — mobile, tablet e desktop | 3,0 |
| Demonstração de JavaScript e formulário — ao vivo: menu mobile, interações, validação e feedback do formulário | 3,0 |
| Domínio técnico de HTML, CSS e JavaScript — decisões de estrutura, estilo, responsividade e interatividade | 4,0 |
| Domínio técnico de HTML, CSS e JavaScript — *(linha repetida no PDF, mesmo texto)* | 4,0 |
| Participação dos integrantes — participação oral efetiva de todos; "a simples presença sem participação não caracteriza participação" | 4,0 |
| Respostas às perguntas do professor — funcionamento, código, decisões técnicas e contribuição da equipe | 3,0 |
| **Total** | **30,0** |

⚠ **Divergência no PDF:** a linha "Domínio técnico de HTML, CSS e JavaScript" aparece **duas vezes** (4,0 + 4,0); só com a duplicata a soma fecha em 30,0. Provável erro de digitação dos professores.

---

## 6. Engenharia de Software & Modelo de Negócio (Software Engineering and Business Model)

### Objetivo / detalhes da entrega
- "A equipe deverá documentar e defender a CitizenTech desenvolvida para a Global Solution, explicando qual problema do cidadão ela resolve, como funciona e como se sustenta."
- "O documento deverá conectar o modelo de negócio ao produto: backlog, diagramas e protótipo devem representar a mesma solução. A precificação, o ROI e o SLA devem partir desse mesmo escopo."
- "Nesta disciplina, a entrega é documental. As telas podem utilizar o protótipo ou a aplicação desenvolvida pelo grupo nas demais disciplinas."
- Estrutura própria: 12 blocos documentais (100 pts, peso 70%) + **vídeo pitch** (dentro dos 100) + backlog no **Jira ou Trello** + apresentação presencial (100 pts próprios, peso 30%).

### Requisitos

**Estrutura do documento (5 pts)** — "Um único PDF deverá reunir os conteúdos da disciplina, com identidade visual do grupo e organização que permita localizar e ler cada artefato."
- [ ] Capa e identificação (1) — Nome da empresa e da solução, turma, nomes completos e RMs de todos os integrantes.
- [ ] Links do projeto (1) — Incluir no PDF os links do backlog e do pitch. O link do protótipo ou da solução é opcional.
- [ ] Organização (1) — Sumário, seções na sequência dos requisitos e páginas numeradas.
- [ ] Sumário executivo (1) — Síntese do problema, solução, público, diferenciais e viabilidade do projeto.
- [ ] Leitura e referências (1) — Diagramas e prints legíveis, com fontes e referências identificadas.

**Negócio e Business Model Canvas (10 pts)** — "Explicar a oportunidade identificada e o funcionamento do negócio. O BMC deverá sintetizar a proposta e manter coerência entre seus nove blocos."
- [ ] Problema e oportunidade (3) — Público afetado, dores e impactos. Sustentar o problema com evidências e fontes.
- [ ] Solução proposta (2) — Funcionamento, tecnologias aplicadas, benefícios e relação com CitizenTech e os ODS pertinentes.
- [ ] Modelo de negócio (2) — Quem usa, quem paga, fonte de receita, relacionamento B2B/B2C/B2B2C e tipo de inovação justificado.
- [ ] Business Model Canvas (3) — Apresentar os nove blocos completos e legíveis, coerentes com o público, a solução e sua operação.

**Mercado e benchmark (10 pts)** — "Analisar alternativas reais para o mesmo problema e demonstrar em que a solução do grupo se diferencia. Toda informação pesquisada deverá indicar fonte e data."
- [ ] Mercado-alvo (2) — Definir o segmento de clientes e o contexto em que o público utilizará a solução.
- [ ] Alternativas existentes (4) — Pesquisar ao menos duas alternativas diretas ou indiretas. Justificar quando não houver concorrente direto.
- [ ] Comparação e diferenciais (4) — Comparar público, funcionalidades, preços disponíveis e limitações. Fundamentar a vantagem competitiva.

**Backlog do produto (10 pts)** — "Disponibilizar o backlog completo no Jira ou Trello. Cada História de Usuário deverá estar em um card próprio, vinculada a uma funcionalidade e detalhada para avaliação."
- [ ] Funcionalidades e gestão (1) — Organizar por funcionalidade, prioridade, responsável e status, mostrando a evolução do trabalho.
- [ ] Histórias de Usuário em 3W (3) — Escrever no formato: Eu, como [perfil], quero [ação], para [benefício]. *(os colchetes são o molde do formato, não placeholder a manter)*
- [ ] Requisitos Funcionais (RF) (3) — Identificar os comportamentos esperados do sistema e relacioná-los à HU correspondente.
- [ ] Requisitos Não Funcionais (RNF) (2) — Definir qualidades com metas verificáveis e relacionar os requisitos pertinentes à HU.
- [ ] Regras de Negócio (RN) (1) — Registrar políticas, condições e restrições do negócio aplicáveis a cada história.

**Casos de uso (10 pts)** — "Incluir no PDF o diagrama geral e três casos de uso detalhados. Os diagramas devem estar legíveis no documento, mesmo quando enviados também em arquivos separados."
- [ ] Diagrama geral (3) — Representar a solução completa com atores, limite do sistema, casos de uso nomeados e associações.
- [ ] Relações e explicação (2) — Usar include, extend e generalização quando aplicáveis. Explicar o diagrama e vinculá-lo às HUs.
- [ ] Três casos de uso detalhados (3) — Para cada caso: ID, objetivo, ator, gatilho, pré-condições, pós-condições e fluxo principal numerado.
- [ ] Alternativas e exceções (2) — Explicar condições, caminhos alternativos e falhas de cada caso detalhado, com as RF e RN relacionadas.

**Diagramas de atividades (5 pts)** — "Os três diagramas de atividades deverão estar no PDF, um para cada caso de uso detalhado. Arquivos separados podem complementar a entrega, mas não substituem os diagramas no documento."
- [ ] Correspondência com o caso de uso (1) — Identificar o caso representado e manter coerência com seus fluxos, requisitos e regras de negócio.
- [ ] Fluxo principal (2) — Representar início, fim e sequência das atividades com notação adequada e leitura clara.
- [ ] Decisões, alternativas e exceções (1) — Mostrar condições nas decisões e os caminhos alternativos ou de erro previstos no processo.
- [ ] Responsabilidades (1) — Indicar quem executa cada atividade, usando raias quando houver divisão de responsabilidades.

**UX e protótipo (10 pts)** — "Apresentar prints do protótipo ou da própria solução no PDF. O link é opcional. O grupo pode usar Lovable, Figma ou Figma Make, inclusive com IA, ou a solução que irá desenvolver."
- [ ] Jornada do usuário (3) — Representar nas telas o fluxo principal e os estados relevantes, como confirmação, erro e ausência de dados.
- [ ] Evidências das telas (2) — Incluir prints legíveis, com nome e finalidade de cada tela e relação com as HUs correspondentes.
- [ ] Heurísticas de Nielsen (3) — Para cada tela apresentada, identificar e justificar as heurísticas pertinentes com exemplos visíveis.
- [ ] UX Writing (2) — Explicar o tom de voz e as escolhas de rótulos, instruções, ações e mensagens de erro ou sucesso.

**Precificação da solução (10 pts)** — "Demonstrar como o grupo formou o preço apresentado ao cliente. Os valores deverão partir do escopo da solução e de premissas explícitas e justificadas."
- [ ] Custos e despesas (2) — Identificar custos diretos e indiretos e despesas consideradas. Informar fontes ou hipóteses das estimativas.
- [ ] Valor da hora técnica (2) — Demonstrar a formação do custo por hora, considerando os custos da equipe e as horas produtivas.
- [ ] Esforço em Hora/Homem (3) — Informar as horas estimadas de trabalho e o valor total correspondente.
- [ ] Preço final ao cliente (3) — Apresentar o preço final e explicar o lucro considerado.

**Retorno do investimento — ROI (5 pts)** — "Demonstrar o retorno esperado para o cliente, utilizando o preço da solução e um período de análise definido. As estimativas deverão ser justificadas."
- [ ] Investimento e período (1) — Informar investimento inicial, custos recorrentes e horizonte da análise, sem contar custos duas vezes.
- [ ] Métricas e benefícios (1) — Quantificar ganhos ou economias e explicar sua conversão em valores financeiros com premissas explícitas.
- [ ] Cálculo do ROI (2) — Apresentar o cálculo do retorno esperado para o cliente, com os valores utilizados.
- [ ] Interpretação (1) — Explicar o resultado para o cliente, as hipóteses adotadas e os limites da estimativa.

**Acordo de Nível de Serviço — SLA (5 pts)** — "Propor um SLA compatível com a solução e seu preço. Os compromissos deverão permitir verificar se o serviço foi prestado conforme o combinado."
- [ ] Escopo e disponibilidade (1) — Definir serviços, responsabilidades, dias e horários de operação e janelas de manutenção.
- [ ] Metas e medição (1) — Indicar meta de disponibilidade, período, cálculo de apuração e exclusões.
- [ ] Suporte e prioridades (1) — Definir canais, Help Desk/Service Desk, prioridades por impacto e escalonamento.
- [ ] Resposta e resolução (1) — Definir resposta e resolução por prioridade e a regra de contagem dos prazos.
- [ ] Compensações (1) — Definir condições e cálculo de multas, descontos ou créditos por descumprimento.

**Vídeo pitch (10 pts)** — "Entregar um vídeo de até 5 minutos com a voz real dos alunos e material visual de apoio."
- [ ] Problema e público (3) — Explicar quem é o cidadão afetado e apresentar evidência real da relevância do problema.
- [ ] Solução e demonstração (3) — Selecionar um recorte da solução que evidencie seu valor e demonstrá-lo brevemente, respeitando o tempo do pitch.
- [ ] Modelo de negócio (2) — Explicar a forma de receita e como o negócio se manterá viável.
- [ ] Impacto e fechamento (2) — Apresentar como medir o impacto, a relação com os ODS e por que a proposta merece destaque.

**Registro do uso de IA (10 pts)** — "O registro é obrigatório e deve retratar todo o uso de IA no projeto, com evidências. Declarações genéricas ou parciais não atendem ao critério. Se o grupo não utilizou IA, deverá declarar isso explicitamente."
- [ ] Ferramentas e finalidade (2) — Relacionar todas as ferramentas, etapas, finalidades e partes do trabalho produzidas com apoio de IA.
- [ ] Prompts e evidências (2) — Registrar prompts representativos de cada etapa e respostas aproveitadas, com trechos ou capturas legíveis.
- [ ] Revisão crítica (4) — Mostrar o que foi aceito, corrigido ou descartado e explicar a validação feita pelo grupo.
- [ ] Aprendizado (2) — Relatar o que o grupo aprendeu e como a ferramenta contribuiu ou apresentou limitações.

### Vídeo pitch — regras
- [ ] **Até 5 minutos.** "O que passar disso não é avaliado."
- [ ] **Link público:** YouTube (público ou não listado) ou Drive com acesso aberto. Testar o link numa aba anônima antes de entregar.
- [ ] **Onde entregar:** o link vai na entrega de Software Engineering and Business Model, na área de trabalhos do Portal do Aluno.
- **Vale para a premiação:** além da nota da disciplina, o pitch é usado para eleger o melhor projeto da GS (elegibilidade exige ≥ 90 no pitch).

Roteiro sugerido ("Como defender a solução em 5 minutos"):
| Tempo | Bloco | Conteúdo |
|---|---|---|
| 0:00 | O problema | Quem é o cidadão afetado e por que o problema importa. Traga um dado ou uma evidência real. |
| 0:45 | A solução | O que a CitizenTech do grupo faz e qual melhoria concreta ela entrega. |
| 1:30 | Demonstração | A solução funcionando: mostre o protótipo rodando, não só telas estáticas. |
| 3:00 | Modelo de negócio | Quem paga, quem participa do ecossistema e como a solução se sustenta e escala. |
| 4:00 | Impacto | Como o impacto será medido, quais ODS a solução atende e o fechamento. |

Dicas: áudio limpo vale mais que edição elaborada; fale com quem vai usar a solução, não com o professor; termine dizendo por que a proposta merece vencer.

### Pontuação da entrega (documental — 100 pts, peso 70%)
| Critério | Pontos |
|---|---|
| Estrutura do documento | 5 |
| Negócio e Business Model Canvas | 10 |
| Mercado e benchmark | 10 |
| Backlog do produto | 10 |
| Casos de uso | 10 |
| Diagramas de atividades | 5 |
| UX e protótipo | 10 |
| Precificação da solução | 10 |
| Retorno do investimento (ROI) | 5 |
| Acordo de Nível de Serviço (SLA) | 5 |
| Vídeo pitch | 10 |
| Registro do uso de IA | 10 |
| **Total** | **100** |

"A apresentação presencial tem rubrica própria de 100 pontos e peso de 30%."

### O que tira pontos
"A mesma falha não gera dois descontos. A perda fica limitada ao item prejudicado, considerando as evidências que ainda possam ser avaliadas."

| Penalidade | Efeito |
|---|---|
| PDF ausente, corrompido ou entregue fora do Portal — a entrega não pode ser avaliada ou não foi submetida no canal obrigatório | −100 pts (nota documental zero) |
| Capa sem identificação completa — ausência de empresa/solução, turma, nomes ou RMs | −1 pt (perda única do ponto de identificação) |
| Backlog sem acesso e sem evidências no PDF — não é possível avaliar as HUs e seus requisitos | −10 pts (desconsiderar os 10 pontos do backlog) |
| Jornada do usuário não representada — ausência de telas ou evidências do fluxo principal | −3 pts (desconsiderar os 3 pontos de jornada) |
| Pitch privado, inválido ou indisponível — não é possível assistir ao vídeo | −10 pts (desconsiderar os 10 pontos do pitch) |
| Registro de IA ausente — o grupo não declarou uso nem não uso de IA | −10 pts (desconsiderar os 10 pontos desse registro) |

"Não somar estes descontos à perda do mesmo requisito. Ausências parciais perdem só os pontos explícitos do subitem. Nota mínima = 0."

### Entregáveis e formato
- [ ] **Um único arquivo PDF**, enviado pelo representante na área de Software Engineering and Business Model, no Portal do Aluno, dentro do prazo da GS.
- [ ] No documento: capa e identificação do grupo, sumário, sumário executivo e todos os requisitos desta seção.
- [ ] Diagramas e prints legíveis, cálculos, SLA, referências e registro de uso ou não uso de IA.
- [ ] Links no próprio PDF — **obrigatórios:** backlog no Jira ou Trello e vídeo pitch. Link do protótipo ou da solução é opcional.
- [ ] Manter o acesso liberado durante toda a correção e testar os links em janela anônima antes do envio.
- [ ] Os diagramas devem estar no PDF. *(Opcional: pasta extra com os arquivos exportados para facilitar a visualização.)*
- ⚠ **Divergência com a regra geral:** aqui a entrega é **PDF único** (não .zip), então o ".txt em cada .zip" não se aplica diretamente; a identificação vai na capa.

### Apresentação presencial (100 pts próprios, vale 30% da nota — 23 a 27/11, na aula da disciplina)
| Critério | Pontos |
|---|---|
| Backlog e evolução — abrir o Jira/Trello e explicar épicos, HUs, prioridades, responsáveis e evolução até a entrega | 15 |
| Negócio e mercado — defender problema, público, BMC e diferenciais frente às alternativas pesquisadas | 15 |
| Viabilidade da solução — justificar o preço, as premissas e o cálculo do ROI e os compromissos definidos no SLA | 20 |
| Modelagem — explicar um caso de uso, seus atores e fluxos e o diagrama de atividades correspondente | 20 |
| Demonstração e UX — mostrar a jornada no protótipo, justificar decisões de UX e relacionar as telas às HUs | 15 |
| Domínio e participação — todos devem participar oralmente e responder às perguntas com domínio do conteúdo | 15 |
| **Total** | **100** |

---

## Resumo de divergências e placeholders do PDF

| # | Onde | O que | Sugestão segura |
|---|---|---|---|
| 1 | Regras gerais — Uso de IA generativa | As 3 colunas (permitido / não permitido / como declarar) são só `[ex.: ...]` | Seguir os exemplos + o "Registro do uso de IA" de Eng. Software |
| 2 | IA & Chatbot — Formato | `[ex.: um .zip com o código-fonte e o .txt de identificação do grupo]` | Fazer exatamente isso |
| 3 | IA & Chatbot — framework da API | Detalhes: "Flask, FastAPI etc"; requisito/pontuação: Flask | Usar Flask |
| 4 | Banco de Dados — registros | 50 (detalhes, pontuação, .sql) × 60 (requisito 05) | Inserir 60 |
| 5 | Banco de Dados — conteúdo do .zip | "somente PDF e .sql" × capturas de tela na lista de entregas | Capturas dentro do PDF; confirmar |
| 6 | Banco de Dados / Eng. Software / Java — identificação | Regra geral pede .txt em cada .zip; BD pede capa; Java aceita README.md ou .txt; Eng. Software é PDF único | Incluir .txt em todo .zip + capa nos PDFs |
| 7 | Python — .txt | Penalidade cita ".txt de identificação", lista de entregas não | Incluir o .txt |
| 8 | Front-end — seção 3 | Rótulos "Integrantes" e "Rotas" parecem trocados; título "RESPONVIDADE" | — |
| 9 | Front-end — apresentação | "Domínio técnico de HTML, CSS e JavaScript" duplicado (soma só fecha com a duplicata) | Confirmar com o professor |
| 10 | Front-end — entregas | Fala em "Páginas HTML" e "Estilos CSS" (stack é React/TS/Tailwind) | Entregar o projeto React completo, sem node_modules |
| 11 | Java — vídeo × Front — vídeo | Java: até 5 min (YouTube não listado); Front: até 3 min (público ou não listado) | Dois vídeos distintos, ou um de até 3 min que atenda os dois |
