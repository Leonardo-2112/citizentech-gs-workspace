"""
dados.py - Persistência: arquivo JSON local, relatório .txt, exportação para o
front-end e sincronização com o Oracle da FIAP.

O JSON (data/ocorrencias.json) é a base de trabalho e funciona sem internet.
O Oracle é opcional: usa as MESMAS tabelas tb_* da API Java (seção 6 do Documento
Base), então o que o terminal envia aparece no site e o que o site registra pode
ser importado para o terminal.
As credenciais nunca ficam no código: vêm do arquivo .env.
"""
import json
import os
from datetime import date, datetime

from regras import (busca_bairro, busca_categoria, calcula_prioridade, classe_prioridade,
                    dias_em_aberto, esta_atrasada, primeiro_nome, proximo_id,
                    transicao_permitida)
from util import data_para_texto

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQ_DADOS = os.path.join(PASTA_PROJETO, "data", "ocorrencias.json")
ARQ_RELATORIO = os.path.join(PASTA_PROJETO, "relatorios", "relatorio_bairros.txt")
ARQ_EXPORTACAO = os.path.join(PASTA_PROJETO, "exports", "ocorrencias_api.json")

# Tabelas do Documento Base (seção 6.2) que o terminal usa no Oracle
TABELAS = ("tb_orgao", "tb_bairro", "tb_cidadao", "tb_categoria",
           "tb_ocorrencia", "tb_atualizacao", "tb_apoio")


# ================================================================= .env
def carrega_env() -> None:
    """Lê o arquivo .env (CHAVE=valor por linha) e coloca os valores em os.environ."""
    caminho = os.path.join(PASTA_PROJETO, ".env")
    if not os.path.exists(caminho):
        return
    with open(caminho, mode="r", encoding="utf-8") as arq:
        for linha in arq:
            linha = linha.strip()
            if linha != "" and not linha.startswith("#") and "=" in linha:
                chave, valor = linha.split("=", 1)
                os.environ.setdefault(chave.strip(), valor.strip())


# ================================================================= JSON e TXT
# Valor padrão de cada campo da ocorrência (usado se o JSON vier sem algum campo)
CAMPOS_PADRAO = (("id_oracle", None), ("data_resolucao", None), ("apoiadores", []),
                 ("prazo_previsto", None), ("risco_atraso", None), ("historico", []))
CAMPOS_OBRIGATORIOS = ("id", "descricao", "endereco", "status", "data_abertura",
                       "categoria", "bairro", "autor_nome", "autor_email")


def ocorrencia_valida(ocorrencia) -> bool:
    """
    Confere se o registro lido do JSON tem os campos obrigatórios e completa os opcionais.
    Assim um arquivo editado à mão não derruba o programa com KeyError.
    """
    if not isinstance(ocorrencia, dict):
        return False
    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in ocorrencia:
            return False
    for campo, padrao in CAMPOS_PADRAO:
        if campo not in ocorrencia:
            ocorrencia[campo] = padrao
    return True


def carrega_dados(caminho: str) -> list:
    """
    Lê as ocorrências do arquivo JSON. Se o arquivo não existe, começa vazio.
    Se estiver corrompido, guarda uma cópia .bak e começa vazio (não perde nada).
    Registros incompletos são ignorados com aviso.
    """
    try:
        with open(caminho, mode="r", encoding="utf-8") as arq:
            lidas = json.load(arq)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        os.replace(caminho, f"{caminho}.bak")
        print("  [AVISO] O arquivo de dados estava corrompido; uma cópia foi salva como .bak.")
        return []
    if not isinstance(lidas, list):
        print("  [AVISO] O arquivo de dados não tem uma lista de ocorrências; começando vazio.")
        return []
    ocorrencias = []
    ignoradas = 0
    for ocorrencia in lidas:
        if ocorrencia_valida(ocorrencia):
            ocorrencias.append(ocorrencia)
        else:
            ignoradas = ignoradas + 1
    if ignoradas > 0:
        print(f"  [AVISO] {ignoradas} registro(s) incompleto(s) no JSON foram ignorados.")
    return ocorrencias


def salva_dados(caminho: str, ocorrencias: list) -> None:
    """Grava a lista de ocorrências no arquivo JSON (indentado, com acentos)."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, mode="w", encoding="utf-8") as arq:
        json.dump(ocorrencias, arq, indent=4, ensure_ascii=False)


def salva_relatorio(caminho: str, linhas: list) -> None:
    """Grava o relatório em .txt, uma linha de texto por item da lista."""
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, mode="w", encoding="utf-8") as arq:
        for texto in linhas:
            arq.write(f"{texto}\n")


# ================================================================= exportação para o front
def monta_json_api(ocorrencia: dict, hoje: date) -> dict:
    """Monta a ocorrência no formato da API Java (seção 8.3: camelCase, datas AAAA-MM-DD)."""
    categoria = busca_categoria(ocorrencia["categoria"])
    bairro = busca_bairro(ocorrencia["bairro"])
    pontos = calcula_prioridade(ocorrencia, hoje)
    classe = None
    if pontos is not None:
        classe = classe_prioridade(pontos)
    id_publico = ocorrencia["id"]
    if ocorrencia["id_oracle"] is not None:
        id_publico = ocorrencia["id_oracle"]
    return {
        "id": id_publico,
        "descricao": ocorrencia["descricao"],
        "endereco": ocorrencia["endereco"],
        "status": ocorrencia["status"],
        "dataAbertura": ocorrencia["data_abertura"],
        "dataResolucao": ocorrencia["data_resolucao"],
        "categoria": {"id": categoria[0], "nome": categoria[1], "prazoDias": categoria[3],
                      "gravidade": categoria[4], "orgao": categoria[2]},
        "bairro": {"id": bairro[0], "nome": bairro[1], "subprefeitura": bairro[2]},
        "autor": primeiro_nome(ocorrencia["autor_nome"]),  # RN13: sem e-mail nem telefone
        "prazoPrevistoDias": ocorrencia["prazo_previsto"],
        "riscoAtraso": ocorrencia["risco_atraso"],
        "qtdApoios": len(ocorrencia["apoiadores"]),
        "diasEmAberto": dias_em_aberto(ocorrencia, hoje),
        "atrasada": esta_atrasada(ocorrencia, hoje),
        "pontuacaoPrioridade": pontos,
        "prioridade": classe,
    }


def exporta_json_api(caminho: str, ocorrencias: list, hoje: date) -> int:
    """Grava todas as ocorrências no formato da API (para o front ou para testes). Devolve a quantidade."""
    lista = []
    for ocorrencia in ocorrencias:
        lista.append(monta_json_api(ocorrencia, hoje))
    conteudo = {
        "geradoEm": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "total": len(lista),
        "dados": lista,
    }
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, mode="w", encoding="utf-8") as arq:
        json.dump(conteudo, arq, indent=4, ensure_ascii=False)
    return len(lista)


# ================================================================= Oracle: conexão
def conecta_oracle() -> tuple:
    """
    Abre a conexão com o Oracle FIAP usando DB_USER e DB_PASSWORD do .env.

    Devolve (conexao, "") se conectou, ou (None, "mensagem do problema").
    """
    try:
        import oracledb
    except ImportError:
        return None, "Biblioteca oracledb não instalada (pip install -r requirements.txt)."
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    if not usuario or not senha:
        return None, "Defina DB_USER e DB_PASSWORD no arquivo .env."
    host = os.getenv("DB_HOST", "oracle.fiap.com.br")
    porta = int(os.getenv("DB_PORT", "1521"))
    sid = os.getenv("DB_SID", "orcl")
    try:
        dsn = oracledb.makedsn(host, porta, sid=sid)
        conexao = oracledb.connect(user=usuario, password=senha, dsn=dsn, tcp_connect_timeout=10)
    except Exception as falha:
        return None, f"Não foi possível conectar ao Oracle: {falha}"
    return conexao, ""


def testa_oracle() -> tuple:
    """Conecta e confere se as 7 tabelas existem. Devolve (deu_certo, lista de mensagens)."""
    conexao, problema = conecta_oracle()
    if conexao is None:
        return False, [problema]
    mensagens = []
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT USER FROM dual")
        mensagens.append(f"Conectado ao Oracle como {cursor.fetchone()[0]}.")
        cursor.execute("SELECT table_name FROM user_tables")
        existentes = set()
        for linha in cursor.fetchall():
            existentes.add(linha[0].lower())
        faltando = []
        for tabela in TABELAS:
            if tabela not in existentes:
                faltando.append(tabela)
        mensagens.append(f"Tabelas do ZelaBairro encontradas: {len(TABELAS) - len(faltando)} de {len(TABELAS)}.")
        if len(faltando) > 0:
            mensagens.append(f"Faltando: {', '.join(faltando)} (rode o script SQL do grupo).")
            return False, mensagens
        cursor.execute("SELECT COUNT(*) FROM tb_ocorrencia")
        mensagens.append(f"Ocorrências no Oracle: {cursor.fetchone()[0]}.")
        return True, mensagens
    except Exception as falha:
        return False, [f"Erro ao consultar o Oracle: {falha}"]
    finally:
        conexao.close()


# ================================================================= Oracle: importar (SELECT)
SQL_OCORRENCIAS = """
    SELECT o.cd_ocorrencia, o.ds_ocorrencia, o.ds_endereco, o.st_ocorrencia, o.dt_abertura,
           o.dt_resolucao, o.nr_prazo_previsto, o.fl_risco_atraso,
           c.nm_categoria, b.nm_bairro, p.nm_cidadao, p.ds_email
      FROM tb_ocorrencia o
      JOIN tb_categoria c ON c.cd_categoria = o.cd_categoria
      JOIN tb_bairro b ON b.cd_bairro = o.cd_bairro
      JOIN tb_cidadao p ON p.cd_cidadao = o.cd_cidadao
     ORDER BY o.cd_ocorrencia"""

SQL_APOIOS = """
    SELECT a.cd_ocorrencia, p.ds_email
      FROM tb_apoio a JOIN tb_cidadao p ON p.cd_cidadao = a.cd_cidadao"""

SQL_HISTORICOS = """
    SELECT cd_ocorrencia, dt_atualizacao, st_anterior, st_novo, ds_comentario
      FROM tb_atualizacao ORDER BY cd_ocorrencia, cd_atualizacao"""


def data_oracle_para_texto(valor):
    """O Oracle devolve DATE como datetime; o JSON guarda AAAA-MM-DD (ou None)."""
    if valor is None:
        return None
    return valor.strftime("%Y-%m-%d")


def busca_por_id_oracle(ocorrencias: list, id_oracle: int):
    """Procura a ocorrência local que já foi ligada a um id do Oracle."""
    for ocorrencia in ocorrencias:
        if ocorrencia["id_oracle"] == id_oracle:
            return ocorrencia
    return None


def le_apoios_oracle(cursor) -> dict:
    """Devolve {cd_ocorrencia: set de e-mails dos apoiadores}."""
    cursor.execute(SQL_APOIOS)
    apoios = {}
    for cd_ocorrencia, email in cursor.fetchall():
        if cd_ocorrencia not in apoios:
            apoios[cd_ocorrencia] = set()
        apoios[cd_ocorrencia].add(email.lower())
    return apoios


def le_historicos_oracle(cursor) -> dict:
    """Devolve {cd_ocorrencia: lista de atualizações no formato do JSON local}."""
    cursor.execute(SQL_HISTORICOS)
    historicos = {}
    for cd_ocorrencia, data, anterior, novo, comentario in cursor.fetchall():
        if cd_ocorrencia not in historicos:
            historicos[cd_ocorrencia] = []
        historicos[cd_ocorrencia].append({
            "data": data_oracle_para_texto(data),
            "de": anterior,
            "para": novo,
            "comentario": comentario or "",
            "enviado": True,  # já está no Oracle
        })
    return historicos


def tem_pendencia(ocorrencia: dict) -> bool:
    """True se a ocorrência tem mudança de status ainda não enviada ao Oracle."""
    for item in ocorrencia["historico"]:
        if not item["enviado"]:
            return True
    return False


def importa_do_oracle(ocorrencias: list, hoje: date) -> tuple:
    """
    SELECT no Oracle e atualização do JSON local.
    - Ocorrência que ainda não existe aqui: é adicionada.
    - Ocorrência que já existe: une os apoios (set) e adota o status do Oracle,
      desde que o local não tenha mudanças ainda não enviadas. Nada é apagado.

    Devolve (novas, atualizadas, avisos).
    """
    conexao, problema = conecta_oracle()
    if conexao is None:
        return 0, 0, [problema]
    avisos = []
    novas = 0
    atualizadas = 0
    try:
        cursor = conexao.cursor()
        cursor.execute(SQL_OCORRENCIAS)
        linhas = cursor.fetchall()
        apoios = le_apoios_oracle(cursor)
        historicos = le_historicos_oracle(cursor)
    except Exception as falha:
        return 0, 0, [f"Erro ao consultar o Oracle: {falha}"]
    finally:
        conexao.close()

    for (cd, descricao, endereco, status, abertura, resolucao, prazo, risco,
         categoria, bairro, nome, email) in linhas:
        emails = apoios.get(cd, set())
        local = busca_por_id_oracle(ocorrencias, cd)
        if local is None:
            if busca_categoria(categoria) is None or busca_bairro(bairro) is None:
                avisos.append(f"Oracle #{cd}: categoria ou bairro fora da lista do terminal; ignorada.")
                continue
            ocorrencias.append({
                "id": proximo_id(ocorrencias),
                "id_oracle": cd,
                "descricao": descricao,
                "endereco": endereco,
                "status": status,
                "data_abertura": data_oracle_para_texto(abertura),
                "data_resolucao": data_oracle_para_texto(resolucao),
                "categoria": categoria,
                "bairro": bairro,
                "autor_nome": nome,
                "autor_email": email.lower(),
                "apoiadores": list(emails),
                "prazo_previsto": prazo,
                "risco_atraso": risco,
                "historico": historicos.get(cd, []),
            })
            novas += 1
        else:
            mudou = False
            uniao = set(local["apoiadores"]) | emails  # união de conjuntos
            if len(uniao) != len(local["apoiadores"]):
                local["apoiadores"] = list(uniao)
                mudou = True
            if status != local["status"] and not tem_pendencia(local):
                local["historico"].append({"data": data_para_texto(hoje), "de": local["status"],
                                           "para": status, "comentario": "Atualizado no Oracle",
                                           "enviado": True})
                local["status"] = status
                local["data_resolucao"] = data_oracle_para_texto(resolucao)
                mudou = True
            if mudou:
                atualizadas += 1
    return novas, atualizadas, avisos


# ================================================================= Oracle: enviar (INSERT/UPDATE)
SQL_COD_CIDADAO = "SELECT cd_cidadao FROM tb_cidadao WHERE LOWER(ds_email) = :email"
SQL_COD_CATEGORIA = "SELECT cd_categoria FROM tb_categoria WHERE nm_categoria = :nome"
SQL_COD_BAIRRO = "SELECT cd_bairro FROM tb_bairro WHERE nm_bairro = :nome"

SQL_INSERE_OCORRENCIA = """
    INSERT INTO tb_ocorrencia (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia,
                               dt_abertura, dt_resolucao, nr_prazo_previsto, fl_risco_atraso,
                               cd_cidadao, cd_categoria, cd_bairro)
    VALUES (sq_tb_ocorrencia.NEXTVAL, :descricao, :endereco, :status, :abertura, :resolucao,
            :prazo, :risco, :cidadao, :categoria, :bairro)"""

SQL_STATUS_ORACLE = "SELECT st_ocorrencia FROM tb_ocorrencia WHERE cd_ocorrencia = :id"
SQL_ATUALIZA_STATUS = """
    UPDATE tb_ocorrencia SET st_ocorrencia = :status, dt_resolucao = :resolucao
     WHERE cd_ocorrencia = :id"""

SQL_APOIO_EXISTE = "SELECT COUNT(*) FROM tb_apoio WHERE cd_cidadao = :cidadao AND cd_ocorrencia = :id"
SQL_INSERE_APOIO = """
    INSERT INTO tb_apoio (cd_cidadao, cd_ocorrencia, dt_apoio) VALUES (:cidadao, :id, SYSDATE)"""

# Na v1.2+ do Documento Base tb_atualizacao tem cd_gestor (NOT NULL); na v1.0 não tem.
SQL_TEM_GESTOR = """
    SELECT COUNT(*) FROM user_tab_columns
     WHERE table_name = 'TB_ATUALIZACAO' AND column_name = 'CD_GESTOR'"""
SQL_COD_GESTOR = "SELECT cd_gestor FROM tb_gestor WHERE LOWER(ds_email) = :email"
SQL_INSERE_ATUALIZACAO = """
    INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo,
                                ds_comentario, dt_atualizacao)
    VALUES (sq_tb_atualizacao.NEXTVAL, :id, :anterior, :novo, :comentario, :data)"""
SQL_INSERE_ATUALIZACAO_GESTOR = """
    INSERT INTO tb_atualizacao (cd_atualizacao, cd_ocorrencia, st_anterior, st_novo,
                                ds_comentario, cd_gestor, dt_atualizacao)
    VALUES (sq_tb_atualizacao.NEXTVAL, :id, :anterior, :novo, :comentario, :gestor, :data)"""


def busca_codigo(cursor, sql: str, parametros: dict):
    """Executa um SELECT de uma coluna e devolve o número (ou None se não achou)."""
    cursor.execute(sql, parametros)
    linha = cursor.fetchone()
    if linha is None:
        return None
    return int(linha[0])


def texto_para_datetime(texto):
    """AAAA-MM-DD -> datetime (o Oracle recebe DATE); None continua None."""
    if texto is None:
        return None
    return datetime.strptime(texto, "%Y-%m-%d")


def insere_ocorrencia(cursor, ocorrencia: dict, avisos: list):
    """
    INSERT em tb_ocorrencia. O autor, a categoria e o bairro precisam existir no Oracle
    (RN01); o cidadão é cadastrado pelo site, nunca pelo terminal (RN02).
    Devolve o cd_ocorrencia criado, ou None se não foi possível enviar.
    """
    numero = ocorrencia["id"]
    cd_cidadao = busca_codigo(cursor, SQL_COD_CIDADAO, {"email": ocorrencia["autor_email"]})
    cd_categoria = busca_codigo(cursor, SQL_COD_CATEGORIA, {"nome": ocorrencia["categoria"]})
    cd_bairro = busca_codigo(cursor, SQL_COD_BAIRRO, {"nome": ocorrencia["bairro"]})
    if cd_cidadao is None:
        avisos.append(f"#{numero}: o autor {ocorrencia['autor_email']} não está cadastrado no Oracle (cadastro pelo site).")
        return None
    if cd_categoria is None or cd_bairro is None:
        avisos.append(f"#{numero}: categoria ou bairro não encontrado no Oracle.")
        return None
    cursor.execute(SQL_INSERE_OCORRENCIA, {
        "descricao": ocorrencia["descricao"],
        "endereco": ocorrencia["endereco"],
        "status": ocorrencia["status"],
        "abertura": texto_para_datetime(ocorrencia["data_abertura"]),
        "resolucao": texto_para_datetime(ocorrencia["data_resolucao"]),
        "prazo": ocorrencia["prazo_previsto"],
        "risco": ocorrencia["risco_atraso"],
        "cidadao": cd_cidadao,
        "categoria": cd_categoria,
        "bairro": cd_bairro,
    })
    cursor.execute("SELECT sq_tb_ocorrencia.CURRVAL FROM dual")  # id gerado pela sequence
    return int(cursor.fetchone()[0])


def atualiza_status_oracle(cursor, ocorrencia: dict, id_oracle: int, avisos: list) -> str:
    """
    UPDATE do status de uma ocorrência que já está no Oracle.
    Só envia se a mudança respeita a RN05 a partir do status que está lá.
    Devolve 'igual', 'atualizada' ou 'conflito'.
    """
    cursor.execute(SQL_STATUS_ORACLE, {"id": id_oracle})
    linha = cursor.fetchone()
    if linha is None:
        avisos.append(f"#{ocorrencia['id']}: não existe mais no Oracle (id {id_oracle}).")
        return "conflito"
    status_oracle = linha[0]
    if status_oracle == ocorrencia["status"]:
        return "igual"
    if not transicao_permitida(status_oracle, ocorrencia["status"]):
        avisos.append(f"#{ocorrencia['id']}: Oracle está em {status_oracle} e o local em "
                      f"{ocorrencia['status']}; importe do Oracle antes de enviar.")
        return "conflito"
    cursor.execute(SQL_ATUALIZA_STATUS, {
        "status": ocorrencia["status"],
        "resolucao": texto_para_datetime(ocorrencia["data_resolucao"]),
        "id": id_oracle,
    })
    return "atualizada"


def envia_apoios(cursor, ocorrencia: dict, id_oracle: int, avisos: list) -> int:
    """INSERT em tb_apoio para cada apoiador que já é cidadão no Oracle. Devolve quantos enviou."""
    enviados = 0
    for email in ocorrencia["apoiadores"]:
        cd_cidadao = busca_codigo(cursor, SQL_COD_CIDADAO, {"email": email})
        if cd_cidadao is None:
            avisos.append(f"#{ocorrencia['id']}: apoiador {email} não está cadastrado no Oracle.")
            continue
        if busca_codigo(cursor, SQL_APOIO_EXISTE, {"cidadao": cd_cidadao, "id": id_oracle}) == 0:
            cursor.execute(SQL_INSERE_APOIO, {"cidadao": cd_cidadao, "id": id_oracle})
            enviados += 1
    return enviados


def descobre_gestor(cursor, email_gestor: str) -> tuple:
    """
    RN06 e RN16: toda atualização guarda o gestor que a fez, e só gestor muda status.
    Procura em tb_gestor o gestor pelo e-mail informado no terminal.
    Devolve (precisa_de_gestor, cd_gestor) conforme a versão da tabela tb_atualizacao.
    """
    if busca_codigo(cursor, SQL_TEM_GESTOR, {}) == 0:
        return False, None
    return True, busca_codigo(cursor, SQL_COD_GESTOR, {"email": email_gestor})


def envia_historico(cursor, ocorrencia: dict, id_oracle: int, gestor: tuple, avisos: list) -> bool:
    """INSERT em tb_atualizacao das mudanças de status ainda não enviadas. Devolve True se enviou."""
    pendentes = []
    for item in ocorrencia["historico"]:
        if not item["enviado"]:
            pendentes.append(item)
    if len(pendentes) == 0:
        return False
    precisa_gestor, cd_gestor = gestor
    if precisa_gestor and cd_gestor is None:
        avisos.append(f"#{ocorrencia['id']}: histórico não enviado (não há gestor em tb_gestor).")
        return False
    for item in pendentes:
        parametros = {"id": id_oracle, "anterior": item["de"], "novo": item["para"],
                      "comentario": item["comentario"] or None,
                      "data": texto_para_datetime(item["data"])}
        if precisa_gestor:
            parametros["gestor"] = cd_gestor
            cursor.execute(SQL_INSERE_ATUALIZACAO_GESTOR, parametros)
        else:
            cursor.execute(SQL_INSERE_ATUALIZACAO, parametros)
    return True


def envia_uma(cursor, ocorrencia: dict, gestor: tuple, avisos: list) -> tuple:
    """Envia uma ocorrência. Devolve (acao, id_oracle, historico_enviado, qtd_apoios)."""
    id_oracle = ocorrencia["id_oracle"]
    acao = "nada"
    if id_oracle is None:
        id_oracle = insere_ocorrencia(cursor, ocorrencia, avisos)
        if id_oracle is None:
            return "ignorada", None, False, 0
        acao = "nova"
    else:
        resultado = atualiza_status_oracle(cursor, ocorrencia, id_oracle, avisos)
        if resultado == "conflito":
            return "conflito", id_oracle, False, 0
        if resultado == "atualizada":
            acao = "atualizada"
    qtd_apoios = envia_apoios(cursor, ocorrencia, id_oracle, avisos)
    historico_enviado = envia_historico(cursor, ocorrencia, id_oracle, gestor, avisos)
    return acao, id_oracle, historico_enviado, qtd_apoios


def envia_para_oracle(ocorrencias: list, email_gestor: str) -> tuple:
    """
    Envia ao Oracle as ocorrências novas, as mudanças de status, os apoios e o histórico.
    O e-mail precisa ser de um gestor cadastrado em tb_gestor (RN06 e RN16); se não for,
    nada é enviado. Cada ocorrência tem seu próprio COMMIT (ou ROLLBACK se der erro);
    o JSON local só é marcado como enviado depois do COMMIT.

    Devolve (novas, atualizadas, apoios_enviados, avisos).
    """
    conexao, problema = conecta_oracle()
    if conexao is None:
        return 0, 0, 0, [problema]
    avisos = []
    novas = 0
    atualizadas = 0
    apoios = 0
    try:
        cursor = conexao.cursor()
        gestor = descobre_gestor(cursor, email_gestor)
        if gestor[0] and gestor[1] is None:
            avisos.append(f"RN16: {email_gestor} não é um gestor cadastrado em tb_gestor; nada foi enviado.")
            return 0, 0, 0, avisos
        for ocorrencia in ocorrencias:
            try:
                acao, id_oracle, historico_ok, qtd_apoios = envia_uma(cursor, ocorrencia, gestor, avisos)
                conexao.commit()
            except Exception as falha:
                conexao.rollback()
                avisos.append(f"#{ocorrencia['id']}: erro no Oracle, nada foi gravado ({falha}).")
                continue
            # Só depois do COMMIT o JSON local passa a refletir o que foi enviado
            if id_oracle is not None:
                ocorrencia["id_oracle"] = id_oracle
            if historico_ok:
                for item in ocorrencia["historico"]:
                    item["enviado"] = True
            apoios = apoios + qtd_apoios
            if acao == "nova":
                novas += 1
            elif acao == "atualizada":
                atualizadas += 1
    except Exception as falha:
        avisos.append(f"Erro no Oracle: {falha}")
    finally:
        conexao.close()
    return novas, atualizadas, apoios, avisos
