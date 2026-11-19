"""Gera ZelaBairro_Documentacao_Python_GS.pdf (Computational Thinking Using Python).

Uso (nesta pasta):  uv run --with reportlab python gerar_documentacao.py
Entradas: o projeto em ZelaBairro_Python/. As telas do capítulo 9 são capturadas rodando o
          main.py de verdade (numa cópia temporária, sem .env e sem internet), então o PDF
          nunca fica diferente do programa. A contagem de funções vem da árvore sintática.
Saída:    ZelaBairro_Python/ZelaBairro_Documentacao_Python_GS.pdf
"""
import ast
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether, ListFlowable,
                                ListItem, NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                Preformatted, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

PASTA = Path(__file__).resolve().parent
PROJETO = PASTA / "ZelaBairro_Python"
SAIDA = PROJETO / "ZelaBairro_Documentacao_Python_GS.pdf"
HOJE = date.today().strftime("%d/%m/%Y")

INTEGRANTES = [
    ("573982", "Leonardo Afonço Sousa"),
    ("569259", "Syang Cristina Gomes Souza"),
    ("573559", "Matheus Jones Sousa de Freitas"),
    ("569023", "Vitor Gonçalves de Souza"),
    ("572364", "Joao Machado Nascimento"),
]

FONTES = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FONTES + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FONTES + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic", FONTES + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FONTES + "DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic",
                              boldItalic="Sans-Bold")

ROSA = colors.HexColor("#ED145B")
ESCURO = colors.HexColor("#16161D")
ESCURO_2 = colors.HexColor("#3A0F2A")
TELA = colors.HexColor("#1E1E24")
TEXTO_TELA = colors.HexColor("#E8E8EC")
CINZA = colors.HexColor("#5B6470")
CINZA_CLARO = colors.HexColor("#F3F3F5")
LINHA = colors.HexColor("#D5D7DC")

ST = {
    "corpo": ParagraphStyle("corpo", fontName="Sans", fontSize=9.3, leading=13.6, spaceAfter=5,
                            alignment=4),
    "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=16, leading=21, spaceBefore=8,
                         spaceAfter=8, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=11, leading=15, spaceBefore=8,
                         spaceAfter=4, keepWithNext=1),
    "cel": ParagraphStyle("cel", fontName="Sans", fontSize=7.8, leading=10),
    "cel_b": ParagraphStyle("cel_b", fontName="Sans-Bold", fontSize=7.8, leading=10,
                            textColor=colors.white),
    "code": ParagraphStyle("code", fontName="Mono", fontSize=6.9, leading=8.6,
                           textColor=TEXTO_TELA),
    "toc1": ParagraphStyle("toc1", fontName="Sans", fontSize=10, leading=19),
    "legenda": ParagraphStyle("legenda", fontName="Sans-Italic", fontSize=7.8, leading=10.5,
                              textColor=CINZA, spaceAfter=8),
}
LARGURA = 17 * cm


# --------------------------------------------------------------------------- helpers
def p(texto, estilo="corpo"):
    return Paragraph(texto, ST[estilo])


def c(texto):
    """Trecho de código no meio do texto."""
    return f"<font name='Mono' color='#C2185B'>{escape(texto)}</font>"


def h1(texto):
    par = Paragraph(texto, ST["h1"])
    par._toc = texto
    return [CondPageBreak(6 * cm), par]


def h2(texto):
    return [Paragraph(texto, ST["h2"])]


def bullets(itens):
    return ListFlowable([ListItem(p(i), leftIndent=12) for i in itens], bulletType="bullet",
                        start="•", leftIndent=14, bulletFontName="Sans", bulletFontSize=9,
                        bulletColor=ROSA)


def tabela(linhas, larguras, negrito_primeira=False):
    dados = [[Paragraph(str(x), ST["cel_b"]) for x in linhas[0]]]
    dados += [[Paragraph(str(x), ST["cel"]) for x in linha] for linha in linhas[1:]]
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), ESCURO),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINHA),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CINZA_CLARO]),
    ]
    if negrito_primeira:
        estilo.append(("FONTNAME", (0, 1), (0, -1), "Sans-Bold"))
    t.setStyle(TableStyle(estilo))
    return [t, Spacer(1, 7)]


def tela(texto, legenda=None, max_linhas=16):
    """
    Bloco escuro de terminal/código. É montado em faixas de poucas linhas, coladas umas nas
    outras, para que telas longas possam continuar na página seguinte sem deixar buracos.
    """
    linhas = texto.strip("\n").split("\n")
    partes = []
    total = len(linhas)
    if total <= 26:  # tela curta: fica inteira numa página só
        max_linhas = total
    for inicio in range(0, total, max_linhas):
        trecho = "\n".join(linhas[inicio:inicio + max_linhas])
        t = Table([[Preformatted(trecho, ST["code"])]], colWidths=[LARGURA])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), TELA),
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 7 if inicio == 0 else 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7 if inicio + max_linhas >= total else 0),
        ]))
        partes.append(t)
    if legenda:
        partes[-1] = KeepTogether([partes[-1], Paragraph(legenda, ST["legenda"])])
    else:
        partes.append(Spacer(1, 8))
    return partes


def bloco(titulo, conteudo):
    """Subtítulo sempre junto do começo do conteúdo (nunca sozinho no pé da página)."""
    return [KeepTogether([Paragraph(titulo, ST["h2"]), conteudo[0]])] + conteudo[1:]


# --------------------------------------------------------------------------- dados do código
def conta_funcoes() -> int:
    total = 0
    for arquivo in PROJETO.glob("*.py"):
        arvore = ast.parse(arquivo.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if isinstance(no, ast.FunctionDef):
                total += 1
    return total


def executa(entradas: str) -> list:
    """Roda o main.py numa cópia temporária (dados originais, sem .env) e devolve a saída."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "app"
        shutil.copytree(PROJETO, copia, ignore=shutil.ignore_patterns(
            ".env", "__pycache__", "*.pdf", "relatorios", "exports"))
        # mostra na tela o que foi "digitado", como num terminal de verdade
        ecoa = ("import builtins, runpy\n"
                "original = builtins.input\n"
                "def digita(texto=''):\n"
                "    valor = original(texto)\n"
                "    print(valor)\n"
                "    return valor\n"
                "builtins.input = digita\n"
                "runpy.run_path('main.py', run_name='__main__')\n")
        saida = subprocess.run([sys.executable, "-c", ecoa], cwd=copia, input=entradas,
                               capture_output=True, text=True, timeout=60,
                               env={"PATH": "/usr/bin:/bin", "PYTHONIOENCODING": "utf-8"})
    return saida.stdout.split("\n")


def recorta(linhas: list, inicio: str, fim: str, ocorrencia: int = 1, antes: int = 0) -> str:
    """Recorta da n-ésima linha que contém `inicio` até a primeira seguinte que contém `fim`."""
    achados = []
    for i in range(len(linhas)):
        if inicio in linhas[i]:
            achados.append(i)
    comeco = achados[ocorrencia - 1] - antes
    final = comeco + antes
    while fim not in linhas[final]:
        final += 1
    trecho = []
    for linha in linhas[comeco:final + 1]:
        if "Pressione ENTER" not in linha:
            trecho.append(linha.rstrip())
    texto = "\n".join(trecho)
    while "\n\n\n" in texto:
        texto = texto.replace("\n\n\n", "\n\n")
    return texto.strip("\n")


def captura_telas() -> dict:
    """Executa os roteiros do capítulo 9 e devolve cada tela já recortada."""
    telas = {}
    saida = executa("4\n4\n0\n\n0\n")
    telas["menu"] = recorta(saida, "+-----", "Escolha uma opção")
    telas["fila"] = recorta(saida, "FILA DE PRIORIDADE", "(0 = voltar): 0", antes=1)

    saida = executa("1\nCarla Mendes\ncarla@email.com\n2\n4\n0\n\nAv. Lins de Vasconcelos, 900\n"
                    "Poste apagado ha uma semana na rua inteira\n\n0\n")
    telas["registro"] = recorta(saida, "Escolha o bairro", "Prioridade inicial")

    saida = executa("1\nJoana Martins\njoana.martins@exemplo.com\n2\n4\n4\nN\n\n0\n")
    telas["rn08"] = recorta(saida, "ID para apoiar", "Quer registrar")

    saida = executa("3\n2\n2\n\n\n0\n")
    telas["rn05"] = recorta(saida, "ATUALIZAR STATUS", "EM_ANDAMENTO -> RESOLVIDA ou", antes=1)

    saida = executa("5\n\n0\n")
    telas["relatorio"] = recorta(saida, "RELATÓRIO POR BAIRRO", "Relatório salvo", antes=1)

    saida = executa("7\n3\n4\n\n0\n0\n")
    telas["detalhe"] = recorta(saida, "OCORRÊNCIA #4", "->", antes=1)
    return telas


# --------------------------------------------------------------------------- documento
class Documento(BaseDocTemplate):
    def __init__(self, arquivo):
        super().__init__(str(arquivo), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                         topMargin=2.2 * cm, bottomMargin=2 * cm,
                         title="ZelaBairro Terminal - Documentação Python",
                         author="Equipe ZelaBairro - 1TDSPV",
                         subject="Global Solution 2026/2 - CitizenTech")
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate("capa", [frame], onPage=self._capa),
                               PageTemplate("normal", [frame], onPage=self._pagina)])

    def afterFlowable(self, flowable):
        if hasattr(flowable, "_toc"):
            self.notify("TOCEntry", (0, flowable._toc, self.page))

    def _capa(self, canv, doc):
        largura, altura = A4
        canv.saveState()
        faixas = 60
        for i in range(faixas):  # fundo escuro em degradê para o vinho
            t = i / (faixas - 1)
            cor = colors.Color(ESCURO.red + (ESCURO_2.red - ESCURO.red) * t,
                               ESCURO.green + (ESCURO_2.green - ESCURO.green) * t,
                               ESCURO.blue + (ESCURO_2.blue - ESCURO.blue) * t)
            canv.setFillColor(cor)
            canv.rect(0, altura - (i + 1) * altura / faixas, largura, altura / faixas + 1,
                      fill=1, stroke=0)
        canv.setStrokeColor(ROSA)
        canv.setLineWidth(1.2)
        canv.roundRect(2 * cm, altura - 3.6 * cm, 2.6 * cm, 1.3 * cm, 4, stroke=1, fill=0)
        canv.setFillColor(colors.white)
        canv.setFont("Sans-Bold", 13)
        canv.drawCentredString(3.3 * cm, altura - 3.12 * cm, "FIAP")
        canv.setFont("Sans-Bold", 7.5)
        canv.drawRightString(largura - 2 * cm, altura - 2.8 * cm, "COMPUTATIONAL THINKING")
        canv.drawRightString(largura - 2 * cm, altura - 3.15 * cm, "USING PYTHON")

        canv.setFillColor(ROSA)
        canv.setFont("Sans-Bold", 7.5)
        canv.drawString(2 * cm, altura - 8.6 * cm, "DOCUMENTAÇÃO TÉCNICA E GUIA DE EXECUÇÃO")
        canv.setFillColor(colors.white)
        canv.setFont("Sans-Bold", 30)
        canv.drawString(2 * cm, altura - 10 * cm, "ZelaBairro Terminal")
        canv.setStrokeColor(ROSA)
        canv.line(2 * cm, altura - 10.6 * cm, 4.5 * cm, altura - 10.6 * cm)
        canv.setFillColor(colors.HexColor("#C9C9D1"))
        canv.setFont("Sans", 9.5)
        canv.drawString(2 * cm, altura - 11.5 * cm,
                        "Ferramenta de triagem para o gestor da prefeitura: zeladoria urbana colaborativa")
        canv.drawString(2 * cm, altura - 12.05 * cm,
                        "com priorização inteligente, em Python, com JSON local e integração opcional ao Oracle.")

        campos = [("DESAFIO", "Global Solution 2026/2 · CitizenTech", "TURMA", "1TDSPV · Turmas de Fevereiro"),
                  ("DISCIPLINA", "Computational Thinking Using Python", "LINGUAGEM", "Python 3.10+"),
                  ("ENTREGA", "19/11/2026", "DOCUMENTO", "Documentação e Guia de Execução")]
        y = altura - 15 * cm
        for rot1, val1, rot2, val2 in campos:
            for x, rot, val in ((2 * cm, rot1, val1), (11 * cm, rot2, val2)):
                canv.setFillColor(colors.HexColor("#9A9AA6"))
                canv.setFont("Sans-Bold", 6.5)
                canv.drawString(x, y, rot)
                canv.setFillColor(colors.white)
                canv.setFont("Sans-Bold", 9)
                canv.drawString(x, y - 0.5 * cm, val)
            canv.setStrokeColor(colors.HexColor("#44444F"))
            canv.setLineWidth(0.4)
            canv.line(2 * cm, y + 0.45 * cm, largura - 2 * cm, y + 0.45 * cm)
            y -= 1.6 * cm

        caixa_y = 3.2 * cm
        canv.setFillColor(colors.Color(1, 1, 1, alpha=0.06))
        canv.roundRect(2 * cm, caixa_y, largura - 4 * cm, 5.2 * cm, 4, stroke=0, fill=1)
        canv.setFillColor(ROSA)
        canv.setFont("Sans-Bold", 6.8)
        canv.drawString(2.6 * cm, caixa_y + 4.55 * cm, "INTEGRANTES DO GRUPO")
        for i, (rm, nome) in enumerate(INTEGRANTES):
            x = 2.6 * cm if i % 2 == 0 else 11 * cm
            yy = caixa_y + 3.7 * cm - (i // 2) * 1.15 * cm
            canv.setFillColor(colors.white)
            canv.setFont("Sans-Bold", 8.8)
            canv.drawString(x, yy, nome)
            canv.setFillColor(colors.HexColor("#9A9AA6"))
            canv.setFont("Sans", 7.5)
            canv.drawString(x, yy - 0.42 * cm, f"RM {rm}")

        canv.setFillColor(colors.HexColor("#9A9AA6"))
        canv.setFont("Sans", 7)
        canv.drawString(2 * cm, 1.5 * cm,
                        "Documentação elaborada para a Global Solution 2026/2 — Computational Thinking Using Python")
        canv.drawRightString(largura - 2 * cm, 1.5 * cm, "1TDSPV · Turmas de Fevereiro")
        canv.restoreState()

    def _pagina(self, canv, doc):
        largura, altura = A4
        canv.saveState()
        canv.setFont("Sans-Bold", 6.8)
        canv.setFillColor(ROSA)
        canv.drawString(2 * cm, altura - 1.3 * cm, "DOCUMENTAÇÃO TÉCNICA · PYTHON")
        canv.setFillColor(CINZA)
        canv.drawRightString(largura - 2 * cm, altura - 1.3 * cm, "ZELABAIRRO TERMINAL")
        canv.setStrokeColor(LINHA)
        canv.setLineWidth(0.4)
        canv.line(2 * cm, altura - 1.5 * cm, largura - 2 * cm, altura - 1.5 * cm)
        canv.line(2 * cm, 1.5 * cm, largura - 2 * cm, 1.5 * cm)
        canv.setFont("Sans", 7.2)
        canv.drawCentredString(largura / 2, 1.05 * cm,
                               f"ZelaBairro Terminal • FIAP Global Solution 2026/2 • Página {doc.page} de {TOTAL_PAGINAS[0]}")
        canv.restoreState()


TOTAL_PAGINAS = ["?"]


def conteudo(telas: dict) -> list:
    qtd_funcoes = conta_funcoes()
    s = [NextPageTemplate("normal"), PageBreak()]
    toc = TableOfContents()
    toc.levelStyles = [ST["toc1"]]
    toc.dotsMinLevel = 0
    s += [Paragraph("Sumário", ST["h1"]), toc, PageBreak()]

    # 1 ------------------------------------------------------------------------------------
    s += h1("1 Objetivo e Justificativa do Projeto")
    s += [p("O <b>ZelaBairro Terminal</b> é a aplicação em Python da solução <b>ZelaBairro</b>, criada para o tema "
            "<b>CitizenTech</b> da Global Solution 2026/2 (tecnologia com o cidadão no centro da inovação). O "
            "ZelaBairro é uma plataforma de <b>zeladoria urbana colaborativa</b>: o cidadão registra e apoia problemas "
            "do seu bairro (buraco na rua, poste apagado, bueiro entupido, árvore com risco de queda) e a prefeitura "
            "recebe esses chamados já agrupados e ordenados por prioridade."),
          p("Dentro desse contexto, o terminal é a <b>ferramenta de triagem do gestor da prefeitura</b>. Com ele o "
            "gestor registra ocorrências, vê quais já foram reportadas por outros moradores, atualiza o andamento, "
            "consulta a fila ordenada por urgência, identifica o que está atrasado e compara os bairros.")]
    s += h2("Objetivos")
    s += [bullets([
        "Registrar e apoiar ocorrências de zeladoria, evitando duplicados (um problema reportado dez vezes vira "
        "uma ocorrência com dez apoios).",
        "Calcular a <b>prioridade</b> com uma fórmula pública e fácil de explicar (RN10), em vez de atender por "
        "ordem de chegada.",
        "Controlar o ciclo de vida da ocorrência (ABERTA, EM_ANDAMENTO, RESOLVIDA, CANCELADA) com transições "
        "válidas (RN05).",
        "Apontar ocorrências <b>atrasadas</b> (RN11) e mostrar o tempo médio por bairro, tornando visível a "
        "desigualdade entre regiões.",
        "Funcionar <b>sem internet</b> e, quando houver conexão, sincronizar com o Oracle, consultar o ViaCEP e "
        "usar a API de IA do grupo."])]
    s += h2("Justificativa")
    s += [p("Segundo o portal de dados abertos da Prefeitura de São Paulo, o canal SP156 recebe em média cerca de "
            "<b>157 mil solicitações por mês</b> (dados de 2022). Com esse volume, chamados duplicados e sem critério "
            "de urgência fazem um bueiro entupido antes da chuva esperar na mesma fila de um pedido de poda. O "
            "cidadão, sem retorno, desiste de reclamar; o problema pequeno vira grande (buraco vira acidente, bueiro "
            "vira alagamento) e a distância entre bairros cresce."),
          p("A GS pede soluções <i>simples, seguras, inclusivas e que continuem úteis fora do cenário ideal de "
            "conectividade</i>. Por isso o terminal guarda os dados em arquivo JSON local e só usa a rede quando o "
            "gestor escolhe. A solução se conecta aos <b>ODS 11</b> (cidades e comunidades sustentáveis, metas 11.3 e "
            "11.5) e <b>ODS 10</b> (redução das desigualdades), pois o relatório por bairro evidencia onde o "
            "atendimento demora mais.")]

    # 2 ------------------------------------------------------------------------------------
    s += h1("2 Contexto e Problema")
    s += [p("O cidadão afetado é o morador de cidade brasileira que convive com problemas de zeladoria, em especial "
            "nos bairros periféricos, onde a resolução costuma demorar mais, e as pessoas com mobilidade reduzida, "
            "para quem uma calçada quebrada ou uma rua escura são barreiras reais.")]
    s += tabela([["Quem", "Dor", "Como o terminal responde"],
                 ["Cidadão", "Não sabe se o pedido foi recebido, quanto vai demorar nem se alguém já reclamou do "
                  "mesmo problema.", "Sugere apoiar ocorrência já aberta (RN07); mostra histórico e prazo de "
                  "referência por categoria."],
                 ["Prefeitura", "Volume enorme de chamados misturados, com duplicados e sem critério de urgência.",
                  "Fila por prioridade (RN10) com o cálculo explicado passo a passo; destaque de atrasadas (RN11)."],
                 ["Cidade", "Problemas pequenos viram grandes; desigualdade entre bairros cresce.",
                  "Relatório por bairro com abertas, atrasadas e tempo médio de resolução."]],
                [2.6, 6.6, 7.8], negrito_primeira=True)
    s += [p("<b>Escopo do MVP:</b> registrar, apoiar e consultar ocorrências, atualizar status com histórico, prazo "
            "previsto e risco de atraso via IA (opcional), fila por prioridade, ocorrências atrasadas e relatório por "
            "bairro. <b>Fora do escopo:</b> login com senha, fotos, mapa, notificações, aplicativo nativo e chatbot. "
            "Como não há login, o e-mail identifica o cidadão (RN02) e as listagens mostram só o primeiro nome "
            "(RN13, LGPD).")]

    # 3 ------------------------------------------------------------------------------------
    s += h1("3 Funcionalidades Implementadas")
    s += [p("O menu principal tem 8 opções e dois submenus (Consultar e Integrações); a opção 3 também abre um "
            "submenu de novo status. Cada funcionalidade cita no código a regra de negócio (RN) do Documento Base "
            "que ela aplica.")]
    s += tabela([["Opção", "O que faz", "Regras", "Estruturas em destaque"],
                 ["1 Registrar", "Pede nome, e-mail, categoria, bairro, endereço (CEP opcional) e descrição; sugere "
                  "apoiar ocorrências iguais; consulta a IA.", "RN01 RN03 RN04 RN07 RN12",
                  "input, if/elif, f-strings, funções"],
                 ["2 Apoiar", "Registra o apoio de um cidadão (e-mail) a uma ocorrência em aberto.", "RN08",
                  "set, dicionário"],
                 ["3 Atualizar status", "Muda o status criando uma entrada no histórico; recusa transições "
                  "inválidas; preenche a data de resolução.", "RN05 RN06", "match-case, lista de dicionários"],
                 ["4 Fila de prioridade", "Calcula e ordena por pontos; mostra o cálculo de qualquer ocorrência.",
                  "RN10", "for, selection sort, tuplas"],
                 ["5 Relatório por bairro", "Abertas, atrasadas, resolvidas e tempo médio; salva .txt.", "RN11",
                  "dicionário de contagem, arquivo .txt"],
                 ["6 Atrasadas", "Lista ocorrências em aberto acima do prazo da categoria.", "RN11", "for, if"],
                 ["7 Consultar", "Submenu: listar, filtrar por status, ver detalhe e histórico.", "RN13",
                  "while, if/elif"],
                 ["8 Integrações", "Submenu: testar/importar/enviar ao Oracle (envio identificado pelo e-mail do "
                  "gestor), exportar JSON para o front, consultar CEP.", "RN02 RN05 RN06 RN12 RN16",
                  "match-case, oracledb, requests"],
                 ["0 Sair", "Salva o JSON e encerra.", "—", "while, json"]],
                [3.1, 7.2, 2.6, 4.1], negrito_primeira=True)

    # 4 ------------------------------------------------------------------------------------
    s += h1("4 Arquitetura e Estrutura do Código")
    s += [p(f"O sistema segue uma arquitetura procedural modular (sem classes), em 5 módulos, cada um com uma "
            f"responsabilidade. Nenhuma função usa variável global: a lista de ocorrências é criada em "
            f"{c('main()')} e passada como parâmetro. As credenciais do Oracle nunca ficam no código nem no "
            f"pacote entregue: cada pessoa cria o próprio {c('.env')} a partir do {c('.env.example')}.")]
    s += bloco("Integração entre os componentes", tela(r"""
      ViaCEP (API pública)          API de IA do grupo (Flask)
            ^                              ^
            | requests                     | requests (opcional, RN12)
            |                              |
      +-----+------------------------------+-----+        +---------------------------+
      |       ZELABAIRRO TERMINAL (Python)       | <----> | data/ocorrencias.json     |
      | main.py regras.py dados.py util.py       |        | (base local, sem rede)    |
      +--------------------+---------------------+        +---------------------------+
                           | oracledb (opcional, e-mail do gestor - RN16)
                           v
                Oracle FIAP (tb_ocorrencia, tb_apoio, tb_atualizacao ...)
                           ^
                           | JDBC
                  API Java (Render) <---- Front-end React (Vercel)""",
        "O terminal funciona sozinho com o JSON. Ao falar com o Oracle, usa as mesmas tabelas da API Java; "
        "o front-end lê esses dados pela API."))

    s += tabela([["Arquivo", "Responsabilidade", "Principais funções"],
                 ["main.py", "Menus, submenus e telas; laço principal com while e match-case.",
                  "main() menu_principal() registra_ocorrencia() fila_prioridade()"],
                 ["regras.py", "Regras de negócio RN03 a RN13, constantes em tuplas. Não lê teclado nem grava "
                  "arquivo.", "calcula_prioridade() transicao_permitida() apoia() ordena_por_prioridade()"],
                 ["dados.py", "Persistência: JSON (com conferência dos campos ao carregar), relatório .txt, "
                  "exportação para o front, conexão e sincronização com o Oracle.",
                  "carrega_dados() salva_dados() importa_do_oracle() envia_para_oracle()"],
                 ["api_externa.py", "Consumo de APIs externas (opcional): ViaCEP e API de IA.",
                  "busca_cep() prever_ia()"],
                 ["util.py", "Tela do terminal (caixa, tabela, mensagens), leitura validada e datas.",
                  "le_inteiro() le_texto() le_email() mostra_tabela()"]],
                [2.6, 7.4, 7.0], negrito_primeira=True)
    # 5 ------------------------------------------------------------------------------------
    s += h1("5 Lógica Computacional e Algoritmos")
    s += bloco("5.1 Prioridade da ocorrência (RN10)", [
        p("A pontuação é calculada na hora (nunca gravada) e só existe para ocorrências ABERTA ou EM_ANDAMENTO:"),
        *tela("""pontos = gravidade_da_categoria * 10
       + min(quantidade_de_apoios, 20) * 2
       + min(dias_em_aberto, 30)
       + 15   (se risco_atraso = 'S' OU a ocorrência estiver atrasada; soma uma vez só)
classe:  pontos >= 70 -> ALTA  |  40 a 69 -> MEDIA  |  abaixo de 40 -> BAIXA""")])
    s += tabela([["Caso", "Grav.", "Apoios", "Dias", "Risco/atraso", "Cálculo", "Pts", "Classe"],
                 ["Árvore com risco de queda", "5", "3", "2", "risco S", "50 + 6 + 2 + 15", "73", "ALTA"],
                 ["Buraco na via", "4", "0", "5", "N, no prazo", "40 + 0 + 5", "45", "MEDIA"],
                 ["Poda de árvore", "2", "0", "10", "N, no prazo", "20 + 0 + 10", "30", "BAIXA"],
                 ["Iluminação (atrasada)", "4", "25", "40", "atrasada", "40 + 40 + 30 + 15", "125", "ALTA"]],
                [4.1, 1.2, 1.4, 1.2, 2.4, 3.6, 1.2, 1.9], negrito_primeira=True)
    s += [p("<i>Casos de conferência do Documento Base, verificados com a função</i> "
            f"{c('calcula_prioridade()')}<i>. Atenção: como \"dias em aberto\" cresce a cada dia, a "
            "pontuação das ocorrências da massa inicial também cresce com o calendário. Por exemplo, a "
            "ocorrência 1 (árvore com risco) vale 73 pontos com 2 dias em aberto e passa a valer mais nos dias "
            "seguintes. Só a ocorrência 4 fica fixa em 125, porque já atingiu os limites de 20 apoios e 30 "
            "dias.</i>", "legenda")]
    s += bloco("5.2 Transições de status (RN05) com match-case", [
        p(f"A função {c('transicao_permitida(atual, novo)')} decide pelo status atual com {c('match-case')}. "
          "RESOLVIDA e CANCELADA são finais."),
        *tela('''def transicao_permitida(atual: str, novo: str) -> bool:
    match atual:
        case "ABERTA":
            return novo in ("EM_ANDAMENTO", "CANCELADA")
        case "EM_ANDAMENTO":
            return novo in ("RESOLVIDA", "CANCELADA")
        case _:
            return False''')])
    s += bloco("5.3 Ordenação da fila: selection sort", [
        p(f"A fila é uma lista de tuplas {c('(pontos, ocorrencia)')}. Em vez de funções prontas de ordenação, "
          f"usa-se o <b>selection sort</b> visto em aula: a cada volta do {c('for')} externo, o maior elemento do "
          "restante vai para a posição i. No empate, fica na frente a ocorrência mais antiga (menor id)."),
        *tela('''def ordena_por_prioridade(fila: list) -> None:
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
        fila[maior] = aux''')])
    s += bloco("5.4 Apoio sem repetição (RN08) com set", [
        p(f"Os apoiadores são e-mails. O {c('set')} garante que o mesmo e-mail não conte duas vezes: "
          f"converte-se a lista em conjunto, testa-se com {c('in')}, adiciona-se com {c('.add()')} e volta-se "
          "para lista antes de gravar no JSON (set não é aceito pelo formato JSON). Também são recusados o "
          "autor da ocorrência e ocorrências já encerradas. Se o apoio sugerido pela RN07 for recusado, o "
          "programa pergunta se o usuário quer mesmo registrar uma nova ocorrência, em vez de criar um "
          "duplicado sem avisar.")])
    s += bloco("5.5 Atraso (RN11) e relatório por bairro", [
        p("Dias em aberto = dias inteiros entre a abertura e hoje (ou a data de resolução). Uma ocorrência está "
          "atrasada quando os dias em aberto superam o prazo de referência da categoria. O relatório usa um "
          "<b>dicionário de contagem</b>: para cada ocorrência, a chave é o bairro e o valor é outro dicionário "
          "com abertas, atrasadas, resolvidas e soma de dias; o tempo médio é a soma dividida pela quantidade "
          "de resolvidas.")])
    s += bloco("5.6 Fluxo de registro de uma ocorrência", tela(r"""
[Nome e e-mail] -> [Categoria] -> [Bairro] -> existe ocorrência aberta igual? (RN07)
                                                   |                     |
                                                  SIM                   NAO
                                                   v                     |
                               escolhe um ID para apoiar ou 0 = nova     |
                                   |                    |                |
                              apoio aceito         apoio recusado (RN08) |
                                   v                    v                |
                            apoia e termina    "registrar nova mesmo assim?"
                                                   | SIM        | NAO -> volta ao menu
                                                   v            |
                                     [CEP (opcional) -> Endereço (RN03)] <--+
                                                   v
                                     [Descrição 10 a 500 caracteres (RN03)]
                                                   v
                                     [Consulta a IA] --falhou--> sem previsão (RN12)
                                                   v
                                     [Cria ocorrência ABERTA, abertura = hoje (RN04)]
                                                   v
                                     [Mostra prioridade e salva no JSON]"""))

    # 6 ------------------------------------------------------------------------------------
    s += h1("6 Estruturas de Dados Utilizadas")
    s += tabela([["Estrutura", "Onde é usada", "Por que foi escolhida"],
                 ["Tupla", "STATUS, CATEGORIAS (código, nome, órgão, prazo, gravidade), BAIRROS, campos padrão do "
                  "JSON; pares (pontos, ocorrencia) na fila; retorno de várias informações.",
                  "Dados fixos que não mudam durante a execução (tabela 6.4 do Documento Base); tuplas são "
                  "imutáveis e leves."],
                 ["Lista", "Lista de ocorrências; apoiadores; histórico; linhas de tabela e do relatório.",
                  "Coleção ordenada que cresce com append e é percorrida com for."],
                 ["Dicionário", "Cada ocorrência é um dicionário; contagem por bairro e por status.",
                  "Acesso por nome do campo (oc[\"status\"]) deixa o código legível e casa com o JSON."],
                 ["Set", "Verificação e união de apoiadores (RN08) e das tabelas existentes no Oracle.",
                  "Não aceita repetidos e testa pertencimento direto; a união de conjuntos junta apoios do JSON "
                  "e do Oracle."],
                 ["String", "Validação de tamanho (RN03), e-mail, formatação com f-strings, datas AAAA-MM-DD.",
                  "Datas em texto ISO são o mesmo formato da API Java e do front-end."]],
                [2.3, 7.2, 7.5], negrito_primeira=True)
    s += bloco("Formato de uma ocorrência em data/ocorrencias.json", tela('''{
    "id": 4,                       "id_oracle": null,
    "descricao": "Quarteirão inteiro às escuras há semanas...",
    "endereco": "Estrada de Itapecerica, 3200",
    "status": "EM_ANDAMENTO",      "data_abertura": "2026-10-08", "data_resolucao": null,
    "categoria": "Iluminação pública apagada",   "bairro": "Capão Redondo",
    "autor_nome": "Joana Martins", "autor_email": "joana.martins@exemplo.com",
    "apoiadores": ["morador01@exemplo.com", "..."],
    "prazo_previsto": 8,           "risco_atraso": "S",
    "historico": [ {"data": "2026-10-20", "de": "ABERTA", "para": "EM_ANDAMENTO",
                    "comentario": "Equipe de iluminação agendada", "enviado": false} ]
}''', 'Os nomes de categoria, bairro e status são idênticos aos do banco, da API de IA e do front-end '
      '("nomes são contrato").'))

    # 7 ------------------------------------------------------------------------------------
    s += h1("7 Persistência e Integrações")
    s += bloco("7.1 Arquivos locais", [
        p(f"<b>JSON</b> ({c('data/ocorrencias.json')}): carregado ao abrir e gravado após cada operação e ao "
          f"sair ({c('json.load')} / {c('json.dump')} com {c('with open')}). Se o arquivo não existir, o "
          "programa começa vazio; se estiver corrompido, guarda uma cópia .bak; se algum registro estiver "
          "sem campos obrigatórios (arquivo editado à mão), ele é ignorado com aviso, em vez de derrubar o "
          f"programa. <b>TXT</b> ({c('relatorios/relatorio_bairros.txt')}): relatório por bairro. <b>JSON para "
          f"o front</b> ({c('exports/ocorrencias_api.json')}): mesmas chaves do GET /ocorrencias/{{id}} da API "
          "Java.")])
    s += h2("7.2 Oracle FIAP (menu 8)")
    s += [p(f"A conexão usa {c('oracledb')} com DB_USER e DB_PASSWORD lidos do {c('.env')} de quem executa. "
            "O terminal trabalha com as mesmas tabelas do banco do grupo (Documento Base, seção 6). O cidadão é "
            "cadastrado pelo site; o terminal o localiza pelo e-mail (RN02).")]
    s += tabela([["Opção", "Operação", "O que acontece"],
                 ["8.1 Testar", "SELECT em user_tables", "Confirma a conexão e se as 7 tabelas existem."],
                 ["8.2 Importar", "SELECT com JOIN em tb_ocorrencia, tb_categoria, tb_bairro, tb_cidadao, "
                  "tb_apoio, tb_atualizacao", "Traz ocorrências novas (inclusive as registradas no site); nas já "
                  "existentes une os apoios e adota o status do Oracle se não houver mudança local pendente. Nada "
                  "é apagado."],
                 ["8.3 Enviar", "SELECT em tb_gestor; INSERT em tb_ocorrencia, tb_apoio e tb_atualizacao; "
                  "UPDATE do status", "Avisa que o banco é o mesmo do site e pede confirmação. Pede o <b>e-mail "
                  "do gestor</b>: se não estiver em tb_gestor, nada é enviado (RN16); se estiver, cada "
                  "atualização grava esse gestor (RN06). Só grava mudança de status que respeite a RN05 a partir "
                  "do status que está no Oracle. Um COMMIT por ocorrência (ROLLBACK se der erro)."]],
                [2.4, 5.4, 9.2], negrito_primeira=True)
    s += [p("O JSON local só é marcado como \"enviado\" depois do COMMIT, então uma falha no meio do envio nunca "
            "deixa o arquivo dizendo algo que o banco não tem. Todo comando usa parâmetros nomeados (:nome), nunca "
            "texto concatenado.")]
    s += bloco("7.3 API externa ViaCEP", [
        p("Ao registrar, o gestor pode informar o CEP; o programa faz um GET em "
          f"{c('https://viacep.com.br/ws/{cep}/json/')} com {c('requests')}, lê o JSON e preenche a rua do "
          "endereço de referência. Sem internet ou com CEP inexistente, mostra a mensagem e deixa digitar à mão. "
          "A consulta avulsa está no menu 8.5.")])
    s += bloco("7.4 API de IA do ZelaBairro (opcional)", [
        p(f"Se {c('IA_API_URL')} estiver no .env (por exemplo, a API publicada em "
          f"{c('https://zelabairro-ia.onrender.com')}), a ocorrência recebe prazo previsto e risco de atraso por "
          f"dois POST ({c('/prever/prazo')} e {c('/prever/atraso')}), com o corpo JSON "
          + c('{"categoria", "subprefeitura", "mes", "dia_semana"}') + ". Se a API não estiver configurada "
          "ou não responder, a ocorrência é criada mesmo assim, sem previsão (RN12): a IA nunca bloqueia o "
          "cidadão.")])

    # 8 ------------------------------------------------------------------------------------
    s += h1("8 Validação de Entradas e Usabilidade")
    s += tabela([["Campo", "Regra", "Tratamento"],
                 ["Opção de menu / IDs", "Número inteiro dentro da faixa",
                  "while + try/except ValueError: repete com mensagem clara."],
                 ["Nome", "3 a 100 caracteres", "Repete até atender, informando o tamanho digitado."],
                 ["E-mail (RN02)", "Formato nome@dominio.xx, até 120 caracteres",
                  "Função email_valido(); guardado em minúsculas."],
                 ["Descrição (RN03)", "Obrigatória, 10 a 500 caracteres", "Repete até atender."],
                 ["Endereço (RN03)", "Obrigatório, até 200 caracteres", "Repete até atender (ou compõe pelo CEP)."],
                 ["Comentário", "Opcional, até 300 caracteres", "Repete se passar do limite."],
                 ["Status (RN05)", "Só transições permitidas", "Recusa e mostra quais são permitidas."],
                 ["Apoio (RN08)", "Sem repetir, sem autor, só em aberto",
                  "Mensagem específica para cada caso; na sugestão da RN07, pergunta antes de criar outra."],
                 ["E-mail do gestor (RN16)", "Precisa existir em tb_gestor", "Sem gestor, nada é enviado ao Oracle."],
                 ["Rede e banco", "Oracle, ViaCEP e IA podem falhar",
                  "Capturam erros e voltam ao menu sem fechar o programa."]],
                [3.6, 5.4, 8.0], negrito_primeira=True)
    s += [p("<b>Usabilidade:</b> telas com largura fixa de 78 colunas (cabem no PyCharm e no VS Code sem quebrar), "
            "caixas e tabelas alinhadas, toda saída com f-strings, mensagens padronizadas ([OK], [ERRO], [AVISO]), "
            "pausa antes de voltar ao menu, listas numeradas para escolher categoria e bairro e confirmação (S/N) "
            "antes de enviar dados ao Oracle. Ctrl+C ou fim da entrada encerram com segurança, salvando os dados.")]

    # 9 ------------------------------------------------------------------------------------
    s += h1("9 Telas do Sistema e Resultados Esperados")
    s += [p(f"As telas abaixo foram capturadas da execução real do programa com a massa inicial, em {HOJE}. Como "
            "a prioridade depende dos dias em aberto, os pontos mudam conforme a data em que o programa é "
            "executado (ver 5.1).")]
    s += bloco("Menu principal", tela(telas["menu"]))
    s += bloco("Fila de prioridade (opção 4) e cálculo passo a passo", tela(telas["fila"]))
    s += bloco("Registro com sugestão de apoio (RN07)",
               tela("   (... lista das 8 categorias e dos 12 bairros ...)\n" + telas["registro"]))
    s += bloco("Apoio recusado na sugestão (RN08): o programa pergunta antes de criar outra",
               tela("   (o autor da ocorrência #4 tenta apoiar a própria ocorrência)\n" + telas["rn08"]))
    s += bloco("Recusa de transição inválida (RN05)", tela(telas["rn05"]))
    s += bloco("Relatório por bairro (opção 5)", tela(telas["relatorio"]))
    s += bloco("Detalhe e histórico (opção 7 > 3)", tela(telas["detalhe"]))

    # 10 -----------------------------------------------------------------------------------
    s += h1("10 Requisitos da Disciplina Atendidos")
    s += tabela([["Critério (pontos)", "Como foi atendido", "Onde ver"],
                 ["Menus (5)", "Menu principal com 8 opções + submenus Consultar, Integrações e de novo status.",
                  "menu_principal() menu_consultar() menu_integracoes()"],
                 ["Interação com usuário (4)", "Entradas com variáveis validadas; todas as saídas com f-strings.",
                  "util.le_*, telas em main.py"],
                 ["Estruturas de decisão (6)", "match-case no menu principal, no submenu de status, nas "
                  "integrações e na RN05; if/elif/else nas validações, classe de prioridade e submenus.",
                  "main() transicao_permitida() classe_prioridade()"],
                 ["Estruturas de repetição (6)", "while nos menus e na leitura validada; for nos cálculos, filas, "
                  "relatórios e ordenação.", "ordena_por_prioridade() conta_por_bairro()"],
                 ["Sequências (8)", "Lista, tupla, dicionário, set e string (capítulo 6).", "regras.py dados.py"],
                 ["Funções (6)", f"{qtd_funcoes} funções pequenas, todas com docstring, parâmetros, type hints e "
                  "retorno; sem variáveis globais.", "todos os módulos"],
                 ["Persistência (4)", "Arquivo JSON (base), TXT (relatório) e Banco Oracle (sincronização).",
                  "dados.py"],
                 ["Usabilidade (6)", "Mensagens claras, listas numeradas, tabelas alinhadas, confirmações, erros "
                  "que não fecham o programa.", "capítulos 8 e 9"],
                 ["Organização e comentários (5)", "5 módulos por responsabilidade; docstrings e comentários citando "
                  "a RN de cada regra; nomes em português e snake_case.", "todo o código"]],
                [3.7, 8.4, 4.9], negrito_primeira=True)
    s += [p("<b>Proibições da disciplina:</b> o código não usa classes (orientação a objetos) nem list "
            "comprehension. As exceções de rede e banco são tratadas com try/except e as funções devolvem tuplas "
            "(resultado, mensagem) em vez de criar tipos próprios. A conferência foi feita por varredura do "
            "código-fonte (análise da árvore sintática do Python) procurando definições de classe, comprehensions, "
            "expressões geradoras, lambda e global: nenhuma ocorrência.")]

    # 11 -----------------------------------------------------------------------------------
    s += h1("11 Guia de Execução")
    s += h2("11.1 Pré-requisitos")
    s += [bullets([
        f"Python 3.10 ou superior (o programa usa {c('match-case')}). Verifique com {c('python --version')}.",
        "Para o menu 8 (Oracle, ViaCEP e IA): bibliotecas oracledb e requests (arquivo requirements.txt), "
        "acesso à internet e, para o Oracle, um usuário do Oracle FIAP com as tabelas do grupo.",
        "Sem as bibliotecas e sem internet, todos os demais menus funcionam normalmente."])]
    s += h2("11.2 Passo a passo")
    s += tabela([["Passo", "Ação", "Comando / detalhe"],
                 ["1", "Descompacte o ZIP e abra a pasta no PyCharm ou no VS Code.",
                  "A pasta contém main.py, regras.py, dados.py, api_externa.py, util.py"],
                 ["2", "(Opcional) crie o ambiente virtual.", "python -m venv .venv e ative-o"],
                 ["3", "(Opcional) instale as dependências.", "pip install -r requirements.txt"],
                 ["4", "(Opcional, só para Oracle/IA) crie o .env.",
                  "Copie .env.example para .env e preencha DB_USER e DB_PASSWORD com o seu usuário do Oracle "
                  "FIAP. IA_API_URL é opcional."],
                 ["5", "Execute o programa.", "python main.py"],
                 ["6", "Use o menu digitando o número da opção e ENTER.", "0 salva e sai"]],
                [1.4, 7.2, 8.4])
    s += bloco("11.3 Configuração do .env (modelo .env.example)", tela("""DB_USER=rmXXXXXX                   # usuário do Oracle FIAP
DB_PASSWORD=sua_senha              # senha do Oracle FIAP
DB_HOST=oracle.fiap.com.br         # opcional (padrão)
DB_PORT=1521                       # opcional (padrão)
DB_SID=orcl                        # opcional (padrão)
IA_API_URL=                        # opcional: https://zelabairro-ia.onrender.com (vazio = RN12)""",
        "O .env com senha não é entregue no ZIP nem enviado ao GitHub (está no .gitignore)."))
    s += h2("11.4 Roteiro sugerido de demonstração")
    s += [bullets([
        "<b>4 Fila de prioridade:</b> mostra a ordenação e, ao pedir o cálculo do ID 4, a fórmula da RN10 "
        "(125 pontos, com os limites de 20 apoios e 30 dias; este valor não muda com a data).",
        "<b>1 Registrar:</b> escolha Iluminação pública apagada + Capão Redondo para ver a sugestão de apoio "
        "(RN07); com o e-mail joana.martins@exemplo.com (autora da #4), veja a recusa da RN08 e a pergunta antes "
        "de criar outra.",
        "<b>2 Apoiar:</b> tente apoiar duas vezes com o mesmo e-mail e com o e-mail do autor para ver a RN08.",
        "<b>3 Atualizar status:</b> tente ABERTA para RESOLVIDA (recusado, RN05) e depois ABERTA para "
        "EM_ANDAMENTO e para RESOLVIDA.",
        "<b>5 e 6:</b> relatório por bairro (gera o .txt) e atrasadas (RN11).",
        "<b>8 Integrações:</b> exportar o JSON para o front e consultar um CEP (ex.: 01310-100); com o .env "
        "configurado, testar o Oracle."])]
    s += h2("11.5 Problemas comuns")
    s += tabela([["Mensagem", "Causa e solução"],
                 ["Biblioteca oracledb não instalada", "Rode pip install -r requirements.txt (só é necessária para o "
                  "Oracle)."],
                 ["Defina DB_USER e DB_PASSWORD no arquivo .env", "Copie .env.example para .env e preencha com o seu "
                  "usuário do Oracle FIAP."],
                 ["Não foi possível conectar ao Oracle", "Verifique internet/VPN da FIAP e as credenciais no .env."],
                 ["Faltando: tb_... (rode o script SQL do grupo)", "As tabelas do ZelaBairro ainda não foram criadas "
                  "nesse usuário do Oracle."],
                 ["RN16: ... não é um gestor cadastrado", "Informe o e-mail de um gestor que exista em tb_gestor "
                  "(o primeiro vem do seed do banco)."],
                 ["Autor ... não está cadastrado no Oracle", "O cidadão é cadastrado pelo site; use o mesmo e-mail "
                  "do cadastro."],
                 ["IA não configurada", "Normal sem IA_API_URL: a ocorrência é criada sem previsão (RN12)."],
                 ["Acentos estranhos no terminal", "Use o terminal do PyCharm/VS Code (UTF-8); o programa já "
                  "configura a saída em UTF-8."]],
                [6.2, 10.8])

    # 12 -----------------------------------------------------------------------------------
    s += h1("12 Considerações Finais")
    s += [p("<b>Resultado esperado.</b> Ao final de uma sessão o gestor tem a fila ordenada por urgência, sabe o que "
            "está atrasado e em quais bairros o atendimento demora mais, com tudo salvo em arquivo e, quando "
            "quiser, sincronizado com o banco que alimenta a API Java e o site."),
          p("<b>Limitações conhecidas do MVP.</b> Não há login (o e-mail identifica o cidadão); não há fotos nem "
            "mapa; o terminal não cadastra cidadãos no Oracle (isso é feito pelo site, com senha protegida); o "
            "Oracle exige que as tabelas do grupo já tenham sido criadas; o Oracle é compartilhado com o site, "
            "então o envio (8.3) deve ser usado só com dados reais."),
          p("<b>Próximos passos.</b> Autenticação do gestor, painel web integrado ao terminal e treinamento contínuo "
            "dos modelos de IA com os dados do próprio ZelaBairro.")]
    s += h2("Uso de IA generativa")
    s += [p("Ferramenta: Claude (Anthropic). Uso: apoio na estruturação e na escrita do código, nos testes e na "
            "redação desta documentação, a partir do Documento Base do projeto, dos exemplos de aula e do projeto "
            "anterior da equipe. O grupo revisou o material, executou o programa e responde pelo seu funcionamento "
            "na apresentação.")]
    s += h2("Fontes")
    s += [bullets([
        "FIAP. Global Solution 2026/2 – CitizenTech, requisitos da disciplina Computational Thinking Using Python.",
        "Equipe ZelaBairro. Documento Base do Projeto ZelaBairro (regras RN01 a RN18, modelo de dados e contratos).",
        "Prefeitura de São Paulo. Portal de Dados Abertos – Dados do SP156 (dados.prefeitura.sp.gov.br).",
        "ViaCEP – API pública de consulta de CEP (viacep.com.br).",
        "ONU. Objetivos de Desenvolvimento Sustentável 10 e 11 (sdgs.un.org)."])]
    return s


def gera():
    telas = captura_telas()
    # 1ª passada descobre o total de páginas; a 2ª imprime "Página X de N"
    for _ in range(2):
        doc = Documento(SAIDA)
        doc.multiBuild(conteudo(telas))
        TOTAL_PAGINAS[0] = doc.page
    print(f"PDF gerado: {SAIDA} ({TOTAL_PAGINAS[0]} páginas)")


if __name__ == "__main__":
    gera()
