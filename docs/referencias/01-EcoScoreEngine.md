# EcoScoreEngine (Challenge) — resumo técnico

- Repositório: https://github.com/Leonardo-2112/EcoScoreEngine (app publicada: https://ecoscoreengine.vercel.app)
- O que fazia: SPA em React (Front-end da Sprint 4 do Challenge SoulUp/FIAP 2026, turma 1TDSPV) em que o participante registra ações sustentáveis, ganha pontos, converte em créditos e saca via PIX, consumindo a API Java publicada no Render.

> Observação importante: apesar do pedido mencionar várias disciplinas, **este repositório contém só o Front-end**. Não há notebooks, Python, Flask, modelos `.joblib`, scripts SQL nem PDFs de Eng. Software aqui. A API Java fica no repo `EcoScoreEngine-API` (resumido à parte). O clone analisado é raso (1 commit visível: merge do PR #75 de `develop`), então o histórico de commits não pôde ser avaliado.

## Disciplinas cobertas

| Disciplina | Pasta / arquivos neste repo |
|---|---|
| Front-end (React + Vite + TS + Tailwind) | `src/`, `index.html`, `vite.config.ts`, `tsconfig*.json`, `package.json`, `vercel.json`, `.env.example` |
| Documentação de entrega (README com integrantes, prints, links, vídeo) | `README.md`, `public/docs/prints/*.png`, `public/img/` |
| IA & Chatbot | **não existe neste repo** |
| Python | **não existe neste repo** |
| Banco de Dados | **não existe neste repo** (só a tipagem dos DTOs em `src/types/api.ts` reflete o modelo) |
| Java | **não existe neste repo** (só é consumida via `VITE_API_URL`) |
| Eng. Software | **não existe neste repo** (o código cita "telas 02 a 14 do protótipo", mas o protótipo não está aqui) |

## Stack e versões

Tiradas de `package.json` (faixas declaradas, não a versão instalada):

| Pacote | Versão | Uso |
|---|---|---|
| react / react-dom | ^19.2.8 | UI |
| react-router-dom | ^7.18.3 | rotas, `lazy()`, rota protegida, 404 |
| react-hook-form | ^7.87.0 | formulários (Contato, Cadastro, Login) |
| tailwindcss + @tailwindcss/vite | ^4.3.3 | estilos (Tailwind v4 com `@theme`) |
| lucide-react | ^1.66.0 | ícones |
| react-error-boundary | ^6.1.6 | `ErrorBoundary` no layout |
| vite | ^8.3.0 | build/dev server |
| @vitejs/plugin-react | ^6.1.1 | plugin React do Vite |
| typescript | ~6.0.2 | tipagem (`tsc -b` no build) |
| oxlint | ^1.81.0 | lint (no lugar do ESLint) |
| @types/node, @types/react, @types/react-dom | ^24.13.3, ^19.2.18, ^19.2.7 | tipos |

README pede Node.js 20+. Não há Axios. API externa pública: ViaCEP.

## Estrutura de pastas

```
EcoScoreEngine/
├── index.html            lang="pt-BR", Google Fonts (Inter, Space Grotesk, IBM Plex Mono)
├── vercel.json           rewrite de tudo para /index.html (SPA)
├── .env.example          VITE_API_URL=https://ecoscoreengine-api.onrender.com
├── .oxlintrc.json        regras react/rules-of-hooks
├── public/               favicon.svg · img/ (fotos dos integrantes, hero) · docs/prints/
└── src/
    ├── main.tsx          StrictMode + BrowserRouter + AuthProvider
    ├── App.tsx           rotas com lazy(), RotaProtegida e path="*"
    ├── index.css         @theme (tokens) + @layer base + @layer components (.card, .btn-primary, .field)
    ├── types/            api.ts (DTOs da API) · member.ts
    ├── services/         api.ts (cliente fetch único) + 1 service por recurso + viaCepService.ts
    ├── contexts/         AuthContext.tsx (sessão em localStorage)
    ├── hooks/            useAuth, useDocumentTitle, useAcoes, useAcao, usePainel, useRanking, useUsuario
    ├── utils/            formatadores.ts (Intl) · validacoes.ts (CPF, telefone, CEP, idade)
    ├── layouts/          MainLayout.tsx (Header + ErrorBoundary + Suspense + Outlet)
    ├── components/       22 componentes (MensagemErro, ListaVazia, GridSkeleton, FormField, Card...)
    ├── data/             members.ts (integrantes, dados estáticos)
    └── pages/            17 páginas XxxPage.tsx (uma por rota)
```

## Padrões que usamos (Front-end)

**1. Cliente HTTP único com fetch** — `src/services/api.ts`. URL vem de `VITE_API_URL`; toda resposta não-2xx vira `ApiError` com mensagem em português por status (0 = rede, 400, 404, 409, 422, 500, 503).

```ts
export async function request<T>(path: string, { method = "GET", body, usuarioId }: RequestOptions = {}): Promise<T> {
  const headers: Record<string, string> = { Accept: "application/json" };
  if (body !== undefined) headers["Content-Type"] = "application/json";
  ...
  try { response = await fetch(`${API_URL}${path}`, { method, headers, body: ... }); }
  catch { throw new ApiError(0, null); }
  if (!response.ok) throw await lerErro(response);
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}
```

**2. Um service fino por recurso** — `src/services/acaoService.ts`, `registroService.ts`, `carteiraService.ts`: cada função só chama `request<T>()` com rota e verbo, comentada com o endpoint.

```ts
// GET /acoes/{id} → ação escolhida (tela 07).
export function getAcaoById(id: number): Promise<Acao> {
  return request<Acao>(`/acoes/${id}`);
}
```

**3. Hook por recurso com loading/erro/recarregar** — `src/hooks/useAcoes.ts`, `useAcao.ts`. Flag `ativo` ignora resposta após desmontar; `tentativa` permite o botão "Tentar novamente"; o id da rota entra nas dependências do `useEffect`.

**4. Tela com os 4 estados** — `src/pages/EscolherAcaoPage.tsx`: `loading ? <GridSkeleton/> : erro ? <MensagemErro onTentarNovamente={recarregar}/> : vazio ? <ListaVazia/> : lista`. Componentes `MensagemErro` (`role="alert"`) e `ListaVazia` (ícone + mensagem + link).

**5. Tipos espelhando o JSON da API, com union types em vez de enum** — `src/types/api.ts` (o `tsconfig` usa `erasableSyntaxOnly`, que proíbe `enum`):

```ts
export type StatusSaque = "PENDENTE" | "PROCESSADO" | "CANCELADO" | "REJEITADO";
export type EstadoRequisicao = "carregando" | "sucesso" | "erro" | "vazio";
export type RegistroComAcao = RegistroAcao & { acaoDetalhe: Acao }; // intersection type
```

**6. Rotas** — `src/App.tsx`: todas as páginas com `lazy()`; um `<Route element={<MainLayout/>}>` pai; rotas com parâmetro (`integrantes/:id`, `registrar/:acaoId`, `registrar/:acaoId/registrada`); `<RotaProtegida/>` (redireciona para `/login` com `state.mensagem`); `path="*"` → `NotFoundPage`. `MainLayout` envolve o `<Outlet/>` em `ErrorBoundary` (com `resetKeys={[location.pathname]}`) e `Suspense`.

**7. Formulários com React Hook Form** — `src/pages/ContatoPage.tsx` e `CadastroPage.tsx`: `register(campo, { required, pattern, validate })`, `noValidate` no form, `aria-invalid` no campo, mensagem de erro abaixo. No Cadastro, erros 400 da API são devolvidos ao campo com `setError(campo, { type: "server", ... })`. Validadores puros em `src/utils/validacoes.ts` (CPF com dígito verificador, CEP, telefone, idade mínima).

**8. POST com tratamento de regra de negócio** — `src/pages/ConfirmarRegistroPage.tsx`: valida no cliente, desabilita o botão (`enviando`), chama o service, navega com o resultado em `navigate(..., { state })`; se `ApiError` 422 com detalhe específico, mostra o estado "limite atingido", senão a caixa vermelha.

**9. Design tokens Tailwind v4** — `src/index.css`: cores e fontes em `@theme` (`--color-primary` gera `bg-primary`), classes reutilizáveis `.card`, `.btn-primary`, `.btn-secondary`, `.field` com `@apply`, foco visível (`focus-visible:outline-2`), botões `min-h-11` (44 px de alvo de toque).

**10. Utilidades** — `src/utils/formatadores.ts` com `Intl.NumberFormat("pt-BR")` (moeda, pontos, kg) e `formatarData("2026-10-01") → "01/10/2026"`; `src/hooks/useDocumentTitle.ts` muda o título da aba por página.

**11. Integrantes como dados estáticos** — `src/data/members.ts` (id, nome, RM, turma, foto, GitHub, LinkedIn) usado em `/integrantes` e na rota dinâmica `/integrantes/:id` (`useParams` + `members.find`).

## Como rodava / deploy

- Local: `npm install` → `cp .env.example .env` → `npm run dev` (http://localhost:5173). Build: `npm run build` (`tsc -b && vite build`). Lint: `npm run lint` (oxlint).
- Deploy: Vercel, com `vercel.json` reescrevendo todas as rotas para `/index.html` (sem isso o F5 em `/ranking` dá 404). `VITE_API_URL` cadastrada em Environment Variables na Vercel; `.env` no `.gitignore`.
- Back-end: API Java (Spring Boot + Oracle) no Render; README avisa que o plano gratuito "dorme" e o primeiro acesso leva até 1 minuto.
- "Login": `POST /auth/login` devolve o usuário (sem token); o id é salvo em `localStorage` e enviado no header `X-Usuario-Id`.
- README de entrega: tecnologias, estrutura de pastas, tabela página → endpoint → verbo, tabela de integrantes com foto/RM/GitHub/LinkedIn, prints, links (GitHub, YouTube, Vercel, Render), como rodar.

## O que reaproveitar no ZelaBairro

| Padrão do EcoScoreEngine | Onde aplicar no ZelaBairro (Documento Base v1.1) |
|---|---|
| `services/api.ts` com `request<T>()`, `ApiError`, mensagens PT-BR por status, tratamento de 204 | 9.2 (toda chamada em `src/services/api.ts`, só fetch, `VITE_API_URL`); status da 8.2 (400, 404, 409, 405, 500) |
| Tipos com union types e campos camelCase iguais ao JSON | 9.2 (`interface Ocorrencia` com `status: 'ABERTA' \| 'EM_ANDAMENTO' \| 'RESOLVIDA' \| 'CANCELADA'`) e 8.3 |
| Hook por recurso (`dados/loading/erro/recarregar`) + tela com 4 estados | 9.2 ("toda tela que chama a API mostra carregando, erro e lista vazia"); componentes `Carregando`, `MensagemErro`, `EstadoVazio` |
| `MensagemErro` e `ListaVazia` | Base direta para `MensagemErro` e `EstadoVazio` exigidos na 9.2 |
| Rota com parâmetro + hook dependente do id (`useAcao(id)`) | 9.1 `/ocorrencias/:id` (detalhe, histórico, Apoiar) |
| `lazy()` + `MainLayout` com `ErrorBoundary`/`Suspense` + `path="*"` | 9.1 (todas as rotas); 404 não é exigido, mas é boa prática |
| React Hook Form + `setError` com erros 400 da API | 9.2 ("formulários validam antes de enviar e mostram sucesso/erro da API"); 9.1 `/contato` e `/ocorrencias/nova` |
| POST que trata 409/422 de regra de negócio como estado da tela | 9.1 `/ocorrencias/:id` Apoiar (409 RN08) e `/painel` mudar status (409 RN05) |
| `@theme` + `.field`, `.btn-primary`, foco visível, alvo 44 px | 9.2 (acessibilidade: label, contraste, foco visível; público idoso) e responsivo 390/768/1440 |
| `data/members.ts` + `IntegrantesPage` | 9.1 `/integrantes` (foto, nome, RM, turma, GitHub, LinkedIn) |
| `ContatoPage` (RHF, sem API, mensagem de sucesso) | 9.1 `/contato` |
| `FaqItem`, `PageHero`, `SobrePage` | 9.1 `/faq`, `/sobre`, `/` |
| Sessão em `localStorage` com `try/catch` (`AuthContext`) | 4.4 "sem login, o front guarda o cidadão escolhido no navegador" |
| `vercel.json` (rewrite SPA) + `.env.example` + `.env` no `.gitignore` | 9 / 12 (deploy na Vercel); 13.3 (nada de chave no código) |
| `formatarData` (AAAA-MM-DD → DD/MM/AAAA) | 8.3 (datas AAAA-MM-DD) nas telas de detalhe e painel |
| README com tabela página → endpoint → verbo, prints e links | 2.1 Front-end (GitHub público, vídeo ≤ 3 min) |

## Divergências e cuidados

- **Formato de erro diferente.** `lerErro()` em `src/services/api.ts` espera `{"erro", "detalhe"}` e, no 400, um mapa `{campo: mensagem}`. O ZelaBairro (8.3) usa `{status, erro, mensagem, caminho, timestamp, campos: [{campo, mensagem}]}`. É preciso trocar `detalhe` por `mensagem` e ler `campos` como array.
- **Chamada fetch fora de `api.ts`.** `src/services/viaCepService.ts` faz `fetch` direto. A 9.2 diz "toda chamada HTTP fica em `src/services/api.ts`". No ZelaBairro, ou não usar API externa, ou colocar tudo em `api.ts` (o mais seguro para a correção é ter todas as funções de serviço dentro de `api.ts`, em vez de um arquivo por recurso).
- **(Atualizado em 15/11, Documento Base v1.2: o ZelaBairro passou a ter login. Reaproveitar `LoginPage`, `AuthContext` e `RotaProtegida`, adaptados à seção 8.5; o texto abaixo é a análise original.)** **Login com senha e header `X-Usuario-Id`.** O ZelaBairro não tem login (4.4 e limitação da seção 14). Não copiar `LoginPage`, `RotaProtegida`, bloqueio por perfil nem o header; `/painel` é página aberta.
- **Rota com parâmetro sobre dados estáticos.** No EcoScore a rota dinâmica institucional (`/integrantes/:id`) lê `data/members.ts`. No ZelaBairro a rota com parâmetro que conta é `/ocorrencias/:id`, lendo da API Java (12: mocks não são aceitos).
- **Contato sem envio.** `ContatoPage` só valida e mostra "Mensagem registrada"; ok para página institucional, mas nenhuma tela da solução pode simular resposta.
- **Pastas extras.** `hooks/`, `contexts/`, `layouts/`, `utils/`, `data/` não conflitam, mas a 9.2 lista `components`, `pages`, `services`, `types`; manter as quatro obrigatórias bem visíveis.
- **Nomes de componentes.** Usar os nomes exigidos pela 9.2 (`OcorrenciaCard`, `StatusBadge`, `PrioridadeBadge`, `Carregando`, `MensagemErro`, `EstadoVazio`) em vez de `GridSkeleton`/`ListaVazia`.
- **Mistura de idiomas no código.** Há nomes em inglês (`Member`, `ContactFormData`, `handleEnviar` com `submitted`) e em português; padronizar em português, como os nomes da 8.3.
- **Classes em TypeScript.** `ApiError extends Error` é uma classe. No front isso é permitido; a proibição de classes e list comprehension vale só para o Python (seção 10). Não levar esse estilo para o app Python.
- **Versões muito novas.** `typescript ~6.0.2`, `vite ^8.3.0` e `oxlint` (em vez de ESLint) funcionaram no Challenge; se o template da disciplina usar ESLint, conferir com o professor antes de trocar.
- Não foram encontrados Axios, JPA, classes Python ou list comprehension neste repo (não há Python nem Java aqui).

## Termos e conceitos que o grupo já domina

- SPA, React Router (rotas aninhadas, `Outlet`, `useParams`, `useNavigate`, `Navigate`, `lazy` + `Suspense`, rota 404)
- Fetch API, `response.ok`, status HTTP (200, 201, 204, 400, 404, 409, 422, 500), JSON camelCase
- Camada de services, custom hooks, Context API (`createContext`/`useContext`)
- Estados de tela: carregando (skeleton), erro com "tentar novamente", lista vazia
- TypeScript: interfaces, union types, intersection types, generics (`request<T>`), `erasableSyntaxOnly`
- React Hook Form: `register`, `handleSubmit`, `validate`, `setError` com erro do servidor
- Tailwind v4: `@theme` (design tokens), `@layer components`, `@apply`, breakpoints `sm/md/lg/xl`
- Error Boundary, acessibilidade (`role="alert"`, `aria-invalid`, `label htmlFor`, `sr-only`, foco visível)
- Variáveis de ambiente no Vite (`import.meta.env.VITE_*`), deploy na Vercel com rewrite de SPA
- API Java no Render (cold start do plano gratuito), integração com API pública (ViaCEP)
