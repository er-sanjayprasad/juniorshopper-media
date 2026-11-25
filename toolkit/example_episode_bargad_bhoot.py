import os, sys, subprocess, wave, math, random
sys.path.insert(0, "/home/claude/utoon"); sys.path.insert(0, "/home/claude/toon2"); sys.path.insert(0, "/home/claude/ep2")
from toon import Char, draw, INK, _ell, _poly
from draw import hfont, pop_text, tag, subscribe_banner, end_bg, thumbs, bell, ease, lerp
from PIL import Image, ImageDraw, ImageFilter
from script import SEG

W, H, FPS = 1920, 1080, 30
D = "/home/claude/ep2"
def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
PRE, POST = 0.2, 0.4
VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
EXTRA = {"title": 1.0, "ghost": 0.8, "run": 0.6, "reveal1": 0.5, "bunty": 0.6, "end": 3.0, "end1": 0.4, "night": 0.5}
DUR = []
for i, (sc, sp, _) in enumerate(SEG):
    last = i == len(SEG) - 1 or SEG[i + 1][0] != sc
    DUR.append(PRE + VL[i] + POST + (EXTRA.get(sc, 0) if last else 0))
SC_START, acc = [], {}
for i, (sc, _, _) in enumerate(SEG):
    SC_START.append(acc.get(sc, 0.0)); acc[sc] = acc.get(sc, 0.0) + DUR[i]
SC_LEN = acc

G = Char("boy", shirt=(250, 200, 60), bottom=(60, 90, 160), hair="neat", wide=1.35, tie=False)
P = Char("girl", shirt=(240, 120, 160), bottom=(120, 60, 140), hair="ponytail", s=0.96, tie=False)
B = Char("boy", shirt=(70, 150, 230), bottom=(40, 42, 60), hair="spiky", s=1.04, skin=(236, 192, 150), tie=False)
C = Char("boy", shirt=(110, 190, 110), bottom=(90, 70, 50), hair="spiky", s=0.82, skin=(214, 168, 122), glasses=True, tie=False)
R = Char("boy", shirt=(240, 140, 60), bottom=(245, 245, 240), hair="neat", s=0.95, skin=(196, 146, 100), tie=False)
A = Char("girl", shirt=(245, 245, 240), bottom=(240, 240, 235), hair="bun", s=1.18, adult=True, glasses=True, hc=(200, 200, 205), skin=(236, 196, 156))
FL = 1040
TREE_X = 1500

def village(night=False):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    top, bot = ((120, 190, 240), (220, 240, 250)) if not night else ((10, 16, 50), (40, 50, 100))
    for y in range(700): d.line([(0, y), (W, y)], fill=tuple(int(lerp(top[k], bot[k], y / 700)) for k in range(3)))
    if night:
        rnd = random.Random(4)
        for _ in range(150):
            x, y = rnd.randint(0, W), rnd.randint(0, 600); r = rnd.choice([1, 2, 2, 3]); d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 220))
        d.ellipse([200, 80, 340, 220], fill=(255, 250, 210), outline=INK, width=4)
    else:
        d.ellipse([200, 80, 340, 220], fill=(255, 220, 80), outline=INK, width=5)
    def nc(c): return c if not night else tuple(int(v * 0.42) for v in c)
    # far fields and hills
    d.polygon([(0, 620), (400, 520), (800, 600), (1200, 510), (1920, 600), (1920, 720), (0, 720)], fill=nc((130, 180, 100)), outline=INK)
    d.rectangle([0, 700, W, H], fill=nc((200, 170, 110))); d.line([(0, 700), (W, 700)], fill=INK, width=5)
    for k in range(12): d.line([(k * 180 - 100, 720), (k * 180 + 60, H)], fill=nc((185, 152, 96)), width=4)
    # huts
    for hx in (120, 560):
        d.rectangle([hx, 480, hx + 300, 720], fill=nc((210, 150, 90)), outline=INK, width=6)
        d.polygon([(hx - 40, 490), (hx + 150, 360), (hx + 340, 490)], fill=nc((190, 160, 70)), outline=INK)
        for k in range(8): d.line([(hx - 20 + k * 45, 485), (hx + 150, 370)], fill=nc((160, 130, 50)), width=3)
        d.rectangle([hx + 110, 590, hx + 190, 720], fill=nc((110, 70, 40)), outline=INK, width=5)
    # well
    d.ellipse([920, 640, 1100, 690], fill=nc((150, 150, 160)), outline=INK, width=5); d.rectangle([920, 665, 1100, 740], fill=nc((150, 150, 160)), outline=INK, width=5)
    d.line([(930, 665), (930, 560), (1090, 560), (1090, 665)], fill=INK, width=8)
    # haystack
    d.chord([1050, 560, 1300, 820], 180, 360, fill=nc((230, 190, 80)), outline=INK, width=5); d.rectangle([1050, 690, 1300, 720], fill=nc((230, 190, 80)))
    # banyan tree
    tx = TREE_X
    d.polygon([(tx - 90, 720), (tx - 60, 330), (tx + 60, 330), (tx + 100, 720)], fill=nc((120, 80, 50)), outline=INK)
    for k in range(-6, 7):
        if abs(k) > 1: d.line([(tx + k * 55, 300), (tx + k * 58, 690)], fill=nc((110, 75, 45)), width=6)
    d.line([(tx - 40, 360), (tx - 300, 280)], fill=nc((120, 80, 50)), width=34)
    leaf = [nc((60, 130, 60)), nc((80, 150, 70)), nc((50, 115, 55))]
    for k, (dx, dy, r) in enumerate([(0, 180, 220), (-250, 230, 170), (250, 220, 180), (-120, 90, 170), (140, 80, 170), (380, 160, 120), (-380, 170, 120)]):
        d.ellipse([tx + dx - r, dy - r, tx + dx + r, dy + r], fill=leaf[k % 3], outline=INK, width=4)
    if night:
        v = Image.new("RGBA", (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(v)
        vd.ellipse([-300, -200, W + 300, H + 300], fill=(0, 0, 0, 0)); im = im
    return im
BG_DAY = village(False); BG_NIGHT = village(True)

def laddoo_plate(d, x, y):
    _ell(d, [x - 80, y - 20, x + 80, y + 20], (230, 230, 235), 4)
    for k, (dx, dy) in enumerate([(-35, -20), (0, -25), (35, -20), (-15, -45), (18, -45)]):
        _ell(d, [x + dx - 20, y + dy - 18, x + dx + 20, y + dy + 18], (245, 170, 40), 3)

def charpai(d, x, y):
    d.rectangle([x - 260, y - 90, x + 260, y - 60], fill=(150, 100, 60), outline=INK, width=4)
    for k in range(-240, 260, 30): d.line([(x + k, y - 88), (x + k + 20, y - 62)], fill=(230, 210, 170), width=3)
    for lx in (-250, 250): d.rectangle([x + lx - 10, y - 60, x + lx + 10, y], fill=(120, 80, 50), outline=INK, width=3)

def cloth_ghost(d, x, y, t, s=1.0, reveal=False):
    pts = [(x - 70 * s, y)]
    for k in range(9):
        pts.append((x - 70 * s + k * 17.5 * s, y + 210 * s + math.sin(t * 6 + k) * 18 * s))
    pts.append((x + 70 * s, y))
    _poly(d, [(px + math.sin(t * 3) * 12 * s, py) for px, py in pts], (250, 250, 252) if not reveal else (245, 245, 238), 5)
    if not reveal:
        for ex in (-25, 25): d.ellipse([x + ex * s - 14 * s + math.sin(t * 3) * 12 * s, y + 60 * s, x + ex * s + 14 * s + math.sin(t * 3) * 12 * s, y + 95 * s], fill=(40, 40, 50))
    else:
        d.line([(x - 60 * s, y + 140 * s), (x + 60 * s, y + 150 * s)], fill=(200, 120, 60), width=int(8 * s))  # dhoti border

def owl(d, x, y, s=1.0, t=0.0, lit=False):
    col = (140, 100, 70) if lit else (40, 35, 40)
    _ell(d, [x - 55 * s, y - 70 * s, x + 55 * s, y + 70 * s], col, 5)
    _poly(d, [(x - 50 * s, y - 50 * s), (x - 40 * s, y - 95 * s), (x - 15 * s, y - 60 * s)], col, 4)
    _poly(d, [(x + 50 * s, y - 50 * s), (x + 40 * s, y - 95 * s), (x + 15 * s, y - 60 * s)], col, 4)
    blink = (t % 2.5) < 0.15
    for ex in (-24, 24):
        if blink: d.line([(x + ex * s - 20 * s, y - 25 * s), (x + ex * s + 20 * s, y - 25 * s)], fill=INK, width=5)
        else:
            _ell(d, [x + ex * s - 24 * s, y - 50 * s, x + ex * s + 24 * s, y - 2 * s], (255, 220, 60), 4)
            d.ellipse([x + ex * s - 9 * s, y - 35 * s, x + ex * s + 9 * s, y - 17 * s], fill=INK)
    _poly(d, [(x - 9 * s, y - 5 * s), (x + 9 * s, y - 5 * s), (x, y + 14 * s)], (240, 170, 50), 3)
    if lit:
        for k in range(3): d.arc([x - 35 * s, y + k * 15 * s, x + 35 * s, y + 30 * s + k * 15 * s], 20, 160, fill=(100, 70, 50), width=3)

def torch_beam(im, x0, y0, x1, y1, spread=160):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    ang = math.atan2(y1 - y0, x1 - x0); px, py = -math.sin(ang), math.cos(ang)
    od.polygon([(x0, y0), (x1 + px * spread, y1 + py * spread), (x1 - px * spread, y1 - py * spread)], fill=(255, 245, 180, 90))
    od.ellipse([x1 - spread, y1 - spread, x1 + spread, y1 + spread], fill=(255, 245, 180, 70))
    ov = ov.filter(ImageFilter.GaussianBlur(14)); im.paste(ov, (0, 0), ov)

def lantern(d, x, y, t):
    d.line([(x, y - 60), (x, y - 40)], fill=INK, width=5)
    _ell(d, [x - 30, y - 45, x + 30, y + 30], (255, 200, 80), 4)
    d.rectangle([x - 34, y + 22, x + 34, y + 36], fill=(80, 60, 40), outline=INK, width=3)

def mouth(on, t): return (0.25 + 0.75 * abs(math.sin(t * 11))) if on else 0.0
def blink(t, k=0):
    p = (t + k * 0.9) % 3.4
    return p < 0.16 or (k % 3 == 0 and 0.32 < p < 0.46)
def camera(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = max(0, min(W - w, cx - w / 2)); y0 = max(0, min(H - h, cy - h / 2))
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)

PREV, PHASE = {}, {}
CH = {"G": G, "P": P, "B": B, "C": C, "R": R, "A": A}

def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    on = PRE < t < PRE + VL[i]
    tk = {k: mouth(on and sp == k, t) for k in "GPBCRAKNO"}
    night = sc not in ("title", "arrive", "raju", "brag", "end")
    if sc == "end": return fade(i, t, end_card(st))
    im = (BG_NIGHT if night else BG_DAY).copy(); d = ImageDraw.Draw(im)
    zoom, zc = 1.0, (960, 540)
    who = {}; ex = {}; arms = {}; look = {}
    def put(k, x, e="happy", a=("down", "down"), lk=(0, 0)): who[k] = x; ex[k] = e; arms[k] = a; look[k] = lk
    props_after = []
    if sc == "title":
        for k, x in zip("GPBC", (300, 620, 940, 1240)): put(k, x, "happy", ("down", "wave"))
    elif sc == "arrive":
        ent = -1100 * (1 - ease(st / 2.8))
        put("G", 420 + ent, "laugh" if SC_START[i] < 0.1 else "happy", ("up", "up") if (SC_START[i] < 3 and st > 2.8) else ("down", "down"), (0.5, 0)); put("P", 700 + ent); put("B", 920 + ent); put("C", 1120 + ent)
        put("A", 1550, "happy", ("hold", "wave") if sp == "A" else ("hold", "hold"), (-0.6, 0))
    elif sc == "raju":
        put("G", 380, "surprised" if sp == "K" else "happy", lk=(0.6, 0)); put("P", 640, "surprised" if sp == "K" else "happy", lk=(0.6, 0)); put("B", 880, lk=(0.6, 0)); put("C", 1090, lk=(0.6, 0))
        rx = lerp(2100, 1400, ease(st / 2.0)); put("R", rx, "worried" if sp == "R" else "happy", ("down", "point") if sp == "R" else ("down", "down"), (-0.6, 0))
        if sp == "R": zoom, zc = 1.3, (1100, 560)
    elif sc == "brag":
        put("G", 380, lk=(0.5, 0)); put("P", 640, lk=(0.5, 0)); put("B", 900, "smug" if sp == "B" else "happy", ("hip", "hip") if sp == "B" else ("down", "down"), (0.3, 0))
        put("C", 1130, "worried", ("down", "point") if sp == "C" else ("down", "down"), (0.6, 0)); put("R", 1400, "worried", ("down", "up") if sp == "R" else ("down", "down"), (-0.6, 0))
    elif sc == "night":
        charpai(d, 620, FL - 40)
        sleepy = SC_START[i] < 0.1
        for k, x in zip("GPBC", (380, 560, 760, 940)):
            put(k, x, "happy" if sleepy else "surprised", lk=(0.8, -0.3) if not sleepy else (0, 0))
        if sp == "O" and on: pop_text(d, TREE_X, 120, "हू... हू...", 80, fill=(200, 220, 255), stroke=INK)
    elif sc == "ghost":
        if SC_START[i] < 0.1: zoom, zc = 1.0 + 0.8 * ease(st / 2.0), (TREE_X - 250, 420)
        else:
            for k, x in zip("GPBC", (380, 560, 760, 940)): put(k, x, "surprised", ("up", "up"), (0.8, 0))
        props_after.append(lambda d: cloth_ghost(d, TREE_X - 290, 290, st, 1.5))
        if sp == "K": pop_text(d, 700, 160, "भूत!!", 140, fill=(255, 80, 80), stroke="white")
    elif sc == "run":
        put("G", 380, "surprised", ("up", "up"), (0.6, 0)); put("P", 560, "surprised", lk=(0.6, 0)); put("C", 740, "surprised", lk=(0.6, 0))
        bx = 940 - ease((st - 1.5) / 2.0) * 1400 if st > 1.5 else 940
        put("B", bx, "surprised", ("up", "up"), (-0.8, 0))
        props_after.append(lambda d: cloth_ghost(d, TREE_X - 290, 290, st, 1.5))
    elif sc == "scared":
        put("G", 520, "worried", ("chin", "chin") if sp == "G" else ("down", "down"), (0.5, 0)); put("P", 860, "angry" if sp == "P" else "happy", ("hip", "point") if sp == "P" else ("hip", "hip"), (-0.5, 0))
        put("C", 1120, "happy", ("down", "up") if sp == "C" else ("down", "down"), (-0.5, 0))
        props_after.append(lambda d: cloth_ghost(d, TREE_X - 290, 290, st, 1.5))
        if sp == "G": zoom, zc = 1.4, (650, 540)
    elif sc == "walk":
        p = ease(st / SC_LEN[sc])
        base = lerp(380, 820, p)
        put("C", base + 260, "worried", ("down", "point"), (0.6, -0.3)); put("P", base + 60, "worried", lk=(0.6, -0.3)); put("G", base - 180, "worried", ("down", "hold"), (0.6, -0.3))
        props_after.append(lambda d: cloth_ghost(d, TREE_X - 290, 290, st, 1.5))
        if sp == "O" and on: pop_text(d, TREE_X + 200, 120, "हू... हू...", 80, fill=(200, 220, 255), stroke=INK)
    elif sc in ("reveal1", "reveal2"):
        put("C", 1080, "happy", ("down", "point"), (0.6, -0.5)); put("P", 880, "happy" if sc == "reveal2" else "surprised", lk=(0.6, -0.5)); put("G", 640, "surprised", lk=(0.6, -0.5))
        zoom, zc = 1.35, (1250, 480)
    elif sc == "nani":
        put("C", 900, "happy", lk=(0.6, 0)); put("P", 700, "laugh"); put("G", 480, "laugh")
        put("A", lerp(2100, 1250, ease(st / 2.5)), "laugh", ("hold", "up"), (0.3, -0.3))
    elif sc == "bunty":
        put("C", 700, "laugh" if sp == "K" else "happy", lk=(0.6, 0)); put("P", 520, "laugh" if sp == "K" else "happy", lk=(0.6, 0)); put("G", 320, "laugh" if sp == "K" else "happy", lk=(0.6, 0))
        put("A", 1700, "laugh", ("hold", "hold"), (-0.6, 0))
        up = ease((st - 1.5) / 1.0)
        put("B", 1170, "worried", ("down", "down"), (-0.5, 0))
    elif sc == "moral":
        put("G", 380, lk=(0.6, 0)); put("P", 600, lk=(0.6, 0)); put("B", 820, lk=(0.6, 0)); put("C", 1020, lk=(0.6, 0))
        put("A", 1450, "happy", ("hold", "wave"), (-0.6, 0))
    elif sc == "raju2":
        put("G", 380, "laugh", lk=(0.6, 0)); put("P", 600, "happy", lk=(0.6, 0)); put("B", 820, "smug", ("hip", "hip"), (0.6, 0)); put("C", 1020, "happy", lk=(0.6, 0))
        put("R", 1350, "laugh", ("down", "up"), (-0.6, 0))
    elif sc == "end1":
        for k, x in zip("GPBC", (380, 640, 900, 1130)): put(k, x, "laugh")
        arms["G"] = ("up", "up"); put("A", 1500, "laugh", ("hold", "hold"), (-0.6, 0)); put("R", 1750, "laugh", lk=(-0.6, 0))
    # draw characters (ordered by x)
    infos = {}
    if sc == "bunty":
        # haystack with Bunty popping out
        up = ease((st - 1.2) / 1.0)
        spr = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(spr)
        bi = draw(sd, B, 1170, FL + 330 - up * 330, "worried", talk=tk["B"], blink=blink(st, 3), look=(-0.5, 0), t=st)
        hx, hy = bi["head"]
        for k in range(12):
            a = -math.pi + k * math.pi / 11; sd.line([(hx + math.cos(a) * 80, hy - 90 + math.sin(a) * 40), (hx + math.cos(a) * 150, hy - 120 + math.sin(a) * 70)], fill=(230, 190, 80), width=7)
        mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).rectangle([0, 0, W, 900], fill=255)
        im.paste(spr, (0, 0), Image.composite(spr.split()[3], Image.new("L", (W, H), 0), mask))
        d = ImageDraw.Draw(im)
        d.chord([900, 740, 1440, 1180], 180, 360, fill=(120, 100, 45), outline=INK, width=5)
        d.rectangle([900, 958, 1440, 1080], fill=(120, 100, 45))
        for k in range(14): d.line([(930 + k * 36, 960), (950 + k * 36, 800 + abs(7 - k) * 12)], fill=(150, 125, 60), width=4)
        del who["B"]
        if sp == "K": pop_text(d, 960, 120, "हा हा हा!", 110, fill=(255, 220, 60), stroke=INK)
    walkph = {}
    for k in who:
        key = (i, k)
        if key in PREV and abs(who[k] - PREV[key]) > 0.8:
            PHASE[k] = PHASE.get(k, 0.0) + abs(who[k] - PREV[key]) / (190 * CH[k].s)
            walkph[k] = PHASE[k]
        PREV[key] = who[k]
    if sp in who:
        for k in who:
            if k != sp and look[k] == (0, 0): look[k] = (0.6 if who[sp] > who[k] else -0.6, 0)
    for k in sorted(who, key=lambda k: who[k]):
        lb = abs(math.sin(st * 9 + ord(k))) * 14 if ex[k] == "laugh" else 0
        kt = tk["K"] * 0.8 if sp == "K" and k not in ("A", "R") else 0
        infos[k] = draw(d, CH[k], who[k], FL - lb, ex[k], talk=max(tk.get(k, 0), kt), blink=blink(st, ord(k)), look=look[k], arms=arms[k], t=st, walk=walkph.get(k))
    # props
    for f in props_after: f(d)
    if sc in ("reveal1", "reveal2", "nani", "bunty", "moral", "raju2", "end1"):
        if sc != "reveal2": owl(d, TREE_X - 120, 330, 1.0, st, lit=True)
        if sc in ("reveal1",): cloth_ghost(d, TREE_X - 290, 290, st, 1.5, reveal=True)
        if sc == "reveal2": owl(d, TREE_X - 120, 330, 1.0, st, lit=True); cloth_ghost(d, TREE_X - 290, 290, st, 1.5, reveal=True)
    elif night and sc not in ("night",):
        owl(d, TREE_X - 120, 330, 1.0, st, lit=False)
    elif sc == "night":
        owl(d, TREE_X - 120, 330, 1.0, st, lit=False)
    if sc in ("walk", "reveal1", "reveal2") and "C" in infos:
        hx, hy = infos["C"]["hand_r"]
        d.rounded_rectangle([hx - 10, hy - 18, hx + 40, hy + 8], 6, fill=(200, 60, 60), outline=INK, width=3)
        target = (TREE_X - 120, 330) if sc != "reveal2" else (TREE_X - 270, 400)
        torch_beam(im, hx + 40, hy - 5, target[0], target[1], 150); d = ImageDraw.Draw(im)
    if sc == "scared" and sp == "C" and "C" in infos:
        hx, hy = infos["C"]["hand_r"]; d.rounded_rectangle([hx - 10, hy - 18, hx + 40, hy + 8], 6, fill=(200, 60, 60), outline=INK, width=3)
    if sc == "arrive" and "A" in infos:
        hx, hy = infos["A"]["hand_l"]; laddoo_plate(d, hx + 10, hy - 10)
    if sc in ("nani", "bunty", "moral", "end1") and "A" in infos:
        hx, hy = infos["A"]["hand_l"]; lantern(d, hx, hy + 50, st)
    if sc == "reveal1" and sp == "C": pop_text(d, TREE_X - 120, 120, "उल्लू!", 110, fill=(255, 220, 60), stroke=INK)
    if sc == "reveal2" and sp == "C": pop_text(d, TREE_X - 270, 600, "सफ़ेद कपड़ा!", 90, fill=(255, 220, 60), stroke=INK)
    if sc == "nani": pop_text(d, 960, 110, "नानी की धोती!", 100, fill=(255, 220, 60), stroke=INK)
    if sc == "moral" and su > 0.5: pop_text(d, 960, 110, "सच जानो, डर भगाओ!", 100, fill=(255, 255, 255), stroke=(240, 80, 110))
    if sc == "end1" and SC_START[i] < 0.1 and su > 0.3: pop_text(d, 700, 120, "दो लड्डू?", 110, fill=(255, 220, 60), stroke=INK)
    if sc == "raju" and sp == "R": pop_text(d, TREE_X - 300, 230, "भूत?!", 90, fill=(255, 80, 80), stroke="white")
    if sc == "title":
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(st / 0.6); od.rounded_rectangle([460, 70, 1460, 290], 60, fill=(255, 255, 255, int(235 * a)), outline=(60, 60, 120, int(255 * a)), width=10)
        im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
        if a > 0.5: pop_text(d, 960, 95, "बरगद वाला भूत!", 130, fill=(80, 60, 160), stroke=(255, 255, 255), sw=10)
    if sc == "scared" and SC_START[i] < 0.1: subscribe_banner(im, t)
    im = camera(im, zc[0], zc[1], zoom)
    return fade(i, t, im)

def end_card(st):
    im = end_bg(); d = ImageDraw.Draw(im)
    for ch, x, k in [(G, 260, 1), (P, 520, 2), (B, 1420, 3), (C, 1680, 4)]: draw(d, ch, x, 1060, "happy", blink=blink(st, k), arms=("down", "wave"), t=st)
    pop_text(d, 960, 70, "कहानी पसंद आई?", 100, fill=(240, 80, 110), stroke=(255, 255, 255), sw=10)
    clicked = st > 6.0; pulse = 1 + 0.05 * math.sin(st * 6); bw, bh = 560 * pulse, 140 * pulse
    d.rounded_rectangle([960 - bw / 2, 300, 960 + bw / 2, 300 + bh], 70, fill=(130, 130, 130) if clicked else (230, 30, 40))
    bell(d, 960 - bw / 2 + 90, 300 + bh / 2 - 6, 1.2, ang=math.sin(st * 14) if clicked else 0)
    d.text((960 - bw / 2 + 150, 300 + bh * 0.12), "सब्सक्राइब्ड" if clicked else "सब्सक्राइब", font=hfont(76 * pulse), fill="white")
    d.rounded_rectangle([660, 490, 940, 600], 55, fill=(40, 120, 230)); thumbs(d, 725, 532, 0.9); d.text((785, 498), "लाइक", font=hfont(56), fill="white")
    d.rounded_rectangle([980, 490, 1220, 600], 55, fill=(40, 170, 90)); d.text((1030, 498), "शेयर", font=hfont(56), fill="white")
    if 4.5 < st < 6.2:
        hx = lerp(1300, 1000, ease((st - 4.5) / 1.0)); hy = lerp(700, 380, ease((st - 4.5) / 1.0))
        d.ellipse([hx - 26, hy - 26, hx + 26, hy + 26], fill="white", outline=INK, width=5)
    tag(d, 960, 680, "हर शनिवार नया कारनामा", 50, bg=(240, 80, 110))
    return im

def fade(i, t, im):
    sc = SEG[i][0]
    fi = min(1, t / 0.3) if (i == 0 or SEG[i - 1][0] != sc) and sc in ("title", "night", "end") else 1
    fo = min(1, (DUR[i] - t) / 0.3) if (i == len(SEG) - 1 or SEG[i + 1][0] != sc) and sc in ("brag", "end") else 1
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
