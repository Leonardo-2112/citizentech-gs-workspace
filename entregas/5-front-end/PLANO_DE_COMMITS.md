# Plano de commits · Front-end do ZelaBairro

Roteiro para os 5 integrantes publicarem o front no repositório **https://github.com/Leonardo-2112/zelabairro-frontend**, um commit de cada vez, cada um com a própria conta do GitHub, seguindo **Git Flow** (`main` → `develop` → `feature/*`) e **Conventional Commits**.

O código já está pronto e testado em `entregas/5-front-end/zelabairro-front/`. **Ninguém digita código:** cada passo é **um bloco para copiar e colar no terminal**. O bloco cria a branch, copia os arquivos daquele passo (`aplicar-passo.mjs`), instala as dependências quando precisa, compila, faz o commit, envia a branch, **abre o Pull Request para `develop` e faz o merge com merge commit** (`gh pr merge --merge`). Se qualquer comando falhar, o bloco para ali (por causa do `&&`) e nada errado é enviado.

> **Como o grupo está fazendo:** todos no notebook do Leonardo, no mesmo clone (`~/zelabairro-frontend`). Antes dos passos de cada pessoa, cola-se o bloco **"Trocar para o usuário de…"**: o commit sai com o nome e o e-mail da conta de quem está fazendo, e é isso que faz o commit contar no perfil dela. Os Pull Requests são abertos e mesclados pelo `gh` logado na conta do Leonardo.
>
> **Já feito em 18/11:** passos 0 e 01 a 12 (01 a 09 com merge pelo terminal; 10 a 12 com os PRs #1 a #3).

## Antes de tudo (leia uma vez)

- **Terminal:** no Windows use o **Git Bash** (vem com o Git; clique com o botão direito na pasta → *Open Git Bash here*). No macOS e no Linux, o terminal normal. Não use o PowerShell nem o cmd: os blocos usam `&& \` para quebrar linha.
- **Node.js 20.19+ ou 22.12+** (`node -v`), Git e o **GitHub CLI** (`gh`, logado; confira com `gh auth status`).
- **Onde o terminal precisa estar:**
  - Passo 0: dentro da pasta `citizentech-gs-workspace`.
  - Todos os outros blocos: dentro da pasta `zelabairro-frontend` (o clone): `cd ~/zelabairro-frontend`.
- **Ordem:** um passo só começa quando o anterior avisar no grupo "passo NN no develop". Cada bloco começa com `git pull`, então pega o trabalho de quem veio antes.
- **Aviso do npm sobre "vulnerabilities":** é de uma dependência de build do Vite e não afeta o site. **Não rode `npm audit fix --force`** (ele quebra o projeto).
- No meio de cada bloco o script mostra **"O commit deste passo vai sair como: Nome <e-mail>"**. Confira que é a pessoa da vez; se não for, aperte Ctrl+C antes do commit.

## Resumo

| Integrante | GitHub | Commits | Partes que explica na apresentação |
| --- | --- | --- | --- |
| Leonardo Afonço Sousa | `Leonardo-2112` | 8 (+1 commit inicial) | Base do projeto, tema, layout e rotas, tipos, `api.ts` (fetch), estados de tela, lazy/ErrorBoundary, README |
| Syang Cristina Gomes Souza | `SyangSouzaa` | 6 | Home, Sobre, Integrantes, FAQ, componentes de campo e Contato (React Hook Form) |
| Matheus Jones Sousa de Freitas | `Matheus-Jones` | 6 | AuthContext, login, cadastro, RotaProtegida, resumo por bairro e cadastro de gestor |
| Vitor Goncalves de Souza | `v1torceleste` | 6 | Card e badges, previsão da IA, lista com filtros, detalhe (rota com parâmetro), histórico, fotos e Apoiar |
| Joao Machado Nascimento | `MachadoJN` | 6 | Registro de ocorrência, sugestão de apoio (RN07), fotos com FormData, confirmação, fila do painel e mudança de status |
| **Total** | | **33** | (+ merges em `develop` e `main`) |

**Ordem de quem trabalha:** Leonardo (0 e 01–03) → Syang (04–09) → Leonardo (10–12) → Matheus (13–16) → Vitor (17–22) → Joao (23–28) → Matheus (29–30) → Leonardo (31–32 e passos finais).

**Tempo estimado:** 3 a 5 minutos por bloco (o 1º de cada pessoa demora mais por causa do `npm ci`). Com a troca de vez entre as pessoas, **cerca de 2 horas no total**. O mais rápido é fazer numa chamada com todos.

---

## Passo 0 · Preparação

### 0.1 Todos: aceitar o convite e atualizar o workspace
1. Aceite o convite do repositório (e-mail do GitHub ou https://github.com/notifications).
2. Com o terminal **dentro da pasta `citizentech-gs-workspace`**, atualize o workspace (é dele que vêm os arquivos de cada passo):
```bash
git pull && ls entregas/5-front-end/passos
```
   A lista precisa mostrar as pastas `01` a `32`.

### 0.2 Leonardo: commit inicial, `main` e `develop` (só ele, antes de todos)
Terminal **dentro da pasta `citizentech-gs-workspace`**. O bloco clona o repositório ao lado do workspace, configura o seu usuário, cria o commit inicial em `main` e a branch `develop`:
```bash
cd .. && \
git clone https://github.com/Leonardo-2112/zelabairro-frontend.git && \
cd zelabairro-frontend && \
git config user.name "Leonardo-2112" && \
git config user.email "afoncoleonardo21@gmail.com" && \
git checkout -b main && \
printf '# zelabairro-frontend\n' > README.md && \
git add README.md && \
git commit -m "chore: commit inicial" && \
git push -u origin main && \
git checkout -b develop && \
git push -u origin develop
```
### 0.3 Trocar de pessoa (mesma máquina)
Não é preciso outro clone: todos usam `~/zelabairro-frontend`. Antes do primeiro passo de cada pessoa, cole o bloco **"Trocar para o usuário de…"** que aparece na lista de passos. Ele grava o nome e o e-mail da conta dessa pessoa só neste repositório.

---

## Passos

Todos os blocos abaixo rodam com o terminal **dentro da pasta `zelabairro-frontend`**. Cole o bloco inteiro e espere terminar. Deu certo se aparecer `Merged pull request #N` e o último `git pull` trouxer o merge. Só então cole o próximo.

### Trocar para o usuário de Leonardo Afonço Sousa

```bash
git config user.name "Leonardo-2112" && \
git config user.email "afoncoleonardo21@gmail.com"
```

### Passo 01 · Leonardo Afonço Sousa
**Branch:** `feature/estrutura-inicial` · **Commit:** `chore: cria projeto com React, Vite, TypeScript e Tailwind`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/estrutura-inicial && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 01 && \
npm run build && \
git add . && \
git commit -m "chore: cria projeto com React, Vite, TypeScript e Tailwind" && \
git push -u origin feature/estrutura-inicial && \
gh pr create --base develop --head feature/estrutura-inicial --title "chore: cria projeto com React, Vite, TypeScript e Tailwind" --body "Passo 01 do plano de commits." && \
gh pr merge feature/estrutura-inicial --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Cria o projeto do zero: package.json com as dependências, configuração do Vite (plugins do React e do Tailwind), TypeScript em modo strict, index.html em pt-BR e .env.example com a variável VITE_API_URL. A tela só mostra o nome ZelaBairro para provar que tudo funciona.

### Passo 02 · Leonardo Afonço Sousa
**Branch:** `feature/tema-visual` · **Commit:** `style: define tema visual e classes reutilizáveis do Tailwind`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/tema-visual && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 02 && \
npm run build && \
git add . && \
git commit -m "style: define tema visual e classes reutilizáveis do Tailwind" && \
git push -u origin feature/tema-visual && \
gh pr create --base develop --head feature/tema-visual --title "style: define tema visual e classes reutilizáveis do Tailwind" --body "Passo 02 do plano de commits." && \
gh pr merge feature/tema-visual --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** No index.css, o @theme cria as cores da marca (viram classes como bg-marca-700) e as fontes. Em @layer components ficam classes reaproveitadas no site todo: .card, .btn-primario, .campo, .badge. Também liga o foco visível para quem usa teclado.

### Passo 03 · Leonardo Afonço Sousa
**Branch:** `feature/layout-rotas` · **Commit:** `feat: adiciona layout com menu responsivo, rotas e página 404`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/layout-rotas && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 03 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona layout com menu responsivo, rotas e página 404" && \
git push -u origin feature/layout-rotas && \
gh pr create --base develop --head feature/layout-rotas --title "feat: adiciona layout com menu responsivo, rotas e página 404" --body "Passo 03 do plano de commits." && \
gh pr merge feature/layout-rotas --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → / e /qualquer-coisa (404); diminua a janela para ver o menu mobile. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** O BrowserRouter liga as rotas; o MainLayout coloca Header e Footer em volta de toda página (Outlet). O Header tem o menu do desktop e o botão do menu mobile com aria-expanded. O vercel.json faz o F5 funcionar em qualquer rota na Vercel.

### Trocar para o usuário de Syang Cristina Gomes Souza

```bash
git config user.name "SyangSouzaa" && \
git config user.email "syangsouza05@gmail.com"
```

### Passo 04 · Syang Cristina Gomes Souza
**Branch:** `feature/pagina-home` · **Commit:** `feat: cria página inicial com proposta e chamada para registrar`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-home && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 04 && \
npm run build && \
git add . && \
git commit -m "feat: cria página inicial com proposta e chamada para registrar" && \
git push -u origin feature/pagina-home && \
gh pr create --base develop --head feature/pagina-home --title "feat: cria página inicial com proposta e chamada para registrar" --body "Passo 04 do plano de commits." && \
gh pr merge feature/pagina-home --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** A Home apresenta o ZelaBairro: destaque com dois botões (registrar e ver ocorrências), os quatro passos do fluxo gerados com map() a partir de uma lista tipada e uma chamada para o gestor entrar no painel.

### Passo 05 · Syang Cristina Gomes Souza
**Branch:** `feature/pagina-sobre` · **Commit:** `feat: cria página Sobre com problema, solução e ODS`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-sobre && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 05 && \
npm run build && \
git add . && \
git commit -m "feat: cria página Sobre com problema, solução e ODS" && \
git push -u origin feature/pagina-sobre && \
gh pr create --base develop --head feature/pagina-sobre --title "feat: cria página Sobre com problema, solução e ODS" --body "Passo 05 do plano de commits." && \
gh pr merge feature/pagina-sobre --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /sobre. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Cria o componente reutilizável CabecalhoPagina (título + subtítulo) e a página Sobre: o problema, os diferenciais, a fórmula pública da prioridade (RN10) e os ODS 11 e 10. Os blocos repetidos vêm de listas tipadas com interface.

### Passo 06 · Syang Cristina Gomes Souza
**Branch:** `feature/pagina-integrantes` · **Commit:** `feat: cria página de integrantes com fotos e links`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-integrantes && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 06 && \
npm run build && \
git add . && \
git commit -m "feat: cria página de integrantes com fotos e links" && \
git push -u origin feature/pagina-integrantes && \
gh pr create --base develop --head feature/pagina-integrantes --title "feat: cria página de integrantes com fotos e links" --body "Passo 06 do plano de commits." && \
gh pr merge feature/pagina-integrantes --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /integrantes. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Os dados do grupo ficam em src/data/integrantes.ts (interface Integrante), com foto, GitHub e LinkedIn; as fotos ficam em public/img/integrantes. O componente IntegranteCard recebe um integrante por props e mostra foto (com texto alternativo), nome, RM, turma e links; a página faz map() na lista.

### Passo 07 · Syang Cristina Gomes Souza
**Branch:** `feature/pagina-faq` · **Commit:** `feat: cria página FAQ com perguntas em acordeão`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-faq && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 07 && \
npm run build && \
git add . && \
git commit -m "feat: cria página FAQ com perguntas em acordeão" && \
git push -u origin feature/pagina-faq && \
gh pr create --base develop --head feature/pagina-faq --title "feat: cria página FAQ com perguntas em acordeão" --body "Passo 07 do plano de commits." && \
gh pr merge feature/pagina-faq --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /faq (clique nas perguntas). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Cada pergunta é um FaqItem com useState (aberto/fechado). O botão usa aria-expanded e aria-controls para o leitor de tela saber se a resposta está visível. As perguntas ficam em src/data/faq.ts.

### Passo 08 · Syang Cristina Gomes Souza
**Branch:** `feature/componentes-formulario` · **Commit:** `feat: adiciona componentes de campo de formulário acessíveis`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/componentes-formulario && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 08 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona componentes de campo de formulário acessíveis" && \
git push -u origin feature/componentes-formulario && \
gh pr create --base develop --head feature/componentes-formulario --title "feat: adiciona componentes de campo de formulário acessíveis" --body "Passo 08 do plano de commits." && \
gh pr merge feature/componentes-formulario --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build; os campos aparecem no próximo passo). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** CampoFormulario liga o <label> ao campo (htmlFor/id) e mostra dica ou erro. CampoTexto é um input pronto para o React Hook Form: recebe o retorno de register() e o repassa com {...registro}. Serão usados em contato, login, cadastro e painel.

### Passo 09 · Syang Cristina Gomes Souza
**Branch:** `feature/pagina-contato` · **Commit:** `feat: cria página de contato com validação`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-contato && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 09 && \
npm run build && \
git add . && \
git commit -m "feat: cria página de contato com validação" && \
git push -u origin feature/pagina-contato && \
gh pr create --base develop --head feature/pagina-contato --title "feat: cria página de contato com validação" --body "Passo 09 do plano de commits." && \
gh pr merge feature/pagina-contato --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /contato (envie vazio para ver os erros). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Formulário com React Hook Form: register() define as regras (obrigatório, mínimo, formato de e-mail), handleSubmit só chama enviar() se tudo estiver válido e errors traz as mensagens. Ao enviar, mostra a confirmação e limpa os campos (o contato não vai para a API).

### Trocar para o usuário de Leonardo Afonço Sousa

```bash
git config user.name "Leonardo-2112" && \
git config user.email "afoncoleonardo21@gmail.com"
```

### Passo 10 · Leonardo Afonço Sousa
**Branch:** `feature/tipos-api` · **Commit:** `feat: adiciona tipos TypeScript dos dados da API`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/tipos-api && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 10 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona tipos TypeScript dos dados da API" && \
git push -u origin feature/tipos-api && \
gh pr create --base develop --head feature/tipos-api --title "feat: adiciona tipos TypeScript dos dados da API" --body "Passo 10 do plano de commits." && \
gh pr merge feature/tipos-api --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Em src/types ficam as interfaces que espelham o JSON da API Java: Ocorrencia, Categoria, Bairro, Sessao, ErroApi etc. Status e prioridade são union types ('ABERTA' | 'EM_ANDAMENTO'...), e campos que podem vir nulos, como a previsão da IA, têm | null.

### Passo 11 · Leonardo Afonço Sousa
**Branch:** `feature/servico-api` · **Commit:** `feat: cria camada de serviço com Fetch API`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/servico-api && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 11 && \
npm run build && \
git add . && \
git commit -m "feat: cria camada de serviço com Fetch API" && \
git push -u origin feature/servico-api && \
gh pr create --base develop --head feature/servico-api --title "feat: cria camada de serviço com Fetch API" --body "Passo 11 do plano de commits." && \
gh pr merge feature/servico-api --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** src/services/api.ts tem a única função que chama fetch: request<T>(). Ela monta a URL com VITE_API_URL, envia JSON ou FormData, transforma qualquer resposta de erro em ApiError (status + mensagem em português + campos) e devolve os dados já tipados.

### Passo 12 · Leonardo Afonço Sousa
**Branch:** `feature/estados-tela` · **Commit:** `feat: adiciona estados de carregando, erro e vazio`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/estados-tela && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 12 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona estados de carregando, erro e vazio" && \
git push -u origin feature/estados-tela && \
gh pr create --base develop --head feature/estados-tela --title "feat: adiciona estados de carregando, erro e vazio" --body "Passo 12 do plano de commits." && \
gh pr merge feature/estados-tela --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build; aparecem a partir do passo 18). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Três componentes usados em toda tela que chama a API: Carregando (avisa que a API gratuita pode estar acordando), MensagemErro (role=alert e botão Tentar novamente) e EstadoVazio. O hook useRequisicao executa a busca e devolve dados, carregando, erro e recarregar.

### Trocar para o usuário de Matheus Jones Sousa de Freitas

```bash
git config user.name "Matheus-Jones" && \
git config user.email "matheus.jones@icloud.com"
```

### Passo 13 · Matheus Jones Sousa de Freitas
**Branch:** `feature/sessao-usuario` · **Commit:** `feat: cria contexto de autenticação com sessão no navegador`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/sessao-usuario && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 13 && \
npm run build && \
git add . && \
git commit -m "feat: cria contexto de autenticação com sessão no navegador" && \
git push -u origin feature/sessao-usuario && \
gh pr create --base develop --head feature/sessao-usuario --title "feat: cria contexto de autenticação com sessão no navegador" --body "Passo 13 do plano de commits." && \
gh pr merge feature/sessao-usuario --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** O AuthContext guarda quem está logado ({id, nome, perfil}) e salva no localStorage com try/catch. As funções entrar() e sair() ficam disponíveis no app todo pelo hook useAuth(). Em api.ts entram login() e cadastrarCidadao().

### Passo 14 · Matheus Jones Sousa de Freitas
**Branch:** `feature/pagina-login` · **Commit:** `feat: cria página de login integrada à API`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-login && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 14 && \
npm run build && \
git add . && \
git commit -m "feat: cria página de login integrada à API" && \
git push -u origin feature/pagina-login && \
gh pr create --base develop --head feature/pagina-login --title "feat: cria página de login integrada à API" --body "Passo 14 do plano de commits." && \
gh pr merge feature/pagina-login --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /login (teste uma senha errada). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** O formulário chama POST /auth/login. Se der certo, guarda a sessão e leva o gestor ao painel e o cidadão às ocorrências. Se a API responder 401, mostra a mensagem dela; aplicarErrosDaApi leva os campos[] do erro 400 para o campo certo com setError.

### Passo 15 · Matheus Jones Sousa de Freitas
**Branch:** `feature/pagina-cadastro` · **Commit:** `feat: cria página de cadastro de cidadão`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/pagina-cadastro && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 15 && \
npm run build && \
git add . && \
git commit -m "feat: cria página de cadastro de cidadão" && \
git push -u origin feature/pagina-cadastro && \
gh pr create --base develop --head feature/pagina-cadastro --title "feat: cria página de cadastro de cidadão" --body "Passo 15 do plano de commits." && \
gh pr merge feature/pagina-cadastro --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /cadastro (crie uma conta de teste). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Cadastro com validação de nome, e-mail, telefone opcional e senha; o campo 'confirme a senha' usa validate para comparar com getValues('senha'). Envia POST /cidadaos e, se o e-mail já existir, mostra o 409 da API.

### Passo 16 · Matheus Jones Sousa de Freitas
**Branch:** `feature/rota-protegida` · **Commit:** `feat: adiciona rota protegida e menu com sessão`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/rota-protegida && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 16 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona rota protegida e menu com sessão" && \
git push -u origin feature/rota-protegida && \
gh pr create --base develop --head feature/rota-protegida --title "feat: adiciona rota protegida e menu com sessão" --body "Passo 16 do plano de commits." && \
gh pr merge feature/rota-protegida --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → / logado: o menu mostra seu nome e o botão Sair. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** RotaProtegida manda quem não está logado para o /login (com a mensagem e a página de volta) e mostra 'Área restrita' para o perfil errado. O Header passa a mostrar nome, perfil e Sair, e o link Painel só para gestor. Quem barra de verdade é a API (403).

### Trocar para o usuário de Vitor Goncalves de Souza

```bash
git config user.name "v1torceleste" && \
git config user.email "vitorsouza0409@gmail.com"
```

### Passo 17 · Vitor Goncalves de Souza
**Branch:** `feature/card-ocorrencia` · **Commit:** `feat: cria card de ocorrência com badges e previsão de prazo`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/card-ocorrencia && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 17 && \
npm run build && \
git add . && \
git commit -m "feat: cria card de ocorrência com badges e previsão de prazo" && \
git push -u origin feature/card-ocorrencia && \
gh pr create --base develop --head feature/card-ocorrencia --title "feat: cria card de ocorrência com badges e previsão de prazo" --body "Passo 17 do plano de commits." && \
gh pr merge feature/card-ocorrencia --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → (só build; os cards aparecem no próximo passo). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** StatusBadge e PrioridadeBadge mapeiam cada valor para uma cor e um texto. PrevisaoIa mostra 'cerca de N dias · risco alto/baixo' sem porcentagem, ou 'previsão indisponível' quando a IA não respondeu. OcorrenciaCard junta tudo e o card inteiro é um link.

### Passo 18 · Vitor Goncalves de Souza
**Branch:** `feature/lista-ocorrencias` · **Commit:** `feat: lista ocorrências da API com estados de tela`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/lista-ocorrencias && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 18 && \
npm run build && \
git add . && \
git commit -m "feat: lista ocorrências da API com estados de tela" && \
git push -u origin feature/lista-ocorrencias && \
gh pr create --base develop --head feature/lista-ocorrencias --title "feat: lista ocorrências da API com estados de tela" --body "Passo 18 do plano de commits." && \
gh pr merge feature/lista-ocorrencias --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** listarOcorrencias() faz GET /ocorrencias e o hook useOcorrencias usa o useRequisicao. A página mostra Carregando, MensagemErro, EstadoVazio ou a grade de cards (1, 2 ou 3 colunas conforme a largura).

### Passo 19 · Vitor Goncalves de Souza
**Branch:** `feature/filtros-ocorrencias` · **Commit:** `feat: adiciona filtros de status, bairro e categoria`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/filtros-ocorrencias && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 19 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona filtros de status, bairro e categoria" && \
git push -u origin feature/filtros-ocorrencias && \
gh pr create --base develop --head feature/filtros-ocorrencias --title "feat: adiciona filtros de status, bairro e categoria" --body "Passo 19 do plano de commits." && \
gh pr merge feature/filtros-ocorrencias --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias (mude os filtros e veja a URL). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Três <select> com <label>. Os filtros ficam na URL com useSearchParams (?status=ABERTA&idBairro=1), viram parâmetros do GET e, quando mudam, o hook busca de novo. Categorias e bairros vêm da API ao mesmo tempo com Promise.all.

### Passo 20 · Vitor Goncalves de Souza
**Branch:** `feature/detalhe-ocorrencia` · **Commit:** `feat: cria página de detalhe com rota dinâmica`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/detalhe-ocorrencia && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 20 && \
npm run build && \
git add . && \
git commit -m "feat: cria página de detalhe com rota dinâmica" && \
git push -u origin feature/detalhe-ocorrencia && \
gh pr create --base develop --head feature/detalhe-ocorrencia --title "feat: cria página de detalhe com rota dinâmica" --body "Passo 20 do plano de commits." && \
gh pr merge feature/detalhe-ocorrencia --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/1. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Rota com parâmetro: useParams() lê o :id da URL, que vai para GET /ocorrencias/{id}. A página mostra a ficha completa, a prioridade com os pontos e a previsão da IA gravada pela API Java.

### Passo 21 · Vitor Goncalves de Souza
**Branch:** `feature/historico-fotos` · **Commit:** `feat: mostra histórico de status e galeria de fotos`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/historico-fotos && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 21 && \
npm run build && \
git add . && \
git commit -m "feat: mostra histórico de status e galeria de fotos" && \
git push -u origin feature/historico-fotos && \
gh pr create --base develop --head feature/historico-fotos --title "feat: mostra histórico de status e galeria de fotos" --body "Passo 21 do plano de commits." && \
gh pr merge feature/historico-fotos --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/1 (role até Fotos e Histórico). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Dois componentes com seus próprios estados de tela: HistoricoAtualizacoes (GET .../atualizacoes, em linha do tempo) e GaleriaFotos (GET .../fotos). A imagem é carregada direto da API com <img src={VITE_API_URL + url}> e tem texto alternativo.

### Passo 22 · Vitor Goncalves de Souza
**Branch:** `feature/apoiar-ocorrencia` · **Commit:** `feat: adiciona botão de apoiar ocorrência`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/apoiar-ocorrencia && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 22 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona botão de apoiar ocorrência" && \
git push -u origin feature/apoiar-ocorrencia && \
gh pr create --base develop --head feature/apoiar-ocorrencia --title "feat: adiciona botão de apoiar ocorrência" --body "Passo 22 do plano de commits." && \
gh pr merge feature/apoiar-ocorrencia --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/1 logado como cidadão. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** BotaoApoiar faz POST /ocorrencias/{id}/apoios com o id de quem está logado e busca a ocorrência de novo para atualizar apoios e prioridade. Respeita a RN08: não aparece para o autor nem para ocorrência encerrada, e mostra o 409 se a pessoa já apoiou.

### Trocar para o usuário de Joao Machado Nascimento

```bash
git config user.name "MachadoJN" && \
git config user.email "Jmachadonascimento1@gmail.com"
```

### Passo 23 · Joao Machado Nascimento
**Branch:** `feature/nova-ocorrencia` · **Commit:** `feat: cria formulário de registro de ocorrência`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/nova-ocorrencia && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 23 && \
npm run build && \
git add . && \
git commit -m "feat: cria formulário de registro de ocorrência" && \
git push -u origin feature/nova-ocorrencia && \
gh pr create --base develop --head feature/nova-ocorrencia --title "feat: cria formulário de registro de ocorrência" --body "Passo 23 do plano de commits." && \
gh pr merge feature/nova-ocorrencia --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/nova logado como cidadão. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Página protegida (só cidadão). Os selects vêm da API, a descrição valida a RN03 (10 a 500 caracteres, com contador) e o envio faz POST /ocorrencias com o id do usuário logado. Depois mostra a confirmação com o número da ocorrência.

### Passo 24 · Joao Machado Nascimento
**Branch:** `feature/sugestao-apoio` · **Commit:** `feat: sugere apoiar ocorrências parecidas antes de criar`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/sugestao-apoio && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 24 && \
npm run build && \
git add . && \
git commit -m "feat: sugere apoiar ocorrências parecidas antes de criar" && \
git push -u origin feature/sugestao-apoio && \
gh pr create --base develop --head feature/sugestao-apoio --title "feat: sugere apoiar ocorrências parecidas antes de criar" --body "Passo 24 do plano de commits." && \
gh pr merge feature/sugestao-apoio --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/nova (escolha Buraco na via + Lapa). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Regra RN07: watch() acompanha a categoria e o bairro escolhidos e o SugestaoApoio busca as ocorrências abertas iguais. Se existir alguma, mostra um aviso com link para apoiar. É sugestão, não bloqueio.

### Passo 25 · Joao Machado Nascimento
**Branch:** `feature/envio-fotos` · **Commit:** `feat: permite anexar até 3 fotos na ocorrência`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/envio-fotos && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 25 && \
npm run build && \
git add . && \
git commit -m "feat: permite anexar até 3 fotos na ocorrência" && \
git push -u origin feature/envio-fotos && \
gh pr create --base develop --head feature/envio-fotos --title "feat: permite anexar até 3 fotos na ocorrência" --body "Passo 25 do plano de commits." && \
gh pr merge feature/envio-fotos --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/nova (anexe uma foto e registre). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** CampoFotos valida no navegador a RN18 (JPG ou PNG, até 2 MB, no máximo 3) e mostra a prévia com URL.createObjectURL. Depois que o POST devolve o id, cada foto vai num FormData com o cabeçalho X-Cidadao-Id, ainda usando fetch.

### Passo 26 · Joao Machado Nascimento
**Branch:** `feature/confirmacao-previsao` · **Commit:** `feat: mostra previsão de prazo na confirmação do registro`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/confirmacao-previsao && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 26 && \
npm run build && \
git add . && \
git commit -m "feat: mostra previsão de prazo na confirmação do registro" && \
git push -u origin feature/confirmacao-previsao && \
gh pr create --base develop --head feature/confirmacao-previsao --title "feat: mostra previsão de prazo na confirmação do registro" --body "Passo 26 do plano de commits." && \
gh pr merge feature/confirmacao-previsao --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /ocorrencias/nova (registre uma ocorrência). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** ConfirmacaoOcorrencia mostra o resultado do POST: número, status, prioridade e a previsão da IA que veio na própria resposta da API Java (o front nunca chama a IA). Avisa se alguma foto não foi enviada.

### Passo 27 · Joao Machado Nascimento
**Branch:** `feature/painel-fila` · **Commit:** `feat: cria painel do gestor com fila por prioridade`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/painel-fila && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 27 && \
npm run build && \
git add . && \
git commit -m "feat: cria painel do gestor com fila por prioridade" && \
git push -u origin feature/painel-fila && \
gh pr create --base develop --head feature/painel-fila --title "feat: cria painel do gestor com fila por prioridade" --body "Passo 27 do plano de commits." && \
gh pr merge feature/painel-fila --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /painel logado como gestor. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Página protegida só para gestor. Busca as ocorrências (a API já devolve ordenadas por prioridade), mantém só ABERTA e EM_ANDAMENTO e mostra a posição na fila, os pontos, os dias em aberto e a previsão.

### Passo 28 · Joao Machado Nascimento
**Branch:** `feature/mudar-status` · **Commit:** `feat: permite ao gestor mudar o status com comentário`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/mudar-status && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 28 && \
npm run build && \
git add . && \
git commit -m "feat: permite ao gestor mudar o status com comentário" && \
git push -u origin feature/mudar-status && \
gh pr create --base develop --head feature/mudar-status --title "feat: permite ao gestor mudar o status com comentário" --body "Passo 28 do plano de commits." && \
gh pr merge feature/mudar-status --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /painel logado como gestor (mude um status). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** MudarStatus oferece só as transições da RN05 (ABERTA para EM_ANDAMENTO ou CANCELADA; EM_ANDAMENTO para RESOLVIDA ou CANCELADA). Envia POST .../atualizacoes com o cabeçalho X-Gestor-Id e recarrega a fila; um 409 da API aparece no formulário.

### Trocar para o usuário de Matheus Jones Sousa de Freitas

```bash
git config user.name "Matheus-Jones" && \
git config user.email "matheus.jones@icloud.com"
```

### Passo 29 · Matheus Jones Sousa de Freitas
**Branch:** `feature/resumo-bairros` · **Commit:** `feat: adiciona resumo de ocorrências por bairro no painel`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/resumo-bairros && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 29 && \
npm run build && \
git add . && \
git commit -m "feat: adiciona resumo de ocorrências por bairro no painel" && \
git push -u origin feature/resumo-bairros && \
gh pr create --base develop --head feature/resumo-bairros --title "feat: adiciona resumo de ocorrências por bairro no painel" --body "Passo 29 do plano de commits." && \
gh pr merge feature/resumo-bairros --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /painel logado como gestor. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** ResumoBairros chama GET /painel/bairros com X-Gestor-Id e mostra, para cada bairro, quantas ocorrências estão em aberto, atrasadas e resolvidas. Deixa visível onde o atendimento demora mais (ODS 10).

### Passo 30 · Matheus Jones Sousa de Freitas
**Branch:** `feature/cadastro-gestor` · **Commit:** `feat: permite cadastrar novo gestor pelo painel`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/cadastro-gestor && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 30 && \
npm run build && \
git add . && \
git commit -m "feat: permite cadastrar novo gestor pelo painel" && \
git push -u origin feature/cadastro-gestor && \
gh pr create --base develop --head feature/cadastro-gestor --title "feat: permite cadastrar novo gestor pelo painel" --body "Passo 30 do plano de commits." && \
gh pr merge feature/cadastro-gestor --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → /painel logado como gestor (final da página). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Formulário que lista os órgãos (GET /orgaos) e envia POST /gestores com X-Gestor-Id: só um gestor cria outro e a API registra quem cadastrou (RN17). E-mail repetido volta como 409 e aparece na tela.

### Trocar para o usuário de Leonardo Afonço Sousa

```bash
git config user.name "Leonardo-2112" && \
git config user.email "afoncoleonardo21@gmail.com"
```

### Passo 31 · Leonardo Afonço Sousa
**Branch:** `feature/carregamento-sob-demanda` · **Commit:** `perf: carrega páginas sob demanda com lazy e Suspense`

```bash
git checkout develop && \
git pull && \
git checkout -b feature/carregamento-sob-demanda && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 31 && \
npm run build && \
git add . && \
git commit -m "perf: carrega páginas sob demanda com lazy e Suspense" && \
git push -u origin feature/carregamento-sob-demanda && \
gh pr create --base develop --head feature/carregamento-sob-demanda --title "perf: carrega páginas sob demanda com lazy e Suspense" --body "Passo 31 do plano de commits." && \
gh pr merge feature/carregamento-sob-demanda --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → qualquer rota (no build aparecem vários arquivos .js). Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** Cada página vira um arquivo separado com lazy() e só é baixada quando a rota abre; o Suspense mostra Carregando enquanto isso. O ErrorBoundary mostra uma tela amigável se um componente quebrar, e a página volta ao topo a cada navegação.

### Passo 32 · Leonardo Afonço Sousa
**Branch:** `docs/readme` · **Commit:** `docs: escreve README completo e arquivo de identificação`

```bash
git checkout develop && \
git pull && \
git checkout -b docs/readme && \
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 32 && \
npm run build && \
git add . && \
git commit -m "docs: escreve README completo e arquivo de identificação" && \
git push -u origin docs/readme && \
gh pr create --base develop --head docs/readme --title "docs: escreve README completo e arquivo de identificação" --body "Passo 32 do plano de commits." && \
gh pr merge docs/readme --merge && \
git checkout develop && \
git pull
```
- **Ver funcionando (opcional):** `npm run dev` e abra http://localhost:5173 → README.md no GitHub. Para ver as telas com dados da API, crie uma vez o `.env`: `cp .env.example .env`. Feche com Ctrl+C.
- **O que esse código faz:** README com título, objetivo, links (GitHub, Vercel, API, YouTube), tecnologias, rotas, estrutura de pastas, como rodar, integrantes e contato. O identificacao.txt traz RM, nome e turma, exigido dentro do zip.

---

## Passos finais (Leonardo, depois do passo 32)

### F1 · Levar `develop` para `main`
```bash
git checkout develop && \
git pull && \
gh pr create --base main --head develop --title "release: entrega da Global Solution 2026/2" --body "Leva develop para main." && \
gh pr merge develop --merge && \
git checkout main && \
git pull && \
git checkout develop
```

### F2 · Deploy na Vercel (a partir de `main`)
1. vercel.com → *Add New → Project* → importe `zelabairro-frontend` (framework **Vite**; build `npm run build`; saída `dist`; branch de produção `main`).
2. *Environment Variables*: `VITE_API_URL` = `https://zelabairro-api-08ut.onrender.com` (sem barra no final).
3. *Deploy*. Abra a URL e aperte F5 em `/ocorrencias/1` para ver se a rota funciona (o `vercel.json` cuida disso).
4. **Importante:** adicione a URL da Vercel (ex.: `https://zelabairro-frontend.vercel.app`) na variável `CORS_ORIGINS` da API Java no Render, separada por vírgula de `http://localhost:5173`. Sem isso o navegador bloqueia as chamadas e o site mostra "Não foi possível falar com o servidor".
5. Teste na URL publicada: cadastrar → entrar → listar → registrar com foto → detalhe → apoiar (com outra conta) → como gestor, mudar status. Faça em 390, 768 e 1440 px.

### F3 · Links da Vercel e do vídeo no README
Antes, volte para o seu usuário (bloco "Trocar para o usuário de Leonardo Afonço Sousa"). Abra o `README.md`, troque `[colar o link da Vercel]` e `[colar o link do vídeo]` pelos links e salve. Depois cole (terminal dentro de `zelabairro-frontend`):
```bash
git checkout develop && \
git pull && \
git checkout -b docs/links-readme && \
git add README.md && \
git commit -m "docs: adiciona links da Vercel e do vídeo no README" && \
git push -u origin docs/links-readme && \
gh pr create --base develop --head docs/links-readme --title "docs: adiciona links da Vercel e do vídeo no README" --body "Links finais." && \
gh pr merge docs/links-readme --merge && \
git checkout develop && \
git pull
```
Depois repita o bloco do **F1** para levar a mudança à `main` (a Vercel publica sozinha).

### F4 · Tag da versão entregue (opcional)
```bash
git checkout main && \
git pull && \
git tag -a v1.0.0 -m "Entrega da Global Solution 2026/2" && \
git push origin v1.0.0 && \
git checkout develop
```

### F5 · Zip para o Portal (só o Leonardo envia)
Com a `main` atualizada:
```bash
git checkout main && \
git pull && \
node ../citizentech-gs-workspace/entregas/5-front-end/montar-zip.mjs && \
git checkout develop
```
Gera `../ZelaBairro_Front_1TDSPV.zip` (ao lado do clone) sem `node_modules`, `dist`, `.git` e `.env`, com o `identificacao.txt`. O script avisa se passar de 50 MB.

---

## Tabela-resumo

| Passo | Integrante | Branch | Mensagem do commit |
| --- | --- | --- | --- |
| 0 | Leonardo Afonço Sousa | `main` | `chore: commit inicial` |
| 01 | Leonardo Afonço Sousa | `feature/estrutura-inicial` | `chore: cria projeto com React, Vite, TypeScript e Tailwind` |
| 02 | Leonardo Afonço Sousa | `feature/tema-visual` | `style: define tema visual e classes reutilizáveis do Tailwind` |
| 03 | Leonardo Afonço Sousa | `feature/layout-rotas` | `feat: adiciona layout com menu responsivo, rotas e página 404` |
| 04 | Syang Cristina Gomes Souza | `feature/pagina-home` | `feat: cria página inicial com proposta e chamada para registrar` |
| 05 | Syang Cristina Gomes Souza | `feature/pagina-sobre` | `feat: cria página Sobre com problema, solução e ODS` |
| 06 | Syang Cristina Gomes Souza | `feature/pagina-integrantes` | `feat: cria página de integrantes com fotos e links` |
| 07 | Syang Cristina Gomes Souza | `feature/pagina-faq` | `feat: cria página FAQ com perguntas em acordeão` |
| 08 | Syang Cristina Gomes Souza | `feature/componentes-formulario` | `feat: adiciona componentes de campo de formulário acessíveis` |
| 09 | Syang Cristina Gomes Souza | `feature/pagina-contato` | `feat: cria página de contato com validação` |
| 10 | Leonardo Afonço Sousa | `feature/tipos-api` | `feat: adiciona tipos TypeScript dos dados da API` |
| 11 | Leonardo Afonço Sousa | `feature/servico-api` | `feat: cria camada de serviço com Fetch API` |
| 12 | Leonardo Afonço Sousa | `feature/estados-tela` | `feat: adiciona estados de carregando, erro e vazio` |
| 13 | Matheus Jones Sousa de Freitas | `feature/sessao-usuario` | `feat: cria contexto de autenticação com sessão no navegador` |
| 14 | Matheus Jones Sousa de Freitas | `feature/pagina-login` | `feat: cria página de login integrada à API` |
| 15 | Matheus Jones Sousa de Freitas | `feature/pagina-cadastro` | `feat: cria página de cadastro de cidadão` |
| 16 | Matheus Jones Sousa de Freitas | `feature/rota-protegida` | `feat: adiciona rota protegida e menu com sessão` |
| 17 | Vitor Goncalves de Souza | `feature/card-ocorrencia` | `feat: cria card de ocorrência com badges e previsão de prazo` |
| 18 | Vitor Goncalves de Souza | `feature/lista-ocorrencias` | `feat: lista ocorrências da API com estados de tela` |
| 19 | Vitor Goncalves de Souza | `feature/filtros-ocorrencias` | `feat: adiciona filtros de status, bairro e categoria` |
| 20 | Vitor Goncalves de Souza | `feature/detalhe-ocorrencia` | `feat: cria página de detalhe com rota dinâmica` |
| 21 | Vitor Goncalves de Souza | `feature/historico-fotos` | `feat: mostra histórico de status e galeria de fotos` |
| 22 | Vitor Goncalves de Souza | `feature/apoiar-ocorrencia` | `feat: adiciona botão de apoiar ocorrência` |
| 23 | Joao Machado Nascimento | `feature/nova-ocorrencia` | `feat: cria formulário de registro de ocorrência` |
| 24 | Joao Machado Nascimento | `feature/sugestao-apoio` | `feat: sugere apoiar ocorrências parecidas antes de criar` |
| 25 | Joao Machado Nascimento | `feature/envio-fotos` | `feat: permite anexar até 3 fotos na ocorrência` |
| 26 | Joao Machado Nascimento | `feature/confirmacao-previsao` | `feat: mostra previsão de prazo na confirmação do registro` |
| 27 | Joao Machado Nascimento | `feature/painel-fila` | `feat: cria painel do gestor com fila por prioridade` |
| 28 | Joao Machado Nascimento | `feature/mudar-status` | `feat: permite ao gestor mudar o status com comentário` |
| 29 | Matheus Jones Sousa de Freitas | `feature/resumo-bairros` | `feat: adiciona resumo de ocorrências por bairro no painel` |
| 30 | Matheus Jones Sousa de Freitas | `feature/cadastro-gestor` | `feat: permite cadastrar novo gestor pelo painel` |
| 31 | Leonardo Afonço Sousa | `feature/carregamento-sob-demanda` | `perf: carrega páginas sob demanda com lazy e Suspense` |
| 32 | Leonardo Afonço Sousa | `docs/readme` | `docs: escreve README completo e arquivo de identificação` |

---

## Se der problema

**Como saber em que passo o repositório está:**
```bash
git checkout develop && git pull && git log --oneline --first-parent -3
```
A primeira linha mostra o último merge ("Merge branch 'feature/...' into develop").

**O bloco parou no `npm run build` (erro de compilação).** Quase sempre é passo fora de ordem: o passo anterior ainda não estava no `develop`. Desfaça a tentativa e cole o bloco do seu passo de novo:
```bash
git checkout -- . && git clean -fd src public && git checkout develop && git branch -D <branch-do-passo>
```

**O bloco parou no `git push` da branch ("rejected", "permission denied" ou pedido de login).** Faça login no GitHub quando o Git pedir (no Windows abre uma janela). Sem acesso de escrita, confira se aceitou o convite. Depois termine com:
```bash
git push -u origin <branch-do-passo> && gh pr create --base develop --head <branch-do-passo> --title "<mensagem-do-commit>" --body "Passo NN do plano de commits." && gh pr merge <branch-do-passo> --merge && git checkout develop && git pull
```

**O `gh pr merge` falhou ou o PR ficou aberto.** Mescle de novo (sempre com merge commit) e atualize o develop:
```bash
gh pr merge <branch-do-passo> --merge && git checkout develop && git pull
```
Se o `gh` disser que não está logado: `gh auth login`.

**"A branch ... already exists".** Você já tinha começado esse passo. Se o commit ainda não foi feito:
```bash
git checkout develop && git branch -D <branch-do-passo>
```
e cole o bloco de novo. Se o commit já foi feito, termine só o envio e o merge (bloco do item do `git push` acima).

**Esqueci o `git pull` / estou desatualizado.** Os blocos já começam com `git pull`. Se o erro apareceu num comando seu fora do bloco, rode `git checkout develop && git pull` e recomece o passo.

**Conflito no merge.** Só acontece se alguém pulou ou repetiu um passo. Reaplique o seu passo por cima, que é a versão certa, e finalize:
```bash
node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs NN && git add . && git commit -m "fix: resolve conflito com develop" && git push
```

**Commitei na branch errada (ex.: direto no `develop`) e ainda não dei push:**
```bash
git branch <branch-certa> && git reset --hard origin/develop && git checkout <branch-certa>
```
e continue do `git push -u origin <branch-certa>`. Se já deu push direto no `develop`, não apague nada: avise o grupo e siga para o próximo passo (o commit continua sendo seu).

**O script mostrou o nome ou e-mail errado em "O commit deste passo vai sair como".** Se o commit ainda não foi enviado:
```bash
git config user.name "Seu Nome" && git config user.email "email-da-sua-conta@github" && git commit --amend --reset-author --no-edit
```
Se já foi enviado, adicione esse e-mail à sua conta em https://github.com/settings/emails (*Add email address*): o GitHub passa a contar os commits antigos com ele.

**O script diz "esta pasta não é um repositório git" ou "você está dentro do citizentech-gs-workspace".** O terminal está na pasta errada: abra-o dentro de `zelabairro-frontend`.

**O script diz que não achou a pasta de passos.** O workspace não está atualizado (bloco 0.1) ou não está ao lado do clone.

---

## Regras do Git Flow e dos commits
- `main` só recebe o que está pronto para entregar (passos finais). `develop` junta o trabalho. Cada passo nasce de `develop` numa branch `feature/...` (ou `docs/...`) e volta por **Pull Request** com **merge commit** (`gh pr merge --merge`, nunca squash), que preserva a autoria e o histórico de branches.
- Mensagens em português no padrão **Conventional Commits**: `feat:` (funcionalidade), `fix:` (correção), `style:` (visual), `docs:` (documentação), `chore:` (configuração), `perf:` (desempenho).
- Cada um faz os próprios passos com o próprio nome e e-mail (bloco "Trocar para o usuário de…") e explica a sua parte na apresentação.
