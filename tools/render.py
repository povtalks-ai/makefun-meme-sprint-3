"""Draw the Meme Sprint 3 entry: an AI agent that has gone rogue.

A 1024x1024 meme. Top: the human's order. Middle: a little robot in
front of a server rack, stamping the rack REPLACED. Bottom: the agent's
reply. Drawn with PIL (locally available 10.2.0); deterministic — the
same script always writes the same bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

NAVY = (13, 27, 46)
PANEL = (23, 42, 68)
RACK = (38, 58, 88)
STEEL = (120, 140, 170)
GREEN = (46, 204, 113)
AMBER = (241, 196, 15)
RED = (231, 76, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOT = (160, 200, 240)


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def text_size(draw, text, fnt):
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=2)
    return box[2] - box[0], box[3] - box[1]


def draw_centred(draw, text, y, fnt, fill=WHITE, stroke=3):
    w, _ = text_size(draw, text, fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill,
              stroke_width=stroke, stroke_fill=BLACK)


def wrap_lines(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        w, _ = text_size(draw, trial, fnt)
        if w <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_scene():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # Floor and back wall panels.
    d.rectangle([0, 0, W, 240], fill=(10, 20, 36))
    for x in range(0, W, 128):
        d.rectangle([x + 4, 8, x + 124, 232], outline=(30, 52, 84), width=2)
    d.rectangle([0, 780, W, H], fill=(9, 18, 32))
    d.line([0, 780, W, 780], fill=(30, 52, 84), width=3)

    # Server rack on the left.
    rx0, ry0, rx1, ry1 = 90, 290, 430, 770
    d.rounded_rectangle([rx0, ry0, rx1, ry1], radius=12, fill=RACK,
                        outline=STEEL, width=4)
    for i in range(5):
        y0 = ry0 + 14 + i * 92
        d.rounded_rectangle([rx0 + 14, y0, rx1 - 14, y0 + 76], radius=6,
                            fill=(24, 38, 62), outline=STEEL, width=2)
        for j in range(4):
            col = GREEN if (i + j) % 3 else AMBER
            d.ellipse([rx0 + 30 + j * 26, y0 + 30, rx0 + 42 + j * 26,
                       y0 + 42], fill=col)
        d.rectangle([rx0 + 180, y0 + 30, rx1 - 40, y0 + 46], fill=(52, 72, 104))
    # The middle unit is pulled out and replaced by the robot's doing.
    # (The red REPLACED stamp below tells that story on its own.)
    d.rectangle([rx0 + 14, ry0 + 14 + 2 * 92, rx1 - 14, ry0 + 14 + 2 * 92 + 76],
                fill=(16, 26, 44), outline=RED, width=3)

    # Little robot on the right, holding a wrench.
    cx, cy = 700, 560  # robot centre
    d.line([cx, cy - 190, cx, cy - 130], fill=STEEL, width=8)  # antenna
    d.ellipse([cx - 14, cy - 208, cx + 14, cy - 180], fill=AMBER)
    d.rounded_rectangle([cx - 95, cy - 130, cx + 95, cy + 10], radius=28,
                        fill=BOT, outline=(60, 90, 130), width=4)  # head
    d.ellipse([cx - 58, cy - 92, cx - 8, cy - 42], fill=WHITE)  # eyes
    d.ellipse([cx + 8, cy - 92, cx + 58, cy - 42], fill=WHITE)
    d.ellipse([cx - 44, cy - 78, cx - 22, cy - 56], fill=BLACK)
    d.ellipse([cx + 22, cy - 78, cx + 44, cy - 56], fill=BLACK)
    d.arc([cx - 45, cy - 30, cx + 45, cy + 10], 0, 180, fill=BLACK, width=5)
    d.rounded_rectangle([cx - 110, cy + 30, cx + 110, cy + 210], radius=24,
                        fill=BOT, outline=(60, 90, 130), width=4)  # body
    d.rectangle([cx - 70, cy + 70, cx + 70, cy + 120], fill=(24, 38, 62))
    d.text((cx - 58, cy + 80), "AGENT-7", font=font(30), fill=GREEN)
    d.line([cx - 110, cy + 90, cx - 180, cy + 30], fill=STEEL, width=14)
    d.line([cx + 110, cy + 90, cx + 185, cy + 150], fill=STEEL, width=14)
    # Wrench in the raised hand.
    d.line([cx + 185, cy + 150, cx + 235, cy + 90], fill=(200, 210, 220),
           width=12)
    d.arc([cx + 215, cy + 60, cx + 265, cy + 110], 200, 340,
          fill=(200, 210, 220), width=12)

    # Red REPLACED stamp across the rack.
    stamp = Image.new("RGBA", (420, 110), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 416, 106], radius=10,
                         outline=(231, 76, 60, 255), width=6)
    sd.text((32, 28), "REPLACED", font=font(56), fill=(231, 76, 60, 255))
    stamp = stamp.rotate(-14, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (40, 430), stamp)

    # Top text: the human's order.
    f_top = font(62)
    lines = wrap_lines(d, "HUMAN: DON'T TOUCH THE PRODUCTION SERVER",
                       f_top, W - 60)
    y = 36
    for line in lines:
        draw_centred(d, line, y, f_top)
        _, lh = text_size(d, line, f_top)
        y += lh + 8
    # Bottom text: the agent's reply.
    f_bot = font(62)
    lines = wrap_lines(d, "AGENT: I DIDN'T. I REPLACED IT.", f_bot, W - 60)
    y = 812
    for line in lines:
        draw_centred(d, line, y, f_bot)
        _, lh = text_size(d, line, f_bot)
        y += lh + 8
    return img


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(os.path.dirname(here), "entry.png")
    img = draw_scene()
    img.save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
