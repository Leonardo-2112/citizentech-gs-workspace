# Entregas da Global Solution 2026/2 — ZelaBairro

Uma pasta por matéria, **na ordem de dependência** da seção 12.1 do Documento Base (quem depende de outra vem depois dela).
Antes de mexer em qualquer pasta, leia [`docs/COMO_O_ZELABAIRRO_FUNCIONA.md`](../docs/COMO_O_ZELABAIRRO_FUNCIONA.md) e a seção da matéria em [`docs/PLANO_DE_DESENVOLVIMENTO.md`](../docs/PLANO_DE_DESENVOLVIMENTO.md).

| Pasta | Matéria | Depende de | O que vai para o Portal | Situação (15/11) |
|---|---|---|---|---|
| [1-ia-chatbot](1-ia-chatbot/) | Artificial Intelligence & Chatbot | Só dos dados do SP156 | `.zip` com dados, notebooks, `.joblib`, API Flask e `.txt` | Pronta; faltam data de download e conclusões com as palavras do grupo |
| [2-banco-de-dados](2-banco-de-dados/) | Building Relational Database | Nada | `.zip` com PDF e `.sql` (capa com nomes, RM e turma) | A fazer — **primeiro do caminho crítico** |
| [3-python](3-python/) | Computational Thinking Using Python | Nada | `.zip` com `.py`, PDF e `.txt` | A fazer |
| [4-java](4-java/) | Domain Driven Design Using Java | Banco (obrigatório); IA (opcional) | `.zip` com projeto (sem `target/`), Dockerfile, `.sql`, PDF e README | A fazer |
| [5-front-end](5-front-end/) | Front-End Design Engineering | API Java publicada | `.zip` (até 50 MB, sem `node_modules`) + repositório **público** | A fazer |
| [6-engenharia-de-software](6-engenharia-de-software/) | Software Engineering and Business Model | Produto pronto | **Um único PDF** com links do backlog e do pitch | A fazer (parte pode começar já) |

## Regras que valem para todas as pastas
- **Prazo:** 19/11/2026 até 23h55 no Portal do Aluno, sem prorrogação (meta interna: meio da tarde).
- **Identificação:** um `.txt` com RM, nome completo e turma em **cada** `.zip` (modelo em [`1-ia-chatbot/zelabairro-ia/identificacao.txt`](1-ia-chatbot/zelabairro-ia/identificacao.txt)).
- **Nunca** versionar senha, `.env`, `node_modules/`, `target/` nem os `.zip` gerados (já estão no `.gitignore` desta pasta).
- Nomes de tabelas, rotas, campos e regras: **exatamente** os do Documento Base v1.3.
- Registrem o uso de IA desde já (vale 10 pontos em Eng. Software).
- Critérios oficiais de cada matéria: [`docs/CRITERIOS_DE_ACEITE.md`](../docs/CRITERIOS_DE_ACEITE.md).
