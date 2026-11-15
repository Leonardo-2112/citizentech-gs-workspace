"""Gera o Documento Base do projeto ZelaBairro (GS 2026/2 - CitizenTech).

Uso: python gerar_documento_base.py  (requer reportlab)
Saida: ZelaBairro-Documento-Base.pdf na mesma pasta deste script.
"""
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, ListFlowable, ListItem,
                                NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

VERSAO = "1.3"
DATA = "15/11/2026"
SAIDA = Path(__file__).with_name("ZelaBairro-Documento-Base.pdf")

FONTES = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FONTES + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTES + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONTES + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTES + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic",
                              boldItalic="Sans-Bold")

VERDE = colors.HexColor("#0F5C4D")
VERDE_CLARO = colors.HexColor("#E3F1EC")
AMBAR_CLARO = colors.HexColor("#FDF3DC")
AMBAR = colors.HexColor("#B7791F")
VERMELHO_CLARO = colors.HexColor("#FBE6E4")
VERMELHO = colors.HexColor("#A33A2E")
CINZA = colors.HexColor("#5B6470")
CINZA_CLARO = colors.HexColor("#F2F4F6")
LINHA = colors.HexColor("#CBD2D9")

ST = {
    "corpo": ParagraphStyle("corpo", fontName="Sans", fontSize=9.5, leading=14, spaceAfter=6),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=17, leading=22, textColor=VERDE,
                         spaceBefore=4, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=12, leading=16, textColor=VERDE,
                         spaceBefore=10, spaceAfter=5),
    "h3": ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10, leading=14, spaceBefore=6,
                         spaceAfter=3),
    "cel": ParagraphStyle("cel", fontName="Sans", fontSize=8.3, leading=11),
    "cel_b": ParagraphStyle("cel_b", fontName="Sans-Bold", fontSize=8.3, leading=11,
                            textColor=colors.white),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=7.6, leading=10),
    "toc1": ParagraphStyle("toc1", fontName="Sans", fontSize=10, leading=17, leftIndent=0),
}


def p(texto, estilo="corpo"):
    return Paragraph(texto, ST[estilo])


def h1(texto):
    par = Paragraph(texto, ST["h1"])
    par._toc = texto
    return par


def h2(texto):
    return Paragraph(texto, ST["h2"])


def h3(texto):
    return Paragraph(texto, ST["h3"])


def bullets(itens, numerado=False):
    return ListFlowable(
        [ListItem(p(i), leftIndent=12) for i in itens],
        bulletType="1" if numerado else "bullet", start="1" if numerado else "•",
        leftIndent=14, bulletFontName="Sans", bulletFontSize=9)


def tabela(linhas, larguras, destaque_primeira_coluna=False):
    dados = [[Paragraph(str(c), ST["cel_b"]) for c in linhas[0]]]
    for linha in linhas[1:]:
        dados.append([Paragraph(str(c), ST["cel"]) for c in linha])
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), VERDE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINHA),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA_CLARO]),
    ]
    if destaque_primeira_coluna:
        estilo.append(("FONTNAME", (0, 1), (0, -1), "Sans-Bold"))
    t.setStyle(TableStyle(estilo))
    return t


def caixa(texto, tipo="info"):
    fundo, borda = {"info": (VERDE_CLARO, VERDE), "atencao": (AMBAR_CLARO, AMBAR),
                    "risco": (VERMELHO_CLARO, VERMELHO)}[tipo]
    t = Table([[p(texto)]], colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fundo),
        ("LINEBEFORE", (0, 0), (0, -1), 3, borda),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def codigo(texto):
    t = Table([[Preformatted(texto.strip("\n"), ST["code"])]], colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.4, LINHA),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def diagrama_integracao():
    d = Drawing(17 * cm, 6.4 * cm)

    def caixa_d(x, y, w, h, titulo, sub, cor):
        d.add(Rect(x, y, w, h, rx=6, ry=6, fillColor=cor, strokeColor=VERDE, strokeWidth=1))
        d.add(String(x + w / 2, y + h - 16, titulo, fontName="Sans-Bold", fontSize=9,
                     textAnchor="middle", fillColor=VERDE))
        linha_y = y + h - 30
        for linha in sub.split("\n"):
            d.add(String(x + w / 2, linha_y, linha, fontName="Sans", fontSize=7.3,
                         textAnchor="middle", fillColor=CINZA))
            linha_y -= 10

    def seta(x1, y1, x2, y2, rotulo, dy=4):
        d.add(Line(x1, y1, x2, y2, strokeColor=CINZA, strokeWidth=1.2))
        if x2 > x1:
            d.add(Polygon([x2, y2, x2 - 6, y2 + 3, x2 - 6, y2 - 3], fillColor=CINZA,
                          strokeColor=CINZA))
        else:
            d.add(Polygon([x2, y2, x2 + 3, y2 + 6, x2 - 3, y2 + 6], fillColor=CINZA,
                          strokeColor=CINZA))
        d.add(String((x1 + x2) / 2, (y1 + y2) / 2 + dy, rotulo, fontName="Sans", fontSize=6.8,
                     textAnchor="middle", fillColor=CINZA))

    caixa_d(0, 100, 110, 70, "Front-end", "React + Vite + TS\nTailwind · Vercel\nsó Fetch API",
            VERDE_CLARO)
    caixa_d(170, 100, 120, 70, "API Java", "Spring Boot · JDBC\nDocker · Render", VERDE_CLARO)
    caixa_d(350, 100, 125, 70, "Oracle FIAP", "9 tabelas tb_*\nsequences sq_tb_*", VERDE_CLARO)
    caixa_d(170, 5, 120, 62, "API de IA", "Flask · 2 modelos\n.joblib", AMBAR_CLARO)
    caixa_d(350, 5, 125, 62, "App Python", "menu no terminal\ndados em JSON local", AMBAR_CLARO)
    seta(110, 135, 170, 135, "HTTP + JSON")
    seta(290, 135, 350, 135, "JDBC")
    seta(230, 100, 230, 67, "", 0)
    d.add(String(236, 82, "POST /prever/* (desejável)", fontName="Sans", fontSize=6.8,
                 fillColor=CINZA))
    d.add(String(412, 75, "independente (sem rede)", fontName="Sans", fontSize=6.8,
                 textAnchor="middle", fillColor=CINZA))
    return d


class Documento(BaseDocTemplate):
    def __init__(self, arquivo):
        super().__init__(str(arquivo), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                         topMargin=2 * cm, bottomMargin=2 * cm,
                         title="ZelaBairro - Documento Base do Projeto",
                         author="Grupo ZelaBairro - 1TDS FIAP",
                         subject="Global Solution 2026/2 - CitizenTech")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("capa", [frame], onPage=self._capa),
                               PageTemplate("normal", [frame], onPage=self._rodape)])

    def afterFlowable(self, flowable):
        if hasattr(flowable, "_toc"):
            self.notify("TOCEntry", (0, flowable._toc, self.page))

    def _capa(self, canv, doc):
        canv.saveState()
        canv.setFillColor(VERDE)
        canv.rect(0, A4[1] - 9 * cm, A4[0], 9 * cm, fill=1, stroke=0)
        canv.restoreState()

    def _rodape(self, canv, doc):
        canv.saveState()
        canv.setFont("Sans", 7.5)
        canv.setFillColor(CINZA)
        canv.drawString(2 * cm, 1.2 * cm, f"ZelaBairro · Documento Base v{VERSAO} · {DATA}")
        canv.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
        canv.setStrokeColor(LINHA)
        canv.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
        canv.restoreState()


def capa():
    branco = ParagraphStyle("cb", fontName="Sans", fontSize=11, leading=15,
                            textColor=colors.white)
    titulo = ParagraphStyle("ct", fontName="Sans-Bold", fontSize=34, leading=40,
                            textColor=colors.white)
    return [
        Spacer(1, 0.6 * cm),
        Paragraph("GLOBAL SOLUTION 2026/2 · CITIZENTECH · FIAP 1TDS", branco),
        Spacer(1, 0.5 * cm),
        Paragraph("ZelaBairro", titulo),
        Paragraph("Zeladoria urbana colaborativa com priorização inteligente", branco),
        Spacer(1, 3.6 * cm),
        Paragraph("Documento Base do Projeto", ST["h1"]),
        p("Fonte única da verdade para todo o grupo: contexto, problema, solução, regras de "
          "negócio, modelo de dados e contratos entre as seis disciplinas."),
        Spacer(1, 0.4 * cm),
        tabela([["Campo", "Valor"],
                ["Versão", f"{VERSAO} — {DATA}"],
                ["Status", "Em desenvolvimento. IA pronta; decisões a confirmar e pendências na "
                           "seção 14"],
                ["Entrega da GS", "19/11/2026 até 23h55, no Portal do Aluno (sem prorrogação)"],
                ["Cadastro do grupo", "até 13/11/2026"],
                ["Integrantes (turma 1TDSPV)", "RM 573982 – Leonardo Afonço Sousa<br/>"
                                               "RM 569259 – Syang Cristina Gomes Souza<br/>"
                                               "RM 573559 – Matheus Jones Sousa de Freitas<br/>"
                                               "RM 569023 – Vitor Goncalves de Souza<br/>"
                                               "RM 572364 – Joao Machado Nascimento"]],
               [5, 12], destaque_primeira_coluna=True),
        Spacer(1, 0.6 * cm),
        caixa("<b>Regra de ouro:</b> se uma regra, nome de tabela, campo ou rota não está neste "
              "documento, ela ainda não existe. Antes de inventar, proponha no grupo e atualize o "
              "documento (nova versão). Em caso de conflito entre o código e este documento, "
              "vale o documento até ele ser alterado."),
        NextPageTemplate("normal"),
        PageBreak(),
    ]


def conteudo():
    s = []
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"]]
    toc.dotsMinLevel = 0
    s += [Paragraph("Sumário", ST["h1"]), toc, PageBreak()]

    # 1 ------------------------------------------------------------------
    s += [h1("1. Como usar este documento")]
    s += [p("Este documento existe para que as cinco pessoas do grupo construam <b>a mesma "
            "solução</b> em seis disciplinas diferentes, sem que cada uma invente suas próprias "
            "regras. Ele não substitui os documentos de entrega de cada disciplina: é a base de "
            "onde todos eles copiam o problema, as regras e os nomes."),
          bullets([
              "<b>Leia inteiro uma vez.</b> Depois, consulte a seção da sua disciplina e as "
              "seções 5 (regras) e 6 (banco), que valem para todos.",
              "<b>Nomes são contrato.</b> Tabelas, colunas, status, rotas e campos JSON devem ser "
              "escritos exatamente como aqui. Um nome diferente quebra a integração.",
              "<b>Mudanças:</b> quem precisar mudar algo avisa no grupo, todos concordam, o "
              "documento ganha nova versão (1.1, 1.2...) e o histórico é anotado na seção 15.",
              "<b>Textos para as entregas:</b> podem copiar e adaptar trechos deste documento "
              "nos PDFs de cada disciplina, sempre revisando e entendendo o que está escrito "
              "(regra da FIAP sobre IA generativa).",
          ])]

    # 2 ------------------------------------------------------------------
    s += [h1("2. Contexto da Global Solution")]
    s += [p("A Global Solution 2026/2 tem o tema <b>CitizenTech: tecnologia com o cidadão no "
            "centro da inovação</b>. O grupo deve escolher um problema real do cotidiano e criar "
            "<b>uma única solução</b> que serve de base para as entregas das seis disciplinas. A "
            "GS vale 60% da nota do semestre."),
          tabela([["Data", "Marco"],
                  ["04/11", "Kickoff"],
                  ["13/11", "Prazo final para cadastrar o grupo (sem cadastro, o grupo não "
                            "aparece no portal de entrega)"],
                  ["19/11, 23h55", "Entrega de todas as disciplinas no Portal do Aluno, sem "
                                   "prorrogação. Um .txt com RM, nome e turma em cada .zip"],
                  ["23 a 27/11", "Apresentações presenciais (30% da nota de cada disciplina); "
                                 "todos devem saber responder"],
                  ], [3, 14]),
          Spacer(1, 8),
          h2("2.1 O que cada disciplina exige da solução"),
          tabela([["Disciplina", "Exigência que afeta o projeto"],
                  ["IA & Chatbot", "≥ 2 modelos (regressão, classificação e/ou agrupamento) com "
                                   "dados reais em .csv; notebooks .ipynb; modelos .joblib/.pickle;"
                                   " API REST em Flask consumindo os modelos."],
                  ["Banco de Dados", "Oracle; ≥ 6 tabelas; dois 1:N e um N:N com associativa; PK, "
                                     "FK, NOT NULL, UNIQUE, CHECK; 60 registros; UPDATE e DELETE "
                                     "com WHERE; 10 consultas (JOINs, HAVING, subconsulta); modelos"
                                     " conceitual, lógico e relacional; dicionário de dados."],
                  ["Python", "Menu no terminal; match-case e if/elif; while e for; listas, "
                             "tuplas, dicionários, sets; funções. <b>Proibido: classes/POO (nota "
                             "zero) e list comprehension (−15 por ocorrência).</b>"],
                  ["Java (DDD)", "Spring Boot; <b>JDBC puro</b> (sem JPA/Hibernate); padrão "
                                 "tb_/cd_/nm_/ds_/dt_ e sequences sq_tb_; DTOs com ModelMapper; "
                                 "Bean Validation; @RestControllerAdvice; status HTTP corretos; "
                                 "CORS; Docker multi-stage no Render; regra de negócio com exceção"
                                 " própria."],
                  ["Front-end", "React + Vite + TS + Tailwind; <b>só Fetch API</b>; 5 páginas "
                                "institucionais + ≥ 2 da solução; rota com parâmetro; responsivo "
                                "(390, 768, 1440 px); deploy na Vercel; GitHub público com ≥ 5 "
                                "commits por integrante; vídeo ≤ 3 min."],
                  ["Eng. Software & Negócio", "PDF com BMC, benchmark, backlog no Jira/Trello "
                                              "(HUs, RF, RNF, RN), casos de uso, diagramas de "
                                              "atividades, protótipo + Nielsen, precificação, "
                                              "ROI, SLA, registro de uso de IA e pitch ≤ 5 min."],
                  ], [3.6, 13.4], destaque_primeira_coluna=True)]

    # 3 ------------------------------------------------------------------
    s += [h1("3. O problema")]
    s += [h2("3.1 Quem é o cidadão afetado"),
          p("O morador de uma cidade brasileira que convive com problemas de <b>zeladoria "
            "urbana</b>: buraco na rua, poste apagado, lixo e entulho descartados na calçada, "
            "árvore com risco de queda, bueiro entupido. Em especial, moradores de bairros "
            "periféricos, onde esses problemas costumam demorar mais para serem resolvidos, e "
            "pessoas com mobilidade reduzida, para quem uma calçada quebrada ou uma rua escura "
            "são barreiras reais."),
          h2("3.2 Qual é a dor"),
          bullets([
              "<b>Do cidadão:</b> não sabe se o pedido foi recebido, quanto vai demorar nem se "
              "alguém já reclamou do mesmo problema. Sem retorno, desiste de reclamar.",
              "<b>Da prefeitura:</b> recebe um volume enorme de chamados misturados, com muitos "
              "duplicados e sem critério claro de urgência. Um bueiro entupido antes da chuva "
              "fica na mesma fila que um pedido de poda.",
              "<b>Da cidade:</b> problemas pequenos viram problemas grandes (buraco vira "
              "acidente, bueiro vira alagamento) e a desigualdade entre bairros cresce.",
          ]),
          h2("3.3 Evidência"),
          p("São Paulo publica no portal de dados abertos da prefeitura o conjunto <b>Dados do "
            "SP156</b>, com as solicitações feitas pelos cidadãos desde 2012. A própria "
            "prefeitura informa uma média de cerca de <b>157 mil solicitações por mês</b> "
            "(dados de 2022). Esse volume mostra a relevância do problema e é a base de dados "
            "dos modelos de IA."),
          caixa("<b>Resolvido em 13/11:</b> os arquivos trimestrais do SP156 foram baixados e as "
                "colunas conferidas. A partir de 2020 existe a coluna \"Data de Finalização\", que "
                "permite calcular o tempo de resolução. Os modelos foram treinados com "
                "<b>982.475 chamados reais</b> (1º tri/2020 a 3º tri/2023). Detalhes na seção 7.1; "
                "o plano B não foi necessário.")]

    # 4 ------------------------------------------------------------------
    s += [h1("4. A solução: ZelaBairro")]
    s += [h2("4.1 Em uma frase"),
          p("<b>O ZelaBairro é uma plataforma em que o cidadão registra e apoia problemas de "
            "zeladoria do seu bairro, e a prefeitura recebe esses chamados já agrupados, com "
            "prazo previsto e risco de atraso calculados por IA, para atender primeiro o que "
            "é mais urgente.</b>"),
          h2("4.2 Como funciona (fluxo principal)"),
          bullets([
              "O cidadão cria a conta (nome, e-mail e senha) ou faz <b>login</b> e escolhe a "
              "<b>categoria</b> e o <b>bairro</b> do problema.",
              "Antes de criar, o sistema mostra ocorrências <b>abertas da mesma categoria no "
              "mesmo bairro</b>. Se o problema já foi registrado, o cidadão <b>apoia</b> a "
              "ocorrência existente em vez de criar outra (RN07).",
              "Se for um problema novo, o cidadão descreve, informa o endereço de referência e, "
              "se quiser, anexa <b>até 3 fotos</b> (RN18). A ocorrência nasce com status ABERTA.",
              "No momento do registro, a <b>API Java</b> (e só ela) consulta a API de IA, que "
              "devolve o <b>prazo previsto em dias</b> e o <b>risco de atraso</b> (S/N). A Java "
              "grava esses valores na ocorrência, e o cidadão já vê a previsão na confirmação e "
              "depois no detalhe (seção 7.4).",
              "O sistema calcula a <b>pontuação de prioridade</b> (RN10) a partir da gravidade "
              "da categoria, dos apoios, do tempo em aberto e do risco.",
              "O gestor da prefeitura faz login (só quem está em tb_gestor entra no painel), vê "
              "a fila ordenada por prioridade e registra "
              "<b>atualizações</b> de status (EM_ANDAMENTO, RESOLVIDA ou CANCELADA), com "
              "comentário. O cidadão acompanha o histórico.",
              "O painel por bairro mostra abertas, atrasadas e tempo médio, o que permite "
              "enxergar a desigualdade entre regiões.",
          ], numerado=True),
          h2("4.3 Diferenciais"),
          bullets([
              "<b>Prioridade explicável:</b> a fila não é só por ordem de chegada; a fórmula é "
              "pública e simples de explicar (RN10).",
              "<b>Previsão com dados reais:</b> o prazo e o risco de atraso vêm de modelos "
              "treinados com o histórico real do SP156.",
              "<b>Menos duplicados:</b> o apoio transforma dez reclamações iguais em uma "
              "ocorrência com dez apoios, o que é melhor para a prefeitura e mostra a urgência.",
              "<b>Transparência por bairro:</b> o painel deixa visível onde o atendimento demora "
              "mais (ODS 10).",
          ]),
          h2("4.4 Escopo do MVP (o que vamos construir)"),
          tabela([["Dentro do escopo", "Fora do escopo (não fazer)"],
                  ["Cadastro de cidadão (nome, e-mail, senha, telefone) e login por e-mail e "
                   "senha; painel só para gestores, que cadastram outros gestores",
                   "Tokens (JWT), recuperação de senha, login social, Spring Security completo"],
                  ["Registrar, listar, filtrar, editar e cancelar ocorrências",
                   "Mapa interativo / geolocalização"],
                  ["Apoiar e retirar apoio de uma ocorrência",
                   "Notificações por e-mail, SMS ou push"],
                  ["Atualizações de status com histórico", "Aplicativo mobile nativo"],
                  ["Até 3 fotos por ocorrência (v1.3), guardadas no Oracle",
                   "Análise das fotos por IA (citar como evolução futura)"],
                  ["Prazo previsto e risco de atraso via IA",
                   "Chatbot dentro do front ou gravando ocorrências (ver nota abaixo)"],
                  ["Fila por prioridade e painel por bairro",
                   "Integração com sistemas reais da prefeitura"],
                  ], [8.5, 8.5]),
          Spacer(1, 6),
          p("Simplificação assumida (v1.2): o login é simples, sem token. A API devolve o id e o "
            "perfil, o front guarda isso no navegador e envia o id nas rotas protegidas; a API "
            "confere no banco se o id é de um gestor. Funciona e é fácil de explicar, mas o id "
            "pode ser forjado: citar como limitação conhecida e o JWT como próxima etapa (seção "
            "8.5)."),
          caixa("<b>Chatbot (v1.1):</b> existe como <b>complemento da disciplina de IA &amp; "
                "Chatbot</b>, servido pela própria API Flask (GET /, GET /chat/inicio, POST /chat). "
                "Ele orienta o cidadão, mostra a previsão da IA e manda concluir o registro no "
                "front; <b>não grava ocorrências</b> e não muda tabelas, rotas da Java, regras RN "
                "nem telas do front. A rubrica de IA não exige chatbot: ele não vale ponto, mas "
                "todos precisam saber explicá-lo. Decisão a confirmar pelo grupo (seção 14).")]

    # 5 ------------------------------------------------------------------
    s += [h1("5. Atores, glossário e regras de negócio")]
    s += [h2("5.1 Atores"),
          tabela([["Ator", "O que faz"],
                  ["Cidadão", "Registra ocorrências, apoia ocorrências de outros, acompanha "
                              "status e histórico."],
                  ["Gestor da prefeitura", "Faz login, vê a fila por prioridade e o painel por "
                                           "bairro, registra atualizações de status e cadastra "
                                           "outros gestores. Pertence a um órgão."],
                  ["Órgão responsável", "Equipe que executa o serviço (iluminação, limpeza...). "
                                        "No MVP é só um cadastro ligado à categoria."],
                  ["Serviço de IA", "Ator de sistema: calcula prazo previsto e risco de "
                                    "atraso."],
                  ], [4, 13], destaque_primeira_coluna=True),
          h2("5.2 Glossário"),
          tabela([["Termo", "Significado no projeto"],
                  ["Ocorrência", "Um problema de zeladoria registrado por um cidadão, em um "
                                 "bairro e de uma categoria."],
                  ["Apoio", "Um cidadão dizendo \"eu também tenho esse problema\" em uma "
                            "ocorrência existente. Relação N:N cidadão-ocorrência."],
                  ["Atualização", "Registro de mudança de status de uma ocorrência, com "
                                  "comentário e data. Forma o histórico."],
                  ["Prazo de referência", "Número de dias que a categoria deveria levar para ser "
                                          "resolvida (nr_prazo_dias, tabela 6.4)."],
                  ["Prazo previsto", "Número de dias que a IA estima para resolver aquela "
                                     "ocorrência (nr_prazo_previsto)."],
                  ["Risco de atraso", "Previsão da IA (S/N) de que a ocorrência vai passar do "
                                      "prazo de referência (fl_risco_atraso)."],
                  ["Dias em aberto", "Dias inteiros entre a abertura e hoje (ou a data de "
                                     "resolução, se já resolvida)."],
                  ["Atrasada", "Dias em aberto maior que o prazo de referência da categoria."],
                  ["Prioridade", "Pontuação calculada pela RN10 e classe ALTA/MEDIA/BAIXA."],
                  ["Gravidade", "Peso de 1 a 5 da categoria (5 = risco à segurança)."],
                  ["Perfil", "CIDADAO ou GESTOR. Não é uma coluna: vem da tabela em que o e-mail "
                             "está (tb_cidadao ou tb_gestor)."],
                  ], [3.6, 13.4], destaque_primeira_coluna=True)]

    s += [h2("5.3 Regras de negócio (valem para todas as disciplinas)"),
          p("Os códigos RN são os mesmos no backlog (Eng. Software), no Java (exceções), no "
            "Python, no front (validações) e no banco (constraints). Ao implementar uma regra, "
            "cite o código no comentário."),
          tabela([["Código", "Regra", "Onde aparece"],
                  ["RN01", "Toda ocorrência tem exatamente 1 cidadão autor, 1 categoria e 1 "
                           "bairro.", "BD (FK NOT NULL), Java, Front"],
                  ["RN02", "Cidadão e gestor são identificados por e-mail único (UNIQUE em cada "
                           "tabela). Não guardamos CPF nem endereço do cidadão (LGPD: "
                           "minimização de dados).",
                   "BD (UNIQUE), Java (409), Front"],
                  ["RN03", "Descrição da ocorrência: obrigatória, de 10 a 500 caracteres. "
                           "Endereço de referência: obrigatório, até 200 caracteres.",
                   "BD, Java (Bean Validation), Front, Python"],
                  ["RN04", "Status possíveis: ABERTA, EM_ANDAMENTO, RESOLVIDA, CANCELADA. "
                           "Toda ocorrência nasce ABERTA, com data de abertura = hoje e sem "
                           "data de resolução.", "BD (CHECK, DEFAULT), Java, Python"],
                  ["RN05", "Transições permitidas: ABERTA → EM_ANDAMENTO; ABERTA → CANCELADA; "
                           "EM_ANDAMENTO → RESOLVIDA; EM_ANDAMENTO → CANCELADA. RESOLVIDA e "
                           "CANCELADA são finais. Qualquer outra transição é recusada (409).",
                   "Java (exceção própria), Python (match-case)"],
                  ["RN06", "O status só muda criando uma atualização (POST de atualização). "
                           "A data de resolução é preenchida automaticamente quando o novo status"
                           " é RESOLVIDA. Toda atualização guarda o gestor que a fez.",
                   "Java, BD (tb_atualizacao)"],
                  ["RN07", "Antes de criar, o sistema mostra as ocorrências ABERTA/EM_ANDAMENTO "
                           "da mesma categoria e bairro e sugere apoiar. É sugestão, não "
                           "bloqueio.", "Front, Python"],
                  ["RN08", "Um cidadão apoia uma ocorrência no máximo uma vez, não pode apoiar a"
                           " própria ocorrência e só pode apoiar ocorrências ABERTA ou "
                           "EM_ANDAMENTO (409).", "BD (PK composta), Java, Python (set)"],
                  ["RN09", "Ocorrência só pode ser editada (descrição, endereço, categoria, "
                           "bairro) enquanto estiver ABERTA. Ocorrência com apoios ou "
                           "atualizações não é excluída: deve ser CANCELADA (409).",
                   "Java, Front"],
                  ["RN10", "Prioridade (só para ABERTA/EM_ANDAMENTO) — fórmula abaixo.",
                   "Java, Python, BD (consulta)"],
                  ["RN11", "Atrasada = dias em aberto &gt; prazo de referência da categoria.",
                   "Java, Python, BD, painel"],
                  ["RN12", "Se a API de IA estiver fora do ar, a ocorrência é criada mesmo "
                           "assim, com prazo previsto e risco nulos. A IA nunca bloqueia o "
                           "cidadão.", "Java"],
                  ["RN13", "Listagens públicas nunca mostram o e-mail ou telefone do "
                           "cidadão; mostram só o primeiro nome.", "Java (DTO), Front"],
                  ["RN14", "Categoria e bairro com ocorrências vinculadas não podem ser "
                           "excluídos (409).", "Java, BD (FK)"],
                  ["RN15", "Login por e-mail e senha (mínimo 6 caracteres). A senha é guardada só "
                           "como hash BCrypt e nunca volta em nenhuma resposta. Credenciais "
                           "erradas: 401 com mensagem genérica (\"e-mail ou senha inválidos\").",
                   "Java, BD, Front"],
                  ["RN16", "Só gestor muda status, vê o painel e cadastra gestores. A API confere "
                           "no banco, a cada requisição, se o id enviado existe em tb_gestor; se "
                           "não existir: 403. Esconder o menu no front não basta.",
                   "Java, Front"],
                  ["RN17", "Gestor só é criado por outro gestor, e fica registrado quem o "
                           "cadastrou. O primeiro gestor vem do seed do banco. O cadastro público "
                           "(POST /cidadaos) sempre cria cidadão.", "Java, BD (FK própria)"],
                  ["RN18", "Fotos (v1.3): só o autor envia ou remove, só enquanto a ocorrência "
                           "estiver ABERTA; no máximo 3 por ocorrência; só JPG ou PNG de até 2 MB. "
                           "Tipo ou tamanho inválido: 400; quarta foto ou ocorrência não ABERTA: "
                           "409; quem não é o autor: 403.", "Java, BD (CHECK), Front"],
                  ], [1.8, 10.7, 4.5], destaque_primeira_coluna=True),
          h3("RN10: fórmula da prioridade"),
          codigo("""
pontos = gravidade_categoria * 10
       + min(qtd_apoios, 20) * 2
       + min(dias_em_aberto, 30)
       + 15  (se risco_atraso = 'S' OU a ocorrência estiver atrasada; soma uma vez só)

classe:  pontos >= 70  -> ALTA
         40 a 69       -> MEDIA
         pontos < 40   -> BAIXA
Ocorrências RESOLVIDA/CANCELADA não têm prioridade (null).
A pontuação é CALCULADA na hora; não é gravada no banco.
"""),
          p("Exemplos para todos conferirem o próprio código (devem dar exatamente isto):"),
          tabela([["Caso", "Gravidade", "Apoios", "Dias", "Risco/atraso", "Pontos", "Classe"],
                  ["Árvore com risco de queda", "5", "3", "2", "S", "50+6+2+15 = 73", "ALTA"],
                  ["Buraco na via", "4", "0", "5", "N, no prazo", "40+0+5 = 45", "MEDIA"],
                  ["Poda de árvore", "2", "0", "10", "N, no prazo", "20+0+10 = 30", "BAIXA"],
                  ["Iluminação (atrasada)", "4", "25", "40", "atrasada", "40+40+30+15 = 125",
                   "ALTA"],
                  ], [3.3, 2.4, 1.7, 1.3, 2.5, 3.7, 2.1])]

    # 6 ------------------------------------------------------------------
    s += [h1("6. Modelo de dados canônico (Oracle)")]
    s += [p("Um único banco serve à disciplina de Banco de Dados e à API Java. Por isso o modelo "
            "segue <b>o padrão de nomes exigido em Java</b> (tb_, cd_, nm_, ds_, dt_ e "
            "sequences sq_tb_), que também atende à regra de BD de nomes sem espaço e sem acento."),
          h2("6.1 Convenção de nomes"),
          tabela([["Prefixo", "Uso", "Exemplo"],
                  ["tb_", "tabela", "tb_ocorrencia"],
                  ["sq_tb_", "sequence da chave primária", "sq_tb_ocorrencia"],
                  ["cd_", "código / chave (PK e FK)", "cd_ocorrencia, cd_bairro"],
                  ["nm_", "nome", "nm_categoria"],
                  ["ds_", "descrição ou texto livre (inclui e-mail)", "ds_ocorrencia, ds_email"],
                  ["dt_", "data", "dt_abertura"],
                  ["nr_", "número", "nr_prazo_dias, nr_telefone"],
                  ["st_", "status", "st_ocorrencia"],
                  ["fl_", "flag S/N", "fl_risco_atraso"],
                  ["bl_", "arquivo binário (BLOB) — v1.3", "bl_imagem"],
                  ], [2.5, 8, 6.5]),
          h2("6.2 Tabelas e relacionamentos"),
          tabela([["Relacionamento", "Tipo", "FK"],
                  ["tb_orgao → tb_categoria", "1:N", "tb_categoria.cd_orgao"],
                  ["tb_categoria → tb_ocorrencia", "1:N", "tb_ocorrencia.cd_categoria"],
                  ["tb_bairro → tb_ocorrencia", "1:N", "tb_ocorrencia.cd_bairro"],
                  ["tb_cidadao → tb_ocorrencia (autor)", "1:N", "tb_ocorrencia.cd_cidadao"],
                  ["tb_ocorrencia → tb_atualizacao", "1:N", "tb_atualizacao.cd_ocorrencia"],
                  ["tb_cidadao ↔ tb_ocorrencia (apoio)", "N:N",
                   "associativa tb_apoio (cd_cidadao, cd_ocorrencia)"],
                  ["tb_orgao → tb_gestor (v1.2)", "1:N", "tb_gestor.cd_orgao"],
                  ["tb_gestor → tb_gestor (quem cadastrou)", "1:N", "tb_gestor.cd_gestor_cadastro "
                                                                   "(autorrelacionamento)"],
                  ["tb_gestor → tb_atualizacao (v1.2)", "1:N", "tb_atualizacao.cd_gestor"],
                  ["tb_ocorrencia → tb_foto (v1.3)", "1:N", "tb_foto.cd_ocorrencia"],
                  ], [6.5, 1.5, 9]),
          Spacer(1, 6),
          p("Total: <b>9 tabelas</b> (mínimo exigido: 6). Ordem de criação, respeitando as FKs: "
            "tb_orgao, tb_bairro, tb_cidadao, tb_gestor, tb_categoria, tb_ocorrencia, "
            "tb_atualizacao, tb_apoio, tb_foto."),
          caixa("<b>Por que tabelas separadas para cidadão e gestor (v1.2):</b> são papéis do "
                "domínio com dados diferentes (o gestor pertence a um órgão e sabe quem o "
                "cadastrou), a mudança não renomeia nada do que já existia e evita a \"tb_usuario\" "
                "genérica que o PDF de Java critica (\"nada de CRUD genérico de usuário\"). "
                "Consequência: o mesmo e-mail não deve existir nas duas tabelas; o cadastro de "
                "cidadão e o de gestor recusam (409) um e-mail que já esteja na outra.")]

    col = [3.6, 2.9, 1.3, 9.2]
    s += [h2("6.3 Dicionário de dados"),
          h3("tb_orgao — órgãos que executam os serviços"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_orgao", "NUMBER(10)", "N", "PK (sq_tb_orgao)"],
                  ["nm_orgao", "VARCHAR2(100)", "N", "UNIQUE. Nome do órgão"],
                  ["ds_email", "VARCHAR2(120)", "N", "E-mail de contato"],
                  ["nr_telefone", "VARCHAR2(20)", "S", "Telefone de contato"]], col),
          h3("tb_bairro — bairros/distritos atendidos"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_bairro", "NUMBER(10)", "N", "PK (sq_tb_bairro)"],
                  ["nm_bairro", "VARCHAR2(80)", "N", "Nome do bairro/distrito. UNIQUE junto com "
                                                     "nm_subprefeitura"],
                  ["nm_subprefeitura", "VARCHAR2(80)", "N", "Subprefeitura (mesmo nome usado no "
                                                            "SP156 e na API de IA)"],
                  ["nr_populacao", "NUMBER(9)", "S", "CHECK (nr_populacao &gt; 0)"]], col),
          h3("tb_cidadao — quem registra e apoia"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_cidadao", "NUMBER(10)", "N", "PK (sq_tb_cidadao)"],
                  ["nm_cidadao", "VARCHAR2(100)", "N", "Nome completo"],
                  ["ds_email", "VARCHAR2(120)", "N", "UNIQUE (RN02)"],
                  ["ds_senha", "VARCHAR2(100)", "N", "Hash BCrypt da senha (RN15). Nunca a senha"],
                  ["nr_telefone", "VARCHAR2(20)", "S", "Opcional"],
                  ["dt_cadastro", "DATE", "N", "DEFAULT SYSDATE"]], col),
          h3("tb_gestor — servidores da prefeitura que acessam o painel (v1.2)"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_gestor", "NUMBER(10)", "N", "PK (sq_tb_gestor)"],
                  ["nm_gestor", "VARCHAR2(100)", "N", "Nome completo"],
                  ["ds_email", "VARCHAR2(120)", "N", "UNIQUE (RN02)"],
                  ["ds_senha", "VARCHAR2(100)", "N", "Hash BCrypt da senha (RN15)"],
                  ["cd_orgao", "NUMBER(10)", "N", "FK → tb_orgao (onde o gestor trabalha)"],
                  ["cd_gestor_cadastro", "NUMBER(10)", "S", "FK → tb_gestor: quem cadastrou "
                                                            "(RN17). Nulo só no gestor do seed"],
                  ["dt_cadastro", "DATE", "N", "DEFAULT SYSDATE"]], col),
          h3("tb_categoria — tipos de problema"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_categoria", "NUMBER(10)", "N", "PK (sq_tb_categoria)"],
                  ["nm_categoria", "VARCHAR2(60)", "N", "UNIQUE. Nome canônico (tabela 6.4)"],
                  ["ds_categoria", "VARCHAR2(255)", "S", "Explicação para o cidadão"],
                  ["nr_prazo_dias", "NUMBER(3)", "N", "Prazo de referência. CHECK (&gt; 0)"],
                  ["nr_gravidade", "NUMBER(1)", "N", "CHECK (nr_gravidade BETWEEN 1 AND 5)"],
                  ["cd_orgao", "NUMBER(10)", "N", "FK → tb_orgao"]], col),
          h3("tb_ocorrencia — o problema registrado"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_ocorrencia", "NUMBER(10)", "N", "PK (sq_tb_ocorrencia)"],
                  ["ds_ocorrencia", "VARCHAR2(500)", "N", "Descrição, 10 a 500 caracteres (RN03)"],
                  ["ds_endereco", "VARCHAR2(200)", "N", "Endereço de referência (rua, número "
                                                        "aproximado, ponto de referência)"],
                  ["st_ocorrencia", "VARCHAR2(15)", "N", "DEFAULT 'ABERTA'. CHECK IN ('ABERTA',"
                                                         "'EM_ANDAMENTO','RESOLVIDA','CANCELADA')"],
                  ["dt_abertura", "DATE", "N", "DEFAULT SYSDATE"],
                  ["dt_resolucao", "DATE", "S", "Preenchida só ao resolver. CHECK (dt_resolucao "
                                                "IS NULL OR dt_resolucao &gt;= dt_abertura)"],
                  ["nr_prazo_previsto", "NUMBER(4)", "S", "Dias previstos pela IA (RN12)"],
                  ["fl_risco_atraso", "CHAR(1)", "S", "CHECK IN ('S','N'). Previsão da IA"],
                  ["cd_cidadao", "NUMBER(10)", "N", "FK → tb_cidadao (autor)"],
                  ["cd_categoria", "NUMBER(10)", "N", "FK → tb_categoria"],
                  ["cd_bairro", "NUMBER(10)", "N", "FK → tb_bairro"]], col),
          h3("tb_atualizacao — histórico de status"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_atualizacao", "NUMBER(10)", "N", "PK (sq_tb_atualizacao)"],
                  ["cd_ocorrencia", "NUMBER(10)", "N", "FK → tb_ocorrencia"],
                  ["st_anterior", "VARCHAR2(15)", "N", "Status antes da mudança"],
                  ["st_novo", "VARCHAR2(15)", "N", "Mesmo CHECK de st_ocorrencia"],
                  ["ds_comentario", "VARCHAR2(300)", "S", "Ex.: \"Equipe agendada para 14/11\""],
                  ["cd_gestor", "NUMBER(10)", "N", "FK → tb_gestor: quem fez a atualização "
                                                   "(RN06, v1.2)"],
                  ["dt_atualizacao", "DATE", "N", "DEFAULT SYSDATE"]], col),
          h3("tb_apoio — associativa do N:N cidadão ↔ ocorrência"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_cidadao", "NUMBER(10)", "N", "PK composta + FK → tb_cidadao"],
                  ["cd_ocorrencia", "NUMBER(10)", "N", "PK composta + FK → tb_ocorrencia"],
                  ["dt_apoio", "DATE", "N", "DEFAULT SYSDATE"]], col),
          h3("tb_foto — fotos do problema (v1.3)"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_foto", "NUMBER(10)", "N", "PK (sq_tb_foto)"],
                  ["cd_ocorrencia", "NUMBER(10)", "N", "FK → tb_ocorrencia"],
                  ["bl_imagem", "BLOB", "N", "O arquivo da imagem (bytes)"],
                  ["ds_tipo", "VARCHAR2(20)", "N", "CHECK IN ('image/jpeg','image/png') (RN18)"],
                  ["nr_tamanho", "NUMBER(8)", "N", "Bytes. CHECK (nr_tamanho BETWEEN 1 AND "
                                                    "2097152), ou seja, até 2 MB (RN18)"],
                  ["dt_envio", "DATE", "N", "DEFAULT SYSDATE"]], col),
          p("Prefixo novo <b>bl_</b> = BLOB (arquivo binário). O limite de 3 fotos por ocorrência "
            "é verificado na Java (contagem antes de inserir), porque um CHECK não consegue "
            "contar linhas de outra consulta."),
          caixa("Cada tabela precisa de COMMENT ON TABLE no script (exigência de BD). As "
                "sequences existem para todas as tabelas, menos tb_apoio, que usa chave "
                "composta.")]

    s += [h2("6.4 Dados fixos (seed) — categorias e órgãos"),
          p("Estes nomes são usados igualzinho no banco, na API de IA (de-para do SP156), no "
            "Python e no front. Os prazos e gravidades são premissas do projeto; a IA pode "
            "propor ajuste com base na mediana real do SP156 <b>até 13/11</b>. Depois disso, "
            "ficam congelados."),
          tabela([["cd", "nm_categoria", "Órgão responsável", "Prazo (dias)", "Gravidade"],
                  ["1", "Buraco na via", "Subprefeitura - Zeladoria", "15", "4"],
                  ["2", "Iluminação pública apagada", "Iluminação Pública", "7", "4"],
                  ["3", "Descarte irregular de lixo", "Limpeza Urbana", "10", "3"],
                  ["4", "Árvore com risco de queda", "Áreas Verdes", "5", "5"],
                  ["5", "Poda de árvore", "Áreas Verdes", "30", "2"],
                  ["6", "Calçada danificada", "Subprefeitura - Zeladoria", "30", "3"],
                  ["7", "Bueiro entupido", "Subprefeitura - Zeladoria", "10", "4"],
                  ["8", "Sinalização de trânsito danificada", "Trânsito e Sinalização", "10",
                   "3"],
                  ], [1, 5.6, 5, 2.4, 3]),
          Spacer(1, 4),
          p("Órgãos (5): Subprefeitura - Zeladoria; Iluminação Pública; Limpeza Urbana; Áreas "
            "Verdes; Trânsito e Sinalização. Bairros: usar distritos reais de São Paulo com a "
            "subprefeitura correta (ex.: Lapa/Lapa, Pinheiros/Pinheiros, Capão Redondo/Campo "
            "Limpo, Itaim Paulista/Itaim Paulista, Sé/Sé), para casar com os dados do SP156."),
          p("<b>Fotos no seed (v1.3):</b> para que tb_foto também tenha registros (exigência de "
            "BD), usar imagens PNG minúsculas (1×1 pixel, cerca de 70 bytes) inseridas com "
            "HEXTORAW('89504E47...') no INSERT. Fotos reais entram pela aplicação."),
          p("<b>Gestor inicial (v1.2):</b> o seed cria pelo menos um gestor, com "
            "cd_gestor_cadastro nulo, para que alguém consiga entrar no painel e cadastrar os "
            "demais (RN17). O hash BCrypt da senha desse gestor é gerado uma vez (pela própria API "
            "ou por um gerador BCrypt) e colado no INSERT; a senha em texto fica só com o grupo, "
            "nunca no script nem no GitHub."),
          caixa("<b>v1.1:</b> os nomes de tb_bairro.nm_subprefeitura devem ser <b>exatamente</b> "
                "os do arquivo data/depara_distrito_subprefeitura.csv do projeto de IA (32 "
                "subprefeituras). Nome diferente não quebra a API, mas a previsão fica genérica. "
                "Os prazos foram congelados em 13/11 sem alteração. Ponto de atenção para as "
                "apresentações: em Sinalização de trânsito a mediana real (18 dias) já passa do "
                "prazo de referência (10 dias), e 61% dos chamados atrasam.", "atencao"),
          h2("6.5 Perguntas que o banco responde (base para as 10 consultas)"),
          bullets([
              "Quais bairros têm mais ocorrências abertas? (GROUP BY + HAVING)",
              "Qual o tempo médio de resolução por categoria? (AVG + cálculo de datas)",
              "Quais ocorrências estão atrasadas? (cálculo no SELECT + WHERE + JOIN categoria)",
              "Quais ocorrências ainda não receberam nenhum apoio? (LEFT JOIN tb_apoio)",
              "Qual a ocorrência mais apoiada? (subconsulta com MAX/COUNT)",
              "Quantas ocorrências cada órgão tem sob sua responsabilidade? (INNER JOIN em 3 "
              "tabelas + COUNT)",
              "Quais categorias nunca tiveram ocorrência? (RIGHT JOIN)",
              "Histórico de status de uma ocorrência (JOIN tb_atualizacao + ORDER BY)",
              "Maior e menor prazo previsto pela IA por subprefeitura (MAX/MIN)",
              "Cidadãos mais engajados (soma de ocorrências criadas e apoios)",
              "(v1.3, alternativa) Ocorrências abertas sem nenhuma foto (LEFT JOIN tb_foto + "
              "WHERE cd_foto IS NULL)",
              "(v1.2, alternativa) Atualizações feitas por gestor e por órgão (JOIN tb_gestor + "
              "tb_orgao) e quem cadastrou cada gestor (autojunção em tb_gestor)",
          ], numerado=True),
          p("Sugestões de UPDATE/DELETE com WHERE: mudar o status de uma ocorrência para "
            "RESOLVIDA (UPDATE) e retirar um apoio (DELETE em tb_apoio).")]

    # 7 ------------------------------------------------------------------
    s += [h1("7. Inteligência Artificial")]
    s += [h2("7.1 Dados"),
          bullets([
              "<b>Fonte:</b> Dados do SP156, portal de dados abertos da Prefeitura de São Paulo "
              "(dados.prefeitura.sp.gov.br, conjunto \"dados-do-sp156\"). Citar fonte e data de "
              "download no notebook e nas apresentações.",
              "<b>Recorte:</b> somente os assuntos que correspondem às 8 categorias da tabela "
              "6.4, criando uma coluna <b>categoria</b> com o nome canônico (de-para). O "
              "de-para fica salvo em data/depara_sp156.csv.",
              "<b>Janela usada (v1.1):</b> chamados abertos de <b>01/01/2020 a 30/09/2023</b>, "
              "982.475 linhas em data/dados_sp156.csv. Antes de 2020 a data de fim era a \"Data "
              "do Parecer\", que em vários anos cai no mesmo dia da abertura e não mede o "
              "atendimento. Faltam nos dados o 2º tri/2023 e fev–mar/2021.",
              "<b>Subprefeitura:</b> derivada do distrito por data/depara_distrito_subprefeitura.csv "
              "(96 distritos → 32 subprefeituras); confere com a Prefeitura Operacional do SP156 "
              "em 98,4% dos chamados.",
              "<b>O que o prazo mede:</b> pelo glossário oficial, a \"Data de Finalização\" é o "
              "fechamento do protocolo pelo órgão, não necessariamente o dia do conserto.",
              "<b>Categoria sem dados:</b> \"Iluminação pública apagada\" não tem nenhum chamado no "
              "SP156 a partir de 2018. Os modelos não aprenderam nada sobre ela (ver 7.4).",
              "<b>Limitações a citar:</b> período inclui a pandemia; os dados vão só até set/2023.",
          ]),
          h2("7.2 Modelos"),
          tabela([["Modelo", "Tipo", "Alvo", "Métricas"],
                  ["M1 – Prazo previsto", "Regressão (ex.: RandomForestRegressor)",
                   "dias_para_resolver = data de encerramento − data de abertura",
                   "MAE, RMSE, R²"],
                  ["M2 – Risco de atraso", "Classificação (ex.: RandomForestClassifier ou "
                                           "LogisticRegression)",
                   "atrasou = 1 se dias_para_resolver &gt; nr_prazo_dias da categoria (mesma "
                   "regra da RN11), senão 0",
                   "Acurácia, precisão, recall, F1, matriz de confusão"],
                  ["M3 – Perfis de subprefeitura (opcional)", "Agrupamento (KMeans)",
                   "grupos de subprefeituras por volume e tempo médio por categoria",
                   "Silhueta, método do cotovelo"],
                  ], [3.6, 4.2, 5.5, 3.7], destaque_primeira_coluna=True),
          Spacer(1, 6),
          p("<b>Variáveis de entrada (features) dos modelos M1 e M2</b>, as mesmas que a API "
            "recebe: categoria, subprefeitura, mes (1–12) e dia_semana (0 = segunda ... 6 = "
            "domingo, igual ao weekday() do Python). Só usar informações que existem <b>no "
            "momento da abertura</b>; nunca usar a data de encerramento como entrada."),
          h3("Resultado obtido (v1.1) — conjunto de teste de 20%, random_state = 42"),
          tabela([["Modelo", "Algoritmo final", "Métricas no teste", "Baseline"],
                  ["M1 – Prazo", "RandomForestRegressor sobre log(1 + dias)",
                   "MAE 23,3 dias · RMSE 61,0 · R² 0,06",
                   "MAE 24,5 (mediana por categoria) · 26,6 (mediana geral)"],
                  ["M2 – Atraso", "RandomForestClassifier com class_weight=\"balanced\"",
                   "ROC AUC 0,754 · recall 0,834 · precisão 0,421 · F1 0,559 · acurácia 0,609",
                   "acurácia 0,702 (sempre \"no prazo\")"],
                  ], [2.6, 4.6, 5.4, 4.4], destaque_primeira_coluna=True),
          Spacer(1, 6),
          bullets([
              "<b>Mês recebido, mas ignorado:</b> no teste \"no tempo\" (treino 2020–2022, teste "
              "2023) o mês piora os dois modelos. A API continua recebendo mes (contrato), mas os "
              "modelos não o usam.",
              "<b>Limiar do risco:</b> risco_atraso = \"S\" quando probabilidade &gt;= 0,5 "
              "(a v1.0 não definia).",
              "<b>Probabilidade inflada:</b> o balanceamento empurra as probabilidades para cima "
              "(buraco na Lapa: 0,66, mas só 33% dos buracos atrasam). Tratar como "
              "<b>indicador de risco</b>, não como chance real.",
              "M3 (agrupamento) não foi feito: era opcional.",
              "<b>Alinhamento às aulas (v1.3, a aplicar nos notebooks):</b> antes do Random "
              "Forest, treinar e comparar os modelos interpretáveis vistos em aula (Regressão "
              "Linear e Árvore de Decisão no M1; Regressão Logística e Árvore de Decisão no M2), "
              "trocar o Ridge por LinearRegression, plotar a curva ROC e retirar a curva de "
              "calibração. Detalhes em docs/referencias/06-ia-aulas-prof-alfonso.md.",
          ]),
          h2("7.3 Contrato da API Flask"),
          tabela([["Método", "Rota", "Resposta 200"],
                  ["GET", "/health", '{"status": "ok"}'],
                  ["POST", "/prever/prazo", '{"prazo_previsto_dias": 12}'],
                  ["POST", "/prever/atraso", '{"risco_atraso": "S", "probabilidade": 0.73}'],
                  ], [2, 4, 11]),
          Spacer(1, 6),
          p("Corpo das duas rotas POST (JSON, nomes exatamente assim):"),
          codigo("""
{
  "categoria": "Buraco na via",
  "subprefeitura": "Lapa",
  "mes": 11,
  "dia_semana": 2
}
Erro (400): {"erro": "categoria desconhecida: Buraco"}
"""),
          p("Arquivos esperados: data/*.csv, notebooks/01_eda.ipynb, 02_modelo_prazo.ipynb, "
            "03_modelo_atraso.ipynb, models/modelo_prazo.joblib, models/modelo_atraso.joblib, "
            "app.py (Flask). A demonstração ao vivo da API vale 20 pontos na apresentação."),
          p("<b>Rotas extras (v1.1, não alteram o contrato acima):</b> GET /modelo/info (lista as "
            "categorias com histórico suficiente, mínimo de 200 chamados) e as rotas do chatbot "
            "(GET /, GET /chat/inicio, POST /chat). Modelo ausente ou ilegível: 503."),
          h2("7.4 Integração: como a previsão chega ao cidadão"),
          p("A IA é um <b>serviço separado</b> (API Flask com os arquivos .joblib). Ela <b>não "
            "acessa o banco</b> nem a API Java: recebe 4 informações e devolve o prazo e o risco, "
            "como uma calculadora. O <b>front também não chama a IA</b>: ele só conhece a API "
            "Java. Quem chama a IA é a Java, uma única vez, quando a ocorrência é criada."),
          codigo("""
Cidadão → Front (React) → POST /ocorrencias → API Java
                                                │ 1. valida e monta {categoria, subprefeitura,
                                                │    mes, dia_semana}
                                                │ 2. POST /prever/prazo e /prever/atraso → API de IA
                                                │ 3. grava a ocorrência + nr_prazo_previsto +
                                                │    fl_risco_atraso no Oracle
Front ← 201 com "prazoPrevistoDias" e "riscoAtraso" ┘
"""),
          tabela([["Onde a previsão aparece", "Quem vê", "De onde vem"],
                  ["Confirmação do registro", "Cidadão", "Resposta do POST /ocorrencias"],
                  ["/ocorrencias/:id (detalhe)", "Qualquer pessoa",
                   "GET /ocorrencias/{id}: lida do banco, sem chamar a IA de novo"],
                  ["/ocorrencias (lista)", "Qualquer pessoa", "Selo de prioridade, que inclui o "
                                                              "risco (RN10)"],
                  ["/painel", "Gestor", "Fila por prioridade: risco S soma +15 pontos (RN10)"],
                  ], [4.5, 3, 9.5]),
          Spacer(1, 6),
          bullets([
              "<b>No site,</b> a previsão é sempre apresentada como estimativa: \"Previsão: cerca "
              "de 16 dias. Risco de atraso: alto.\" Sem porcentagem (D4).",
              "<b>Configuração:</b> a URL da Flask fica na variável IA_API_URL da API Java. A Flask "
              "precisa estar publicada (ex.: Render) para a Java alcançá-la.",
              "<b>Se a IA estiver fora do ar ou não integrada,</b> a ocorrência é criada sem "
              "previsão (RN12) e o site mostra \"previsão indisponível\". A integração é "
              "desejável: nem IA nem Java perdem nota sem ela, e a demo de IA é feita chamando a "
              "Flask direto (Postman/Insomnia).",
              "<b>Por que não o front chamando a IA:</b> a previsão não ficaria gravada (o gestor "
              "não a veria), o front dependeria de duas APIs e a prioridade, calculada na Java, "
              "ficaria sem o risco.",
          ]),
          caixa("<b>Iluminação pública apagada:</b> a API aceita a categoria (contrato) e devolve "
                "uma previsão, mas ela <b>não tem base</b> (nenhum chamado no treino). Proposta: a "
                "Java trata essa categoria como a RN12 e grava prazo e risco nulos (ou consulta "
                "GET /modelo/info). Decisão a confirmar pelo grupo (seção 14).", "atencao"),
          h2("7.5 Plano B"),
          p("Não foi necessário: o CSV do SP156 tem data de finalização a partir de 2020 (ver "
            "7.1). Mantido aqui apenas como registro da v1.0.")]

    # 8 ------------------------------------------------------------------
    s += [h1("8. API Java (Domain Driven Design)")]
    s += [h2("8.1 Estrutura"),
          p("Spring Boot com pacotes <b>model</b> (entidades), <b>dao</b> (JDBC com "
            "PreparedStatement, DataSource pelo construtor), <b>dto</b> (entrada e saída, "
            "ModelMapper), <b>controller</b>, <b>exception</b>, <b>handler</b> "
            "(@RestControllerAdvice) e <b>config</b> (CORS). Nunca JPA/Hibernate/Spring Data."),
          p("Entidades obrigatórias com CRUD completo: <b>Cidadao, Gestor, Bairro, Categoria, "
            "Ocorrencia</b>, mais as rotas aninhadas de <b>Atualizacao</b> (1:N) e <b>Apoio</b> "
            "(N:N), as <b>fotos</b> (FotoDAO, rotas aninhadas, v1.3) e o <b>login</b> (AuthController). tb_orgao fica só no banco (seed) e aparece "
            "como nome dentro da categoria e do gestor. Exceções novas (v1.2): "
            "CredenciaisInvalidasException (401) e AcessoNegadoException (403)."),
          h2("8.2 Endpoints"),
          tabela([["Método", "Rota", "Sucesso", "Erros"],
                  ["POST", "/auth/login (v1.2)", "200", "400, 401 (RN15)"],
                  ["POST", "/cidadaos (cadastro público, com senha)", "201 + Location",
                   "400, 409 (e-mail repetido)"],
                  ["GET", "/cidadaos  ·  /cidadaos/{id}", "200", "404"],
                  ["PUT / DELETE", "/cidadaos/{id}", "200 / 204", "400, 404, 409"],
                  ["CRUD", "/bairros  ·  /bairros/{id}", "201/200/204", "400, 404, 409 (RN14)"],
                  ["GET", "/bairros/{id}/ocorrencias", "200", "404"],
                  ["CRUD", "/categorias  ·  /categorias/{id}", "201/200/204",
                   "400, 404, 409 (RN14)"],
                  ["GET", "/categorias/{id}/ocorrencias", "200", "404"],
                  ["POST", "/ocorrencias", "201 + Location", "400, 404 (FK inexistente)"],
                  ["GET", "/ocorrencias?status=&amp;idBairro=&amp;idCategoria=", "200", "—"],
                  ["GET", "/ocorrencias/{id}", "200", "404"],
                  ["PUT", "/ocorrencias/{id}", "200", "400, 404, 409 (RN09)"],
                  ["DELETE", "/ocorrencias/{id}", "204", "404, 409 (RN09)"],
                  ["GET", "/ocorrencias/{id}/atualizacoes", "200", "404"],
                  ["POST", "/ocorrencias/{id}/atualizacoes [G]", "201 + Location",
                   "400, 403, 404, 409 (RN05)"],
                  ["GET", "/ocorrencias/{id}/apoios", "200", "404"],
                  ["POST", "/ocorrencias/{id}/apoios", "201", "400, 404, 409 (RN08)"],
                  ["DELETE", "/ocorrencias/{id}/apoios/{idCidadao}", "204", "404"],
                  ["POST", "/ocorrencias/{id}/fotos  [A] (multipart, campo \"arquivo\")",
                   "201 + Location", "400, 403, 404, 409 (RN18)"],
                  ["GET", "/ocorrencias/{id}/fotos (lista sem os bytes)", "200", "404"],
                  ["GET", "/fotos/{idFoto} (devolve a imagem)", "200 (image/jpeg ou png)", "404"],
                  ["DELETE", "/ocorrencias/{id}/fotos/{idFoto}  [A]", "204", "403, 404, 409"],
                  ["GET", "/painel/bairros (desejável) [G]", "200", "403"],
                  ["POST", "/gestores [G]", "201 + Location", "400, 403, 409 (RN17)"],
                  ["GET", "/gestores  ·  /gestores/{id} [G]", "200", "403, 404"],
                  ["PUT / DELETE", "/gestores/{id} [G]", "200 / 204",
                   "400, 403, 404, 409 (gestor com atualizações)"],
                  ], [2.3, 7.7, 2.8, 4.2]),
          p("[A] = só o autor da ocorrência (RN18): o front envia o cabeçalho <b>X-Cidadao-Id</b> "
            "e a API compara com tb_ocorrencia.cd_cidadao; diferente: 403."),
          p("[G] = rota de gestor (RN16): o front envia o cabeçalho <b>X-Gestor-Id</b> e a API "
            "confere no banco se esse id existe em tb_gestor; senão, 403. As demais rotas são "
            "abertas, como na v1.1."),
          Spacer(1, 6),
          p("Método não suportado: 405. Erro inesperado: 500 com mensagem genérica. A lista de "
            "ocorrências vem ordenada por prioridade (maior primeiro)."),
          h2("8.3 JSON (campos em camelCase, datas no formato AAAA-MM-DD)"),
          p("<b>POST /ocorrencias</b> (entrada):"),
          codigo("""
{
  "descricao": "Buraco grande na faixa da direita, perto do ponto de ônibus",
  "endereco": "Rua Guaicurus, 1200",
  "idCidadao": 7,
  "idCategoria": 1,
  "idBairro": 3
}
Validações: descricao @NotBlank @Size(min=10, max=500); endereco @NotBlank @Size(max=200);
            idCidadao, idCategoria, idBairro @NotNull @Positive
"""),
          KeepTogether([p("<b>Saída de uma ocorrência</b> (GET /ocorrencias/{id}):"), codigo("""
{
  "id": 15,
  "descricao": "Buraco grande na faixa da direita, perto do ponto de ônibus",
  "endereco": "Rua Guaicurus, 1200",
  "status": "ABERTA",
  "dataAbertura": "2026-11-10",
  "dataResolucao": null,
  "categoria": { "id": 1, "nome": "Buraco na via", "prazoDias": 15, "gravidade": 4,
                 "orgao": "Subprefeitura - Zeladoria" },
  "bairro": { "id": 3, "nome": "Lapa", "subprefeitura": "Lapa" },
  "autor": "Mariana",
  "prazoPrevistoDias": 12,
  "riscoAtraso": "S",
  "qtdApoios": 3,
  "qtdFotos": 2,
  "diasEmAberto": 1,
  "atrasada": false,
  "pontuacaoPrioridade": 62,
  "prioridade": "MEDIA"
}
""")]),
          p("<b>POST /ocorrencias/{id}/atualizacoes:</b> "
            '<font name="Mono" size="8">{"status": "EM_ANDAMENTO", "comentario": "Equipe '
            'agendada"}</font>. <b>POST /ocorrencias/{id}/apoios:</b> '
            '<font name="Mono" size="8">{"idCidadao": 4}</font>. <b>POST /cidadaos:</b> '
            '<font name="Mono" size="8">{"nome", "email" (@Email), "senha" (@Size min=6), '
            '"telefone"}</font>. <b>POST /gestores:</b> <font name="Mono" size="8">{"nome", '
            '"email", "senha", "idOrgao"}</font> (quem cadastra vem do X-Gestor-Id). Nenhuma '
            'resposta devolve a senha ou o hash.'),
          KeepTogether([p("<b>Foto</b> (item de GET /ocorrencias/{id}/fotos, v1.3):"), codigo("""
{"id": 3, "tipo": "image/jpeg", "tamanho": 183402, "dataEnvio": "2026-11-16",
 "url": "/fotos/3"}
O front exibe com <img src={VITE_API_URL + url}>. A saída da ocorrência ganha "qtdFotos".
""")]),
          KeepTogether([p("<b>Login</b> (POST /auth/login):"), codigo("""
Entrada:  {"email": "mariana@email.com", "senha": "minhasenha"}
Saída 200: {"id": 7, "nome": "Mariana", "perfil": "CIDADAO"}      // ou "GESTOR"
Erro 401:  {"status": 401, "erro": "Não autorizado",
            "mensagem": "RN15: e-mail ou senha inválidos", ...}
""")]),
          p("<b>Formato padrão de erro</b> (sempre JSON, nunca stack trace ou SQL):"),
          codigo("""
{
  "status": 409,
  "erro": "Regra de negócio violada",
  "mensagem": "RN08: o cidadão já apoia esta ocorrência",
  "caminho": "/ocorrencias/15/apoios",
  "timestamp": "2026-11-11T14:32:10",
  "campos": []          // no 400: [{"campo": "descricao", "mensagem": "mínimo 10 caracteres"}]
}
"""),
          h2("8.4 Configuração e deploy"),
          p("Variáveis de ambiente (nomes fixos; <b>valores nunca no código</b>, sob pena de "
            "−10): DB_URL, DB_USER, DB_PASSWORD, IA_API_URL, CORS_ORIGINS. Dockerfile multi-stage, "
            "deploy no Render. O plano gratuito do Render \"dorme\": abrir a API alguns minutos "
            "antes de qualquer demonstração."),
          h2("8.5 Como funciona o login (v1.2)"),
          bullets([
              "<b>Cadastro:</b> a API recebe a senha, gera o hash com BCrypt (biblioteca "
              "spring-security-crypto, a mesma do projeto EcoScoreEngine-API, sem o Spring Security "
              "completo) e grava só o hash em ds_senha.",
              "<b>Login:</b> a API procura o e-mail em tb_gestor e depois em tb_cidadao e compara a "
              "senha com o hash (BCrypt.matches). Acertou: devolve id, nome e perfil. Errou: 401 "
              "com mensagem genérica, sem dizer se o erro foi no e-mail ou na senha.",
              "<b>Rotas de gestor:</b> o front manda o id do gestor no cabeçalho X-Gestor-Id. Um "
              "componente da API (ex.: GestorBo.validarGestor) busca o id em tb_gestor antes de "
              "executar; se não achar, lança AcessoNegadoException (403).",
              "<b>CORS:</b> a configuração precisa liberar os cabeçalhos X-Gestor-Id e X-Cidadao-Id "
              "(além de Content-Type), senão o navegador bloqueia essas rotas.",
              "<b>Fotos (v1.3):</b> o controller recebe MultipartFile; o FotoDAO grava com "
              "PreparedStatement.setBytes e lê com getBytes. No application.properties: "
              "spring.servlet.multipart.max-file-size=2MB e max-request-size=7MB. O disco do "
              "Render não serve para guardar arquivos (some ao reiniciar), por isso a foto fica "
              "no Oracle.",
              "<b>Limitação assumida:</b> não há token; quem souber o id de um gestor consegue "
              "forjar o cabeçalho. Para um MVP acadêmico é aceitável e deve ser dito na "
              "apresentação. Próxima etapa: JWT assinado com expiração.",
          ])]

    # 9 ------------------------------------------------------------------
    s += [h1("9. Front-end")]
    s += [h2("9.1 Rotas"),
          tabela([["Rota", "Página", "Tipo"],
                  ["/", "Home: proposta do ZelaBairro, chamada para registrar", "Institucional"],
                  ["/sobre", "Sobre: problema, solução, ODS", "Institucional"],
                  ["/integrantes", "Integrantes: foto, nome, RM, turma, GitHub, LinkedIn",
                   "Institucional"],
                  ["/faq", "Perguntas frequentes", "Institucional"],
                  ["/contato", "Formulário de contato com validação", "Institucional"],
                  ["/ocorrencias", "Lista com filtros (status, bairro, categoria) e badges de "
                                   "prioridade", "Solução (GET)"],
                  ["/ocorrencias/nova", "Formulário de registro com sugestão de apoio (RN07) e "
                                        "anexo de até 3 fotos com pré-visualização (RN18)",
                   "Solução (POST)"],
                  ["/ocorrencias/:id", "Detalhe, previsão da IA, histórico, galeria de fotos, botão "
                                       "Apoiar", "Solução (rota com "
                                                                            "parâmetro)"],
                  ["/login  ·  /cadastro", "Login (e-mail e senha) e cadastro de cidadão (v1.2)",
                   "Solução (POST)"],
                  ["/painel", "[G] Só gestor (v1.2). Fila por prioridade, mudar status, cadastrar "
                              "gestor, resumo por "
                              "bairro", "Solução (POST/PUT)"],
                  ], [3.6, 9.4, 4]),
          h2("9.2 Organização e regras"),
          bullets([
              "Pastas: src/components, src/pages, src/services, src/types.",
              "Toda chamada HTTP fica em src/services/api.ts usando <b>fetch</b> (Axios é "
              "proibido). URL da API em VITE_API_URL.",
              "Os tipos em src/types copiam exatamente os JSON da seção 8.3 (ex.: interface "
              "Ocorrencia com status: 'ABERTA' | 'EM_ANDAMENTO' | 'RESOLVIDA' | 'CANCELADA').",
              "Componentes reutilizáveis mínimos: OcorrenciaCard, StatusBadge, PrioridadeBadge, "
              "Carregando, MensagemErro, EstadoVazio.",
              "Toda tela que chama a API mostra carregando, erro e lista vazia. Formulários "
              "validam antes de enviar e mostram sucesso/erro da API.",
              "Testar em 390×844, 768×1024 e 1440×900, sem rolagem horizontal.",
              "Acessibilidade: label em todo campo, contraste adequado, foco visível, textos "
              "simples (o público inclui idosos).",
              "<b>Sessão (v1.2):</b> depois do login, o front guarda {id, nome, perfil} no "
              "localStorage (com try/catch) num AuthContext, mostra o menu Painel só para GESTOR, "
              "protege /painel e /ocorrencias/nova com um componente RotaProtegida (como no "
              "EcoScoreEngine) e envia X-Gestor-Id nas rotas [G]. O id do cidadão logado preenche "
              "idCidadao no registro e no apoio. Botão Sair limpa a sessão.",
              "<b>Fotos (v1.3):</b> input type=file com accept=\"image/jpeg,image/png\"; validar "
              "tipo, tamanho (2 MB) e quantidade (3) antes de enviar; enviar cada foto com fetch e "
              "FormData (continua sendo Fetch API) depois que o POST /ocorrencias devolver o id; "
              "não definir Content-Type à mão (o navegador monta o multipart).",
              "Repositório público. <b>Cada integrante faz pelo menos 5 commits</b> neste "
              "repositório (mínimo 15 no total).",
          ])]

    # 10 -----------------------------------------------------------------
    s += [h1("10. Aplicação Python")]
    s += [p("<b>ZelaBairro Terminal</b>: ferramenta de triagem para o gestor, que funciona "
            "<b>sem internet</b> (atende ao critério da GS de continuar útil fora do cenário "
            "ideal de conectividade). Implementa as mesmas regras RN04, RN05, RN07, RN08, RN10 e "
            "RN11, com os mesmos nomes de categorias e status."),
          tabela([["Opção do menu", "O que faz", "Estruturas exigidas"],
                  ["1 Registrar ocorrência", "Pede dados, valida RN03, sugere similares (RN07)",
                   "input, if/elif, f-strings"],
                  ["2 Apoiar ocorrência", "Guarda os apoiadores em um set (evita duplicado, "
                                          "RN08)", "set, dicionário"],
                  ["3 Atualizar status", "Valida a transição (RN05)", "match-case"],
                  ["4 Fila de prioridade", "Calcula RN10 e ordena", "for, funções, lista"],
                  ["5 Relatório por bairro", "Abertas, atrasadas, tempo médio; salva .txt",
                   "dicionário de contagem"],
                  ["6 Ocorrências atrasadas", "Aplica RN11", "for, if"],
                  ["0 Sair", "Salva os dados em JSON e encerra", "while"],
                  ], [4, 7.5, 5.5]),
          Spacer(1, 6),
          bullets([
              "Constantes em tuplas: STATUS = ('ABERTA', 'EM_ANDAMENTO', 'RESOLVIDA', "
              "'CANCELADA') e a lista de categorias da tabela 6.4.",
              "Dados em data/ocorrencias.json (carregados ao abrir e salvos ao sair).",
              "<b>Proibido: class (nota zero) e list comprehension (−15 cada).</b> Antes de "
              "entregar, procurar no código por \"class \" e por \"[\" seguido de \"for\" na "
              "mesma linha.",
              "Entrega própria: .py comentados + PDF com capa, sumário, descrição e guia de "
              "execução.",
          ])]

    # 11 -----------------------------------------------------------------
    s += [h1("11. Modelo de negócio (base para Eng. Software)")]
    s += [p("Os itens abaixo são <b>premissas iniciais</b> para manter todos alinhados. A "
            "disciplina de Eng. Software deve fundamentar cada número com fonte ou cálculo."),
          tabela([["Item", "Definição do projeto"],
                  ["Cliente (quem paga)", "Prefeituras de cidades médias (100 mil a 500 mil "
                                          "habitantes), que não têm um canal como o SP156."],
                  ["Usuário", "Cidadão (gratuito) e gestor/servidor da prefeitura."],
                  ["Relação", "B2B2C (na prática B2G): a prefeitura contrata e o cidadão usa."],
                  ["Receita", "Assinatura SaaS mensal por faixa de população + taxa única de "
                              "implantação. Valores saem da precificação (hora técnica × "
                              "esforço + margem)."],
                  ["Tipo de inovação", "Incremental: melhora um processo que já existe "
                                       "(canais 156) com priorização e previsão."],
                  ["Proposta de valor", "Atender primeiro o que é mais urgente, reduzir "
                                        "duplicados e dar transparência ao cidadão."],
                  ["Indicadores de impacto", "Tempo médio de resolução; % de ocorrências "
                                             "atrasadas; apoios por ocorrência (duplicados "
                                             "evitados); diferença de tempo entre bairros."],
                  ["ODS", "11 (cidades sustentáveis; metas 11.3 gestão participativa e 11.5 "
                          "redução de impactos de desastres, ligada a bueiros e alagamentos) e "
                          "10 (redução das desigualdades)."],
                  ["Alternativas a pesquisar", "Colab (app de zeladoria), canais oficiais "
                                               "SP156 e 1746 (Rio), Fala.BR (ouvidoria federal). "
                                               "Registrar fonte e data de cada informação."],
                  ["SLA (ponto de partida)", "Disponibilidade mensal de 99,5%; suporte em dias "
                                             "úteis, das 8h às 18h; prioridades P1/P2/P3 com "
                                             "prazos de resposta e resolução; créditos na "
                                             "mensalidade se a meta não for cumprida."],
                  ], [4, 13], destaque_primeira_coluna=True),
          Spacer(1, 6),
          p("O backlog no Jira/Trello deve usar estas mesmas regras (RN01–RN14), os mesmos "
            "atores (seção 5.1) e as mesmas telas (seção 9.1), para que diagramas, protótipo e "
            "código representem a mesma solução, como a disciplina exige.")]

    # 12 -----------------------------------------------------------------
    s += [h1("12. Arquitetura e integração")]
    s += [diagrama_integracao(), Spacer(1, 8),
          bullets([
              "<b>Front → API Java:</b> única integração obrigatória do front (Fetch, JSON da "
              "seção 8.3). Mocks não são aceitos.",
              "<b>API Java → Oracle:</b> JDBC puro, tabelas da seção 6.",
              "<b>API Java → API de IA:</b> desejável; com fallback da RN12.",
              "<b>App Python:</b> independente, com dados locais em JSON e as mesmas regras.",
              "<b>Banco:</b> o mesmo script SQL é entregue em BD e em Java. Credenciais do "
              "Oracle de quem hospedar o banco ficam só nas variáveis de ambiente do Render.",
          ]),
          h2("12.1 Ordem de dependência entre as disciplinas (v1.1)"),
          p("Cada disciplina só aparece depois daquelas de que precisa. Uma frente só é dada como "
            "pronta quando passa no teste da última coluna; é esse teste que libera a próxima."),
          tabela([["Nível", "Disciplina", "Depende de", "Teste que libera a próxima"],
                  ["0", "Documento Base", "—", "Lido e aceito por todos"],
                  ["1", "IA &amp; Chatbot", "Só dos dados do SP156",
                   "pytest passando; /health e /prever/* respondendo localmente"],
                  ["1", "Banco de Dados", "Nada",
                   "Script .sql rodando no Oracle da FIAP: 9 tabelas, seed com as 8 categorias, o gestor inicial "
                   "e bairros reais, 10 consultas retornando dados"],
                  ["1", "Python", "Nada (JSON local, sem rede)",
                   "Menu funcionando; busca por \"class \" e por list comprehension sem resultado"],
                  ["2", "API Java", "<b>Banco</b> (obrigatório); IA (opcional)",
                   "Endpoints da seção 8 com dados do Oracle; publicada no Render; RN12 testada "
                   "com a Flask desligada"],
                  ["3", "Front-end", "<b>API Java publicada</b> (mocks não são aceitos)",
                   "Login funcionando; telas da solução lendo e gravando pela Java, nas 3 "
                   "resoluções, na Vercel; /painel bloqueado para cidadão"],
                  ["4", "Eng. Software &amp; Negócio", "Produto pronto (telas, regras, registro "
                                                       "de IA)",
                   "Diagramas e protótipo batendo com o construído; pitch gravado"],
                  ], [1.2, 3.3, 4.5, 8]),
          Spacer(1, 6),
          bullets([
              "<b>Caminho crítico:</b> Banco → Java → Front. Atraso no Banco ou na Java atrasa o "
              "Front, que não pode usar mocks.",
              "<b>Podem andar em paralelo sem quebrar a ordem:</b> as 5 páginas institucionais do "
              "front (não usam a API) e BMC, backlog, casos de uso e protótipo de Eng. Software "
              "(saem deste documento).",
              "<b>Java ↔ IA</b> é a única ligação opcional: publicar a Flask no Render só quando a "
              "Java existir. Sem ela, vale a RN12 e nenhuma das duas disciplinas perde ponto.",
          ])]

    # 13 -----------------------------------------------------------------
    s += [h1("13. Organização do grupo")]
    s += [h2("13.1 Responsáveis"),
          tabela([["Frente", "Responsável", "Também apoia"],
                  ["IA (notebooks + Flask)", "________________", "Pitch (dados e evidências)"],
                  ["Banco de Dados (modelos + script + consultas)", "________________",
                   "Java (script SQL)"],
                  ["API Java + deploy no Render", "________________", "Integração com IA"],
                  ["Front-end + deploy na Vercel", "________________", "Protótipo/UX"],
                  ["Python + Eng. Software (documento, backlog, pitch)", "________________",
                   "Registro de IA"],
                  ], [7.5, 4, 5.5]),
          Spacer(1, 6),
          p("Todos precisam conseguir explicar o projeto inteiro: as apresentações cobram que "
            "<b>qualquer integrante</b> responda. Façam revisões cruzadas."),
          h2("13.2 Cronograma (revisado em 15/11, seguindo a ordem da seção 12.1)"),
          tabela([["Data", "Entrega interna"],
                  ["11–13/11 (feito)", "CSV do SP156 validado; grupo cadastrado; categorias e "
                                       "prazos congelados; IA treinada e exportada."],
                  ["15/11", "<b>Nível 1:</b> fechar e testar Banco (script no Oracle com seed), "
                            "Python e o acabamento da IA. <b>Iniciar a API Java</b> (ainda não "
                            "existe e é o caminho crítico). Front faz as páginas institucionais."],
                  ["16/11", "<b>Nível 2:</b> Java com CRUD sobre o Oracle e primeira versão no "
                            "Render para o front consumir."],
                  ["17/11", "<b>Nível 3:</b> front ↔ Java ↔ Oracle; testes nas três resoluções. "
                            "Se a Java estiver estável: publicar a Flask e ligar Java ↔ IA."],
                  ["18/11", "Gravar vídeos (pitch ≤ 5 min, front ≤ 3 min, Java ≤ 5 min). "
                            "Fechar os PDFs. Testar links em aba anônima."],
                  ["19/11", "Montar cada .zip com o .txt de identificação e entregar <b>até o "
                            "meio da tarde</b>, com folga para imprevistos."],
                  ], [2.5, 14.5]),
          h2("13.3 Combinados"),
          bullets([
              "<b>Registro de uso de IA:</b> cada integrante anota, desde já, as ferramentas, "
              "prompts relevantes e o que foi aceito, corrigido ou descartado (vale 10 pontos em "
              "Eng. Software e é regra da GS). Este documento foi elaborado com apoio do Claude "
              "(Anthropic) e revisado pelo grupo: registrar isso.",
              "Nada de senha, usuário de banco ou chave no código ou no GitHub.",
              "Cada .zip: sem node_modules, sem target, com o .txt de RM/nome/turma.",
          ])]

    # 14 -----------------------------------------------------------------
    s += [h1("14. Riscos e pendências")]
    s += [tabela([["Item", "Risco / pendência", "Dono", "Prazo"],
                  ["CSV do SP156", "<b>Resolvido em 13/11</b> (seção 7.1)", "IA", "—"],
                  ["API Java", "Ainda não iniciada em 15/11; é o caminho crítico do Front "
                               "(seção 12.1)", "Java", "16/11"],
                  ["Acabamento da IA", "Preencher a data de download no notebook 01; reexecutar "
                                       "os notebooks na máquina do grupo; conclusões com as "
                                       "palavras do grupo; montar o .zip com "
                                       "scripts/empacotar.py", "IA", "18/11"],
                  ["Nome da empresa", "Eng. Software exige nome da empresa e da solução na capa",
                   "Grupo", "13/11"],
                  ["Banco Oracle", "Definir em qual conta FIAP o banco fica e compartilhar o "
                                   "acesso com segurança", "BD + Java", "13/11"],
                  ["Render dormindo", "API demora ~1 min para acordar → abrir antes das demos",
                   "Java", "Sempre"],
                  ["Flask publicada", "Se não houver deploy, a integração Java↔IA cai na RN12 "
                                      "(e a demo da IA é local)", "IA", "17/11"],
                  ["Login sem token", "O id do gestor no cabeçalho pode ser forjado (seção 8.5); "
                                      "explicar como limitação e o JWT como próxima etapa",
                   "Todos", "—"],
                  ["Fotos no Oracle (v1.3)", "Espaço do Oracle da FIAP é limitado: respeitar 3 fotos "
                                             "de 2 MB. Upload é a última funcionalidade a entrar; "
                                             "o site funciona sem foto", "BD + Java + Front",
                   "17/11"],
                  ["Senha do gestor inicial", "Hash BCrypt no seed; a senha em texto fica só com o "
                                              "grupo, nunca no script nem no GitHub", "BD + Java",
                   "16/11"],
                  ], [3, 8.8, 2.4, 2.8]),
          h2("14.1 Decisões registradas na v1.1 que o grupo precisa confirmar"),
          tabela([["#", "Decisão adotada", "Alternativa"],
                  ["D1", "Chatbot como complemento da disciplina de IA, fora do MVP do front "
                         "(seção 4.4)", "Retirar o chatbot da entrega de IA"],
                  ["D2", "risco_atraso = \"S\" quando probabilidade &gt;= 0,5 (seção 7.2)",
                   "Outro limiar (o notebook 03 mostra o efeito de 0,3 a 0,7)"],
                  ["D3", "Iluminação pública apagada: Java grava prazo e risco nulos, como na "
                         "RN12 (seção 7.4)", "Gravar a previsão da API mesmo sem base"],
                  ["D4", "Probabilidade mostrada como indicador de risco, sem prometer chance "
                         "real (seção 7.2)", "Calibrar o modelo e retreinar"],
                  ["D5", "Prazo de Sinalização mantido em 10 dias, como congelado em 13/11 "
                         "(seção 6.4)", "Reabrir o congelamento (exige refazer dados e modelos)"],
                  ], [1.2, 9.3, 6.5], destaque_primeira_coluna=True),
          p("<b>Decidido na v1.3 (15/11):</b> fotos das ocorrências em tabela própria (tb_foto) "
            "com BLOB no Oracle (RN18); fluxo da previsão explicitado (seção 7.4); notebooks de IA "
            "serão alinhados às aulas (seção 7.2)."),
          p("<b>Decidido na v1.2 (15/11):</b> login por e-mail e senha para cidadão e gestor; "
            "cidadão e gestor em tabelas separadas (tb_cidadao e tb_gestor); painel restrito a "
            "gestores, que cadastram outros gestores (RN15–RN17)."),
          h1("15. Histórico de versões"),
          tabela([["Versão", "Data", "Mudança", "Autor"],
                  ["1.0", "11/11/2026", "Primeira versão: problema, solução, regras RN01–RN14, "
                                        "modelo de dados, contratos de IA, Java, front e Python",
                   "Leonardo (com apoio de IA)"],
                  ["1.1", "15/11/2026", "Integrantes na capa; CSV do SP156 resolvido e plano B "
                                 "descartado; seção 7 com dados, resultados e decisões reais da "
                                 "IA; nota sobre o chatbot; nomes de subprefeitura ligados ao "
                                 "de-para; ordem de dependência entre disciplinas (12.1); "
                                 "cronograma revisado; decisões a confirmar (14.1)",
                   "Leonardo (com apoio de IA)"],
                  ["1.2", "15/11/2026", "Login por e-mail e senha (BCrypt); nova tabela tb_gestor (8 "
                                 "tabelas) com órgão e quem cadastrou; ds_senha em tb_cidadao; "
                                 "cd_gestor em tb_atualizacao; RN15–RN17; rotas /auth/login e "
                                 "/gestores; páginas /login e /cadastro; /painel só para gestor; "
                                 "seção 8.5; escopo 4.4 e riscos atualizados",
                   "Leonardo (com apoio de IA)"],
                  [VERSAO, DATA, "Fotos: tabela tb_foto (9 tabelas), prefixo bl_, RN18, rotas "
                                 "/ocorrencias/{id}/fotos e /fotos/{id}, cabeçalho X-Cidadao-Id, "
                                 "upload no front; seção 7.4 reescrita (como a previsão chega ao "
                                 "cidadão); alinhamento da IA às aulas (7.2); riscos atualizados",
                   "Leonardo (com apoio de IA)"],
                  ], [1.8, 2.4, 9.3, 3.5]),
          Spacer(1, 10),
          h2("Fontes"),
          bullets([
              "FIAP. Global Solution 2026/2 – CitizenTech, 1TDS Fevereiro (slides do kickoff e "
              "requisitos das disciplinas).",
              "Prefeitura de São Paulo. Portal de Dados Abertos – conjunto \"Dados do SP156\". "
              "dados.prefeitura.sp.gov.br (consultado em 11/11/2026).",
              "Prefeitura de São Paulo, Secretaria Municipal de Inovação e Tecnologia – "
              "informações sobre o SP156 (média de 157.120 solicitações/mês em 2022). "
              "prefeitura.sp.gov.br/web/inovacao.",
              "ONU. Objetivos de Desenvolvimento Sustentável 10 e 11. sdgs.un.org.",
          ])]
    return s


if __name__ == "__main__":
    doc = Documento(SAIDA)
    doc.multiBuild(capa() + conteudo())
    print(f"PDF gerado: {SAIDA}")
