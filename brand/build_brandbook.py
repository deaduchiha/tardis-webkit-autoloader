#!/usr/bin/env python3
"""Render the approved TARDIS identity guide to a print-ready landscape PDF."""

from pathlib import Path
import sys

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "tardis-visual-identity-brandbook.pdf"
W, H = landscape(A4)
M = 42
INDIGO = colors.HexColor("#0A00B0")
MIDNIGHT = colors.HexColor("#080914")
PANEL = colors.HexColor("#14152F")
PAPER = colors.HexColor("#F5F5FF")
LAVENDER = colors.HexColor("#A6A2FF")
CYAN = colors.HexColor("#56C7FF")
MUTED = colors.HexColor("#66677F")
WHITE = colors.white

STYLES = {
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=15, textColor=MIDNIGHT),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.2, leading=11.5, textColor=MUTED),
    "inverse": ParagraphStyle("inverse", fontName="Helvetica", fontSize=11, leading=16, textColor=PAPER),
    "inverse_small": ParagraphStyle("inverse_small", fontName="Helvetica", fontSize=8.5, leading=12, textColor=colors.HexColor("#C4C5DE")),
    "card": ParagraphStyle("card", fontName="Helvetica", fontSize=9, leading=13, textColor=MIDNIGHT),
}


def p(c, text, x, top, width, style="body"):
    para = Paragraph(text, STYLES[style])
    _, height = para.wrap(width, H)
    para.drawOn(c, x, top - height)
    return top - height


def img(c, path, x, y, width, height):
    path = ROOT / path
    with Image.open(path) as im:
        iw, ih = im.size
        scale = min(width / iw, height / ih)
        dw, dh = iw * scale, ih * scale
        c.drawImage(ImageReader(im.convert("RGBA")), x + (width - dw) / 2, y + (height - dh) / 2,
                    width=dw, height=dh, mask="auto", preserveAspectRatio=True)


def rect(c, x, y, w, h, fill, radius=0, stroke=None, sw=1):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(sw)
    if radius:
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)
    else:
        c.rect(x, y, w, h, fill=1, stroke=1 if stroke else 0)


def label(c, text, x, y, color=INDIGO, size=8):
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    t = c.beginText(x, y)
    t.setCharSpace(1.25)
    t.textLine(text.upper())
    c.drawText(t)
    c.restoreState()


def title(c, kicker, heading, page, dark=False):
    fg = PAPER if dark else MIDNIGHT
    muted = colors.HexColor("#999AB5") if dark else MUTED
    label(c, kicker, M, H - 38, LAVENDER if dark else INDIGO, 7.5)
    c.setFillColor(fg)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(M, H - 70, heading)
    c.setStrokeColor(colors.HexColor("#30314D") if dark else colors.HexColor("#DCDD EA".replace(" ", "")))
    c.setLineWidth(0.7)
    c.line(M, H - 84, W - M, H - 84)
    footer(c, page, dark, muted)


def footer(c, page, dark=False, muted=None):
    muted = muted or (colors.HexColor("#8586A5") if dark else colors.HexColor("#77788D"))
    c.setFillColor(muted)
    c.setFont("Helvetica", 7.5)
    c.drawString(M, 22, "TARDIS  /  VISUAL IDENTITY")
    c.drawRightString(W - M, 22, "OCT 2026  |  %02d" % page)


def page_bg(c, color=PAPER):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def card(c, x, y, w, h, fill=WHITE, stroke=colors.HexColor("#E5E5EF"), radius=10):
    rect(c, x, y, w, h, fill, radius, stroke, 0.7)


def draw_cover(c):
    page_bg(c, MIDNIGHT)
    # Quiet grid, with a single interrupted line recalling the central split in the mark.
    c.setStrokeColor(colors.HexColor("#191A35"))
    c.setLineWidth(0.5)
    for x in range(48, int(W), 48):
        c.line(x, 0, x, H)
    for y in range(36, int(H), 36):
        c.line(0, y, W, y)
    rect(c, 520, 0, 2, H, colors.HexColor("#232346"))
    img(c, "brand/renders/tardis-white-master.png", 58, 342, 92, 92)
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(58, 282, "TARDIS")
    label(c, "Visual identity guide", 60, 253, LAVENDER, 9)
    c.setFillColor(colors.HexColor("#D5D6EA"))
    c.setFont("Helvetica", 16)
    c.drawString(60, 200, "A clear way through complex systems.")
    p(c, "An evolutionary identity built from the paired-pillar mark and the indigo already recognized across Tardis products.", 60, 170, 360, "inverse")
    rect(c, 582, 86, 205, 423, INDIGO, 18)
    img(c, "brand/renders/tardis-white-master.png", 624, 170, 120, 250)
    c.setFillColor(colors.HexColor("#DCD9FF"))
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(684, 126, "TARDIS INDIGO  /  #0A00B0")
    footer(c, 1, True)
    c.showPage()


def page_story(c):
    page_bg(c)
    title(c, "01 / Strategy", "One mark. One clear promise.", 2)
    p(c, "Tardis creates calm, dependable interfaces for technical tools. Its paired pillars make a simple passage: two strong forms with a clear opening between them.", M, H-112, 345)
    p(c, "Keystone keeps the shape people already know, then redraws it with mirror-balanced geometry, a consistent 15-degree shoulder, and a central opening that stays visible at small sizes.", M, H-192, 345)
    card(c, M, 110, 345, 104, fill=MIDNIGHT, stroke=MIDNIGHT)
    label(c, "Brand idea", M+18, 190, LAVENDER)
    p(c, "A clear way through complex systems.", M+18, 171, 300, "inverse")
    p(c, "Keep the paired-pillar silhouette and saturated indigo as the two strongest recognition cues.", M+18, 145, 310, "inverse_small")
    # Three compact principles.
    x0, y0, gap = 424, 346, 16
    items = [
        ("CAPABLE", "Strong geometry; no unnecessary effects."),
        ("PRECISE", "Names, versions, and states stay explicit."),
        ("COMPOSED", "A dark, quiet interface keeps focus on the task."),
    ]
    for i, (head, body) in enumerate(items):
        x = x0 + i * 122
        card(c, x, y0-106, 108, 106)
        label(c, head, x+12, y0-25, INDIGO, 7)
        p(c, body, x+12, y0-43, 85, "small")
    img(c, "brand/renders/tardis-horizontal-master.png", 420, 125, 356, 105)
    label(c, "Horizontal signature", 424, 108, MUTED, 7)
    c.showPage()


def page_logo(c):
    page_bg(c)
    title(c, "02 / Logo", "Use the master artwork as supplied.", 3)
    card(c, M, 328, 250, 112)
    img(c, "brand/renders/tardis-horizontal-master.png", M+14, 348, 222, 74)
    label(c, "Primary / horizontal", M+14, 338, MUTED, 7)
    card(c, 314, 328, 172, 112)
    img(c, "brand/renders/tardis-symbol-master.png", 360, 341, 78, 82)
    label(c, "Symbol", 328, 338, MUTED, 7)
    card(c, 500, 328, 295, 112)
    img(c, "brand/renders/tardis-stacked-master.png", 603, 348, 80, 85)
    label(c, "Stacked signature", 516, 338, MUTED, 7)

    # Clear-space diagram: one mark-side margin around the symbol.
    card(c, M, 111, 359, 194)
    label(c, "Clear space", M+16, 284, INDIGO)
    c.setStrokeColor(LAVENDER)
    c.setDash(3, 3)
    c.rect(M+76, 144, 132, 128, fill=0, stroke=1)
    c.setDash()
    img(c, "brand/renders/tardis-symbol-master.png", M+96, 153, 92, 110)
    c.setFillColor(INDIGO)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(M+142, 130, "24 UNITS MINIMUM")
    p(c, "Clear space scales from the symbol's 24-unit side margin. In a lockup, leave at least the T-height between symbol and wordmark.", 429, 286, 350, "small")
    p(c, "Minimums: symbol 16 px (use the small-size file below 24 px); wordmark 96 px wide; horizontal signature 140 px wide. For print, symbol 6 mm high and horizontal signature 28 mm wide.", 429, 220, 350, "body")
    p(c, "Approved backgrounds: indigo on white or a pale neutral; white on Indigo or Midnight; white over a quiet image area. Use the app-icon tile when a container is needed.", 429, 151, 350, "small")
    c.showPage()


def page_color(c):
    page_bg(c)
    title(c, "03 / Color", "Indigo leads. Neutrals make room.", 4)
    swatches = [
        ("TARDIS INDIGO", "#0A00B0", "10 / 0 / 176", "94 / 100 / 0 / 31", INDIGO, WHITE),
        ("MIDNIGHT", "#080914", "8 / 9 / 20", "60 / 55 / 0 / 92", MIDNIGHT, PAPER),
        ("PANEL", "#14152F", "20 / 21 / 47", "57 / 55 / 0 / 82", PANEL, PAPER),
        ("PAPER", "#F5F5FF", "245 / 245 / 255", "4 / 4 / 0 / 0", PAPER, MIDNIGHT),
        ("LAVENDER", "#A6A2FF", "166 / 162 / 255", "35 / 36 / 0 / 0", LAVENDER, MIDNIGHT),
        ("SIGNAL CYAN", "#56C7FF", "86 / 199 / 255", "66 / 22 / 0 / 0", CYAN, MIDNIGHT),
    ]
    cw, ch, gx, gy = 238, 140, 16, 20
    startx, starty = M, H-112
    for i, (name, hx, rgb, cmyk, fill, fg) in enumerate(swatches):
        col, row = i % 3, i // 3
        x, y = startx+col*(cw+gx), starty-row*(ch+gy)-ch
        card(c, x, y, cw, ch, fill=fill, stroke=fill, radius=10)
        c.setFillColor(fg)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(x+16, y+ch-24, name)
        c.setFont("Helvetica-Bold", 19)
        c.drawString(x+16, y+ch-54, hx)
        c.setFont("Helvetica", 8)
        c.drawString(x+16, y+24, "RGB  " + rgb)
        c.drawString(x+16, y+11, "CMYK  " + cmyk + "  approx.")
    p(c, "Logo use: primary indigo on light surfaces; reversed white on indigo or dark surfaces. Keep lavender as the readable dark-mode accent. Cyan is optional and secondary. Semantic UI colors are separate from the logo palette: success #88E6BC, caution #F3C977, error #FF858E.", M, 91, W-2*M, "small")
    c.showPage()


def page_type(c):
    page_bg(c)
    title(c, "04 / Typography", "Distinctive in the mark. Native in the product.", 5)
    card(c, M, 333, 350, 110)
    img(c, "brand/renders/tardis-wordmark-master.png", M+20, 353, 310, 70)
    label(c, "Custom TARDIS wordmark / vector master", M+16, 342, MUTED, 7)
    label(c, "Interface sans", 430, 421, INDIGO)
    c.setFillColor(MIDNIGHT)
    c.setFont("Helvetica-Bold", 21)
    c.drawString(430, 388, "Clear actions. Honest status.")
    p(c, "Use -apple-system, BlinkMacSystemFont, Segoe UI, Arial, sans-serif. Regular for body text; semibold for controls and labels; bold for headlines. No remote font is required.", 430, 369, 352, "small")
    card(c, M, 113, 353, 180, fill=MIDNIGHT, stroke=MIDNIGHT)
    label(c, "Diagnostic mono", M+18, 266, LAVENDER)
    c.setFillColor(PAPER)
    c.setFont("Courier", 15)
    c.drawString(M+18, 226, "[2/3] relapse.js")
    c.setFillColor(colors.HexColor("#88E6BC"))
    c.drawString(M+18, 197, "Kernel read/write ready")
    c.setFillColor(colors.HexColor("#F3C977"))
    c.drawString(M+18, 168, "!1000  wait before next payload")
    p(c, "Use SFMono-Regular, Consolas, or a system monospace for payload names, logs, addresses, and versions. Keep diagnostic text readable and never use the display wordmark font for technical data.", M+18, 154, 315, "inverse_small")
    p(c, "Type scale for product surfaces: 22-28 px page title; 14-18 px control labels; 14 px minimum for desktop explanatory copy when space allows; 13 px minimum on compact screens; 14 px or larger for console output on desktop. Favor short, sentence-case headings.", 430, 285, 352, "body")
    p(c, "The TARDIS wordmark is custom outlined artwork. Do not type it in a stock font. Interface font families are system stacks and do not require distribution or remote loading.", 430, 199, 352, "small")
    c.showPage()


def page_system(c):
    page_bg(c)
    title(c, "05 / Graphic system", "Repeat the geometry, not the logo.", 6)
    card(c, M, 300, 260, 140, fill=colors.HexColor("#F1F0FF"), stroke=colors.HexColor("#E7E6FA"))
    img(c, "brand/renders/tardis-pattern.png", M+10, 310, 240, 120)
    label(c, "Pillar repeat / 12% tint", M+14, 287, MUTED, 7)
    p(c, "Use the paired-pillar pattern on broad, quiet surfaces. Leave it off console text, dense charts, and exploit details.", 332, 422, 435, "body")
    # Spacing and corner samples.
    label(c, "Digital rhythm", 332, 350, INDIGO)
    x, y = 332, 324
    for i, size in enumerate([8, 16, 24, 32]):
        rect(c, x+i*58, y, size, size, INDIGO, 2)
        c.setFillColor(MUTED)
        c.setFont("Helvetica", 7.5)
        c.drawCentredString(x+i*58+size/2, y-12, str(size)+" px")
    card(c, 586, 282, 198, 52, fill=MIDNIGHT, stroke=MIDNIGHT, radius=12)
    label(c, "12 px card corner", 606, 302, LAVENDER, 7)
    p(c, "Prefer filled or simple outline icons with consistent weight and square or lightly rounded corners. Use indigo for the active state, not as a substitute for written labels.", 332, 248, 435, "small")
    # Motion rule.
    card(c, M, 117, W-2*M, 90, fill=MIDNIGHT, stroke=MIDNIGHT)
    label(c, "Motion and sound", M+18, 184, LAVENDER)
    p(c, "Keep the logo static on core product screens. A separate brand reveal may assemble the two pillars from the center and resolve within 600 ms. Never delay exploit startup or cover a status message; respect reduced-motion preferences. No sound cue is defined.", M+18, 165, W-2*M-36, "inverse_small")
    c.showPage()


def page_product(c):
    page_bg(c)
    title(c, "06 / Product application", "Tardis WebKit Autoloader", 7)
    p(c, "The brand frames the task; technical information stays in front. The installer and autoloader work offline, so keep every visual asset embedded or local and avoid remote fonts and images.", M, H-108, W-2*M, "body")
    # PS5 icon card.
    card(c, M, 156, 210, 226)
    label(c, "Homescreen icon", M+16, 358, INDIGO)
    img(c, "assets/icon0.png", M+38, 198, 134, 134)
    p(c, "White mark on solid Indigo; 10% safe padding.", M+16, 184, 178, "small")
    # Dark browser mockup.
    x, y, w, h = 286, 156, 508, 226
    card(c, x, y, w, h, fill=MIDNIGHT, stroke=colors.HexColor("#30314D"), radius=13)
    img(c, "brand/renders/tardis-white-master.png", x+22, y+h-72, 36, 42)
    c.setFillColor(PAPER)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x+68, y+h-44, "TARDIS")
    c.setFillColor(colors.HexColor("#A6A2FF"))
    c.setFont("Helvetica", 7.8)
    c.drawString(x+68, y+h-58, "WEBKIT AUTOLOADER")
    c.setFillColor(colors.HexColor("#B9B8D9"))
    c.setFont("Helvetica-Bold", 7.5)
    c.drawString(x+22, y+h-77, "SYSTEM OUTPUT")
    c.setFillColor(colors.HexColor("#767694"))
    c.drawRightString(x+w-22, y+h-77, "LIVE SESSION")
    rect(c, x+22, y+54, w-44, 85, colors.HexColor("#070816"), 8, colors.HexColor("#343551"), 0.7)
    c.setFillColor(colors.HexColor("#A8ABC7"))
    c.setFont("Courier", 8)
    c.drawString(x+34, y+117, "[1/3] elfldr-check.js")
    c.drawString(x+34, y+100, "[2/3] relapse.js")
    c.setFillColor(colors.HexColor("#88E6BC"))
    c.drawString(x+34, y+83, "Kernel read/write ready")
    rect(c, x+22, y+28, w-44, 14, colors.HexColor("#17182D"), 5)
    rect(c, x+22, y+28, (w-44)*.65, 14, colors.HexColor("#5148FF"), 5)
    c.setFillColor(PAPER)
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(x+w/2, y+32, "Kernel read/write ready")
    label(c, "Product descriptor is separate from the logo", x+22, y+12, colors.HexColor("#999AB5"), 6.5)
    p(c, "Keep focus states visible, keep status meanings explicit, and preserve the original payload order and console output.", 286, 136, 500, "small")
    c.showPage()


def page_assets(c):
    page_bg(c)
    title(c, "07 / Files and stewardship", "One source of truth. Easy handoff.", 8)
    cols = [
        ("VECTOR MASTERS", "brand/logo/tardis-symbol.svg<br/>brand/logo/tardis-symbol-small.svg<br/>brand/logo/tardis-wordmark.svg<br/>brand/logo/tardis-lockup-horizontal.svg<br/>brand/logo/tardis-lockup-stacked.svg"),
        ("READY-TO-USE EXPORTS", "brand/exports/ has indigo, black, and reversed SVGs, square and app-icon assets, PNG size sets, favicon.ico, Apple touch icon, webmanifest, and PWA icons."),
        ("PRODUCT FILES", "assets/icon.svg is the PS5 icon source.<br/>frontend/autoloader/ is the exploit experience.<br/>frontend/installer-page/ and frontend/pointer/ carry the install and launch states."),
    ]
    for i, (head, body) in enumerate(cols):
        x = M + i*256
        card(c, x, 290, 238, 152)
        label(c, head, x+14, 416, INDIGO, 7)
        p(c, body, x+14, 394, 210, "small")
    label(c, "Handoff checklist", M, 248, INDIGO)
    checks = [
        "Use SVG for scale-independent screens; use the supplied PNG and ICO for app, browser, and device slots.",
        "Use the small-size mark below 24 px. If the wordmark becomes too small, switch to symbol-only.",
        "For print, use a one-color vector and confirm color with the printer's profile; supplied CMYK values are estimates.",
        "Preserve offline operation. Do not add remote fonts, images, or requests to the cached PS5 experience.",
        "Keep the app label, setup page, pointer page, and running screen named Tardis WebKit Autoloader.",
    ]
    y = 222
    for txt in checks:
        c.setFillColor(INDIGO)
        c.circle(M+4, y+2, 2.5, fill=1, stroke=0)
        y = p(c, txt, M+16, y+8, W-2*M-22, "small") - 10
    card(c, M, 48, W-2*M, 48, fill=colors.HexColor("#EBE9FF"), stroke=colors.HexColor("#EBE9FF"))
    p(c, "Clear, repeatable guidance keeps the identity consistent. Trademark clearance was not part of this design work.", M+16, 79, W-2*M-32, "small")
    c.showPage()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
    c.setTitle("TARDIS Visual Identity Guide")
    c.setAuthor("Tardis")
    c.setSubject("Logo, color, typography, and PS5 WebKit Autoloader brand system")
    draw_cover(c)
    page_story(c)
    page_logo(c)
    page_color(c)
    page_type(c)
    page_system(c)
    page_product(c)
    page_assets(c)
    c.save()
    print(OUT)


if __name__ == "__main__":
    sys.exit(main())
