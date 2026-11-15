# Aulas de AI & Chatbot (Prof. Alfonso Rodriguez) — resumo técnico

Materiais lidos em 15/11/2026: Aula 02 (Ciência de Dados e Estatística), Aula 04 (Dataviz), Aula 05 (Aprendizado de Máquina), Aula 06 (Classificação e Pré-Checkpoint), Exercício de Regressão Linear e enunciado do Checkpoint 3.
Objetivo: alinhar o projeto de IA do ZelaBairro (`zelabairro-ia`) ao que foi ensinado, para que **todos consigam explicar** cada linha na apresentação (10 pts de "todos respondem").

## 1. Conteúdo coberto em aula

| Tema | O que o professor ensinou | Aula |
|---|---|---|
| Ciclo de um projeto | Coleta → limpeza/normalização (≈ 80% do tempo) → EDA → modelagem → interpretação; pipeline Ingestão → Preparação → Treino → Avaliação → Implantação | 02 |
| Estatística | Média, mediana, moda, médias geométrica/harmônica/ponderada, variância e desvio padrão (amostral × populacional), quartis (Q1, Q2, Q3), correlação. Bibliotecas `statistics`, NumPy, Pandas | 02 |
| Mediana × média | Exemplo de **tempo de entrega**: lista com alguns valores enormes (30, 42, 45 dias) → **mediana 4,5 dias, média 10 dias**. A média é puxada pelos extremos | 02 |
| Dataviz | Hierarquia de Cleveland e McGill (posição > comprimento > cor), taxonomia de Abela (comparação, distribuição, composição, relação), tipos de variável (nominal, ordinal, discreta, contínua), framework de 3 passos (pergunta de negócio → variáveis → gráfico), tratamento de outliers (remoção, winsorização, destaque, zoom). **Sem pizza, sem 3D, sem enfeite**; versão "profissional" = barras 2D neutras com destaque só no que importa. Biblioteca: **Plotly Express** (`px.bar`, `px.line`, `px.box`, `px.histogram`, `px.scatter`…) | 04 |
| ML: conceitos | Supervisionado × não supervisionado (K-Means), inferência, overfitting (desconfiar de 100% de acurácia), "entrada ruim → saída ruim" | 05 |
| Otimização | Engenharia de atributos, **GridSearchCV** (ex.: `max_depth`), **Random Forest / XGBoost** quando o modelo simples estagna, foco no **recall** em base desbalanceada, **validação cruzada K-Fold** | 05 |
| Classificação | Árvore de Decisão (nó raiz, nós de decisão, folhas; limitar `max_depth` / `min_samples_leaf` contra overfitting), Regressão Logística com **MinMaxScaler**, trade-off **acurácia × interpretabilidade** (Random Forest = alta acurácia, "caixa preta"; árvore e regressão linear = interpretáveis) | 06 |
| Métricas de classificação | Matriz de confusão, acurácia (só em base equilibrada), precisão (custo do falso positivo), **recall** (custo do falso negativo), **F1** (recomendado em base desbalanceada), **curva ROC e AUC** com `predict_proba(X_teste)[:, 1]` | 06 |
| Regressão | `LinearRegression`, `r2_score`, `mean_absolute_error`, leitura de `intercept_` e `coef_` ("cada quarto adiciona R$ X") | Exercício |
| Arquitetura | Papel de **Flask**, **Pickle** e **Node-RED** em produção (pergunta 10 do CP3) | CP3 |

## 2. Estilo de código do professor

- Ambiente: Google Colab / Jupyter, `display(dados.head())`.
- Nomes em português: `dados`, `X`, `y`, `X_treino`, `X_teste`, `y_treino`, `y_teste`, `modelo`, `previsoes`, `acuracia`.
- Sempre `train_test_split(X, y, test_size=0.2, random_state=42)` (80/20, semente 42).
- Passos numerados em comentário (`# Passo 1: Ingestão e Leitura dos Dados`, `# 1. ...`, `# 2. ...`) e um comentário explicando cada linha importante.
- Saída com f-string e porcentagem: `print(f"Acurácia do modelo: {acuracia * 100:.2f}%")`.
- Fecha com uma previsão de exemplo ("novas medidas") e com uma **interpretação de negócio** do resultado.
- No exercício da Aula 06, exige **código + saída + interpretação**; resposta sem evidência no notebook vale zero.
- Regra de IA do professor (CP3): pode consultar IA, mas **as respostas devem ser com as próprias palavras**; copiar e colar resposta de IA tira pontos.

## 3. Projeto atual × aulas

> **Aplicado em 15/11/2026** na pasta `entregas/1-ia-chatbot/zelabairro-ia/`: notebooks regenerados e executados com Árvore de Decisão, Regressão Linear/Logística, curva ROC, estatística do IQR e gráficos no padrão da Aula 04; Ridge e curva de calibração removidos; chatbot sem porcentagem. Resultados no README do projeto (seção 3.2). A tabela abaixo é a análise que motivou os ajustes.

| No `zelabairro-ia` hoje | Visto em aula? | Recomendação |
|---|---|---|
| `train_test_split` 80/20, `random_state=42` | ✅ igual | Manter |
| `RandomForestRegressor` / `RandomForestClassifier` | ✅ (Aula 05: "migrar para Random Forest quando o simples estagna"; Aula 06: trade-off) | Manter, **mas mostrar antes uma Árvore de Decisão** (e Regressão Linear / Logística) e contar a história da aula: começamos pelo interpretável, comparamos, e migramos para a floresta porque ela errou menos |
| `GridSearchCV` (`max_depth`, `min_samples_leaf`) | ✅ (Aulas 05 e 06) | Manter |
| Validação cruzada 5 folds | ✅ (Aula 05, K-Fold) | Manter |
| Matriz de confusão, precisão, recall, F1, ROC AUC | ✅ (Aula 06, mesmas funções) | Manter; acrescentar o **gráfico da curva ROC** com `roc_curve`, como no slide |
| MAE, RMSE, R² | ✅ MAE e R² (exercício); RMSE é a raiz do erro quadrático | Manter |
| `class_weight="balanced"` | ⚠️ conceito visto (base desbalanceada, foco no recall), parâmetro não | Manter e explicar em uma frase: "a base tem 70% no prazo e 30% atrasados; o balanceamento dá mais peso aos atrasos para aumentar o recall, como a aula recomenda quando o falso negativo é caro" |
| Alvo em `log(1 + dias)` (`TransformedTargetRegressor`) | ⚠️ conceito visto (mediana × média, outliers), técnica não | Manter e explicar com o exemplo da Aula 02: "o tempo tem outliers (chamados de 1.668 dias); a média é puxada, como no exemplo média 10 × mediana 4,5; o log diminui o peso desses extremos e o modelo passa a prever o tempo típico". Sem o log, a floresta erra mais que a simples mediana |
| `OneHotEncoder` + `ColumnTransformer` + `Pipeline` | ❌ | Manter (as entradas são texto: categoria e subprefeitura; o modelo só entende números), explicando como "transformar cada categoria em colunas 0/1". O `Pipeline` é o mesmo conceito de "esteira" da Aula 02 |
| `MinMaxScaler` | ✅ visto | Não se aplica: todas as entradas são categóricas (viram 0/1, que já estão entre 0 e 1). Dizer isso se perguntarem |
| Curva de calibração e tabela de limiares | ❌ | **Simplificar:** manter só a tabela de limiares (é a mesma ideia da curva ROC) e tirar a curva de calibração, deixando uma frase sobre a probabilidade inflada |
| Teste "no tempo" (treino 2020–2022, teste 2023) | ⚠️ parente da validação | Manter: é o que justifica tirar o mês do modelo |
| `DummyRegressor` / `DummyClassifier` (baseline) | ❌ nome, ✅ ideia (Aula 05: modelo que "chuta" e tem 90% de acurácia) | Manter, chamando de "modelo que chuta" como na aula |
| `Ridge` | ❌ | **Trocar por `LinearRegression`**, que é a da aula |
| Gráficos em matplotlib | ⚠️ aula usa Plotly Express | Revisar os gráficos do notebook 01 pelo framework de 3 passos: título com a pergunta de negócio, barras horizontais neutras com destaque, boxplot para outliers, sem pizza/3D. Trocar para Plotly é opcional |
| Estatística descritiva no EDA | ✅ parcial (`describe`, mediana, quantis) | Acrescentar média × mediana × desvio padrão do tempo de resolução, quartis e IQR, e um boxplot, com a interpretação |
| `joblib` | ✅ equivalente ao Pickle (o PDF da GS aceita os dois) | Manter; dizer que é o "pickle otimizado" do scikit-learn |
| Flask | ✅ (arquitetura do CP3) | Manter |
| Chatbot com regras (palavras-chave) | ❌ (Node-RED citado só na arquitetura) | Opcional: não vale ponto na GS. Decidir se fica |

## 4. Resumo para a apresentação

"Seguimos o ciclo da aula: coletamos dados reais do SP156, limpamos (de-para de categorias, distrito → subprefeitura, só chamados finalizados), fizemos a estatística e os gráficos da EDA, treinamos primeiro modelos interpretáveis (Árvore de Decisão, Regressão Linear/Logística) e depois o Random Forest, ajustamos com GridSearchCV, conferimos com validação cruzada e avaliamos com as métricas certas: MAE e R² para o prazo; matriz de confusão, recall, F1 e curva ROC para o atraso, porque a base é desbalanceada e não avisar um atraso é o erro mais caro. Exportamos com joblib e servimos com Flask."
