"""Ajusta o PDF de entrega de Software Engineering and Business Model.

O PDF original foi gerado fora deste repositório (sem o script-fonte), então
este script aplica as correções por cima dele, sem mexer no resto do layout:

- capa: turma, RMs e nomes; versão do documento;
- página 4: turma, integrantes, links do Jira, do vídeo pitch e da aplicação e nota sobre o acesso;
- página 10: link do backlog no texto do capítulo 4;
- página 30 (11): link do vídeo pitch;
- página 31 (12.2): troca os campos "[Cada integrante cola...]" e "[INSERIR AQUI...]"
  pela referência ao Anexo A;
- sumário: entrada do Anexo A;
- rodapé: data;
- página nova no fim: Anexo A, prompts representativos de cada frente.

Uso:
    python ajustar_pdf_entrega.py ORIGINAL.pdf SAIDA.pdf

Requer: pymupdf e reportlab.
"""

import io
import sys

import fitz  # PyMuPDF
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Frame, Paragraph, Spacer, Table, TableStyle

FONTES = "/usr/share/fonts/truetype/crosextra/"
REG = FONTES + "Carlito-Regular.ttf"
BOLD = FONTES + "Carlito-Bold.ttf"
ITAL = FONTES + "Carlito-Italic.ttf"

TEXTO = (0x1F / 255, 0x29 / 255, 0x37 / 255)       # 0x1f2937
VERDE_ESCURO = (0x0B / 255, 0x4F / 255, 0x4A / 255)  # 0x0b4f4a
CINZA = (0x6B / 255, 0x72 / 255, 0x80 / 255)         # 0x6b7280

DATA = "19/11/2026"
VERSAO = "1.2"
TURMA = "1TDSPV"
JIRA_URL = "https://syangsouza05.atlassian.net/jira/software/projects/KAN/list"
PITCH_URL = "https://youtu.be/qMPR5RB8i10"
APP_URL = "https://zelabairro-frontend.vercel.app"
INTEGRANTES = [
    ("573982", "Leonardo Afonço Sousa (representante)"),
    ("569259", "Syang Cristina Gomes Souza"),
    ("573559", "Matheus Jones Sousa de Freitas"),
    ("569023", "Vitor Goncalves de Souza"),
    ("572364", "Joao Machado Nascimento"),
]


# ---------------------------------------------------------------- utilidades
def apagar(page, rect, fill=False):
    """Remove o texto dentro do retângulo, sem apagar fundos e linhas."""
    page.add_redact_annot(fitz.Rect(rect), fill=fill)


def aplicar(page):
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                          graphics=fitz.PDF_REDACT_LINE_ART_NONE)


def escrever(page, x, y_topo, texto, tamanho, fonte=REG, cor=TEXTO, direita=None):
    """Escreve uma linha; y_topo é o topo da caixa do texto (como no PDF original)."""
    nome = {REG: "carreg", BOLD: "carbold", ITAL: "carital"}[fonte]
    if direita is not None:
        largura = fitz.Font(fontfile=fonte).text_length(texto, fontsize=tamanho)
        x = direita - largura
    base = y_topo + tamanho * 0.80
    page.insert_text((x, base), texto, fontsize=tamanho, fontname=nome,
                     fontfile=fonte, color=cor)


def achar(page, trecho):
    for b in page.get_text("dict")["blocks"]:
        for linha in b.get("lines", []):
            for s in linha["spans"]:
                if trecho in s["text"]:
                    return fitz.Rect(s["bbox"])
    raise SystemExit(f"Trecho não encontrado na página {page.number + 1}: {trecho!r}")


def encolher(r):
    """Retângulo um pouco menor na vertical, para não pegar linhas vizinhas."""
    return fitz.Rect(r.x0 - 0.5, r.y0 + 1.5, r.x1 + 0.5, r.y1 - 1.5)


# ---------------------------------------------------------------- capa
def ajustar_capa(page):
    r = achar(page, "Turma: [PREENCHER")
    apagar(page, encolher(r))
    for i in range(1, 6):
        apagar(page, encolher(achar(page, f"[RM {i}]")))
        apagar(page, encolher(achar(page, f"[Nome completo do integrante {i}]")))
    r_versao = achar(page, "Versão do documento")
    apagar(page, encolher(r_versao))
    aplicar(page)

    escrever(page, 70, 404.0, f"Turma: {TURMA}", 10.5, BOLD, VERDE_ESCURO)
    y = 446.4
    for rm, nome in INTEGRANTES:
        escrever(page, 70, y, rm, 10)
        escrever(page, 140, y, nome, 10)
        y += 18
    escrever(page, 54, r_versao.y0,
             f"Entrega: 19/11/2026, até 23h55, no Portal do Aluno  ·  "
             f"Versão do documento: {VERSAO} ({DATA})", 9.5, REG, (1, 1, 1))


# ---------------------------------------------------------------- sumário
def ajustar_sumario(page):
    ref = achar(page, "13. Referências")
    y = ref.y0 + 17
    titulo = "Anexo A. Prompts representativos por frente"
    escrever(page, 42, y, titulo, 10, BOLD)
    fonte = fitz.Font(fontfile=BOLD)
    inicio = 42 + fonte.text_length(titulo + " ", fontsize=10)
    fim = 553.1 - fonte.text_length("  34", fontsize=10)
    pontos = ""
    while fonte.text_length(pontos + " .  ", fontsize=10) < fim - inicio:
        pontos += " .  "
    escrever(page, inicio, y, pontos.rstrip(), 10, BOLD)
    escrever(page, 0, y, "34", 10, BOLD, direita=553.1)


# ---------------------------------------------------------------- página 4
def ajustar_identificacao(page):
    alvos = ["[PREENCHER A TURMA]", "[PREENCHER: RM e nome",
             "Backlog (Jira ou Trello)", "[COLE AQUI O LINK PÚBLICO",
             "Acesso liberado a quem tem o", "Os campos em destaque",
             "durante toda a correção.", "[COLE AQUI O LINK DO VÍDEO PITCH",
             "OU DRIVE ABERTO]", "[OPCIONAL: LINK DA APLICAÇÃO"]
    caixas = {t: achar(page, t) for t in alvos}
    # a palavra "link" sozinha na segunda linha do status
    for b in page.get_text("dict")["blocks"]:
        for linha in b.get("lines", []):
            for s in linha["spans"]:
                if s["text"].strip() == "link":
                    caixas["link"] = fitz.Rect(s["bbox"])
    for r in caixas.values():
        apagar(page, encolher(r))
    aplicar(page)

    t = caixas
    escrever(page, 196, t["[PREENCHER A TURMA]"].y0, TURMA, 8.6)
    escrever(page, 196, t["[PREENCHER: RM e nome"].y0,
             "Leonardo Afonço Sousa (RM 573982) e mais 4 integrantes; lista completa na capa", 8.6)
    escrever(page, 46, t["Backlog (Jira ou Trello)"].y0, "Backlog (Jira), obrigatório", 8.6)

    y = t["[COLE AQUI O LINK PÚBLICO"].y0
    escrever(page, 196, y, "https://syangsouza05.atlassian.net/jira/", 8.6, cor=VERDE_ESCURO)
    escrever(page, 196, y + 10.8, "software/projects/KAN/list", 8.6, cor=VERDE_ESCURO)
    page.insert_link({"kind": fitz.LINK_URI, "uri": JIRA_URL,
                      "from": fitz.Rect(196, y, 430, y + 20)})
    escrever(page, 437.3, y, "Professor convidado", 8.6)
    escrever(page, 437.3, y + 10.8, "por e-mail no Jira", 8.6)

    y = t["[COLE AQUI O LINK DO VÍDEO PITCH"].y0
    escrever(page, 196, y, PITCH_URL, 8.6, cor=VERDE_ESCURO)
    page.insert_link({"kind": fitz.LINK_URI, "uri": PITCH_URL,
                      "from": fitz.Rect(196, y, 330, y + 10)})

    y = t["[OPCIONAL: LINK DA APLICAÇÃO"].y0
    escrever(page, 196, y, APP_URL, 8.6, cor=VERDE_ESCURO)
    page.insert_link({"kind": fitz.LINK_URI, "uri": APP_URL,
                      "from": fitz.Rect(196, y, 330, y + 10)})

    y = t["Os campos em destaque"].y0
    escrever(page, 42, y, "O quadro do Jira é privado do grupo: o professor recebe acesso por convite e o mantém durante "
             "toda a correção. Se o link não", 8.6, ITAL)
    escrever(page, 42, y + 11, "abrir, o capítulo 4 traz o backlog completo como evidência. "
             "Os links foram testados antes do envio.", 8.6, ITAL)


# ---------------------------------------------------------------- página 10
def ajustar_backlog(page):
    r = achar(page, "[COLE AQUI O LINK PÚBLICO DO BACKLOG")
    # o restante da linha (". Para o caso de o link não") é reescrito logo após o novo texto
    resto = fitz.Rect(r.x1, r.y0, 560, r.y1)
    apagar(page, encolher(r))
    apagar(page, encolher(resto))
    aplicar(page)
    texto = "quadro KAN no Jira (endereço na página 4)"
    escrever(page, r.x0, r.y0, texto, 10, BOLD, VERDE_ESCURO)
    largura = fitz.Font(fontfile=BOLD).text_length(texto, fontsize=10)
    escrever(page, r.x0 + largura, r.y0, ". Para o caso de o link não", 10)
    page.insert_link({"kind": fitz.LINK_URI, "uri": JIRA_URL,
                      "from": fitz.Rect(r.x0, r.y0, r.x0 + largura, r.y1)})


# ---------------------------------------------------------------- página 30
def ajustar_pitch(page):
    r = achar(page, "COLE AQUI O LINK DO VÍDEO PITCH")
    # o restante da linha (". O roteiro completo e os slides") é reescrito logo após o link
    resto = fitz.Rect(r.x1, r.y0, 560, r.y1)
    apagar(page, encolher(r))
    apagar(page, encolher(resto))
    aplicar(page)
    escrever(page, r.x0, r.y0, PITCH_URL, 10, BOLD, VERDE_ESCURO)
    largura = fitz.Font(fontfile=BOLD).text_length(PITCH_URL, fontsize=10)
    escrever(page, r.x0 + largura, r.y0, ". O roteiro completo e os slides", 10)
    page.insert_link({"kind": fitz.LINK_URI, "uri": PITCH_URL,
                      "from": fitz.Rect(r.x0, r.y0, r.x0 + largura, r.y1)})


# ---------------------------------------------------------------- página 31
def ajustar_registro_ia(page):
    r1 = achar(page, "[Cada integrante cola")
    r2 = achar(page, "[Trecho aproveitado]")
    r3 = achar(page, "[INSERIR AQUI")
    apagar(page, encolher(r1))
    apagar(page, encolher(r2))
    apagar(page, fitz.Rect(42, 643.4, 553.3, 657.0), fill=(1, 1, 1))
    aplicar(page)
    escrever(page, 131, r1.y0, "Prompts reais de cada frente, transcritos das", 8.6)
    escrever(page, 131, r1.y0 + 10.8, "conversas: ver Anexo A (página 34)", 8.6)
    escrever(page, 381, r2.y0, "Ver Anexo A, coluna \"Resposta aproveitada\"", 8.6)
    escrever(page, 42, r3.y0 + 0.5,
             "Os trechos legíveis dos prompts de IA, Banco, Python, Java, Front e da correção de "
             "erro de integração estão no Anexo A.", 8.6, ITAL)


# ---------------------------------------------------------------- rodapé
def ajustar_rodape(page):
    try:
        r = achar(page, "Documento de entrega · 17/11/2026")
    except SystemExit:
        return
    apagar(page, encolher(r))
    aplicar(page)
    escrever(page, 42, r.y0, f"Calçada Digital Tecnologia Cívica · Documento de entrega · {DATA}", 8.5, REG, CINZA)


# ---------------------------------------------------------------- Anexo A
ANEXO = [
    ("IA e Chatbot",
     "\"[...] quero que você analise esta entrega da matéria de IA e chatbot, de acordo com o pdf "
     "enviado pelos professores e também de acordo com o nosso documento base [...] anexei dois zips "
     "[...] analise os dois\"",
     "Diagnóstico dos notebooks contra o PDF; realinhamento ao conteúdo das aulas (árvore de decisão, "
     "regressão linear e logística, curva ROC); código da API Flask; rascunho das conclusões.",
     "Executou os notebooks, conferiu as métricas e reescreveu e revisou as conclusões."),
    ("Banco de Dados",
     "\"Você vai desenvolver a entrega da matéria Building Relational Database (Banco de Dados) [...] "
     "O mesmo banco Oracle atende a disciplina de Banco de Dados e a API Java, então o script precisa "
     "servir às duas. [...] Critérios oficiais da matéria (obrigatório seguir TODOS)\"",
     "Script Oracle (tabelas tb_, sequences sq_tb_, carga de teste e as 10 consultas) e a "
     "documentação em PDF. Uma segunda conversa fez uma revisão independente da entrega.",
     "Fez os modelos do Data Modeler e as capturas de tela; executou e revisou o script."),
    ("Python",
     "\"[...] adicionei um zip referente a disciplina de python na pasta de entregas, sua função será "
     "avaliar este projeto com base no pdf enviado pelo professor e então anotar possíveis percas de "
     "ponto [...]\"",
     "Lista de pontos de risco frente ao PDF e correções no menu do terminal e na documentação, "
     "seguindo os exemplos de aula.",
     "Conferiu que não há classes nem list comprehension e executou todas as opções do menu."),
    ("Java",
     "\"Você vai desenvolver a entrega da disciplina Domain Driven Design Using Java [...] A API Java "
     "é o centro do sistema: o front (React, Vercel) só conversa com ela, e só ela acessa o Oracle e "
     "chama a IA.\"",
     "Código Spring Boot com JDBC (camadas, DTOs, exceções e status HTTP), testes e documentação; "
     "publicação no Render.",
     "Revisou e executou o código e os testes."),
    ("Front-end",
     "\"Você vai desenvolver a entrega da disciplina Front-End Design Engineering [...] A matéria exige "
     "um repositório GitHub público com no mínimo 5 commits de cada integrante [...] Você gera um "
     "plano de commits passo a passo\"",
     "Componentes React/TypeScript com Fetch e tipos iguais aos JSON da API; plano de commits por "
     "integrante.",
     "Cada integrante fez os próprios commits no repositório público e revisou as telas."),
    ("Integração",
     "\"Ocorre este erro ao registrar uma ocorrencia, me retorne possiveis causas, primeiro quando "
     "adiciona a imagem ele aparece este erro [...] e a IA não esta respondendo\"",
     "Explicação das causas prováveis do erro entre front, API Java e API de IA.",
     "Analisou as causas sugeridas e testou de novo o registro de ocorrência após a correção."),
    ("Eng. Software e Documento Base",
     "Prompts já transcritos na seção 12.2.",
     "Documento Base, plano de desenvolvimento, critérios de aceite e estrutura deste documento.",
     "Preencheu os dados do grupo, montou o backlog no Jira e revisou cada seção."),
]


def gerar_anexo_pdf():
    pdfmetrics.registerFont(TTFont("Carlito", REG))
    pdfmetrics.registerFont(TTFont("Carlito-Bold", BOLD))
    pdfmetrics.registerFont(TTFont("Carlito-Italic", ITAL))
    verde = colors.HexColor("#0b4f4a")
    teal = colors.HexColor("#0f766e")
    texto = colors.HexColor("#1f2937")
    h1 = ParagraphStyle("h1", fontName="Carlito-Bold", fontSize=19, leading=23, textColor=verde)
    corpo = ParagraphStyle("c", fontName="Carlito", fontSize=10, leading=13.6, textColor=texto)
    cel = ParagraphStyle("cel", fontName="Carlito", fontSize=8.6, leading=10.8, textColor=texto)
    cab = ParagraphStyle("cab", parent=cel, fontName="Carlito-Bold", textColor=colors.white)
    nota = ParagraphStyle("n", parent=cel, fontName="Carlito-Italic")

    linhas = [[Paragraph(x, cab) for x in
               ("Frente", "Trecho do prompt (transcrito da conversa)", "Resposta aproveitada",
                "Validação feita pelo grupo")]]
    for frente, prompt, resposta, validacao in ANEXO:
        linhas.append([Paragraph(frente, cel), Paragraph(prompt, cel),
                       Paragraph(resposta, cel), Paragraph(validacao, cel)])
    tabela = Table(linhas, colWidths=[70, 185, 136, 120.3], repeatRows=1)
    estilo = [("BACKGROUND", (0, 0), (-1, 0), teal),
              ("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#d1d5db")),
              ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
              ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    for i in range(2, len(linhas), 2):
        estilo.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f3f4f6")))
    tabela.setStyle(TableStyle(estilo))

    historia = [
        Paragraph("Anexo A. Prompts representativos por frente", h1),
        Spacer(1, 6),
        Paragraph("Trechos copiados das conversas com o <b>Claude (Anthropic)</b>, a única ferramenta de IA "
                  "usada pelo grupo. Os prompts longos foram encurtados com [...], sem mudar o sentido. Em todas "
                  "as frentes a IA foi apoio: o grupo definiu as regras no Documento Base, leu, revisou, executou "
                  "e entendeu o que foi aproveitado, e qualquer integrante sabe explicar cada parte na apresentação.",
                  corpo),
        Spacer(1, 10),
        tabela,
        Spacer(1, 8),
        Paragraph("Os prompts aparecem como foram digitados, inclusive com erros de digitação. As conversas "
                  "completas podem ser mostradas ao professor na apresentação, se solicitado.", nota),
    ]
    buf = io.BytesIO()
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(buf, pagesize=A4)
    frame = Frame(42, 40, 511.3, A4[1] - 40 - 52, leftPadding=0, rightPadding=0,
                  topPadding=0, bottomPadding=0)
    sobra = frame.addFromList(historia, c)
    if historia or sobra:
        raise SystemExit("O Anexo A não coube em uma página; encurte os textos.")
    c.showPage()
    c.save()
    return fitz.open("pdf", buf.getvalue())


def adicionar_anexo(doc):
    ultima = doc.page_count - 1
    doc.fullcopy_page(ultima)  # copia cabeçalho e rodapé da última página
    nova = doc[-1]
    apagar(nova, fitz.Rect(0, 40, 595.3, 805), fill=(1, 1, 1))
    apagar(nova, encolher(achar(nova, "Página ")), fill=(1, 1, 1))
    aplicar(nova)
    # remove as anotações de link herdadas da página copiada
    for link in nova.get_links():
        nova.delete_link(link)
    escrever(nova, 0, 811.5, f"Página {doc.page_count}", 8.5, REG, CINZA, direita=553.3)
    anexo = gerar_anexo_pdf()
    nova.show_pdf_page(nova.rect, anexo, 0)


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    doc = fitz.open(sys.argv[1])
    ajustar_capa(doc[0])
    ajustar_sumario(doc[2])
    ajustar_identificacao(doc[3])
    ajustar_backlog(doc[9])
    ajustar_pitch(doc[29])
    ajustar_registro_ia(doc[30])
    for page in doc:
        ajustar_rodape(page)
    adicionar_anexo(doc)
    doc.subset_fonts()
    doc.set_metadata({**doc.metadata, "modDate": fitz.get_pdf_now()})
    doc.save(sys.argv[2], garbage=3, deflate=True)
    print("PDF salvo em", sys.argv[2], "com", doc.page_count, "páginas")


if __name__ == "__main__":
    main()
