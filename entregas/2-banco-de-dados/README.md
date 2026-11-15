# 2 · Building Relational Database

**Primeira matéria do caminho crítico:** a Java só testa de verdade quando este script estiver rodando no Oracle da FIAP.
Base: Documento Base v1.5, seção 6 (9 tabelas, dicionário, seed) e [`docs/PLANO_DE_DESENVOLVIMENTO.md`](../../docs/PLANO_DE_DESENVOLVIMENTO.md) seção 2.2.

## O que colocar nesta pasta
| Arquivo | Conteúdo |
|---|---|
| `zelabairro.sql` | Nesta ordem: CREATE TABLE (com `COMMENT ON TABLE`) e sequences → **60** INSERTs em todas as tabelas → 10 consultas numeradas → UPDATE com WHERE → DELETE com WHERE |
| `modelos/` | Exportações do Oracle Data Modeler: conceitual, lógico e relacional |
| `capturas/` | Prints da execução (tabelas, inserts, consultas, update, delete) — também vão **dentro do PDF** |
| `documentacao.pdf` | Capa (nomes, RM, turma), levantamento, 3 modelos, dicionário de dados, enunciado das 10 consultas e capturas |
| `identificacao.txt` | RM, nome e turma |

## Checklist
- [ ] 9 tabelas na ordem das FKs: `tb_orgao`, `tb_bairro`, `tb_cidadao`, `tb_gestor`, `tb_categoria`, `tb_ocorrencia`, `tb_atualizacao`, `tb_apoio`, `tb_foto`
- [ ] PK, FK, NOT NULL, UNIQUE e CHECK com regras da solução; sequences `sq_tb_*` (menos `tb_apoio`)
- [ ] Seed: 5 órgãos, 8 categorias da tabela 6.4, bairros com subprefeitura **igual a** `1-ia-chatbot/zelabairro-ia/data/depara_distrito_subprefeitura.csv`, gestor inicial com senha em **hash** (nunca em texto), fotos minúsculas via `HEXTORAW`
- [ ] 10 consultas cobrindo WHERE, ORDER BY, cálculo no SELECT, COUNT/SUM/AVG/MAX/MIN + GROUP BY, HAVING, subconsulta, INNER, LEFT e RIGHT JOIN
- [ ] Zip **somente com o PDF e o `.sql`** (+ `.txt`), capturas dentro do PDF
