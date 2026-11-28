import os, sys, math, random
sys.path.insert(0, "/home/claude/lib"); sys.path.insert(0, "/home/claude/js5")
from common import *
from toon import Char, draw, INK, _ell, _poly
from stick_ui import hfont, pop_text, tag, ease, lerp, mix
from PIL import Image, ImageDraw
from script import SEG

W, H, FPS = 1080, 1920, 30
D = "/home/claude/js5"
PRE, POST = 0.25, 0.3
EXTRA = {"sneak": 1.3, "cta": 1.4}
VL, DUR, SC_START, SC_LEN = timing(SEG, D, PRE, POST, EXTRA)
FL = 1650
S = 1.5
G = Char("boy", shirt=(250, 170, 60), bottom=(60, 90, 160), hair="neat", wide=1.35, s=S, tie=False)
C = Char("boy", shirt=(90, 170, 230), bottom=(50, 50, 70), hair="spiky", s=0.82 * S, skin=(214, 168, 122), glasses=True, tie=False)
M = Char("girl", shirt=(240, 120, 150), bottom=(150, 40, 110), hair="bun", s=1.2 * S, adult=True)

def room():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(1250): d.line([(0, y), (W, y)], fill=mix((255, 236, 200), (250, 214, 170), y / 1250))
    d.rectangle([0, 1250, W, H], fill=(205, 150, 105)); d.line([(0, 1250), (W, 1250)], fill=INK, width=6)
    for k in range(-6, 14): d.line([(540 + (k * 120 - 540) * 0.5, 1250), (540 + (k * 120 - 540) * 1.9, H)], fill=(185, 132, 90), width=4)
    d.rectangle([0, 1190, W, 1250], fill=(240, 220, 190), outline=INK, width=4)
    # window
    d.rectangle([90, 420, 470, 860], fill=(140, 100, 70), outline=INK, width=7); d.rectangle([115, 445, 445, 835], fill=(170, 220, 250), outline=INK, width=4)
    d.ellipse([300, 520, 420, 640], fill=(255, 230, 90)); d.line([(280, 445), (280, 835)], fill=INK, width=6)
    d.rectangle([115, 760, 445, 835], fill=(120, 190, 110))
    # sofa
    d.rounded_rectangle([600, 980, 1060, 1230], 40, fill=(90, 150, 140), outline=INK, width=6)
    d.rounded_rectangle([630, 880, 1030, 1020], 40, fill=(110, 170, 160), outline=INK, width=6)
    d.rounded_rectangle([690, 930, 820, 1010], 20, fill=(250, 200, 80), outline=INK, width=4)
    # photo frame
    d.rectangle([660, 470, 920, 680], fill=(200, 140, 80), outline=INK, width=6); d.rectangle([685, 495, 895, 655], fill=(250, 240, 220))
    for k in range(3): d.ellipse([705 + k * 60, 540, 755 + k * 60, 590], fill=(240, 190, 140), outline=INK, width=3)
    return im

def kitchen():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(1250): d.line([(0, y), (W, y)], fill=mix((214, 238, 226), (190, 222, 210), y / 1250))
    for x in range(0, W, 90):
        for y in range(700, 1100, 90): d.rectangle([x, y, x + 88, y + 88], outline=(170, 205, 195), width=3)
    d.rectangle([0, 1250, W, H], fill=(190, 175, 160)); d.line([(0, 1250), (W, 1250)], fill=INK, width=6)
    for k in range(-6, 14): d.line([(540 + (k * 120 - 540) * 0.5, 1250), (540 + (k * 120 - 540) * 1.9, H)], fill=(170, 155, 140), width=4)
    # counter
    d.rectangle([380, 1000, W, 1250], fill=(170, 110, 70), outline=INK, width=6)
    d.rectangle([360, 980, W, 1010], fill=(230, 225, 215), outline=INK, width=5)
    for x in (450, 700, 950): d.rectangle([x - 90, 1040, x + 90, 1220], fill=(190, 130, 85), outline=INK, width=4); d.ellipse([x + 55, 1120, x + 70, 1135], fill=INK)
    # shelf with jars
    d.rectangle([420, 560, 1040, 585], fill=(170, 110, 70), outline=INK, width=4)
    for k, col in enumerate([(240, 90, 60), (250, 200, 60), (120, 180, 90)]):
        x = 500 + k * 200; d.rounded_rectangle([x - 55, 440, x + 55, 560], 18, fill=(230, 240, 245), outline=INK, width=4); d.rectangle([x - 45, 480, x + 45, 555], fill=col)
    # fridge
    d.rounded_rectangle([40, 560, 330, 1250], 24, fill=(235, 240, 245), outline=INK, width=6); d.line([(40, 820), (330, 820)], fill=INK, width=5)
    d.rectangle([290, 640, 305, 760], fill=(150, 160, 170)); d.rectangle([290, 860, 305, 1000], fill=(150, 160, 170))
    return im
BG_ROOM, BG_KIT = room(), kitchen()

def laddoo_jar(d, x, y, s=1.0, n=6):
    d.rounded_rectangle([x - 80 * s, y - 150 * s, x + 80 * s, y], int(26 * s), fill=(230, 240, 248), outline=INK, width=5)
    d.rectangle([x - 60 * s, y - 180 * s, x + 60 * s, y - 150 * s], fill=(220, 60, 60), outline=INK, width=4)
    pos = [(-40, -30), (0, -30), (40, -30), (-20, -75), (20, -75), (0, -115)]
    for k in range(n):
        px, py = pos[k]; d.ellipse([x + px * s - 24 * s, y + py * s - 24 * s, x + px * s + 24 * s, y + py * s + 24 * s], fill=(250, 170, 50), outline=INK, width=3)

def laddoo(d, x, y, s=1.0):
    d.ellipse([x - 26 * s, y - 26 * s, x + 26 * s, y + 26 * s], fill=(250, 170, 50), outline=INK, width=3)
    for a in range(5): d.ellipse([x - 12 * s + a * 6 * s, y - 10 * s + (a % 2) * 12 * s, x - 8 * s + a * 6 * s, y - 6 * s + (a % 2) * 12 * s], fill=(210, 120, 30))

def car(d, x, y, s=1.0, face=1, t=0.0, moving=False, led=True, waves=False):
    """toy follow-mode car, x,y = ground centre"""
    def X(v): return x + v * s * face
    bob = math.sin(t * 30) * 2 * s if moving else 0
    yy = y - bob
    _poly(d, [(X(-120), yy - 40 * s), (X(-120), yy - 110 * s), (X(-50), yy - 120 * s), (X(-10), yy - 175 * s), (X(70), yy - 175 * s), (X(105), yy - 120 * s), (X(130), yy - 105 * s), (X(130), yy - 40 * s)], (230, 50, 60), max(3, int(5 * s)))
    _poly(d, [(X(0), yy - 125 * s), (X(18), yy - 162 * s), (X(62), yy - 162 * s), (X(88), yy - 125 * s)], (170, 220, 250), max(3, int(4 * s)))
    d.rectangle([min(X(-110), X(110)), yy - 80 * s, max(X(-110), X(110)), yy - 70 * s], fill=(255, 220, 70))
    # sensor eyes (front)
    for dy in (-92, -62):
        _ell(d, [X(118) - 14 * s, yy + dy * s - 14 * s, X(118) + 14 * s, yy + dy * s + 14 * s], (60, 60, 70), 3)
        d.ellipse([X(118) - 6 * s, yy + dy * s - 6 * s, X(118) + 6 * s, yy + dy * s + 6 * s], fill=(150, 200, 255))
    on = led and (t * 3) % 1 < 0.5
    d.ellipse([X(30) - 9 * s, yy - 196 * s, X(30) + 9 * s, yy - 178 * s], fill=(80, 255, 120) if on else (40, 120, 60), outline=INK, width=2)
    rot = (t * 14 if moving else 0)
    for wx in (-75, 80):
        cx, cy = X(wx), y - 30 * s
        _ell(d, [cx - 36 * s, cy - 36 * s, cx + 36 * s, cy + 36 * s], (40, 40, 45), 4)
        d.ellipse([cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s], fill=(200, 200, 210))
        d.line([(cx + math.cos(rot) * 14 * s, cy + math.sin(rot) * 14 * s), (cx - math.cos(rot) * 14 * s, cy - math.sin(rot) * 14 * s)], fill=INK, width=3)
    if waves:
        for k in range(3):
            a = (t * 1.6 + k / 3) % 1; r = (40 + a * 140) * s
            cx, cy = X(125), yy - 77 * s
            d.arc([cx - r, cy - r, cx + r, cy + r], -35 if face > 0 else 145, 35 if face > 0 else 215, fill=(60, 150, 255), width=max(3, int(6 * s * (1 - a) + 2)))

PREV, PHASE = {}, {}
CH = {"G": G, "C": C, "M": M}
def put(d, i, k, x, expr, arms, look, st, tk, y=FL):
    key = (i, k); wp = None
    if key in PREV and abs(x - PREV[key]) > 0.6:
        PHASE[k] = PHASE.get(k, 0.0) + abs(x - PREV[key]) / (190 * CH[k].s); wp = PHASE[k]
    PREV[key] = x
    return draw(d, CH[k], x, y, expr, talk=tk.get(k, 0), blink=blink(st, ord(k)), look=look, arms=arms, t=st, walk=wp)

def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    on = PRE < t < PRE + VL[i]
    tk = {k: mouth(on and sp == k, t) for k in "GCM"}
    if sc == "cta": return fade(i, t, cta(st))
    im = (BG_KIT if sc in ("sneak", "caught") else BG_ROOM).copy(); d = ImageDraw.Draw(im)
    if sc == "intro":
        cx = 200; gx = 850
        put(d, i, "C", cx, "happy", ("down", "point"), (0.6, 0), st, tk)
        put(d, i, "G", gx, "surprised" if st > 1.5 else "happy", ("down", "down"), (-0.6, 0.3), st, tk)
        car(d, 520, FL + 20, 1.0, face=1, t=st, waves=True)
        tag(d, 540, 200, "फॉलो-मोड कार", 72, bg=(230, 50, 60))
    elif sc == "walk":
        # golu walks left then right; car follows with lag
        def gpos(tt):
            if tt < 0.8: return 800
            if tt < 0.8 + 3.0: return lerp(800, 260, ease((tt - 0.8) / 3.0))
            if tt < 4.3: return 260
            return lerp(260, 820, ease((tt - 4.3) / 3.2))
        gx = gpos(st); cxp = gpos(max(0, st - 0.9)); face = -1 if gpos(st) < gpos(max(0, st - 0.05)) - 0.1 else 1
        carx = cxp + (310 if face < 0 else -310) if st > 0.8 else 540
        carx = lerp(540, carx, ease((st - 0.8) / 0.8)) if st < 1.6 else carx
        mv = abs(gpos(st) - gpos(max(0, st - 0.05))) > 0.3
        car(d, carx, FL + 20, 1.0, face=face, t=st, moving=mv or st < 1.6)
        put(d, i, "G", gx, "laugh" if sp == "G" and SEG[i][2].startswith("हा") else "happy", ("down", "down") if mv else ("down", "point"), (-0.6 if face < 0 else 0.6, 0.3), st, tk)
        if SEG[i][2].startswith("हा"):
            hx = 540; pop_text(d, hx, 260, "पालतू पपी!", 110, fill=(255, 220, 60), stroke=INK)
            for k in range(3):
                a = (st * 1.2 + k / 3) % 1; hy = 1200 - a * 300
                x0 = carx + (k - 1) * 70; d.polygon([(x0, hy + 20), (x0 - 22, hy - 4), (x0 - 12, hy - 18), (x0, hy - 8), (x0 + 12, hy - 18), (x0 + 22, hy - 4)], fill=(240, 80, 110))
        else:
            pop_text(d, 540, 260, "पीछे-पीछे!", 110, fill="white", stroke=(230, 50, 60))
    elif sc == "sneak":
        tt = st; gx = lerp(80, 620, ease(min(1, tt / (SC_LEN["sneak"] - 1.2))))
        mv = tt < SC_LEN["sneak"] - 1.2
        carx = gx - 300
        car(d, carx, FL + 20, 1.1, face=1, t=st, moving=mv)
        laddoo_jar(d, 830, 980, 1.0)
        put(d, i, "G", gx, "smug", ("chin", "down") if mv else ("down", "up"), (0.6, -0.3), st, tk)
        pop_text(d, 560, 230, "श्श्श...", 120, fill="white", stroke=(60, 60, 120))
        if not mv and (st * 4) % 1 < 0.6:
            pop_text(d, carx, 1250, "बीप! बीप!", 100, fill=(255, 70, 70), stroke="white")
    elif sc == "caught":
        mx = lerp(1300, 900, ease(st / 1.6))
        car(d, 150, FL + 20, 0.9, face=1, t=st, moving=False)
        first = SC_START[i] < 0.01
        gi = put(d, i, "G", 420, "surprised" if first else ("worried" if sp == "G" else "sad"), ("hold", "hold") if first else ("down", "point") if sp == "G" else ("hold", "hold"), (0.6, 0), st, tk)
        hx, hy = gi["hand_r"]; laddoo(d, (gi["hand_l"][0] + hx) / 2, hy - 10, 1.4)
        put(d, i, "M", mx, "angry" if sp == "M" and first else "smug", ("hip", "hip") if st > 1.6 else ("down", "down"), (-0.6, 0), st, tk)
        if first and st < 1.0 and (st * 4) % 1 < 0.6: pop_text(d, 160, 1250, "बीप!", 100, fill=(255, 70, 70), stroke="white")
        if first and st > 2.0: pop_text(d, 540, 230, "लड्डू चोर!", 130, fill=(255, 220, 60), stroke=INK)
        if sp == "M" and not first: tag(d, 540, 230, "सीधे होमवर्क!", 76, bg=(60, 60, 140))
    elif sc == "science":
        im = Image.new("RGB", (W, H), (24, 36, 70)); d = ImageDraw.Draw(im)
        for x in range(0, W, 60): d.line([(x, 0), (x, H)], fill=(34, 50, 92), width=2)
        for y in range(0, H, 60): d.line([(0, y), (W, y)], fill=(34, 50, 92), width=2)
        car(d, 420, 1000, 2.0, face=1, t=st, waves=True)
        # hand target
        hx = 860 + math.sin(st * 1.5) * 30; hy = 850
        _ell(d, [hx - 60, hy - 70, hx + 60, hy + 70], (246, 205, 160), 5)
        for k in range(4): d.rounded_rectangle([hx - 50 + k * 26, hy - 130, hx - 30 + k * 26, hy - 50], 10, fill=(246, 205, 160), outline=INK, width=4)
        tag(d, 660, 1130, "सेंसर", 60, bg=(40, 120, 230))
        d.line([(660, 1130), (650, 920)], fill="white", width=5)
        pop_text(d, 540, 260, "कैसे काम करती है?", 96, fill="white", stroke=(40, 120, 230))
        if su > 0.45: pop_text(d, 540, 420, "सामने की चीज़ पहचानो", 70, fill=(255, 220, 60), stroke=INK, sw=6)
        if su > 0.65: pop_text(d, 540, 520, "→ पीछे-पीछे चलो!", 70, fill=(120, 230, 140), stroke=INK, sw=6)
        put(d, i, "C", 220, "happy", ("down", "gesture"), (0.6, 0), st, tk, y=1780)
    return fade(i, t, im)

def cta(st):
    im = Image.new("RGB", (W, H), (250, 236, 90)); d = ImageDraw.Draw(im)
    d.ellipse([-200, -200, 400, 400], fill=(240, 80, 110)); d.ellipse([700, 1550, 1300, 2150], fill=(40, 140, 240))
    f = hfont(150); a_, b_ = "Junior", "Shopper"; wa, wb = d.textlength(a_, font=f), d.textlength(b_, font=f)
    x0 = (W - wa - wb) / 2
    d.text((x0, 220), a_, font=f, fill=(240, 80, 60), stroke_width=10, stroke_fill="white"); d.text((x0 + wa, 220), b_, font=f, fill=(40, 120, 230), stroke_width=10, stroke_fill="white")
    pop_text(d, 540, 470, "फॉलो-मोड कार", 100, fill=(70, 40, 140), stroke="white", sw=8)
    car(d, 680 + math.sin(st * 2) * 30, 1000, 1.8, face=1, t=st, moving=True)
    put(d, SEG.index(SEG[-1]), "C", 170, "happy", ("down", "wave"), (0.6, 0), st, {"C": mouth(PRE < st < PRE + VL[-1], st)}, y=1460)
    d.rounded_rectangle([140, 1500, 940, 1640], 70, fill=(240, 80, 110)); pop_text(d, 540, 1512, "juniorshopper.com", 80, fill="white", stroke=(240, 80, 110), sw=0)
    pop_text(d, 540, 1680, "फ्री डिलीवरी • पूरे भारत में", 66, fill=(30, 120, 70), stroke="white", sw=6)
    return im

def fade(i, t, im):
    fi = min(1, t / 0.25) if i == 0 else 1
    fo = min(1, (DUR[i] - t) / 0.3) if i == len(SEG) - 1 else 1
    if min(fi, fo) < 1: im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, min(fi, fo)))
    return im

def rend(i): return render_seg(frame, i, DUR[i], D, W, H)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        tiles = []
        for i in range(len(SEG)):
            for fr in (0.3, 0.8): tiles.append(frame(i, DUR[i] * fr).resize((270, 480)))
        sh = Image.new("RGB", (270 * 9, 480 * ((len(tiles) + 8) // 9)))
        for k, tl in enumerate(tiles): sh.paste(tl, ((k % 9) * 270, (k // 9) * 480))
        sh.save(f"{D}/sheet.png")
    else:
        for i in range(len(SEG)): rend(i)
        s = SC_START[SEG.index(next(x for x in SEG if x[0] == "sneak"))]
        si = [k for k, x in enumerate(SEG) if x[0] == "sneak"][-1]
        t_beep = sum(DUR[:si]) + DUR[si] - 1.25
        fx = [(t_beep + k * 0.25, beep(), 0.6) for k in range(5)] + [(sum(DUR[:si + 1]) + k * 0.25, beep(), 0.5) for k in range(3)]
        build_audio(SEG, D, PRE, DUR, f"{D}/mix.wav", mvol=0.08, extra_fx=fx)
        concat(D, len(SEG), f"{D}/mix.wav", f"{D}/final.mp4")
        print(round(sum(DUR), 1))
