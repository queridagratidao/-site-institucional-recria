# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                 ListFlowable, ListItem, NextPageTemplate, PageBreak)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

GOLD = "#C9A24E"
GOLD_DARK = "#9C7A2E"
BLACK = "#0A0A0A"
GRAY = "#666666"
PAGE_W, PAGE_H = A4

INSTAGRAM = "https://instagram.com/agencia.recria"
SITE = "https://www.agenciarecria.com.br"
GRUPO_WPP = "LINK_GRUPO_WHATSAPP_AQUI"  # TROCAR quando o grupo for criado
URL_PACOTE_INICIAL = "https://www.agenciarecria.com.br/aula-mkt-para-negocios-pac-inicial/"
URL_SESSAO_ESTRATEGICA = "https://www.agenciarecria.com.br/aplicar-sessao-estrategica/"


class BotaoLink(Flowable):
    def __init__(self, text, url, width=7.5*cm, height=1.1*cm, fill=GOLD, text_color=BLACK):
        Flowable.__init__(self)
        self.text = text
        self.url = url
        self.width = width
        self.height = height
        self.fill = fill
        self.text_color = text_color

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(HexColor(self.fill))
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        c.setFillColor(HexColor(self.text_color))
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(self.width/2, self.height/2 - 3.5, self.text)
        c.linkURL(self.url, (0, 0, self.width, self.height), relative=1)
        c.restoreState()

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CapaKicker", fontSize=12, leading=16, textColor=HexColor(GOLD),
                           fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=0))
styles.add(ParagraphStyle(name="CapaTitulo", fontSize=30, leading=36, textColor=white,
                           fontName="Helvetica-Bold", alignment=TA_CENTER))
styles.add(ParagraphStyle(name="CapaSub", fontSize=13, leading=18, textColor=HexColor("#E4C988"),
                           fontName="Helvetica-Oblique", alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Secao", fontSize=15, leading=19, spaceBefore=14, spaceAfter=8,
                           textColor=HexColor(GOLD_DARK), fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Corpo", fontSize=10.5, leading=15, spaceAfter=6,
                           textColor=black, fontName="Helvetica"))
styles.add(ParagraphStyle(name="CorpoBold", fontSize=11, leading=16, spaceAfter=6,
                           textColor=black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="PageHeader", fontSize=10, leading=12, textColor=HexColor(GOLD_DARK),
                           fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Urgencia", fontSize=10, leading=14.5, spaceBefore=4, spaceAfter=12,
                           textColor=HexColor(GOLD_DARK), fontName="Helvetica-BoldOblique"))


def draw_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(HexColor(BLACK))
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # glow dourado sutil nos cantos
    canv.setFillColor(HexColor(GOLD))
    canv.setFillAlpha(0.10)
    canv.circle(0, PAGE_H, 7*cm, fill=1, stroke=0)
    canv.circle(PAGE_W, 0, 9*cm, fill=1, stroke=0)
    canv.setFillAlpha(1)

    # icone (lampada+cerebro)
    try:
        icon_w = 3.2*cm
        icon_h = 3.2*cm
        canv.drawImage("assets/logo_icon.png", (PAGE_W - icon_w)/2, PAGE_H - 6.2*cm,
                        width=icon_w, height=icon_h, mask='auto', preserveAspectRatio=True)
    except Exception:
        pass

    canv.setFont("Helvetica-Bold", 11)
    canv.setFillColor(HexColor(GOLD))
    canv.drawCentredString(PAGE_W/2, PAGE_H - 7.3*cm, "MATERIAL DE APOIO")

    canv.setFont("Helvetica-Bold", 22)
    canv.setFillColor(white)
    linhas_titulo = ["Por que seu marketing não funciona", "e seu comercial não converte", "como deveria?"]
    ty = PAGE_H - 9.1*cm
    for linha in linhas_titulo:
        canv.drawCentredString(PAGE_W/2, ty, linha)
        ty -= 0.85*cm

    canv.setFont("Helvetica-Oblique", 10.5)
    canv.setFillColor(HexColor("#E4C988"))
    sub_linhas = [
        "Vou abrir o jogo com você: 10 anos de experiência em",
        "marketing e comercial, para te mostrar o que ninguém",
        "te mostrou até hoje. Esse é o resumo dessa aula.",
    ]
    ty -= 0.3*cm
    for linha in sub_linhas:
        canv.drawCentredString(PAGE_W/2, ty, linha)
        ty -= 0.55*cm

    canv.setFont("Helvetica-Bold", 13)
    canv.setFillColor(HexColor(GOLD))
    canv.drawCentredString(PAGE_W/2, 3.0*cm, "RECRIA")
    canv.setFont("Helvetica", 9.5)
    canv.setFillColor(HexColor("#999999"))
    canv.drawCentredString(PAGE_W/2, 2.5*cm, "Recriando marketing, simplificando vendas.")
    canv.restoreState()


def draw_footer(canv, doc):
    canv.saveState()
    canv.setStrokeColor(HexColor(GOLD))
    canv.setLineWidth(0.6)
    y_line = 1.9*cm
    canv.line(2*cm, y_line, PAGE_W - 2*cm, y_line)

    canv.setFont("Helvetica-Bold", 8.5)
    canv.setFillColor(HexColor(GOLD_DARK))
    fy = 1.45*cm

    parts = [
        ("Instagram: @agencia.recria", INSTAGRAM),
        ("Site: agenciarecria.com.br", SITE),
        ("Grupo VIP no WhatsApp", GRUPO_WPP),
    ]
    gap = 0.5*cm
    widths = [canv.stringWidth(t, "Helvetica-Bold", 8.5) for t, _ in parts]
    total_w = sum(widths) + gap * (len(parts) - 1)
    x = (PAGE_W - total_w) / 2
    for (text, url), w in zip(parts, widths):
        canv.drawString(x, fy, text)
        canv.linkURL(url, (x, fy - 2, x + w, fy + 9), relative=0)
        x += w + gap

    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(HexColor("#999999"))
    canv.drawCentredString(PAGE_W/2, 1.0*cm, f"Página {doc.page - 1}")
    canv.restoreState()


doc = BaseDocTemplate("material-de-apoio-aulao.pdf", pagesize=A4,
                       leftMargin=2.2*cm, rightMargin=2.2*cm, topMargin=2*cm, bottomMargin=2.8*cm)

frame_cover = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
frame_content = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="content")

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[frame_cover], onPage=draw_cover),
    PageTemplate(id="Content", frames=[frame_content], onPage=draw_footer),
])

story = []
story.append(NextPageTemplate("Content"))
story.append(PageBreak())


def secao(titulo):
    story.append(Paragraph(titulo, styles["Secao"]))


def bullets(items):
    story.append(ListFlowable(
        [ListItem(Paragraph(t, styles["Corpo"]), leftIndent=12) for t in items],
        bulletType="bullet", start="circle"
    ))
    story.append(Spacer(1, 4))


# Página 2
story.append(Paragraph("O resumo do aulão", styles["PageHeader"]))
story.append(Spacer(1, 10))

secao("1. Rede social e funil")
story.append(Paragraph("Hoje, quem não tem rede social é como se o negócio não existisse, seja ele local, físico ou online.", styles["Corpo"]))
bullets([
    "Não sabe que tem o problema",
    "Sabe do problema, não conhece a solução",
    "Conhece a solução, não confia em você ainda",
    "Confia em você, está pronta para comprar",
])
story.append(Paragraph("O anúncio acelera o seu processo de venda. Ele não faz milagre: se a casa não estiver arrumada, o anúncio só leva mais gente para ver a desorganização.", styles["Corpo"]))

secao("2. Arrumando a casa")
bullets([
    "Negócio físico ou misto: site institucional + página de captação (formulário)",
    "Negócio 100% online: LP de vendas, direto pro checkout",
])

secao("3. Comercial treinado")
bullets([
    "Velocidade: lead entrou, atende o mais rápido possível",
    "Ressalva combinada: lead de fim de semana, atende na próxima abertura",
    "Persistência: mínimo 5 tentativas, por canais diferentes, antes de desqualificar",
    "Facilitar o pagamento: parcelado, Pix, boleto, cartão",
])

secao("4. Canal certo para o seu negócio")
bullets([
    "Google é intenção: a pessoa já está buscando a solução, lead mais caro e mais qualificado",
    "Instagram é atenção: a pessoa não estava buscando, jornada mais longa, lead mais barato",
])

story.append(PageBreak())

# Página 3
story.append(Paragraph("O resumo do aulão (continuação)", styles["PageHeader"]))
story.append(Spacer(1, 10))

secao("5. Marketing não vende, comercial vende")
story.append(Paragraph("O marketing leva o lead o mais próximo possível de estar interessado. Quem quebra a objeção e converte é o comercial.", styles["Corpo"]))

secao("6. Automação amarrando tudo")
bullets([
    "Lead: deixou um dado de contato",
    "MQL: tomou uma ação real, ainda não validado pelo comercial",
    "SQL: validado pelo comercial, com perfil, orçamento e momento de compra",
])

secao("7. O ticket muda o esforço")
story.append(Paragraph("Quanto mais caro o produto (infoproduto, físico ou serviço), maior o esforço de marketing e de comercial necessário para fechar a venda.", styles["Corpo"]))

story.append(Spacer(1, 16))
story.append(Paragraph(
    "Esse é o resumo. A aula completa tem os exemplos, analogias e os dois cases reais. "
    "Se você quer ajuda pra aplicar isso no seu negócio, fale com a Amanda na Sessão Estratégica ou conheça o Pacote Inicial da Recria.",
    styles["CorpoBold"]
))

story.append(Spacer(1, 18))
story.append(Paragraph(
    "⏳ Atenção: a partir do momento que você recebeu esse material, o seu acesso às páginas abaixo "
    "é por tempo limitado. Elas saem do ar em breve, então não deixa pra depois.",
    styles["Urgencia"]
))
story.append(Spacer(1, 6))
story.append(BotaoLink("Quero o Pacote Inicial", URL_PACOTE_INICIAL, width=7.6*cm, fill=GOLD, text_color=BLACK))
story.append(Spacer(1, 10))
story.append(BotaoLink("Aplicar para a Sessão Estratégica", URL_SESSAO_ESTRATEGICA, width=7.6*cm, fill=GOLD_DARK, text_color="#FFFFFF"))

doc.build(story)
print("Material de apoio salvo")
