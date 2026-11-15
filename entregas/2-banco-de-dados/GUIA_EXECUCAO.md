# Guia de execução — Banco de Dados (ZelaBairro)

Passo a passo para o grupo rodar o script no Oracle da FIAP, tirar as capturas, desenhar os três modelos e montar o .zip.
Prazo: **19/11/2026 até 23h55**, no Portal do Aluno, sem prorrogação. A meta é entregar até o meio da tarde.

## 1. Rodar o script no Oracle da FIAP (do zero)

1. Abra o **Oracle SQL Developer** e conecte na conta FIAP combinada pelo grupo. Usuário e senha do Oracle **não** vão para nenhum arquivo do repositório.
2. Abra `zelabairro.sql` (Arquivo > Abrir). Confira se a codificação está em UTF-8 (Ferramentas > Preferências > Ambiente > Codificação). Senão, os acentos dos nomes de categoria saem errados.
3. Execute com **Executar Script (F5)**, não com Ctrl+Enter, que roda só um comando.
4. No fim, a aba "Saída do Script" deve mostrar:
   - 9 `Table created` (ou "Table TB_... criado"), 8 `Sequence created` e 9 `Comment created`;
   - 60 `1 row inserted` e 1 `Commit complete`;
   - a conferência da carga: tb_orgao 5, tb_bairro 6, tb_cidadao 8, tb_gestor 3, tb_categoria 8, tb_ocorrencia 12, tb_atualizacao 9, tb_apoio 6, tb_foto 3 (total 60);
   - o resultado das 10 consultas;
   - `1 row updated` e `1 row deleted`.

### Rodar de novo (reexecutar do zero)
O bloco de DROP fica no começo do `zelabairro.sql`, comentado. Para reexecutar:
1. Selecione só as linhas entre `DROP TABLE tb_foto` e `DROP SEQUENCE sq_tb_orgao`.
2. Rode a seleção com F5. Não tire o comentário do arquivo que vai no .zip.
3. Rode o script inteiro de novo com F5.

> **Importante:** as chaves estrangeiras dos INSERTs usam os códigos 1, 2, 3…, que as sequences geram quando começam do zero. Se algum INSERT der erro no meio, **não corrija só aquela linha**: rode os DROPs e o script inteiro de novo. Senão, as sequences "pulam" um número e as FKs seguintes apontam para o registro errado.

> **Conta compartilhada com a Java:** depois de rodar, quem faz a API Java usa estas mesmas tabelas. Não rode os DROPs depois que a Java estiver gravando dados de teste sem avisar o grupo.

## 2. Senha de teste (somente ambiente de teste)

Os 8 cidadãos e os 3 gestores do seed têm o hash BCrypt (`$2a$10$…`) da mesma senha de **teste**:

| Ambiente | Senha de teste |
|---|---|
| Somente desenvolvimento/apresentação | `ZelaTeste#2026` |

Login do gestor inicial: `marcia.santos@prefeitura.exemplo.gov.br`. Essa senha só serve para testar o login da API Java contra o seed. Não use em nenhuma conta real, nem como senha do Oracle.

## 3. Capturas de tela (vão dentro do PDF)

Salve em `imagens/` **com estes nomes exatos**. O gerador do PDF encaixa cada arquivo no lugar certo e, enquanto ele não existe, mostra um quadro "inserir imagem".

| Arquivo | O que mostrar |
|---|---|
| `captura_01_create.png` | Saída do script com as tabelas, comentários e sequences criados |
| `captura_02_inserts.png` | Fim dos INSERTs + resultado da conferência (60 linhas por tabela) |
| `captura_consulta_01.png` … `captura_consulta_10.png` | Cada consulta com o comentário da pergunta visível e o resultado (uma imagem por consulta) |
| `captura_03_update.png` | O UPDATE (`1 row updated`) + a conferência mostrando a ocorrência 9 como RESOLVIDA |
| `captura_04_delete.png` | O DELETE (`1 row deleted`) + a conferência mostrando que o apoio da cidadã 7 sumiu |

Dica: para tirar a captura de uma consulta, selecione só ela e use Ctrl+Enter. O resultado aparece em grade, que fica mais legível que a saída do script.

## 4. Os três modelos no Oracle SQL Developer Data Modeler

Os modelos são **três desenhos separados**. Um não substitui o outro.

1. **Importar o modelo relacional.** Caminho mais simples, com as tabelas já criadas no Oracle: Arquivo > Importar > Dicionário de Dados > escolha a conexão FIAP > marque o seu esquema > marque as 9 tabelas `TB_*` > Concluir.
   - Alternativa: Arquivo > Importar > Arquivo DDL, com um arquivo contendo **somente a PARTE 1** do script. O importador de DDL não lida bem com INSERTs e SELECTs.
2. **Modelo relacional:** é o diagrama que a importação cria. Confira as 9 tabelas, as PKs, as FKs e as 10 linhas de relacionamento (incluindo o autorrelacionamento de `tb_gestor`). Organize: botão direito no fundo > Layout automático. Depois arraste para ficar legível.
3. **Modelo lógico:** com o relacional aberto, use Design > Engenharia para Modelo Lógico (botão `<<`) > Engenharia. Na aba Lógico, confira as entidades, os atributos e as cardinalidades (1:N e o N:N por `tb_apoio`). Notação recomendada: Barker ou Bachman (botão direito no fundo > Notação).
4. **Modelo conceitual:** use uma cópia do diagrama lógico com só entidades e relacionamentos. Botão direito no fundo > Exibir Detalhes > **Somente Nomes**. Mostre entidades, relacionamentos e cardinalidades, sem tipos de dado nem chaves. Se o professor preferir outra ferramenta para o conceitual (ex.: brModelo), use-a, mas mantenha os mesmos nomes.
5. **Exportar cada desenho:** Arquivo > Data Modeler > Imprimir Diagrama > Para Arquivo de Imagem > PNG. Salve como:
   - `imagens/modelo_conceitual.png`
   - `imagens/modelo_logico.png`
   - `imagens/modelo_relacional.png`
6. Salve também o projeto do Data Modeler (`.dmd`) na pasta `modelos/`, para poder reabrir. Ele **não** vai no .zip.

## 5. Gerar o PDF

Na pasta `entregas/2-banco-de-dados/`:

```bash
uv run --with reportlab python gerar_documentacao.py
```

Sai `documentacao.pdf` com a capa (nomes, RM e turma), o levantamento, os três modelos, o dicionário de dados, o enunciado das 10 consultas e as capturas. Rode de novo sempre que trocar uma imagem. Antes de entregar, abra o PDF e confira se **nenhum** quadro "inserir imagem" sobrou.

## 6. Montar o .zip final

O PDF pede "somente o PDF e o .sql". As capturas vão **dentro do PDF**, e o `.txt` de identificação entra por causa da regra geral da GS.

```bash
zip ZelaBairro-BD-1TDSPV.zip documentacao.pdf zelabairro.sql identificacao.txt
```

Confira antes de enviar:

```bash
unzip -l ZelaBairro-BD-1TDSPV.zip
```

O resultado deve listar exatamente 3 arquivos. Envie no Portal do Aluno, na entrega de Building Relational Database.

## 7. O que só o grupo consegue verificar

- O script rodar sem erro **na conta Oracle da FIAP**. Foi testado do zero numa instância local do Oracle Database Free, mas a conta da FIAP pode ter tabelas antigas com o mesmo nome ou cota de espaço diferente.
- Os acentos aparecerem certos no SQL Developer de cada um (codificação UTF-8).
- Os três desenhos no Data Modeler e as capturas de tela.
- A Java conectar nas tabelas com as credenciais combinadas (teste de pronto do plano, seção 2.2).
