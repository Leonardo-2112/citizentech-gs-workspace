# 1 · Artificial Intelligence & Chatbot

O projeto está em [`zelabairro-ia/`](zelabairro-ia/): dados reais do SP156, 3 notebooks executados, 2 modelos `.joblib` e a API Flask (com o chatbot como complemento).
Como rodar: [`zelabairro-ia/COMO_RODAR.txt`](zelabairro-ia/COMO_RODAR.txt). Resultados e roteiro da apresentação: [`zelabairro-ia/README.md`](zelabairro-ia/README.md).

## Checklist da entrega (PDF da GS)
- [x] Dados do treino (`data/dados_sp156.csv` + de-paras) — 10 pts
- [x] Notebooks `.ipynb` executados: EDA, treino e avaliação — 60 pts (alinhados às aulas do Prof. Alfonso em 15/11)
- [x] Modelos pré-treinados `models/modelo_prazo.joblib` e `models/modelo_atraso.joblib` — 10 pts
- [x] API REST em Flask consumindo os modelos (`app.py`, `predictor.py`) — 20 pts
- [x] `.txt` com RM, nome e turma (`identificacao.txt`)
- [ ] Preencher `DATA_DOWNLOAD` na 1ª célula do notebook 01
- [ ] Reescrever as conclusões dos 3 notebooks **com as palavras do grupo** (cada uma tem um aviso escondido `<!-- RASCUNHO -->`)
- [ ] Gerar o zip: `cd zelabairro-ia && python scripts/empacotar.py` (sai em `../zelabairro-ia.zip`, fora do git) e conferir que abre
- [ ] (Opcional) Publicar a Flask no Render para a Java chamar (Documento Base 7.4)

## Para a apresentação (23 a 27/11)
Demo ao vivo: `GET /health`, `POST /prever/prazo` e `/prever/atraso` (Postman/Insomnia), mostrando o erro 400. A IA **não precisa** estar integrada à Java para valer nota. Explicações: [`docs/COMO_O_ZELABAIRRO_FUNCIONA.md`](../../docs/COMO_O_ZELABAIRRO_FUNCIONA.md), seção 5.
