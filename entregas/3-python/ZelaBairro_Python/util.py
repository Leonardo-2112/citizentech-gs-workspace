"""
util.py - Funções de apoio: tela do terminal, leitura de dados e datas.

Aqui NÃO ficam regras de negócio (elas estão em regras.py). Só o que serve para
desenhar a tela, ler o que o usuário digita (com validação) e converter datas.
"""
import textwrap
from datetime import date, datetime

LARGURA = 78  # largura fixa da tela: cabe no PyCharm e no VS Code sem quebrar linha


# ---------------------------------------------------------------- tela
def linha(caractere: str = "-") -> None:
    """Desenha uma linha separadora com a largura da tela."""
    print(f"{caractere * LARGURA}")


def titulo(texto: str) -> None:
    """Mostra um título centralizado entre duas linhas."""
    print()
    linha("=")
    print(f"{texto.upper():^{LARGURA}}")
    linha("=")


def caixa(linhas: list) -> None:
    """Desenha uma caixa com bordas e uma linha de texto por item da lista."""
    borda = "-" * (LARGURA - 2)
    print(f"+{borda}+")
    for texto in linhas:
        print(f"| {texto:<{LARGURA - 4}} |")
    print(f"+{borda}+")


def mensagem(prefixo: str, texto: str) -> None:
    """Imprime uma mensagem com prefixo; textos longos quebram alinhados."""
    partes = textwrap.wrap(texto, LARGURA - len(prefixo) - 4)
    print()
    primeira = True
    for parte in partes:
        if primeira:
            print(f"  {prefixo} {parte}")
            primeira = False
        else:
            recuo = " " * (len(prefixo) + 3)  # alinha a continuação sob o texto
            print(f"{recuo}{parte}")


def sucesso(texto: str) -> None:
    """Mensagem de operação concluída."""
    mensagem("[OK]", texto)


def erro(texto: str) -> None:
    """Mensagem de erro: a operação não foi feita."""
    mensagem("[ERRO]", texto)


def aviso(texto: str) -> None:
    """Mensagem de aviso: algo precisa de atenção, mas o programa continua."""
    mensagem("[AVISO]", texto)


def pausa() -> None:
    """Espera o usuário ler a tela antes de voltar ao menu."""
    input("\n  Pressione ENTER para continuar...")


def ajusta(valor, largura: int) -> str:
    """Prepara um valor para uma coluna: números à direita, textos à esquerda."""
    if valor is None:
        return "-".rjust(largura)
    if isinstance(valor, int):
        return str(valor).rjust(largura)
    if isinstance(valor, float):
        return f"{valor:.1f}".rjust(largura)
    texto = str(valor)
    if len(texto) > largura:
        texto = texto[:largura - 2] + ".."
    return texto.ljust(largura)


def coluna_numerica(linhas: list, chave: str) -> bool:
    """True se algum valor da coluna é número (int ou float)."""
    for item in linhas:
        if isinstance(item[chave], (int, float)):
            return True
    return False


def mostra_tabela(linhas: list, colunas: list) -> None:
    """
    Mostra uma lista de dicionários como tabela alinhada.

    colunas: lista de tuplas (chave, título, largura).
    """
    cabecalho = "  "
    separador = "  "
    for chave, rotulo, largura in colunas:
        # coluna numérica: o título também fica alinhado à direita
        if coluna_numerica(linhas, chave):
            cabecalho = f"{cabecalho}{rotulo:>{largura}} "
        else:
            cabecalho = f"{cabecalho}{ajusta(rotulo, largura)} "
        separador = f"{separador}{'-' * largura} "
    print(f"{cabecalho.rstrip()}")
    print(f"{separador.rstrip()}")
    for item in linhas:
        texto_linha = "  "
        for chave, rotulo, largura in colunas:
            texto_linha = f"{texto_linha}{ajusta(item[chave], largura)} "
        print(f"{texto_linha.rstrip()}")
    print(f"\n  Total: {len(linhas)}")


def mostra_campo(rotulo: str, valor) -> None:
    """Mostra 'Rótulo : valor'; textos longos quebram alinhados sob o valor."""
    if valor is None or valor == "":
        valor = "-"
    partes = textwrap.wrap(str(valor), LARGURA - 26)
    primeira = True
    for parte in partes:
        if primeira:
            print(f"  {rotulo:<20}: {parte}")
            primeira = False
        else:
            recuo = " " * 24  # alinha a continuação sob o valor
            print(f"{recuo}{parte}")


# ---------------------------------------------------------------- leitura
def le_inteiro(texto: str, minimo: int, maximo: int) -> int:
    """Lê um número inteiro entre minimo e maximo, repetindo até digitar certo."""
    numero = 0
    digitou_certo = False
    while not digitou_certo:
        try:
            numero = int(input(f"  {texto}: "))
            if minimo <= numero <= maximo:
                digitou_certo = True
            else:
                aviso(f"Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            aviso("Digite apenas números inteiros.")
    return numero


def le_texto(texto: str, minimo: int, maximo: int) -> str:
    """Lê um texto com tamanho entre minimo e maximo caracteres (minimo 0 = opcional)."""
    resposta = ""
    valido = False
    while not valido:
        resposta = input(f"  {texto}: ").strip()
        tamanho = len(resposta)
        if tamanho < minimo:
            aviso(f"Mínimo de {minimo} caracteres (você digitou {tamanho}).")
        elif tamanho > maximo:
            aviso(f"Máximo de {maximo} caracteres (você digitou {tamanho}).")
        else:
            valido = True
    return resposta


def le_sim_nao(texto: str) -> bool:
    """Pergunta S/N e devolve True para S (repete até responder S ou N)."""
    resposta = ""
    while resposta != "S" and resposta != "N":
        resposta = input(f"  {texto} (S/N): ").strip().upper()
        if resposta != "S" and resposta != "N":
            aviso("Responda apenas S ou N.")
    return resposta == "S"


def email_valido(texto: str) -> bool:
    """Confere o formato básico de um e-mail: algo@dominio.xx, sem espaços."""
    if " " in texto or texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    if usuario == "" or "." not in dominio:
        return False
    return not dominio.startswith(".") and not dominio.endswith(".")


def le_email(texto: str, maximo: int = 120) -> str:
    """Lê um e-mail válido e devolve em minúsculas (RN02: o e-mail identifica o cidadão)."""
    email = ""
    valido = False
    while not valido:
        email = input(f"  {texto}: ").strip().lower()
        if len(email) > maximo:
            aviso(f"O e-mail deve ter no máximo {maximo} caracteres.")
        elif email_valido(email):
            valido = True
        else:
            aviso("E-mail inválido. Exemplo: nome@email.com")
    return email


# ---------------------------------------------------------------- datas
# Os dados guardam datas como texto AAAA-MM-DD (o mesmo formato da API Java);
# na tela elas aparecem como DD/MM/AAAA.
def texto_para_data(texto: str) -> date:
    """Converte o texto AAAA-MM-DD guardado no JSON em data."""
    return datetime.strptime(texto, "%Y-%m-%d").date()


def data_para_texto(data: date) -> str:
    """Converte uma data no texto AAAA-MM-DD usado no JSON."""
    return data.strftime("%Y-%m-%d")


def data_para_br(texto) -> str:
    """Converte AAAA-MM-DD em DD/MM/AAAA ('-' se não houver data)."""
    if not texto:
        return "-"
    return texto_para_data(texto).strftime("%d/%m/%Y")
