# 1 · Artificial Intelligence & Chatbot

O projeto está em [`zelabairro-ia/`](zelabairro-ia/): dados reais do SP156, 3 notebooks executados, 2 modelos `.joblib` e a API Flask (com o chatbot como complemento).
Como rodar: [`zelabairro-ia/COMO_RODAR.txt`](zelabairro-ia/COMO_RODAR.txt). Resultados e roteiro da apresentação: [`zelabairro-ia/README.md`](zelabairro-ia/README.md).

## Checklist da entrega (PDF da GS)
- [x] Dados do treino (`data/dados_sp156.csv` + de-paras) — 10 pts
- [x] Notebooks `.ipynb` executados: EDA, treino e avaliação — 60 pts (alinhados às aulas do Prof. Alfonso em 15/11)
- [x] Modelos pré-treinados `models/modelo_prazo.joblib` e `models/modelo_atraso.joblib` — 10 pts
- [x] API REST em Flask consumindo os modelos (`app.py`, `predictor.py`) — 20 pts
- [x] `.txt` com RM, nome e turma (`identificacao.txt`)
- [x] Fonte e data de acesso na 1ª célula do notebook 01 (acesso em 15/11/2026; arquivos na versão de 10/08/2026 do portal — a data exata do download não foi registrada)
- [x] Conclusões dos 3 notebooks reescritas em linguagem simples, na voz do grupo
- [x] **Leonardo revisou as conclusões** (18/11) (divisão por integrante em [`ROTEIRO_APRESENTACAO_IA.md`](ROTEIRO_APRESENTACAO_IA.md), que não entra no zip)
- [x] Zip `ZelaBairro_IA_1TDSPV.zip` (14,5 MB) gerado em 18/11 com `cd zelabairro-ia && python scripts/empacotar.py --saida ../ZelaBairro_IA_1TDSPV.zip` e testado com `unzip -t` (fica só na pasta local)
- [ ] **Grupo:** enviar o zip no Portal até 19/11 23h55
- [x] Flask publicada no Render: https://zelabairro-ia.onrender.com (repositório https://github.com/Leonardo-2112/zelabairro-ia, sem o CSV de 63 MB) e `IA_API_URL` preenchida na API Java. Testado em 18/11: `/health`, `/prever/*`, erro 400, chatbot e ocorrência criada pela Java com prazo 16 e risco ALTO. Plano gratuito dorme após 15 min sem uso: **abra `/health` uns 2 minutos antes da demo**, senão a 1ª ocorrência nasce sem previsão (timeout de 4 s, RN12)

## Para a apresentação (23 a 27/11)
Roteiro de estudo, perguntas por notebook e divisão por integrante: [`ROTEIRO_APRESENTACAO_IA.md`](ROTEIRO_APRESENTACAO_IA.md) (uso interno).

Demo ao vivo: `GET /health`, `POST /prever/prazo` e `/prever/atraso` (Postman/Insomnia), mostrando o erro 400. A IA **não precisa** estar integrada à Java para valer nota. Explicações: [`docs/COMO_O_ZELABAIRRO_FUNCIONA.md`](../../docs/COMO_O_ZELABAIRRO_FUNCIONA.md), seção 5.
