# Como o ZelaBairro funciona — guia para o grupo

> Explicação em linguagem simples, para todo mundo do grupo conseguir explicar o projeto inteiro em qualquer apresentação.
> A regra oficial está no **Documento Base v1.4** (`docs/ZelaBairro-Documento-Base.pdf`); este guia só explica. Se discordarem, vale o Documento Base.

---

## 1. Em uma frase

**O cidadão registra (com fotos) e apoia problemas de zeladoria do bairro; a prefeitura recebe tudo numa fila por prioridade, com prazo e risco de atraso previstos por uma IA treinada com quase 1 milhão de chamados reais de São Paulo.**

## 2. As peças e quem fala com quem

```
 Cidadão / Gestor (navegador)
        │
        ▼
 FRONT-END (React + Vite + TS + Tailwind, na Vercel)
        │  HTTP + JSON (fetch)            ← o front SÓ conversa com a API Java
        ▼
 API JAVA (Spring Boot + JDBC, Docker no Render)
        │                    │
        │ JDBC               │ HTTP (só ao criar uma ocorrência)
        ▼                    ▼
 ORACLE FIAP            API DE IA (Flask, no Render)
 9 tabelas              2 modelos .joblib
 (guarda tudo,          (não acessa banco nem Java:
  inclusive a previsão   recebe 4 dados e devolve
  e as fotos)            prazo e risco)

 APP PYTHON (terminal)  → independente, sem internet, dados em JSON (ferramenta de triagem do gestor)
```

Três frases para decorar:
1. **O front só conhece a Java.**
2. **A Java é a única que fala com o banco e com a IA.**
3. **A IA é uma calculadora: não guarda nada, só responde.**

## 3. A jornada do cidadão

| Passo | O que ele faz | O que acontece por trás |
|---|---|---|
| 1. Cadastro | Informa nome, e-mail, senha e (opcional) telefone em `/cadastro` | A Java grava em `tb_cidadao` com a senha transformada em **hash BCrypt** (RN15). E-mail repetido → erro 409 (RN02) |
| 2. Login | E-mail e senha em `/login` | A Java confere o hash e devolve `{id, nome, perfil: "CIDADAO"}`. O front guarda isso no navegador |
| 3. Escolhe o problema | Categoria (ex.: Buraco na via) e bairro (ex.: Lapa) em `/ocorrencias/nova` | O site mostra ocorrências **abertas iguais** no mesmo bairro e sugere **apoiar** em vez de duplicar (RN07) |
| 4. Descreve | Descrição (10 a 500 caracteres) e endereço de referência (até 200) | Validação no front e na Java (RN03) |
| 5. Envia | Clica em Registrar | A Java grava a ocorrência como **ABERTA**, chama a IA e grava a previsão junto (seção 5 deste guia) |
| 6. Fotos (opcional) | Anexa até 3 fotos JPG/PNG de até 2 MB | Cada foto vai para `tb_foto`, dentro do Oracle (RN18) |
| 7. Confirmação | Vê: *"Ocorrência nº 15 registrada. Previsão: cerca de 16 dias. Risco de atraso: alto (estimativa)."* | Se a IA estiver fora do ar: *"previsão indisponível"*, e a ocorrência é criada assim mesmo (RN12) |
| 8. Acompanha | Abre `/ocorrencias/15` | Vê status, previsão, histórico de atualizações, fotos e quantos apoios a ocorrência tem |
| 9. Apoia outros | Clica em **Apoiar** numa ocorrência de outra pessoa | `tb_apoio`; um apoio por pessoa, não pode apoiar a própria, só ABERTA ou EM_ANDAMENTO (RN08) |

Privacidade: listas públicas mostram só o **primeiro nome** do autor, nunca e-mail ou telefone (RN13). Não guardamos CPF nem endereço do cidadão (LGPD).

## 4. A jornada do gestor da prefeitura

| O que ele faz | Como funciona |
|---|---|
| Login | Mesmo `/login`. Como o e-mail está em `tb_gestor`, a resposta vem com `perfil: "GESTOR"` e o menu **Painel** aparece |
| Vê a fila | `/painel` lista as ocorrências da maior para a menor **prioridade** (seção 7 deste guia) |
| Muda o status | Registra uma atualização com comentário. Transições permitidas (RN05): ABERTA → EM_ANDAMENTO → RESOLVIDA; ABERTA ou EM_ANDAMENTO → CANCELADA. Fica no histórico, com o nome do gestor (RN06) |
| Cadastra outro gestor | Formulário no painel. Fica registrado quem cadastrou (RN17). O primeiro gestor vem do seed do banco |
| Vê o resumo por bairro | Abertas, atrasadas e tempo médio por bairro: mostra a desigualdade entre regiões (ODS 10) |

**Quem garante que só gestor entra?** A Java. Nas rotas de gestor o front envia o cabeçalho `X-Gestor-Id`, e a Java procura esse id em `tb_gestor` **a cada requisição**. Se não achar, responde **403** (RN16). Esconder o botão no front é só conforto; a trava é no banco.

## 5. A IA, explicada

### 5.1 O que ela aprendeu
- **Dados:** 982.475 chamados reais do **SP156** (canal oficial de reclamações de São Paulo), de 2020 a 2023, nas nossas categorias.
- Cada chamado tem tipo, subprefeitura, data de abertura e data de finalização. Da diferença entre as datas sai **quantos dias ele levou**.

### 5.2 As duas previsões
| Modelo | Pergunta | Tipo (aula) | Exemplo |
|---|---|---|---|
| **M1 – Prazo** | Em quantos dias isso costuma ser resolvido? | **Regressão** (prevê um número) | 16 dias |
| **M2 – Atraso** | Vai passar do prazo de referência da categoria? | **Classificação** (prevê S ou N) | Risco: S |

Entradas (só o que se sabe no momento do registro): **categoria, subprefeitura, mês e dia da semana**. A IA **não lê a descrição nem olha as fotos**.

### 5.3 Como a previsão chega ao cidadão
```
1. Cidadão clica em Registrar  →  front faz POST /ocorrencias para a Java
2. Java valida e pergunta à IA: {"categoria": "Buraco na via", "subprefeitura": "Lapa", "mes": 11, "dia_semana": 2}
3. IA responde: prazo 16 dias; risco S
4. Java grava tudo no Oracle (nr_prazo_previsto = 16, fl_risco_atraso = 'S')
5. Java devolve a ocorrência ao front já com "prazoPrevistoDias": 16 e "riscoAtraso": "S"
6. Site mostra a confirmação; depois, qualquer tela que buscar a ocorrência já recebe a previsão do banco
```
A previsão também **mexe na fila**: risco S soma **+15 pontos** na prioridade (RN10). Um problema com tendência a atrasar sobe **antes** de atrasar. Esse é o valor da IA para a prefeitura.

### 5.4 Quanto ela acerta (diga com honestidade)
- **Prazo:** erra em média **23 dias** (MAE). A tabela simples "mediana de cada categoria" erra 24,5. Ganha, mas por pouco.
- **Atraso:** pega **83% dos casos que realmente atrasam** (recall). De cada 100 avisos de risco, 42 se confirmam (precisão). Escolhemos assim porque **não avisar um atraso** (falso negativo) é o erro mais caro; um alarme a mais só sobe a ocorrência um pouco na fila.
- **Limitações:** dados até 2023 e com a pandemia; o "prazo" do SP156 é até o órgão **fechar o protocolo**, não necessariamente o conserto; "Iluminação pública apagada" não tem dados (sem previsão).

### 5.5 A IA precisa estar ligada à Java para valer nota?
**Não.** A matéria de IA avalia dados, notebooks, modelos `.joblib` e a API Flask funcionando. Na apresentação de IA, chamem a Flask direto (Postman/Insomnia). A ligação com a Java é **desejável**; sem ela vale a RN12.

## 6. Login, explicado em 4 frases
1. No cadastro, a Java guarda a senha como **hash BCrypt** (uma "impressão digital" da senha que não dá para desfazer), nunca a senha.
2. No login, a Java procura o e-mail em `tb_gestor` e depois em `tb_cidadao` e compara a senha com o hash; acertou → devolve id, nome e perfil; errou → **401** "e-mail ou senha inválidos".
3. O front guarda `{id, nome, perfil}` e envia o id no cabeçalho (`X-Gestor-Id` nas rotas de gestor, `X-Cidadao-Id` nas fotos).
4. **Limitação que assumimos:** sem token, quem souber um id consegue forjar o cabeçalho. Para o MVP é aceitável; a próxima etapa é **JWT**.

Por que cidadão e gestor em **tabelas separadas**? São papéis diferentes do domínio (o gestor pertence a um órgão e sabe quem o cadastrou) e o PDF de Java critica "CRUD genérico de usuário".

## 7. Prioridade (RN10), com exemplo
```
pontos = gravidade da categoria × 10
       + mínimo(apoios, 20) × 2
       + mínimo(dias em aberto, 30)
       + 15 se a IA previu risco S OU a ocorrência já está atrasada
ALTA ≥ 70 · MÉDIA 40 a 69 · BAIXA < 40
```
Árvore com risco de queda (gravidade 5), 3 apoios, 2 dias, risco S → 50 + 6 + 2 + 15 = **73 → ALTA**.
Buraco (gravidade 4), sem apoios, 5 dias, sem risco → 40 + 0 + 5 = **45 → MÉDIA**.

## 8. Fotos, explicado
- Ficam no **próprio Oracle**, na tabela `tb_foto` (coluna BLOB `bl_imagem`). Motivos: não precisa de conta em serviço externo, o disco do Render apaga arquivos ao reiniciar, e é o mesmo JDBC (`setBytes` / `getBytes`).
- Regras (RN18): só o autor, só enquanto ABERTA, até 3 fotos, JPG/PNG até 2 MB.
- O front envia com `fetch` + `FormData` (continua sendo Fetch API) e mostra com `<img src=".../fotos/3">`.
- Se faltar tempo, é a **última funcionalidade a entrar**: o resto funciona sem foto.

## 9. As 9 tabelas e para que serve cada uma
| Tabela | Guarda | Ligações |
|---|---|---|
| `tb_orgao` | Órgãos que executam o serviço (Zeladoria, Iluminação…) | 1:N categorias, 1:N gestores |
| `tb_categoria` | Tipos de problema, prazo de referência e gravidade | 1:N ocorrências |
| `tb_bairro` | Bairros e sua subprefeitura (mesmo nome usado pela IA) | 1:N ocorrências |
| `tb_cidadao` | Quem registra e apoia (com hash da senha) | 1:N ocorrências; N:N com ocorrências via apoio |
| `tb_gestor` | Servidores que acessam o painel; órgão e quem cadastrou | 1:N atualizações; autorrelacionamento |
| `tb_ocorrencia` | O problema registrado, status, datas e **previsão da IA** | 1:N atualizações, 1:N fotos |
| `tb_atualizacao` | Histórico de mudanças de status, com o gestor | — |
| `tb_apoio` | Associativa do N:N cidadão ↔ ocorrência | — |
| `tb_foto` | Imagens do problema (BLOB) | — |

## 10. Os outros dois canais
- **App Python (terminal):** ferramenta de triagem para o gestor que funciona **sem internet** (dados em JSON). Tem as mesmas regras (RN04, RN05, RN07, RN08, RN10, RN11). Atende o "continuar útil fora do cenário ideal de conectividade" do PDF da GS.
- **Chatbot (opcional):** complemento da matéria de IA. Conversa com o cidadão, sugere apoio, mostra a previsão e manda concluir no site. Não grava nada e não vale ponto na GS.

## 11. Perguntas prováveis dos professores (e respostas curtas)

| Matéria | Pergunta | Resposta curta |
|---|---|---|
| IA | Por que regressão e classificação? | O prazo é um número (regressão); o atraso é sim/não (classificação) |
| IA | Por que Random Forest? | Comparamos primeiro com modelos interpretáveis (como na aula); a floresta errou menos. Custo: é mais "caixa preta" |
| IA | Por que o recall importa mais aqui? | Base desbalanceada (70% no prazo) e não avisar um atraso é o erro mais caro |
| IA | A IA acessa o banco? | Não. Ela recebe 4 dados da Java e devolve a previsão; a Java grava |
| IA | E se a IA cair? | A ocorrência é criada sem previsão (RN12) |
| Banco | Por que tabela separada de gestor? | Papel diferente, dados diferentes (órgão, quem cadastrou), sem "tabela genérica de usuário" |
| Banco | Onde fica a foto? | BLOB em `tb_foto`, 1:N com a ocorrência |
| Java | Caminho de uma requisição? | Controller recebe o DTO validado → BO aplica a regra → DAO executa o SQL com PreparedStatement → Oracle; volta como DTO de saída |
| Java | Como impede cidadão no painel? | Confere o `X-Gestor-Id` em `tb_gestor` a cada requisição; senão 403 |
| Java | Por que não guardar a senha? | Guardamos o hash BCrypt; nem a gente consegue ver a senha |
| Front | Como o front fala com a API? | Só `fetch`, centralizado em `services/api.ts`, URL em `VITE_API_URL` |
| Front | Como protege o painel? | `RotaProtegida` + menu só para gestor; a trava real é a Java |
| Python | Por que set no apoio? | Set não aceita repetido: cada cidadão apoia uma vez (RN08) |
| Eng. Software | Quem paga? | A prefeitura (assinatura por faixa de população); o cidadão usa de graça (B2B2C) |

## 12. Limitações conhecidas (dizer antes que perguntem)
1. Login sem token (id no cabeçalho pode ser forjado) → próxima etapa: JWT.
2. Sem notificação por e-mail/SMS → o cidadão volta ao site para acompanhar.
3. Previsão da IA com ganho modesto sobre uma tabela de medianas, e sem dados de iluminação.
4. Sem mapa/geolocalização: o endereço é texto.
5. Fotos limitadas a 3 por ocorrência por causa do espaço do Oracle da FIAP.
