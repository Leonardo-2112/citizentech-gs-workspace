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

VERSAO = "1.0"
DATA = "11/11/2026"
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
    caixa_d(350, 100, 125, 70, "Oracle FIAP", "7 tabelas tb_*\nsequences sq_tb_*", VERDE_CLARO)
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
                ["Status", "Aprovado para início do desenvolvimento (pendências na seção 14)"],
                ["Entrega da GS", "19/11/2026 até 23h55, no Portal do Aluno (sem prorrogação)"],
                ["Cadastro do grupo", "até 13/11/2026"],
                ["Integrantes (RM / nome / turma)", "preencher: ______________________________"]],
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
          caixa("<b>Pendência:</b> o grupo ainda precisa baixar o CSV atual do SP156 e confirmar "
                "as colunas (datas de abertura e encerramento, assunto, subprefeitura, status). "
                "Responsável: integrante de IA, até 12/11. Ver seção 7.5 (plano B).", "atencao")]

    # 4 ------------------------------------------------------------------
    s += [h1("4. A solução: ZelaBairro")]
    s += [h2("4.1 Em uma frase"),
          p("<b>O ZelaBairro é uma plataforma em que o cidadão registra e apoia problemas de "
            "zeladoria do seu bairro, e a prefeitura recebe esses chamados já agrupados, com "
            "prazo previsto e risco de atraso calculados por IA, para atender primeiro o que "
            "é mais urgente.</b>"),
          h2("4.2 Como funciona (fluxo principal)"),
          bullets([
              "O cidadão se identifica (nome e e-mail) e escolhe a <b>categoria</b> e o "
              "<b>bairro</b> do problema.",
              "Antes de criar, o sistema mostra ocorrências <b>abertas da mesma categoria no "
              "mesmo bairro</b>. Se o problema já foi registrado, o cidadão <b>apoia</b> a "
              "ocorrência existente em vez de criar outra (RN07).",
              "Se for um problema novo, o cidadão descreve e informa o endereço de referência. "
              "A ocorrência nasce com status ABERTA.",
              "A API Java consulta a API de IA, que devolve o <b>prazo previsto em dias</b> e o "
              "<b>risco de atraso</b> (S/N). Esses valores ficam gravados na ocorrência.",
              "O sistema calcula a <b>pontuação de prioridade</b> (RN10) a partir da gravidade "
              "da categoria, dos apoios, do tempo em aberto e do risco.",
              "O gestor da prefeitura vê a fila ordenada por prioridade e registra "
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
                  ["Cadastro simples de cidadão (nome, e-mail, telefone)",
                   "Login com senha, tokens, autenticação real"],
                  ["Registrar, listar, filtrar, editar e cancelar ocorrências",
                   "Upload de fotos e mapa interativo / geolocalização"],
                  ["Apoiar e retirar apoio de uma ocorrência",
                   "Notificações por e-mail, SMS ou push"],
                  ["Atualizações de status com histórico", "Aplicativo mobile nativo"],
                  ["Prazo previsto e risco de atraso via IA", "Chatbot"],
                  ["Fila por prioridade e painel por bairro",
                   "Integração com sistemas reais da prefeitura"],
                  ], [8.5, 8.5]),
          Spacer(1, 6),
          p("Simplificação assumida: sem login, o front guarda o cidadão escolhido no "
            "navegador, e a área do gestor é uma página aberta (/painel). Essa decisão deve ser "
            "citada como limitação conhecida nas apresentações.")]

    # 5 ------------------------------------------------------------------
    s += [h1("5. Atores, glossário e regras de negócio")]
    s += [h2("5.1 Atores"),
          tabela([["Ator", "O que faz"],
                  ["Cidadão", "Registra ocorrências, apoia ocorrências de outros, acompanha "
                              "status e histórico."],
                  ["Gestor da prefeitura", "Vê a fila por prioridade e o painel por bairro; "
                                           "registra atualizações de status."],
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
                  ], [3.6, 13.4], destaque_primeira_coluna=True)]

    s += [h2("5.3 Regras de negócio (valem para todas as disciplinas)"),
          p("Os códigos RN são os mesmos no backlog (Eng. Software), no Java (exceções), no "
            "Python, no front (validações) e no banco (constraints). Ao implementar uma regra, "
            "cite o código no comentário."),
          tabela([["Código", "Regra", "Onde aparece"],
                  ["RN01", "Toda ocorrência tem exatamente 1 cidadão autor, 1 categoria e 1 "
                           "bairro.", "BD (FK NOT NULL), Java, Front"],
                  ["RN02", "O cidadão é identificado por e-mail único. Não guardamos CPF nem "
                           "endereço do cidadão (LGPD: minimização de dados).",
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
                           " é RESOLVIDA.", "Java, BD (tb_atualizacao)"],
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
                  ], [6.5, 1.5, 9]),
          Spacer(1, 6),
          p("Total: <b>7 tabelas</b> (mínimo exigido: 6). Ordem de criação, respeitando as FKs: "
            "tb_orgao, tb_bairro, tb_cidadao, tb_categoria, tb_ocorrencia, tb_atualizacao, "
            "tb_apoio.")]

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
                  ["nr_telefone", "VARCHAR2(20)", "S", "Opcional"],
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
                  ["dt_atualizacao", "DATE", "N", "DEFAULT SYSDATE"]], col),
          h3("tb_apoio — associativa do N:N cidadão ↔ ocorrência"),
          tabela([["Coluna", "Tipo", "Nulo", "Regra / significado"],
                  ["cd_cidadao", "NUMBER(10)", "N", "PK composta + FK → tb_cidadao"],
                  ["cd_ocorrencia", "NUMBER(10)", "N", "PK composta + FK → tb_ocorrencia"],
                  ["dt_apoio", "DATE", "N", "DEFAULT SYSDATE"]], col),
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
              "<b>Tamanho:</b> usar um recorte gerenciável (ex.: os últimos 12 meses "
              "disponíveis) para treinar rápido em máquina comum.",
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
          h2("7.4 Integração"),
          p("A API Java chama a Flask ao criar uma ocorrência (desejável, não obrigatório para "
            "Java). Para isso, a Flask precisa estar publicada (ex.: Render). Se não estiver, vale "
            "a RN12. A URL fica na variável IA_API_URL da API Java."),
          h2("7.5 Plano B"),
          caixa("Se o CSV do SP156 não tiver data de encerramento ou não der para calcular o tempo "
                "de resolução, a pessoa de IA avisa o grupo <b>até 12/11</b>. Alternativa: M1 vira "
                "regressão do <b>volume mensal de chamados</b> por subprefeitura e categoria, e M2 "
                "classifica se a subprefeitura terá <b>volume acima da média</b> no mês. Nesse caso "
                "este documento é atualizado (v1.1) e o campo nr_prazo_previsto passa a ser "
                "preenchido com o prazo de referência da categoria.", "risco")]

    # 8 ------------------------------------------------------------------
    s += [h1("8. API Java (Domain Driven Design)")]
    s += [h2("8.1 Estrutura"),
          p("Spring Boot com pacotes <b>model</b> (entidades), <b>dao</b> (JDBC com "
            "PreparedStatement, DataSource pelo construtor), <b>dto</b> (entrada e saída, "
            "ModelMapper), <b>controller</b>, <b>exception</b>, <b>handler</b> "
            "(@RestControllerAdvice) e <b>config</b> (CORS). Nunca JPA/Hibernate/Spring Data."),
          p("Entidades obrigatórias com CRUD completo: <b>Cidadao, Bairro, Categoria, "
            "Ocorrencia</b>, mais as rotas aninhadas de <b>Atualizacao</b> (1:N) e <b>Apoio</b> "
            "(N:N). tb_orgao fica só no banco (seed) e aparece como nome dentro da categoria."),
          h2("8.2 Endpoints"),
          tabela([["Método", "Rota", "Sucesso", "Erros"],
                  ["POST", "/cidadaos", "201 + Location", "400, 409 (e-mail repetido)"],
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
                  ["POST", "/ocorrencias/{id}/atualizacoes", "201 + Location",
                   "400, 404, 409 (RN05)"],
                  ["GET", "/ocorrencias/{id}/apoios", "200", "404"],
                  ["POST", "/ocorrencias/{id}/apoios", "201", "400, 404, 409 (RN08)"],
                  ["DELETE", "/ocorrencias/{id}/apoios/{idCidadao}", "204", "404"],
                  ["GET", "/painel/bairros (desejável)", "200", "—"],
                  ], [2.3, 7.7, 2.8, 4.2]),
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
            '<font name="Mono" size="8">{"nome", "email" (@Email), "telefone"}</font>.'),
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
            "antes de qualquer demonstração.")]

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
                  ["/ocorrencias/nova", "Formulário de registro com sugestão de apoio (RN07)",
                   "Solução (POST)"],
                  ["/ocorrencias/:id", "Detalhe, histórico, botão Apoiar", "Solução (rota com "
                                                                            "parâmetro)"],
                  ["/painel", "Área do gestor: fila por prioridade, mudar status, resumo por "
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
          h2("13.2 Cronograma (hoje: 11/11)"),
          tabela([["Data", "Entrega interna"],
                  ["11–12/11", "Validar o CSV do SP156 (IA). Fechar o modelo do banco e o script "
                               "de criação (BD). Ler este documento todos."],
                  ["13/11", "<b>Cadastrar o grupo.</b> Congelar categorias/prazos. Banco criado "
                            "no Oracle com o seed. Backlog criado no Jira/Trello."],
                  ["14–16/11", "Cada frente desenvolve. Java publica uma primeira versão no "
                               "Render para o front consumir. IA treina e exporta modelos."],
                  ["17/11", "Integração: front ↔ Java ↔ Oracle; Java ↔ Flask. Testes nas três "
                            "resoluções."],
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
                  ["CSV do SP156", "Colunas podem não ter data de encerramento → plano B (7.5)",
                   "IA", "12/11"],
                  ["Nome da empresa", "Eng. Software exige nome da empresa e da solução na capa",
                   "Grupo", "13/11"],
                  ["Banco Oracle", "Definir em qual conta FIAP o banco fica e compartilhar o "
                                   "acesso com segurança", "BD + Java", "13/11"],
                  ["Render dormindo", "API demora ~1 min para acordar → abrir antes das demos",
                   "Java", "Sempre"],
                  ["Flask publicada", "Se não houver deploy, a integração Java↔IA cai na RN12 "
                                      "(e a demo da IA é local)", "IA", "17/11"],
                  ["Sem login", "Limitação conhecida do MVP; explicar como próxima etapa",
                   "Todos", "—"],
                  ], [3, 8.8, 2.4, 2.8]),
          h1("15. Histórico de versões"),
          tabela([["Versão", "Data", "Mudança", "Autor"],
                  [VERSAO, DATA, "Primeira versão: problema, solução, regras RN01–RN14, modelo "
                                 "de dados, contratos de IA, Java, front e Python",
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
