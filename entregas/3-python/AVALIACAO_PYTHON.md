# Avaliação do `ZelaBairro_Python.zip` (18/11/2026)

Base da avaliação:
- PDF do professor: `1TDS Fevereiro - Global Solution 2026-2.pdf`, seção *Computational Thinking Using Python*
- O que o grupo combinou: Documento Base v1.5, seção 10 e RN03–RN11, e [`PLANO_DE_DESENVOLVIMENTO.md` §2.3](../../docs/PLANO_DE_DESENVOLVIMENTO.md)
- Estilo do professor: [`05-python-professor-1tdspv.md`](../../docs/referencias/05-python-professor-1tdspv.md)

**O que foi verificado:** o zip abre sem erro. Uma varredura da árvore sintática (AST) não achou nenhuma `class`, list/set/dict comprehension, expressão geradora, `lambda` ou `global`. Os 4 casos da RN10 dão exatamente **73 / 45 / 30 / 125**. As transições da RN05 estão certas. O programa rodou de ponta a ponta com Python 3.12 e sem as bibliotecas externas, nas opções 1 a 8 e 0: o JSON salva, o `.txt` do relatório é gerado, a exportação funciona e o Oracle sem `oracledb` avisa sem quebrar. As 15 ocorrências da massa inicial estão coerentes: categorias e bairros válidos, nenhum autor apoiando a própria ocorrência, nenhum apoio repetido e `data_resolucao` só nas RESOLVIDA.

---

## 1. Nota provável pela rubrica do professor

| Item | Vale | Situação | Risco |
|---|---|---|---|
| Menus e submenus | 5 | Menu principal + submenus Consultar, Integrações e Novo status | — |
| Interação / f-strings | 4 | Entradas validadas. Algumas saídas usam concatenação em vez de f-string (ver 3.4) | baixo (~0,5) |
| Decisão (match-case + if/elif) | 6 | 3 `match` (menu, status, integrações) + `transicao_permitida`; if/elif em vários lugares | — |
| Repetição (while + for) | 6 | 9 `while`, 44 `for` | — |
| Sequências | 8 | Lista, tupla (STATUS, CATEGORIAS, BAIRROS), dicionário, set (RN08) e string | — |
| Funções | 6 | 87 funções com parâmetros, retorno e type hints, sem `global` | — |
| Persistência | 4 | JSON + TXT (+ Oracle opcional) | — |
| Usabilidade | 6 | Mensagens [OK]/[ERRO]/[AVISO], tabelas, S/N, Ctrl+C salva | — |
| Organização e comentários | 5 | 5 módulos e RN citada nos comentários. 11 funções de tela em `main.py` não têm docstring | baixo (~0,5) |
| Capa (RM + nomes) | 3,5 | OK | — |
| Sumário paginado | 3,5 | OK. Conferi as 12 páginas e todas batem | — |
| Descritivo | 10 | Objetivo, justificativa, funcionalidades, lógica, resultados esperados e guia | — |
| Formatação | 3 | Bom. Há títulos "órfãos" no fim de página (ver 3.5) | baixo (~0,5) |
| **Penalidades** | — | Nenhuma é acionada: sem class, sem comprehension, `.txt` presente e zip íntegro | — |

**Estimativa:** de 68 a 70 dos 70 pontos da entrega escrita. **O risco real está na apresentação (30 pts)**, por causa do tamanho do escopo (ver 2.1).

---

## 2. O que está diferente do que combinamos (decidir antes de enviar)

### 2.1 Escopo bem maior que o da seção 10 ⚠️ (risco para a apresentação)
O Documento Base §10 e o Plano §2.3 definem um **terminal offline** com JSON local e as opções 1–6 e 0. O plano dizia ainda para **evitar `requests` e `oracledb`**. O zip acrescenta:
- **Menu 8 – Integrações:** sincroniza com o Oracle (importar/enviar, cerca de 400 linhas em `dados.py`), ViaCEP, API de IA e exportação de JSON para o front;
- **Menu 7 – Consultar** (este é bom: é o submenu que a rubrica pede);
- consulta ao ViaCEP **dentro do Registrar** (opção 1).

Isso **não tira ponto** pela rubrica, já que Persistência aceita Oracle. Mas o item "Domínio técnico de cada integrante" vale **10 pts**, e todos precisam saber explicar `importa_do_oracle`, `envia_para_oracle`, COMMIT/ROLLBACK, `CURRVAL` e a união de sets. Se ninguém além de quem escreveu domina essa parte, o risco é real.
→ **Opções:** (a) manter e treinar o grupo nessa parte; ou (b) tirar `api_externa.py` e a parte Oracle de `dados.py`, voltando ao escopo combinado (o PDF também teria de ser ajustado).

### 2.2 Senha real do Oracle dentro do zip 🔴
O zip leva o arquivo **`.env` com `DB_USER=rm573982` e a senha verdadeira**, e o README diz *"O arquivo `.env` já traz DB_USER e DB_PASSWORD"*. Isso contraria a regra do grupo ("nunca versionar senha, `.env`", em `entregas/README.md`) e o próprio PDF, que diz que *"as credenciais ficam fora do código"*.
→ **Recomendo** tirar o `.env` do zip, deixar só o `.env.example` e ajustar a frase do README. O programa continua funcionando sem ele (testado). Se a ideia era o professor testar o Oracle, é melhor mostrar isso ao vivo na apresentação.

### 2.3 O terminal grava no Oracle **compartilhado** com a API Java e o site
"Enviar para o Oracle" faz INSERT/UPDATE nas mesmas `tb_*` que o front mostra. Dois pontos:
- **RN06** ("toda atualização guarda o gestor que a fez"): o terminal grava `tb_atualizacao` com `MIN(cd_gestor)`, ou seja, atribui a mudança a um gestor que não a fez;
- se alguém clicar em "Enviar" durante um teste ou uma demo, dados de teste entram no banco que alimenta o site.
→ Se o escopo for mantido: avisar o grupo para não usar o 8.3 no banco "de produção", ou citar essa limitação no PDF.

### 2.4 Estilo diferente do professor (Plano §2.3, "Coisas a evitar")
Nada disso tira ponto, mas é o tipo de coisa que o professor pergunta na apresentação:
- `def main()` (o professor usa o laço direto no `if __name__ == "__main__":`);
- `int | None` como type hint (`dados.py:375`), que o plano classificava como "typing avançado";
- `textwrap`, `sys.stdout.reconfigure`, `hasattr`, `isinstance`, `os.environ.setdefault`, `import` dentro de função, `try/finally`, `except Exception`, `continue`, `while True` com `return`, `", ".join(...)`, união de sets com `|`, `.get()`, `.center()/.ljust()/.rjust()`.
→ Cada integrante deve saber explicar pelo menos os que estão em `main.py`, `regras.py` e `util.py`.

### 2.5 Nome do zip fora do padrão das outras matérias
`ZelaBairro_Python.zip` não segue o padrão `ZelaBairro_BD_1TDSPV.zip` / `ZelaBairro_Java_1TDSPV.zip`. → Sugestão: `ZelaBairro_Python_1TDSPV.zip`.

---

## 3. Ajustes pequenos (opcionais)

1. **Os números da massa inicial mudam com a data.** O PDF diz que a massa *"reproduz exatamente estes valores em 17/11/2026"*, e o roteiro de demonstração (11.4) diz *"cálculo do ID 1 → 73 pontos"*. Hoje (18/11) o ID 1 já dá **74**, e em 25/11 dará **81**. Na apresentação, o professor pode estranhar. → Explicar isso na hora ou trocar a frase do PDF para "na data da captura".
2. **RN07, apoio recusado:** em `apoiar_da_sugestao`, se o apoio falhar (o e-mail é do autor ou já apoia), a função volta `None` e o registro segue criando uma ocorrência **duplicada sem perguntar** (`main.py:127-132`). → Perguntar de novo ou avisar "seguindo com nova ocorrência".
3. **Robustez do JSON:** um JSON válido mas sem alguma chave (por exemplo, editado à mão) derruba o programa com `KeyError`. Isso só seria problema se o professor editar o arquivo.
4. **f-strings:** o PDF afirma "todas as saídas com f-strings", mas há saídas montadas por concatenação: `util.caixa`, `mostra_tabela`, `mostra_campo`, `mensagem` e `main.py:256, 384, 551`. → Trocar por f-string, ou ajustar a frase do PDF.
5. **Formatação do PDF:** o título "8 Validação de Entradas" ficou sozinho no pé da página 7, e a legenda "Formato de uma ocorrência" ficou no pé da página 6, com o código na página 7. A linha do item 6 no sumário também está com o pontilhado desalinhado.
6. **Docstrings faltando em `main.py`:** `registra_ocorrencia`, `apoiar_ocorrencia`, `atualizar_status`, `fila_prioridade`, `relatorio_bairro`, `listar_atrasadas`, `menu_consultar`, `consulta_cep`, `mostra_avisos`, `menu_integracoes` e `main`.
7. **Grafia de nome:** o `.txt` do Python usa "Vitor **Gonçalves**" e o da IA usa "Vitor **Goncalves**". Vale padronizar em todos os zips.

---

## 4. O que está conforme (para não mexer)
- Menu com as opções 1–6 e 0 iguais à seção 10. STATUS e CATEGORIAS em tuplas, idênticos à tabela 6.4.
- RN03, RN04, RN05 (match-case), RN06, RN07, RN08 (set), RN10 (selection sort, como nas aulas), RN11 e RN13 implementadas e com a RN citada nos comentários.
- Dados em `data/ocorrencias.json`, carregados ao abrir e salvos ao sair (e também após cada operação).
- O contrato com a API de IA (`/prever/prazo`, `/prever/atraso`, campos `prazo_previsto_dias` e `risco_atraso`) bate com o `app.py` da IA.
- As colunas Oracle usadas (`st_ocorrencia`, `fl_risco_atraso`, `sq_tb_ocorrencia` etc.) existem no Documento Base.
- O PDF cobre tudo o que o professor pede (capa, sumário paginado, descritivo, lógica, resultados esperados e guia de execução) e ainda tem o registro de uso de IA.

---

## 5. Correções aplicadas (18/11/2026)
- **Novo pacote:** `ZelaBairro_Python_1TDSPV.zip`, sem `.env`. O zip original foi guardado em `_original/`.
- **Projeto descompactado** em `ZelaBairro_Python/`. **Gerador do PDF** em `gerar_documentacao.py` (`uv run --with reportlab python gerar_documentacao.py`); ele captura as telas rodando o programa de verdade.
- Corrigidos: 2.2, 2.3, 2.5, 3.1 a 3.6, mais o `int | None` e os `while True` do item 2.4.
- **Mantidos de propósito:** o escopo do item 2.1 (decisão do grupo) e o `main()` e os demais recursos de estilo do item 2.4 (não tiram ponto; o grupo precisa saber explicá-los). O item 3.7 é do zip da IA.
