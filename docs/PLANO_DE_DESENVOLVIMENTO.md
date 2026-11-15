# Plano de desenvolvimento — ZelaBairro (GS 2026/2)

> Versão de 15/11/2026 (atualizada para o Documento Base **v1.4**: login por e-mail e senha com `tb_gestor` (RN15–RN17), fotos com `tb_foto` (RN18) e o fluxo da previsão da IA explicado na seção 7.4). Entrega: **19/11/2026 até 23h55, sem prorrogação.**
> Este plano não cria regra nova: as regras e os nomes vêm do **Documento Base v1.4** (`docs/ZelaBairro-Documento-Base.pdf`), os critérios de nota vêm de [`CRITERIOS_DE_ACEITE.md`](CRITERIOS_DE_ACEITE.md) e o "jeito de fazer" vem dos nossos projetos anteriores, resumidos em [`referencias/`](referencias/).
> Se este plano e o Documento Base discordarem, vale o Documento Base.

## 0. Como usar este plano

> **Onde fica cada entrega:** pasta [`entregas/`](../entregas/), uma subpasta por matéria na ordem de dependência, cada uma com um README de checklist.

> **Antes de tudo, leia [COMO_O_ZELABAIRRO_FUNCIONA.md](COMO_O_ZELABAIRRO_FUNCIONA.md):** explica em linguagem simples o sistema inteiro (jornadas, IA, login, fotos, tabelas) e traz as perguntas prováveis dos professores.

1. **A ordem é a da seção 12.1 do Documento Base.** Uma matéria só é dada como pronta quando passa no teste de "pronto" do seu nível. Esse teste é o que libera a próxima.
2. **Cada matéria segue um projeto que já fizemos.** Na apresentação, a frase-chave é *"fizemos do mesmo jeito que no projeto X, com estas mudanças exigidas pela GS"*. Cada seção abaixo diz qual é a referência e o que muda.
3. **Cada tarefa aponta para os pontos que ela vale.** Se faltar tempo, cortem primeiro o que vale menos (as tabelas de pontos estão em `CRITERIOS_DE_ACEITE.md`).
4. **Registro de uso de IA começa hoje.** Ele vale 10 pontos em Eng. Software e precisa de evidências (prompts, o que foi aceito/corrigido/descartado). Esta sessão com o Claude, a correção do projeto de IA e este plano entram no registro.

### Referências técnicas (o que aprendemos)

| Resumo | Projeto original | Serve de base para |
|---|---|---|
| [01-EcoScoreEngine](referencias/01-EcoScoreEngine.md) | Front do Challenge (React + Vite + TS + Tailwind, Vercel) | Front-end: `api.ts` único, hooks, 4 estados de tela, React Hook Form |
| [02-EcoScoreEngine-API](referencias/02-EcoScoreEngine-API.md) | API Java do Challenge (Spring Boot, JDBC puro, Docker, Render) | API Java inteira |
| [03-receitario-cp5](referencias/03-receitario-cp5.md) | CP5 de Front-end | Front-end: rota com parâmetro, skeleton, `vercel.json` |
| [04-OrbitalMed](referencias/04-OrbitalMed.md) | 1ª GS (site HTML/CSS/JS) | Páginas institucionais, formulário de contato, README da entrega |
| [05-python-professor-1tdspv](referencias/05-python-professor-1tdspv.md) | Repositório do professor de Python | Estilo exato do app Python |
| [06-ia-aulas-prof-alfonso](referencias/06-ia-aulas-prof-alfonso.md) | Aulas e checkpoint de AI & Chatbot | Algoritmos, métricas, Dataviz e estilo dos notebooks de IA |

Nenhum projeto anterior tem **Banco de Dados** nem **IA**. Para IA, a referência são as aulas do professor (resumo 06); para Banco, o conteúdo da disciplina e o Documento Base.

---

## 1. Decisões que o grupo precisa tomar hoje (15/11)

| # | Decisão | Recomendação | Por quê |
|---|---|---|---|
| G1 | Preencher os **responsáveis** da tabela 13.1 do Documento Base | Uma pessoa dona de cada frente, e todos commitando no front | Sem dono, a tarefa não anda; o front exige 5 commits **de cada** integrante |
| G2 | **Onde fica o código de cada matéria** | ✅ **Decidido em 15/11:** este repositório (`citizentech-gs-workspace`) é só para **desenvolver e organizar** (pasta `entregas/`). Matérias que exigem repositório ganham um **repositório próprio** para a versão entregue: **Front-end** (público, obrigatório) e **Java** (exigido na prática pelo deploy no Render; pode ser privado); a IA só se publicarem a Flask no Render. Banco, Python e Eng. Software são entregues como `.zip`/PDF direto no Portal | O front precisa ser público; o Render publica a partir de um repositório GitHub |
| G3 | Confirmar as decisões D1–D5 da seção 14.1 do Documento Base | Aceitar como estão | Já estão implementadas no projeto de IA |
| G4 | **Conta Oracle** que hospeda o banco (pendência da seção 14) | A de quem faz o Banco | A Java precisa das credenciais (só em variáveis de ambiente) |
| G5 | Nome da empresa (capa de Eng. Software) | Definir hoje | Exigido na capa (−1 pt se faltar) |

---

## 2. Nível 1 — matérias independentes (começam já, em paralelo)

### 2.1 IA & Chatbot — **praticamente pronta**

**Referência:** o próprio projeto `zelabairro-ia` (versão corrigida "GS IA - Zelabairro.zip"). A análise de 15/11 confirmou os 99 testes passando, a API respondendo e o contrato da seção 7.3 respeitado.

**Alinhamento às aulas: FEITO em 15/11** (pasta `entregas/1-ia-chatbot/zelabairro-ia/`; notebooks reexecutados, 99 testes passando, API com as mesmas respostas). Quase tudo o que o projeto usa foi visto em aula (Random Forest, GridSearchCV, validação cruzada, matriz de confusão, recall, F1, ROC AUC). Os ajustes recomendados estão na seção 3 de [06-ia-aulas-prof-alfonso](referencias/06-ia-aulas-prof-alfonso.md): comparar antes com Árvore de Decisão e Regressão Linear/Logística, trocar Ridge por LinearRegression, plotar a curva ROC, tirar a curva de calibração, reforçar a estatística do EDA e revisar os gráficos pelo framework de Dataviz.

**Falta (em ordem de impacto na nota):**

| # | Tarefa | Vale | Pronto quando |
|---|---|---|---|
| 1 | Preencher `DATA_DOWNLOAD` na 1ª célula do notebook 01 e apagar o aviso "Preencha antes de entregar" | Notebooks (60) | Não sobra nenhum "PREENCHER" nos notebooks |
| 2 | ~~Reexecutar os 3 notebooks~~ (feito em 15/11; reexecutar de novo só se mudarem dados) — opcional rodar na máquina do grupo (01 e 03: minutos; 02: até ~3 h), o que tira o caminho `/home/claude/...` das saídas | Notebooks (60) + regra de IA | Saídas com o caminho de quem rodou; métricas iguais às do README |
| 3 | Reescrever as conclusões dos notebooks **com as palavras do grupo** (os números estão certos) | Notebooks (60) + arguição | Cada integrante consegue explicar as conclusões |
| 4 | Gerar o `.zip` com `python scripts/empacotar.py`, incluindo `.idea` na lista de pastas ignoradas | Item zerado se faltar arquivo | O zip abre, tem `identificacao.txt` na raiz e não tem `__pycache__`, `.venv` nem `.idea` |
| 5 | ~~Chatbot: falar "risco alto/baixo" em vez de "68% de chance" (D4)~~ feito em 15/11 | Apresentação: métricas (20) | Chat sem porcentagem |
| 6 | (Opcional, nível 2) Publicar a Flask no Render para a Java chamá-la (seção 7.4 do Documento Base) | — (desejável) | `/health` público respondendo |

**Como a IA entra no sistema (seção 7.4 do Documento Base):** a IA é um serviço à parte. Ela não acessa o banco nem a Java, e o front não a chama. Quem chama é a **Java**, uma vez, ao criar a ocorrência; a Java grava o prazo e o risco no Oracle, e o site mostra a previsão na confirmação, no detalhe e (via prioridade) no painel. Sem a integração, a ocorrência nasce sem previsão (RN12) e a nota de IA não muda: a demo de IA é chamar a Flask direto.

**Teste de pronto:** `python -m pytest tests -q` com 99 testes passando; `/health`, `/prever/prazo` e `/prever/atraso` respondendo; zip conferido.

**Apresentação (100 pts):** problema e papel da IA (15) → dados e EDA, com origem SP156, janela 2020–2023 e o motivo (15) → escolha dos modelos, com regressão para prazo, classificação para atraso e comparação com o baseline (20) → métricas (MAE 23,3 × 24,5 do baseline; AUC 0,754; recall 0,834) (20) → demo ao vivo seguindo o roteiro da seção 7 do README (20) → todos respondem (10).

---

### 2.2 Banco de Dados — **primeiro do caminho crítico**

**Referência:** não temos projeto anterior de banco. Base: seção 6 do Documento Base (**9 tabelas** desde a v1.3, dicionário e seed), conteúdo da disciplina (Oracle SQL Developer + Data Modeler).
Da API Java antiga ([02](referencias/02-EcoScoreEngine-API.md)) aprendemos o que **não** repetir: lá as colunas eram `ID_`/`DS_` e o id vinha de IDENTITY. Aqui é `cd_`/`st_` e **sequences `sq_tb_*`**, porque a Java exige.

| # | Tarefa | Vale (entrega 100) |
|---|---|---|
| 1 | Levantamento: problema, público, objetivo, atores, dados, perguntas e ODS, **escrito sobre o ZelaBairro** (seções 3, 5.1 e 6.5 do Documento Base) | 10 |
| 2 | Data Modeler: modelos **conceitual, lógico e relacional** (três desenhos separados) | 10 + 15 |
| 3 | Dicionário de dados: tabela, coluna, tipo, tamanho, nulo, chave, restrição e significado (seção 6.3) | 15 |
| 4 | Script: CREATE TABLE na ordem das FKs (`tb_orgao`, `tb_bairro`, `tb_cidadao`, `tb_gestor`, `tb_categoria`, `tb_ocorrencia`, `tb_atualizacao`, `tb_apoio`, `tb_foto`), incluindo `tb_foto` com BLOB e os CHECKs de tipo e tamanho (RN18), `ds_senha` em `tb_cidadao`/`tb_gestor`, o autorrelacionamento `tb_gestor.cd_gestor_cadastro` e `tb_atualizacao.cd_gestor`, `COMMENT ON TABLE` em todas, PK/FK/NOT NULL/UNIQUE/CHECK, sequences `sq_tb_*` (menos `tb_apoio`) | 15 |
| 5 | **60 registros** (o PDF diz 50 e 60, então 60 atende os dois) espalhados por todas as tabelas. Seed: 5 órgãos, 8 categorias da tabela 6.4, bairros reais com a subprefeitura **igual ao `depara_distrito_subprefeitura.csv`**, cidadãos, **pelo menos um gestor inicial** (com `cd_gestor_cadastro` nulo e senha como hash BCrypt, nunca em texto), ocorrências em todos os status, atualizações (cada uma com o gestor), apoios e **algumas fotos** (PNG minúsculo via `HEXTORAW`, para a tabela ter registros) | 15 |
| 6 | UPDATE e DELETE **com WHERE** (sugestão do Documento Base: mudar status para RESOLVIDA; retirar um apoio) | dentro do 15 |
| 7 | 10 consultas numeradas a partir da seção 6.5, cobrindo WHERE, ORDER BY, cálculo no SELECT, COUNT/SUM/AVG/MAX/MIN com GROUP BY, HAVING, subconsulta, INNER, LEFT e RIGHT JOIN | 15 + 15 |
| 8 | Capturas da execução (tabelas, inserts, consultas, update e delete) **dentro do PDF** | 5 |
| 9 | Ordem do `.sql`: tabelas → inserts → 10 consultas → UPDATE → DELETE. Capa com nomes, RM e turma; `.txt` no zip | 5 |

**Teste de pronto (libera a Java):** script (9 tabelas) roda do zero no Oracle da FIAP sem erro; as 10 consultas retornam linhas; quem faz a Java consegue conectar com as credenciais combinadas.

**Apresentação (100):** problema e papel do banco (15) → os 3 modelos e o dicionário (15) → CREATE ao vivo (15) → CRUD ao vivo (15) → filtro, agregação e subconsulta (20) → os 3 JOINs, com qualquer integrante respondendo (20).

---

### 2.3 Python — independente (JSON local, sem rede)

**Referência:** [05-python-professor-1tdspv](referencias/05-python-professor-1tdspv.md). Copiar **o estilo do professor**, que é o que ele vai reconhecer:
- funções em snake_case e em português, com verbo (`cadastra_ocorrencia`, `recupera_ocorrencias`), type hints e f-strings;
- `menu() -> int` + `while opcao != 0` dentro de `if __name__ == "__main__":`; dados passados por parâmetro, sem `global`;
- `match-case` com `case _` (usar na RN05, transição de status);
- arquivos com `with open(...)` + `json.load` / `json.dump(indent=4)`, com mensagem de confirmação;
- validação de entrada com `while` + `try/except`;
- organização em módulos como no exemplo `locadora/` do professor (app / service / util);
- ordenação **manual** (selection sort, como nas aulas) para a fila da RN10;
- sets: o professor não usou, mas a rubrica exige. Usar só o básico (`set()`, `.add()`, `in`, `len()`) e converter para lista antes de salvar no JSON.

| # | Tarefa | Vale (código 50) |
|---|---|---|
| 1 | Menu principal **com submenus** (a rubrica pede "menus e submenus"; o Documento Base só lista o menu principal da seção 10, então o submenu entra em "Relatórios", com fila, por bairro e atrasadas) | Menus 5 |
| 2 | Opções da seção 10: registrar (RN03 + RN07), apoiar (set, RN08), atualizar status (match-case, RN05), fila (RN10), relatório por bairro (salva `.txt`), atrasadas (RN11), sair salvando JSON | Decisão 6, repetição 6, sequências 8, funções 6 |
| 3 | Constantes em tuplas: STATUS e as 8 categorias com prazo e gravidade da tabela 6.4 | Sequências |
| 4 | Persistência em `data/ocorrencias.json` | Persistência 4 |
| 5 | Mensagens claras em todo erro de entrada | Usabilidade 6 |
| 6 | Comentários citando a RN de cada regra | Organização 5 |
| 7 | **Checagem antes de entregar:** busca por `class ` e por `[` seguido de `for` na mesma linha, sem nenhum resultado | Evita nota zero e −15 por ocorrência |
| 8 | PDF: capa com RM e nomes, sumário paginado, descritivo (objetivo, justificativa, funcionalidades) e guia de execução | Documentação 20 |
| 9 | Zip: `.py` + PDF + `.txt` de identificação (sem o `.txt`: −25) | — |

**Teste de pronto:** os 4 exemplos da RN10 (seção 5.3) dão exatamente 73/45/30/125; transições proibidas da RN05 recusadas; JSON salvo e recarregado.

**Apresentação (30):** papel do app no projeto (offline, triagem do gestor) (5) → módulos (5) → funções, parâmetros e retornos (5) → por que set, tupla e dicionário (5) → todos respondem (10).

---

## 3. Nível 2 — API Java (depende do Banco)

**Referência:** [02-EcoScoreEngine-API](referencias/02-EcoScoreEngine-API.md). Repetimos a stack que já usamos: Java 21, Spring Boot 4.1.x, `spring-boot-starter-jdbc` (só para o DataSource/Hikari), ojdbc17, ModelMapper 3.2.0, Bean Validation, Dockerfile multi-stage (temurin 21 jdk → jre) e Render, com CORS lendo `CORS_ORIGINS` e banco por `DB_URL`/`DB_USER`/`DB_PASSWORD`.

**O que muda em relação ao projeto antigo (exigências da GS e do Documento Base):**

| No EcoScoreEngine-API | No ZelaBairro | Motivo |
|---|---|---|
| Pacote `resource` | `controller` | Pacotes exigidos pelo PDF |
| `@RestControllerAdvice` dentro de `exception` | Pacote `handler` separado | Idem |
| DAO recebe `ConnectionFactory` | DAO recebe **`DataSource` pelo construtor** | Requisito 03 da Java |
| Colunas `ID_`/`DS_`, id por IDENTITY | `cd_`/`nm_`/`ds_`/`dt_`/`st_`/`fl_` e `sq_tb_*.NEXTVAL` | Requisito 02 e seção 6 |
| Regra de negócio → 422 | **409** | Requisito 09 e seção 8.2 |
| Erro `{erro, detalhe}` | `{status, erro, mensagem, caminho, timestamp, campos}` | Seção 8.3 |
| Sem testes e sem Swagger | Testar pelo Insomnia/Postman (é o que a apresentação pede) | Apresentação, item 01 |

Login (v1.2): **igual ao EcoScoreEngine-API**, que já usava BCrypt (`spring-security-crypto`) e um id no cabeçalho. Aqui o cabeçalho é `X-Gestor-Id`, conferido no banco nas rotas de gestor (RN16), e o login devolve `{id, nome, perfil}` (seção 8.5 do Documento Base).

Podemos manter a camada `bo` (regras e transação manual com commit/rollback) que o grupo já conhece, documentando-a no PDF como responsável pelas regras RN05, RN08, RN09 e RN10.

| # | Tarefa | Vale (entrega 70) |
|---|---|---|
| 1 | Projeto + `model` das entidades Cidadao, **Gestor**, Bairro, Categoria, Ocorrencia, Atualizacao e Apoio (**pode começar antes do banco ficar pronto**, porque os nomes já estão na seção 6) | 5 |
| 2 | `dao` com JDBC: um DAO por entidade, PreparedStatement, try-with-resources, sequences | 15 |
| 3 | `dto` de entrada e saída + ModelMapper; JSON em camelCase como na seção 8.3; RN13 (só primeiro nome, sem e-mail) | 10 |
| 4 | `controller` com as rotas da seção 8.2: 201 + Location, 200, 204, 400, 404, 405 e 409 | 10 |
| 5 | Regras com exceção própria: RN05 (transição), RN08 (apoio), RN09 (edição/exclusão), RN14, RN15 (401), RN16 (403) e RN17; `handler` com o JSON padrão, sem stack trace nem SQL | 10 |
| 5b | **Login e gestores (v1.2):** `AuthController` (`POST /auth/login`), CRUD de `/gestores` só para gestor, hash BCrypt no cadastro, senha nunca devolvida | dentro do 10 + 15 |
| 6 | Prioridade RN10 e "atrasada" RN11 calculadas na saída; lista ordenada por prioridade | dentro do 10 |
| 7 | `config` com CORS liberado para a URL da Vercel | 5 |
| 8 | Dockerfile multi-stage + deploy no Render, com variáveis de ambiente e **nenhuma senha no código** (−10) | 5 |
| 5c | **Fotos (v1.3):** `FotoDAO` (`setBytes`/`getBytes`), `POST /ocorrencias/{id}/fotos` com `MultipartFile`, `GET /ocorrencias/{id}/fotos`, `GET /fotos/{id}` devolvendo a imagem, `DELETE`; RN18 com `X-Cidadao-Id`; limites de upload no `application.properties`; CORS liberando `X-Cidadao-Id`. **Última funcionalidade a entrar** se o tempo apertar | dentro do 15 + 10 |
| 9 | (Desejável) Chamar a Flask ao criar ocorrência (`IA_API_URL`), gravar `nr_prazo_previsto` e `fl_risco_atraso` e devolver no JSON; fallback RN12 e D3 (Iluminação → nulo) | — |
| 10 | PDF técnico: capa e links, solução, diagrama de classes, DER, endpoints com JSON, pacotes, regras e validações, deploy com os nomes das variáveis | 10 |
| 11 | README na raiz: integrantes e RM, como rodar, URL do Render e link do vídeo; zip **sem `target/`** | — |

**Teste de pronto (libera o Front):** coleção do Insomnia/Postman passando nos endpoints da 8.2 contra a URL do Render; 400 com `campos` e 404 retornando o JSON padrão; RN12 testada com a Flask desligada.

**Atenção:** o **vídeo da Java** (até 5 min) precisa mostrar o **front integrado**, então ele só pode ser gravado no nível 3. Sugestão: um vídeo único de até 3 minutos serve para a Java e para o Front.

**Apresentação (30):** CRUD pelo Insomnia/Postman (8) → 400 e 404 ao vivo (4) → caminho controller → DTO → BO → DAO → Oracle (6) → entidades, 1:N e regra (4) → todos respondem (8).

---

## 4. Nível 3 — Front-end (depende da Java publicada)

**Referência:** [01-EcoScoreEngine](referencias/01-EcoScoreEngine.md) + [03-receitario-cp5](referencias/03-receitario-cp5.md) para a stack e o código; [04-OrbitalMed](referencias/04-OrbitalMed.md) para páginas institucionais, formulário de contato e README. Stack que já usamos: React 19, Vite 8, TypeScript 6, Tailwind 4 (tema em `@theme`), react-router-dom 7, React Hook Form, `vercel.json` com rewrite da SPA.

**Reaproveitar:**
- `src/services/api.ts` com um único `request<T>()` usando fetch, do EcoScoreEngine. Adaptar a leitura de erro ao formato 8.3 e levar o `campos[]` para o `setError` do React Hook Form;
- hook por recurso (lista, loading, erro, recarregar);
- os 4 estados de tela (skeleton, `MensagemErro` com "Tentar novamente", `EstadoVazio`, lista);
- `lazy` + `Suspense` + `ErrorBoundary` + rota 404;
- `useParams` em `/ocorrencias/:id`;
- **login (v1.2):** `LoginPage`, `AuthContext` com a sessão no `localStorage` (com try/catch) e `RotaProtegida` do EcoScoreEngine. Aqui a sessão guarda `{id, nome, perfil}`, o menu Painel só aparece para GESTOR e as rotas de gestor enviam `X-Gestor-Id`.

**Não repetir:**
- URL fixa no código: usar `VITE_API_URL`;
- fetch fora do `api.ts`;
- rota com parâmetro lendo dados estáticos (mocks não são aceitos);
- campos sem `<label>`;
- `tsconfig` sem `strict`;
- nomes misturando inglês e português (usar os componentes da seção 9.2).

| # | Tarefa | Vale (entrega 70) |
|---|---|---|
| 1 | **Hoje:** criar o repositório **público**, com estrutura `components`/`pages`/`services`/`types` e Tailwind; **cada integrante faz commits desde já** (mínimo 5 por pessoa e 15 no total) | 10 + 2 |
| 2 | **Hoje (não depende da API):** Home, Sobre, Integrantes, FAQ e Contato (com validação), menu e menu mobile | 10 + 7 |
| 3 | Tipos em `src/types`, copiando a seção 8.3 | 3 |
| 3b | `/login` e `/cadastro` (POST com validação: e-mail, senha com mínimo de 6) + `AuthContext` + `RotaProtegida` em `/painel` e `/ocorrencias/nova` | 4 + 7 |
| 4 | `/ocorrencias`: GET com filtros e badges de prioridade, com os 4 estados | 3 + 3 |
| 5 | `/ocorrencias/nova`: POST, RN07 (sugerir apoio), validação RN03, mensagens de sucesso e erro da API; confirmação mostrando a previsão ("cerca de 16 dias · risco alto" ou "previsão indisponível") | 4 + 7 |
| 5b | **Fotos (v1.3):** campo de arquivo com pré-visualização, validação (JPG/PNG, 2 MB, até 3) e envio com `fetch` + `FormData` depois do POST da ocorrência; enviar `X-Cidadao-Id` | 4 + 7 |
| 6 | `/ocorrencias/:id`: detalhe, **previsão da IA**, histórico, **galeria de fotos**, botão Apoiar (POST de apoio) | 2 |
| 7 | `/painel` (só gestor): fila por prioridade, mudança de status (POST de atualização com `X-Gestor-Id`) e formulário "cadastrar gestor" | — |
| 8 | Testar em 390×844, 768×1024 e 1440×900, sem rolagem horizontal | 8 |
| 9 | Deploy na Vercel e conferir rotas e API na versão publicada | 7 |
| 10 | README completo (título, objetivo, tecnologias, pastas, integrantes, execução, links do GitHub, Vercel, API e YouTube, contato) + vídeo de até 3 min | 10 |
| 11 | Zip **sem `node_modules`**, até 50 MB, com `.txt` | evita −3 e −2 |

**Teste de pronto:** na URL da Vercel, cadastrar, fazer login, listar, criar, apoiar e (como gestor) mudar status funcionando contra a API do Render, nas 3 resoluções.

**Apresentação (30):** problema (3) → solução (3) → páginas e navegação (3) → responsividade (3) → formulário e menu mobile ao vivo (3) → domínio técnico (4 + 4) → **todos falam** (4) → perguntas (3).

---

## 5. Nível 4 — Engenharia de Software & Modelo de Negócio (consolida tudo)

**Referência:** seções 3, 4, 5, 9 e 11 do Documento Base, que já trazem problema, atores, RN01–RN18, telas, BMC inicial e SLA de partida. Nenhum projeto anterior teve essa matéria documentada.

**Pode começar hoje (sai do Documento Base):**

| # | Bloco | Vale |
|---|---|---|
| 1 | Capa (nome da empresa e da solução, turma, nomes e RMs), sumário, sumário executivo | 5 |
| 2 | Problema com evidência (SP156: cerca de 157 mil solicitações/mês; atraso por categoria, dado do projeto de IA), solução, modelo de negócio, BMC com 9 blocos | 10 |
| 3 | Mercado e benchmark com fonte e data (Colab, SP156, 1746, Fala.BR) | 10 |
| 4 | Backlog no **Jira ou Trello**: uma HU por card (Eu, como…, quero…, para…), RF, RNF com meta verificável e as RN01–RN18 do Documento Base (inclui HUs de login, cadastro de gestor e envio de fotos) | 10 |
| 5 | Diagrama de casos de uso + 3 casos detalhados (sugestão: Registrar ocorrência, **Fazer login** (fluxos alternativos claros: senha errada → 401, cidadão no painel → 403) e Atualizar status) com alternativas e exceções | 10 |
| 6 | 3 diagramas de atividades com raias, um por caso detalhado | 5 |
| 7 | Precificação (custos, hora técnica, horas/homem, preço), ROI e SLA (seção 11 do Documento Base como ponto de partida) | 10 + 5 + 5 |

**Depende do produto pronto (nível 3):**

| # | Bloco | Vale |
|---|---|---|
| 8 | UX: prints das telas reais com jornada, estados de erro e vazio, Nielsen por tela e UX writing | 10 |
| 9 | Pitch de até 5 min com a voz do grupo, seguindo o roteiro do PDF; link testado em aba anônima | 10 |
| 10 | **Registro do uso de IA** (ferramentas, prompts, evidências, o que foi aceito/corrigido/descartado, aprendizado) | 10 |

Entrega: **um único PDF**, com os links do backlog e do pitch.

**Apresentação (100):** backlog e evolução (15) → negócio e mercado (15) → preço, ROI e SLA (20) → um caso de uso + diagrama de atividades (20) → jornada no protótipo (15) → todos falam (15).

---

## 6. Cronograma de 15 a 19/11 (seguindo a ordem)

| Dia | Nível 1 (IA, BD, Python) | Nível 2 (Java) | Nível 3 (Front) | Nível 4 (Eng. Software) |
|---|---|---|---|---|
| **Dom 15/11** | BD: script e seed rodando no Oracle. Python: menu e regras. IA: itens 1 e 3 (o 2 já foi feito) | Projeto criado, `model` e `dto` (sem banco ainda) | Repo público, páginas institucionais, **commits de todos** | Capa, BMC, benchmark, backlog no Jira/Trello |
| **Seg 16/11** | BD: modelos no Data Modeler e dicionário. Python: persistência e PDF. IA: zip de teste | DAOs + CRUD no Oracle; **1ª versão no Render à noite** | Tipos, `api.ts`, `/ocorrencias` contra a API | Casos de uso, diagramas de atividades, precificação |
| **Ter 17/11** | BD: capturas e PDF. Python: **pronto** | Regras, handler, CORS; (opcional) Java ↔ Flask | Nova ocorrência, detalhe, painel; responsividade | ROI e SLA |
| **Qua 18/11** | Zips finais de IA, BD e Python | PDF técnico | Vercel, README, **vídeo único** | Prints e Nielsen, pitch, registro de IA |
| **Qui 19/11** | — | Zip sem `target/` | Zip sem `node_modules` | PDF final | 
| | **Entregar tudo até o meio da tarde** (o Documento Base pede folga). Conferir o `.txt` em cada zip e os links em aba anônima. | | | |

**Caminho crítico:** Banco (15/11) → Java no Render (16/11) → Front integrado (17/11) → vídeo e prints (18/11). Qualquer atraso no banco empurra tudo.

---

## 7. Checklist final de entrega (19/11)

| Matéria | Arquivo | Conferir |
|---|---|---|
| IA | `.zip` | `data/*.csv`, 3 notebooks executados, 2 `.joblib`, `app.py`, `identificacao.txt` |
| Banco | `.zip` | PDF (capa, levantamento, 3 modelos, dicionário, consultas, capturas) + `.sql` na ordem pedida + `.txt` |
| Python | `.zip` | `.py` + PDF + `.txt`; nenhuma `class` nem list comprehension |
| Java | `.zip` | Projeto sem `target/`, Dockerfile, `.sql`, PDF técnico, README com URL do Render e do vídeo |
| Front | `.zip` (até 50 MB) | Sem `node_modules`; README com GitHub, Vercel, API e YouTube; `.txt` |
| Eng. Software | PDF único | Links do backlog e do pitch abrindo em aba anônima; registro de IA |

Dica comum a todas: a API no Render "dorme" no plano gratuito. Abram `/health` (Flask) e a API Java alguns minutos antes de qualquer demo e da correção.
