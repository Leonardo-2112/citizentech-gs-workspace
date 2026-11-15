# OrbitalMed (1ª Global Solution) — resumo técnico

- Repositório: https://github.com/Leonardo-2112/OrbitalMed (GS 2026/1, tema "O Espaço e a Nova Fronteira", grupo **GaiaTech**, turma 1TDSPV).
- Problema e solução: comunidades isoladas (Amazônia, Pantanal, Sertão) demoram dias para ter atendimento médico. A proposta é telemedicina via satélite de baixa órbita, em que o Agente Comunitário de Saúde (ACS) faz a triagem e um médico remoto orienta. O repositório é **só o site institucional** com uma simulação de triagem.

## Disciplinas cobertas

| Disciplina | Arquivos no repositório |
|---|---|
| Front-End Design Engineering (README: "Contexto acadêmico") | `index.html`, `pages/*.html` (6), `css/style.css`, `css/responsive.css`, `js/main.js`, `assets/` |
| Python, Banco de Dados, Java, IA, Eng. Software/Negócio | **Nada neste repositório.** Não há `.py`, `.sql`, PDF, BMC nem pitch. Se existiram, foram entregues em outro lugar |

## Stack

- HTML5, CSS3 e JavaScript puro (sem framework, sem build, sem dependências). Para manter a compatibilidade, o código usa `var` e `for` clássico.
- Google Fonts: Exo 2 e Orbitron.
- Git/GitHub. O README não cita deploy (Vercel ou GitHub Pages). O README também usa um diagrama Mermaid.

## Estrutura de pastas

```text
OrbitalMed/
├── index.html            # home
├── pages/                # sobre, solucao, triagem, faq, integrantes, contato
├── css/style.css         # ~876 linhas, variáveis em :root
├── css/responsive.css    # media queries 992 / 768 / 480 px
├── js/main.js            # ~319 linhas, todas as interações
├── assets/foto_*.png     # 5 fotos dos integrantes
├── assets/prints/*.png   # 7 prints de tela usados no README
└── README.md             # ~294 linhas
```

## Padrões que usamos

**Front-end: HTML semântico e acessível.** Todas as páginas repetem o mesmo esqueleto (`header.site-header > nav.navbar`, `main` com `section.page-hero` e `section.section-space`, e `footer.site-footer`). O link da página atual leva `class="active"`. O botão do menu mobile tem ARIA (`pages/triagem.html`):
```html
<button class="menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false">
  <span></span><span></span><span></span>
</button>
...
<label for="symptoms">Digite os sintomas</label>
<textarea id="symptoms" name="symptoms" rows="6"></textarea>
<div class="triage-result" id="triageResult" role="status" aria-live="polite"></div>
```

**CSS: tokens e breakpoints.** As cores ficam em variáveis em `css/style.css` (`--bg`, `--azul`, `--borda`, `--sombra`), com um reset básico. Em `css/responsive.css`, os grids de 3 colunas passam para 2 colunas até 992px e para 1 coluna até 768px. O ajuste fino fica em 480px.
```css
@media (max-width: 992px) {
  .menu-toggle { display: block; }
  .nav-menu.open { display: flex; }
  .split-layout, .split-layout.reverse, .contact-layout { grid-template-columns: 1fr; }
}
```

**JS: uma função por recurso, chamada no `DOMContentLoaded`** (`js/main.js`). As funções são `menuMobile`, `faqAcordeao` (abre um item por vez), `formularioContato` (validação com mensagem por campo em `[data-error-for]` e regex de e-mail), `formularioTriagem`, `animacaoFadeIn` (IntersectionObserver) e `scrollSuave`. Cada função sai cedo se o elemento não existe na página.

**Regra de negócio em dados** (`js/main.js`): os níveis de urgência ficam numa lista ordenada do mais grave ao mais leve, e o código para no primeiro nível que casa:
```js
var URGENCIAS = [
  { nivel: "Crítica", instrucao: "Acionar emergência imediatamente...",
    sintomas: ["convulsão", "sangramento intenso", "inconsciência", ...] },
  { nivel: "Alta", ... }, { nivel: "Média", ... }, { nivel: "Baixa", ... }
];
// texto normalizado com removerAcentos() + toLowerCase() antes do includes()
```

**Componentes visuais recorrentes:** `stat-card` (números na home), `cards-grid` com ODS 3, 9 e 10, `flow-diagram` (Paciente → ACS → Satélite → Médico, em `pages/solucao.html`), `comparison-card` com variante `featured`, `urgency-table` com `role="table"` e cores por nível, `team-card` (foto, nome, RM, turma, GitHub e LinkedIn) e `faq-item` em acordeão.

**Documentação (README.md):** pitch de uma linha ("O satélite é o meio. A pessoa em sofrimento é o propósito."), seguido de objetivo, problema, solução em 3 camadas, relação com o tema, ODS, público-alvo (usuários diretos × organizações contratantes), diferenciais, funcionalidades, tabela de páginas, tecnologias, árvore de pastas, fluxo em Mermaid, prints, responsividade, tabela de integrantes, link do repositório e contexto acadêmico.

**Modelo de negócio (só esboço):** o README separa quem usa (ACS, pacientes) de quem contrata (prefeituras, secretarias, Ministério da Saúde, ONGs). Não há preço, BMC, ROI nem SLA.

## Como a entrega foi organizada

- O README funciona como documento de entrega: descreve tudo, embute os 7 prints (`assets/prints/`) e traz a tabela de integrantes com RM, turma, GitHub e LinkedIn.
- A página `integrantes.html` repete esses dados com foto.
- Não foram encontrados no repositório: `.txt` de integrantes, `.zip`, link de vídeo, link de deploy, PDF.
- O histórico do Git não pôde ser avaliado porque o clone é raso (1 commit visível). O último merge é o "PR #65", o que indica trabalho com branches e PRs.

## O que reaproveitar no ZelaBairro

| Padrão do OrbitalMed | Onde aplicar (Documento Base v1.1) |
|---|---|
| 5 páginas institucionais (home, sobre, FAQ, integrantes, contato) | §9.1: rotas `/`, `/sobre`, `/faq`, `/integrantes`, `/contato`. O conteúdo e a ordem das seções podem ser portados para componentes React |
| `team-card` com foto, nome, RM, turma, GitHub e LinkedIn | §9.1 `/integrantes` |
| Validação do contato com mensagem por campo + `role="status"` | §9.1 `/contato` e §9.2 ("formulários validam antes de enviar") |
| `label for` em todo campo, `aria-expanded`, `aria-live` | §9.2 Acessibilidade |
| Breakpoints e passagem dos grids de 3 → 2 → 1 coluna | §9.2: testar em 390, 768 e 1440 px (reescrever em Tailwind `md:`/`lg:`) |
| Variáveis de cor em `:root` | §9.2. Usar como tema do Tailwind |
| Cores por nível em `urgency-table` | §9.2 `StatusBadge` e `PrioridadeBadge` |
| `URGENCIAS` como dados ordenados por gravidade | §10 (constantes em tuplas, fila de prioridade RN10). Em Python usar tupla/dicionário + `for` |
| `removerAcentos` + `lower()` antes de comparar | §10 opção 1 (sugerir similares, RN07) |
| `flow-diagram` do fluxo da solução | §9.1 `/sobre` e pitch (§2.1 Eng. Software) |
| README completo com prints e tabela de integrantes | §2.1 Front-end (GitHub público) e §13.3 |
| Público "usuário × quem contrata" | §11: cidadão/gestor × prefeitura (B2G) |
| Cards de ODS | §11: ODS 11 (11.3, 11.5) e ODS 10 |

## Divergências e cuidados

- **Stack mudou:** antes era HTML/CSS/JS puro em arquivos `.html` soltos. Agora é obrigatório React + Vite + TS + Tailwind (§2.1). Reaproveitar o conteúdo e o layout, não os arquivos.
- **Sem API:** o OrbitalMed não fazia nenhuma chamada HTTP e a triagem era 100% local. O ZelaBairro exige Fetch API em `src/services/api.ts` com estados de carregando, erro e vazio (§9.2).
- **Formulário de contato "falso":** ele só exibe sucesso e limpa os campos. Isso basta para `/contato`, mas os formulários da solução precisam mostrar a resposta real da API.
- **`innerHTML` com concatenação** em `formularioTriagem`. No React, renderizar via JSX.
- **Sem deploy nem vídeo documentados:** o ZelaBairro exige Vercel e vídeo ≤ 3 min (§2.1). Colocar os links no README.
- **Commits:** a regra é ≥ 5 por integrante (§9.2). Como o histórico do OrbitalMed não estava disponível, não dá para saber se isso foi cumprido.
- **Revisar o texto:** há muitas palavras sem acento ("Navegacao", "Niveis", "diagnosticos", "satálites"). Os e-mails divergem entre o README (`orbitalmed@gmail.com`) e `contato.html` (`orbitalmed@gmail.com.br`). Os `alt` das fotos ainda dizem "Foto placeholder".
- Os itens específicos de Python (classes, list comprehension) não se aplicam, porque não há Python neste repositório.

## Termos e conceitos que o grupo já domina

HTML semântico (`header/nav/main/section/article/aside/footer`); atributos ARIA (`aria-label`, `aria-expanded`, `aria-live`, `role`); CSS custom properties; Grid e Flexbox; media queries e menu hambúrguer; acordeão; validação de formulário com `preventDefault` e regex; IntersectionObserver; normalização de texto (NFD, remoção de acentos); regra de classificação por níveis de prioridade; ODS da ONU; público usuário × contratante (B2G); README com prints e diagrama Mermaid; fluxo com PRs no GitHub.
