# receitario-cp5 (Front-end) — resumo técnico

- Repositório: https://github.com/Leonardo-2112/receitario-cp5 · Deploy: https://receitario-cp5.vercel.app (segundo o README) · tag `v1.0.1`
- O que fazia: SPA de catálogo de receitas que consome a API pública DummyJSON (`GET /recipes?limit=0` e `GET /recipes/{id}`), com busca por nome, filtro por culinária, favoritos em estado local e página de detalhe.

## Stack e versões

Fonte: `package.json`, `vite.config.ts`, `tsconfig.app.json`, `src/index.css`.

| Item | Versão / configuração |
| ---- | --------------------- |
| React / React DOM | `^19.2.8` |
| Vite | `^8.2.0` com `@vitejs/plugin-react ^6.0.4` |
| TypeScript | `~6.0.2` (`strict` não aparece no `tsconfig.app.json`; tem `noUnusedLocals`, `noUnusedParameters`, `verbatimModuleSyntax`) |
| Tailwind CSS | `^4.3.3` via plugin `@tailwindcss/vite` (Tailwind v4: **não há `tailwind.config.js`**; tema definido em CSS com `@theme`) |
| Roteamento | `react-router-dom ^7.18.3` |
| Ícones | `lucide-react ^1.47.0` |
| Erros de render | `react-error-boundary ^6.1.6` |
| Lint | ESLint `^10.8.0` + `typescript-eslint`, `react-hooks`, `react-refresh` |
| Scripts | `dev: vite --host`, `build: tsc -b && vite build`, `lint`, `preview` |

`vite.config.ts` só registra `plugins: [react(), tailwindcss()]`. Não há HTTP client extra: só `fetch`.

## Estrutura de pastas

```
receitario-cp5/
  index.html            lang="pt-BR", fontes Google (Inter, Space Grotesk, IBM Plex Mono)
  vercel.json           rewrite de todas as rotas para /index.html
  vite.config.ts  eslint.config.js  tsconfig*.json
  public/               favicon.svg, bg-culinaria.svg
  docs/catalogo.png     print para o README
  src/
    main.tsx  App.tsx  index.css
    components/  Header, RecipeCard, RecipeList, RecipeCardSkeleton,
                 RecipeGridSkeleton, ErrorFallback
    hooks/       useRecipes.ts
    layouts/     MainLayout.tsx
    pages/       CatalogPage, RecipePage, NotFoundPage
    services/    recipes.ts
    types/       recipe.ts, recipesResponse.ts
    utils/       formatTime.ts
```

## Padrões que usamos

### Roteamento (react-router-dom v7, com rota de parâmetro)
`src/App.tsx`: `BrowserRouter` + rota de layout sem path + `index`, rota com parâmetro e catch-all. Páginas carregadas com `lazy()`.

```tsx
const RecipePage = lazy(() => import('./pages/RecipePage').then(
  (module) => ({ default: module.RecipePage })))
...
<Route element={<MainLayout />}>
  <Route index element={<CatalogPage />} />
  <Route path="/receitas/:id" element={<RecipePage />} />
  <Route path="*" element={<NotFoundPage />} />
</Route>
```
- Parâmetro lido com `const { id } = useParams()` e convertido com `Number(id)` (`src/pages/RecipePage.tsx`).
- Navegação com `<Link to=...>` (Header, RecipeCard, NotFoundPage).
- `src/layouts/MainLayout.tsx`: Header + `<main>` com `ErrorBoundary` > `Suspense` (fallback = skeleton) > `<Outlet />` + footer.

### Componentes e props tipadas
Export nomeado (`export function X`), props em `interface XProps`, callbacks opcionais e valores padrão na desestruturação (`src/components/RecipeCard.tsx`):

```tsx
interface RecipeCardProps {
    recipe: Recipe
    favorite?: boolean
    onToggleFavorite?: (recipeId: number) => void
}
export function RecipeCard({ recipe, favorite = false, onToggleFavorite }: RecipeCardProps) {
```
- Renderização condicional `{onToggleFavorite && (<button ...>)}`: o mesmo card serve com ou sem o botão.
- `RecipeList` faz `recipes.map(...)` com `key={value.id}` e repassa props ("prop drilling": `CatalogPage` → `RecipeList` → `RecipeCard`).
- `ErrorFallback` tipado com `FallbackProps` da lib.

### Estado
- Só `useState`, `useEffect` e `useMemo`; **sem Context, sem Redux**.
- Custom hook `src/hooks/useRecipes.ts` encapsula lista + `loading` + `error` e devolve objeto tipado (`interface useRecipesResult`). Também deriva a lista de culinárias com `new Set`.
- Filtro com `useMemo` sobre `[recipes, cuisine, query]` (`CatalogPage.tsx`).
- Atualização funcional de estado: `setFavorites((current) => current.includes(id) ? current.filter(...) : [...current, id])`.
- `RecipePage` reseta o estado quando o `id` da URL muda (compara `id !== currentId` durante o render).

### Chamadas HTTP (fetch, camada de serviço)
`src/services/recipes.ts`: funções que retornam `Promise<Tipo>`, com `.then` encadeado, checagem de `response.ok` e 404 tratado como `null`:

```ts
export function getRecipeById(id: number): Promise<Recipe | null> {
    const response = fetch(`${API}/recipes/${id}`)
        .then((data) => {
            if (data.status === 404) { return null }
            if (!data.ok) { throw new Error('Não foi possível carregar a receita') }
            return data.json() as Promise<Recipe>
        })
    return response
}
```
- URL base fixa no código: `const API = 'https://dummyjson.com'`.
- Só GET; não existe POST/PUT/DELETE no projeto.
- Estados na tela (`CatalogPage.tsx`), em ternário encadeado:

```tsx
loading ? <RecipeGridSkeleton /> :
error ? <p className="... text-red-600">{error}</p> :
filtered.length === 0 ? <p ...>Nenhuma receita encontrada</p> :
<RecipeList recipes={filtered} ... />
```
- `RecipePage` usa early returns: carregando → erro → "Receita não encontrada" (null) → conteúdo.

### Formulários e validação
- Não há formulário com envio. Há apenas um `<input>` de busca e um `<select>` controlados (`value` + `onChange`) na `CatalogPage`.
- Não usa react-hook-form nem zod; não existe validação de campos nem mensagens de sucesso.

### Estilização Tailwind e responsividade
- `src/index.css`: `@import "tailwindcss"`, `@theme` com fontes (`--font-display`, `--font-sans`, `--font-mono`), `@layer base` (body) e `@layer components` com classes próprias via `@apply`: `.card`, `.btn-primary`, `.field`, `.recipe-grid`.

```css
.recipe-grid {
    @apply grid grid-cols-1 gap-5 min-[480px]:grid-cols-2 md:grid-cols-3 xl:grid-cols-4
}
```
- Mobile-first com breakpoints `sm:`, `md:`, `xl:` e arbitrário `min-[480px]:`; container `mx-auto max-w-7xl px-4 sm:px-6`; detalhe em `grid sm:grid-cols-2`.
- Header `sticky top-0` com `backdrop-blur-sm`; skeletons com `animate-pulse`; imagens `aspect-4/3 object-cover`.
- Foco visível: `focus-visible:ring-2 focus-visible:ring-orange-500` em botões e campos.

### Tipos / interfaces
- `src/types/recipe.ts`: `interface Recipe` espelha o JSON da API (campos com mesmo nome).
- `src/types/recipesResponse.ts`: envelope `{ recipes: Recipe[]; total; skip; limit }`.
- `import type` em todo o código (exigido por `verbatimModuleSyntax`).

### Acessibilidade (o que existe)
- `lang="pt-BR"`, `alt` nas imagens, botão de favorito com `aria-label` e `aria-pressed`, `<dl>/<dt>/<dd>` para tempos, `<ol>` para passos.

### Variáveis de ambiente
- Nenhuma. Não há `.env`, `.env.example` nem `import.meta.env` no código (`*.local` está no `.gitignore`).

### Deploy
- Vercel, preset Vite, com `vercel.json` para SPA: `{"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]}` (permite recarregar `/receitas/:id`).
- README documenta Git Flow (main/develop, `feature/*`, PRs, `release/1.0.0`, tag) e Conventional Commits (`feat:`, `fix:`, `refactor:`, `style:`, `docs:`).

## Mapa para o ZelaBairro

| Padrão encontrado no receitario | Onde aplicar no ZelaBairro (seção 9) |
| ------------------------------- | ------------------------------------ |
| `BrowserRouter` + `MainLayout` com `<Outlet />` | `App.tsx` com as 9 rotas (`/`, `/sobre`, `/integrantes`, `/faq`, `/contato`, `/ocorrencias`, `/ocorrencias/nova`, `/ocorrencias/:id`, `/painel`) |
| Rota `/receitas/:id` + `useParams` + `Number(id)` | `/ocorrencias/:id` → `OcorrenciaDetalhePage` |
| Catch-all `*` → `NotFoundPage` | Mesmo padrão (garante "acesso direto às rotas sem erros") |
| `vercel.json` com rewrite | Copiar igual para o front do ZelaBairro |
| `services/recipes.ts` (fetch + `ok` + 404→null) | `services/api.ts` (`getOcorrencias`, `getOcorrenciaById`, `criarOcorrencia`, `apoiar`, `criarAtualizacao`, `getBairros`, `getCategorias`) |
| `types/recipe.ts` espelhando o JSON | `types/ocorrencia.ts`, `bairro.ts`, `categoria.ts`, `erroApi.ts` copiando a seção 8.3 |
| `useRecipes` (lista + loading + error) | `useOcorrencias(filtros)` para `/ocorrencias` e `/painel` |
| Ternário loading/erro/vazio + skeleton | `Carregando`, `MensagemErro`, `EstadoVazio` em toda tela que chama a API |
| `RecipeCard` com prop opcional de ação | `OcorrenciaCard` (botão Apoiar opcional); `RecipeList` → `OcorrenciaList` |
| Filtro com `<select>` controlado + `useMemo` | Filtros status/bairro/categoria em `/ocorrencias` (ou via query string na API) |
| Classes `@layer components` (`.card`, `.btn-primary`, `.field`) | Mesmas classes base; acrescentar `.badge` para `StatusBadge`/`PrioridadeBadge` |
| `.recipe-grid` responsiva | Grade de `OcorrenciaCard` (testar 390/768/1440) |
| `aria-label` / `aria-pressed` no favorito | Botão Apoiar; `label` em todo campo dos formulários |
| `ErrorBoundary` + `Suspense` + `lazy` no layout | Igual no `MainLayout` do ZelaBairro |

## Lacunas frente às exigências da GS 2026/2

O que o receitario **não** tem e o ZelaBairro precisa (só o que foi verificado no código):

1. **Nenhuma operação de escrita** (POST/PUT/PATCH/DELETE): só GET. A GS dá 4 pts para escrita.
2. **Nenhum formulário com validação** nem mensagens de erro/sucesso (critério 05, 7 pts; e `/contato`, `/ocorrencias/nova`).
3. **URL da API fixa no código**; não usa `VITE_API_URL` / `import.meta.env` nem `.env.example`.
4. **Sem menu de navegação**: o Header só tem o logo. A GS exige menu e a apresentação pede demonstrar **menu mobile** ao vivo.
5. **Sem páginas institucionais** (Home, Sobre, Integrantes, FAQ, Contato): só 3 páginas.
6. **Campos de busca/filtro sem `<label>`** (só `placeholder`); o Documento Base exige label em todo campo.
7. Não trata o **formato de erro JSON** da API (`mensagem`, `campos[]`); a mensagem de erro é texto fixo no service.
8. Serviço em arquivo por recurso (`recipes.ts`); o Documento Base pede `src/services/api.ts` único (ajuste simples).
9. `tsconfig.app.json` não liga `"strict": true` (vale ligar no ZelaBairro).
10. Responsividade não documentada nas resoluções exatas 390/768/1440 (usa breakpoints padrão do Tailwind).
11. Clone raso (1 commit visível): **não foi possível conferir** commits por integrante nem branches neste repositório.

Pontos já alinhados: React + Vite + TS + Tailwind, só Fetch API (sem Axios), pastas components/pages/services/types, rota com parâmetro, tratamento de loading/erro/vazio, deploy Vercel com rewrite, README com rotas e comandos.

## Esqueleto sugerido do front do ZelaBairro

```
zelabairro-front/
  index.html                lang="pt-BR"
  vercel.json               rewrite /(.*) → /index.html
  .env.example              VITE_API_URL=https://<api-java>.onrender.com
  vite.config.ts            react() + tailwindcss()
  src/
    main.tsx  App.tsx  index.css     (@theme + .card .btn-primary .field .badge)
    layouts/MainLayout.tsx           Header + Outlet + Footer + ErrorBoundary/Suspense
    components/
      Header.tsx  MenuMobile.tsx  Footer.tsx
      OcorrenciaCard.tsx  OcorrenciaList.tsx
      StatusBadge.tsx  PrioridadeBadge.tsx
      Carregando.tsx  MensagemErro.tsx  EstadoVazio.tsx
      CampoTexto.tsx                 input + label + mensagem de erro
      ErrorFallback.tsx
    pages/
      HomePage  SobrePage  IntegrantesPage  FaqPage  ContatoPage
      OcorrenciasPage                /ocorrencias (GET + filtros)
      NovaOcorrenciaPage             /ocorrencias/nova (POST + RN03 + RN07)
      OcorrenciaDetalhePage          /ocorrencias/:id (GET, histórico, POST apoio)
      PainelPage                     /painel (fila, POST atualização de status)
      NotFoundPage
    services/api.ts                  const API = import.meta.env.VITE_API_URL; fetch
    hooks/useOcorrencias.ts  useOcorrencia.ts
    types/ocorrencia.ts  categoria.ts  bairro.ts  cidadao.ts  atualizacao.ts  erroApi.ts
    utils/validacao.ts  formatarData.ts
    data/integrantes.ts  faq.ts      conteúdo estático das institucionais
```

## Termos que o grupo já domina

- SPA, React + Vite + TypeScript, componente funcional, props tipadas com `interface`
- `useState`, `useEffect`, `useMemo`, custom hook (`useRecipes`)
- React Router: `BrowserRouter`, `Routes/Route`, rota de layout, `Outlet`, `Link`, `useParams`, rota com parâmetro, catch-all 404
- Fetch API, `Promise`/`.then/.catch/.finally`, `response.ok`, tratamento de 404
- Estados de carregando / erro / vazio, skeleton loading
- `lazy` + `Suspense` (code splitting), `ErrorBoundary`
- Tailwind v4: classes utilitárias, `@theme`, `@layer`, `@apply`, mobile-first, breakpoints `sm/md/xl`
- Componente controlado (`value` + `onChange`), renderização condicional, `map` com `key`
- Deploy na Vercel com `vercel.json` (rewrite de SPA), Git Flow e Conventional Commits
