/* =====================================================================
   ZelaBairro - Global Solution 2026/2 (CitizenTech) - FIAP 1TDSPV
   Disciplina: Building Relational Database
   Banco: Oracle (o mesmo banco atende a API Java do projeto)
   Fonte do modelo: Documento Base v1.5, secao 6 (nomes sao contrato)

   Ordem deste arquivo (exigida pela disciplina):
     PARTE 1 - CREATE TABLE (ordem das FKs) + COMMENT + sequences
     PARTE 2 - 60 INSERTs (todas as tabelas com registro)
     PARTE 3 - 10 consultas numeradas
     PARTE 4 - UPDATE com WHERE
     PARTE 5 - DELETE com WHERE

   Como executar: no Oracle SQL Developer, abrir este arquivo e usar
   "Executar Script" (F5), num esquema sem estas tabelas. Para rodar de
   novo do zero, execute antes o bloco de DROP comentado logo abaixo.

   Os codigos RNxx citados nos comentarios sao as regras de negocio da
   secao 5.3 do Documento Base. Regras que um CHECK nao consegue
   verificar (ex.: RN05, RN08 "nao apoiar a propria", limite de 3 fotos
   da RN18) sao garantidas pela API Java.

   Atencao ao editar: no SQL Developer/SQL*Plus, um "-- comentario"
   DEPOIS do ";" na mesma linha impede que o comando termine. Por isso
   os comentarios ao lado dos INSERTs ficam ANTES do ";", entre
   barra-asterisco e asterisco-barra.

   Validado em 15/11/2026: executado do zero e reexecutado com o bloco
   de DROP em Oracle AI Database 26ai Free (container oficial), sem erros.
   ===================================================================== */

SET DEFINE OFF;

/* ---------------------------------------------------------------------
   (OPCIONAL) Limpeza para reexecutar o script do zero.
   Tire o comentario deste bloco somente se as tabelas ja existirem.

DROP TABLE tb_foto        CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_apoio       CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_atualizacao CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_ocorrencia  CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_categoria   CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_gestor      CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_cidadao     CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_bairro      CASCADE CONSTRAINTS PURGE;
DROP TABLE tb_orgao       CASCADE CONSTRAINTS PURGE;
DROP SEQUENCE sq_tb_foto;
DROP SEQUENCE sq_tb_atualizacao;
DROP SEQUENCE sq_tb_ocorrencia;
DROP SEQUENCE sq_tb_categoria;
DROP SEQUENCE sq_tb_gestor;
DROP SEQUENCE sq_tb_cidadao;
DROP SEQUENCE sq_tb_bairro;
DROP SEQUENCE sq_tb_orgao;
   --------------------------------------------------------------------- */


/* =====================================================================
   PARTE 1 - CRIACAO DAS TABELAS (ordem das chaves estrangeiras)
   tb_orgao, tb_bairro, tb_cidadao, tb_gestor, tb_categoria,
   tb_ocorrencia, tb_atualizacao, tb_apoio, tb_foto
   ===================================================================== */

-- 1. tb_orgao -----------------------------------------------------------
CREATE TABLE tb_orgao (
    cd_orgao     NUMBER(10)     NOT NULL,
    nm_orgao     VARCHAR2(100)  NOT NULL,
    ds_email     VARCHAR2(120)  NOT NULL,
    nr_telefone  VARCHAR2(20),
    CONSTRAINT pk_tb_orgao PRIMARY KEY (cd_orgao),
    CONSTRAINT uk_tb_orgao_nm UNIQUE (nm_orgao)
);
COMMENT ON TABLE tb_orgao IS 'Orgaos da prefeitura que executam os servicos de zeladoria (ex.: Iluminacao Publica). Cada categoria e cada gestor pertencem a um orgao.';
CREATE SEQUENCE sq_tb_orgao START WITH 1 INCREMENT BY 1 NOCACHE;

-- 2. tb_bairro ----------------------------------------------------------
CREATE TABLE tb_bairro (
    cd_bairro         NUMBER(10)    NOT NULL,
    nm_bairro         VARCHAR2(80)  NOT NULL,
    nm_subprefeitura  VARCHAR2(80)  NOT NULL,  -- mesmo nome do de-para da API de IA
    nr_populacao      NUMBER(9),
    CONSTRAINT pk_tb_bairro PRIMARY KEY (cd_bairro),
    CONSTRAINT uk_tb_bairro_nm_sub UNIQUE (nm_bairro, nm_subprefeitura),
    CONSTRAINT ck_tb_bairro_pop CHECK (nr_populacao > 0)
);
COMMENT ON TABLE tb_bairro IS 'Bairros/distritos atendidos e sua subprefeitura. A subprefeitura usa o mesmo nome do SP156 para a previsao da IA.';
CREATE SEQUENCE sq_tb_bairro START WITH 1 INCREMENT BY 1 NOCACHE;

-- 3. tb_cidadao ---------------------------------------------------------
CREATE TABLE tb_cidadao (
    cd_cidadao   NUMBER(10)     NOT NULL,
    nm_cidadao   VARCHAR2(100)  NOT NULL,
    ds_email     VARCHAR2(120)  NOT NULL,
    ds_senha     VARCHAR2(100)  NOT NULL,  -- RN15: somente o hash BCrypt, nunca a senha
    nr_telefone  VARCHAR2(20),
    dt_cadastro  DATE           DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_tb_cidadao PRIMARY KEY (cd_cidadao),
    CONSTRAINT uk_tb_cidadao_email UNIQUE (ds_email)  -- RN02: e-mail unico
);
COMMENT ON TABLE tb_cidadao IS 'Cidadaos que registram e apoiam ocorrencias. Sem CPF nem endereco (RN02, LGPD). Senha guardada so como hash BCrypt (RN15).';
CREATE SEQUENCE sq_tb_cidadao START WITH 1 INCREMENT BY 1 NOCACHE;

-- 4. tb_gestor ----------------------------------------------------------
CREATE TABLE tb_gestor (
    cd_gestor           NUMBER(10)     NOT NULL,
    nm_gestor           VARCHAR2(100)  NOT NULL,
    ds_email            VARCHAR2(120)  NOT NULL,
    ds_senha            VARCHAR2(100)  NOT NULL,  -- RN15: hash BCrypt
    cd_orgao            NUMBER(10)     NOT NULL,
    cd_gestor_cadastro  NUMBER(10),               -- RN17: nulo so no gestor do seed
    dt_cadastro         DATE           DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_tb_gestor PRIMARY KEY (cd_gestor),
    CONSTRAINT uk_tb_gestor_email UNIQUE (ds_email),  -- RN02
    CONSTRAINT fk_tb_gestor_orgao FOREIGN KEY (cd_orgao)
        REFERENCES tb_orgao (cd_orgao),
    CONSTRAINT fk_tb_gestor_cadastro FOREIGN KEY (cd_gestor_cadastro)
        REFERENCES tb_gestor (cd_gestor)            -- RN17: autorrelacionamento (quem cadastrou)
);
COMMENT ON TABLE tb_gestor IS 'Servidores da prefeitura que acessam o painel (RN16). Pertencem a um orgao e registram quem os cadastrou (RN17).';
CREATE SEQUENCE sq_tb_gestor START WITH 1 INCREMENT BY 1 NOCACHE;

-- 5. tb_categoria -------------------------------------------------------
CREATE TABLE tb_categoria (
    cd_categoria   NUMBER(10)     NOT NULL,
    nm_categoria   VARCHAR2(60)   NOT NULL,
    ds_categoria   VARCHAR2(255),
    nr_prazo_dias  NUMBER(3)      NOT NULL,
    nr_gravidade   NUMBER(1)      NOT NULL,
    cd_orgao       NUMBER(10)     NOT NULL,
    CONSTRAINT pk_tb_categoria PRIMARY KEY (cd_categoria),
    CONSTRAINT uk_tb_categoria_nm UNIQUE (nm_categoria),
    CONSTRAINT ck_tb_categoria_prazo CHECK (nr_prazo_dias > 0),                  -- prazo de referencia (RN11)
    CONSTRAINT ck_tb_categoria_gravidade CHECK (nr_gravidade BETWEEN 1 AND 5),   -- peso da RN10
    CONSTRAINT fk_tb_categoria_orgao FOREIGN KEY (cd_orgao)
        REFERENCES tb_orgao (cd_orgao)
);
COMMENT ON TABLE tb_categoria IS 'Tipos de problema de zeladoria, com prazo de referencia em dias e gravidade de 1 a 5 (tabela 6.4 do Documento Base).';
CREATE SEQUENCE sq_tb_categoria START WITH 1 INCREMENT BY 1 NOCACHE;

-- 6. tb_ocorrencia ------------------------------------------------------
CREATE TABLE tb_ocorrencia (
    cd_ocorrencia      NUMBER(10)     NOT NULL,
    ds_ocorrencia      VARCHAR2(500)  NOT NULL,
    ds_endereco        VARCHAR2(200)  NOT NULL,                     -- RN03: obrigatorio, ate 200
    st_ocorrencia      VARCHAR2(15)   DEFAULT 'ABERTA' NOT NULL,    -- RN04: nasce ABERTA
    dt_abertura        DATE           DEFAULT SYSDATE NOT NULL,     -- RN04: abertura = hoje
    dt_resolucao       DATE,                                        -- RN06: preenchida ao resolver
    nr_prazo_previsto  NUMBER(4),                                   -- RN12: nulo se a IA estiver fora
    fl_risco_atraso    CHAR(1),                                     -- RN12: nulo se a IA estiver fora
    cd_cidadao         NUMBER(10)     NOT NULL,                     -- RN01: 1 autor
    cd_categoria       NUMBER(10)     NOT NULL,                     -- RN01: 1 categoria
    cd_bairro          NUMBER(10)     NOT NULL,                     -- RN01: 1 bairro
    CONSTRAINT pk_tb_ocorrencia PRIMARY KEY (cd_ocorrencia),
    CONSTRAINT ck_tb_ocorrencia_ds CHECK (LENGTH(ds_ocorrencia) BETWEEN 10 AND 500),  -- RN03
    CONSTRAINT ck_tb_ocorrencia_st CHECK
        (st_ocorrencia IN ('ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'CANCELADA')),     -- RN04
    CONSTRAINT ck_tb_ocorrencia_dt CHECK
        (dt_resolucao IS NULL OR dt_resolucao >= dt_abertura),
    CONSTRAINT ck_tb_ocorrencia_risco CHECK (fl_risco_atraso IN ('S', 'N')),
    CONSTRAINT fk_tb_ocorrencia_cidadao FOREIGN KEY (cd_cidadao)
        REFERENCES tb_cidadao (cd_cidadao),                                         -- RN01
    CONSTRAINT fk_tb_ocorrencia_categoria FOREIGN KEY (cd_categoria)
        REFERENCES tb_categoria (cd_categoria),                                     -- RN01, RN14
    CONSTRAINT fk_tb_ocorrencia_bairro FOREIGN KEY (cd_bairro)
        REFERENCES tb_bairro (cd_bairro)                                            -- RN01, RN14
);
COMMENT ON TABLE tb_ocorrencia IS 'Problema de zeladoria registrado por um cidadao, com status, datas e a previsao da IA (prazo em dias e risco de atraso).';
CREATE SEQUENCE sq_tb_ocorrencia START WITH 1 INCREMENT BY 1 NOCACHE;

-- 7. tb_atualizacao -----------------------------------------------------
CREATE TABLE tb_atualizacao (
    cd_atualizacao  NUMBER(10)     NOT NULL,
    cd_ocorrencia   NUMBER(10)     NOT NULL,
    st_anterior     VARCHAR2(15)   NOT NULL,
    st_novo         VARCHAR2(15)   NOT NULL,
    ds_comentario   VARCHAR2(300),
    cd_gestor       NUMBER(10)     NOT NULL,                        -- RN06: quem fez a atualizacao
    dt_atualizacao  DATE           DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_tb_atualizacao PRIMARY KEY (cd_atualizacao),
    CONSTRAINT ck_tb_atualizacao_st_novo CHECK
        (st_novo IN ('ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'CANCELADA')),           -- RN04
    CONSTRAINT fk_tb_atualizacao_ocorrencia FOREIGN KEY (cd_ocorrencia)
        REFERENCES tb_ocorrencia (cd_ocorrencia),
    CONSTRAINT fk_tb_atualizacao_gestor FOREIGN KEY (cd_gestor)
        REFERENCES tb_gestor (cd_gestor)                                            -- RN06, RN16
);
COMMENT ON TABLE tb_atualizacao IS 'Historico de mudancas de status de cada ocorrencia, com comentario e o gestor que fez a mudanca (RN05, RN06).';
CREATE SEQUENCE sq_tb_atualizacao START WITH 1 INCREMENT BY 1 NOCACHE;

-- 8. tb_apoio (associativa do N:N cidadao <-> ocorrencia) ----------------
CREATE TABLE tb_apoio (
    cd_cidadao     NUMBER(10)  NOT NULL,
    cd_ocorrencia  NUMBER(10)  NOT NULL,
    dt_apoio       DATE        DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_tb_apoio PRIMARY KEY (cd_cidadao, cd_ocorrencia),  -- RN08: apoia no maximo 1 vez
    CONSTRAINT fk_tb_apoio_cidadao FOREIGN KEY (cd_cidadao)
        REFERENCES tb_cidadao (cd_cidadao),
    CONSTRAINT fk_tb_apoio_ocorrencia FOREIGN KEY (cd_ocorrencia)
        REFERENCES tb_ocorrencia (cd_ocorrencia)
);
COMMENT ON TABLE tb_apoio IS 'Tabela associativa do N:N entre cidadao e ocorrencia: o cidadao diz "eu tambem tenho esse problema" (RN08). Chave composta, sem sequence.';
-- tb_apoio nao tem sequence: a chave e composta (cd_cidadao, cd_ocorrencia).

-- 9. tb_foto ------------------------------------------------------------
CREATE TABLE tb_foto (
    cd_foto        NUMBER(10)    NOT NULL,
    cd_ocorrencia  NUMBER(10)    NOT NULL,
    bl_imagem      BLOB          NOT NULL,
    ds_tipo        VARCHAR2(20)  NOT NULL,
    nr_tamanho     NUMBER(8)     NOT NULL,
    dt_envio       DATE          DEFAULT SYSDATE NOT NULL,
    CONSTRAINT pk_tb_foto PRIMARY KEY (cd_foto),
    CONSTRAINT ck_tb_foto_tipo CHECK (ds_tipo IN ('image/jpeg', 'image/png')),     -- RN18: so JPG ou PNG
    CONSTRAINT ck_tb_foto_tamanho CHECK (nr_tamanho BETWEEN 1 AND 2097152),       -- RN18: ate 2 MB
    CONSTRAINT fk_tb_foto_ocorrencia FOREIGN KEY (cd_ocorrencia)
        REFERENCES tb_ocorrencia (cd_ocorrencia)
);
COMMENT ON TABLE tb_foto IS 'Fotos do problema (BLOB), 1:N com a ocorrencia. JPG ou PNG ate 2 MB; o limite de 3 por ocorrencia e checado na API Java (RN18).';
CREATE SEQUENCE sq_tb_foto START WITH 1 INCREMENT BY 1 NOCACHE;


/* =====================================================================
   PARTE 2 - INSERTS (60 registros no total)
     tb_orgao 5 | tb_bairro 6 | tb_cidadao 8 | tb_gestor 3 |
     tb_categoria 8 | tb_ocorrencia 12 | tb_atualizacao 9 |
     tb_apoio 6 | tb_foto 3                                  = 60
   As sequences comecam em 1, entao o comentario "cd = n" mostra o
   codigo que cada linha recebe. As FKs usam esses codigos.
   Datas relativas a hoje (TRUNC(SYSDATE) - n) para que "dias em aberto"
   e "atrasada" (RN11) facam sentido em qualquer dia de execucao.
   Senhas: ds_senha guarda apenas hash BCrypt (RN15) de uma senha de
   TESTE; a senha em texto nao esta neste arquivo.
   ===================================================================== */

-- tb_orgao (5) - tabela 6.4 ------------------------------------------------
INSERT INTO tb_orgao (cd_orgao, nm_orgao, ds_email, nr_telefone)
VALUES (sq_tb_orgao.NEXTVAL, 'Subprefeitura - Zeladoria', 'zeladoria@prefeitura.exemplo.gov.br', '(11) 3000-0001') /* cd = 1 */;
INSERT INTO tb_orgao (cd_orgao, nm_orgao, ds_email, nr_telefone)
VALUES (sq_tb_orgao.NEXTVAL, 'Iluminação Pública', 'iluminacao@prefeitura.exemplo.gov.br', '(11) 3000-0002') /* cd = 2 */;
INSERT INTO tb_orgao (cd_orgao, nm_orgao, ds_email, nr_telefone)
VALUES (sq_tb_orgao.NEXTVAL, 'Limpeza Urbana', 'limpeza@prefeitura.exemplo.gov.br', '(11) 3000-0003') /* cd = 3 */;
INSERT INTO tb_orgao (cd_orgao, nm_orgao, ds_email, nr_telefone)
VALUES (sq_tb_orgao.NEXTVAL, 'Áreas Verdes', 'areasverdes@prefeitura.exemplo.gov.br', NULL) /* cd = 4 */;
INSERT INTO tb_orgao (cd_orgao, nm_orgao, ds_email, nr_telefone)
VALUES (sq_tb_orgao.NEXTVAL, 'Trânsito e Sinalização', 'transito@prefeitura.exemplo.gov.br', '(11) 3000-0005') /* cd = 5 */;

-- tb_bairro (6) - distritos reais; nm_subprefeitura igual ao
-- depara_distrito_subprefeitura.csv da API de IA. Populacao aproximada.
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Lapa', 'Lapa', 65739) /* cd = 1 */;
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Pinheiros', 'Pinheiros', 65364) /* cd = 2 */;
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Capão Redondo', 'Campo Limpo', 268729) /* cd = 3 */;
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Itaim Paulista', 'Itaim Paulista', 224074) /* cd = 4 */;
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Sé', 'Sé', 23651) /* cd = 5 */;
INSERT INTO tb_bairro (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
VALUES (sq_tb_bairro.NEXTVAL, 'Cidade Tiradentes', 'Cidade Tiradentes', 211501) /* cd = 6 */;

-- tb_cidadao (8) - ds_senha = hash BCrypt (RN15) ---------------------------
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Ana Paula Ribeiro', 'ana.ribeiro@email.exemplo.com',
        '$2a$10$0iZbuS/ffaeDKU0KBGmpnuD9zslwOChnnLiw8v87G2YfAR/z1OjQG', '(11) 98000-0001', TRUNC(SYSDATE) - 60) /* cd = 1 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Bruno Carvalho Lima', 'bruno.lima@email.exemplo.com',
        '$2a$10$Tx8XAXpOCJyI9hjOOSZYzOreerFJeonT5ArsMQjF7S43gAgU/etby', NULL, TRUNC(SYSDATE) - 58) /* cd = 2 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Carla Mendes Souza', 'carla.souza@email.exemplo.com',
        '$2a$10$rz0UFZUFgb1FJ1iJwLwVbOOJv4yR5AGxhhSbQWYo/DwWcRU7IrieC', '(11) 98000-0003', TRUNC(SYSDATE) - 55) /* cd = 3 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Diego Fernandes Rocha', 'diego.rocha@email.exemplo.com',
        '$2a$10$h5xdTMa/Mtvmhb5vU2cqg.GeTcpJ7BauENXTAnhvlmBuLOofI57bW', NULL, TRUNC(SYSDATE) - 50) /* cd = 4 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Elaine Cristina Alves', 'elaine.alves@email.exemplo.com',
        '$2a$10$77hwuJnfoX7MuZuZ9oJzAucYWya3plZ.d4MDU0x0CFZPS7X8O8c5q', '(11) 98000-0005', TRUNC(SYSDATE) - 45) /* cd = 5 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Felipe Augusto Nunes', 'felipe.nunes@email.exemplo.com',
        '$2a$10$nNFA43lCIlGG1t0KTV9PZe1YAXLhzVLUv1WW3WrfpEo3DKoVvuoqO', NULL, TRUNC(SYSDATE) - 44) /* cd = 6 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Gabriela Torres Pinto', 'gabriela.pinto@email.exemplo.com',
        '$2a$10$mNo.fE9r8XuiS2ejsOWmW.FbZMr9gxxPgFgIKlHmefoFUv4M9b68q', '(11) 98000-0007', TRUNC(SYSDATE) - 42) /* cd = 7 */;
INSERT INTO tb_cidadao (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
VALUES (sq_tb_cidadao.NEXTVAL, 'Henrique Batista Moura', 'henrique.moura@email.exemplo.com',
        '$2a$10$YruTMFyUC4wcrppJHfUXaOvVYteAvJ388grHpScPZGmC4qETpNJKG', NULL, TRUNC(SYSDATE) - 40) /* cd = 8 */;

-- tb_gestor (3) - o 1o e o gestor inicial do seed (RN17) -------------------
INSERT INTO tb_gestor (cd_gestor, nm_gestor, ds_email, ds_senha, cd_orgao, cd_gestor_cadastro, dt_cadastro)
VALUES (sq_tb_gestor.NEXTVAL, 'Marcia Oliveira Santos', 'marcia.santos@prefeitura.exemplo.gov.br',
        '$2a$10$rRbN9JXMnYIyKBtF6EOlF.SZM7Bt.5wM9IPDTMol615xbD8JvC8Ei', 1, NULL, TRUNC(SYSDATE) - 90) /* cd = 1 (RN17: sem quem cadastrou) */;
INSERT INTO tb_gestor (cd_gestor, nm_gestor, ds_email, ds_senha, cd_orgao, cd_gestor_cadastro, dt_cadastro)
VALUES (sq_tb_gestor.NEXTVAL, 'Roberto Almeida Costa', 'roberto.costa@prefeitura.exemplo.gov.br',
        '$2a$10$6OBhBp8VSAdqOxInoq9a1eo3f8j.TZHYIzupVTQXRAqpmphCH9nwu', 4, 1, TRUNC(SYSDATE) - 80) /* cd = 2 (cadastrado pelo gestor 1) */;
INSERT INTO tb_gestor (cd_gestor, nm_gestor, ds_email, ds_senha, cd_orgao, cd_gestor_cadastro, dt_cadastro)
VALUES (sq_tb_gestor.NEXTVAL, 'Juliana Pereira Dias', 'juliana.dias@prefeitura.exemplo.gov.br',
        '$2a$10$mouzTRXfqGkYCu9FxEkDtOX7wqL59mhxHPMp2W13inY6YbCkRsJFO', 3, 1, TRUNC(SYSDATE) - 75) /* cd = 3 (cadastrado pelo gestor 1) */;

-- tb_categoria (8) - tabela 6.4 (prazo em dias, gravidade 1-5, orgao) ------
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Buraco na via', 'Buraco ou afundamento no asfalto da rua.', 15, 4, 1) /* cd = 1 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Iluminação pública apagada', 'Poste apagado ou piscando na via pública.', 7, 4, 2) /* cd = 2 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Descarte irregular de lixo', 'Lixo ou entulho deixado na calçada ou em terreno.', 10, 3, 3) /* cd = 3 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Árvore com risco de queda', 'Árvore inclinada, rachada ou com galhos soltos.', 5, 5, 4) /* cd = 4 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Poda de árvore', 'Galhos encostando em fios, telhados ou cobrindo a iluminação.', 30, 2, 4) /* cd = 5 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Calçada danificada', 'Calçada quebrada, com desnível ou buraco.', 30, 3, 1) /* cd = 6 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Bueiro entupido', 'Boca de lobo ou bueiro entupido, com risco de alagamento.', 10, 4, 1) /* cd = 7 */;
INSERT INTO tb_categoria (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade, cd_orgao)
VALUES (sq_tb_categoria.NEXTVAL, 'Sinalização de trânsito danificada', 'Placa caída, semáforo ou faixa apagada.', 10, 3, 5) /* cd = 8 */;

-- tb_ocorrencia (12) - todos os status da RN04 -----------------------------
--   ABERTA: 1 a 6 | EM_ANDAMENTO: 7 e 9 | RESOLVIDA: 8, 10 e 11 | CANCELADA: 12
--   Previsao nula em 3 e 6 (RN12; Iluminacao segue a decisao D3).
--   Atrasadas de proposito (RN11): 1 (20 > 15), 3 (12 > 7) e 7 (9 > 5).
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Buraco grande no meio da faixa, carros desviando para a contramão.',
        'Rua Guaicurus, 1200 - em frente à padaria', 'ABERTA', TRUNC(SYSDATE) - 20, NULL, 18, 'S', 1, 1, 1) /* cd = 1 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Bueiro entupido com folhas, a rua alaga em qualquer chuva.',
        'Rua Clélia, 450 - esquina com a Rua Catão', 'ABERTA', TRUNC(SYSDATE) - 3, NULL, 9, 'N', 2, 7, 1) /* cd = 2 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Três postes apagados seguidos, a rua fica totalmente escura à noite.',
        'Estrada de Itapecerica, 5000 - perto do ponto de ônibus', 'ABERTA', TRUNC(SYSDATE) - 12, NULL, NULL, NULL, 3, 2, 3) /* cd = 3 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Entulho de obra descartado na calçada, bloqueando a passagem.',
        'Rua Comendador Antunes dos Santos, 300', 'ABERTA', TRUNC(SYSDATE) - 2, NULL, 11, 'S', 4, 3, 3) /* cd = 4 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Calçada com placas soltas, difícil passar com cadeira de rodas.',
        'Rua Direita, 80 - em frente à loja de tecidos', 'ABERTA', TRUNC(SYSDATE) - 8, NULL, 25, 'N', 5, 6, 5) /* cd = 5 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Galhos da árvore encostando nos fios de energia.',
        'Rua dos Pinheiros, 900', 'ABERTA', TRUNC(SYSDATE) - 1, NULL, NULL, NULL, 6, 5, 2) /* cd = 6 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Árvore inclinada sobre a rua depois da ventania, com raiz exposta.',
        'Avenida Marechal Tito, 3100 - perto da escola', 'EM_ANDAMENTO', TRUNC(SYSDATE) - 9, NULL, 6, 'S', 7, 4, 4) /* cd = 7 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Buraco na entrada da rua, já estourou o pneu de dois carros.',
        'Rua Doutor Luís da Fonseca Galvão, 150', 'RESOLVIDA', TRUNC(SYSDATE) - 40, TRUNC(SYSDATE) - 20, 14, 'N', 1, 1, 3) /* cd = 8 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Bueiro transbordando esgoto perto do terminal de ônibus.',
        'Avenida dos Metalúrgicos, 2200 - ao lado do terminal', 'EM_ANDAMENTO', TRUNC(SYSDATE) - 5, NULL, 12, 'S', 8, 7, 6) /* cd = 9 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Sacos de lixo acumulados na esquina há mais de uma semana.',
        'Rua Teodoro Sampaio, 1500 - esquina com a Rua Fradique Coutinho', 'RESOLVIDA', TRUNC(SYSDATE) - 30, TRUNC(SYSDATE) - 22, 9, 'N', 2, 3, 2) /* cd = 10 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Móveis velhos e colchão largados ao lado da praça.',
        'Praça Cornélia, 20 - lado da Rua Tito', 'RESOLVIDA', TRUNC(SYSDATE) - 25, TRUNC(SYSDATE) - 21, 10, 'N', 3, 3, 1) /* cd = 11 */;
INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura, dt_resolucao,
                           nr_prazo_previsto, fl_risco_atraso, cd_cidadao, cd_categoria, cd_bairro)
VALUES (sq_tb_ocorrencia.NEXTVAL, 'Calçada afundada em frente ao posto de saúde.',
        'Rua Barão de Alagoas, 500 - em frente à UBS', 'CANCELADA', TRUNC(SYSDATE) - 15, NULL, 28, 'N', 4, 6, 4) /* cd = 12 */;

-- tb_atualizacao (9) - so transicoes permitidas pela RN05, cada uma com gestor (RN06)
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 8, 'ABERTA', 'EM_ANDAMENTO', 'Equipe de tapa-buraco agendada.', 1, TRUNC(SYSDATE) - 35) /* cd = 1 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 8, 'EM_ANDAMENTO', 'RESOLVIDA', 'Buraco recapeado.', 1, TRUNC(SYSDATE) - 20) /* cd = 2 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 10, 'ABERTA', 'EM_ANDAMENTO', 'Coleta extra solicitada à concessionária.', 3, TRUNC(SYSDATE) - 28) /* cd = 3 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 10, 'EM_ANDAMENTO', 'RESOLVIDA', 'Lixo recolhido e local limpo.', 3, TRUNC(SYSDATE) - 22) /* cd = 4 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 11, 'ABERTA', 'EM_ANDAMENTO', 'Cata-bagulho agendado.', 3, TRUNC(SYSDATE) - 24) /* cd = 5 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 11, 'EM_ANDAMENTO', 'RESOLVIDA', 'Móveis retirados.', 3, TRUNC(SYSDATE) - 21) /* cd = 6 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 7, 'ABERTA', 'EM_ANDAMENTO', 'Vistoria feita; remoção agendada com a Defesa Civil.', 2, TRUNC(SYSDATE) - 7) /* cd = 7 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 9, 'ABERTA', 'EM_ANDAMENTO', 'Equipe de desobstrução a caminho.', 1, TRUNC(SYSDATE) - 4) /* cd = 8 */;
INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo, ds_comentario, cd_gestor, dt_atualizacao)
VALUES (sq_tb_atualizacao.NEXTVAL, 12, 'ABERTA', 'CANCELADA', 'Trecho já incluído na obra de requalificação da calçada.', 1, TRUNC(SYSDATE) - 13) /* cd = 9 */;

-- tb_apoio (6) - RN08: so em ocorrencias ABERTA/EM_ANDAMENTO, nunca na
-- propria ocorrencia, no maximo uma vez por cidadao (PK composta)
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (2, 1, TRUNC(SYSDATE) - 18) /* autor da 1 e o cidadao 1 */;
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (5, 1, TRUNC(SYSDATE) - 15);
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (6, 1, TRUNC(SYSDATE) - 10);
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (4, 3, TRUNC(SYSDATE) - 11) /* autor da 3 e o cidadao 3 */;
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (7, 3, TRUNC(SYSDATE) - 6);
INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (1, 7, TRUNC(SYSDATE) - 8) /* autor da 7 e o cidadao 7 */;

-- tb_foto (3) - PNG real de 1x1 pixel (69 bytes). RN18: tipo PNG, tamanho
-- ate 2 MB, so em ocorrencia ABERTA e no maximo 3 por ocorrencia.
INSERT INTO tb_foto (cd_foto, cd_ocorrencia, bl_imagem, ds_tipo, nr_tamanho, dt_envio)
VALUES (sq_tb_foto.NEXTVAL, 1,
        TO_BLOB(HEXTORAW('89504E470D0A1A0A0000000D4948445200000001000000010802000000907753DE0000000C4944415478DA63A8A8A8000002D40169E0B6E2570000000049454E44AE426082')),
        'image/png', 69, TRUNC(SYSDATE) - 20) /* cd = 1 */;
INSERT INTO tb_foto (cd_foto, cd_ocorrencia, bl_imagem, ds_tipo, nr_tamanho, dt_envio)
VALUES (sq_tb_foto.NEXTVAL, 1,
        TO_BLOB(HEXTORAW('89504E470D0A1A0A0000000D4948445200000001000000010802000000907753DE0000000C4944415478DA63D088D20000015800AB8C48B17E0000000049454E44AE426082')),
        'image/png', 69, TRUNC(SYSDATE) - 20) /* cd = 2 */;
INSERT INTO tb_foto (cd_foto, cd_ocorrencia, bl_imagem, ds_tipo, nr_tamanho, dt_envio)
VALUES (sq_tb_foto.NEXTVAL, 5,
        TO_BLOB(HEXTORAW('89504E470D0A1A0A0000000D4948445200000001000000010802000000907753DE0000000C4944415478DA6338B1C50600040001B95CD754B50000000049454E44AE426082')),
        'image/png', 69, TRUNC(SYSDATE) - 8) /* cd = 3 */;

COMMIT;

-- Conferencia da carga (nao faz parte das 10 consultas): linhas por tabela
SELECT 'tb_orgao' AS tabela, COUNT(*) AS linhas FROM tb_orgao
UNION ALL SELECT 'tb_bairro', COUNT(*) FROM tb_bairro
UNION ALL SELECT 'tb_cidadao', COUNT(*) FROM tb_cidadao
UNION ALL SELECT 'tb_gestor', COUNT(*) FROM tb_gestor
UNION ALL SELECT 'tb_categoria', COUNT(*) FROM tb_categoria
UNION ALL SELECT 'tb_ocorrencia', COUNT(*) FROM tb_ocorrencia
UNION ALL SELECT 'tb_atualizacao', COUNT(*) FROM tb_atualizacao
UNION ALL SELECT 'tb_apoio', COUNT(*) FROM tb_apoio
UNION ALL SELECT 'tb_foto', COUNT(*) FROM tb_foto;


/* =====================================================================
   PARTE 3 - 10 CONSULTAS (perguntas da secao 6.5 do Documento Base)
   ===================================================================== */

-- CONSULTA 01 ------------------------------------------------------------
-- Pergunta: quais bairros têm mais ocorrências em aberto (ABERTA ou
-- EM_ANDAMENTO)? Mostra só os bairros com 2 ou mais.
-- Recursos: INNER JOIN, WHERE, COUNT, GROUP BY, HAVING, ORDER BY
SELECT b.nm_bairro,
       b.nm_subprefeitura,
       COUNT(*) AS qtd_em_aberto
  FROM tb_ocorrencia o
 INNER JOIN tb_bairro b ON b.cd_bairro = o.cd_bairro
 WHERE o.st_ocorrencia IN ('ABERTA', 'EM_ANDAMENTO')
 GROUP BY b.nm_bairro, b.nm_subprefeitura
HAVING COUNT(*) >= 2
 ORDER BY qtd_em_aberto DESC, b.nm_bairro;

-- CONSULTA 02 ------------------------------------------------------------
-- Pergunta: qual o tempo médio de resolução (em dias) por categoria,
-- comparado ao prazo de referência?
-- Recursos: INNER JOIN, WHERE, cálculo de datas, COUNT, AVG, MIN, MAX,
-- GROUP BY, ORDER BY
SELECT c.nm_categoria,
       c.nr_prazo_dias                                     AS prazo_referencia,
       COUNT(*)                                            AS qtd_resolvidas,
       ROUND(AVG(o.dt_resolucao - o.dt_abertura), 1)       AS media_dias_resolucao,
       MIN(o.dt_resolucao - o.dt_abertura)                 AS menor_dias,
       MAX(o.dt_resolucao - o.dt_abertura)                 AS maior_dias
  FROM tb_ocorrencia o
 INNER JOIN tb_categoria c ON c.cd_categoria = o.cd_categoria
 WHERE o.st_ocorrencia = 'RESOLVIDA'
 GROUP BY c.nm_categoria, c.nr_prazo_dias
 ORDER BY media_dias_resolucao DESC;

-- CONSULTA 03 ------------------------------------------------------------
-- Pergunta: quais ocorrências em aberto estão atrasadas (RN11: dias em
-- aberto maior que o prazo de referência da categoria) e há quantos dias?
-- Recursos: INNER JOIN (3 tabelas), cálculo no SELECT e no WHERE, ORDER BY
SELECT o.cd_ocorrencia,
       c.nm_categoria,
       b.nm_bairro,
       o.st_ocorrencia,
       TRUNC(SYSDATE) - o.dt_abertura                      AS dias_em_aberto,
       c.nr_prazo_dias                                     AS prazo_referencia,
       (TRUNC(SYSDATE) - o.dt_abertura) - c.nr_prazo_dias  AS dias_de_atraso
  FROM tb_ocorrencia o
 INNER JOIN tb_categoria c ON c.cd_categoria = o.cd_categoria
 INNER JOIN tb_bairro b    ON b.cd_bairro    = o.cd_bairro
 WHERE o.st_ocorrencia IN ('ABERTA', 'EM_ANDAMENTO')
   AND (TRUNC(SYSDATE) - o.dt_abertura) > c.nr_prazo_dias
 ORDER BY dias_de_atraso DESC;

-- CONSULTA 04 ------------------------------------------------------------
-- Pergunta: quais ocorrências em aberto ainda não receberam nenhum apoio?
-- Recursos: LEFT JOIN, INNER JOIN, WHERE com IS NULL, ORDER BY
SELECT o.cd_ocorrencia,
       c.nm_categoria,
       o.ds_endereco,
       o.st_ocorrencia,
       o.dt_abertura
  FROM tb_ocorrencia o
 INNER JOIN tb_categoria c ON c.cd_categoria = o.cd_categoria
  LEFT JOIN tb_apoio a     ON a.cd_ocorrencia = o.cd_ocorrencia
 WHERE a.cd_ocorrencia IS NULL
   AND o.st_ocorrencia IN ('ABERTA', 'EM_ANDAMENTO')
 ORDER BY o.dt_abertura;

-- CONSULTA 05 ------------------------------------------------------------
-- Pergunta: qual a ocorrência mais apoiada pelos cidadãos?
-- Recursos: INNER JOIN, COUNT, GROUP BY, HAVING com SUBCONSULTA (MAX de COUNT)
SELECT o.cd_ocorrencia,
       c.nm_categoria,
       b.nm_bairro,
       COUNT(*) AS qtd_apoios
  FROM tb_apoio a
 INNER JOIN tb_ocorrencia o ON o.cd_ocorrencia = a.cd_ocorrencia
 INNER JOIN tb_categoria c  ON c.cd_categoria  = o.cd_categoria
 INNER JOIN tb_bairro b     ON b.cd_bairro     = o.cd_bairro
 GROUP BY o.cd_ocorrencia, c.nm_categoria, b.nm_bairro
HAVING COUNT(*) = (SELECT MAX(COUNT(*))
                     FROM tb_apoio
                    GROUP BY cd_ocorrencia);

-- CONSULTA 06 ------------------------------------------------------------
-- Pergunta: quantas ocorrências cada órgão tem sob sua responsabilidade,
-- e quantas delas ainda estão em aberto e quantas foram resolvidas?
-- Recursos: INNER JOIN em 3 tabelas, COUNT, SUM com CASE, GROUP BY, ORDER BY
SELECT org.nm_orgao,
       COUNT(o.cd_ocorrencia) AS total_ocorrencias,
       SUM(CASE WHEN o.st_ocorrencia IN ('ABERTA', 'EM_ANDAMENTO')
                THEN 1 ELSE 0 END) AS em_aberto,
       SUM(CASE WHEN o.st_ocorrencia = 'RESOLVIDA'
                THEN 1 ELSE 0 END) AS resolvidas
  FROM tb_orgao org
 INNER JOIN tb_categoria c  ON c.cd_orgao     = org.cd_orgao
 INNER JOIN tb_ocorrencia o ON o.cd_categoria = c.cd_categoria
 GROUP BY org.nm_orgao
 ORDER BY total_ocorrencias DESC, org.nm_orgao;

-- CONSULTA 07 ------------------------------------------------------------
-- Pergunta: quais categorias nunca tiveram ocorrência registrada?
-- Recursos: RIGHT JOIN, WHERE com IS NULL, ORDER BY
SELECT c.nm_categoria,
       c.nr_prazo_dias,
       c.nr_gravidade
  FROM tb_ocorrencia o
 RIGHT JOIN tb_categoria c ON c.cd_categoria = o.cd_categoria
 WHERE o.cd_ocorrencia IS NULL
 ORDER BY c.nm_categoria;

-- CONSULTA 08 ------------------------------------------------------------
-- Pergunta: qual o histórico de status da ocorrência 8, com o gestor e o
-- órgão de quem fez cada atualização (RN06)?
-- Recursos: INNER JOIN (4 tabelas), WHERE, ORDER BY
SELECT o.cd_ocorrencia,
       c.nm_categoria,
       a.dt_atualizacao,
       a.st_anterior,
       a.st_novo,
       a.ds_comentario,
       g.nm_gestor,
       org.nm_orgao AS orgao_do_gestor
  FROM tb_atualizacao a
 INNER JOIN tb_ocorrencia o ON o.cd_ocorrencia = a.cd_ocorrencia
 INNER JOIN tb_categoria c  ON c.cd_categoria  = o.cd_categoria
 INNER JOIN tb_gestor g     ON g.cd_gestor     = a.cd_gestor
 INNER JOIN tb_orgao org    ON org.cd_orgao    = g.cd_orgao
 WHERE a.cd_ocorrencia = 8
 ORDER BY a.dt_atualizacao, a.cd_atualizacao;

-- CONSULTA 09 ------------------------------------------------------------
-- Pergunta: qual o maior e o menor prazo previsto pela IA por
-- subprefeitura (desconsiderando ocorrências sem previsão, RN12)?
-- Recursos: INNER JOIN, WHERE com IS NOT NULL, COUNT, MAX, MIN, AVG,
-- GROUP BY, ORDER BY
SELECT b.nm_subprefeitura,
       COUNT(*)                              AS qtd_com_previsao,
       MAX(o.nr_prazo_previsto)              AS maior_prazo_previsto,
       MIN(o.nr_prazo_previsto)              AS menor_prazo_previsto,
       ROUND(AVG(o.nr_prazo_previsto), 1)    AS media_prazo_previsto
  FROM tb_ocorrencia o
 INNER JOIN tb_bairro b ON b.cd_bairro = o.cd_bairro
 WHERE o.nr_prazo_previsto IS NOT NULL
 GROUP BY b.nm_subprefeitura
 ORDER BY maior_prazo_previsto DESC;

-- CONSULTA 10 ------------------------------------------------------------
-- Pergunta: quais são os cidadãos mais engajados (ocorrências criadas +
-- apoios dados)? Mostra só o primeiro nome (RN13).
-- Recursos: LEFT JOIN com SUBCONSULTAS agregadas (COUNT + GROUP BY),
-- NVL, cálculo no SELECT (soma e primeiro nome), ORDER BY
SELECT SUBSTR(c.nm_cidadao, 1, INSTR(c.nm_cidadao || ' ', ' ') - 1)  AS primeiro_nome,
       NVL(cr.qtd, 0)                                                AS ocorrencias_criadas,
       NVL(ap.qtd, 0)                                                AS apoios_dados,
       NVL(cr.qtd, 0) + NVL(ap.qtd, 0)                               AS engajamento_total
  FROM tb_cidadao c
  LEFT JOIN (SELECT cd_cidadao, COUNT(*) AS qtd
               FROM tb_ocorrencia
              GROUP BY cd_cidadao) cr ON cr.cd_cidadao = c.cd_cidadao
  LEFT JOIN (SELECT cd_cidadao, COUNT(*) AS qtd
               FROM tb_apoio
              GROUP BY cd_cidadao) ap ON ap.cd_cidadao = c.cd_cidadao
 ORDER BY engajamento_total DESC, primeiro_nome;


/* =====================================================================
   PARTE 4 - UPDATE COM WHERE
   A ocorrência 9 (Bueiro entupido, EM_ANDAMENTO) foi resolvida: muda
   para RESOLVIDA e preenche a data de resolução (RN06). O WHERE também
   confere o status atual, porque só EM_ANDAMENTO -> RESOLVIDA é uma
   transição permitida (RN05).
   Observação: na aplicação, a API Java faz esta mudança junto com o
   INSERT da linha em tb_atualizacao (RN06). Aqui o UPDATE aparece
   sozinho para demonstrar o comando pedido pela disciplina.
   ===================================================================== */
UPDATE tb_ocorrencia
   SET st_ocorrencia = 'RESOLVIDA',
       dt_resolucao  = TRUNC(SYSDATE)
 WHERE cd_ocorrencia = 9
   AND st_ocorrencia = 'EM_ANDAMENTO';

COMMIT;

-- Conferencia do UPDATE (nao faz parte das 10 consultas)
SELECT cd_ocorrencia, st_ocorrencia, dt_abertura, dt_resolucao
  FROM tb_ocorrencia
 WHERE cd_ocorrencia = 9;


/* =====================================================================
   PARTE 5 - DELETE COM WHERE
   A cidadã 7 (Gabriela) retirou o apoio que tinha dado à ocorrência 3.
   Retirar apoio é permitido pela aplicação (escopo do MVP, seção 4.4).
   ===================================================================== */
DELETE FROM tb_apoio
 WHERE cd_cidadao    = 7
   AND cd_ocorrencia = 3;

COMMIT;

-- Conferencia do DELETE (nao faz parte das 10 consultas)
SELECT cd_cidadao, cd_ocorrencia, dt_apoio
  FROM tb_apoio
 WHERE cd_ocorrencia = 3;
