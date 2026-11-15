# 5 · Front-End Design Engineering

Depende da **API Java publicada** (mocks não são aceitos). Base: Documento Base v1.4, seção 9; padrões em [`docs/referencias/01-EcoScoreEngine.md`](../../docs/referencias/01-EcoScoreEngine.md) e [`03-receitario-cp5.md`](../../docs/referencias/03-receitario-cp5.md); plano seção 4.

> **Atenção:** a matéria exige um **repositório GitHub público** com pelo menos **5 commits de cada integrante** (15 no total). Este repositório é privado, então o código do front deve viver num repositório público próprio (ex.: `zelabairro-front`). Esta pasta guarda só o que ajuda a entrega: links, checklist e, se quiserem, uma cópia final.

## O que registrar aqui
- [ ] URL do repositório público
- [ ] URL da Vercel
- [ ] URL da API Java (Render)
- [ ] Link do vídeo (até 3 min, público ou não listado)

## Checklist
- [ ] React + Vite + TypeScript + Tailwind; **só `fetch`**, centralizado em `src/services/api.ts`, URL em `VITE_API_URL`
- [ ] Home, Integrantes, Sobre, FAQ, Contato + páginas da solução (`/ocorrencias`, `/ocorrencias/nova`, `/ocorrencias/:id`, `/login`, `/cadastro`, `/painel`)
- [ ] GET e escrita reais na API; carregando, erro e vazio em toda tela; formulários com validação e mensagens
- [ ] Responsivo em 390×844, 768×1024 e 1440×900, sem rolagem horizontal
- [ ] README com título, objetivo, tecnologias, pastas, integrantes, execução e links (GitHub, Vercel, API, YouTube)
- [ ] Zip até 50 MB, **sem `node_modules`**, com `.txt`
