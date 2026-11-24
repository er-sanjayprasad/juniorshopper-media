"""Stickman cartoon toolkit: big black heads with warm outline, colourful clothes, stick limbs."""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
BALOO = "/home/claude/fonts/Baloo2.ttf"
def hfont(sz, wt=800):
    f = ImageFont.truetype(BALOO, max(1, int(sz)))
    try: f.set_variation_by_axes([wt])
    except Exception: pass
    return f

def lerp(a, b, t): return a + (b - a) * t
def ease(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def mix(c1, c2, t): return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

FLOOR = 880   # feet line in classroom

# ---------------- backgrounds ----------------
def classroom():
    im = Image.new("RGB", (W, H), (246, 236, 214)); d = ImageDraw.Draw(im)
    for y in range(0, 760):  # warm wall gradient
        d.line([(0, y), (W, y)], fill=mix((250, 242, 225), (238, 224, 196), y / 760))
    d.rectangle([0, 700, W, 760], fill=(222, 200, 165))                    # skirting
    for y in range(760, H):
        d.line([(0, y), (W, y)], fill=mix((226, 196, 150), (206, 170, 120), (y - 760) / 320))
    for k in range(-6, 26):                                               # floor planks (perspective)
        x0 = 960 + (k * 120 - 960) * 0.55; x1 = 960 + (k * 120 - 960) * 1.6
        d.line([(x0, 760), (x1, H)], fill=(196, 160, 112), width=3)
    for y in (830, 920, 1020): d.line([(0, y), (W, y)], fill=(200, 165, 118), width=2)
    # window with light
    d.rectangle([1500, 120, 1880, 560], fill=(196, 150, 100))
    d.rectangle([1520, 140, 1860, 540], fill=(214, 236, 246))
    d.line([(1690, 140), (1690, 540)], fill=(196, 150, 100), width=14); d.line([(1520, 340), (1860, 340)], fill=(196, 150, 100), width=14)
    d.rectangle([1490, 555, 1890, 580], fill=(186, 140, 92))
    pot = (1600, 470); d.polygon([(1570, 555), (1640, 555), (1630, 500), (1580, 500)], fill=(200, 110, 70))
    for a in range(-3, 4): d.line([(1605, 500), (1605 + a * 22, 430 - abs(a) * 6)], fill=(70, 150, 80), width=10)
    # sunlight beam
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(beam)
    bd.polygon([(1520, 140), (1860, 140), (1500, 1080), (900, 1080)], fill=(255, 250, 220, 45))
    beam = beam.filter(ImageFilter.GaussianBlur(30)); im.paste(beam, (0, 0), beam); d = ImageDraw.Draw(im)
    # chalkboard
    d.rounded_rectangle([60, 150, 640, 520], 10, fill=(176, 130, 82))
    d.rectangle([80, 170, 620, 500], fill=(52, 104, 78))
    d.rectangle([80, 500, 620, 516], fill=(150, 108, 66))
    f = hfont(54); d.text((130, 210), "क ख ग  1 2 3", font=f, fill=(235, 240, 230))
    d.line([(140, 330), (360, 330)], fill=(235, 240, 230), width=5); d.ellipse([430, 300, 520, 390], outline=(235, 240, 230), width=5)
    d.rectangle([180, 498, 230, 508], fill="white")
    # clock
    d.ellipse([300, 30, 410, 140], fill=(250, 250, 245), outline=(150, 108, 66), width=8)
    d.line([(355, 85), (355, 50)], fill=(60, 60, 60), width=5); d.line([(355, 85), (385, 95)], fill=(60, 60, 60), width=5)
    # bunting
    cols = [(236, 102, 120), (90, 160, 225), (250, 200, 80), (120, 196, 120), (190, 120, 220)]
    pts = [(700 + i * 80, 40 + 24 * math.sin(i / 11 * math.pi)) for i in range(12)]
    d.line(pts, fill=(140, 110, 80), width=3)
    for i in range(11):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        d.polygon([(xa + 6, ya), (xb - 6, yb), ((xa + xb) / 2, (ya + yb) / 2 + 60)], fill=cols[i % 5])
    # posters
    d.rectangle([700, 150, 840, 300], fill=(250, 250, 248), outline=(220, 210, 190), width=4)
    d.ellipse([735, 175, 805, 245], fill=(236, 102, 120)); d.rectangle([730, 255, 810, 285], fill=(90, 160, 225))
    d.rectangle([880, 130, 1040, 260], fill=(250, 250, 248), outline=(220, 210, 190), width=4)
    d.polygon([(900, 240), (960, 160), (1020, 240)], fill=(120, 196, 120))
    # bookshelf (the kitten's hiding place) — x 1080..1420
    d.rectangle([1080, 300, 1420, 760], fill=(170, 116, 70))
    d.rectangle([1095, 315, 1405, 745], fill=(140, 92, 54))
    for sy in (430, 545, 660): d.rectangle([1095, sy, 1405, sy + 14], fill=(170, 116, 70))
    rnd = random.Random(4)
    for sy in (315, 444, 559):
        x = 1105
        while x < 1390:
            w = rnd.randint(18, 34); h = rnd.randint(70, 105)
            d.rectangle([x, sy + 115 - h, x + w, sy + 113], fill=rnd.choice(cols)); x += w + 3
    d.rectangle([1105, 674, 1395, 742], fill=(120, 80, 48))
    for bx in (1130, 1260): d.rounded_rectangle([bx, 690, bx + 100, 742], 8, fill=rnd.choice(cols))
    # dark gap between shelf and wall (hiding gap)
    d.rectangle([1420, 330, 1470, 760], fill=(40, 28, 22))
    # globe on shelf
    d.ellipse([1200, 210, 1290, 300], fill=(90, 160, 225)); d.ellipse([1220, 230, 1260, 270], fill=(120, 196, 120))
    d.rectangle([1238, 296, 1252, 304], fill=(120, 90, 60))
    # little desks right
    for dx in (1560, 1760):
        d.rectangle([dx - 90, 760, dx + 90, 790], fill=(210, 170, 120)); d.rectangle([dx - 80, 790, dx - 66, 900], fill=(160, 120, 80)); d.rectangle([dx + 66, 790, dx + 80, 900], fill=(160, 120, 80))
    return im

def height_chart(d, x=520, top=180, bottom=FLOOR):
    d.rounded_rectangle([x - 34, top, x + 34, bottom], 10, fill=(250, 250, 245), outline=(200, 190, 170), width=4)
    cols = [(236, 102, 120), (250, 200, 80), (120, 196, 120), (90, 160, 225)]
    n = 12
    for i in range(n):
        y0 = lerp(bottom, top, i / n); y1 = lerp(bottom, top, (i + 1) / n)
        d.rectangle([x - 26, y1 + 3, x + 26, y0 - 3], fill=cols[i % 4])
        d.line([(x - 34, y0), (x - 14, y0)], fill=(80, 80, 80), width=3)

def end_bg():
    im = Image.new("RGB", (W, H), (250, 236, 90)); d = ImageDraw.Draw(im)
    rnd = random.Random(11)
    for _ in range(260):
        x, y = rnd.randint(0, W), rnd.randint(0, H); r = rnd.choice([4, 5, 6])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 200))
    d.ellipse([-260, -260, 380, 300], fill=(240, 80, 110)); d.ellipse([1580, -200, 2200, 360], fill=(40, 140, 240))
    d.ellipse([-200, 860, 420, 1380], fill=(40, 140, 240)); d.ellipse([1600, 820, 2200, 1400], fill=(240, 80, 110))
    return im

# ---------------- characters ----------------
OUT = (245, 168, 92)  # warm outline like the reference
class Kid:
    def __init__(self, shirt, pants=(50, 60, 90), hair="none", dress=False, s=1.0, adult=False, glasses=False):
        self.shirt, self.pants, self.hair, self.dress, self.s, self.adult, self.glasses = shirt, pants, hair, dress, s, adult, glasses

def _line(d, a, b, w, col=(15, 15, 15)): d.line([a, b], fill=col, width=int(w))

def draw_kid(d, k, x, y, expr="happy", talk=False, blink=False, arms="down", walk=0.0, look=0, crouch=0.0, bounce=0.0):
    """x,y: feet centre. expr: happy/sad/worried/smug/wow/laugh/cry. arms: down/wave/up/point/face/hold/clap/reach"""
    s = k.s; y = y - bounce
    leg = 150 * s * (1 - 0.45 * crouch); body = 150 * s; R = 70 * s * (1.08 if not k.adult else 1.0)
    hip = (x, y - leg); neck = (x, hip[1] - body)
    hc = (x + look * 4 * s, neck[1] - R * 0.95)
    lw = max(6, 13 * s)
    # shadow
    d.ellipse([x - 60 * s, y - 10 * s, x + 60 * s, y + 12 * s], fill=(0, 0, 0, 0) if False else (190, 160, 120))
    # legs
    sw = math.sin(walk * math.pi * 2) * 28 * s
    for side, ph in ((-1, sw), (1, -sw)):
        fx = x + side * 26 * s + ph
        knee = (lerp(hip[0] + side * 18 * s, fx, 0.5) + crouch * side * 30 * s, lerp(hip[1], y, 0.5))
        _line(d, (hip[0] + side * 18 * s, hip[1]), knee, lw); _line(d, knee, (fx, y - 6 * s), lw)
        d.ellipse([fx - 22 * s, y - 16 * s, fx + 26 * s, y + 6 * s], fill=(15, 15, 15))
    # body
    if k.dress:
        d.polygon([(neck[0] - 40 * s, neck[1] + 4), (neck[0] + 40 * s, neck[1] + 4), (x + 78 * s, hip[1] + 30 * s), (x - 78 * s, hip[1] + 30 * s)], fill=k.shirt, outline=OUT)
    else:
        d.rounded_rectangle([x - 48 * s, neck[1], x + 48 * s, hip[1] - 30 * s], int(14 * s), fill=k.shirt, outline=OUT, width=max(2, int(4 * s)))
        d.rectangle([x - 46 * s, hip[1] - 34 * s, x + 46 * s, hip[1] + 6 * s], fill=k.pants)
        if not k.adult:
            pass
    # arms
    sh_l = (x - 46 * s, neck[1] + 22 * s); sh_r = (x + 46 * s, neck[1] + 22 * s)
    t = walk
    def arm(sh, side, pose):
        if pose == "down":   hand = (sh[0] + side * 18 * s - side * math.sin(t * math.pi * 2) * 16 * s, sh[1] + 120 * s)
        elif pose == "wave": hand = (sh[0] + side * 70 * s, sh[1] - 90 * s + math.sin(t * 12) * 18 * s)
        elif pose == "up":   hand = (sh[0] + side * 50 * s, sh[1] - 130 * s)
        elif pose == "point":hand = (sh[0] + side * 140 * s, sh[1] - 10 * s)
        elif pose == "face": hand = (hc[0] + side * 40 * s, hc[1] + 30 * s)
        elif pose == "hold": hand = (x + side * 22 * s, sh[1] + 60 * s)
        elif pose == "clap": hand = (x + side * (8 + 22 * abs(math.sin(t * 9))) * s, sh[1] + 30 * s)
        elif pose == "reach":hand = (sh[0] + side * 150 * s, sh[1] + 30 * s)
        elif pose == "hip":  hand = (sh[0] + side * 30 * s, sh[1] + 90 * s)
        else: hand = (sh[0], sh[1] + 120 * s)
        el = (lerp(sh[0], hand[0], 0.5) + side * 14 * s, lerp(sh[1], hand[1], 0.5) + 6 * s)
        _line(d, sh, el, lw * 0.9); _line(d, el, hand, lw * 0.9)
        d.ellipse([hand[0] - 13 * s, hand[1] - 13 * s, hand[0] + 13 * s, hand[1] + 13 * s], fill=(15, 15, 15))
        return hand
    al, ar = (arms if isinstance(arms, tuple) else (arms, arms))
    hl = arm(sh_l, -1, al); hr = arm(sh_r, 1, ar)
    # neck
    _line(d, (x, neck[1] + 6), (x, neck[1] - 12 * s), lw)
    # hair behind (ponytail / bun)
    if k.hair == "ponytail":
        d.ellipse([hc[0] - R - 40 * s, hc[1] - 10 * s, hc[0] - R + 30 * s, hc[1] + 70 * s], fill=(15, 15, 15), outline=OUT, width=max(2, int(4 * s)))
    if k.hair == "bun":
        d.ellipse([hc[0] - 30 * s, hc[1] - R - 40 * s, hc[0] + 30 * s, hc[1] - R + 20 * s], fill=(15, 15, 15), outline=OUT, width=max(2, int(4 * s)))
    # head
    d.ellipse([hc[0] - R - 6 * s, hc[1] - R - 6 * s, hc[0] + R + 6 * s, hc[1] + R + 6 * s], fill=OUT)
    d.ellipse([hc[0] - R, hc[1] - R, hc[0] + R, hc[1] + R], fill=(15, 15, 15))
    if k.hair == "curly":
        for a in range(-4, 5):
            ang = -math.pi / 2 + a * 0.32; cx = hc[0] + math.cos(ang) * R * 0.92; cy = hc[1] + math.sin(ang) * R * 0.92
            d.ellipse([cx - 22 * s, cy - 22 * s, cx + 22 * s, cy + 22 * s], fill=(15, 15, 15), outline=OUT, width=max(2, int(3 * s)))
        d.ellipse([hc[0] - R + 4, hc[1] - R + 14 * s, hc[0] + R - 4, hc[1] + R - 2], fill=(15, 15, 15))
    if k.hair == "spiky":
        for a in (-0.7, -0.25, 0.2, 0.6):
            bx = hc[0] + a * R; by = hc[1] - R * 0.9
            d.polygon([(bx - 24 * s, by + 12 * s), (bx + a * 10 * s, by - 46 * s), (bx + 24 * s, by + 12 * s)], fill=(15, 15, 15), outline=OUT)
        d.ellipse([hc[0] - R + 4, hc[1] - R + 8, hc[0] + R - 4, hc[1] + R - 4], fill=(15, 15, 15))
    if k.hair == "tuft":
        d.arc([hc[0] - 10 * s, hc[1] - R - 40 * s, hc[0] + 40 * s, hc[1] - R + 20 * s], 180, 330, fill=(15, 15, 15), width=int(8 * s))
    # face
    ex = 26 * s; ey = hc[1] - 8 * s
    for sx in (-1, 1):
        cx = hc[0] + sx * ex + look * 8 * s
        if blink or expr == "laugh":
            d.arc([cx - 14 * s, ey - 10 * s, cx + 14 * s, ey + 12 * s], 200, 340, fill="white", width=int(5 * s))
        else:
            d.ellipse([cx - 16 * s, ey - 19 * s, cx + 16 * s, ey + 19 * s], fill="white")
            py = ey + (6 * s if expr in ("sad", "cry") else -2 * s)
            d.ellipse([cx - 8 * s + look * 6 * s, py - 9 * s, cx + 8 * s + look * 6 * s, py + 9 * s], fill=(15, 15, 15))
            if expr == "smug":
                d.rectangle([cx - 17 * s, ey - 20 * s, cx + 17 * s, ey - 3 * s], fill=(15, 15, 15))
                d.line([(cx - 17 * s, ey - 3 * s), (cx + 17 * s, ey - 3 * s)], fill="white", width=int(3 * s))
        if expr in ("sad", "worried", "cry"):
            d.line([(cx - 16 * s, ey - 30 * s + sx * 6 * s), (cx + 14 * s, ey - 30 * s - sx * 6 * s)], fill="white", width=int(4 * s))
        if k.glasses:
            d.ellipse([cx - 22 * s, ey - 24 * s, cx + 22 * s, ey + 24 * s], outline=(200, 200, 210), width=int(4 * s))
    my = hc[1] + 32 * s; mw = 26 * s
    if talk:
        o = 10 * s
        d.chord([hc[0] - mw * 0.8, my - o, hc[0] + mw * 0.8, my + o * 2], 0, 180, fill="white")
    elif expr in ("happy", "laugh"):
        d.arc([hc[0] - mw, my - 22 * s, hc[0] + mw, my + 10 * s], 20, 160, fill="white", width=int(6 * s))
        if expr == "laugh": d.chord([hc[0] - mw, my - 14 * s, hc[0] + mw, my + 18 * s], 0, 180, fill="white")
    elif expr == "smug":
        d.arc([hc[0] - mw * 0.4, my - 20 * s, hc[0] + mw * 1.2, my + 6 * s], 20, 150, fill="white", width=int(6 * s))
    elif expr in ("sad", "cry"):
        d.arc([hc[0] - mw * 0.8, my - 4 * s, hc[0] + mw * 0.8, my + 26 * s], 200, 340, fill="white", width=int(6 * s))
        if expr == "cry": d.ellipse([hc[0] + ex - 6 * s, ey + 22 * s, hc[0] + ex + 6 * s, ey + 40 * s], fill=(120, 190, 255))
    elif expr == "worried":
        pts = [(hc[0] - mw + i * mw / 3, my + (6 * s if i % 2 else -4 * s)) for i in range(7)]
        d.line(pts, fill="white", width=int(5 * s))
    elif expr == "wow":
        d.ellipse([hc[0] - 12 * s, my - 6 * s, hc[0] + 12 * s, my + 20 * s], fill="white")
    return {"head": hc, "R": R, "hand_l": hl, "hand_r": hr, "top": hc[1] - R}

def kitten(d, x, y, s=1.0, t=0.0, curl=False, eyes_only=False):
    if eyes_only:
        for sx in (-1, 1):
            d.ellipse([x + sx * 14 * s - 9 * s, y - 9 * s, x + sx * 14 * s + 9 * s, y + 9 * s], fill=(250, 230, 90))
            d.ellipse([x + sx * 14 * s - 3 * s, y - 8 * s, x + sx * 14 * s + 3 * s, y + 8 * s], fill=(20, 20, 20))
        return
    wh, org = (252, 250, 246), (245, 160, 70)
    tail = math.sin(t * 5) * 14 * s
    d.line([(x - 50 * s, y - 30 * s), (x - 90 * s, y - 80 * s + tail)], fill=org, width=int(14 * s))
    d.ellipse([x - 60 * s, y - 60 * s, x + 40 * s, y], fill=wh, outline=(200, 190, 180), width=2)
    d.ellipse([x - 40 * s, y - 55 * s, x - 5 * s, y - 25 * s], fill=org)
    hx, hy = x + 40 * s, y - 70 * s
    d.polygon([(hx - 34 * s, hy - 20 * s), (hx - 26 * s, hy - 58 * s), (hx - 6 * s, hy - 30 * s)], fill=org)
    d.polygon([(hx + 34 * s, hy - 20 * s), (hx + 26 * s, hy - 58 * s), (hx + 6 * s, hy - 30 * s)], fill=wh, outline=(200, 190, 180))
    d.ellipse([hx - 40 * s, hy - 38 * s, hx + 40 * s, hy + 32 * s], fill=wh, outline=(200, 190, 180), width=2)
    for sx in (-1, 1):
        d.ellipse([hx + sx * 15 * s - 7 * s, hy - 10 * s, hx + sx * 15 * s + 7 * s, hy + 6 * s], fill=(30, 30, 30))
        d.line([(hx + sx * 22 * s, hy + 12 * s), (hx + sx * 50 * s, hy + 6 * s)], fill=(150, 150, 150), width=2)
    d.polygon([(hx - 6 * s, hy + 8 * s), (hx + 6 * s, hy + 8 * s), (hx, hy + 15 * s)], fill=(240, 120, 140))
    for px in (-40, -10, 15):
        d.ellipse([x + px * s, y - 10 * s, x + px * s + 20 * s, y + 4 * s], fill=wh, outline=(200, 190, 180))

def basket(d, x, y, s=1.0):
    d.chord([x - 70 * s, y - 60 * s, x + 70 * s, y + 40 * s], 0, 180, fill=(196, 140, 80), outline=(150, 100, 50), width=4)
    d.arc([x - 55 * s, y - 120 * s, x + 55 * s, y + 10 * s], 180, 360, fill=(150, 100, 50), width=int(8 * s))
    for i in range(-3, 4): d.line([(x + i * 18 * s, y - 8 * s), (x + i * 16 * s, y + 34 * s)], fill=(160, 110, 60), width=3)

# ---------------- UI pieces ----------------
def tag(d, x, y, text, sz=46, bg=(70, 40, 140), fg="white"):
    f = hfont(sz); w = d.textlength(text, font=f)
    d.rounded_rectangle([x - w / 2 - 28, y, x + w / 2 + 28, y + sz * 1.45], int(sz * 0.7), fill=bg, outline=(255, 220, 90), width=5)
    d.text((x - w / 2, y + sz * 0.05), text, font=f, fill=fg)

def pop_text(d, x, y, text, sz, fill=(255, 255, 255), stroke=(70, 40, 140), sw=8):
    f = hfont(sz); w = d.textlength(text, font=f)
    d.text((x - w / 2, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)

def thumbs(d, x, y, s=1.0, col=(255, 255, 255)):
    d.rounded_rectangle([x - 34 * s, y - 10 * s, x + 26 * s, y + 46 * s], int(12 * s), fill=col)
    d.rounded_rectangle([x - 50 * s, y - 6 * s, x - 34 * s, y + 46 * s], int(4 * s), fill=col)
    d.polygon([(x - 30 * s, y - 8 * s), (x - 8 * s, y - 50 * s), (x + 8 * s, y - 44 * s), (x, y - 8 * s)], fill=col)

def bell(d, x, y, s=1.0, ang=0.0, col=(255, 255, 255)):
    dx = math.sin(ang) * 10 * s
    d.chord([x - 30 * s + dx, y - 34 * s, x + 30 * s + dx, y + 40 * s], 180, 360, fill=col)
    d.rectangle([x - 30 * s + dx, y + 2 * s, x + 30 * s + dx, y + 24 * s], fill=col)
    d.rounded_rectangle([x - 38 * s + dx, y + 20 * s, x + 38 * s + dx, y + 30 * s], int(4 * s), fill=col)
    d.ellipse([x - 8 * s + dx * 1.5, y + 28 * s, x + 8 * s + dx * 1.5, y + 42 * s], fill=col)

def subscribe_banner(im, t, x=1920 - 40, y=1080 - 190):
    """slide-in like/subscribe banner, t in seconds since start (show ~6s)"""
    if t < 0 or t > 6.5: return
    a = ease(t / 0.5) * (1 - ease((t - 6.0) / 0.5))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    off = (1 - a) * 900
    x0 = x - 820 + off
    d.rounded_rectangle([x0, y, x0 + 380, y + 120], 60, fill=(40, 120, 230, 255))
    thumbs(d, x0 + 70, y + 50, 0.9); d.text((x0 + 130, y + 20), "लाइक", font=hfont(58), fill="white")
    clicked = t > 3.0
    d.rounded_rectangle([x0 + 400, y, x0 + 820, y + 120], 60, fill=(120, 120, 120, 255) if clicked else (230, 30, 40, 255))
    bell(d, x0 + 470, y + 52, 0.9, ang=math.sin(t * 14) * (1 if t > 3.3 else 0))
    d.text((x0 + 520, y + 20), "सब्सक्राइब्ड" if clicked else "सब्सक्राइब", font=hfont(52), fill="white")
    # tapping hand cursor
    if 1.8 < t < 3.4:
        hx = lerp(x0 + 900, x0 + 640, ease((t - 1.8) / 0.9)); hy = lerp(y + 260, y + 80, ease((t - 1.8) / 0.9))
        d.ellipse([hx - 22, hy - 22, hx + 22, hy + 22], fill=(255, 255, 255, 230), outline=(30, 30, 30), width=4)
    im.paste(ov, (0, 0), ov)
