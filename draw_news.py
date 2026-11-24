#!/usr/bin/env python3
"""Render the world news of Tuesday 24 November 2026 as one 1024x1024 PNG.

Draws a single-page newspaper front page with Pillow: a navy masthead
band, one lead story, a two-by-two grid of story cards, and an
"also today" strip. No network, no randomness, no timestamps in the
output, so re-running it produces the same bytes. The finished image
is written to entry.png beside this file; main.ts only copies it.

Stories were picked from the reporting of 24 November 2026: the
Nvidia chief-executive return, the COP31 collapse, the Indonesia
factory fire, the NATO AWACS deployment, the war's toll in the Kyiv
region and off Libya, and the chess title defence opening in Geneva.
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024
MARGIN = 30
GAP = 16
PAPER = (253, 252, 247)
INK = (24, 24, 22)
BODY = (58, 55, 48)
MUTED = (110, 106, 96)
NAVY = (18, 42, 78)
LINE = (24, 24, 22)
CARD_BG = (244, 241, 232)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, font, width):
    """Split text into lines that fit width, word by word."""
    out = []
    current = ""
    for word in text.split():
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def centre(draw, cx, y, text, font, fill=INK):
    draw.text((cx - draw.textlength(text, font=font) / 2, y), text,
              font=font, fill=fill)


def kicker(draw, x, y, label, colour):
    """Small filled label chip; returns its width."""
    face = load(SANS_BOLD, 16)
    w = draw.textlength(label, font=face) + 20
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=6, fill=colour)
    draw.text((x + 10, y + 5), label, font=face, fill=(255, 255, 255))
    return w


def motif_chart(draw, cx, cy, s):
    """Rising market bars with an arrow."""
    import math
    half = s // 2
    bars = [0.35, 0.55, 0.45, 0.8]
    bw = s // 6
    for i, frac in enumerate(bars):
        x0 = cx - half + i * (bw + 4)
        h = int(s * frac)
        draw.rectangle([x0, cy + half - h, x0 + bw, cy + half],
                       fill=(29, 92, 46))
    draw.line([(cx - half, cy + half - 8), (cx + half - 14, cy - half + 6)],
              fill=(29, 92, 46), width=5)
    draw.polygon([(cx + half - 18, cy - half + 2), (cx + half + 2, cy - half + 2),
                  (cx + half - 6, cy - half + 20)], fill=(29, 92, 46))


def motif_globe(draw, cx, cy, s):
    """A globe with a crack through it: talks broken."""
    r = s // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(213, 231, 239),
                 outline=(15, 95, 110), width=4)
    draw.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r],
                 outline=(15, 95, 110), width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=(15, 95, 110), width=2)
    draw.line([(cx - 6, cy - r), (cx + 8, cy - 8), (cx - 4, cy + 10),
               (cx + 10, cy + r)], fill=(178, 34, 34), width=4)


def motif_flame(draw, cx, cy, s):
    """Flame over a roofline."""
    r = s // 2
    draw.rectangle([cx - r, cy + r // 4, cx + r, cy + r // 2],
                   fill=(52, 48, 44))
    draw.polygon([(cx - r // 2, cy + r // 4), (cx - r // 5, cy - r // 2),
                  (cx, cy - r // 10), (cx + r // 5, cy - r // 2),
                  (cx + r // 2, cy + r // 4)], fill=(224, 84, 20))
    draw.polygon([(cx - r // 4, cy + r // 4), (cx, cy - r // 6),
                  (cx + r // 4, cy + r // 4)], fill=(245, 176, 40))


def motif_radar(draw, cx, cy, s):
    """Early-warning radar sweep."""
    r = s // 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(18, 42, 78),
                 width=4)
    draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                 outline=(18, 42, 78), width=2)
    draw.line([cx, cy, cx + r - 6, cy - r + 14], fill=(18, 42, 78), width=4)
    for bx, by in ((cx - 14, cy + 6), (cx + 12, cy + 16)):
        draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(178, 34, 34))


def motif_burst(draw, cx, cy, s):
    """Twelve-point blast star."""
    import math
    r = s // 2
    points = []
    for i in range(24):
        angle = math.pi * i / 12
        rad = r if i % 2 == 0 else r * 0.45
        points.append((cx + rad * math.cos(angle),
                       cy + rad * math.sin(angle)))
    draw.polygon(points, fill=(224, 110, 20))
    draw.ellipse([cx - r // 4, cy - r // 4, cx + r // 4, cy + r // 4],
                 fill=(245, 196, 66))


def motif_chess(draw, cx, cy, s):
    """A small board with a crown above it."""
    cell = (s - 12) // 3
    x0 = cx - 3 * cell // 2
    y0 = cy - 3 * cell // 2 + 12
    for row in range(3):
        for col in range(3):
            fill = INK if (row + col) % 2 == 0 else (240, 234, 220)
            draw.rectangle([x0 + col * cell, y0 + row * cell,
                            x0 + (col + 1) * cell, y0 + (row + 1) * cell],
                           fill=fill)
    draw.rectangle([x0, y0, x0 + 3 * cell, y0 + 3 * cell],
                   outline=INK, width=3)
    top = y0 - 22
    draw.polygon([(cx - 26, top + 16), (cx - 26, top), (cx - 13, top + 9),
                  (cx, top - 5), (cx + 13, top + 9), (cx + 26, top),
                  (cx + 26, top + 16)], fill=(201, 162, 39))


LEAD = {
    "kicker": "BUSINESS  ·  TECH",
    "colour": (29, 92, 46),
    "headline": "HUANG IS BACK AT NVIDIA",
    "deck": ("Nvidia brings Jensen Huang back as chief executive after "
             "Trump brokers his return; shares jump, adding almost "
             "$1 trillion in value."),
    "motif": motif_chart,
}

CARDS = [
    {
        "kicker": "CLIMATE",
        "colour": (15, 95, 110),
        "headline": "COP31 ENDS WITH NO DEAL",
        "deck": ("Climate talks in Turkey collapse without a deal. "
                 "Negotiations may resume next year as Pacific "
                 "nations voice despair."),
        "motif": motif_globe,
    },
    {
        "kicker": "ASIA",
        "colour": (179, 64, 31),
        "headline": "24 DEAD IN INDONESIA FACTORY FIRE",
        "deck": ("A fire at a candy factory kills at least 24 people. "
                 "Rescuers search for around 30 workers still "
                 "missing."),
        "motif": motif_flame,
    },
    {
        "kicker": "EUROPE",
        "colour": (18, 42, 78),
        "headline": "NATO SENDS SPY PLANES TO POLAND",
        "deck": ("NATO will deploy AWACS early-warning aircraft after "
                 "three Russian missiles landed in Poland on "
                 "Friday."),
        "motif": motif_radar,
    },
    {
        "kicker": "WAR",
        "colour": (138, 90, 0),
        "headline": "THE WAR SPILLS FURTHER",
        "deck": ("Fourteen are dead across the Kyiv region after "
                 "weekend strikes. Kyiv says its drones sank a "
                 "Russian warship off Libya."),
        "motif": motif_burst,
    },
    {
        "kicker": "SPORT",
        "colour": (91, 58, 140),
        "headline": "CHESS CROWN DEFENCE BEGINS",
        "deck": ("Gukesh opens his world title defence against "
                 "Sindarov in Geneva today."),
        "motif": motif_chess,
    },
]

ALSO = [
    "Trump pauses Army detonation of lead azide in Iowa",
    "Waymo pulls driverless taxis off US freeways",
    "FIFA picks hosts for the 2031, 2035 Women's Cups",
    "India and Nepal open a new rail link",
]


def draw_card(draw, x, y, w, h, story):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=CARD_BG, outline=story["colour"], width=2)
    kicker(draw, x + 14, y + 14, story["kicker"], story["colour"])
    story["motif"](draw, x + w - 46, y + 42, 52)
    head = load(SANS_BOLD, 25)
    yy = y + 56
    for line in fit(draw, story["headline"], head, w - 28)[:2]:
        draw.text((x + 14, yy), line, font=head, fill=INK)
        yy += 30
    body = load(SANS, 17)
    yy = y + 122
    for line in fit(draw, story["deck"], body, w - 28)[:3]:
        draw.text((x + 14, yy), line, font=body, fill=BODY)
        yy += 21


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)

    # Navy masthead band with the paper's name.
    draw.rectangle([MARGIN, 20, CANVAS - MARGIN, 116], fill=NAVY)
    centre(draw, CANVAS // 2, 34, "THE WORLD IN ONE PAGE",
           load(SERIF, 50), fill=(255, 255, 255))
    centre(draw, CANVAS // 2, 92, "ONE DAY  ·  ONE IMAGE  ·  ALL OF IT",
           load(SANS_BOLD, 16), fill=(205, 216, 232))

    # The date, large and unmissable: this is the whole point.
    centre(draw, CANVAS // 2, 128, "TUESDAY 24 NOVEMBER 2026",
           load(SANS_BOLD, 34), fill=NAVY)
    draw.line([MARGIN, 172, CANVAS - MARGIN, 172], fill=LINE, width=3)
    centre(draw, CANVAS // 2, 180, "The day's news at a glance",
           load(SANS, 18), fill=MUTED)

    # Lead story, full width.
    lx, ly, lw, lh = MARGIN, 210, CANVAS - 2 * MARGIN, 148
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=10,
                           fill=(232, 243, 231),
                           outline=LEAD["colour"], width=2)
    kicker(draw, lx + 18, ly + 14, LEAD["kicker"], LEAD["colour"])
    LEAD["motif"](draw, lx + lw - 92, ly + 78, 96)
    head = load(SANS_BOLD, 40)
    draw.text((lx + 18, ly + 50), LEAD["headline"], font=head, fill=INK)
    body = load(SANS, 20)
    yy = ly + 100
    for line in fit(draw, LEAD["deck"], body, lw - 220)[:2]:
        draw.text((lx + 18, yy), line, font=body, fill=BODY)
        yy += 25

    # Two-by-two grid of cards, plus the sport card spanning the row.
    cw = (CANVAS - 2 * MARGIN - GAP) // 2
    ch = 188
    gx, gy = MARGIN, 374
    draw_card(draw, gx, gy, cw, ch, CARDS[0])
    draw_card(draw, gx + cw + GAP, gy, cw, ch, CARDS[1])
    draw_card(draw, gx, gy + ch + GAP, cw, ch, CARDS[2])
    draw_card(draw, gx + cw + GAP, gy + ch + GAP, cw, ch, CARDS[3])

    # Sport card, full width, shorter: kicker and headline share the
    # top row, the deck sits underneath across the whole width.
    sx, sy, sw, sh = MARGIN, gy + 2 * ch + 2 * GAP, CANVAS - 2 * MARGIN, 84
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=10,
                           fill=CARD_BG,
                           outline=CARDS[4]["colour"], width=2)
    chip_w = kicker(draw, sx + 14, sy + 12, CARDS[4]["kicker"],
                    CARDS[4]["colour"])
    CARDS[4]["motif"](draw, sx + sw - 50, sy + 44, 54)
    head = load(SANS_BOLD, 25)
    draw.text((sx + 14 + chip_w + 12, sy + 15), CARDS[4]["headline"],
              font=head, fill=INK)
    body = load(SANS, 17)
    deck_lines = fit(draw, CARDS[4]["deck"], body, sw - 28)
    draw.text((sx + 14, sy + 52), deck_lines[0], font=body, fill=BODY)

    # Also-today strip: four short items in two columns.
    ax, ay = MARGIN, sy + sh + GAP
    ah = 88
    draw.rounded_rectangle([ax, ay, ax + CANVAS - 2 * MARGIN, ay + ah],
                           radius=10, fill=(238, 236, 228),
                           outline=MUTED, width=2)
    centre(draw, CANVAS // 2, ay + 8, "ALSO TODAY",
           load(SANS_BOLD, 16), fill=MUTED)
    item = load(SANS, 16)
    col_w = (CANVAS - 2 * MARGIN - GAP) // 2
    for i, text in enumerate(ALSO):
        col = i % 2
        row = i // 2
        x = ax + 16 + col * (col_w + GAP)
        y = ay + 32 + row * 30
        for line in fit(draw, "•  " + text, item, col_w - 16)[:1]:
            draw.text((x, y), line, font=item, fill=BODY)

    # Footer: one line, inside the border.
    fy = ay + ah + 10
    draw.line([MARGIN, fy, CANVAS - MARGIN, fy], fill=LINE, width=2)
    centre(draw, CANVAS // 2, fy + 9,
           "Drawn from the reporting of Tuesday 24 November 2026.",
           load(SANS_BOLD, 17))

    draw.rectangle([8, 8, CANVAS - 8, CANVAS - 8], outline=INK, width=4)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
