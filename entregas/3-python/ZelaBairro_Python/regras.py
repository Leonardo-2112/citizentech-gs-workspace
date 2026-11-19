"""
regras.py - Regras de negócio do ZelaBairro (RN03 a RN13 do Documento Base).

Só cálculos e decisões: nenhuma função daqui lê do teclado nem grava arquivo.
Cada função cita a regra (RN) que ela aplica.
"""
from datetime import date

from util import data_para_texto, texto_para_data

# ---------------------------------------------------------------- constantes (tuplas)
# RN04: status possíveis
STATUS = ("ABERTA", "EM_ANDAMENTO", "RESOLVIDA", "CANCELADA")
STATUS_ABERTOS = ("ABERTA", "EM_ANDAMENTO")

# Tabela 6.4 do Documento Base: (código, nome, órgão responsável, prazo em dias, gravidade 1-5)
CATEGORIAS = (
    (1, "Buraco na via", "Subprefeitura - Zeladoria", 15, 4),
    (2, "Iluminação pública apagada", "Iluminação Pública", 7, 4),
    (3, "Descarte irregular de lixo", "Limpeza Urbana", 10, 3),
    (4, "Árvore com risco de queda", "Áreas Verdes", 5, 5),
    (5, "Poda de árvore", "Áreas Verdes", 30, 2),
    (6, "Calçada danificada", "Subprefeitura - Zeladoria", 30, 3),
    (7, "Bueiro entupido", "Subprefeitura - Zeladoria", 10, 4),
    (8, "Sinalização de trânsito danificada", "Trânsito e Sinalização", 10, 3),
)

# Distritos reais de São Paulo: (código, bairro, subprefeitura) - nomes iguais ao SP156 e à API de IA
BAIRROS = (
    (1, "Lapa", "Lapa"),
    (2, "Pinheiros", "Pinheiros"),
    (3, "Butantã", "Butantã"),
    (4, "Capão Redondo", "Campo Limpo"),
    (5, "Itaim Paulista", "Itaim Paulista"),
    (6, "Sé", "Sé"),
    (7, "Mooca", "Mooca"),
    (8, "Itaquera", "Itaquera"),
    (9, "Santo Amaro", "Santo Amaro"),
    (10, "Brasilândia", "Freguesia/Brasilândia"),
    (11, "Grajaú", "Capela do Socorro"),
    (12, "Cidade Tiradentes", "Cidade Tiradentes"),
)

# RN03: tamanhos dos textos
NOME_MAX = 100
EMAIL_MAX = 120
DESC_MIN = 10
DESC_MAX = 500
ENDERECO_MAX = 200
COMENTARIO_MAX = 300


# ---------------------------------------------------------------- consultas nas tuplas
def busca_categoria(nome: str):
    """Devolve a tupla da categoria pelo nome (ou None se não existir)."""
    for categoria in CATEGORIAS:
        if categoria[1] == nome:
            return categoria
    return None


def busca_bairro(nome: str):
    """Devolve a tupla do bairro pelo nome (ou None se não existir)."""
    for bairro in BAIRROS:
        if bairro[1] == nome:
            return bairro
    return None


def primeiro_nome(nome: str) -> str:
    """RN13: as listagens mostram só o primeiro nome do cidadão."""
    partes = nome.split()
    if len(partes) == 0:
        return "-"
    return partes[0]


# ---------------------------------------------------------------- ocorrências
def proximo_id(ocorrencias: list) -> int:
    """Próximo número livre para uma ocorrência nova."""
    maior = 0
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] > maior:
            maior = ocorrencia["id"]
    return maior + 1


def busca_ocorrencia(ocorrencias: list, id_ocorrencia: int):
    """Procura uma ocorrência pelo id (None se não achar)."""
    for ocorrencia in ocorrencias:
        if ocorrencia["id"] == id_ocorrencia:
            return ocorrencia
    return None


def cria_ocorrencia(ocorrencias: list, dados: dict, hoje: date) -> dict:
    """
    RN01 e RN04: monta a ocorrência com 1 autor, 1 categoria e 1 bairro.
    Ela nasce ABERTA, com data de abertura = hoje e sem data de resolução.
    """
    return {
        "id": proximo_id(ocorrencias),
        "id_oracle": None,  # preenchido quando a ocorrência é enviada ao Oracle
        "descricao": dados["descricao"],
        "endereco": dados["endereco"],
        "status": "ABERTA",
        "data_abertura": data_para_texto(hoje),
        "data_resolucao": None,
        "categoria": dados["categoria"],
        "bairro": dados["bairro"],
        "autor_nome": dados["autor_nome"],
        "autor_email": dados["autor_email"],
        "apoiadores": [],
        "prazo_previsto": dados["prazo_previsto"],  # vem da IA (RN12: pode ser None)
        "risco_atraso": dados["risco_atraso"],      # 'S', 'N' ou None
        "historico": [],
    }


def busca_similares(ocorrencias: list, categoria: str, bairro: str) -> list:
    """RN07: ocorrências ABERTA/EM_ANDAMENTO da mesma categoria e do mesmo bairro."""
    similares = []
    for ocorrencia in ocorrencias:
        if (ocorrencia["categoria"] == categoria and ocorrencia["bairro"] == bairro
                and ocorrencia["status"] in STATUS_ABERTOS):
            similares.append(ocorrencia)
    return similares


def apoia(ocorrencia: dict, email: str) -> tuple:
    """
    RN08: um cidadão apoia no máximo uma vez, não apoia a própria ocorrência
    e só apoia ocorrência ABERTA ou EM_ANDAMENTO.

    Devolve (deu_certo, mensagem).
    """
    email = email.strip().lower()
    if ocorrencia["status"] not in STATUS_ABERTOS:
        return False, "RN08: só é possível apoiar ocorrências ABERTA ou EM_ANDAMENTO."
    if email == ocorrencia["autor_email"]:
        return False, "RN08: o autor não pode apoiar a própria ocorrência."
    apoiadores = set(ocorrencia["apoiadores"])  # set não aceita repetido
    if email in apoiadores:
        return False, "RN08: este e-mail já apoia esta ocorrência."
    apoiadores.add(email)
    ocorrencia["apoiadores"] = list(apoiadores)  # no JSON o set vira lista
    return True, f"Apoio registrado. A ocorrência agora tem {len(apoiadores)} apoio(s)."


def transicao_permitida(atual: str, novo: str) -> bool:
    """
    RN05: ABERTA -> EM_ANDAMENTO ou CANCELADA; EM_ANDAMENTO -> RESOLVIDA ou CANCELADA.
    RESOLVIDA e CANCELADA são finais.
    """
    match atual:
        case "ABERTA":
            return novo in ("EM_ANDAMENTO", "CANCELADA")
        case "EM_ANDAMENTO":
            return novo in ("RESOLVIDA", "CANCELADA")
        case _:
            return False


def atualiza_status(ocorrencia: dict, novo: str, comentario: str, hoje: date) -> tuple:
    """
    RN05 e RN06: o status só muda criando uma atualização no histórico.
    A data de resolução é preenchida sozinha quando o novo status é RESOLVIDA.

    Devolve (deu_certo, mensagem).
    """
    atual = ocorrencia["status"]
    if not transicao_permitida(atual, novo):
        return False, f"RN05: a transição {atual} -> {novo} não é permitida."
    ocorrencia["historico"].append({
        "data": data_para_texto(hoje),
        "de": atual,
        "para": novo,
        "comentario": comentario,
        "enviado": False,  # ainda não foi enviada ao Oracle
    })
    ocorrencia["status"] = novo
    if novo == "RESOLVIDA":
        ocorrencia["data_resolucao"] = data_para_texto(hoje)
    return True, f"Status alterado de {atual} para {novo}."


# ---------------------------------------------------------------- prazo e atraso (RN11)
def dias_em_aberto(ocorrencia: dict, hoje: date) -> int:
    """Dias inteiros entre a abertura e hoje (ou a data de resolução, se já resolvida)."""
    abertura = texto_para_data(ocorrencia["data_abertura"])
    if ocorrencia["data_resolucao"]:
        fim = texto_para_data(ocorrencia["data_resolucao"])
    else:
        fim = hoje
    dias = (fim - abertura).days
    if dias < 0:
        dias = 0
    return dias


def esta_atrasada(ocorrencia: dict, hoje: date) -> bool:
    """RN11: atrasada = dias em aberto maior que o prazo de referência da categoria."""
    if ocorrencia["status"] == "CANCELADA":
        return False
    categoria = busca_categoria(ocorrencia["categoria"])
    return dias_em_aberto(ocorrencia, hoje) > categoria[3]


# ---------------------------------------------------------------- prioridade (RN10)
def detalha_prioridade(ocorrencia: dict, hoje: date):
    """
    RN10: pontos = gravidade*10 + min(apoios,20)*2 + min(dias,30) + 15 (se risco 'S' OU atrasada).

    Devolve a tupla (pts_gravidade, pts_apoios, pts_dias, pts_risco, total),
    ou None se a ocorrência não está ABERTA/EM_ANDAMENTO (não tem prioridade).
    """
    if ocorrencia["status"] not in STATUS_ABERTOS:
        return None
    categoria = busca_categoria(ocorrencia["categoria"])
    pts_gravidade = categoria[4] * 10
    pts_apoios = min(len(ocorrencia["apoiadores"]), 20) * 2
    pts_dias = min(dias_em_aberto(ocorrencia, hoje), 30)
    pts_risco = 0
    if ocorrencia["risco_atraso"] == "S" or esta_atrasada(ocorrencia, hoje):
        pts_risco = 15  # soma uma vez só
    total = pts_gravidade + pts_apoios + pts_dias + pts_risco
    return pts_gravidade, pts_apoios, pts_dias, pts_risco, total


def calcula_prioridade(ocorrencia: dict, hoje: date):
    """Pontuação total da RN10 (None se não tem prioridade). Calculada na hora, nunca gravada."""
    detalhe = detalha_prioridade(ocorrencia, hoje)
    if detalhe is None:
        return None
    return detalhe[4]


def classe_prioridade(pontos: int) -> str:
    """RN10: 70 ou mais = ALTA; de 40 a 69 = MEDIA; abaixo de 40 = BAIXA."""
    if pontos >= 70:
        return "ALTA"
    elif pontos >= 40:
        return "MEDIA"
    else:
        return "BAIXA"


def monta_fila(ocorrencias: list, hoje: date) -> list:
    """Lista de tuplas (pontos, ocorrência) só das ocorrências em aberto."""
    fila = []
    for ocorrencia in ocorrencias:
        pontos = calcula_prioridade(ocorrencia, hoje)
        if pontos is not None:
            fila.append((pontos, ocorrencia))
    return fila


def ordena_por_prioridade(fila: list) -> None:
    """
    Selection sort (visto em aula): a maior pontuação vai para o começo.
    No empate, a ocorrência mais antiga (menor id) fica na frente.
    """
    for i in range(len(fila) - 1):
        maior = i
        for j in range(i + 1, len(fila)):
            pontos_j = fila[j][0]
            pontos_maior = fila[maior][0]
            if pontos_j > pontos_maior or (
                    pontos_j == pontos_maior and fila[j][1]["id"] < fila[maior][1]["id"]):
                maior = j
        aux = fila[i]
        fila[i] = fila[maior]
        fila[maior] = aux


# ---------------------------------------------------------------- relatórios
def conta_por_status(ocorrencias: list) -> dict:
    """Dicionário de contagem: quantas ocorrências há em cada status."""
    contagem = {}
    for status in STATUS:
        contagem[status] = 0
    for ocorrencia in ocorrencias:
        contagem[ocorrencia["status"]] = contagem[ocorrencia["status"]] + 1
    return contagem


def conta_por_bairro(ocorrencias: list, hoje: date) -> dict:
    """
    Dicionário de contagem por bairro: abertas, atrasadas (entre as abertas),
    resolvidas e soma dos dias das resolvidas (para o tempo médio).
    """
    bairros = {}
    for ocorrencia in ocorrencias:
        nome = ocorrencia["bairro"]
        if nome not in bairros:
            bairros[nome] = {"abertas": 0, "atrasadas": 0, "resolvidas": 0, "soma_dias": 0}
        dados = bairros[nome]
        if ocorrencia["status"] in STATUS_ABERTOS:
            dados["abertas"] = dados["abertas"] + 1
            if esta_atrasada(ocorrencia, hoje):
                dados["atrasadas"] = dados["atrasadas"] + 1
        elif ocorrencia["status"] == "RESOLVIDA":
            dados["resolvidas"] = dados["resolvidas"] + 1
            dados["soma_dias"] = dados["soma_dias"] + dias_em_aberto(ocorrencia, hoje)
    return bairros


def tempo_medio(soma_dias: int, quantidade: int) -> float:
    """Tempo médio de resolução em dias (0.0 se ainda não há resolvidas)."""
    if quantidade == 0:
        return 0.0
    return soma_dias / quantidade
