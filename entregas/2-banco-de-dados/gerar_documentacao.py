"""Gera documentacao.pdf da entrega de Building Relational Database (ZelaBairro).

Uso (nesta pasta):  uv run --with reportlab python gerar_documentacao.py
Entrada: zelabairro.sql (as 10 consultas, o UPDATE e o DELETE sao lidos dele, para o
         PDF nunca ficar diferente do script) e as imagens da pasta imagens/.
Saida:   documentacao.pdf nesta pasta.

Imagens esperadas em imagens/ (veja GUIA_EXECUCAO.md). Enquanto uma imagem nao existe,
o PDF mostra um quadro "INSERIR IMAGEM" no lugar dela.
"""
import re
from pathlib import Path

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
SQL = PASTA / "zelabairro.sql"
IMAGENS = PASTA / "imagens"
SAIDA = PASTA / "documentacao.pdf"
DATA = "19/11/2026"

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


PENDENTES = []


def imagem(arquivo, legenda, altura_max=21 * cm):
    """Insere imagens/<arquivo>; se ainda nao existir, desenha um quadro reservado."""
    caminho = IMAGENS / arquivo
    if caminho.exists():
        largura_px, altura_px = ImageReader(str(caminho)).getSize()
        escala = min(LARGURA / largura_px, altura_max / altura_px)
        figura = Image(str(caminho), width=largura_px * escala, height=altura_px * escala)
    else:
        PENDENTES.append(arquivo)
        figura = Table([[p(f"<b>INSERIR IMAGEM</b><br/>Salve o arquivo <b>imagens/{arquivo}</b> "
                           "e rode de novo <i>gerar_documentacao.py</i> (ver GUIA_EXECUCAO.md).")]],
                       colWidths=[LARGURA], rowHeights=[4.2 * cm])
        figura.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1.2, AMBAR), ("BACKGROUND", (0, 0), (-1, -1), AMBAR_CLARO),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ]))
    return KeepTogether([figura, Paragraph(legenda, ST["legenda"])])


# --------------------------------------------------------------------------- leitura do .sql
def ler_sql():
    """Devolve (consultas, update, delete) extraidos de zelabairro.sql."""
    texto = SQL.read_text(encoding="utf-8")
    parte3 = texto.split("PARTE 3 - 10 CONSULTAS")[1].split("PARTE 4 - UPDATE")[0]
    blocos = re.split(r"^-- CONSULTA (\d{2}) -+\n", parte3, flags=re.M)[1:]
    consultas = []
    for numero, corpo in zip(blocos[0::2], blocos[1::2]):
        corpo = corpo.split("/* ====")[0].strip()
        comentarios, sql = [], []
        for linha in corpo.splitlines():
            (comentarios if linha.startswith("--") and not sql else sql).append(linha)
        texto_com = " ".join(l.lstrip("- ").strip() for l in comentarios)
        pergunta = texto_com.split("Recursos:")[0].replace("Pergunta:", "").strip()
        recursos = texto_com.split("Recursos:")[1].strip() if "Recursos:" in texto_com else ""
        pergunta = pergunta[:1].upper() + pergunta[1:]
        consultas.append((numero, pergunta, recursos, "\n".join(sql).strip()))

    def comando(inicio, fim):
        trecho = texto.split(inicio)[1]
        trecho = trecho.split("*/", 1)[1]
        return trecho.split(fim)[0].strip()

    update = comando("PARTE 4 - UPDATE COM WHERE", "COMMIT;")
    delete = comando("PARTE 5 - DELETE COM WHERE", "COMMIT;")
    return consultas, update, delete


# --------------------------------------------------------------------------- documento
class Documento(BaseDocTemplate):
    def __init__(self, arquivo):
        super().__init__(str(arquivo), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                         topMargin=2 * cm, bottomMargin=2 * cm,
                         title="ZelaBairro - Building Relational Database",
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
        canv.drawString(2 * cm, 1.2 * cm, f"ZelaBairro · Building Relational Database · {TURMA}")
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
        Paragraph("Building Relational Database", ST["h1"]),
        p("Levantamento de requisitos, modelos conceitual, lógico e relacional, dicionário de "
          "dados, script Oracle e as 10 consultas do banco do ZelaBairro."),
        Spacer(1, 0.4 * cm),
        tabela([["Integrante", "RM"]] + [[nome, rm] for rm, nome in INTEGRANTES],
               [12, 5], destaque_primeira_coluna=True),
        Spacer(1, 0.4 * cm),
        tabela([["Campo", "Valor"],
                ["Turma", TURMA],
                ["Disciplina", "Building Relational Database (Oracle SQL Developer e Data Modeler)"],
                ["Arquivos da entrega", "documentacao.pdf, zelabairro.sql e identificacao.txt"],
                ["Data", DATA]], [5, 12], destaque_primeira_coluna=True),
        NextPageTemplate("normal"),
        PageBreak(),
    ]


# Dicionario de dados: (coluna, tipo, tamanho, nulo, chave, restricao, significado)
DICIONARIO = [
    ("tb_orgao", "Órgãos da prefeitura que executam os serviços (ex.: Iluminação Pública).", [
        ("cd_orgao", "NUMBER", "10", "Não", "PK", "sequence sq_tb_orgao", "Código do órgão"),
        ("nm_orgao", "VARCHAR2", "100", "Não", "UK", "UNIQUE", "Nome do órgão"),
        ("ds_email", "VARCHAR2", "120", "Não", "", "", "E-mail de contato do órgão"),
        ("nr_telefone", "VARCHAR2", "20", "Sim", "", "", "Telefone de contato"),
    ]),
    ("tb_bairro", "Bairros/distritos atendidos e sua subprefeitura.", [
        ("cd_bairro", "NUMBER", "10", "Não", "PK", "sequence sq_tb_bairro", "Código do bairro"),
        ("nm_bairro", "VARCHAR2", "80", "Não", "UK", "UNIQUE (nm_bairro, nm_subprefeitura)",
         "Nome do bairro/distrito"),
        ("nm_subprefeitura", "VARCHAR2", "80", "Não", "UK", "UNIQUE (com nm_bairro)",
         "Subprefeitura, com o mesmo nome usado no SP156 e na API de IA"),
        ("nr_populacao", "NUMBER", "9", "Sim", "", "CHECK (nr_populacao &gt; 0)",
         "População aproximada do distrito"),
    ]),
    ("tb_cidadao", "Quem registra e apoia ocorrências. Sem CPF nem endereço (RN02, LGPD).", [
        ("cd_cidadao", "NUMBER", "10", "Não", "PK", "sequence sq_tb_cidadao", "Código do cidadão"),
        ("nm_cidadao", "VARCHAR2", "100", "Não", "", "", "Nome completo"),
        ("ds_email", "VARCHAR2", "120", "Não", "UK", "UNIQUE (RN02)", "E-mail de login"),
        ("ds_senha", "VARCHAR2", "100", "Não", "", "Somente hash BCrypt (RN15)",
         "Hash da senha; a senha em texto nunca é gravada"),
        ("nr_telefone", "VARCHAR2", "20", "Sim", "", "", "Telefone opcional"),
        ("dt_cadastro", "DATE", "—", "Não", "", "DEFAULT SYSDATE", "Data do cadastro"),
    ]),
    ("tb_gestor", "Servidores da prefeitura que acessam o painel (RN16).", [
        ("cd_gestor", "NUMBER", "10", "Não", "PK", "sequence sq_tb_gestor", "Código do gestor"),
        ("nm_gestor", "VARCHAR2", "100", "Não", "", "", "Nome completo"),
        ("ds_email", "VARCHAR2", "120", "Não", "UK", "UNIQUE (RN02)", "E-mail de login"),
        ("ds_senha", "VARCHAR2", "100", "Não", "", "Somente hash BCrypt (RN15)", "Hash da senha"),
        ("cd_orgao", "NUMBER", "10", "Não", "FK", "→ tb_orgao", "Órgão onde o gestor trabalha"),
        ("cd_gestor_cadastro", "NUMBER", "10", "Sim", "FK", "→ tb_gestor (autorrelacionamento, RN17)",
         "Gestor que fez o cadastro; nulo só no gestor inicial do seed"),
        ("dt_cadastro", "DATE", "—", "Não", "", "DEFAULT SYSDATE", "Data do cadastro"),
    ]),
    ("tb_categoria", "Tipos de problema, com prazo de referência e gravidade.", [
        ("cd_categoria", "NUMBER", "10", "Não", "PK", "sequence sq_tb_categoria",
         "Código da categoria"),
        ("nm_categoria", "VARCHAR2", "60", "Não", "UK", "UNIQUE", "Nome canônico da categoria"),
        ("ds_categoria", "VARCHAR2", "255", "Sim", "", "", "Explicação para o cidadão"),
        ("nr_prazo_dias", "NUMBER", "3", "Não", "", "CHECK (nr_prazo_dias &gt; 0)",
         "Prazo de referência em dias (base da RN11)"),
        ("nr_gravidade", "NUMBER", "1", "Não", "", "CHECK (BETWEEN 1 AND 5)",
         "Peso da categoria na prioridade (RN10); 5 = risco à segurança"),
        ("cd_orgao", "NUMBER", "10", "Não", "FK", "→ tb_orgao", "Órgão responsável"),
    ]),
    ("tb_ocorrencia", "O problema registrado pelo cidadão, com status, datas e previsão da IA.", [
        ("cd_ocorrencia", "NUMBER", "10", "Não", "PK", "sequence sq_tb_ocorrencia",
         "Código da ocorrência"),
        ("ds_ocorrencia", "VARCHAR2", "500", "Não", "", "CHECK (LENGTH BETWEEN 10 AND 500) (RN03)",
         "Descrição do problema"),
        ("ds_endereco", "VARCHAR2", "200", "Não", "", "Obrigatório, até 200 (RN03)",
         "Endereço de referência"),
        ("st_ocorrencia", "VARCHAR2", "15", "Não", "", "DEFAULT 'ABERTA'; CHECK IN (ABERTA, "
         "EM_ANDAMENTO, RESOLVIDA, CANCELADA) (RN04)", "Status atual"),
        ("dt_abertura", "DATE", "—", "Não", "", "DEFAULT SYSDATE (RN04)", "Data de abertura"),
        ("dt_resolucao", "DATE", "—", "Sim", "", "CHECK (nula ou &gt;= dt_abertura)",
         "Preenchida quando a ocorrência é resolvida (RN06)"),
        ("nr_prazo_previsto", "NUMBER", "4", "Sim", "", "Nulo se a IA estiver fora (RN12)",
         "Dias previstos pela IA para resolver"),
        ("fl_risco_atraso", "CHAR", "1", "Sim", "", "CHECK IN ('S','N')",
         "Previsão da IA de que vai atrasar"),
        ("cd_cidadao", "NUMBER", "10", "Não", "FK", "→ tb_cidadao (RN01)", "Autor da ocorrência"),
        ("cd_categoria", "NUMBER", "10", "Não", "FK", "→ tb_categoria (RN01, RN14)",
         "Categoria do problema"),
        ("cd_bairro", "NUMBER", "10", "Não", "FK", "→ tb_bairro (RN01, RN14)", "Bairro do problema"),
    ]),
    ("tb_atualizacao", "Histórico de mudanças de status, com o gestor que mudou (RN05, RN06).", [
        ("cd_atualizacao", "NUMBER", "10", "Não", "PK", "sequence sq_tb_atualizacao",
         "Código da atualização"),
        ("cd_ocorrencia", "NUMBER", "10", "Não", "FK", "→ tb_ocorrencia", "Ocorrência atualizada"),
        ("st_anterior", "VARCHAR2", "15", "Não", "", "", "Status antes da mudança"),
        ("st_novo", "VARCHAR2", "15", "Não", "", "CHECK IN (mesmos 4 status) (RN04)",
         "Status depois da mudança"),
        ("ds_comentario", "VARCHAR2", "300", "Sim", "", "", "Comentário do gestor"),
        ("cd_gestor", "NUMBER", "10", "Não", "FK", "→ tb_gestor (RN06)", "Quem fez a atualização"),
        ("dt_atualizacao", "DATE", "—", "Não", "", "DEFAULT SYSDATE", "Data da atualização"),
    ]),
    ("tb_apoio", "Associativa do N:N cidadão ↔ ocorrência (\"eu também tenho esse problema\").", [
        ("cd_cidadao", "NUMBER", "10", "Não", "PK, FK", "PK composta (RN08); → tb_cidadao",
         "Cidadão que apoia"),
        ("cd_ocorrencia", "NUMBER", "10", "Não", "PK, FK", "PK composta (RN08); → tb_ocorrencia",
         "Ocorrência apoiada"),
        ("dt_apoio", "DATE", "—", "Não", "", "DEFAULT SYSDATE", "Data do apoio"),
    ]),
    ("tb_foto", "Fotos do problema, guardadas como BLOB (RN18).", [
        ("cd_foto", "NUMBER", "10", "Não", "PK", "sequence sq_tb_foto", "Código da foto"),
        ("cd_ocorrencia", "NUMBER", "10", "Não", "FK", "→ tb_ocorrencia", "Ocorrência da foto"),
        ("bl_imagem", "BLOB", "até 2 MB", "Não", "", "", "Bytes do arquivo de imagem"),
        ("ds_tipo", "VARCHAR2", "20", "Não", "", "CHECK IN ('image/jpeg','image/png') (RN18)",
         "Tipo do arquivo"),
        ("nr_tamanho", "NUMBER", "8", "Não", "", "CHECK (BETWEEN 1 AND 2097152) (RN18)",
         "Tamanho em bytes (até 2 MB)"),
        ("dt_envio", "DATE", "—", "Não", "", "DEFAULT SYSDATE", "Data do envio"),
    ]),
]

RELACIONAMENTOS = [
    ["Orgao → Categoria (responsavel_por)", "1:N", "Um órgão é responsável por várias categorias",
     "tb_categoria.cd_orgao"],
    ["Orgao → Gestor (lota)", "1:N", "Um órgão tem vários gestores", "tb_gestor.cd_orgao"],
    ["Gestor → Gestor (cadastra)", "1:N", "Um gestor cadastra outros gestores (RN17)",
     "tb_gestor.cd_gestor_cadastro"],
    ["Categoria → Ocorrencia (classifica)", "1:N", "Uma categoria classifica várias ocorrências",
     "tb_ocorrencia.cd_categoria"],
    ["Bairro → Ocorrencia (localiza)", "1:N", "Um bairro tem várias ocorrências",
     "tb_ocorrencia.cd_bairro"],
    ["Cidadao → Ocorrencia (registra)", "1:N", "Um cidadão é autor de várias ocorrências (RN01)",
     "tb_ocorrencia.cd_cidadao"],
    ["Ocorrencia → Atualizacao (possui)", "1:N", "Uma ocorrência tem várias atualizações de status",
     "tb_atualizacao.cd_ocorrencia"],
    ["Gestor → Atualizacao (realiza)", "1:N", "Um gestor faz várias atualizações (RN06)",
     "tb_atualizacao.cd_gestor"],
    ["Ocorrencia → Foto (contem)", "1:N", "Uma ocorrência tem até 3 fotos (RN18)",
     "tb_foto.cd_ocorrencia"],
    ["Cidadao ↔ Ocorrencia (apoia)", "N:N", "Um cidadão apoia várias ocorrências e uma ocorrência "
     "recebe vários apoios (RN08)", "associativa tb_apoio (cd_cidadao, cd_ocorrencia)"],
]

RELACIONAL = """
tb_orgao       (cd_orgao, nm_orgao, ds_email, nr_telefone)
tb_bairro      (cd_bairro, nm_bairro, nm_subprefeitura, nr_populacao)
tb_cidadao     (cd_cidadao, nm_cidadao, ds_email, ds_senha, nr_telefone, dt_cadastro)
tb_gestor      (cd_gestor, nm_gestor, ds_email, ds_senha, #cd_orgao, #cd_gestor_cadastro,
                dt_cadastro)
tb_categoria   (cd_categoria, nm_categoria, ds_categoria, nr_prazo_dias, nr_gravidade,
                #cd_orgao)
tb_ocorrencia  (cd_ocorrencia, ds_ocorrencia, ds_endereco, st_ocorrencia, dt_abertura,
                dt_resolucao, nr_prazo_previsto, fl_risco_atraso, #cd_cidadao,
                #cd_categoria, #cd_bairro)
tb_atualizacao (cd_atualizacao, #cd_ocorrencia, st_anterior, st_novo, ds_comentario,
                #cd_gestor, dt_atualizacao)
tb_apoio       (#cd_cidadao, #cd_ocorrencia, dt_apoio)
tb_foto        (cd_foto, #cd_ocorrencia, bl_imagem, ds_tipo, nr_tamanho, dt_envio)

Primeiro atributo de cada tabela = chave primária (em tb_apoio, a PK é o par
cd_cidadao + cd_ocorrencia). # = chave estrangeira.
"""


def conteudo():
    consultas, update, delete = ler_sql()
    s = []
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"]]
    toc.dotsMinLevel = 0
    s += [Paragraph("Sumário", ST["h1"]), toc, PageBreak()]

    # 1 ---------------------------------------------------------------------
    s += [h1("1. Levantamento de requisitos"),
          h2("1.1 Problema"),
          p("Moradores de cidades brasileiras convivem com problemas de <b>zeladoria urbana</b>: "
            "buraco na rua, poste apagado, lixo e entulho na calçada, árvore com risco de queda, "
            "bueiro entupido. O cidadão não sabe se o pedido foi recebido, quanto vai demorar nem "
            "se alguém já reclamou do mesmo problema; sem retorno, desiste de reclamar. A "
            "prefeitura recebe um volume enorme de chamados misturados, com duplicados e sem "
            "critério claro de urgência: um bueiro entupido antes da chuva fica na mesma fila que "
            "um pedido de poda. Problemas pequenos viram grandes e a desigualdade entre bairros "
            "cresce."),
          p("Evidência: o canal SP156 da Prefeitura de São Paulo recebe em média cerca de "
            "<b>157 mil solicitações por mês</b> (dados de 2022), publicadas no Portal de Dados "
            "Abertos. A IA do projeto foi treinada com 982.475 chamados reais desse conjunto."),
          h2("1.2 Público"),
          bullets([
              "<b>Cidadão</b> morador, em especial de bairros periféricos (onde a zeladoria "
              "costuma demorar mais) e pessoas com mobilidade reduzida, para quem uma calçada "
              "quebrada ou uma rua escura são barreiras reais.",
              "<b>Gestor da prefeitura</b>, que precisa decidir o que atender primeiro.",
          ]),
          h2("1.3 Objetivo da solução e papel do banco"),
          p("<b>O ZelaBairro é uma plataforma em que o cidadão registra e apoia problemas de "
            "zeladoria do seu bairro, e a prefeitura recebe esses chamados já agrupados, com "
            "prazo previsto e risco de atraso calculados por IA, para atender primeiro o que é "
            "mais urgente.</b>"),
          p("O banco Oracle é o centro da solução: guarda cidadãos, gestores, ocorrências, "
            "apoios, histórico de status e fotos, e é o mesmo banco usado pela API Java do "
            "projeto. Ele precisa responder às perguntas que tornam a fila justa e transparente "
            "(o que está atrasado, onde se concentram os problemas, quem atende o quê)."),
          h2("1.4 Atores"),
          tabela([["Ator", "O que faz", "Onde fica no banco"],
                  ["Cidadão", "Cria conta, registra ocorrências (com até 3 fotos), apoia "
                              "ocorrências de outros e acompanha o histórico",
                   "tb_cidadao, tb_ocorrencia, tb_apoio, tb_foto"],
                  ["Gestor da prefeitura", "Faz login, vê a fila por prioridade e o painel por "
                                           "bairro, muda status e cadastra outros gestores",
                   "tb_gestor, tb_atualizacao"],
                  ["Órgão responsável", "Equipe que executa o serviço; ligado à categoria",
                   "tb_orgao, tb_categoria"],
                  ["Serviço de IA", "Calcula prazo previsto e risco de atraso no registro",
                   "tb_ocorrencia.nr_prazo_previsto e fl_risco_atraso"],
                  ], [3.6, 8.2, 5.2], destaque_primeira_coluna=True),
          h2("1.5 Dados que o banco guarda"),
          tabela([["Tabela", "Guarda"]] + [[t, d] for t, d, _ in DICIONARIO], [3.6, 13.4],
                 destaque_primeira_coluna=True),
          Spacer(1, 6),
          p("Por que cidadão e gestor ficam em tabelas separadas: são papéis com dados "
            "diferentes (o gestor pertence a um órgão e registra quem o cadastrou), o que evita "
            "uma tabela genérica de usuário. Por LGPD, não guardamos CPF nem endereço do cidadão, "
            "e a senha fica só como hash BCrypt."),
          h2("1.6 Regras de negócio que o banco implementa"),
          tabela([["Regra", "O que diz", "Como aparece no banco"],
                  ["RN01", "Toda ocorrência tem 1 cidadão autor, 1 categoria e 1 bairro",
                   "FKs NOT NULL em tb_ocorrencia"],
                  ["RN02", "E-mail único para cidadão e para gestor; sem CPF/endereço",
                   "UNIQUE em ds_email"],
                  ["RN03", "Descrição de 10 a 500 caracteres; endereço obrigatório até 200",
                   "CHECK de LENGTH; NOT NULL"],
                  ["RN04", "Status ABERTA, EM_ANDAMENTO, RESOLVIDA, CANCELADA; nasce ABERTA hoje",
                   "CHECK IN + DEFAULT 'ABERTA' e SYSDATE"],
                  ["RN05/RN06", "Status muda por atualização, com o gestor; resolução preenche a "
                                "data", "tb_atualizacao.cd_gestor NOT NULL; CHECK de datas"],
                  ["RN08", "Cidadão apoia uma ocorrência no máximo uma vez",
                   "PK composta de tb_apoio"],
                  ["RN10", "Prioridade da fila considera a gravidade da categoria (1 a 5)",
                   "nr_gravidade com CHECK BETWEEN 1 AND 5"],
                  ["RN11", "Atrasada = dias em aberto &gt; prazo da categoria",
                   "nr_prazo_dias com CHECK; consulta 03"],
                  ["RN12", "Se a IA cair, a ocorrência é criada sem previsão",
                   "nr_prazo_previsto e fl_risco_atraso aceitam nulo"],
                  ["RN13", "Em listas públicas, o cidadão aparece só pelo primeiro nome",
                   "consulta 10 (SUBSTR/INSTR)"],
                  ["RN14", "Categoria e bairro com ocorrências não podem ser excluídos",
                   "FKs sem ON DELETE CASCADE"],
                  ["RN15", "Senha guardada só como hash BCrypt", "ds_senha VARCHAR2(100)"],
                  ["RN16", "Só gestores (servidores) acessam o painel da prefeitura",
                   "tabela tb_gestor separada de tb_cidadao"],
                  ["RN17", "Gestor é cadastrado por outro gestor; o primeiro vem do seed",
                   "FK cd_gestor_cadastro (autorrelacionamento)"],
                  ["RN18", "Até 3 fotos JPG/PNG de até 2 MB por ocorrência",
                   "CHECK de tipo e tamanho; contagem de 3 na API Java"],
                  ], [2.2, 8.3, 6.5], destaque_primeira_coluna=True),
          h2("1.7 Perguntas que o banco responde"),
          bullets([c[1] for c in consultas]),
          h2("1.8 ODS"),
          bullets([
              "<b>ODS 11 – Cidades e comunidades sustentáveis:</b> meta 11.3 (gestão "
              "participativa: o cidadão registra e apoia) e meta 11.5 (reduzir impactos de "
              "desastres: bueiros e árvores com risco têm gravidade alta e entram primeiro na "
              "fila).",
              "<b>ODS 10 – Redução das desigualdades:</b> o banco permite comparar bairros "
              "(abertas, atrasadas e tempo médio, consultas 01, 03 e 09) e mostrar onde o "
              "atendimento demora mais.",
          ]),
          PageBreak()]

    # 2 ---------------------------------------------------------------------
    s += [h1("2. Modelo conceitual"),
          p("Visão de negócio do ZelaBairro, independente do banco: 8 entidades (Orgao, Categoria, "
            "Gestor, Bairro, Ocorrencia, Atualizacao, Cidadao e Foto), seus atributos (P = "
            "identificador primário, * = obrigatório, o = opcional) e os relacionamentos nomeados com as "
            "cardinalidades, em notação Barker. Aqui o N:N <b>apoia</b> entre Cidadao e Ocorrencia "
            "aparece direto, sem entidade intermediária, e não há chaves estrangeiras: elas só "
            "surgem no modelo lógico e no relacional, onde o N:N vira a associativa tb_apoio. Não há "
            "atributo multivalorado nem grupo repetido: as fotos são a entidade Foto."),
          imagem("modelo_conceitual.png", "Figura 1 – Modelo conceitual (Oracle SQL Developer "
                                          "Data Modeler)"),
          tabela([["Relacionamento (nome)", "Card.", "Leitura", "No banco (lógico/relacional)"]] + RELACIONAMENTOS,
                 [4.6, 1.3, 6.0, 5.1]),
          Spacer(1, 4),
          p("Exigência da disciplina: mínimo de 6 tabelas, dois relacionamentos 1:N e um N:N "
            "com tabela associativa. O ZelaBairro tem 9 tabelas, 9 relacionamentos 1:N e o N:N "
            "cidadão ↔ ocorrência resolvido pela associativa <b>tb_apoio</b>."),
          PageBreak(),
          h1("3. Modelo lógico"),
          p("Entidades com seus atributos, identificadores e relacionamentos, gerado no Data "
            "Modeler a partir do modelo relacional (Engenharia para Modelo Lógico)."),
          imagem("modelo_logico.png", "Figura 2 – Modelo lógico (Oracle SQL Developer Data "
                                      "Modeler)"),
          PageBreak(),
          h1("4. Modelo relacional"),
          p("Tabelas Oracle com colunas, tipos, chaves primárias e estrangeiras. Nomes sem espaço "
            "e sem acento, no padrão tb_ (tabela), sq_tb_ (sequence), cd_ (código/chave), nm_ "
            "(nome), ds_ (descrição), dt_ (data), nr_ (número), st_ (status), fl_ (flag S/N) e "
            "bl_ (BLOB)."),
          imagem("modelo_relacional.png", "Figura 3 – Modelo relacional (Oracle SQL Developer "
                                          "Data Modeler)"),
          h3("Esquema relacional em texto"),
          codigo(RELACIONAL),
          PageBreak()]

    # 5 ---------------------------------------------------------------------
    s += [h1("5. Dicionário de dados"),
          p("Todas as tabelas têm COMMENT ON TABLE no script. As sequences sq_tb_* geram as "
            "chaves primárias de todas as tabelas, menos tb_apoio, que tem chave composta. "
            "PK = chave primária, FK = chave estrangeira, UK = UNIQUE.")]
    for nome, descricao, colunas in DICIONARIO:
        linhas = [["Coluna", "Tipo", "Tam.", "Nulo", "Chave", "Restrição", "Significado"]]
        linhas += [list(c) for c in colunas]
        s += [CondPageBreak(4 * cm), h3(f"{nome} — {descricao}"),
              tabela(linhas, [3.3, 2.0, 1.2, 1.2, 1.5, 4.0, 3.8]), Spacer(1, 6)]
    s += [PageBreak()]

    # 6 ---------------------------------------------------------------------
    s += [h1("6. Script e carga de dados"),
          p("O arquivo <b>zelabairro.sql</b> está nesta ordem: (1) CREATE TABLE das 9 tabelas na "
            "ordem das chaves estrangeiras (tb_orgao, tb_bairro, tb_cidadao, tb_gestor, "
            "tb_categoria, tb_ocorrencia, tb_atualizacao, tb_apoio, tb_foto), com COMMENT ON "
            "TABLE e sequences; (2) 60 INSERTs; (3) as 10 consultas numeradas; (4) UPDATE com "
            "WHERE; (5) DELETE com WHERE."),
          tabela([["Tabela", "Registros", "O que foi carregado"],
                  ["tb_orgao", "5", "Os 5 órgãos responsáveis"],
                  ["tb_bairro", "6", "Distritos reais de São Paulo com a subprefeitura correta"],
                  ["tb_cidadao", "8", "Cidadãos fictícios; senha só como hash BCrypt"],
                  ["tb_gestor", "3", "Gestor inicial (sem quem cadastrou) e 2 cadastrados por ele"],
                  ["tb_categoria", "8", "As 8 categorias com prazo, gravidade e órgão"],
                  ["tb_ocorrencia", "12", "Ocorrências nos 4 status, com e sem previsão da IA"],
                  ["tb_atualizacao", "9", "Histórico só com transições permitidas (RN05)"],
                  ["tb_apoio", "6", "Apoios que respeitam a RN08"],
                  ["tb_foto", "3", "Imagens PNG mínimas (1×1 pixel) em BLOB"],
                  ["<b>Total</b>", "<b>60</b>", ""],
                  ], [3.6, 2.2, 11.2], destaque_primeira_coluna=True),
          Spacer(1, 8),
          imagem("captura_01_create.png", "Captura 1 – Criação das tabelas, comentários e "
                                          "sequences no Oracle", altura_max=11 * cm),
          imagem("captura_02_inserts.png", "Captura 2 – INSERTs executados e conferência de "
                                           "registros por tabela", altura_max=11 * cm),
          PageBreak()]

    # 7 ---------------------------------------------------------------------
    s += [h1("7. As 10 consultas"),
          p("Cada consulta responde a uma pergunta do ZelaBairro. No conjunto, elas usam WHERE, "
            "ORDER BY, cálculo no SELECT, COUNT, SUM, AVG, MAX e MIN com GROUP BY, HAVING, "
            "subconsulta, INNER JOIN, LEFT JOIN e RIGHT JOIN."),
          tabela([["Nº", "Pergunta", "Recursos SQL"]] +
                 [[n, perg, rec] for n, perg, rec, _ in consultas], [1, 9, 7]),
          PageBreak()]
    for numero, pergunta, recursos, sql in consultas:
        s += [CondPageBreak(9 * cm), h2(f"Consulta {numero}"),
              p(f"<b>Pergunta:</b> {pergunta}"), p(f"<b>Recursos:</b> {recursos}"),
              codigo(sql), Spacer(1, 6),
              imagem(f"captura_consulta_{numero}.png",
                     f"Captura – resultado da consulta {numero} no Oracle", altura_max=9 * cm)]
    s += [PageBreak()]

    # 8 ---------------------------------------------------------------------
    s += [h1("8. Atualização e exclusão (com WHERE)"),
          h2("8.1 UPDATE"),
          p("A ocorrência 9 (bueiro entupido, EM_ANDAMENTO) foi resolvida: o status passa para "
            "RESOLVIDA e a data de resolução é preenchida (RN06). O WHERE também confere o status "
            "atual, porque só EM_ANDAMENTO → RESOLVIDA é permitido (RN05). Na aplicação, a API "
            "Java faz essa mudança junto com o registro em tb_atualizacao."),
          codigo(update), Spacer(1, 6),
          imagem("captura_03_update.png", "Captura – UPDATE executado e conferência",
                 altura_max=9 * cm),
          h2("8.2 DELETE"),
          p("A cidadã 7 retirou o apoio que tinha dado à ocorrência 3. Retirar apoio é uma "
            "funcionalidade do MVP; a chave composta garante que só aquela linha é removida."),
          codigo(delete), Spacer(1, 6),
          imagem("captura_04_delete.png", "Captura – DELETE executado e conferência",
                 altura_max=9 * cm)]
    return s


if __name__ == "__main__":
    doc = Documento(SAIDA)
    doc.multiBuild(capa() + conteudo())
    print(f"PDF gerado: {SAIDA}")
    pendentes = sorted(set(PENDENTES))
    if pendentes:
        print(f"Atenção: {len(pendentes)} imagem(ns) ainda faltando em imagens/:")
        for nome in pendentes:
            print(f"  - {nome}")
