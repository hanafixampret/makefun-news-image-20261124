#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page as a 1024x1024 PNG.

Python 3 + Pillow, standard library plus PIL, no network, fully
deterministic. Writes entry.png next to this file; main.ts copies it
to the output directory, byte for byte.

Layout: newspaper masthead with the date, one lead story (Nvidia /
Jensen Huang), then six panels: COP31, the Indonesia factory fire,
the ICJ Myanmar ruling, the World Chess Championship, the Kyiv
strikes, and an "also today" ticker. Every story happened, or was
first reported, on Tuesday 24 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 232)
INK = (22, 21, 19)
GREY = (96, 91, 80)
RULE = (60, 56, 48)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centred(d, cx, y, text, f, fill=INK):
    d.text((cx - d.textlength(text, font=f) / 2, y), text, font=f, fill=fill)


def tag_chip(d, x, y, text, color):
    f = font(SANS_B, 17)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 22, y + 30], radius=6, fill=color)
    d.text((x + 11, y + 5), text, font=f, fill=(255, 255, 255))


def panel(d, x, y, w, h, tint, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=tint,
                        outline=accent, width=2)


def chip_icon(d, cx, cy, s):
    """A green AI chip with gold pins."""
    half = s // 2
    for i in range(-1, 2):
        yy = cy + i * s // 4
        d.rectangle([cx - half - 12, yy - 5, cx - half, yy + 5], fill=(176, 141, 58))
        d.rectangle([cx + half, yy - 5, cx + half + 12, yy + 5], fill=(176, 141, 58))
    d.rounded_rectangle([cx - half, cy - half, cx + half, cy + half],
                        radius=12, fill=(20, 83, 45))
    d.rounded_rectangle([cx - half + 16, cy - half + 16, cx + half - 16, cy + half - 16],
                        radius=6, outline=(212, 175, 55), width=4)
    f = font(SANS_B, s // 3)
    txt = "AI"
    d.text((cx - d.textlength(txt, font=f) / 2, cy - s // 6), txt,
           font=f, fill=(255, 255, 255))


def globe_icon(d, cx, cy, s):
    """A globe: climate talks broken."""
    r = s // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 232, 240),
              outline=(15, 95, 110), width=4)
    d.ellipse([cx - r // 3, cy - r, cx + r // 3, cy + r], outline=(15, 95, 110), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(15, 95, 110), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 180, fill=(15, 95, 110), width=2)
    d.polygon([(cx - r // 2, cy - r // 3), (cx - r // 6, cy - r // 2),
               (cx + r // 6, cy - r // 4), (cx + r // 2, cy - r // 3),
               (cx + r // 3, cy), (cx, cy + r // 5), (cx - r // 3, cy)],
              fill=(46, 125, 50))


def flame_icon(d, cx, cy, s):
    """A flame over a factory roofline."""
    r = s // 2
    d.rectangle([cx - r, cy + r // 3, cx + r, cy + r // 2], fill=(52, 48, 44))
    d.rectangle([cx - r + 6, cy - r // 6, cx - r + 16, cy + r // 3], fill=(52, 48, 44))
    d.polygon([(cx - r // 2, cy + r // 4), (cx - r // 5, cy - r // 2),
               (cx, cy - r // 8), (cx + r // 5, cy - r // 2),
               (cx + r // 2, cy + r // 4)], fill=(230, 92, 20))
    d.polygon([(cx - r // 4, cy + r // 4), (cx - r // 10, cy - r // 6),
               (cx + r // 10, cy - r // 6), (cx + r // 4, cy + r // 4)],
              fill=(245, 176, 40))


def scales_icon(d, cx, cy, s):
    """Scales of justice."""
    r = s // 2
    col = (31, 58, 110)
    d.line([cx, cy - r, cx, cy + r], fill=col, width=5)
    d.line([cx - r + 6, cy - r + 10, cx + r - 6, cy - r + 10], fill=col, width=5)
    d.ellipse([cx - 5, cy - r - 4, cx + 5, cy - r + 6], fill=col)
    for sx in (cx - r + 6, cx + r - 6):
        d.line([sx, cy - r + 10, sx - 14, cy + r // 3], fill=col, width=3)
        d.line([sx, cy - r + 10, sx + 14, cy + r // 3], fill=col, width=3)
        d.arc([sx - 16, cy + r // 3 - 4, sx + 16, cy + r // 3 + 16], 0, 180, fill=col, width=4)
    d.rectangle([cx - 18, cy + r - 4, cx + 18, cy + r + 4], fill=col)


def chess_icon(d, cx, cy, s):
    """A 4x4 board under a gold crown."""
    r = s // 2
    cell = (s - 16) // 4
    x0, y0 = cx - 2 * cell, cy - 2 * cell + 10
    for row in range(4):
        for col in range(4):
            fill = INK if (row + col) % 2 == 0 else (240, 234, 220)
            d.rectangle([x0 + col * cell, y0 + row * cell,
                         x0 + (col + 1) * cell, y0 + (row + 1) * cell], fill=fill)
    d.rectangle([x0, y0, x0 + 4 * cell, y0 + 4 * cell], outline=INK, width=3)
    crown_y = y0 - 26
    d.polygon([(cx - 30, crown_y + 18), (cx - 30, crown_y), (cx - 15, crown_y + 10),
               (cx, crown_y - 4), (cx + 15, crown_y + 10), (cx + 30, crown_y),
               (cx + 30, crown_y + 18)], fill=(201, 162, 39))
    d.rectangle([cx - 30, crown_y + 18, cx + 30, crown_y + 24], fill=(201, 162, 39))


def burst_icon(d, cx, cy, s):
    """An explosion starburst."""
    import math
    r = s // 2
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r // 2
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=(224, 110, 20))
    d.polygon([(cx, cy - r // 2), (cx + r // 5, cy - r // 5), (cx + r // 2, cy),
               (cx + r // 5, cy + r // 5), (cx, cy + r // 2),
               (cx - r // 5, cy + r // 5), (cx - r // 2, cy),
               (cx - r // 5, cy - r // 5)], fill=(245, 196, 66))


def story_panel(d, x, y, w, h, tag, color, tint, headline, deck, icon):
    panel(d, x, y, w, h, tint, color)
    tag_chip(d, x + 14, y + 14, tag, color)
    icon(d, x + w - 42, y + 36, 48)
    hf = font(SANS_B, 26)
    lines = wrap(d, headline, hf, w - 28)[:2]
    yy = y + 68
    for line in lines:
        d.text((x + 14, yy), line, font=hf, fill=INK)
        yy += 30
    df = font(SANS, 18)
    dlines = wrap(d, deck, df, w - 28)[:3]
    yy = y + 138
    for line in dlines:
        d.text((x + 14, yy), line, font=df, fill=(52, 48, 42))
        yy += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    centred(d, W // 2, 22, "THE WORLD TODAY", font(SERIF_B, 58))
    d.line([28, 100, W - 28, 100], fill=RULE, width=3)
    d.line([28, 106, W - 28, 106], fill=RULE, width=1)
    centred(d, W // 2, 118, "TUESDAY, 24 NOVEMBER 2026", font(SANS_B, 40))
    centred(d, W // 2, 166, "SIX STORIES THAT DEFINED THE DAY",
            font(SANS, 20), fill=GREY)

    # Lead story: Nvidia reinstates Jensen Huang.
    lx, ly, lw, lh = 28, 196, 968, 214
    panel(d, lx, ly, lw, lh, (230, 242, 226), (29, 92, 46))
    d.rectangle([lx, ly + 8, lx + 10, ly + lh - 8], fill=(29, 92, 46))
    tag_chip(d, lx + 26, ly + 16, "BUSINESS · TECH", (29, 92, 46))
    chip_icon(d, lx + lw - 110, ly + 112, 140)
    hf = font(SANS_B, 44)
    d.text((lx + 26, ly + 58), "HUANG IS BACK AT NVIDIA", font=hf, fill=INK)
    df = font(SANS, 22)
    deck = ("Nvidia's board reinstates Jensen Huang as chief executive, days after "
            "he quit over an alleged affair with a suspected spy — shares soar "
            "and Trump claims credit.")
    yy = ly + 116
    for line in wrap(d, deck, df, 680)[:3]:
        d.text((lx + 26, yy), line, font=df, fill=(52, 48, 42))
        yy += 26

    # Row 2.
    y2, ph = 416, 236
    story_panel(d, 28, y2, 316, ph, "CLIMATE", (15, 95, 110), (226, 238, 240),
                "COP31 ENDS WITH NO DEAL",
                "Climate talks in Antalya collapse with no deal; talks may "
                "resume next year.", globe_icon)
    story_panel(d, 356, y2, 316, ph, "ASIA", (179, 64, 31), (247, 230, 220),
                "24 DEAD IN INDONESIA FACTORY FIRE",
                "Fire at a candy factory kills at least 24; 34 more are "
                "missing.", flame_icon)
    story_panel(d, 684, y2, 316, ph, "JUSTICE", (31, 58, 110), (228, 233, 244),
                "MYANMAR GUILTY OF GENOCIDE",
                "The UN's top court rules Myanmar committed genocide against "
                "the Rohingya minority.", scales_icon)

    # Row 3.
    y3 = 668
    story_panel(d, 28, y3, 316, ph, "SPORT", (91, 58, 140), (236, 230, 245),
                "CHESS CROWN ON THE LINE",
                "Gukesh begins his world title defence against Sindarov in "
                "Geneva.", chess_icon)
    story_panel(d, 356, y3, 316, ph, "WAR", (138, 90, 0), (247, 236, 212),
                "14 KILLED IN KYIV STRIKES",
                "Russian strikes kill 14 in Kyiv region; the Russian war "
                "dead pass 700,000.", burst_icon)

    # Also today ticker panel.
    ax, ay, aw = 684, y3, 316
    panel(d, ax, ay, aw, ph, (239, 234, 217), (90, 86, 78))
    tag_chip(d, ax + 14, ay + 14, "ALSO TODAY", (90, 86, 78))
    items = [
        "Trump halts the Army's detonation of unstable explosives in Iowa",
        "Waymo pulls its driverless taxis off all US freeways",
        "UK confirmed as host of the 2035 Women's World Cup",
    ]
    tf = font(SANS, 17)
    yy = ay + 58
    for item in items:
        for line in wrap(d, "•  " + item, tf, aw - 28)[:2]:
            d.text((ax + 14, yy), line, font=tf, fill=(52, 48, 42))
            yy += 21
        yy += 8

    # Footer.
    d.line([28, 922, W - 28, 922], fill=RULE, width=2)
    centred(d, W // 2, 936, "Every story here happened, or was first reported, "
            "on Tuesday 24 November 2026.", font(SANS_B, 19))
    centred(d, W // 2, 966, "Compiled from the day's reporting · One image, one day",
            font(SANS, 16), fill=GREY)

    d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=4)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
