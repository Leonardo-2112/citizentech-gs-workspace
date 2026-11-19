# Roteiro dos vídeos · Front-end e Java

Dois vídeos separados, gravados pelo **João**:

| Vídeo | Duração máxima | YouTube | Vai em |
| --- | --- | --- | --- |
| **1 · Front-end** | **3 min** | público ou **não listado** | README do `zelabairro-frontend` (tabela de links) |
| **2 · Java** | **5 min** | **não listado** (obrigatório) | `zelabairro-api/README.md`, `gerar_documentacao.py` (capa do PDF) e README da pasta `4-java` |

Os textos entre aspas são sugestões de fala: pode falar com as suas palavras, desde que passe pelos mesmos pontos e respeite os tempos. Se estourar o tempo, corte as partes marcadas com *(opcional)*.

---

## Preparação (fazer antes de gravar os dois)

1. **Acorde a API 5 minutos antes:** abra https://zelabairro-api-08ut.onrender.com/health no navegador e espere aparecer a resposta. O plano gratuito do Render "dorme" e o primeiro acesso leva até 1 minuto: isso não pode cair no vídeo.
2. **Contas de teste:**
   - Cidadão: crie uma conta nova em `/cadastro` **durante** o vídeo 1 (ex.: `joao.video@email.exemplo.com`, senha `teste123`) e anote. Para o apoio, use uma segunda conta já criada antes (ex.: `apoio.video@email.exemplo.com`).
   - Gestor: `marcia.santos@prefeitura.exemplo.gov.br`, com a senha de teste do seed (seção 2 do `entregas/2-banco-de-dados/GUIA_EXECUCAO.md`).
3. **Tenha uma foto** JPG ou PNG pequena (menos de 2 MB) no computador, de preferência de um problema de rua (buraco, lixo).
4. **Navegador:** Chrome em tela cheia, zoom 100%, abas extras fechadas, sem favoritos e notificações à vista. Feche WhatsApp, e-mail e qualquer coisa com dados pessoais.
5. **Gravação:** OBS Studio (grátis) ou a gravação de tela do Windows (Win + Alt + R) / macOS (Cmd + Shift + 5). Microfone ligado e ambiente silencioso; grave em 1080p.
6. **Abas já abertas** antes de começar:
   - Vídeo 1: https://zelabairro-frontend.vercel.app
   - Vídeo 2: o site, o Postman com a coleção `entregas/4-java/ZelaBairro.postman_collection.json` importada (a variável `baseUrl` já aponta para o Render) e o repositório https://github.com/Leonardo-2112/zelabairro-api aberto no código.

---

## Vídeo 1 · Front-end (até 3:00)

**Objetivo do critério:** mostrar a aplicação funcionando e a integração com a API Java.

| Tempo | Tela | O que fazer | O que falar |
| --- | --- | --- | --- |
| 0:00–0:15 | Home | Mostrar o topo da Home | "Este é o ZelaBairro: o cidadão registra e apoia problemas de zeladoria do bairro, e a prefeitura atende pela prioridade. Front em React, Vite, TypeScript e Tailwind, publicado na Vercel e ligado à nossa API Java no Render." |
| 0:15–0:40 | Sobre, Integrantes, FAQ, Contato | Clicar rápido em cada item do menu; no FAQ abrir uma pergunta; no Contato clicar em **Enviar** vazio para aparecerem os erros | "Temos as cinco páginas institucionais. O contato valida os campos antes de enviar." |
| 0:40–0:55 | Qualquer página | Abrir o DevTools (F12) → ícone de celular → **iPhone 12 Pro (390×844)**; abrir o menu mobile; depois **iPad (768×1024)**; fechar o modo celular | "O layout se adapta ao celular, ao tablet e ao desktop, sem rolagem lateral." |
| 0:55–1:20 | `/ocorrencias` | Abrir a aba **Network** do DevTools e deixar visível; na página, filtrar **Status = Aberta** e um **Bairro** | "Esta lista vem da API Java: dá para ver aqui a chamada `GET /ocorrencias` indo para o Render. Os filtros viram parâmetros da chamada e a lista já vem ordenada pela prioridade." Fechar o DevTools. |
| 1:20–1:35 | `/cadastro` → `/login` | Criar a conta de teste e entrar | "Cadastro e login também são chamadas reais: a senha vai para a API, que guarda só o hash." |
| 1:35–2:10 | `/ocorrencias/nova` | Escolher **Buraco na via** + **Lapa** e mostrar o aviso de ocorrência parecida; depois trocar para outra categoria/bairro, digitar descrição curta e clicar em registrar para mostrar o erro; corrigir, anexar a foto e registrar | "Antes de criar, o sistema sugere apoiar uma ocorrência igual, para evitar duplicados. O formulário valida a descrição e as fotos. Ao registrar, a API devolve a ocorrência com a prioridade e a previsão de prazo." |
| 2:10–2:30 | Detalhe da ocorrência | Clicar em **Ver a ocorrência**: mostrar a foto, a previsão e o histórico. Sair e entrar com a 2ª conta de cidadão em `/ocorrencias/1` e clicar em **Apoiar** | "Esta é a rota com parâmetro, `/ocorrencias/:id`. Com outra conta eu apoio a ocorrência e a prioridade é recalculada." |
| 2:30–2:55 | `/painel` | Sair, entrar como gestora (Márcia), mostrar o resumo por bairro e mudar o status da ocorrência criada para **Em andamento** com um comentário | "O gestor vê a fila por prioridade e muda o status; a API confere se quem chamou é mesmo gestor." |
| 2:55–3:00 | Home | — | "Código no GitHub, aplicação na Vercel e API no Render: os links estão no README." |

**Dicas do vídeo 1**
- Se a previsão aparecer como "Previsão indisponível", fale: "quando o serviço de IA não responde, a ocorrência é criada mesmo assim".
- Ensaie uma vez antes de gravar: os tempos são apertados.

---

## Vídeo 2 · Java (até 5:00)

**Objetivo do critério:** "o front do grupo funcionando integrado à API e a explicação do sistema".

| Tempo | Tela | O que fazer | O que falar |
| --- | --- | --- | --- |
| 0:00–0:30 | Home do site | Mostrar a Home | "O ZelaBairro resolve um problema de zeladoria urbana. O centro do sistema é esta API REST em Java com Spring Boot: o front só conversa com ela, só ela acessa o banco Oracle e só ela chama a IA que prevê o prazo." |
| 0:30–1:15 | Diagrama (slide ou desenho simples) ou o README da API | Mostrar a arquitetura: React (Vercel) → API Java (Render, Docker) → Oracle; API → IA (Flask) | "A API foi publicada no Render com um Dockerfile multi-stage. As credenciais do banco ficam em variáveis de ambiente, nunca no código." |
| 1:15–2:00 | GitHub `zelabairro-api`, pasta `src/main/java/br/com/zelabairro` | Abrir rapidamente as pastas `model`, `dao`, `dto`, `bo`, `controller`, `handler`; abrir um DAO e mostrar o `PreparedStatement` | "A API é em camadas: model são as entidades; DAO acessa o banco com JDBC puro e PreparedStatement, sem JPA; DTO define o que entra e sai, com Bean Validation; BO guarda as regras de negócio; controller expõe os endpoints; e o handler devolve todo erro num JSON padrão." |
| 2:00–3:00 | Site (front integrado) | Entrar como cidadão, registrar uma ocorrência e abrir o detalhe; depois entrar como gestora e mudar o status | "Aqui o front usa a API de verdade: o POST de ocorrência valida os dados, calcula a prioridade e devolve 201. A mudança de status só é aceita para gestor e respeita as transições permitidas." |
| 3:00–4:10 | Postman | Rodar `GET /ocorrencias` e `GET /ocorrencias/1`; depois, na pasta **99 - Erros para a demo**, rodar nesta ordem: **"400 - cadastro inválido (lista os campos)"** (mostrar o `campos[]`), **"404 - id que não existe"**, **"409 - transição proibida ABERTA -> RESOLVIDA (RN05)"** e **"403 - mudar status sem ser gestor (RN16)"** | "Cada situação tem o status HTTP certo: 201 com Location ao criar, 400 com a lista de campos inválidos, 404 quando não existe, 409 quando uma regra de negócio é violada e 403 quando não é gestor. Nunca aparece stack trace nem SQL." |
| 4:10–4:40 | Postman ou site | Mostrar a ocorrência com `prioridade` e `pontuacaoPrioridade` no JSON | "A prioridade é calculada na hora: gravidade da categoria, apoios, dias em aberto e risco de atraso. Assim a prefeitura atende primeiro o que é mais urgente." |
| 4:40–5:00 | README da API | Mostrar a seção de links | "O código, a coleção de testes e a documentação estão no repositório e no PDF. Obrigado." |

**Dicas do vídeo 2**
- *(opcional, se sobrar tempo)* mostrar o `GET /health` respondendo e o Dockerfile.
- Se ficar longo, corte o trecho de 2:00–3:00 pela metade (só registrar a ocorrência).

---

## Depois de gravar

1. **YouTube:** *Criar → Enviar vídeo*. Título sugerido: "ZelaBairro · Front-end (GS 2026/2 · 1TDSPV)" e "ZelaBairro · API Java (GS 2026/2 · 1TDSPV)". Em **Visibilidade**, escolha **Não listado** nos dois. Na pergunta "é conteúdo para crianças?", marque **Não**.
2. Confira a duração de cada um: **até 3:00** (Front) e **até 5:00** (Java).
3. Teste os dois links numa aba anônima (sem login): precisam abrir.
4. Mande os links para o Leonardo colocar:
   - Front: README do `zelabairro-frontend` (PR → `develop` → `main`) e, se quiser, release `v1.0.2`.
   - Java: `zelabairro-api/README.md` e `gerar_documentacao.py` (gerar o PDF de novo e rodar `montar_zip.py`).
