# 5 · Front-End Design Engineering

Depende da **API Java publicada** (mocks não são aceitos). Base: Documento Base v1.5, seção 9; padrões em [`docs/referencias/01-EcoScoreEngine.md`](../../docs/referencias/01-EcoScoreEngine.md) e [`03-receitario-cp5.md`](../../docs/referencias/03-receitario-cp5.md); plano seção 4.

> **Atenção:** a matéria exige um **repositório GitHub público** com pelo menos **5 commits de cada integrante** (15 no total). Este repositório é privado, então o código do front vai para o repositório público [`Leonardo-2112/zelabairro-frontend`](https://github.com/Leonardo-2112/zelabairro-frontend), reproduzido pelos integrantes passo a passo.

## O que tem nesta pasta

| Arquivo | Para quê |
| --- | --- |
| [`zelabairro-front/`](zelabairro-front/) | **Projeto de referência** completo (o "gabarito"), testado contra a API do Render |
| [`PLANO_DE_COMMITS.md`](PLANO_DE_COMMITS.md) | Passo 0, os 32 passos como blocos de colar no terminal (Git Flow + Conventional Commits), passos finais, tabela-resumo e "se der problema" |
| [`aplicar-passo.mjs`](aplicar-passo.mjs) | Copia os arquivos de um passo para o clone do repositório público: `node ../citizentech-gs-workspace/entregas/5-front-end/aplicar-passo.mjs 07` |
| [`passos/`](passos/) | Snapshot de cada passo (só os arquivos que ele cria ou altera, na versão daquele momento) |
| [`montar-zip.mjs`](montar-zip.mjs) | Gera o zip da entrega sem `node_modules`, `dist`, `.git` e `.env`, conferindo o limite de 50 MB |

## O que registrar aqui
- [x] URL do repositório público: https://github.com/Leonardo-2112/zelabairro-frontend (passos aplicados pelo grupo; `main` com a tag `v1.0.1`)
- [x] URL da Vercel: https://zelabairro-frontend.vercel.app
- [x] URL da API Java (Render): https://zelabairro-api-08ut.onrender.com
- [x] Link do vídeo (até 3 min, público ou não listado): https://youtu.be/IfAloPZ-dAE

## Checklist
- [x] React 19 + Vite 8 + TypeScript (`strict`) + Tailwind 4; **só `fetch`**, centralizado em `src/services/api.ts`, URL em `VITE_API_URL` (`.env.example`, sem `.env` versionado)
- [x] Home, Integrantes, Sobre, FAQ, Contato + páginas da solução (`/ocorrencias`, `/ocorrencias/nova`, `/ocorrencias/:id`, `/login`, `/cadastro`, `/painel`) + 404; `vercel.json` com rewrite da SPA
- [x] GET e escrita reais na API (cadastro, login, criar ocorrência com foto, apoiar); carregando, erro e vazio em toda tela; formulários com validação e `campos[]` da API no `setError` — **testado em 18/11** contra o Render
- [x] Previsão da IA só a partir do JSON da Java ("cerca de N dias · risco alto/baixo" ou "previsão indisponível")
- [x] Responsivo em 390×844, 768×1024 e 1440×900, sem rolagem horizontal (14 rotas medidas em 18/11)
- [x] Painel do gestor testado em 18/11 com o gestor inicial do seed (senha de teste no `GUIA_EXECUCAO.md` do Banco): fila por prioridade, resumo por bairro, mudança de status ABERTA → EM_ANDAMENTO → RESOLVIDA com histórico no detalhe, e cadastro de gestor (validação e 409 de e-mail repetido); sem rolagem horizontal em 390, 768 e 1440 px
- [x] README com título, objetivo, tecnologias, pastas, integrantes, execução, contato e links (GitHub, Vercel e YouTube preenchidos)
- [x] Plano de commits validado em 18/11: todos os blocos executados com 5 clones e um remoto de teste; 32 builds OK, 6+ commits por integrante, 32 merges em `develop`, merge em `main`, tag, resultado idêntico à referência
- [x] **Grupo:** passos aplicados, cada um com a própria conta. Na `main` em 18/11: Leonardo 42, Syang 12, João, Matheus e Vitor 6 commits cada
- [x] **Grupo:** deploy na Vercel com `VITE_API_URL`; `CORS_ORIGINS` da API aceita `https://zelabairro-frontend.vercel.app` (conferido em 18/11)
- [x] **Grupo:** vídeo de até 3 min
- [x] Zip `ZelaBairro_Front_1TDSPV.zip` (0,18 MB, 79 arquivos) gerado em 18/11 com `montar-zip.mjs` a partir de um clone da `main` do repositório público (idêntica à referência): sem `node_modules`, `dist`, `.git` e `.env`, com `identificacao.txt`
- [ ] **Grupo:** enviar o zip no Portal até 19/11 23h55

## Divergências registradas
- **API × Documento Base 8.3:** a API devolve `riscoAtraso` como `"ALTO"`/`"BAIXO"` (não `"S"`/`"N"`), traz `idAutor`, a categoria vem com `descricao` e `idOrgao`, o bairro com `populacao`, e existe `GET /orgaos`. O front segue a API.
- **PDF × Documento Base:** nenhum conflito encontrado para o front.
