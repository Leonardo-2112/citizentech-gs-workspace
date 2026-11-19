"""
ZelaBairro Terminal - Global Solution 2026/2 (CitizenTech) - FIAP 1TDS
Computational Thinking Using Python

Integrantes (turma 1TDSPV):
    RM573982 - Leonardo Afonço Sousa
    RM569259 - Syang Cristina Gomes Souza
    RM573559 - Matheus Jones Sousa de Freitas
    RM569023 - Vitor Gonçalves de Souza
    RM572364 - Joao Machado Nascimento

Ferramenta de triagem para o gestor da prefeitura: registra e apoia problemas de
zeladoria urbana, controla o status, calcula a prioridade (RN10) e os atrasos (RN11).
Funciona sem internet (dados em data/ocorrencias.json) e, se houver conexão, pode
sincronizar com o Oracle da FIAP, consultar o ViaCEP e chamar a API de IA do grupo.

Execução:  python main.py      (veja o README.md)
"""
import sys
from datetime import date

from api_externa import busca_cep, prever_ia
from dados import (ARQ_DADOS, ARQ_EXPORTACAO, ARQ_RELATORIO, carrega_dados, carrega_env,
                   envia_para_oracle, exporta_json_api, importa_do_oracle, salva_dados,
                   salva_relatorio, testa_oracle)
from regras import (BAIRROS, CATEGORIAS, COMENTARIO_MAX, DESC_MAX, DESC_MIN, ENDERECO_MAX,
                    NOME_MAX, STATUS, STATUS_ABERTOS, apoia, atualiza_status, busca_bairro,
                    busca_categoria, busca_ocorrencia, busca_similares, calcula_prioridade,
                    classe_prioridade, conta_por_bairro, conta_por_status, cria_ocorrencia,
                    detalha_prioridade, dias_em_aberto, esta_atrasada, monta_fila,
                    ordena_por_prioridade, primeiro_nome, tempo_medio)
from util import (LARGURA, aviso, caixa, data_para_br, erro, le_email, le_inteiro, le_sim_nao,
                  le_texto, linha, mostra_campo, mostra_tabela, pausa, sucesso, titulo)

# Colunas das tabelas: (chave, título, largura)
COLUNAS_LISTA = [("id", "ID", 3), ("categoria", "Categoria", 22), ("bairro", "Bairro", 15),
                 ("status", "Status", 12), ("apoios", "Apo", 4), ("dias", "Dias", 4),
                 ("autor", "Autor", 9)]
COLUNAS_FILA = [("pos", "Pos", 3), ("id", "ID", 3), ("categoria", "Categoria", 19),
                ("bairro", "Bairro", 14), ("apoios", "Apo", 4), ("dias", "Dias", 4),
                ("pontos", "Pts", 4), ("classe", "Prior.", 6), ("alerta", "Alerta", 8)]
COLUNAS_ATRASADAS = [("id", "ID", 3), ("categoria", "Categoria", 22), ("bairro", "Bairro", 15),
                     ("abertura", "Abertura", 10), ("dias", "Dias", 4), ("prazo", "Prazo", 5),
                     ("atraso", "Atraso", 6)]
COLUNAS_BAIRROS = [("bairro", "Bairro", 20), ("abertas", "Abertas", 7), ("atrasadas", "Atrasadas", 9),
                   ("resolvidas", "Resolvidas", 10), ("media", "Tempo médio", 11)]


# ================================================================= apoio às telas
def linhas_lista(ocorrencias: list, hoje: date) -> list:
    """Converte as ocorrências em linhas simples (dicionários) para mostrar na tabela."""
    linhas = []
    for oc in ocorrencias:
        linhas.append({
            "id": oc["id"],
            "categoria": oc["categoria"],
            "bairro": oc["bairro"],
            "status": oc["status"],
            "apoios": len(oc["apoiadores"]),
            "dias": dias_em_aberto(oc, hoje),
            "autor": primeiro_nome(oc["autor_nome"]),  # RN13
        })
    return linhas


def escolhe_categoria() -> tuple:
    """Mostra as 8 categorias (tabela 6.4) e devolve a tupla da escolhida."""
    print("\n  Categorias:")
    for cd, nome, orgao, prazo, gravidade in CATEGORIAS:
        print(f"   [{cd}] {nome:<35} prazo {prazo:>2} dias  gravidade {gravidade}")
    numero = le_inteiro("Escolha a categoria", 1, len(CATEGORIAS))
    return CATEGORIAS[numero - 1]


def escolhe_bairro() -> tuple:
    """Mostra os bairros e devolve a tupla do escolhido."""
    print("\n  Bairros:")
    for cd, nome, subprefeitura in BAIRROS:
        print(f"   [{cd:>2}] {nome:<20} subprefeitura: {subprefeitura}")
    numero = le_inteiro("Escolha o bairro", 1, len(BAIRROS))
    return BAIRROS[numero - 1]


def le_ocorrencia(ocorrencias: list):
    """Pergunta um ID e devolve a ocorrência (ou None, já avisando que não existe)."""
    numero = le_inteiro("ID da ocorrência", 1, 999999)
    ocorrencia = busca_ocorrencia(ocorrencias, numero)
    if ocorrencia is None:
        erro(f"Não existe ocorrência com o ID {numero}.")
    return ocorrencia


def le_endereco() -> str:
    """Lê o endereço de referência (RN03); se o usuário quiser, preenche a rua pelo ViaCEP."""
    print("\n  Digite o CEP para preencher a rua (ViaCEP) ou ENTER para digitar à mão.")
    cep = input("  CEP: ").strip()
    rua = ""
    if cep != "":
        dados, problema = busca_cep(cep)
        if dados is None:
            aviso(problema)
        elif dados["logradouro"] == "":
            aviso("Esse CEP não tem rua cadastrada; digite o endereço à mão.")
        else:
            sucesso(f"CEP encontrado: {dados['logradouro']}, {dados['bairro']} - {dados['cidade']}/{dados['uf']}")
            rua = dados["logradouro"]
    if rua != "":
        complemento = le_texto("Número aproximado e ponto de referência", 1, 100)
        return f"{rua}, {complemento}"[:ENDERECO_MAX]  # RN03: no máximo 200 caracteres
    return le_texto("Endereço de referência (rua, número, ponto de referência)", 3, ENDERECO_MAX)


# ================================================================= 1 - Registrar (RN01, RN03, RN04, RN07, RN12)
def apoiar_da_sugestao(similares: list, email: str) -> str:
    """
    RN07: oferece apoiar uma ocorrência parecida (é sugestão, não bloqueio).

    Devolve "apoiou" (não precisa criar outra), "criar" (o usuário quer uma nova)
    ou "voltar" (desistiu do registro). Se o apoio for recusado pela RN08, pergunta
    de novo em vez de criar uma ocorrência duplicada sem avisar.
    """
    print("\n  Já existem ocorrências abertas da mesma categoria neste bairro:\n")
    mostra_tabela(linhas_lista(similares, date.today()), COLUNAS_LISTA)
    print("\n  Apoiar uma delas é melhor do que criar outra igual (fila mais justa).")
    resultado = ""
    while resultado == "":
        numero = le_inteiro("ID para apoiar (0 = criar uma nova mesmo assim)", 0, 999999)
        if numero == 0:
            resultado = "criar"
        else:
            escolhida = busca_ocorrencia(similares, numero)
            if escolhida is None:
                aviso("Esse ID não está na lista acima.")
            else:
                deu_certo, texto = apoia(escolhida, email)
                if deu_certo:
                    sucesso(texto)
                    resultado = "apoiou"
                else:
                    erro(texto)  # RN08 recusou (é o autor ou já apoia)
                    if le_sim_nao("Quer registrar uma ocorrência nova mesmo assim?"):
                        resultado = "criar"
                    else:
                        resultado = "voltar"
    return resultado


def registra_ocorrencia(ocorrencias: list) -> None:
    """Opção 1: registra uma ocorrência nova (RN01, RN03, RN04, RN07 e RN12)."""
    titulo("Registrar ocorrência")
    hoje = date.today()
    # Quem registra (RN01 e RN02: o e-mail identifica o cidadão)
    nome = le_texto("Seu nome completo", 3, NOME_MAX)
    email = le_email("Seu e-mail")
    categoria = escolhe_categoria()
    bairro = escolhe_bairro()

    # RN07: antes de criar, sugere apoiar uma ocorrência igual (sugestão, não bloqueio)
    similares = busca_similares(ocorrencias, categoria[1], bairro[1])
    if len(similares) > 0:
        if apoiar_da_sugestao(similares, email) != "criar":
            return  # apoiou uma existente ou desistiu: não cria outra

    # RN03: endereço (até 200) e descrição (10 a 500) obrigatórios
    endereco = le_endereco()
    descricao = le_texto(f"Descrição do problema ({DESC_MIN} a {DESC_MAX} caracteres)", DESC_MIN, DESC_MAX)

    # Previsão da IA (opcional). RN12: se falhar, a ocorrência é criada sem previsão.
    prazo, risco, problema = prever_ia(categoria[1], bairro[2], hoje.month, hoje.weekday())
    if prazo is None:
        aviso(problema)

    dados = {"descricao": descricao, "endereco": endereco, "categoria": categoria[1],
             "bairro": bairro[1], "autor_nome": nome, "autor_email": email,
             "prazo_previsto": prazo, "risco_atraso": risco}
    nova = cria_ocorrencia(ocorrencias, dados, hoje)  # RN04: nasce ABERTA
    ocorrencias.append(nova)

    sucesso(f"Ocorrência #{nova['id']} registrada com status {nova['status']}.")
    pontos = calcula_prioridade(nova, hoje)
    print()
    mostra_campo("Órgão responsável", categoria[2])
    mostra_campo("Prazo de referência", f"{categoria[3]} dias")
    mostra_campo("Prioridade inicial", f"{pontos} pontos ({classe_prioridade(pontos)})")
    if prazo is not None:
        mostra_campo("Previsão da IA", f"{prazo} dias, risco de atraso = {risco}")


# ================================================================= 2 - Apoiar (RN08)
def apoiar_ocorrencia(ocorrencias: list) -> None:
    """Opção 2: registra o apoio de um cidadão a uma ocorrência em aberto (RN08)."""
    titulo("Apoiar ocorrência")
    hoje = date.today()
    abertas = []
    for oc in ocorrencias:
        if oc["status"] in STATUS_ABERTOS:
            abertas.append(oc)
    mostra_tabela(linhas_lista(abertas, hoje), COLUNAS_LISTA)
    print()
    email = le_email("Seu e-mail")
    ocorrencia = le_ocorrencia(ocorrencias)
    if ocorrencia is None:
        return
    deu_certo, texto = apoia(ocorrencia, email)
    if deu_certo:
        sucesso(texto)
    else:
        erro(texto)


# ================================================================= 3 - Atualizar status (RN05, RN06)
def atualizar_status(ocorrencias: list) -> None:
    """Opção 3: muda o status pelo submenu, validando a transição (RN05 e RN06)."""
    titulo("Atualizar status")
    ocorrencia = le_ocorrencia(ocorrencias)
    if ocorrencia is None:
        return
    atual = ocorrencia["status"]
    print(f"\n  Ocorrência #{ocorrencia['id']} - {ocorrencia['categoria']} ({ocorrencia['bairro']})")
    print(f"  Status atual: {atual}")
    if atual not in STATUS_ABERTOS:
        aviso(f"RN05: {atual} é um status final; não pode mais mudar.")
        return

    # Submenu do novo status (match-case)
    print("\n  Novo status:")
    print("   [1] EM_ANDAMENTO")
    print("   [2] RESOLVIDA")
    print("   [3] CANCELADA")
    print("   [0] Voltar")
    escolha = le_inteiro("Escolha", 0, 3)
    match escolha:
        case 1:
            novo = "EM_ANDAMENTO"
        case 2:
            novo = "RESOLVIDA"
        case 3:
            novo = "CANCELADA"
        case _:
            return
    comentario = le_texto("Comentário (opcional)", 0, COMENTARIO_MAX)
    deu_certo, texto = atualiza_status(ocorrencia, novo, comentario, date.today())
    if deu_certo:
        sucesso(texto)
        if novo == "RESOLVIDA":
            print(f"  Data de resolução preenchida: {data_para_br(ocorrencia['data_resolucao'])} (RN06)")
    else:
        erro(texto)
        print("  Transições permitidas: ABERTA -> EM_ANDAMENTO ou CANCELADA;")
        print("                         EM_ANDAMENTO -> RESOLVIDA ou CANCELADA.")


# ================================================================= 4 - Fila de prioridade (RN10)
def alerta_da_ocorrencia(oc: dict, hoje: date) -> str:
    """Texto curto da coluna Alerta da fila."""
    if esta_atrasada(oc, hoje):
        return "ATRASADA"
    elif oc["risco_atraso"] == "S":
        return "RISCO IA"
    return "-"


def mostra_calculo(oc: dict, hoje: date) -> None:
    """Mostra passo a passo como a pontuação da RN10 foi calculada."""
    gravidade, apoios, dias, risco, total = detalha_prioridade(oc, hoje)
    qtd_apoios = len(oc["apoiadores"])
    print(f"\n  Ocorrência #{oc['id']} - {oc['categoria']}")
    print(f"    Gravidade x 10                  = {gravidade:>3}")
    print(f"    Apoios ({qtd_apoios}) x 2, máximo 20 apoios = {apoios:>3}")
    print(f"    Dias em aberto, máximo 30       = {dias:>3}   ({dias_em_aberto(oc, hoje)} dias)")
    print(f"    +15 se risco IA = S ou atrasada = {risco:>3}")
    print(f"    {'-' * 36}")
    print(f"    Total                           = {total:>3}   -> {classe_prioridade(total)}")


def fila_prioridade(ocorrencias: list) -> None:
    """Opção 4: mostra a fila ordenada pela pontuação da RN10 e o cálculo de cada uma."""
    titulo("Fila de prioridade (RN10)")
    hoje = date.today()
    fila = monta_fila(ocorrencias, hoje)
    ordena_por_prioridade(fila)
    linhas = []
    posicao = 1
    for pontos, oc in fila:
        linhas.append({"pos": posicao, "id": oc["id"], "categoria": oc["categoria"],
                       "bairro": oc["bairro"], "apoios": len(oc["apoiadores"]),
                       "dias": dias_em_aberto(oc, hoje), "pontos": pontos,
                       "classe": classe_prioridade(pontos), "alerta": alerta_da_ocorrencia(oc, hoje)})
        posicao = posicao + 1
    mostra_tabela(linhas, COLUNAS_FILA)
    print("\n  Pontos = gravidade x 10 + apoios x 2 (até 20) + dias (até 30)")
    print("           + 15 se o risco de atraso for S ou se estiver atrasada")
    print("  ALTA: 70 ou mais | MEDIA: 40 a 69 | BAIXA: menos de 40")
    if len(fila) == 0:
        return
    print()
    numero = le_inteiro("Ver o cálculo de qual ID? (0 = voltar)", 0, 999999)
    while numero != 0:
        ocorrencia = busca_ocorrencia(ocorrencias, numero)
        if ocorrencia is None or ocorrencia["status"] not in STATUS_ABERTOS:
            aviso("Esse ID não está na fila (só ABERTA e EM_ANDAMENTO têm prioridade).")
        else:
            mostra_calculo(ocorrencia, hoje)
        print()
        numero = le_inteiro("Ver o cálculo de qual ID? (0 = voltar)", 0, 999999)


# ================================================================= 5 - Relatório por bairro
def relatorio_bairro(ocorrencias: list) -> None:
    """Opção 5: abertas, atrasadas e tempo médio por bairro; salva o relatório em .txt."""
    titulo("Relatório por bairro")
    hoje = date.today()
    bairros = conta_por_bairro(ocorrencias, hoje)
    linhas = []
    linhas_txt = ["ZELABAIRRO - RELATORIO POR BAIRRO", f"Gerado em {hoje.strftime('%d/%m/%Y')}", "",
                  f"{'Bairro':<20} {'Abertas':>7} {'Atrasadas':>9} {'Resolvidas':>10} {'Tempo medio (dias)':>19}",
                  "-" * 70]
    total_abertas = 0
    total_atrasadas = 0
    for nome in bairros:
        dados = bairros[nome]
        media = tempo_medio(dados["soma_dias"], dados["resolvidas"])
        texto_media = "-"
        if dados["resolvidas"] > 0:
            texto_media = f"{media:.1f}"
        else:
            media = None  # ainda não há resolvidas neste bairro
        linhas.append({"bairro": nome, "abertas": dados["abertas"], "atrasadas": dados["atrasadas"],
                       "resolvidas": dados["resolvidas"], "media": media})
        linhas_txt.append(f"{nome:<20} {dados['abertas']:>7} {dados['atrasadas']:>9} "
                          f"{dados['resolvidas']:>10} {texto_media:>19}")
        total_abertas = total_abertas + dados["abertas"]
        total_atrasadas = total_atrasadas + dados["atrasadas"]
    mostra_tabela(linhas, COLUNAS_BAIRROS)
    print(f"\n  Em aberto: {total_abertas} | Atrasadas: {total_atrasadas}")
    print("  Tempo médio = média de dias das ocorrências RESOLVIDAS do bairro.")
    linhas_txt.append("-" * 70)
    linhas_txt.append(f"Total em aberto: {total_abertas} | Atrasadas: {total_atrasadas}")
    try:
        salva_relatorio(ARQ_RELATORIO, linhas_txt)
        sucesso("Relatório salvo em relatorios/relatorio_bairros.txt")
    except OSError as falha:
        erro(f"Não foi possível salvar o relatório: {falha}")


# ================================================================= 6 - Atrasadas (RN11)
def listar_atrasadas(ocorrencias: list) -> None:
    """Opção 6: lista as ocorrências em aberto que passaram do prazo da categoria (RN11)."""
    titulo("Ocorrências atrasadas (RN11)")
    hoje = date.today()
    linhas = []
    for oc in ocorrencias:
        if oc["status"] in STATUS_ABERTOS and esta_atrasada(oc, hoje):
            prazo = busca_categoria(oc["categoria"])[3]
            dias = dias_em_aberto(oc, hoje)
            linhas.append({"id": oc["id"], "categoria": oc["categoria"], "bairro": oc["bairro"],
                           "abertura": data_para_br(oc["data_abertura"]), "dias": dias,
                           "prazo": prazo, "atraso": dias - prazo})
    if len(linhas) == 0:
        sucesso("Nenhuma ocorrência em aberto está atrasada.")
        return
    mostra_tabela(linhas, COLUNAS_ATRASADAS)
    print("\n  Atrasada = dias em aberto maior que o prazo de referência da categoria.")


# ================================================================= 7 - Consultar (submenu)
def mostra_detalhe(oc: dict) -> None:
    """Tela completa de uma ocorrência, com o histórico de atualizações."""
    hoje = date.today()
    categoria = busca_categoria(oc["categoria"])
    bairro = busca_bairro(oc["bairro"])
    pontos = calcula_prioridade(oc, hoje)
    titulo(f"Ocorrência #{oc['id']}")
    mostra_campo("Status", oc["status"])
    mostra_campo("Categoria", f"{oc['categoria']} (gravidade {categoria[4]})")
    mostra_campo("Órgão", categoria[2])
    mostra_campo("Bairro", f"{oc['bairro']} - subprefeitura {bairro[2]}")
    mostra_campo("Endereço", oc["endereco"])
    mostra_campo("Descrição", oc["descricao"])
    mostra_campo("Autor", primeiro_nome(oc["autor_nome"]))  # RN13
    mostra_campo("Abertura", data_para_br(oc["data_abertura"]))
    mostra_campo("Resolução", data_para_br(oc["data_resolucao"]))
    mostra_campo("Dias em aberto", f"{dias_em_aberto(oc, hoje)} (prazo de referência: {categoria[3]})")
    if esta_atrasada(oc, hoje):
        mostra_campo("Atrasada", "SIM")
    else:
        mostra_campo("Atrasada", "não")
    if oc["prazo_previsto"] is None:
        mostra_campo("Previsão da IA", "indisponível")
    else:
        mostra_campo("Previsão da IA", f"{oc['prazo_previsto']} dias, risco de atraso = {oc['risco_atraso']}")
    mostra_campo("Apoios", len(oc["apoiadores"]))
    if pontos is None:
        mostra_campo("Prioridade", "- (ocorrência encerrada)")
    else:
        mostra_campo("Prioridade", f"{pontos} pontos ({classe_prioridade(pontos)})")
    print("\n  Histórico:")
    if len(oc["historico"]) == 0:
        print("   (nenhuma atualização)")
    for item in oc["historico"]:
        texto = f"   {data_para_br(item['data'])}  {item['de']} -> {item['para']}"
        if item["comentario"]:
            texto = f"{texto}  | {item['comentario']}"
        print(f"{texto}")


def menu_consultar(ocorrencias: list) -> None:
    """Opção 7: submenu de consulta (listar, filtrar por status e ver detalhe)."""
    opcao = -1
    while opcao != 0:
        print()
        caixa(["CONSULTAR OCORRÊNCIAS".center(LARGURA - 4), "-" * (LARGURA - 4),
               "[1] Listar todas", "[2] Filtrar por status", "[3] Ver detalhes e histórico",
               "[0] Voltar"])
        opcao = le_inteiro("Escolha uma opção", 0, 3)
        hoje = date.today()
        if opcao == 1:
            titulo("Todas as ocorrências")
            mostra_tabela(linhas_lista(ocorrencias, hoje), COLUNAS_LISTA)
            pausa()
        elif opcao == 2:
            print("\n  Status: [1] ABERTA  [2] EM_ANDAMENTO  [3] RESOLVIDA  [4] CANCELADA")
            status = STATUS[le_inteiro("Escolha o status", 1, 4) - 1]
            filtradas = []
            for oc in ocorrencias:
                if oc["status"] == status:
                    filtradas.append(oc)
            titulo(f"Ocorrências com status {status}")
            mostra_tabela(linhas_lista(filtradas, hoje), COLUNAS_LISTA)
            pausa()
        elif opcao == 3:
            ocorrencia = le_ocorrencia(ocorrencias)
            if ocorrencia is not None:
                mostra_detalhe(ocorrencia)
            pausa()


# ================================================================= 8 - Integrações (submenu)
def consulta_cep() -> None:
    """Submenu 8.5: consulta avulsa de um CEP na API pública ViaCEP."""
    titulo("Consultar CEP (ViaCEP)")
    cep = le_texto("CEP com 8 números (ENTER para voltar)", 0, 9)
    if cep == "":
        return
    dados, problema = busca_cep(cep)
    if dados is None:
        erro(problema)
        return
    print()
    mostra_campo("CEP", dados["cep"])
    mostra_campo("Rua", dados["logradouro"])
    mostra_campo("Bairro", dados["bairro"])
    mostra_campo("Cidade/UF", f"{dados['cidade']}/{dados['uf']}")


def mostra_avisos(avisos: list) -> None:
    """Mostra, um por linha, os avisos devolvidos pelas operações com o Oracle."""
    for texto in avisos:
        print(f"   - {texto}")


def menu_integracoes(ocorrencias: list) -> None:
    """Opção 8: submenu de integrações opcionais (Oracle, exportação para o front e ViaCEP)."""
    opcao = -1
    while opcao != 0:
        print()
        caixa(["INTEGRAÇÕES".center(LARGURA - 4), "-" * (LARGURA - 4),
               "[1] Testar conexão com o Oracle", "[2] Importar do Oracle (SELECT)",
               "[3] Enviar para o Oracle (INSERT/UPDATE)",
               "[4] Exportar JSON no formato da API/front-end",
               "[5] Consultar CEP (API ViaCEP)", "[0] Voltar"])
        opcao = le_inteiro("Escolha uma opção", 0, 5)
        hoje = date.today()
        match opcao:
            case 1:
                print("\n  Conectando ao Oracle FIAP...")
                deu_certo, mensagens = testa_oracle()
                for texto in mensagens:
                    if deu_certo:
                        sucesso(texto)
                    else:
                        erro(texto)
                pausa()
            case 2:
                print("\n  Conectando ao Oracle FIAP...")
                novas, atualizadas, avisos = importa_do_oracle(ocorrencias, hoje)
                if novas + atualizadas > 0:
                    sucesso(f"Importação concluída: {novas} nova(s) e {atualizadas} atualizada(s).")
                else:
                    aviso("Nada novo para importar.")
                mostra_avisos(avisos)
                pausa()
            case 3:
                aviso("O Oracle é o mesmo banco da API Java e do site: o que for enviado "
                      "aparece para todos. Não envie dados de teste.")
                if le_sim_nao("Enviar as ocorrências do JSON para o Oracle?"):
                    # RN06 e RN16: a atualização fica registrada no nome do gestor que enviou
                    email_gestor = le_email("E-mail do gestor (cadastrado no site)")
                    print("\n  Conectando ao Oracle FIAP...")
                    novas, atualizadas, apoios, avisos = envia_para_oracle(ocorrencias, email_gestor)
                    resumo = (f"Envio concluído: {novas} nova(s), {atualizadas} com status atualizado, "
                              f"{apoios} apoio(s).")
                    if novas + atualizadas + apoios == 0 and len(avisos) > 0:
                        aviso(resumo)  # nada foi gravado: os avisos abaixo explicam o motivo
                    else:
                        sucesso(resumo)
                    mostra_avisos(avisos)
                pausa()
            case 4:
                try:
                    total = exporta_json_api(ARQ_EXPORTACAO, ocorrencias, hoje)
                    sucesso(f"{total} ocorrências exportadas em exports/ocorrencias_api.json")
                except OSError as falha:
                    erro(f"Não foi possível gravar o arquivo: {falha}")
                pausa()
            case 5:
                consulta_cep()
                pausa()


# ================================================================= menu principal
def menu_principal(ocorrencias: list) -> int:
    """Desenha o menu principal e devolve a opção escolhida (0 a 8)."""
    contagem = conta_por_status(ocorrencias)
    em_aberto = contagem["ABERTA"] + contagem["EM_ANDAMENTO"]
    print()
    caixa([
        "ZELABAIRRO TERMINAL".center(LARGURA - 4),
        "Zeladoria urbana colaborativa com priorização inteligente".center(LARGURA - 4),
        "-" * (LARGURA - 4),
        f"Hoje: {date.today().strftime('%d/%m/%Y')}   Ocorrências: {len(ocorrencias)}   Em aberto: {em_aberto}",
        "-" * (LARGURA - 4),
        "[1] Registrar ocorrência",
        "[2] Apoiar ocorrência",
        "[3] Atualizar status",
        "[4] Fila de prioridade",
        "[5] Relatório por bairro",
        "[6] Ocorrências atrasadas",
        "[7] Consultar ocorrências  >",
        "[8] Integrações (Oracle, front-end, ViaCEP)  >",
        "[0] Sair e salvar",
    ])
    return le_inteiro("Escolha uma opção", 0, 8)


def main() -> None:
    """Carrega os dados, roda o menu principal até escolher 0 e salva ao sair."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # acentos corretos em qualquer terminal
    carrega_env()
    ocorrencias = carrega_dados(ARQ_DADOS)
    try:
        opcao = menu_principal(ocorrencias)
        while opcao != 0:
            match opcao:
                case 1:
                    registra_ocorrencia(ocorrencias)
                case 2:
                    apoiar_ocorrencia(ocorrencias)
                case 3:
                    atualizar_status(ocorrencias)
                case 4:
                    fila_prioridade(ocorrencias)
                case 5:
                    relatorio_bairro(ocorrencias)
                case 6:
                    listar_atrasadas(ocorrencias)
                case 7:
                    menu_consultar(ocorrencias)
                case 8:
                    menu_integracoes(ocorrencias)
                case _:
                    aviso("Opção inválida.")
            salva_dados(ARQ_DADOS, ocorrencias)  # grava depois de cada operação (não perde dados)
            if opcao in (1, 2, 3, 4, 5, 6):
                pausa()
            opcao = menu_principal(ocorrencias)
    except (KeyboardInterrupt, EOFError):
        print("\n\n  Programa interrompido; os dados serão salvos.")
    salva_dados(ARQ_DADOS, ocorrencias)
    print()
    linha("=")
    print(f"{'Dados salvos em data/ocorrencias.json. Até logo!':^{LARGURA}}")
    linha("=")


if __name__ == "__main__":
    main()
