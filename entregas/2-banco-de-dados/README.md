# 2 · Building Relational Database

**Primeira matéria do caminho crítico:** a Java só testa de verdade quando este script estiver rodando no Oracle da FIAP.
Base: Documento Base v1.5, seção 6 (9 tabelas, dicionário e seed), e [`docs/PLANO_DE_DESENVOLVIMENTO.md`](../../docs/PLANO_DE_DESENVOLVIMENTO.md), seção 2.2.
**Passo a passo do grupo:** [`GUIA_EXECUCAO.md`](GUIA_EXECUCAO.md).

## O que tem nesta pasta
| Arquivo | Conteúdo | Vai no .zip? |
|---|---|---|
| `zelabairro.sql` | Nesta ordem: CREATE TABLE (com `COMMENT ON TABLE`) e sequences → **60** INSERTs em todas as tabelas → 10 consultas numeradas → UPDATE com WHERE → DELETE com WHERE | Sim |
| `documentacao.pdf` | Capa (nomes, RM e turma), levantamento, 3 modelos, dicionário de dados, enunciado das 10 consultas e capturas | Sim |
| `identificacao.txt` | RM, nome e turma | Sim |
| `gerar_documentacao.py` | Gera o PDF (`uv run --with reportlab python gerar_documentacao.py`). Lê as consultas do `.sql` e as imagens de `imagens/` | Não |
| `imagens/` | Os 3 modelos exportados do Data Modeler e as capturas da execução. Os nomes estão no GUIA | Não (vão dentro do PDF) |
| `modelos/` | Projeto do Data Modeler (`.dmd`), para reabrir e editar | Não |
| `GUIA_EXECUCAO.md` | Como rodar no Oracle da FIAP, que capturas tirar, como desenhar os modelos e montar o zip | Não |

## Checklist
- [x] 9 tabelas na ordem das FKs: `tb_orgao`, `tb_bairro`, `tb_cidadao`, `tb_gestor`, `tb_categoria`, `tb_ocorrencia`, `tb_atualizacao`, `tb_apoio`, `tb_foto`
- [x] PK, FK, NOT NULL, UNIQUE e CHECK com regras da solução (código RN no comentário); sequences `sq_tb_*` (menos `tb_apoio`); `COMMENT ON TABLE` em todas
- [x] Seed: 5 órgãos, 8 categorias da tabela 6.4, 6 bairros com subprefeitura **igual a** `1-ia-chatbot/zelabairro-ia/data/depara_distrito_subprefeitura.csv`, 8 cidadãos e 3 gestores com senha em **hash BCrypt**, gestor inicial com `cd_gestor_cadastro` nulo, ocorrências nos 4 status, atualizações coerentes com a RN05, apoios respeitando a RN08 e fotos PNG via `HEXTORAW` respeitando a RN18 (60 linhas)
- [x] 10 consultas cobrindo WHERE, ORDER BY, cálculo no SELECT, COUNT/SUM/AVG/MAX/MIN + GROUP BY, HAVING, subconsulta, INNER, LEFT e RIGHT JOIN
- [x] UPDATE e DELETE com WHERE
- [x] Script testado do zero e reexecutado com DROPs num Oracle Free local (15/11): 0 erros, todas as consultas com linhas, constraints recusando dados inválidos
- [x] `documentacao.pdf` gerado por script, com espaços marcados para os modelos e as capturas; `identificacao.txt`
- [x] **Grupo:** rodar `zelabairro.sql` na conta Oracle da FIAP (GUIA, passo 1)
- [x] **Grupo:** desenhar e exportar os 3 modelos no Data Modeler para `imagens/` (GUIA, passo 4); exportados em SVG e convertidos para PNG em alta resolução (18/11)
- [x] **Grupo:** tirar as 14 capturas da execução para `imagens/` (GUIA, passo 3)
- [x] **Grupo:** regenerar o PDF e conferir que não sobrou nenhum quadro "INSERIR IMAGEM"
- [x] Zip `ZelaBairro_BD_1TDSPV.zip` (fica só na pasta local: `entregas/.gitignore` ignora *.zip) montado **somente com o PDF, o `.sql` e o `.txt`** (capturas dentro do PDF); script retestado do zero num Oracle Free local em 18/11: 0 erros, 60 linhas, 10 consultas com resultado
- [ ] **Grupo:** enviar o zip no Portal até 19/11 23h55

## Critério do PDF → onde está atendido
Fonte: [`docs/CRITERIOS_DE_ACEITE.md`](../../docs/CRITERIOS_DE_ACEITE.md), seção 2. "PDF §n" é a seção do `documentacao.pdf`; "SQL" é o `zelabairro.sql`.

### Requisitos 1/3 — estrutura
| Requisito | Onde está atendido | Status |
|---|---|---|
| 01 Mínimo de 6 tabelas, contando a associativa | 9 tabelas, PARTE 1 do SQL; PDF §2 | OK |
| 02 Dois 1:N e um N:N com associativa | 9 relacionamentos 1:N e o N:N cidadão ↔ ocorrência via `tb_apoio`; PDF §2 (tabela de relacionamentos) | OK |
| 03 PK em toda tabela, FK em todo relacionamento | `pk_tb_*` nas 9 tabelas; 11 `fk_*` (inclui o autorrelacionamento do gestor) | OK |
| 04 Pelo menos um NOT NULL, UNIQUE e CHECK com regra da solução | Ex.: `ck_tb_ocorrencia_st` (RN04), `ck_tb_foto_tipo`/`tamanho` (RN18), `uk_tb_cidadao_email` (RN02) | OK |
| 05 60 registros, toda tabela com registro | 60 INSERTs: 5/6/8/3/8/12/9/6/3; conferência no SQL após o COMMIT | OK |
| 06 UPDATE e DELETE com WHERE | PARTE 4 e PARTE 5 do SQL | OK |

### Requisitos 2/3 — levantamento e modelagem
| Requisito | Onde está atendido | Status |
|---|---|---|
| 01 Levantamento: problema, público, objetivo, atores, dados, perguntas e ODS | PDF §1.1 a §1.8 | OK |
| 02 Texto da própria solução | PDF §1 cita SP156, RNs, tabelas e consultas do ZelaBairro | OK |
| 03 Três desenhos no Data Modeler | PDF §2 (conceitual Barker, N:N apoia direto), §3 e §4, desenhados no Data Modeler; esquema relacional em texto no §4 | OK |
| 04 Dicionário: tabela, coluna, tipo, tamanho, nulo, chave, restrição, significado | PDF §5, com as 9 tabelas e as 7 colunas pedidas | OK |
| 05 Sem multivalorado nem grupo repetido; nomes sem espaço e sem acento | Fotos e apoios em tabelas próprias; nomes `tb_`/`cd_`/... (PDF §2 e §4) | OK |
| 06 CREATE TABLE no Oracle, na ordem das FKs, com comentário em cada tabela | PARTE 1 do SQL; `COMMENT ON TABLE` nas 9 | OK |

### Requisitos 3/3 — consultas
| Requisito | Onde está atendido | Status |
|---|---|---|
| 01 10 consultas numeradas, cada uma com pergunta da solução | CONSULTA 01 a 10 do SQL, com comentário "Pergunta:"; PDF §7 | OK |
| 02 WHERE, ORDER BY e cálculo no SELECT | WHERE em 1–4 e 7–9; ORDER BY em 1–4 e 6–10; cálculo em 2, 3, 6 e 10 | OK |
| 03 COUNT, SUM, AVG, MAX, MIN com GROUP BY + HAVING | COUNT 1, 2, 5, 6, 9, 10; SUM 6; AVG 2, 9; MAX 2, 5, 9; MIN 2, 9; HAVING 1 e 5 | OK |
| 04 Pelo menos uma subconsulta | Consulta 5 (`MAX(COUNT(*))` no HAVING) e 10 (subconsultas no FROM) | OK |
| 05 INNER, LEFT e RIGHT JOIN | INNER em 1–6, 8 e 9; LEFT em 4 e 10; RIGHT em 7 | OK |

### Pontuação da entrega (Portal, 70% da nota)
| Critério (pts) | Onde está atendido | Status |
|---|---|---|
| 01 Levantamento: problema, público, dados, perguntas e ODS (10) | PDF §1 | OK |
| 02 DER: conceitual, entidades, atributos, relacionamentos e cardinalidades (10) | PDF §2 (tabela de relacionamentos pronta) | **Grupo** (imagem do conceitual) |
| 03 Dicionário, lógico e relacional, com chaves e associativa (15) | PDF §3, §4 e §5 | Dicionário OK; **grupo** (imagens do lógico e do relacional) |
| 04 Script no Oracle: tabelas, PK, FK, NOT NULL, UNIQUE, CHECK (15) | PARTE 1 do SQL, testada em Oracle local | OK; **grupo** confirma na FIAP |
| 05 CRUD: registros em todas as tabelas, UPDATE e DELETE com WHERE (15) | PARTES 2, 4 e 5 do SQL | OK |
| 06 Consultas: filtro, cálculo, agregação com GROUP BY e HAVING, subconsulta (15) | Consultas 1–10 (ver 3/3) | OK |
| 07 Joins: INNER, LEFT e RIGHT, pelo menos 1 de cada (15) | Consultas 4, 7 e 10 + INNER nas demais | OK |
| 08 Organização: PDF e .sql, três modelos, capturas, consultas numeradas (5) | PDF com sumário e seções na ordem; SQL na ordem pedida | **Grupo** (modelos e capturas) |

### Entregáveis e formato
| Item | Onde está atendido | Status |
|---|---|---|
| PDF: levantamento, 3 modelos, dicionário e enunciado das 10 consultas | `documentacao.pdf` (§1 a §7) | OK, faltam as imagens |
| .sql na ordem: tabelas, INSERTs, 10 consultas, UPDATE e DELETE | `zelabairro.sql`, PARTES 1 a 5 | OK |
| Capturas da execução: tabelas, INSERTs, consultas, UPDATE e DELETE | Quadros reservados no PDF §6, §7 e §8 | **Grupo** |
| Zip só com PDF e .sql, capa com nomes, RM e turma; .txt da regra geral | Capa do PDF; `identificacao.txt`; comando no GUIA §6 | **Grupo** monta o zip |

### Penalidades evitadas
| Penalidade | Como foi evitada |
|---|---|
| Fora do prazo ou fora do Portal | GUIA recomenda enviar até o meio da tarde de 19/11 |
| Arquivo corrompido ou incompleto | GUIA §6 manda conferir com `unzip -l` (3 arquivos) |
| Sem relação com o tema | Todo o modelo é do ZelaBairro (zeladoria urbana, ODS 10 e 11) |
| Consulta incompleta ou que não executa | As 10 rodaram sem erro e retornaram linhas no Oracle local |
| Faltar modelo conceitual, lógico ou dicionário | Dicionário pronto; os modelos são a principal pendência do grupo |
