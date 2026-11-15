# Repositório do professor de Python (1tdspv_2026) — resumo técnico

- Link: https://github.com/egondo/1tdspv_2026
- Repositório de aulas de Computational Thinking Using Python da 1TDSPV: exemplos e exercícios resolvidos em sala, organizados por pasta temática. Serve de referência do estilo que o ZelaBairro Terminal (seção 10 do Documento Base v1.1) deve seguir.

Observação: o repositório tem um único commit ("Recursao - exemplos e exercicios"), então a ordem das aulas abaixo foi **inferida** pelo conteúdo e pela dificuldade, não pelo histórico do git. São cerca de 2.570 linhas de `.py` no total.

## Organização do repositório

| Pasta | Tema |
|---|---|
| `algoritmos/` | Primeiros programas: entrada, saída, cálculo simples (inclui um `exemplo.c` para comparar) |
| `decisao/` | `if/elif/else`, `match-case` (`exercicio11_lista.py`), calculadora de INSS |
| `checkpoint1/` | Resolução do CP1 (decisão com entrada numérica) |
| `repeticao/` | `while`, `for`/`range`, `random`, tabuada, laço infinito |
| `strings/` | Percorrer string, `in`, `find`, fatiamento |
| `cpf_binario/` | Dígitos de CPF e conversão binária (aritmética com `//` e `%`) |
| `funcao/` | `def`, parâmetros, retorno, type hints, passagem por valor |
| `listas/` | Listas e tuplas; sistema de locação com menu (`locacao.py`); exercício do álbum da Copa |
| `matriz/` | Listas de listas; jogo da velha em módulo separado (`velha.py` + `jogo_velha.py`) |
| `dicionario/` | Dicionários, contagem, lista de dicionários, menus com dicionário (`problema5.py`, `problema7.py`) |
| `busca/` | Busca sequencial e binária, medição com `time` |
| `ordenacao/` | Bubble sort, selection sort, partição (quick sort) implementados à mão |
| `arquivos/` | Leitura/gravação de `.txt`, `csv`, `json` |
| `excecoes/` | `try/except/else`, validação de número digitado, `isnumeric`, regex |
| `jogo21/`, `jogo_forca/` | Jogos com listas, tuplas e módulo próprio (`import baralho as deck`) |
| `processamentoImagensMaterial/` | Matrizes de pixels com Pillow (material de apoio) |
| `oracle/` | `oracledb`: SELECT e INSERT a partir de JSON |
| `locadora/` | App em camadas `app.py` / `service.py` / `banco.py` / `util.py` com Oracle e `datetime` |
| `cliente_api/` | `requests` (ViaCEP, GET/POST em API própria) |
| `livraria_api/`, `futebol_tabela/`, `sistema_enquete/` | APIs com Flask + Oracle |
| `streamlit/` | Interface com Streamlit e pandas (demonstração) |
| `recursao/` | Fatorial, Torre de Hanói (último tema do repositório) |
| `material/` | PDFs: Listas, Dicionário, Busca, Ordenação (não lidos, só os `.py`) |

## Conteúdo coberto até agora

1. Tipos, `input`/`print`, operadores (`//`, `%`), f-strings
2. Condicionais `if/elif/else` e `match-case` com `case _`
3. Laços `while` (contador manual `i = i + 1`) e `for ... in range(...)`
4. Strings (percorrer, `in`, `find`, `lower`, `upper`, `replace`, `isnumeric`)
5. Funções com parâmetros, retorno e type hints
6. Listas (`append`, `pop`, `insert`, índices) e tuplas (constantes, retorno de várias informações)
7. Matrizes (listas de listas)
8. Dicionários (chave/valor, `in`, `.values()`, lista de dicionários, dicionário de contagem)
9. Busca sequencial/binária e ordenação manual (bubble, selection)
10. Arquivos `.txt` (`read`, `readlines`, `for linha in arq`, modo `"a"`), CSV (`csv.reader`) e JSON (`json.load`/`json.dump`)
11. Tratamento de exceção (`try/except ValueError/else`, laço de redigitação)
12. Módulos próprios (`import banco`, `import velha`, `import baralho as deck`) e `if __name__ == "__main__":`
13. Banco Oracle com `oracledb` (conexão, cursor, bind `:nome` com dicionário, `commit`)
14. `datetime` (`strptime`/`strftime` com formato `"%d/%m/%Y %H:%M"`)
15. `requests` (consumo de API) e Flask (criação de API) — fora do escopo do ZelaBairro Terminal
16. Recursão

**Sets não aparecem em nenhum arquivo do repositório** (nenhum `set()` ou `.add(`). Como a seção 10 exige set (RN08) e a rubrica cita "Sets", usar só o básico: `set()`, `.add()`, `in`, `len()`.

## Estilo de código do professor

**Nomes:** `snake_case`, quase sempre em português (`cadastra_veiculo`, `calcula_media_aluno`, `recupera_clientes`, `lista_veiculos`). Funções com verbo no presente (`cadastra`, `consulta`, `insere`, `altera`, `recupera`). Variáveis curtas e descritivas (`opcao`, `lista`, `resp`, `pos`, `aux`). Chaves de dicionário em minúsculas sem acento (`'placa'`, `'data_retirada'`).

**Type hints** em quase todas as funções a partir da aula de funções, inclusive `-> None` e `-> tuple` (`dicionario/problema5.py`):
```python
def insere(whats: dict, num_tel: str, msg: str) -> None:
    if num_tel in whats:
        lista_msg = whats[num_tel]
        lista_msg.insert(0, msg)
    else:
        whats[num_tel] = [msg]
```

**Menu:** função `menu() -> int` que imprime as opções e devolve `int(input(...))`; laço `while opcao != <sair>` com `if/elif` (`dicionario/problema7.py`):
```python
def menu() -> int:
    print("1 - cadastra")
    print("2 - altera")
    print("3 - médias")
    print("4 - sair")
    return int(input("Opção: "))
```
```python
if __name__ == "__main__":
    tdspv = {}
    opcao = menu()
    while opcao != 4:
        if opcao == 1:
            cadastra(tdspv)
        elif opcao == 3:
            calcula_media(tdspv)
        opcao = menu()
```
Variante em `listas/locacao.py`: título do sistema no menu, sair com `9` e `print("_" * 40)` entre as iterações. Os dados ficam numa variável criada no bloco principal e **passada como parâmetro** às funções (não usa `global`).

**match-case:** usado com valor inteiro e `case _` para opção inválida (`decisao/exercicio11_lista.py`):
```python
match forma_pgto:
    case 1:
        desc = valor * 0.1
        print(f"O desconto foi de {desc:.2f}, vc pagara {valor - desc:.2f}")
    case 2:
        ...
    case _:
        print("Forma de pagamento inválida")
```
Nos menus o professor usa `if/elif`; `match-case` aparece só no exercício de decisão. Na GS a rubrica cobra os dois.

**Arquivos/JSON:** sempre `with open(..., mode="r")`, depois `json.load`; gravação com `json.dump(..., indent=4)` e mensagem de confirmação (`arquivos/exemplo_json_gravacao.py`):
```python
with open("lotofacil.txt", mode="w") as arq:
    json.dump(lotofacil, arq, indent=4)

print("arquivo gravado com sucesso")
```
Texto: `arq.write(...)` + `arq.write("\n")` com `mode="a"` (`arquivos/exemplo4.py`). Não usa `encoding=` nem `os.path`; os primeiros exemplos têm caminho absoluto `D:/...`, os de JSON usam caminho relativo.

**Validação de input:** `try/except` dentro de `while` com flag booleana (`excecoes/exercicio_input_numero.py`):
```python
digita_correto = False
while not digita_correto:
    try:
        salario = float(input("Digite o salario: "))
        digita_correto = True
    except:
        print("Digite corretamente o salario")
```
Em `excecoes/exemplo1.py` usa `except ValueError:` com `else:`. Validações de texto são feitas com `if` simples (`if placa:` para "não vazio", `len(...)`, `in`). Nos sistemas com menu o professor costuma fazer `int(input(...))` direto, sem proteção; na GS convém sempre proteger.

**try/except em camadas:** `except Exception as erro: print(erro)` nas APIs Flask; `raise Exception('...')` aparece em `matriz/exemplo3.py`. Não cria exceções próprias.

**main():** não define função `main()`. Usa `if __name__ == "__main__":` no fim do arquivo com o laço do menu (`dicionario/problema7.py`, `locadora/app.py`, `cliente_api/exemplo1.py`). Arquivos mais antigos têm o código solto no nível do módulo.

**Comentários e docstrings:** comentários curtos com `#` explicando a intenção (`#pedindo os dados do veiculo`, `#encerra o comando de repeticao`), muitas linhas de teste comentadas. Docstring com `'''...'''` aparece raramente, para listar regras de negócio (`locadora/service.py`: `'''Algumas regras possiveis: * ...'''`) ou o enunciado do exercício. Comentários sem acento na maioria.

**f-strings:** em toda saída com variável, inclusive formatação `:.2f` e `:.5f` e expressões dentro das chaves (`{valor - desc:.2f}`). Não usa `%` nem `.format()`.

**Estruturas de dados:** registro = dicionário; coleção = lista de dicionários (`dicionario/exemplo2.py`, `locadora/banco.py`); constantes e pares fixos = tupla (`listas/copa_mundo.py`, cartas `(valor, naipe)` em `jogo21/baralho.py`); dicionário de dicionários indexado por id (`turma[rm] = notas` em `problema7.py`); dicionário de contagem (`dicionario/problema1.py`):
```python
for letra in palavra:
    if not letra in dic:
        dic[letra] = 1
    else:
        valor = dic[letra]
        dic[letra] = valor + 1
```

**Ordenação:** implementada à mão com funções (`ordenacao/selection_sort.py`, `bubble_sort.py`); não usa `sorted()`, `.sort()` nem `lambda`.

**List comprehension e classes:** **nenhum** arquivo de aula do professor usa list comprehension nem `class`. As três ocorrências de comprehension estão em `streamlit/gerador_dados.py` e `processamentoImagensMaterial/teste_distribuicao_normal.py` (material de apoio, não conteúdo de aula). Listas são montadas com `lista = []` + `for` + `append`, ou `[' '] * 3`.

**Organização em módulos:** `app.py` (menu/entrada), `service.py` (regras), `banco.py` (persistência), `util.py` (conversões de data) em `locadora/`; cada módulo com funções pequenas e um bloco `if __name__ == "__main__":` para teste.

## Padrões a copiar no ZelaBairro Terminal

| Padrão do professor (arquivo de origem) | Onde usar (opção da seção 10) |
|---|---|
| `menu() -> int` + `while opcao != 0` + bloco `__main__` (`dicionario/problema7.py`) | Menu principal; carregar JSON antes do laço, salvar ao sair (0) |
| `try/except ValueError` em `while` com flag (`excecoes/exercicio_input_numero.py`) | Leitura de toda opção numérica, id de ocorrência, escolha de categoria/bairro |
| Validação com `if`/`len()` e mensagem com f-string (`listas/locacao.py`) | 1 Registrar: RN03 (descrição 10–500, endereço até 200) |
| Lista de dicionários percorrida com `for` + `if` (`locadora/app.py`) | 1 Registrar: RN07, listar ABERTA/EM_ANDAMENTO da mesma categoria e bairro |
| Dicionário de registro montado com chaves (`locadora/app.py`, `realiza_reserva_locacao`) | 1 Registrar: nova ocorrência com `status = 'ABERTA'` e data de abertura (RN04) |
| Set (não visto no repo; usar `set()`, `.add()`, `in`) + dicionário | 2 Apoiar: apoiadores por ocorrência, recusar duplicado e autor (RN08) |
| `match-case` com `case _` (`decisao/exercicio11_lista.py`) | 3 Atualizar status: `match status_atual:` decide os destinos permitidos (RN05) |
| Selection/bubble sort em função própria (`ordenacao/selection_sort.py`) | 4 Fila de prioridade: ordenar pela prioridade RN10 sem `lambda` |
| Funções pequenas com retorno numérico (`dicionario/problema7.py`, `calcula_media_aluno`) | 4 Fila: `calcula_prioridade(...) -> float` |
| Dicionário de contagem (`dicionario/problema1.py`) | 5 Relatório por bairro: abertas, atrasadas, soma de dias por bairro |
| `with open(..., mode="w")` + `arq.write(...)` (`arquivos/exemplo4.py`) | 5 Relatório: salvar `.txt` |
| `datetime.strptime`/`strftime` com formato fixo (`locadora/util.py`) | 4, 5 e 6: dias em aberto (RN10, RN11) |
| `for` + `if` filtrando e acumulando em lista (`listas/locacao.py`, `lista_veiculos`) | 6 Ocorrências atrasadas (RN11) |
| `json.load` / `json.dump(..., indent=4)` com mensagem (`arquivos/`) | Abrir e 0 Sair: `data/ocorrencias.json` |
| Tupla como constante (`listas/copa_mundo.py`) | `STATUS` e `CATEGORIAS` |
| Módulos `app/service/banco/util` (`locadora/`) | Divisão dos arquivos do projeto |

## Coisas a evitar

- `class` e qualquer orientação a objetos: nota zero na GS (−100). O professor nunca usa.
- List comprehension (`[x for x in ...]`), inclusive de dicionário/set: −15 por ocorrência. Conferir antes de entregar: `grep -n "class " *.py` e `grep -nE "\[.*for .* in" *.py` (e também `{... for ...}`).
- `lambda`, `sorted(key=...)`, `map`, `filter`, `enumerate`, `zip`: não aparecem nas aulas (há um `enumerate` isolado em `livraria_api/app_memoria.py`). Preferir `for` + `range` e ordenação manual.
- Bibliotecas não vistas ou desnecessárias: `pandas`, `numpy`, `streamlit`, `flask`, `requests`, `oracledb` (o Terminal é offline e usa JSON local). Usar só `json`, `datetime` e, se preciso, `os` (o professor usou `os.getenv` em `livraria_api/sistema_os.py`).
- `global`, dataclasses, `typing` avançado (`List[...]`, `Optional`), walrus `:=`, f-strings aninhadas complexas.
- Credenciais escritas no código: o repositório do professor tem usuário e senha do Oracle em texto claro (`oracle/`, `locadora/banco.py`); não copiar esse hábito.
- `except:` sem tipo: aparece numa aula, mas na GS preferir `except ValueError:` (mais claro para a nota de organização).
- Caminhos absolutos (`D:/...`): usar caminho relativo `data/ocorrencias.json`.

## Esqueleto sugerido do ZelaBairro Terminal no estilo do professor

Pasta `python/` (nomes em português, snake_case, type hints, comentários citando RN):

**`dados.py`** — constantes e persistência
- `STATUS = ('ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', 'CANCELADA')` e `CATEGORIAS = (...)` da tabela 6.4 (tuplas).
- `carrega_dados(caminho: str) -> list` — `json.load` de `data/ocorrencias.json`; lista vazia se o arquivo não existir (`try/except FileNotFoundError`).
- `salva_dados(caminho: str, ocorrencias: list) -> None` — `json.dump(..., indent=4)`; apoiadores convertidos de set para lista antes de gravar.
- `salva_relatorio(caminho: str, linhas: list) -> None` — grava o relatório `.txt` com `arq.write`.

**`util.py`** — entrada e datas
- `le_inteiro(mensagem: str) -> int` — laço `while` + `try/except ValueError` até digitar um número.
- `le_texto(mensagem: str, minimo: int, maximo: int) -> str` — repete até o tamanho estar na faixa (RN03).
- `str_para_data(data: str)` / `data_para_str(data) -> str` — formato `"%d/%m/%Y"`.
- `dias_em_aberto(ocorrencia: dict) -> int` — hoje menos data de abertura.

**`regras.py`** — regras de negócio (cada função com comentário `# RN..`)
- `nova_ocorrencia(ocorrencias: list, dados: dict) -> dict` — monta o dicionário com `status = 'ABERTA'`, data de abertura = hoje, sem resolução (RN04).
- `busca_similares(ocorrencias: list, categoria: str, bairro: str) -> list` — ABERTA/EM_ANDAMENTO da mesma categoria e bairro (RN07).
- `apoia(ocorrencia: dict, email: str) -> str` — usa o set de apoiadores; recusa autor, duplicado ou status final (RN08); devolve a mensagem.
- `transicao_permitida(atual: str, novo: str) -> bool` — `match atual:` com `case 'ABERTA'`, `case 'EM_ANDAMENTO'`, `case _` (RN05).
- `calcula_prioridade(ocorrencia: dict) -> float` — fórmula da RN10 (só ABERTA/EM_ANDAMENTO).
- `ordena_por_prioridade(fila: list) -> None` — selection sort manual, decrescente.
- `esta_atrasada(ocorrencia: dict) -> bool` — dias em aberto > prazo da categoria (RN11).
- `conta_por_bairro(ocorrencias: list) -> dict` — dicionário de contagem: abertas, atrasadas, soma de dias.

**`app.py`** — menu e telas
- `menu() -> int` — imprime as opções 1–6 e 0 e lê com `le_inteiro`.
- `registrar_ocorrencia(ocorrencias: list) -> None` — opção 1.
- `apoiar_ocorrencia(ocorrencias: list) -> None` — opção 2.
- `atualizar_status(ocorrencias: list) -> None` — opção 3 (usa `match-case` também para o submenu de novo status).
- `fila_prioridade(ocorrencias: list) -> None` — opção 4.
- `relatorio_bairro(ocorrencias: list) -> None` — opção 5, imprime e salva `.txt`.
- `listar_atrasadas(ocorrencias: list) -> None` — opção 6.
- Bloco `if __name__ == "__main__":` — carrega o JSON, `opcao = menu()`, `while opcao != 0` com `match opcao:` (ou `if/elif`, como o professor), salva ao sair com mensagem de confirmação.

**`data/ocorrencias.json`** — massa inicial com as mesmas categorias, bairros e status do banco.
