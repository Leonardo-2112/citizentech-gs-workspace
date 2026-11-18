"""Gera documentacao.pdf da entrega de Domain Driven Design Using Java (ZelaBairro).

Uso (nesta pasta):  uv run --with reportlab python gerar_documentacao.py
Entradas: os DTOs de entrada do projeto (zelabairro-api/src/.../dto/*RequestDto.java) sao lidos
          para montar a tabela de validacoes, assim o PDF nunca fica diferente do codigo;
          imagens/der.png (modelo relacional do Data Modeler, o mesmo da entrega de Banco).
Saida:    documentacao.pdf nesta pasta.

Os 8 itens pedidos no PDF da disciplina: capa e links, a solucao, diagrama de classes, DER,
endpoints com JSON, pacotes, regras e validacoes, deploy (nomes das variaveis, sem valores).
Antes da entrega, preencha URL_API e URL_VIDEO abaixo e gere de novo.
"""
import re
from pathlib import Path

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, Image, KeepTogether,
                                ListFlowable, ListItem, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Preformatted, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

PASTA = Path(__file__).resolve().parent
DTOS = PASTA / "zelabairro-api" / "src" / "main" / "java" / "br" / "com" / "zelabairro" / "dto"
IMAGENS = PASTA / "imagens"
SAIDA = PASTA / "documentacao.pdf"
DATA = "19/11/2026"

# ---- PREENCHER ANTES DA ENTREGA ----------------------------------------------------------
URL_API = "https://zelabairro-api-08ut.onrender.com"
URL_VIDEO = "[COLOCAR O LINK DO VÍDEO NO YOUTUBE]"
URL_REPOSITORIO = "https://github.com/Leonardo-2112/zelabairro-api"
# -------------------------------------------------------------------------------------------

INTEGRANTES = [
    ("573982", "Leonardo Afonço Sousa"),
    ("569259", "Syang Cristina Gomes Souza"),
    ("573559", "Matheus Jones Sousa de Freitas"),
    ("569023", "Vitor Goncalves de Souza"),
    ("572364", "Joao Machado Nascimento"),
]
TURMA = "1TDSPV"

FONTES = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FONTES + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTES + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONTES + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTES + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic",
                              boldItalic="Sans-Bold")

VERDE = colors.HexColor("#0F5C4D")
VERDE_CLARO = colors.HexColor("#E3F1EC")
AMBAR = colors.HexColor("#B7791F")
AMBAR_CLARO = colors.HexColor("#FDF3DC")
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
    "cel": ParagraphStyle("cel", fontName="Sans", fontSize=7.8, leading=10),
    "cel_b": ParagraphStyle("cel_b", fontName="Sans-Bold", fontSize=7.8, leading=10,
                            textColor=colors.white),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=7.2, leading=9.4),
    "toc1": ParagraphStyle("toc1", fontName="Sans", fontSize=10, leading=17),
    "legenda": ParagraphStyle("legenda", fontName="Sans-Italic", fontSize=8, leading=11,
                              textColor=CINZA, spaceAfter=8),
}
LARGURA = 17 * cm


# --------------------------------------------------------------------------- helpers
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


def bullets(itens):
    return ListFlowable([ListItem(p(i), leftIndent=12) for i in itens], bulletType="bullet",
                        start="•", leftIndent=14, bulletFontName="Sans", bulletFontSize=9)


def tabela(linhas, larguras, destaque_primeira_coluna=False):
    dados = [[Paragraph(str(c), ST["cel_b"]) for c in linhas[0]]]
    dados += [[Paragraph(str(c), ST["cel"]) for c in linha] for linha in linhas[1:]]
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
    fundo, borda = {"info": (VERDE_CLARO, VERDE), "atencao": (AMBAR_CLARO, AMBAR)}[tipo]
    t = Table([[p(texto)]], colWidths=[LARGURA])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), fundo),
        ("LINEBEFORE", (0, 0), (0, -1), 3, borda),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether([t, Spacer(1, 8)])


def codigo(texto):
    t = Table([[Preformatted(texto.strip("\n"), ST["code"])]], colWidths=[LARGURA])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CINZA_CLARO),
        ("BOX", (0, 0), (-1, -1), 0.4, LINHA),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def imagem(arquivo, legenda, altura_max=21 * cm, largura_max=LARGURA):
    caminho = IMAGENS / arquivo
    largura_px, altura_px = ImageReader(str(caminho)).getSize()
    escala = min(largura_max / largura_px, altura_max / altura_px)
    figura = Image(str(caminho), width=largura_px * escala, height=altura_px * escala)
    return KeepTogether([figura, Paragraph(legenda, ST["legenda"])])


def exemplo(titulo, entrada, saida):
    """Bloco de endpoint: titulo + JSON de entrada e de saida."""
    partes = [h3(titulo)]
    if entrada:
        partes += [p("<i>Entrada:</i>"), codigo(entrada), Spacer(1, 3)]
    partes += [p("<i>Saída:</i>"), codigo(saida), Spacer(1, 6)]
    return KeepTogether(partes)


# --------------------------------------------------------------------------- diagrama de classes
def diagrama_classes():
    """Desenha o diagrama de classes dos models (atributos, tipos e associacoes)."""
    W, H = LARGURA, 20.0 * cm
    d = Drawing(W, H)
    FS, LH, CAB = 6.2, 8.0, 13  # fonte, altura da linha, cabecalho
    caixas = {}

    def classe(nome, x, y_topo, largura, atributos, metodos=(), estereotipo=None):
        linhas_cab = 2 if estereotipo else 1
        cab = CAB + (LH if estereotipo else 0)
        altura = cab + 4 + len(atributos) * LH + (6 + len(metodos) * LH if metodos else 0) + 2
        y0 = H - y_topo - altura
        d.add(Rect(x, y0, largura, altura, fillColor=colors.white, strokeColor=VERDE, strokeWidth=0.8))
        d.add(Rect(x, y0 + altura - cab, largura, cab, fillColor=VERDE, strokeColor=VERDE, strokeWidth=0.8))
        if estereotipo:
            d.add(String(x + largura / 2, y0 + altura - LH + 0.5, estereotipo, fontName="Sans-Italic",
                         fontSize=FS - 0.4, fillColor=colors.white, textAnchor="middle"))
        d.add(String(x + largura / 2, y0 + altura - cab + 3.5, nome, fontName="Sans-Bold",
                     fontSize=FS + 1.2, fillColor=colors.white, textAnchor="middle"))
        y = y0 + altura - cab - LH - 1
        for a in atributos:
            d.add(String(x + 4, y + 1, a, fontName="Mono", fontSize=FS, fillColor=colors.black))
            y -= LH
        if metodos:
            d.add(Line(x, y + LH - 2, x + largura, y + LH - 2, strokeColor=VERDE, strokeWidth=0.5))
            y -= 4
            for m in metodos:
                d.add(String(x + 4, y + 1, m, fontName="Mono", fontSize=FS, fillColor=VERDE))
                y -= LH
        caixas[nome] = (x, y0, largura, altura)
        _ = linhas_cab

    def ponto(nome, lado, frac=0.5):
        x, y0, w, h = caixas[nome]
        return {"e": (x, y0 + h * frac), "d": (x + w, y0 + h * frac),
                "t": (x + w * frac, y0 + h), "b": (x + w * frac, y0)}[lado]

    def assoc(a, lado_a, b, lado_b, mult_a="1", mult_b="*", rotulo=None, frac_a=0.5, frac_b=0.5):
        (x1, y1), (x2, y2) = ponto(a, lado_a, frac_a), ponto(b, lado_b, frac_b)
        d.add(Line(x1, y1, x2, y2, strokeColor=CINZA, strokeWidth=0.7))

        def rot(xp, yp, lado, texto):
            dx = {"e": -7, "d": 4, "t": 3, "b": 3}[lado]
            dy = {"e": 2, "d": 2, "t": 3, "b": -7}[lado]
            d.add(String(xp + dx, yp + dy, texto, fontName="Sans-Bold", fontSize=6.5, fillColor=AMBAR))
        rot(x1, y1, lado_a, mult_a)
        rot(x2, y2, lado_b, mult_b)
        if rotulo:
            d.add(String((x1 + x2) / 2 + 2, (y1 + y2) / 2 + 3, rotulo, fontName="Sans-Italic",
                         fontSize=5.8, fillColor=CINZA, textAnchor="middle"))

    LC = 140   # largura das caixas
    XA, XB, XC = 0, 170, W - LC
    classe("Orgao", XA, 0, LC, ["- id: int", "- nome: String", "- email: String", "- telefone: String"])
    classe("Gestor", XC, 0, LC, ["- id: int", "- nome: String", "- email: String",
                                  "- senha: String  (hash)", "- orgao: Orgao",
                                  "- idGestorCadastro: Integer", "- dataCadastro: LocalDate"])
    classe("Categoria", XA, 120, LC, ["- id: int", "- nome: String", "- descricao: String",
                                       "- prazoDias: int", "- gravidade: int", "- orgao: Orgao"])
    classe("Ocorrencia", XB, 120, LC + 8,
           ["- id: int", "- descricao: String", "- endereco: String", "- status: StatusOcorrencia",
            "- dataAbertura: LocalDate", "- dataResolucao: LocalDate", "- prazoPrevisto: Integer",
            "- riscoAtraso: String", "- cidadao: Cidadao", "- categoria: Categoria",
            "- bairro: Bairro", "- qtdApoios: int", "- qtdFotos: int"],
           ["+ getDiasEmAberto(): long", "+ isAtrasada(): boolean  (RN11)",
            "+ getPontuacaoPrioridade(): Integer", "+ getPrioridade(): Prioridade (RN10)"])
    classe("Atualizacao", XC, 150, LC, ["- id: int", "- idOcorrencia: int",
                                         "- statusAnterior: StatusOcorrencia",
                                         "- statusNovo: StatusOcorrencia", "- comentario: String",
                                         "- gestor: Gestor", "- data: LocalDate"])
    classe("Bairro", XA, 245, LC, ["- id: int", "- nome: String", "- subprefeitura: String",
                                    "- populacao: Integer"])
    classe("Apoio", XC, 268, LC, ["- cidadao: Cidadao", "- idOcorrencia: int", "- data: LocalDate"])
    classe("Foto", XB, 375, LC + 8, ["- id: int", "- idOcorrencia: int", "- imagem: byte[]",
                                      "- tipo: String", "- tamanho: long", "- dataEnvio: LocalDate"])
    classe("Cidadao", XC, 375, LC, ["- id: int", "- nome: String", "- email: String",
                                     "- senha: String  (hash)", "- telefone: String",
                                     "- dataCadastro: LocalDate"],
           ["+ getPrimeiroNome(): String (RN13)"])
    classe("StatusOcorrencia", XA, 345, LC, ["ABERTA", "EM_ANDAMENTO", "RESOLVIDA", "CANCELADA"],
           ["+ podeIrPara(novo): boolean (RN05)", "+ isEmAberto(): boolean"], "«enum»")
    classe("Prioridade", XA, 470, 108, ["ALTA", "MEDIA", "BAIXA"],
           ["+ daPontuacao(int)"], "«enum»")
    classe("Perfil", XA + 116, 470, 60, ["CIDADAO", "GESTOR"], (), "«enum»")

    assoc("Orgao", "b", "Categoria", "t", rotulo="responsável por")
    assoc("Orgao", "d", "Gestor", "e", frac_a=0.55, frac_b=0.75, rotulo="trabalha em")
    assoc("Gestor", "b", "Atualizacao", "t", rotulo="registra (RN06)")
    assoc("Categoria", "d", "Ocorrencia", "e", frac_a=0.5, frac_b=0.8)
    assoc("Bairro", "d", "Ocorrencia", "e", frac_a=0.5, frac_b=0.42)
    assoc("Ocorrencia", "d", "Atualizacao", "e", frac_a=0.72, frac_b=0.5)
    assoc("Ocorrencia", "d", "Apoio", "e", frac_a=0.35, frac_b=0.5)
    assoc("Ocorrencia", "b", "Foto", "t", mult_b="0..3", rotulo="RN18")
    assoc("Cidadao", "t", "Apoio", "b", rotulo="apoia")
    assoc("Ocorrencia", "d", "Cidadao", "t", mult_a="*", mult_b="1", frac_a=0.12, frac_b=0.15,
          rotulo="autor")
    # autorrelacionamento do gestor (quem cadastrou - RN17)
    x, y0, w, h = caixas["Gestor"]
    xd = x + w
    for (xa, ya, xb, yb) in [(xd, y0 + h * 0.6, xd + 8, y0 + h * 0.6), (xd + 8, y0 + h * 0.6, xd + 8, y0 + h * 0.25),
                             (xd + 8, y0 + h * 0.25, xd, y0 + h * 0.25)]:
        d.add(Line(xa, ya, xb, yb, strokeColor=CINZA, strokeWidth=0.7))
    d.add(String(xd - 2, y0 + h * 0.6 + 2, "1", fontName="Sans-Bold", fontSize=6.5, fillColor=AMBAR, textAnchor="end"))
    d.add(String(xd - 2, y0 + h * 0.25 - 7, "*", fontName="Sans-Bold", fontSize=6.5, fillColor=AMBAR, textAnchor="end"))
    d.add(String(xd - 32, y0 + h * 0.42, "cadastrou (RN17)", fontName="Sans-Italic", fontSize=5.8, fillColor=CINZA))
    _ = Polygon
    return d


# --------------------------------------------------------------------------- validacoes dos DTOs
def validacoes_dtos():
    """Le os *RequestDto.java e devolve [(dto, campo, tipo, [anotacoes legiveis])]."""
    linhas = []
    for arq in sorted(DTOS.glob("*RequestDto.java")):
        texto = arq.read_text(encoding="utf-8")
        pendentes = []
        for linha in texto.splitlines():
            linha = linha.strip()
            if linha.startswith("@"):
                m = re.match(r"@(\w+)(\((.*)\))?", linha)
                nome, args = m.group(1), m.group(3) or ""
                args = re.sub(r',?\s*message = "[^"]*"', "", args).strip(", ")
                pendentes.append(f"@{nome}" + (f"({args})" if args else ""))
            elif linha.startswith("private "):
                tipo, campo = linha.rstrip(";").split()[1:3]
                linhas.append((arq.stem, campo, tipo, pendentes))
                pendentes = []
    return linhas


# --------------------------------------------------------------------------- documento
class Documento(BaseDocTemplate):
    def __init__(self, arquivo):
        super().__init__(str(arquivo), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                         topMargin=2 * cm, bottomMargin=2 * cm,
                         title="ZelaBairro - Domain Driven Design Using Java",
                         author="Grupo ZelaBairro - FIAP 1TDSPV",
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
        canv.drawString(2 * cm, 1.2 * cm, f"ZelaBairro · Domain Driven Design Using Java · {TURMA}")
        canv.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
        canv.setStrokeColor(LINHA)
        canv.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
        canv.restoreState()


def capa():
    branco = ParagraphStyle("cb", fontName="Sans", fontSize=11, leading=15, textColor=colors.white)
    titulo = ParagraphStyle("ct", fontName="Sans-Bold", fontSize=34, leading=40,
                            textColor=colors.white)
    return [
        Spacer(1, 0.6 * cm),
        Paragraph("GLOBAL SOLUTION 2026/2 · CITIZENTECH · FIAP", branco),
        Spacer(1, 0.5 * cm),
        Paragraph("ZelaBairro", titulo),
        Paragraph("Zeladoria urbana colaborativa com priorização inteligente", branco),
        Spacer(1, 3.6 * cm),
        Paragraph("Domain Driven Design Using Java", ST["h1"]),
        p("Documentação técnica da API REST do ZelaBairro: Spring Boot, DAO com JDBC, DTOs com "
          "validação, exceções tratadas num handler global, CORS e deploy com Docker no Render."),
        Spacer(1, 0.4 * cm),
        tabela([["Integrante", "RM"]] + [[nome, rm] for rm, nome in INTEGRANTES],
               [12, 5], destaque_primeira_coluna=True),
        Spacer(1, 0.4 * cm),
        tabela([["Link", "Endereço"],
                ["API publicada (Render)", URL_API],
                ["Vídeo (YouTube, não listado)", URL_VIDEO],
                ["Repositório da API", URL_REPOSITORIO],
                ["Turma · Data", f"{TURMA} · {DATA}"]], [5, 12], destaque_primeira_coluna=True),
        NextPageTemplate("normal"),
        PageBreak(),
    ]


def conteudo():
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"]]
    s = [h2("Sumário"), toc, PageBreak()]

    # 1 ---------------------------------------------------------------------
    s += [h1("1. Capa e links"),
          p("Os integrantes, a turma e os links da API publicada e do vídeo estão na capa. "
            "Teste rápido da API no ar: <font name='Mono'>GET " + URL_API + "/health</font> deve "
            "responder <font name='Mono'>{\"status\":\"UP\",\"banco\":\"UP\"}</font>."),
          caixa("O plano gratuito do Render \"dorme\" após cerca de 15 minutos sem uso. Na correção "
                "ou na demonstração, abra <b>/health</b> e aguarde até 1 minuto na primeira chamada.",
                "atencao")]

    # 2 ---------------------------------------------------------------------
    s += [h1("2. A solução"),
          h2("2.1 O problema do cidadão"),
          p("Buraco na rua, poste apagado, lixo acumulado, árvore com risco de queda: o morador "
            "registra o problema no canal da prefeitura e depois não sabe se alguém viu, quanto "
            "tempo vai levar nem se outros vizinhos têm a mesma queixa. Do lado da prefeitura, a "
            "fila de chamados não mostra o que é mais urgente."),
          h2("2.2 Quem usa"),
          tabela([["Ator", "O que faz na API"],
                  ["Cidadão", "Cadastra-se, faz login, registra ocorrências com fotos, apoia "
                              "ocorrências de outros (\"eu também tenho esse problema\") e acompanha "
                              "o status e o histórico."],
                  ["Gestor da prefeitura", "Faz login, vê a fila por prioridade e o painel por bairro, "
                                           "muda o status das ocorrências e cadastra outros gestores."],
                  ["Serviço de IA (Flask)", "Chamado pela API ao criar a ocorrência: devolve o prazo "
                                            "previsto e o risco de atraso."]],
                 [4, 13], destaque_primeira_coluna=True),
          h2("2.3 O que a API resolve"),
          bullets([
              "Guarda no Oracle cidadãos, gestores, bairros, categorias, ocorrências, histórico de "
              "status, apoios e fotos, com as regras de negócio RN01–RN18 do grupo.",
              "Ordena as ocorrências por <b>prioridade</b> (RN10): gravidade da categoria, apoios, "
              "dias em aberto e risco de atraso. O gestor ataca primeiro o que mais importa.",
              "Mostra ao cidadão a <b>previsão de prazo</b> e o <b>risco de atraso</b> calculados pela "
              "IA. Se a IA estiver fora do ar, a ocorrência é criada mesmo assim (RN12).",
              "Protege as ações do gestor (RN16) e do autor das fotos (RN18) e devolve todo erro num "
              "JSON padronizado, sem stack trace nem SQL.",
          ]),
          h2("2.4 Arquitetura"),
          codigo("""
 Front-end (React, Vercel ou localhost:5173)
        │  HTTP + JSON, CORS (CORS_ORIGINS), cabeçalhos X-Gestor-Id / X-Cidadao-Id
        ▼
 API ZelaBairro (Spring Boot, Docker, Render)
   controller → dto (@Valid + ModelMapper) → bo (regras RNxx) → dao (JDBC) ──► Oracle FIAP
        │                                                                     (9 tabelas, sq_tb_*)
        └── ao criar a ocorrência: POST /prever/prazo e /prever/atraso ──► API de IA (Flask)
                                                                (IA_API_URL; fora do ar = RN12)
"""),
          PageBreak()]

    # 3 ---------------------------------------------------------------------
    s += [h1("3. Diagrama de classes"),
          p("Models do pacote <font name='Mono'>br.com.zelabairro.model</font>, com atributos, tipos "
            "e associações. As chaves estrangeiras viram <b>objetos</b> (ex.: a Ocorrencia tem um "
            "Cidadao, uma Categoria e um Bairro). As regras que dependem só dos dados da própria "
            "ocorrência (dias em aberto, atrasada, prioridade) ficam como métodos no model."),
          diagrama_classes(),
          Paragraph("Diagrama de classes dos models. Multiplicidades em laranja: 1 = um, * = muitos. "
                    "Os relacionamentos 1:N principais são Ocorrencia → Atualizacao (histórico) e "
                    "Bairro/Categoria/Cidadao → Ocorrencia.", ST["legenda"]),
          PageBreak()]

    # 4 ---------------------------------------------------------------------
    s += [h1("4. Modelo do banco (DER)"),
          p("Modelo relacional gerado no Oracle Data Modeler (o mesmo da entrega de Banco de Dados). "
            "Padrão de nomes da disciplina: tabelas <b>tb_</b>, chaves <b>cd_</b>, nomes <b>nm_</b>, "
            "textos <b>ds_</b>, datas <b>dt_</b>, números <b>nr_</b>, status <b>st_</b>, flags "
            "<b>fl_</b>, BLOB <b>bl_</b> e uma sequence <b>sq_tb_nome</b> por tabela (menos tb_apoio, "
            "de chave composta). O script completo é o <b>zelabairro.sql</b> da entrega."),
          imagem("der.png", "DER – tabelas com chave primária (P), estrangeira (F) e únicas (U)",
                 altura_max=11 * cm),
          tabela([["Relacionamento", "Tipo", "Chave estrangeira", "Rota aninhada na API"],
                  ["tb_ocorrencia → tb_atualizacao", "1:N", "tb_atualizacao.cd_ocorrencia",
                   "/ocorrencias/{id}/atualizacoes"],
                  ["tb_bairro → tb_ocorrencia", "1:N", "tb_ocorrencia.cd_bairro", "/bairros/{id}/ocorrencias"],
                  ["tb_categoria → tb_ocorrencia", "1:N", "tb_ocorrencia.cd_categoria",
                   "/categorias/{id}/ocorrencias"],
                  ["tb_cidadao → tb_ocorrencia", "1:N", "tb_ocorrencia.cd_cidadao (autor)", "—"],
                  ["tb_ocorrencia → tb_foto", "1:N", "tb_foto.cd_ocorrencia", "/ocorrencias/{id}/fotos"],
                  ["tb_cidadao ↔ tb_ocorrencia", "N:N", "associativa tb_apoio (PK composta)",
                   "/ocorrencias/{id}/apoios"],
                  ["tb_orgao → tb_categoria / tb_gestor", "1:N", "cd_orgao", "—"],
                  ["tb_gestor → tb_atualizacao", "1:N", "tb_atualizacao.cd_gestor", "—"],
                  ["tb_gestor → tb_gestor", "1:N", "cd_gestor_cadastro (RN17)", "—"]],
                 [5, 1.2, 5, 5.8]),
          PageBreak()]

    # 5 ---------------------------------------------------------------------
    s += [h1("5. Endpoints"),
          p("JSON em camelCase e datas no formato AAAA-MM-DD. <b>[G]</b> = rota de gestor: exige o "
            "cabeçalho <font name='Mono'>X-Gestor-Id</font> de um gestor existente (RN16), senão 403. "
            "<b>[A]</b> = só o autor da ocorrência, pelo cabeçalho <font name='Mono'>X-Cidadao-Id</font> "
            "(RN18). Método não suportado: 405. Erro inesperado: 500 com mensagem genérica."),
          tabela([["Método", "Rota", "Sucesso", "Erros"],
                  ["POST", "/auth/login", "200", "400, 401 (RN15)"],
                  ["POST", "/cidadaos", "201 + Location", "400, 409 (RN02)"],
                  ["GET", "/cidadaos · /cidadaos/{id}", "200", "404"],
                  ["PUT / DELETE", "/cidadaos/{id}", "200 / 204", "400, 404, 409"],
                  ["POST", "/gestores [G]", "201 + Location", "400, 403, 404, 409 (RN17)"],
                  ["GET", "/gestores · /gestores/{id} [G]", "200", "403, 404"],
                  ["PUT / DELETE", "/gestores/{id} [G]", "200 / 204", "400, 403, 404, 409"],
                  ["GET", "/orgaos · /orgaos/{id}", "200", "404"],
                  ["POST", "/bairros", "201 + Location", "400, 409"],
                  ["GET", "/bairros · /bairros/{id}", "200", "404"],
                  ["PUT / DELETE", "/bairros/{id}", "200 / 204", "400, 404, 409 (RN14)"],
                  ["GET", "/bairros/{id}/ocorrencias", "200", "404"],
                  ["POST", "/categorias", "201 + Location", "400, 404, 409"],
                  ["GET", "/categorias · /categorias/{id}", "200", "404"],
                  ["PUT / DELETE", "/categorias/{id}", "200 / 204", "400, 404, 409 (RN14)"],
                  ["GET", "/categorias/{id}/ocorrencias", "200", "404"],
                  ["POST", "/ocorrencias", "201 + Location", "400, 404 (FK inexistente)"],
                  ["GET", "/ocorrencias?status=&amp;idBairro=&amp;idCategoria=", "200 (por prioridade)", "400"],
                  ["GET", "/ocorrencias/{id}", "200", "404"],
                  ["PUT", "/ocorrencias/{id}", "200", "400, 404, 409 (RN09)"],
                  ["DELETE", "/ocorrencias/{id}", "204", "404, 409 (RN09)"],
                  ["GET", "/ocorrencias/{id}/atualizacoes · /{idAtualizacao}", "200", "404"],
                  ["POST", "/ocorrencias/{id}/atualizacoes [G]", "201 + Location", "400, 403, 404, 409 (RN05)"],
                  ["PUT", "/ocorrencias/{id}/atualizacoes/{idAtualizacao} [G]", "200", "400, 403, 404"],
                  ["GET", "/ocorrencias/{id}/apoios · /{idCidadao}", "200", "404"],
                  ["POST", "/ocorrencias/{id}/apoios", "201 + Location", "400, 404, 409 (RN08)"],
                  ["DELETE", "/ocorrencias/{id}/apoios/{idCidadao}", "204", "404"],
                  ["POST", "/ocorrencias/{id}/fotos [A] (multipart, campo arquivo)", "201 + Location",
                   "400, 403, 404, 409 (RN18)"],
                  ["GET", "/ocorrencias/{id}/fotos (sem os bytes)", "200", "404"],
                  ["GET", "/fotos/{idFoto} (a imagem)", "200 image/jpeg ou png", "404"],
                  ["DELETE", "/ocorrencias/{id}/fotos/{idFoto} [A]", "204", "403, 404, 409"],
                  ["GET", "/painel/bairros [G]", "200", "403"],
                  ["GET", "/health", "200 / 503", "—"]],
                 [2.2, 8.3, 3.2, 3.3]),
          PageBreak(),
          h2("5.1 Exemplos de JSON de entrada e de saída"),
          exemplo("POST /ocorrencias → 201 Created, Location: /ocorrencias/15", """
{
  "descricao": "Buraco grande na faixa da direita, perto do ponto de ônibus",
  "endereco": "Rua Guaicurus, 1200",
  "idCidadao": 2,
  "idCategoria": 1,
  "idBairro": 1
}""", """
{
  "id": 15,
  "descricao": "Buraco grande na faixa da direita, perto do ponto de ônibus",
  "endereco": "Rua Guaicurus, 1200",
  "status": "ABERTA",
  "dataAbertura": "2026-11-18",
  "dataResolucao": null,
  "categoria": { "id": 1, "nome": "Buraco na via", "descricao": "Buraco ou afundamento no asfalto da rua.",
                 "prazoDias": 15, "gravidade": 4, "idOrgao": 1, "orgao": "Subprefeitura - Zeladoria" },
  "bairro": { "id": 1, "nome": "Lapa", "subprefeitura": "Lapa", "populacao": 65739 },
  "idAutor": 2,
  "autor": "Bruno",
  "prazoPrevistoDias": 16,
  "riscoAtraso": "ALTO",
  "qtdApoios": 0,
  "qtdFotos": 0,
  "diasEmAberto": 0,
  "atrasada": false,
  "pontuacaoPrioridade": 55,
  "prioridade": "MEDIA"
}"""),
          caixa("<b>Como ler a prioridade (RN10):</b> 4 (gravidade) × 10 + 0 apoios × 2 + 0 dias + 15 "
                "(risco de atraso ALTO previsto pela IA) = <b>55 → MEDIA</b>. O <b>autor</b> mostra só o "
                "primeiro nome (RN13). <b>riscoAtraso</b> aparece como ALTO/BAIXO, sem porcentagem (D4); "
                "<b>prazoPrevistoDias</b> e <b>riscoAtraso</b> vêm nulos quando a IA está fora do ar (RN12) "
                "ou na categoria Iluminação pública apagada (D3)."),
          exemplo("POST /cidadaos → 201 Created, Location: /cidadaos/9", """
{ "nome": "Mariana Lopes", "email": "mariana@email.exemplo.com", "senha": "******", "telefone": "(11) 98888-7777" }""", """
{ "id": 9, "nome": "Mariana Lopes", "email": "mariana@email.exemplo.com",
  "telefone": "(11) 98888-7777", "dataCadastro": "2026-11-18" }        // a senha nunca volta"""),
          exemplo("POST /auth/login → 200 OK", """
{ "email": "mariana@email.exemplo.com", "senha": "******" }""", """
{ "id": 9, "nome": "Mariana Lopes", "perfil": "CIDADAO" }             // ou "GESTOR\""""),
          exemplo("POST /ocorrencias/15/atualizacoes [X-Gestor-Id: 1] → 201 Created", """
{ "status": "EM_ANDAMENTO", "comentario": "Equipe agendada" }""", """
{ "id": 10, "idOcorrencia": 15, "statusAnterior": "ABERTA", "statusNovo": "EM_ANDAMENTO",
  "comentario": "Equipe agendada", "data": "2026-11-18", "idGestor": 1, "gestor": "Marcia Oliveira Santos" }"""),
          exemplo("POST /ocorrencias/15/apoios → 201 Created", """
{ "idCidadao": 3 }""", """
{ "idOcorrencia": 15, "idCidadao": 3, "cidadao": "Carla", "dataApoio": "2026-11-18" }"""),
          exemplo("POST /ocorrencias/15/fotos [X-Cidadao-Id: 2] (multipart, campo \"arquivo\") → 201", None, """
{ "id": 4, "tipo": "image/png", "tamanho": 183402, "dataEnvio": "2026-11-18", "url": "/fotos/4" }"""),
          exemplo("POST /bairros → 201 · POST /categorias → 201", """
{ "nome": "Vila Madalena", "subprefeitura": "Pinheiros", "populacao": 50000 }
{ "nome": "Pichação", "descricao": "Pichação em muro.", "prazoDias": 20, "gravidade": 2, "idOrgao": 1 }""", """
{ "id": 7, "nome": "Vila Madalena", "subprefeitura": "Pinheiros", "populacao": 50000 }
{ "id": 9, "nome": "Pichação", "descricao": "Pichação em muro.", "prazoDias": 20, "gravidade": 2,
  "idOrgao": 1, "orgao": "Subprefeitura - Zeladoria" }"""),
          exemplo("POST /gestores [X-Gestor-Id: 1] → 201", """
{ "nome": "Carlos Gestor", "email": "carlos@prefeitura.exemplo.gov.br", "senha": "******", "idOrgao": 1 }""", """
{ "id": 4, "nome": "Carlos Gestor", "email": "carlos@prefeitura.exemplo.gov.br", "idOrgao": 1,
  "orgao": "Subprefeitura - Zeladoria", "idGestorCadastro": 1, "dataCadastro": "2026-11-18" }"""),
          h2("5.2 Formato padrão de erro"),
          p("Todo erro, inclusive 404 de rota e 405, sai neste JSON pelo <b>GlobalExceptionHandler</b> "
            "(@RestControllerAdvice). O detalhe técnico fica só no log do servidor."),
          exemplo("400 – POST /ocorrencias com dados inválidos", """
{ "descricao": "curta", "endereco": "", "idCidadao": null, "idCategoria": 1, "idBairro": 1 }""", """
{
  "status": 400,
  "erro": "Requisição inválida",
  "mensagem": "Um ou mais campos estão inválidos.",
  "caminho": "/ocorrencias",
  "timestamp": "2026-11-18T01:39:33",
  "campos": [
    { "campo": "descricao", "mensagem": "RN03: a descrição deve ter de 10 a 500 caracteres." },
    { "campo": "endereco", "mensagem": "Informe o endereço de referência." },
    { "campo": "idCidadao", "mensagem": "Informe o cidadão autor." }
  ]
}"""),
          exemplo("404 · 409 · 403 · 401 · 405 · 500", None, """
{"status":404,"erro":"Não encontrado","mensagem":"Ocorrência 999999 não encontrada.","caminho":"/ocorrencias/999999",...,"campos":[]}
{"status":409,"erro":"Regra de negócio violada","mensagem":"RN05: transição de ABERTA para RESOLVIDA não é permitida.",...}
{"status":403,"erro":"Acesso negado","mensagem":"RN16: rota exclusiva de gestor. Envie um X-Gestor-Id válido.",...}
{"status":401,"erro":"Não autorizado","mensagem":"RN15: e-mail ou senha inválidos.",...}
{"status":405,"erro":"Método não permitido","mensagem":"O método PATCH não é suportado nesta rota.",...}
{"status":500,"erro":"Erro interno","mensagem":"Não foi possível concluir a operação. Tente novamente mais tarde.",...}"""),
          PageBreak()]

    # 6 ---------------------------------------------------------------------
    s += [h1("6. Estrutura do projeto"),
          tabela([["Pacote", "Responsabilidade", "Classes"],
                  ["model", "Entidades do domínio, sem anotação de framework. FKs como objetos e "
                            "regras do próprio dado como métodos (RN10, RN11, RN13).",
                   "Cidadao, Gestor, Orgao, Bairro, Categoria, Ocorrencia, Atualizacao, Apoio, Foto; "
                   "enums StatusOcorrencia, Prioridade, Perfil"],
                  ["dao", "Acesso ao banco com JDBC puro: um DAO por tabela, <b>DataSource recebido pelo "
                          "construtor</b>, PreparedStatement, try-with-resources e ids por "
                          "<b>sq_tb_*.NEXTVAL</b>. Sem JPA, Hibernate ou Spring Data.",
                   "OrgaoDao, BairroDao, CidadaoDao, GestorDao, CategoriaDao, OcorrenciaDao, "
                   "AtualizacaoDao, ApoioDao, FotoDao"],
                  ["bo", "Regras de negócio RNxx com exceções próprias, controle de acesso pelos "
                         "cabeçalhos, transações (commit/rollback) e chamada à IA.",
                   "AcessoBo, AuthBo, CidadaoBo, GestorBo, BairroBo, CategoriaBo, OcorrenciaBo, "
                   "AtualizacaoBo, ApoioBo, FotoBo, PainelBo, PrevisaoIaBo"],
                  ["dto", "Entrada (com Bean Validation) e saída da API: nunca recebe nem devolve o "
                          "model. Conversão com ModelMapper.",
                   "*RequestDto, *ResponseDto, CidadaoResumoDto, PainelBairroDto, ErroResponseDto, "
                   "CampoErroDto, OcorrenciaConversor"],
                  ["controller", "Rotas REST e status HTTP: 201 + Location, 200, 204.",
                   "AuthController, CidadaoController, GestorController, OrgaoController, "
                   "BairroController, CategoriaController, OcorrenciaController, AtualizacaoController, "
                   "ApoioController, FotoController, PainelController, HealthController"],
                  ["exception", "Erros do domínio, cada um com seu status.",
                   "EntidadeNaoEncontradaException (404), RegraNegocioException (409), "
                   "ConflitoException (409), CredenciaisInvalidasException (401), "
                   "AcessoNegadoException (403), DadosInvalidosException (400)"],
                  ["handler", "JSON de erro padronizado para toda exceção, sem stack trace nem SQL.",
                   "GlobalExceptionHandler (@RestControllerAdvice)"],
                  ["config", "CORS lendo CORS_ORIGINS (libera X-Gestor-Id e X-Cidadao-Id), "
                             "ModelMapper e BCrypt.",
                   "CorsFilter, ModelMapperConfig, SenhaConfig"]],
                 [2.2, 7.3, 7.5], destaque_primeira_coluna=True),
          h2("6.1 Caminho de uma requisição (POST /ocorrencias)"),
          codigo("""
1. CorsFilter            confere a origem (CORS_ORIGINS) e libera os cabeçalhos
2. OcorrenciaController  @Valid @RequestBody OcorrenciaRequestDto  → 400 se inválido (handler)
                         ModelMapper: DTO → model Ocorrencia (+ ids de cidadão, categoria e bairro)
3. OcorrenciaBo          RN01: cidadão, categoria e bairro existem? (DAOs) → senão 404
                         RN04: status ABERTA, abertura = hoje
                         PrevisaoIaBo: chama a IA uma vez (timeout curto; RN12 e D3)
4. OcorrenciaDao         INSERT ... VALUES (sq_tb_ocorrencia.NEXTVAL, ?, ...) com PreparedStatement
5. Oracle                grava em tb_ocorrencia
6. Volta                 model → OcorrenciaResponseDto (OcorrenciaConversor: RN10, RN11, RN13)
                         201 Created + Location: /ocorrencias/{id}
"""),
          p("Exemplo de DAO (trecho real do <b>BairroDao</b>):"),
          codigo("""
public BairroDao(DataSource dataSource) {          // DataSource recebido pelo construtor
    this.dataSource = dataSource;
}
public void cadastrar(Bairro bairro) throws SQLException {
    try (Connection conexao = dataSource.getConnection();
         PreparedStatement stmt = conexao.prepareStatement(INSERT_SQL, new String[] {"cd_bairro"})) {
        preencher(stmt, bairro);                   // INSERT ... VALUES (sq_tb_bairro.NEXTVAL, ?, ?, ?)
        stmt.executeUpdate();
        try (ResultSet chave = stmt.getGeneratedKeys()) {
            if (chave.next()) bairro.setId(chave.getInt(1));
        }
    }
}"""),
          PageBreak()]

    # 7 ---------------------------------------------------------------------
    s += [h1("7. Regras e validações"),
          h2("7.1 Regras de negócio além do CRUD"),
          p("Os códigos RN são os mesmos do Documento Base do grupo (usados também no banco, no Python "
            "e no front). Cada regra violada lança uma exceção própria, que o handler transforma no "
            "status indicado."),
          tabela([["Código", "Regra", "Onde", "Exceção → status"],
                  ["RN01", "Toda ocorrência tem 1 autor, 1 categoria e 1 bairro existentes.",
                   "OcorrenciaBo", "EntidadeNaoEncontrada → 404"],
                  ["RN02", "E-mail único; o mesmo e-mail não existe como cidadão e como gestor.",
                   "CidadaoBo, GestorBo", "Conflito → 409"],
                  ["RN04", "Nasce ABERTA, com abertura = hoje.", "OcorrenciaBo", "—"],
                  ["RN05", "Transições: ABERTA→EM_ANDAMENTO/CANCELADA; EM_ANDAMENTO→RESOLVIDA/CANCELADA. "
                           "RESOLVIDA e CANCELADA são finais.",
                   "StatusOcorrencia.podeIrPara, AtualizacaoBo", "RegraNegocio → 409"],
                  ["RN06", "Status só muda criando uma atualização (INSERT + UPDATE na mesma transação, "
                           "com SELECT ... FOR UPDATE); RESOLVIDA preenche a data de resolução; guarda o gestor.",
                   "AtualizacaoBo", "—"],
                  ["RN08", "Apoia no máximo uma vez, nunca a própria ocorrência e só ABERTA/EM_ANDAMENTO.",
                   "ApoioBo", "RegraNegocio → 409"],
                  ["RN09", "Edita só enquanto ABERTA; com apoios ou atualizações não exclui (deve ser CANCELADA).",
                   "OcorrenciaBo", "RegraNegocio → 409"],
                  ["RN10", "Prioridade = gravidade×10 + min(apoios,20)×2 + min(dias,30) + 15 (risco ou "
                           "atraso). ≥70 ALTA, 40–69 MEDIA, &lt;40 BAIXA. Lista ordenada por ela.",
                   "Ocorrencia, OcorrenciaBo", "—"],
                  ["RN11", "Atrasada = dias em aberto &gt; prazo de referência da categoria.",
                   "Ocorrencia.isAtrasada", "—"],
                  ["RN12", "IA fora do ar ou lenta: a ocorrência nasce sem previsão. A IA nunca bloqueia.",
                   "PrevisaoIaBo", "—"],
                  ["RN13", "Listagens públicas mostram só o primeiro nome do cidadão, sem e-mail/telefone.",
                   "Cidadao.getPrimeiroNome, DTOs", "—"],
                  ["RN14", "Bairro e categoria com ocorrências não são excluídos.",
                   "BairroBo, CategoriaBo", "RegraNegocio → 409"],
                  ["RN15", "Senha só como hash BCrypt, nunca devolvida; login errado → mensagem genérica.",
                   "AuthBo", "CredenciaisInvalidas → 401"],
                  ["RN16", "Só gestor muda status, vê o painel e cadastra gestores (X-Gestor-Id conferido "
                           "no banco a cada requisição).", "AcessoBo", "AcessoNegado → 403"],
                  ["RN17", "Gestor só é criado por outro gestor; fica registrado quem cadastrou.",
                   "GestorBo", "AcessoNegado → 403"],
                  ["RN18", "Fotos: só o autor (X-Cidadao-Id), só ABERTA, no máximo 3, JPG/PNG até 2 MB "
                           "(tipo conferido pelos bytes do arquivo).",
                   "FotoBo", "403 · 409 · DadosInvalidos → 400"],
                  ["D3", "Iluminação pública apagada: sem histórico na IA → previsão nula.",
                   "PrevisaoIaBo", "—"]],
                 [1.3, 8.4, 3.6, 3.7], destaque_primeira_coluna=True),
          h2("7.2 Validações de cada DTO de entrada (Bean Validation, ativada com @Valid)"),
          p("Tabela gerada a partir do código dos DTOs. Qualquer violação devolve <b>400</b> com a lista "
            "<font name='Mono'>campos</font>; as mensagens estão em português no próprio DTO.")]
    linhas = [["DTO", "Campo", "Tipo", "Validações"]]
    for dto, campo, tipo, anots in validacoes_dtos():
        linhas.append([dto, campo, tipo, " ".join(anots) or "—"])
    s += [tabela(linhas, [4.6, 2.6, 1.6, 8.2]),
          Spacer(1, 6),
          p("Validações que dependem do banco ou de outro campo ficam no BO: e-mail repetido (409), "
            "FK inexistente (404), tipo e tamanho da foto (400), status inválido no filtro (400)."),
          PageBreak()]

    # 8 ---------------------------------------------------------------------
    s += [h1("8. Deploy"),
          p("A API roda num container Docker publicado no <b>Render</b> (Web Service, linguagem Docker), "
            "a partir do repositório GitHub da API. O Dockerfile é multi-stage: a primeira etapa compila "
            "com o JDK 21 e o Maven Wrapper; a segunda leva só o .jar para uma imagem com o JRE 21."),
          codigo("""
FROM eclipse-temurin:21-jdk AS build
WORKDIR /app
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN chmod +x mvnw && ./mvnw -B -q dependency:go-offline
COPY src/ src/
RUN ./mvnw -B -q package -DskipTests

FROM eclipse-temurin:21-jre
WORKDIR /app
ENV TZ=America/Sao_Paulo
COPY --from=build /app/target/zelabairro-api.jar app.jar
EXPOSE 8080
ENTRYPOINT ["sh", "-c", "java -Xmx384m -jar app.jar"]"""),
          h2("8.1 Variáveis de ambiente (somente os nomes)"),
          p("Nenhuma credencial está no código, no application.properties, no README ou neste PDF. "
            "O application.properties só referencia as variáveis, por exemplo "
            "<font name='Mono'>spring.datasource.password=${DB_PASSWORD}</font>."),
          tabela([["Variável", "Obrigatória", "Uso"],
                  ["DB_URL", "sim", "URL JDBC do Oracle da FIAP"],
                  ["DB_USER", "sim", "Usuário do banco"],
                  ["DB_PASSWORD", "sim", "Senha do banco"],
                  ["CORS_ORIGINS", "sim", "Origens do front separadas por vírgula (localhost do Vite e URL da Vercel)"],
                  ["IA_API_URL", "não", "URL da API de IA (Flask). Vazia ou fora do ar: RN12"],
                  ["PORT", "não", "Definida pelo próprio Render (padrão 8080)"],
                  ["IA_TIMEOUT_MS · DB_POOL_SIZE", "não", "Timeout da IA (4000 ms) e pool de conexões (4)"]],
                 [4.5, 2, 10.5], destaque_primeira_coluna=True),
          h2("8.2 Passo a passo no Render"),
          bullets([
              "New → Web Service → conectar o repositório GitHub da API → Language: <b>Docker</b>.",
              "Environment: criar DB_URL, DB_USER, DB_PASSWORD, CORS_ORIGINS e IA_API_URL com os valores do grupo.",
              "Advanced → Health Check Path: <b>/health</b> (responde 200 com o banco no ar e 503 sem ele).",
              "Create Web Service; ao final do build, testar <font name='Mono'>" + URL_API + "/health</font>.",
          ]),
          h2("8.3 Como a API foi testada"),
          p("Antes do deploy, a API foi testada com o <b>zelabairro.sql</b> executado do zero num Oracle "
            "local: o script <font name='Mono'>testes/testar_endpoints.sh</font> faz 117 verificações "
            "com curl (todas as rotas da seção 5, os status 201 + Location, 200, 204, 400 com campos, "
            "401, 403, 404, 405 e 409, o CORS e a ausência de senha nas respostas) e todas passaram. "
            "A integração com a IA foi testada com a Flask ligada (prazo e risco gravados), com a "
            "categoria Iluminação (previsão nula, D3) e com a Flask desligada (ocorrência criada sem "
            "previsão, RN12). A imagem Docker foi gerada e executada localmente. A coleção "
            "<b>ZelaBairro.postman_collection.json</b> repete esses testes no Postman/Insomnia, com uma "
            "pasta só de erros para a demonstração ao vivo.")]
    return s


if __name__ == "__main__":
    doc = Documento(SAIDA)
    doc.multiBuild(capa() + conteudo())
    print(f"PDF gerado: {SAIDA}")
    if "[COLOCAR" in URL_API or "[COLOCAR" in URL_VIDEO:
        print("Atenção: preencha URL_API, URL_VIDEO e URL_REPOSITORIO no topo do script e gere de novo.")
