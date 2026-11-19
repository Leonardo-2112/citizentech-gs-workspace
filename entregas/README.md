# Entregas da Global Solution 2026/2 — ZelaBairro

Uma pasta por matéria, **na ordem de dependência** da seção 12.1 do Documento Base (quem depende de outra vem depois dela).

> **Papel deste repositório (combinado em 15/11):** aqui o grupo **desenvolve e organiza** o projeto e as ideias. Ele **não é** o entregável.
> * Matérias que pedem repositório próprio: o código final vai para **um repositório separado da matéria** (tabela abaixo).
> * Matérias que não pedem repositório: o entregável é o **`.zip` (ou PDF) enviado direto no Portal do Aluno**, gerado a partir desta pasta.
Antes de mexer em qualquer pasta, leia [`docs/COMO_O_ZELABAIRRO_FUNCIONA.md`](../docs/COMO_O_ZELABAIRRO_FUNCIONA.md) e a seção da matéria em [`docs/PLANO_DE_DESENVOLVIMENTO.md`](../docs/PLANO_DE_DESENVOLVIMENTO.md).

| Pasta | Matéria | Depende de | O que vai para o Portal | Repositório próprio? | Situação (18/11) |
|---|---|---|---|---|---|
| [1-ia-chatbot](1-ia-chatbot/) | Artificial Intelligence & Chatbot | Só dos dados do SP156 | `.zip` com dados, notebooks, `.joblib`, API Flask e `.txt` | Não exigido. Só se publicarem a Flask no Render (opcional): repositório da IA | **Pronta.** Zip `ZelaBairro_IA_1TDSPV.zip` gerado; falta enviar no Portal |
| [2-banco-de-dados](2-banco-de-dados/) | Building Relational Database | Nada | `.zip` com PDF e `.sql` (capa com nomes, RM e turma) | Não: só o `.zip` no Portal | **Pronta.** Zip `ZelaBairro_BD_1TDSPV.zip` gerado; falta enviar no Portal |
| [3-python](3-python/) | Computational Thinking Using Python | Nada | `.zip` com `.py`, PDF e `.txt` | Não: só o `.zip` no Portal | Zip `ZelaBairro_Python_1TDSPV.zip` corrigido (ver `AVALIACAO_PYTHON.md`); ajustes finais pendentes |
| [4-java](4-java/) | Domain Driven Design Using Java | Banco (obrigatório); IA (opcional) | `.zip` com projeto (sem `target/`), Dockerfile, `.sql`, PDF e README | Sim, na prática: o deploy no Render (obrigatório) puxa de um repositório GitHub (pode ser privado). O Portal recebe o `.zip` | API no Render; falta o vídeo de 5 min, o link no PDF/README e refazer o zip |
| [5-front-end](5-front-end/) | Front-End Design Engineering | API Java publicada | `.zip` (até 50 MB, sem `node_modules`) + repositório **público** | **Sim, obrigatório e público**, com 5 commits por integrante (deploy na Vercel). O Portal recebe o `.zip` | **Pronta.** Repositório público, Vercel, vídeo e zip `ZelaBairro_Front_1TDSPV.zip`; falta enviar no Portal |
| [6-engenharia-de-software](6-engenharia-de-software/) | Software Engineering and Business Model | Produto pronto | **Um único PDF** com links do backlog e do pitch | Não: só o PDF no Portal (backlog no Jira/Trello) | PDF montado com o link do Jira; falta o vídeo pitch e o link dele no PDF |

## Regras que valem para todas as pastas
- **Prazo:** 19/11/2026 até 23h55 no Portal do Aluno, sem prorrogação (meta interna: meio da tarde).
- **Identificação:** um `.txt` com RM, nome completo e turma em **cada** `.zip` (modelo em [`1-ia-chatbot/zelabairro-ia/identificacao.txt`](1-ia-chatbot/zelabairro-ia/identificacao.txt)).
- **Nunca** versionar senha, `.env`, `node_modules/`, `target/` nem os `.zip` gerados (já estão no `.gitignore` desta pasta).
- Nomes de tabelas, rotas, campos e regras: **exatamente** os do Documento Base v1.5.
- Registrem o uso de IA desde já (vale 10 pontos em Eng. Software).
- Critérios oficiais de cada matéria: [`docs/CRITERIOS_DE_ACEITE.md`](../docs/CRITERIOS_DE_ACEITE.md).
