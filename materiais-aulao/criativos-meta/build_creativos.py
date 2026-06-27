# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

W = H = 1080
BLACK = (10, 10, 10)
GOLD = (201, 162, 78)
GOLD_LIGHT = (228, 201, 136)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

FONT_DIR = "/c/Windows/Fonts"

def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)

f_badge = font("calibrib.ttf", 26)
f_headline = font("georgiab.ttf", 64)
f_sub = font("georgiai.ttf", 34)
f_button = font("calibrib.ttf", 36)
f_logo = font("calibrib.ttf", 28)

def wrap_draw(draw, text, fnt, max_width, x_center, y, fill, line_spacing=1.15, align="center"):
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    line_h = fnt.size * line_spacing
    total_h = line_h * len(lines)
    cy = y
    for line in lines:
        w_line = draw.textlength(line, font=fnt)
        draw.text((x_center - w_line / 2, cy), line, font=fnt, fill=fill)
        cy += line_h
    return cy

def rounded_rect(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)

def base_canvas():
    img = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)
    # subtle gold glow corners
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.ellipse([-350, -350, 450, 450], fill=(201, 162, 78, 55))
    odraw.ellipse([W-550, H-550, W+350, H+350], fill=(201, 162, 78, 40))
    overlay = overlay.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    # logo mark
    draw.ellipse([60, 56, 84, 80], fill=GOLD)
    draw.text((96, 52), "RECRIA", font=f_logo, fill=GOLD)
    return img, draw

def badge(draw, text):
    w_text = draw.textlength(text, font=f_badge)
    pad_x, pad_y = 28, 14
    box_w = w_text + pad_x * 2
    box_h = f_badge.size + pad_y * 2
    x0 = (W - box_w) / 2
    y0 = 150
    rounded_rect(draw, [x0, y0, x0 + box_w, y0 + box_h], radius=box_h/2, fill=None)
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=box_h/2, outline=GOLD, width=2)
    draw.text((W/2, y0 + box_h/2), text, font=f_badge, fill=GOLD_LIGHT, anchor="mm")

def cta_button(draw, text):
    box_w, box_h = 420, 90
    x0 = (W - box_w) / 2
    y0 = H - 170
    rounded_rect(draw, [x0, y0, x0 + box_w, y0 + box_h], radius=box_h/2, fill=GOLD)
    draw.text((W/2, y0 + box_h/2), text, font=f_button, fill=BLACK, anchor="mm")

def build(filename, badge_text, headline, sub, button_text):
    img, draw = base_canvas()
    badge(draw, badge_text)
    y = wrap_draw(draw, headline, f_headline, 920, W/2, 290, WHITE, line_spacing=1.12)
    wrap_draw(draw, sub, f_sub, 820, W/2, y + 30, GOLD_LIGHT, line_spacing=1.2)
    cta_button(draw, button_text)
    draw.text((W/2, H - 50), "agenciarecria.com.br", font=font("calibri.ttf", 22), fill=GRAY, anchor="mm")
    img.save(filename, quality=95)
    print("salvo:", filename)

build(
    "criativo-A-feed.png",
    "AULA GRATUITA · VAGAS LIMITADAS",
    "O que nenhuma agência te conta",
    "nem depois que você é cliente dela.",
    "QUERO ASSISTIR",
)

build(
    "criativo-C-feed.png",
    "AULA GRATUITA · VAGAS LIMITADAS",
    "Seu marketing não funciona. Seu comercial não converte.",
    "E não é sobre gastar mais em anúncio.",
    "QUERO DESCOBRIR",
)
