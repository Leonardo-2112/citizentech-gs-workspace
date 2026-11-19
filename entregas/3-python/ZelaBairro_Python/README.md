# ZelaBairro Terminal

**Global Solution 2026/2 · CitizenTech · Computational Thinking Using Python · FIAP 1TDSPV**

Ferramenta de terminal para o **gestor da prefeitura** do ZelaBairro (zeladoria urbana colaborativa):
registra e apoia problemas do bairro (buraco, poste apagado, bueiro entupido...), controla o status,
calcula a **prioridade (RN10)** e os **atrasos (RN11)** e gera relatórios por bairro.
Funciona **sem internet** (dados em JSON) e, se houver conexão, sincroniza com o **Oracle** da FIAP
(as mesmas tabelas `tb_*` da API Java e do site), consulta o **ViaCEP** e pode chamar a **API de IA** do grupo.

## Integrantes
| Nome | RM |
|---|---|
| Leonardo Afonço Sousa | RM573982 |
| Syang Cristina Gomes Souza | RM569259 |
| Matheus Jones Sousa de Freitas | RM573559 |
| Vitor Gonçalves de Souza | RM569023 |
| Joao Machado Nascimento | RM572364 |

## Como executar
1. Python **3.10 ou superior** (usa `match-case`).
2. (Opcional, só para Oracle/ViaCEP/IA) instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. (Opcional, só para o Oracle/IA) copie `.env.example` para `.env` e preencha `DB_USER` e `DB_PASSWORD`
   com o seu usuário do Oracle FIAP. O `.env` **não** vai no zip nem no GitHub (está no `.gitignore`).
4. Rode:
   ```bash
   python main.py
   ```
   Sem as dependências, tudo funciona menos o menu 8 (Oracle, ViaCEP, IA), que avisa o que falta.

## Menus
```
[1] Registrar ocorrência          RN01, RN03, RN04, RN07 (sugere apoiar), RN12
[2] Apoiar ocorrência             RN08 (set: sem repetido, sem autor, só em aberto)
[3] Atualizar status              RN05 (match-case) e RN06 (data de resolução)
[4] Fila de prioridade            RN10 (selection sort) + cálculo passo a passo
[5] Relatório por bairro          abertas, atrasadas, tempo médio; salva .txt
[6] Ocorrências atrasadas         RN11
[7] Consultar ocorrências  >      [1] listar  [2] filtrar por status  [3] detalhe e histórico
[8] Integrações  >                [1] testar Oracle  [2] importar (SELECT)  [3] enviar (INSERT/UPDATE)
                                  [4] exportar JSON p/ front-end  [5] consultar CEP (ViaCEP)
[0] Sair e salvar
```

## Estrutura (5 módulos)
| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Menus, submenus e telas; laço principal (`while` + `match-case`) |
| `regras.py` | Regras de negócio RN03 a RN13 (sem entrada/saída): prioridade, status, apoio, atraso |
| `dados.py` | Persistência: JSON, relatório `.txt`, exportação para o front e sincronização com o Oracle |
| `api_externa.py` | ViaCEP e API de IA (opcionais) com `requests` |
| `util.py` | Tela do terminal, leitura validada e datas |

Pastas: `data/ocorrencias.json` (dados), `relatorios/` (`.txt`), `exports/` (JSON no formato da API).

## Integração com Oracle, front-end e APIs
- **Oracle (menu 8):** usa `tb_ocorrencia`, `tb_apoio`, `tb_atualizacao` e consulta `tb_cidadao`, `tb_categoria`,
  `tb_bairro` do Documento Base. O cidadão é cadastrado pelo **site**; o terminal liga o autor/apoiador pelo e-mail.
  Importar nunca apaga dados locais; enviar só grava status que respeitem a RN05 e pede o **e-mail de um gestor**
  cadastrado em `tb_gestor`, que fica registrado em cada atualização (RN06 e RN16). O Oracle é o mesmo do site:
  não envie dados de teste.
- **Front-end:** o menu 8 > [4] gera `exports/ocorrencias_api.json` com as mesmas chaves do `GET /ocorrencias/{id}`
  (seção 8.3 do Documento Base). Como o Oracle é o mesmo da API Java, o que for enviado aparece no site.
- **ViaCEP:** ao registrar, o CEP preenche a rua do endereço de referência.
- **API de IA:** se `IA_API_URL` estiver no `.env`, a previsão de prazo e risco de atraso é gravada na ocorrência;
  se a API não responder, a ocorrência é criada sem previsão (RN12).

## Regras da disciplina
Sem `class` (POO) e sem list comprehension; só `for`/`while`, funções, listas, tuplas, dicionários e sets.

## Limitações conhecidas (MVP)
Sem login (o e-mail identifica o cidadão); sem fotos e mapa; Oracle exige as tabelas já criadas pelo script SQL do grupo.
