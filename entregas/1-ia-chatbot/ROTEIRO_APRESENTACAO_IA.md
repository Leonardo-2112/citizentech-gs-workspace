# Roteiro de estudo e apresentação — IA & Chatbot

> **Uso interno do grupo. NÃO entra na entrega:** este arquivo fica fora da pasta `zelabairro-ia/`, então o `empacotar.py` não o coloca no `.zip`.
> Objetivo: cada integrante conseguir explicar as conclusões dos notebooks com as próprias palavras e responder qualquer pergunta do professor (10 pts de "todos respondem").

## 1. Divisão sugerida por integrante

A apresentação vale 100 pontos (30% da nota). Sugestão de divisão pelos critérios oficiais (troquem à vontade):

| Integrante | Parte da apresentação | Pts | Revisa a conclusão de | Base |
|---|---|---|---|---|
| Leonardo Afonço Sousa | Problema CitizenTech e como a IA ajuda | 15 | (coordena a revisão das três) | `docs/COMO_O_ZELABAIRRO_FUNCIONA.md`, seções 1 e 5 |
| Syang Cristina Gomes Souza | Dados e análise exploratória: origem, tratamento e insights | 15 | Notebook 01 | `notebooks/01_eda.ipynb` |
| Matheus Jones Sousa de Freitas | Escolha dos modelos e justificativa | 20 | Notebook 02 | `notebooks/02_modelo_prazo.ipynb` |
| Vitor Goncalves de Souza | Métricas e interpretação dos resultados | 20 | Notebook 03 | `notebooks/03_modelo_atraso.ipynb` |
| Joao Machado Nascimento | Demonstração ao vivo da API Flask | 20 | — | `zelabairro-ia/README.md`, seção 7 |
| **Todos** | Perguntas do professor | 10 | — | Seção 3 deste roteiro |

**Como revisar a conclusão:** leia a célula de conclusões do seu notebook, confira cada número na saída das células acima dela e reescreva o que não soar como você falaria. Depois, explique em voz alta para outra pessoa do grupo, sem ler.

## 2. Roteiro de perguntas por notebook (com as respostas para conferir)

### Notebook 01 — Análise exploratória
| Pergunta | Onde achar | Resposta para conferir |
|---|---|---|
| De onde vêm os dados e de quando? | 1ª célula | SP156 (SMIT, Portal de Dados Abertos de SP), chamados de jan/2020 a set/2023, acesso em 15/11/2026 |
| Por que só 2020–2023? | Seção 2 | Antes de 2020 a data de fim era a "Data do Parecer", que cai no mesmo dia da abertura em 73–100% dos casos |
| Quantos chamados e categorias? | Seção 1 e 3 | 982.475 chamados, 7 das 8 categorias (Iluminação não tem dados), 32 subprefeituras |
| Média ou mediana: qual representa melhor o tempo? | Estatística descritiva | Mediana (7 dias); a média (28,6) é puxada pelos outliers, como no exemplo de tempo de entrega da Aula 02 |
| Como identificamos outliers? | Estatística descritiva | Regra do IQR: acima de Q3 + 1,5 × IQR = 58 dias → 13,6% dos chamados |
| Qual categoria mais atrasa? | Seção 5 | Sinalização (61,3%); a que menos atrasa é Descarte (2,9%) |
| Por que barras horizontais e não pizza? | Seção 3 (texto do framework) | Aula 04: comparação entre categorias → barras; comprimento é mais preciso que área; nomes longos ficam legíveis |

### Notebook 02 — Prazo (regressão)
| Pergunta | Onde achar | Resposta para conferir |
|---|---|---|
| Por que regressão? | Cabeçalho | O alvo é um número (dias) |
| Qual a ordem dos modelos e por quê? | Seção 2 | Aula 05/06: chute → interpretáveis (Linear, Árvore) → Random Forest |
| Qual o MAE de cada um? | Tabela da seção 2 | Linear 30,2; Árvore 28,4 (brutos) e 23,9 (log); tabela de medianas 24,5; Random Forest 23,3 |
| Por que treinar em log(1 + dias)? | Texto da seção 2 | Para reduzir o peso dos outliers e prever o tempo típico |
| O modelo ganhou do baseline? | Seção 4 | Sim, por 1,1 dia (23,3 × 24,5) |
| Por que o R² é tão baixo (0,058)? | Conclusões | Alguns chamados levam centenas de dias e as 4 entradas não explicam o motivo |
| Por que o mês ficou de fora? | Teste no tempo | Treinando em 2020–2022 e testando em 2023, o mês piora (38,2 × 37,8) |
| Como a árvore "pensa"? | Desenho da árvore | Regras se/então: primeiro pergunta se é Descarte, depois se é Poda etc. |

### Notebook 03 — Atraso (classificação)
| Pergunta | Onde achar | Resposta para conferir |
|---|---|---|
| Por que classificação? | Cabeçalho | O alvo é sim/não (atrasou ou não) |
| Por que a acurácia engana? | Seção 1 e 2 | 70% não atrasam; quem chuta sempre "no prazo" acerta 70% (Aula 05) |
| Por que F1 e recall? | Seção 1 | Aula 06: F1 para base desbalanceada; recall quando o falso negativo é caro |
| Qual foi o melhor modelo? | Tabela da seção 2 | Random Forest sem mês (F1 0,561, AUC 0,759) |
| O que a matriz de confusão mostra? | Seção 4 | 48.841 atrasos detectados, 9.710 não detectados, 67.199 alarmes falsos |
| O que é a curva ROC? | Curva ROC | Acertos × alarmes falsos em todos os limiares; AUC 0,5 = chute, 1 = perfeito |
| Por que limiar 0,5? | Tabela de limiares | Equilíbrio: acima disso o recall despenca (0,438 em 0,6) |
| Por que o site não mostra porcentagem? | Célula da probabilidade média | Média prevista 46,2% × real 29,8%: a probabilidade está inflada pelo balanceamento |

## 3. Perguntas que qualquer um pode receber
1. A IA acessa o banco de dados? → Não. Ela recebe 4 informações e devolve a previsão; quem grava é a API Java.
2. O que são os arquivos `.joblib`? → Os modelos treinados salvos (equivalente ao Pickle da aula), que a API Flask carrega para prever.
3. O que acontece se a IA cair? → A ocorrência é criada sem previsão (RN12).
4. Qual é a diferença entre regressão e classificação no projeto? → Prazo é número (regressão); atraso é sim/não (classificação).
5. O que é overfitting e como evitamos? → Decorar o treino; limitamos a árvore (`max_depth`, `min_samples_leaf`), separamos teste e usamos validação cruzada.
6. Por que Random Forest e não só a árvore? → Errou menos; o custo é ser menos interpretável (trade-off da Aula 06).
7. Por que 80/20 e `random_state=42`? → Teste com dados nunca vistos e resultado reproduzível, como nas aulas.
8. Qual a maior limitação? → Poucas informações na abertura do chamado; dados até 2023 e com a pandemia.

## 4. Roteiro da demo (Joao)
1. `GET /health` → `{"status": "ok"}`.
2. `POST /prever/prazo` com Buraco na via / Lapa / mês 11 / dia 2 → 16 dias.
3. `POST /prever/atraso` com o mesmo corpo → risco S.
4. Mesma chamada com categoria "Buraco" → erro 400 com a mensagem.
5. (Se der tempo) abrir o chatbot em `/` e registrar um problema.
Abra a API alguns minutos antes se ela estiver no Render (o plano gratuito "dorme").
