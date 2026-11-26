import os, sys, subprocess, wave, math, random
sys.path.insert(0, "/home/claude/utoon"); sys.path.insert(0, "/home/claude/toon2"); sys.path.insert(0, "/home/claude/ep3")
from toon import Char, draw, INK, bus_bg, _ell, _poly
from draw import hfont, pop_text, tag, subscribe_banner, end_bg, thumbs, bell, ease, lerp
from PIL import Image, ImageDraw, ImageFilter
from script import SEG

W, H, FPS = 1920, 1080, 30
D = "/home/claude/ep3"
def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
PRE, POST = 0.2, 0.4
VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
EXTRA = {"title": 1.0, "idea": 0.4, "thermo": 0.8, "cured": 0.5, "result": 0.4, "end": 3.0, "end1": 0.4}
DUR = []
for i, (sc, sp, _) in enumerate(SEG):
    last = i == len(SEG) - 1 or SEG[i + 1][0] != sc
    DUR.append(PRE + VL[i] + POST + (EXTRA.get(sc, 0) if last else 0))
SC_START, acc = [], {}
for i, (sc, _, _) in enumerate(SEG):
    SC_START.append(acc.get(sc, 0.0)); acc[sc] = acc.get(sc, 0.0) + DUR[i]
SC_LEN = acc

G = Char("boy", hair="neat", wide=1.35, s=1.0)
P = Char("girl", hair="ponytail", s=0.96)
B = Char("boy", hair="spiky", s=1.04, skin=(236, 192, 150))
C = Char("boy", hair="spiky", s=0.82, skin=(214, 168, 122), glasses=True)
T = Char("girl", shirt=(240, 150, 60), bottom=(200, 60, 90), hair="bun", s=1.22, adult=True, glasses=True)
FL = 1040

def classroom2():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(lerp(186, 160, y / H)), int(lerp(222, 205, y / H)), int(lerp(214, 196, y / H))))
    d.rectangle([0, 760, W, H], fill=(196, 150, 100)); d.line([(0, 760), (W, 760)], fill=INK, width=6)
    for k in range(-8, 30): d.line([(960 + (k * 140 - 960) * 0.5, 760), (960 + (k * 140 - 960) * 1.7, H)], fill=(176, 130, 84), width=4)
    d.rectangle([0, 700, W, 760], fill=(140, 190, 180), outline=INK, width=5)
    d.rounded_rectangle([120, 120, 900, 560], 14, fill=(150, 100, 60), outline=INK, width=7)
    d.rectangle([150, 150, 870, 530], fill=(40, 90, 70), outline=INK, width=5)
    f = hfont(64); d.text((200, 180), "गणित टेस्ट  2 + 2 = ?", font=f, fill=(240, 245, 235))
    d.ellipse([230, 330, 330, 430], outline=(240, 245, 235), width=5)
    d.arc([380, 300, 720, 500], 200, 340, fill=(240, 245, 235), width=5); d.polygon([(700, 360), (735, 380), (700, 400)], fill=(240, 245, 235))
    d.rectangle([1080, 140, 1560, 520], fill=(110, 80, 50), outline=INK, width=7)
    d.rectangle([1104, 164, 1536, 496], fill=(170, 220, 245), outline=INK, width=5)
    d.rectangle([1104, 380, 1536, 496], fill=(120, 180, 100))
    d.ellipse([1380, 250, 1520, 390], fill=(80, 150, 70), outline=INK, width=5); d.rectangle([1440, 380, 1460, 470], fill=(110, 80, 50))
    d.line([(1320, 164), (1320, 496)], fill=INK, width=8)
    d.ellipse([1660, 60, 1790, 190], fill="white", outline=INK, width=7); d.line([(1725, 125), (1725, 80)], fill=INK, width=6); d.line([(1725, 125), (1760, 140)], fill=INK, width=6)
    rnd = random.Random(2)
    cols = [(236, 102, 120), (90, 160, 225), (250, 200, 80), (120, 196, 120)]
    for k, x in enumerate(range(1640, 1900, 70)):
        d.rectangle([x, 300, x + 50, 690], fill=cols[k % 4], outline=INK, width=4)  # lockers
        d.ellipse([x + 32, 480, x + 42, 490], fill=INK)
    return im
BG1 = classroom2(); BGBUS = bus_bg()

def tiffin(d, x, y, s=1.0, open_=False, empty=True):
    if open_:
        _ell(d, [x - 90 * s, y - 40 * s, x + 90 * s, y + 30 * s], (200, 205, 215), 5)
        _ell(d, [x - 75 * s, y - 28 * s, x + 75 * s, y + 18 * s], (150, 155, 165) if empty else (230, 180, 90), 4)
        _ell(d, [x - 70 * s, y - 120 * s, x + 110 * s, y - 60 * s], (210, 215, 225), 5)
    else:
        d.rounded_rectangle([x - 90 * s, y - 70 * s, x + 90 * s, y + 30 * s], int(20 * s), fill=(200, 205, 215), outline=INK, width=5)
        d.line([(x - 90 * s, y - 30 * s), (x + 90 * s, y - 30 * s)], fill=INK, width=4)
        d.arc([x - 40 * s, y - 120 * s, x + 40 * s, y - 50 * s], 180, 360, fill=INK, width=8)

def paratha(d, x, y, s=1.0, bite=False):
    _ell(d, [x - 110 * s, y - 70 * s, x + 110 * s, y + 70 * s], (226, 170, 90), 5)
    rnd = random.Random(1)
    for _ in range(10):
        px, py = x + rnd.randint(-80, 80) * s, y + rnd.randint(-45, 45) * s
        d.ellipse([px - 9 * s, py - 6 * s, px + 9 * s, py + 6 * s], fill=(180, 110, 50))
    d.rounded_rectangle([x - 25 * s, y - 30 * s, x + 25 * s, y + 5 * s], int(6 * s), fill=(255, 235, 120), outline=INK, width=3)
    if bite: d.ellipse([x + 70 * s, y - 80 * s, x + 150 * s, y], fill=(255, 255, 255))

def crumbs(d, x, y, s=1.0):
    rnd = random.Random(5)
    for _ in range(9):
        px, py = x + rnd.randint(-40, 40) * s, y + rnd.randint(-30, 30) * s
        d.ellipse([px - 7 * s, py - 5 * s, px + 7 * s, py + 5 * s], fill=(200, 140, 60), outline=INK, width=2)

def magnifier(d, x, y, s=1.0):
    d.line([(x + 40 * s, y + 40 * s), (x + 110 * s, y + 110 * s)], fill=(120, 70, 30), width=int(22 * s))
    d.ellipse([x - 60 * s, y - 60 * s, x + 60 * s, y + 60 * s], fill=(200, 235, 255), outline=INK, width=int(10 * s))

def think_bubble(d, x, y, w, h, tail):
    for k, r in enumerate([16, 24, 32]):
        cx = lerp(tail[0], x + w * 0.3, (k + 1) / 4); cy = lerp(tail[1], y + h, (k + 1) / 4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white", outline=INK, width=5)
    d.rounded_rectangle([x, y, x + w, y + h], 90, fill="white", outline=INK, width=6)

def speech(d, x, y, text, sz=54, tail=None):
    f = hfont(sz); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x - tw / 2 - 30, y, x + tw / 2 + 30, y + sz * 1.6], 40, fill="white", outline=INK, width=5)
    if tail: d.polygon([(x - 20, y + sz * 1.6 - 3), (x + 20, y + sz * 1.6 - 3), tail], fill="white", outline=INK)
    d.text((x - tw / 2, y + sz * 0.15), text, font=f, fill=INK)

def mouth(on, t): return (0.25 + 0.75 * abs(math.sin(t * 11))) if on else 0.0
def blink(t, k=0):
    p = (t + k * 0.9) % 3.4
    return p < 0.16 or (k % 3 == 0 and 0.32 < p < 0.46)

def camera(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = max(0, min(W - w, cx - w / 2)); y0 = max(0, min(H - h, cy - h / 2))
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)

def samosa(d, x, y, s=1.0):
    _poly(d, [(x - 45 * s, y + 30 * s), (x + 45 * s, y + 30 * s), (x, y - 45 * s)], (225, 160, 60), 4)
    d.line([(x - 20 * s, y + 10 * s), (x + 20 * s, y + 10 * s)], fill=(190, 120, 40), width=3)

def thermometer(d, x, y, s=1.0, level=0.5, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    def P(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    pts = [P(-8 * s, 0), P(8 * s, 0), P(8 * s, -140 * s), P(-8 * s, -140 * s)]
    d.polygon(pts, fill=(240, 245, 250), outline=INK)
    lv = [P(-4 * s, -6 * s), P(4 * s, -6 * s), P(4 * s, -(10 + 120 * level) * s), P(-4 * s, -(10 + 120 * level) * s)]
    d.polygon(lv, fill=(230, 50, 60))
    c = P(0, 0); d.ellipse([c[0] - 14 * s, c[1] - 14 * s, c[0] + 14 * s, c[1] + 14 * s], fill=(230, 50, 60), outline=INK, width=3)

def juice(d, x, y, s=1.0, t=0.0):
    _poly(d, [(x - 35 * s, y - 90 * s), (x + 35 * s, y - 90 * s), (x + 28 * s, y), (x - 28 * s, y)], (200, 230, 240), 4)
    d.polygon([(x - 31 * s, y - 70 * s), (x + 31 * s, y - 70 * s), (x + 27 * s, y - 4 * s), (x - 27 * s, y - 4 * s)], fill=(90, 160, 50))
    for k in range(3):
        a = (t * 0.8 + k / 3) % 1
        d.arc([x - 30 * s + k * 20 * s, y - 150 * s - a * 50 * s, x - 10 * s + k * 20 * s, y - 110 * s - a * 50 * s], 200, 340, fill=(110, 170, 60), width=5)

def paper(d, x, y, s=1.0, text=None):
    d.rectangle([x - 70 * s, y - 90 * s, x + 70 * s, y + 90 * s], fill="white", outline=INK, width=4)
    for k in range(6): d.line([(x - 55 * s, y - 60 * s + k * 25 * s), (x + 55 * s, y - 60 * s + k * 25 * s)], fill=(160, 170, 200), width=3)
    if text: pop_text(d, x, y - 40 * s, text, 70 * s, fill=(230, 40, 60), stroke="white", sw=4)

PREV, PHASE = {}, {}
CH = {"G": G, "P": P, "B": B, "C": C, "T": T}

def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    on = PRE < t < PRE + VL[i]
    tk = {k: mouth(on and sp == k, t) for k in "GPBCTKN"}
    if sc == "end": return fade(i, t, end_card(st))
    im = BG1.copy(); d = ImageDraw.Draw(im)
    zoom, zc = 1.0, (960, 540)
    who = {"G": 420, "P": 760, "B": 1060, "C": 1310, "T": 1660}
    ex = {k: "happy" for k in who}; arms = {k: ("down", "down") for k in who}; look = {k: (0, 0) for k in who}
    first = SC_START[i] < 0.05
    if sc == "title":
        for k in "GPBC": arms[k] = ("down", "wave")
        arms["T"] = ("down", "wave")
    elif sc == "class":
        arms["T"] = ("down", "point") if sp == "T" else ("down", "down")
        ex["G"] = "worried" if not first else "happy"
        if first: zoom, zc = 1.0 + 0.5 * ease(st / 3.0), (420, 560)
    elif sc == "panic":
        ex["G"] = "worried"; arms["G"] = ("chin", "chin"); zoom, zc = 1.7, (420, 470)
    elif sc == "idea":
        ex["G"] = "smug"; arms["G"] = ("down", "up"); zoom, zc = 1.6, (420, 470)
    elif sc == "fake":
        ex["G"] = "sad"; arms["G"] = ("chin", "down") if sp == "G" else ("hold", "hold")
        if sp == "K":
            for k in "PBC": ex[k] = "surprised"
            ex["T"] = "surprised"
    elif sc == "samosa":
        ex["P"] = "angry" if sp == "P" else ("laugh" if sp == "K" else "smug"); arms["P"] = ("hip", "point") if sp == "P" else ("hip", "hip")
        ex["G"] = "worried"
        if sp == "K":
            for k in "BC": ex[k] = "laugh"
            ex["T"] = "laugh"
    elif sc == "thermo":
        who["T"] = lerp(1660, 690, ease(st / 2.4)); ex["T"] = "smug"; ex["G"] = "worried"
        if st > 2.4: arms["T"] = ("down", "hold")
    elif sc == "normal":
        who["T"] = 690; arms["T"] = ("down", "up"); ex["T"] = "smug"; ex["G"] = "surprised"
        if sp in ("B", "K"): ex["B"] = "laugh"; arms["B"] = ("hip", "point")
        if sp == "K": ex["P"] = ex["C"] = "laugh"
    elif sc == "belly":
        who["T"] = 690; ex["G"] = "sad"; arms["G"] = ("hold", "hold"); ex["T"] = "smug"; zoom, zc = 1.4, (520, 520)
    elif sc == "karela":
        who["T"] = 690; arms["T"] = ("down", "hold"); ex["T"] = "happy"
        ex["G"] = "surprised" if sp == "G" else "worried"; arms["G"] = ("chin", "chin") if sp == "G" else ("down", "down")
        zoom, zc = 1.35, (540, 520)
    elif sc == "cured":
        who["T"] = 690; ex["T"] = "surprised"
        ex["G"] = "laugh"; arms["G"] = ("up", "up")
        if sp == "K":
            for k in "PBC": ex[k] = "laugh"
    elif sc == "sit":
        who["T"] = lerp(690, 1660, ease(st / 2.0)); arms["T"] = ("down", "point") if st > 2 else ("down", "down"); ex["G"] = "worried"
    elif sc == "test":
        ex["G"] = "worried" if SC_START[i] < 0.1 else ("laugh" if sp != "C" else "happy"); arms["G"] = ("hold", "hold")
        if sp == "C": ex["C"] = "happy"; who["C"] = 760; who["P"] = 1310; look["C"] = (-0.7, 0)
        zoom, zc = 1.45, (600, 520)
    elif sc == "result":
        who["T"] = 1450; arms["T"] = ("down", "up"); ex["T"] = "happy"
        ex["G"] = "surprised" if sp != "G" else "laugh"
        if sp == "G": arms["G"] = ("up", "up")
    elif sc == "moral":
        arms["T"] = ("down", "wave")
    elif sc == "end1":
        for k in "PBC": ex[k] = "laugh"
        ex["G"] = "laugh"; arms["G"] = ("down", "hold"); ex["T"] = "laugh"
    off = max(0, (who["T"] + 320) - who["P"]) if who["T"] < 1500 else 0
    if off:
        for k in "PBC": who[k] += off
    if sp in who:
        for k in who:
            if k != sp and look[k] == (0, 0): look[k] = (0.6 if who[sp] > who[k] else -0.6, 0)
    walkph = {}
    for k in who:
        key = (i, k)
        if key in PREV and abs(who[k] - PREV[key]) > 0.8:
            PHASE[k] = PHASE.get(k, 0.0) + abs(who[k] - PREV[key]) / (190 * CH[k].s); walkph[k] = PHASE[k]
        PREV[key] = who[k]
    infos = {}
    for k in sorted(who, key=lambda k: who[k]):
        lb = abs(math.sin(st * 9 + ord(k))) * 14 if ex[k] == "laugh" else 0
        if sc == "cured" and k == "G": lb = abs(math.sin(st * 6)) * 80
        kt = tk["K"] * 0.8 if sp == "K" and k != "T" else 0
        infos[k] = draw(d, CH[k], who[k], FL - lb, ex[k], talk=max(tk.get(k, 0), kt), blink=blink(st, ord(k)), look=look[k], arms=arms[k], t=st, walk=walkph.get(k))
    gi = infos["G"]; ti = infos["T"]
    # props & effects
    if sc == "title":
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(st / 0.6); od.rounded_rectangle([400, 70, 1520, 290], 60, fill=(255, 255, 255, int(235 * a)), outline=(255, 200, 60, int(255 * a)), width=10)
        im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
        if a > 0.5: pop_text(d, 960, 95, "गोलू का नकली बुखार!", 120, fill=(230, 60, 60), stroke="white", sw=10)
    if sc == "class" and not first: pop_text(d, 520, 160, "गणित टेस्ट!", 90, fill=(255, 220, 60), stroke=INK)
    if sc == "panic":
        for k in range(3):
            a = (st * 1.5 + k / 3) % 1; d.ellipse([gi["head"][0] + 120 + k * 15, gi["head"][1] - 60 + a * 80, gi["head"][0] + 140 + k * 15, gi["head"][1] - 30 + a * 80], fill=(120, 190, 255), outline=INK, width=2)
    if sc == "idea":
        hx, hy = gi["head"][0], gi["top"] - 80
        _ell(d, [hx - 40, hy - 50, hx + 40, hy + 30], (255, 235, 80), 5); d.rectangle([hx - 18, hy + 26, hx + 18, hy + 46], fill=(150, 150, 160), outline=INK, width=3)
        for k in range(8):
            a = k * math.pi / 4; d.line([(hx + math.cos(a) * 60, hy - 10 + math.sin(a) * 60), (hx + math.cos(a) * 85, hy - 10 + math.sin(a) * 85)], fill=(255, 210, 40), width=6)
    if sc == "fake" and sp == "G":
        for k in range(3):
            a = st * 3 + k * 2.1; d.ellipse([gi["head"][0] + math.cos(a) * 140 - 10, gi["top"] - 20 + math.sin(a) * 30 - 10, gi["head"][0] + math.cos(a) * 140 + 10, gi["top"] - 20 + math.sin(a) * 30 + 10], fill=(255, 220, 60), outline=INK, width=2)
        pop_text(d, gi["head"][0] + 300, 160, "आह्ह... ओह्ह...", 70, fill="white", stroke=INK)
    if sc == "samosa" and sp == "P":
        think_bubble(d, 900, 120, 420, 200, (infos["P"]["head"][0] + 60, infos["P"]["top"] - 10))
        for k in range(3): samosa(d, 990 + k * 120, 220, 1.0)
        pop_text(d, 1110, 330, "3 समोसे!", 56, fill=(230, 60, 60), stroke="white", sw=4)
    if sc in ("samosa", "normal", "cured", "end1") and sp == "K":
        for k, (x, y) in enumerate([(820, 200), (1150, 240), (1450, 190)]):
            if t > 0.2 + k * 0.3: pop_text(d, x, y - 10 * math.sin(t * 8 + k), "हा हा!", 80, fill=(255, 220, 60), stroke=INK)
    if sc == "thermo" and st > 2.4:
        hx, hy = gi["head"]; lvl = min(0.55, (st - 2.4) / 4 * 0.55)
        thermometer(d, hx + 30, hy + 75, 0.9, lvl, ang=-1.2)
    if sc == "normal":
        hx, hy = ti["hand_r"]; thermometer(d, hx, hy + 10, 1.0, 0.55)
        if t > PRE: tag(d, ti["head"][0] + 260, 160, "98.6°F  नॉर्मल!", 60, bg=(30, 140, 80))
    if sc == "karela":
        hx, hy = ti["hand_r"]; juice(d, hx + 10, hy + 20, 1.1, st)
        pop_text(d, hx + 330, hy - 120, "करेले का जूस", 56, fill=(110, 200, 60), stroke=INK)
        if sp == "G": pop_text(d, gi["head"][0] - 60, gi["top"] - 120, "छी!", 120, fill=(110, 200, 60), stroke=INK)
    if sc == "cured" and SC_START[i] < 0.1:
        for k, w_ in enumerate(["पेट दर्द ✗", "सिर दर्द ✗", "बुखार ✗"]):
            if su > 0.15 + k * 0.15: tag(d, 1250, 150 + k * 110, w_.replace(" ✗", "  ठीक!"), 50, bg=(30, 140, 80))
    if sc == "test":
        hx, hy = (gi["hand_l"][0] + gi["hand_r"][0]) / 2, gi["hand_l"][1] - 40
        paper(d, hx, hy, 1.0)
        if SC_START[i] > 2:
            n = 4 - (2 if su > 0.55 else 0)
            for k in range(4):
                if k < n: samosa(d, 980 + k * 110, 230, 0.9)
            if su > 0.55: pop_text(d, 1150, 320, "4 − 2 = 2", 70, fill=(255, 220, 60), stroke=INK)
    if sc == "result":
        hx, hy = ti["hand_r"]; paper(d, hx, hy - 60, 1.2, "8/10")
        if sp == "G": pop_text(d, gi["head"][0], gi["top"] - 130, "आठ?!", 110, fill=(255, 220, 60), stroke=INK)
    if sc == "moral" and su > 0.4: pop_text(d, 960, 110, "बहाने नहीं, कोशिश!", 110, fill="white", stroke=(240, 80, 110))
    if sc == "end1":
        hx, hy = gi["hand_r"]; samosa(d, hx, hy - 20, 0.9)
    if sc == "fake" and SC_START[i] < 0.1: subscribe_banner(im, t)
    im = camera(im, zc[0], zc[1], zoom)
    return fade(i, t, im)

def end_card(st):
    im = end_bg(); d = ImageDraw.Draw(im)
    for ch, x, k in [(G, 260, 1), (P, 520, 2), (B, 1420, 3), (C, 1680, 4)]: draw(d, ch, x, 1060, "happy", blink=blink(st, k), arms=("down", "wave"), t=st)
    pop_text(d, 960, 70, "गोलू का कारनामा पसंद आया?", 92, fill=(240, 80, 110), stroke=(255, 255, 255), sw=10)
    clicked = st > 6.0; pulse = 1 + 0.05 * math.sin(st * 6); bw, bh = 560 * pulse, 140 * pulse
    d.rounded_rectangle([960 - bw / 2, 300, 960 + bw / 2, 300 + bh], 70, fill=(130, 130, 130) if clicked else (230, 30, 40))
    bell(d, 960 - bw / 2 + 90, 300 + bh / 2 - 6, 1.2, ang=math.sin(st * 14) if clicked else 0)
    d.text((960 - bw / 2 + 150, 300 + bh * 0.12), "सब्सक्राइब्ड" if clicked else "सब्सक्राइब", font=hfont(76 * pulse), fill="white")
    d.rounded_rectangle([660, 490, 940, 600], 55, fill=(40, 120, 230)); thumbs(d, 725, 532, 0.9); d.text((785, 498), "लाइक", font=hfont(56), fill="white")
    d.rounded_rectangle([980, 490, 1220, 600], 55, fill=(40, 170, 90)); d.text((1030, 498), "शेयर", font=hfont(56), fill="white")
    if 4.5 < st < 6.2:
        hx = lerp(1300, 1000, ease((st - 4.5) / 1.0)); hy = lerp(700, 380, ease((st - 4.5) / 1.0))
        d.ellipse([hx - 26, hy - 26, hx + 26, hy + 26], fill="white", outline=INK, width=5)
    tag(d, 960, 680, "हर शनिवार गोलू का नया कारनामा", 50, bg=(240, 80, 110))
    return im

def fade(i, t, im):
    sc = SEG[i][0]
    fi = min(1, t / 0.3) if (i == 0 or SEG[i - 1][0] != sc) and sc in ("title", "result", "end") else 1
    fo = min(1, (DUR[i] - t) / 0.3) if (i == len(SEG) - 1 or SEG[i + 1][0] != sc) and sc in ("test", "end") else 1
    f = min(fi, fo)
    return Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, f)) if f < 1 else im

def render(i):
    n = int(round(DUR[i] * FPS)); tmp = f"{D}/seg{i:02d}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frame(i, k / FPS).tobytes())
    p.stdin.close(); assert p.wait() == 0
    os.rename(tmp, f"{D}/seg{i:02d}.mp4")

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        idx = [int(x) for x in sys.argv[2].split(",")]
        tiles = [frame(i, DUR[i] * 0.6).resize((640, 360)) for i in idx]
        sh = Image.new("RGB", (1920, 360 * ((len(tiles) + 2) // 3)))
        for k, tl in enumerate(tiles): sh.paste(tl, ((k % 3) * 640, (k // 3) * 360))
        sh.save(f"{D}/sheet.png")
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor() as ex: list(ex.map(render, range(len(SEG))))
        print(round(sum(DUR), 1))
