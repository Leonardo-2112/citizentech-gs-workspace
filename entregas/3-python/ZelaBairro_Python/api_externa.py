"""
api_externa.py - Consumo de APIs externas (opcional: o programa funciona sem internet).

1) ViaCEP (https://viacep.com.br): a partir do CEP devolve rua e bairro, para
   preencher o "endereço de referência" da ocorrência (RN03).
2) API de IA do ZelaBairro (Flask, seção 7.3 do Documento Base): devolve o prazo
   previsto e o risco de atraso. O endereço fica na variável IA_API_URL do .env.
   RN12: se a IA estiver fora do ar, a ocorrência é criada mesmo assim, sem previsão.

Todas as funções devolvem uma tupla (resultado, mensagem) e nunca derrubam o programa.
"""
import os

URL_VIACEP = "https://viacep.com.br/ws/{cep}/json/"
TEMPO_LIMITE = 8  # segundos de espera por resposta


def importa_requests():
    """Importa a biblioteca requests só quando precisa (sem ela o resto do programa funciona)."""
    try:
        import requests
        return requests
    except ImportError:
        return None


def busca_cep(cep: str) -> tuple:
    """
    Consulta o ViaCEP com GET e lê a resposta JSON.

    Devolve ({"cep", "logradouro", "bairro", "cidade", "uf"}, "") se achou,
    ou (None, "mensagem do problema") se não deu certo.
    """
    cep = cep.replace("-", "").replace(".", "").strip()
    if len(cep) != 8 or not cep.isdigit():
        return None, "CEP inválido: informe os 8 números (ex.: 05001-100)."
    requests = importa_requests()
    if requests is None:
        return None, "Biblioteca requests não instalada (pip install -r requirements.txt)."
    try:
        resposta = requests.get(URL_VIACEP.format(cep=cep), timeout=TEMPO_LIMITE)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.Timeout:
        return None, "O ViaCEP demorou demais para responder."
    except requests.RequestException:
        return None, "Sem conexão com o ViaCEP (verifique a internet)."
    except ValueError:
        return None, "O ViaCEP devolveu uma resposta inválida."
    if dados.get("erro"):
        return None, f"CEP {cep} não encontrado."
    resultado = {
        "cep": cep,
        "logradouro": dados.get("logradouro", ""),
        "bairro": dados.get("bairro", ""),
        "cidade": dados.get("localidade", ""),
        "uf": dados.get("uf", ""),
    }
    return resultado, ""


def prever_ia(categoria: str, subprefeitura: str, mes: int, dia_semana: int) -> tuple:
    """
    Chama a API Flask de IA do grupo (POST /prever/prazo e POST /prever/atraso).

    Corpo enviado: {"categoria", "subprefeitura", "mes" (1-12), "dia_semana" (0 = segunda)}.
    Devolve (prazo_previsto_dias, risco_atraso 'S'/'N', mensagem). Se a IA não estiver
    configurada ou não responder, devolve (None, None, motivo) - é a RN12.
    """
    url = os.getenv("IA_API_URL", "").strip().rstrip("/")
    if url == "":
        return None, None, "IA não configurada (defina IA_API_URL no .env para usar)."
    requests = importa_requests()
    if requests is None:
        return None, None, "Biblioteca requests não instalada."
    corpo = {
        "categoria": categoria,
        "subprefeitura": subprefeitura,
        "mes": mes,
        "dia_semana": dia_semana,
    }
    try:
        resposta_prazo = requests.post(url + "/prever/prazo", json=corpo, timeout=TEMPO_LIMITE)
        resposta_prazo.raise_for_status()
        resposta_atraso = requests.post(url + "/prever/atraso", json=corpo, timeout=TEMPO_LIMITE)
        resposta_atraso.raise_for_status()
        prazo = int(resposta_prazo.json()["prazo_previsto_dias"])
        risco = resposta_atraso.json()["risco_atraso"]
    except (requests.RequestException, ValueError, KeyError):
        return None, None, "A API de IA não respondeu; a ocorrência segue sem previsão (RN12)."
    return prazo, risco, ""
