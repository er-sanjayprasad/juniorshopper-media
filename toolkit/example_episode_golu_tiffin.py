import os, sys, subprocess, wave, math, random
sys.path.insert(0, "/home/claude/utoon"); sys.path.insert(0, "/home/claude/toon2"); sys.path.insert(0, "/home/claude/ep1")
from toon import Char, draw, INK, bus_bg, _ell, _poly
from draw import hfont, pop_text, tag, subscribe_banner, end_bg, thumbs, bell, ease, lerp
from PIL import Image, ImageDraw, ImageFilter
from script import SEG

W, H, FPS = 1920, 1080, 30
D = "/home/claude/ep1"
def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
PRE, POST = 0.2, 0.4
VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
EXTRA = {"title": 1.0, "bell": 0.6, "shock": 0.4, "reveal": 0.6, "laugh": 0.6, "end": 3.0, "end1": 0.4}
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
    f = hfont(64); d.text((200, 180), "पानी का चक्र", font=f, fill=(240, 245, 235))
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
def blink(t, k=0): return ((t + k * 0.9) % 3.6) < 0.12

def camera(im, cx, cy, z):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = max(0, min(W - w, cx - w / 2)); y0 = max(0, min(H - h, cy - h / 2))
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)

POS = {"G": 420, "P": 760, "B": 1080, "C": 1340}

def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    on = PRE < t < PRE + VL[i]
    tk = {k: mouth(on and sp == k, t) for k in "GPBCTKN"}
    kt = tk["K"]
    im = (BGBUS if sc == "flash" else (end_bg() if sc == "end" else BG1)).copy(); d = ImageDraw.Draw(im)
    zoom, zc = 1.0, (960, 540)
    ex = {k: "happy" for k in "GPBC"}; arms = {k: ("down", "down") for k in "GPBC"}; look = {k: (0, 0) for k in "GPBC"}
    pos = dict(POS); show_T = False; tex, tarms = "happy", ("down", "down")
    if sc == "title":
        for k in "GPBC": arms[k] = ("down", "wave")
        show_T = True; tarms = ("down", "wave")
    elif sc == "class":
        show_T = True; tarms = ("down", "point") if tk["T"] else ("down", "down")
        ex["G"] = "angry" if False else ("surprised" if SC_START[i] > 8 else "happy")
        if SC_START[i] < 0.1: zoom, zc = 1.0 + 0.6 * ease(st / 2.5), (pos["G"], 560)
        for k in "PBC": look[k] = (0.6, 0)
    elif sc == "dream":
        zoom, zc = 1.3, (720, 600)
        ex["G"] = "laugh" if SC_START[i] < 0.1 else ("surprised" if sp == "X" else "happy"); look["P"] = (-0.7, 0)
        if sp in ("P", "K"): ex["G"] = "worried"
        if sp == "K": ex["B"] = ex["C"] = ex["P"] = "laugh"
    elif sc == "bell":
        for k in "GPBC": arms[k] = ("up", "up"); ex[k] = "laugh"
    elif sc in ("open", "shock"):
        zoom, zc = (1.5, (pos["G"] + 80, 520))
        ex["G"] = "happy" if sc == "open" else ("surprised" if SC_START[i] < 0.1 else "angry")
        arms["G"] = ("hold", "hold")
    elif sc == "detective":
        ex["G"] = "smug"; arms["G"] = ("down", "up")
    elif sc == "bunty":
        pos["G"] = 760; pos["P"] = 260; pos["C"] = 1500; ex["G"] = "angry"; arms["G"] = ("down", "point"); look["G"] = (0.7, 0)
        ex["B"] = "smug" if sp == "B" else "surprised"; arms["B"] = ("hip", "up") if sp == "B" else ("down", "down"); look["B"] = (-0.6, 0)
        zoom, zc = 1.35, (930, 540)
    elif sc == "pinky":
        pos.update({"G": 430, "P": 840, "B": 1180, "C": 1450}); ex["G"] = "smug"; arms["G"] = ("down", "point"); look["G"] = (0.7, 0)
        ex["P"] = "angry"; arms["P"] = ("hip", "hip"); look["P"] = (-0.6, 0)
        zoom, zc = 1.35, (640, 560)
    elif sc in ("chintu", "clue"):
        pos["C"] = 760; pos["P"] = 1050; pos["B"] = 1320
        ex["C"] = "happy"; arms["C"] = ("down", "point") if sc == "chintu" else ("down", "down"); look["C"] = (-0.7, 0)
        ex["G"] = "surprised"; look["G"] = (0, 0.7) if sc == "clue" else (0.6, 0)
        if sc == "clue": ex["P"] = "smug"; arms["P"] = ("hip", "point") if sp == "P" else ("hip", "hip"); look["P"] = (-0.8, 0)
        zoom, zc = 1.4, (560, 520)
    elif sc == "think":
        ex["G"] = "worried"; arms["G"] = ("down", "chin"); zoom, zc = 1.7, (pos["G"], 470)
    elif sc == "flash":
        pass
    elif sc in ("reveal", "laugh"):
        ex["G"] = "surprised" if sc == "reveal" else "sad"; arms["G"] = ("chin", "chin") if sc == "reveal" else ("down", "down")
        if sc == "laugh":
            for k in "PBC": ex[k] = "laugh"; arms[k] = ("hip", "hip")
            show_T = True; tex = "laugh"
        if sc == "reveal": zoom, zc = 1.8, (pos["G"], 450)
    elif sc == "sad":
        ex["G"] = "sad"; arms["G"] = ("hold", "hold"); zoom, zc = 1.5, (pos["G"] + 100, 500)
    elif sc == "share":
        show_T = True; tex = "happy"; tarms = ("down", "wave") if tk["T"] else ("down", "down")
        pos.update({"G": 380, "P": 700, "C": 960, "B": 1200})
        for k in "PCB": arms[k] = ("down", "point") if (sp == k or SC_START[i] > 0 and "PCB".index(k) <= ["P", "C", "B", "T"].index(sp)) else ("down", "down"); look[k] = (-0.7, 0)
        ex["G"] = "laugh" if sp != "P" else "surprised"
    elif sc == "end1":
        for k in "GPBC": ex[k] = "laugh"
        arms["G"] = ("up", "up"); show_T = True; tex = "laugh"
    # ---- draw characters ----
    if sc == "flash":
        d.rectangle([0, 0, W, H], outline=(255, 255, 255), width=30)
        info = draw(d, G, 900, FL, "happy" if (st % 1.5) < 1.1 else "laugh", talk=tk["G"], blink=blink(st), arms=("hold", "chin"), t=st)
        paratha(d, info["hand_l"][0] + 30, info["hand_l"][1] - 10, 0.5, bite=True)
        if su > 0.3: pop_text(d, 960, 80, "सुबह 7 बजे", 80, fill=(255, 220, 60), stroke=INK)
        crumbs(d, 900, FL - 300, 1.2)
        # sepia tint
        im = Image.blend(im, Image.new("RGB", (W, H), (230, 200, 150)), 0.25)
        im = camera(im, 900, 520, 1.25)
        return fade(i, t, im)
    if sc == "end":
        ks = [(G, 260, "G"), (P, 520, "P"), (B, 1420, "B"), (C, 1680, "C")]
        for ch, x, k in ks: draw(d, ch, x, 1060, "happy", blink=blink(st, ord(k)), arms=("down", "wave"), t=st)
        pop_text(d, 960, 70, "गोलू की कहानी पसंद आई?", 96, fill=(240, 80, 110), stroke=(255, 255, 255), sw=10)
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
        return fade(i, t, im)
    order = sorted("GPBC", key=lambda k: pos[k])
    infos = {}
    for k in order:
        ch = {"G": G, "P": P, "B": B, "C": C}[k]
        bob = abs(math.sin(st * 9 + ord(k))) * 14 if ex[k] == "laugh" else 0
        infos[k] = draw(d, ch, pos[k], FL - bob, ex[k], talk=max(tk[k], kt * 0.8 if sp == "K" and k != "G" else 0), blink=blink(st, ord(k)), look=look[k], arms=arms[k], t=st)
    if show_T:
        draw(d, T, 1650, FL, tex, talk=tk["T"], blink=blink(st, 7), arms=tarms, look=(-0.6, 0), t=st)
    gi = infos["G"]
    # ---- props & effects ----
    if sc == "title":
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(st / 0.6); od.rounded_rectangle([360, 70, 1560, 290], 60, fill=(255, 255, 255, int(235 * a)), outline=(255, 200, 60, int(255 * a)), width=10)
        im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
        if a > 0.5: pop_text(d, 960, 95, "गोलू का टिफ़िन गायब!", 120 * (1 + 0.06 * math.sin(min(1, st) * math.pi)), fill=(240, 90, 60), stroke=(255, 255, 255), sw=10)
    if sc == "class" and SC_START[i] < 0.1 and st > 2.5:
        tag(d, pos["G"], gi["top"] - 90, "गोलू", 60, bg=(240, 80, 110))
    if sc == "dream":
        think_bubble(d, 640, 210, 560, 300, (gi["head"][0] + 120, gi["head"][1] - 120))
        paratha(d, 860, 360, 0.9); paratha(d, 1010, 375, 0.8)
        for k in range(3):
            a = (st * 0.6 + k / 3) % 1; d.line([(820 + k * 80, 260 - a * 40), (830 + k * 80, 232 - a * 40)], fill=(200, 200, 200), width=6)
        if sp == "X" and on: pop_text(d, gi["head"][0], gi["head"][1] + 230, "गुड़ गुड़!", 80, fill=(255, 220, 60), stroke=INK)
    if sc == "bell":
        bx, by = 1200 + math.sin(st * 30) * 8, 120
        d.ellipse([bx - 70, by - 70, bx + 70, by + 70], fill=(250, 200, 60), outline=INK, width=7)
        pop_text(d, 960, 260, "ट्रिन ट्रिन!", 110, fill=(255, 220, 60), stroke=INK)
    if sc in ("open", "shock"):
        hx = (gi["hand_l"][0] + gi["hand_r"][0]) / 2; hy = gi["hand_l"][1] - 10
        opened = sc == "shock" or su > 0.75
        tiffin(d, hx, hy, 0.9, open_=opened, empty=True)
        if sc == "shock" and SC_START[i] < 0.1:
            pop_text(d, gi["head"][0], gi["top"] - 150, "खाली!!", 120, fill=(255, 80, 80), stroke="white")
            for k in range(8):
                ang = k * math.pi / 4; r1, r2 = 160, 230
                d.line([(gi["head"][0] + math.cos(ang) * r1, gi["head"][1] + math.sin(ang) * r1), (gi["head"][0] + math.cos(ang) * r2, gi["head"][1] + math.sin(ang) * r2)], fill=(255, 200, 40), width=10)
    if sc in ("detective", "bunty", "pinky"):
        magnifier(d, gi["hand_r"][0] + 10, gi["hand_r"][1] - 50, 1.0)
        # detective cap
        hx, hy = gi["head"]; R_ = gi["R"]
        d.chord([hx - R_ * 1.05, hy - R_ * 1.35, hx + R_ * 1.05, hy - R_ * 0.35], 180, 360, fill=(150, 110, 70), outline=INK, width=5)
        d.rectangle([hx - R_ * 1.15, hy - R_ * 0.88, hx + R_ * 1.15, hy - R_ * 0.78], fill=(120, 85, 50), outline=INK, width=4)
        if sc == "detective" and su > 0.3: tag(d, gi["head"][0], gi["top"] - 140, "जासूस गोलू", 64, bg=(40, 40, 60))
    if sc == "bunty" and sp == "B":
        bi = infos["B"]; bx, by = bi["hand_r"]
        _ell(d, [bx - 50, by - 60, bx + 50, by - 25], (220, 150, 70), 4); d.rectangle([bx - 50, by - 30, bx + 50, by - 18], fill=(90, 160, 60), outline=INK, width=3)
        d.rectangle([bx - 50, by - 18, bx + 50, by - 4], fill=(130, 70, 40), outline=INK, width=3); _ell(d, [bx - 50, by - 8, bx + 50, by + 14], (220, 150, 70), 4)
    if sc in ("chintu", "clue"):
        crumbs(d, gi["head"][0] + 30, gi["head"][1] + 260, 1.0)
        if sc == "clue" and sp == "P":
            hx, hy = gi["head"]; d.ellipse([hx + 30, hy + 60, hx + 70, hy + 85], fill=(255, 235, 120), outline=INK, width=3)
            pop_text(d, hx + 200, hy - 40, "मक्खन!", 70, fill=(255, 220, 60), stroke=INK)
        if sc == "clue" and sp == "G":
            d.ellipse([gi["head"][0] - 10, gi["head"][1] + 230, gi["head"][0] + 120, gi["head"][1] + 330], outline=(255, 60, 60), width=8)
    if sc == "think":
        for k in range(3):
            a = (st * 0.8 + k / 3) % 1
            pop_text(d, gi["head"][0] + 180 + k * 40, gi["head"][1] - 160 - a * 60, "?", 70, fill=(255, 220, 60), stroke=INK)
    if sc == "reveal" and SC_START[i] < 0.1:
        pop_text(d, gi["head"][0], gi["top"] - 140, "ओह नो!", 120, fill=(255, 80, 80), stroke="white")
    if sc == "laugh":
        for k, (x, y) in enumerate([(780, 260), (1100, 300), (1400, 240)]):
            if t > 0.2 + k * 0.3: pop_text(d, x, y - 10 * math.sin(t * 8 + k), "हा हा!", 80, fill=(255, 220, 60), stroke=INK)
    if sc == "sad":
        tiffin(d, (gi["hand_l"][0] + gi["hand_r"][0]) / 2, gi["hand_l"][1] - 10, 0.9, open_=True)
        for k in range(4):
            a = (st * 1.2 + k / 4) % 1; d.ellipse([gi["head"][0] - 300 + k * 30, gi["head"][1] + 150 - a * 40, gi["head"][0] - 280 + k * 30, gi["head"][1] + 170 - a * 40], fill=(120, 120, 120))
    if sc == "share":
        n = ["P", "C", "B", "T"].index(sp) + (1 if t > PRE + 0.5 else 0)
        hx, hy = gi["hand_r"]
        items = [(lambda x, y: _ell(d, [x - 50, y - 30, x + 50, y + 20], (110, 190, 90), 4)),
                 (lambda x, y: _poly(d, [(x - 50, y + 20), (x + 50, y + 20), (x, y - 50)], (250, 220, 150), 4)),
                 (lambda x, y: (_ell(d, [x - 45, y - 45, x + 45, y - 10], (220, 150, 70), 4), d.rectangle([x - 45, y - 18, x + 45, y - 2], fill=(130, 70, 40), outline=INK, width=3)))]
        for k in range(min(3, n)): items[k](hx + 10, hy - 30 - k * 60)
        if sp == "T" and t > PRE + 1: pop_text(d, 960, 120, "दोस्ती = बाँटना", 100, fill=(255, 255, 255), stroke=(240, 80, 110))
    if sc == "end1":
        if SC_START[i] < 0.1 and su > 0.4: pop_text(d, gi["head"][0] + 150, 120, "कल से 2 टिफ़िन!", 100, fill=(255, 220, 60), stroke=INK)
    if sc == "detective" and SC_START[i] < 0.1: subscribe_banner(im, t)
    im = camera(im, zc[0], zc[1], zoom)
    return fade(i, t, im)

def fade(i, t, im):
    sc = SEG[i][0]
    fi = min(1, t / 0.3) if (i == 0 or SEG[i - 1][0] != sc) and sc in ("title", "flash", "reveal", "end") else 1
    fo = min(1, (DUR[i] - t) / 0.3) if (i == len(SEG) - 1 or SEG[i + 1][0] != sc) and sc in ("think", "flash", "end") else 1
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
