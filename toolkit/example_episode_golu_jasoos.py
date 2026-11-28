import os, sys, math, random
sys.path.insert(0, "/home/claude/lib"); sys.path.insert(0, "/home/claude/ep4")
from common import *
from toon import Char, draw, INK, _ell, _poly
from stick_ui import hfont, pop_text, tag, subscribe_banner, end_bg, thumbs, bell, ease, lerp, mix
from PIL import Image, ImageDraw
from script import SEG

W, H, FPS = 1920, 1080, 30
D = "/home/claude/ep4"
PRE, POST = 0.2, 0.4
EXTRA = {"title": 1.0, "leave": 2.2, "gone": 0.4, "coin": 0.4, "crow": 0.6, "pole": 0.8, "end": 3.0, "end1": 0.4, "trap": 0.6}
VL, DUR, SC_START, SC_LEN = timing(SEG, D, PRE, POST, EXTRA)
FL = 1040
G = Char("boy", hair="neat", wide=1.35, s=1.0)
P = Char("girl", hair="ponytail", s=0.96)
B = Char("boy", hair="spiky", s=1.04, skin=(236, 192, 150))
C = Char("boy", hair="spiky", s=0.82, skin=(214, 168, 122), glasses=True)
T = Char("girl", shirt=(240, 150, 60), bottom=(200, 60, 90), hair="bun", s=1.22, adult=True, glasses=True)
CH = {"G": G, "P": P, "B": B, "C": C, "T": T}
SILL = (1440, 520); DESK_TOP = 740; MEDAL_DESK = (1470, 728)

def first_of(sc): return next(k for k, x in enumerate(SEG) if x[0] == sc)
def segs_of(sc): return [k for k, x in enumerate(SEG) if x[0] == sc]

# ---------------- backgrounds ----------------
def classroom():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(lerp(250, 236, y / H)), int(lerp(232, 214, y / H)), int(lerp(196, 176, y / H))))
    d.rectangle([0, 760, W, H], fill=(196, 150, 100)); d.line([(0, 760), (W, 760)], fill=INK, width=6)
    for k in range(-8, 30): d.line([(960 + (k * 140 - 960) * 0.5, 760), (960 + (k * 140 - 960) * 1.7, H)], fill=(176, 130, 84), width=4)
    d.rectangle([0, 700, W, 760], fill=(150, 196, 170), outline=INK, width=5)
    # blackboard
    d.rounded_rectangle([110, 110, 880, 540], 14, fill=(150, 100, 60), outline=INK, width=7)
    d.rectangle([140, 140, 850, 510], fill=(40, 90, 70), outline=INK, width=5)
    f = hfont(60); d.text((190, 170), "आज का विषय: पक्षी", font=f, fill=(240, 245, 235))
    d.text((190, 270), "कौआ • तोता • मैना", font=hfont(50), fill=(240, 245, 235))
    # chalk bird
    d.arc([300, 380, 380, 440], 200, 340, fill=(240, 245, 235), width=5); d.arc([370, 380, 450, 440], 200, 340, fill=(240, 245, 235), width=5)
    # window (open shutters) above desk
    d.rectangle([1220, 120, 1660, 530], fill=(120, 80, 50), outline=INK, width=7)
    d.rectangle([1244, 144, 1636, 506], fill=(170, 222, 248), outline=INK, width=5)
    d.rectangle([1244, 400, 1636, 506], fill=(120, 185, 100))
    d.ellipse([1270, 220, 1420, 370], fill=(80, 150, 70), outline=INK, width=5); d.rectangle([1335, 360, 1355, 470], fill=(110, 80, 50))
    d.ellipse([1500, 170, 1580, 250], fill=(255, 230, 90))
    _poly(d, [(1220, 125), (1120, 165), (1120, 490), (1220, 528)], (150, 105, 70), 6)
    _poly(d, [(1660, 125), (1760, 165), (1760, 490), (1660, 528)], (150, 105, 70), 6)
    d.rectangle([1200, 512, 1680, 534], fill=(170, 120, 80), outline=INK, width=5)  # sill
    # teacher desk
    d.rectangle([1290, DESK_TOP, 1620, DESK_TOP + 24], fill=(150, 95, 55), outline=INK, width=5)
    d.rectangle([1305, DESK_TOP + 24, 1605, 940], fill=(175, 115, 70), outline=INK, width=5)
    d.line([(1455, DESK_TOP + 24), (1455, 940)], fill=INK, width=4)
    # books + flower on desk
    for k, col in enumerate([(230, 80, 80), (80, 140, 220), (240, 200, 70)]): d.rectangle([1320, DESK_TOP - 22 - k * 18, 1410, DESK_TOP - 4 - k * 18], fill=col, outline=INK, width=3)
    d.rectangle([1570, DESK_TOP - 50, 1600, DESK_TOP - 2], fill=(90, 160, 210), outline=INK, width=3)
    for a in (-0.5, 0, 0.5): d.ellipse([1585 + a * 40 - 12, DESK_TOP - 80 - 12, 1585 + a * 40 + 12, DESK_TOP - 80 + 12], fill=(240, 90, 120), outline=INK, width=2)
    # clock
    d.ellipse([960, 80, 1080, 200], fill="white", outline=INK, width=6); d.line([(1020, 140), (1020, 100)], fill=INK, width=5); d.line([(1020, 140), (1050, 150)], fill=INK, width=5)
    return im

def schoolyard():
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(760): d.line([(0, y), (W, y)], fill=mix((120, 196, 250), (200, 236, 255), y / 760))
    for cx, cy in [(300, 120), (900, 80)]:
        for dx, dy, r in [(0, 0, 50), (60, 10, 40), (-60, 12, 40)]: d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r], fill="white")
    # school building
    d.rectangle([0, 300, 640, 780], fill=(240, 200, 140), outline=INK, width=6)
    _poly(d, [(-20, 300), (660, 300), (600, 240), (20, 240)], (200, 90, 70), 6)
    for x in (60, 240, 420):
        d.rectangle([x, 380, x + 120, 500], fill=(170, 220, 245), outline=INK, width=5); d.line([(x + 60, 380), (x + 60, 500)], fill=INK, width=4)
    d.rectangle([250, 580, 390, 780], fill=(150, 95, 55), outline=INK, width=5)
    d.rounded_rectangle([140, 255, 500, 300], 10, fill=(40, 90, 160)); d.text((175, 255), "सरस्वती विद्यालय", font=hfont(34), fill="white")
    d.rectangle([0, 760, W, H], fill=(140, 190, 90)); d.line([(0, 760), (W, 760)], fill=INK, width=5)
    rnd = random.Random(4)
    for _ in range(120):
        x, y = rnd.randint(0, W), rnd.randint(780, H); d.line([(x, y), (x - 4, y - 14)], fill=(110, 160, 70), width=3)
    # neem tree
    _poly(d, [(1290, 780), (1330, 380), (1390, 380), (1440, 780)], (130, 90, 55), 6)
    _poly(d, [(1340, 470), (1180, 350), (1195, 335), (1350, 440)], (130, 90, 55), 5)   # left branch with nest
    _poly(d, [(1385, 450), (1560, 320), (1575, 338), (1395, 480)], (130, 90, 55), 5)   # right branch (crow)
    for cx, cy, r in [(1360, 230, 190), (1180, 270, 130), (1560, 260, 140), (1270, 140, 120), (1470, 130, 130), (1360, 90, 110)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 150, 70), outline=INK, width=5)
    for _ in range(90):
        x, y = rnd.randint(1060, 1680), rnd.randint(20, 380)
        d.ellipse([x - 9, y - 5, x + 9, y + 5], fill=(95, 175, 85))
    # re-draw lower branches over leaves so the nest sits visibly
    _poly(d, [(1340, 470), (1180, 350), (1195, 335), (1350, 440)], (130, 90, 55), 5)
    _poly(d, [(1385, 450), (1560, 320), (1575, 338), (1395, 480)], (130, 90, 55), 5)
    # bench
    d.rectangle([1650, 880, 1880, 905], fill=(170, 110, 60), outline=INK, width=4)
    for x in (1670, 1850): d.rectangle([x - 8, 905, x + 8, 960], fill=(150, 95, 55), outline=INK, width=3)
    return im
BG_CLASS, BG_YARD = classroom(), schoolyard()
NEST = (1215, 345)

def nest(d, x, y, items=True, t=0.0):
    _ell(d, [x - 80, y - 30, x + 80, y + 30], (150, 105, 60), 5)
    if items:
        medal(d, x - 30, y - 30, 0.6, t)
        d.rounded_rectangle([x + 5, y - 45, x + 45, y - 30], 6, fill=(240, 90, 160), outline=INK, width=3)  # hair clip
        d.line([(x + 20, y - 20), (x + 70, y - 50)], fill=(200, 205, 215), width=7); d.ellipse([x + 60, y - 62, x + 82, y - 44], fill=(200, 205, 215), outline=INK, width=2)  # spoon
        d.rounded_rectangle([x - 70, y - 40, x - 45, y - 25], 5, fill=(240, 200, 60), outline=INK, width=2)  # whistle
        if (t * 2) % 1 < 0.5:
            for sx, sy in [(x - 40, y - 70), (x + 40, y - 60)]: star(d, sx, sy, 10)
    for k in range(9):
        a = k / 9 * math.pi; d.line([(x - 80 * math.cos(a), y + 10 + 18 * math.sin(a)), (x - 80 * math.cos(a) + 25, y + 18 * math.sin(a))], fill=(110, 75, 40), width=4)

def star(d, x, y, r, col=(255, 255, 210)):
    pts = []
    for k in range(8):
        rr = r if k % 2 == 0 else r * 0.35; a = k * math.pi / 4
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.polygon(pts, fill=col)

def medal(d, x, y, s=1.0, t=0.0, ribbon=True):
    if ribbon:
        _poly(d, [(x - 30 * s, y - 70 * s), (x - 8 * s, y - 70 * s), (x + 6 * s, y - 20 * s), (x - 14 * s, y - 20 * s)], (220, 50, 60), 3)
        _poly(d, [(x + 30 * s, y - 70 * s), (x + 8 * s, y - 70 * s), (x - 6 * s, y - 20 * s), (x + 14 * s, y - 20 * s)], (40, 90, 200), 3)
    _ell(d, [x - 32 * s, y - 32 * s, x + 32 * s, y + 32 * s], (250, 200, 50), max(2, int(4 * s)))
    d.ellipse([x - 20 * s, y - 20 * s, x + 20 * s, y + 20 * s], outline=(210, 150, 30), width=max(2, int(3 * s)))
    star(d, x, y, 15 * s, (255, 245, 160))

def crow(d, x, y, s=1.0, face=-1, t=0.0, flap=False, item=None, look=0.0):
    """x,y = feet. face -1 looks left"""
    def X(v): return x + v * s * face * -1
    wing = math.sin(t * 22) if flap else 0
    _poly(d, [(X(40), y - 70 * s), (X(105), y - 55 * s), (X(110), y - 40 * s), (X(45), y - 45 * s)], (35, 35, 45), 4)  # tail
    _ell(d, [X(-50) - 0, y - 110 * s, X(60), y - 30 * s], (40, 40, 52), 5) if face < 0 else _ell(d, [X(60), y - 110 * s, X(-50), y - 30 * s], (40, 40, 52), 5)
    hx, hy = X(-55), y - 115 * s + math.sin(t * 4) * 2 * s
    _ell(d, [hx - 34 * s, hy - 34 * s, hx + 34 * s, hy + 34 * s], (40, 40, 52), 5)
    bx = X(-55 - 30)
    _poly(d, [(X(-75), hy - 12 * s), (X(-128), hy + 2 * s), (X(-75), hy + 14 * s)], (120, 120, 130), 3)
    ex = X(-65 - look * 6)
    d.ellipse([ex - 9 * s, hy - 16 * s, ex + 9 * s, hy + 2 * s], fill="white", outline=INK, width=2); d.ellipse([ex - 4 * s, hy - 10 * s, ex + 4 * s, hy - 2 * s], fill=INK)
    if flap:
        wy = y - 80 * s - wing * 70 * s
        _poly(d, [(X(-10), y - 85 * s), (X(30), y - 85 * s), (X(60), wy - 30 * s), (X(-20), wy)], (30, 30, 40), 4)
    else:
        _poly(d, [(X(-20), y - 90 * s), (X(55), y - 80 * s), (X(80), y - 52 * s), (X(10), y - 55 * s)], (30, 30, 40), 4)
    if not flap:
        for lx in (-5, 15): d.line([(X(lx), y - 34 * s), (X(lx), y)], fill=(90, 80, 70), width=max(2, int(4 * s)))
    tip = (X(-118), hy + 4 * s)
    if item == "medal": medal(d, tip[0], tip[1] + 30 * s, 0.55 * s, t)
    elif item == "foil": _ell(d, [tip[0] - 16 * s, tip[1] - 6 * s, tip[0] + 16 * s, tip[1] + 26 * s], (220, 225, 235), 3); star(d, tip[0] + 6 * s, tip[1] + 4 * s, 8 * s)
    elif item == "roti": _ell(d, [tip[0] - 26 * s, tip[1] - 4 * s, tip[0] + 26 * s, tip[1] + 40 * s], (230, 180, 100), 3)

def feather(d, x, y, s=1.0):
    d.line([(x - 50 * s, y + 10 * s), (x + 50 * s, y - 10 * s)], fill=INK, width=max(2, int(3 * s)))
    pts = [(x - 45 * s, y + 9 * s), (x - 10 * s, y - 14 * s), (x + 50 * s, y - 10 * s), (x + 10 * s, y + 14 * s)]
    d.polygon(pts, fill=(30, 30, 40))

def magnifier(d, x, y, s=1.0, ang=0.0):
    d.line([(x, y), (x + 70 * s, y - 70 * s)], fill=(120, 70, 30), width=int(18 * s))
    cx, cy = x + 110 * s, y - 110 * s
    d.ellipse([cx - 52 * s, cy - 52 * s, cx + 52 * s, cy + 52 * s], fill=(210, 240, 255), outline=INK, width=int(9 * s))
    d.arc([cx - 34 * s, cy - 34 * s, cx + 20 * s, cy + 20 * s], 190, 260, fill="white", width=int(6 * s))

def det_hat(d, info):
    hx, hy = info["head"]; R = info["R"]; top = info["top"]
    _ell(d, [hx - R * 1.15, top + R * 0.25, hx + R * 1.15, top + R * 0.62], (130, 90, 50), 5)
    d.chord([hx - R * 0.95, top - R * 0.35, hx + R * 0.95, top + R * 0.9], 180, 360, fill=(150, 105, 60), outline=INK, width=5)
    d.rectangle([hx - R * 0.93, top + R * 0.18, hx + R * 0.93, top + R * 0.32], fill=(70, 50, 30))

def coin(d, x, y, s=1.0):
    _ell(d, [x - 28 * s, y - 28 * s, x + 28 * s, y + 28 * s], (250, 200, 50), 4)
    d.text((x - 14 * s, y - 26 * s), "₹", font=hfont(36 * s), fill=(200, 140, 30))

def bat(d, hand, s=1.0):
    x, y = hand
    d.line([(x, y), (x + 20, y - 40)], fill=(90, 60, 30), width=10)
    _poly(d, [(x + 14, y - 34), (x + 34, y - 30), (x + 80, y - 190), (x + 56, y - 196)], (230, 200, 140), 4)

def think_bubble(d, x, y, w, h, tail):
    for k, r in enumerate([14, 22, 30]):
        cx = lerp(tail[0], x + w * 0.3, (k + 1) / 4); cy = lerp(tail[1], y + h, (k + 1) / 4)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill="white", outline=INK, width=5)
    d.rounded_rectangle([x, y, x + w, y + h], 90, fill="white", outline=INK, width=6)

def bulb(d, hx, hy):
    _ell(d, [hx - 40, hy - 50, hx + 40, hy + 30], (255, 235, 80), 5); d.rectangle([hx - 18, hy + 26, hx + 18, hy + 46], fill=(150, 150, 160), outline=INK, width=3)
    for k in range(8):
        a = k * math.pi / 4; d.line([(hx + math.cos(a) * 60, hy - 10 + math.sin(a) * 60), (hx + math.cos(a) * 85, hy - 10 + math.sin(a) * 85)], fill=(255, 210, 40), width=6)

def samosa(d, x, y, s=1.0):
    _poly(d, [(x - 45 * s, y + 30 * s), (x + 45 * s, y + 30 * s), (x, y - 45 * s)], (225, 160, 60), 4)
    d.line([(x - 20 * s, y + 10 * s), (x + 20 * s, y + 10 * s)], fill=(190, 120, 40), width=3)

def roti(d, x, y, s=1.0): _ell(d, [x - 40 * s, y - 30 * s, x + 40 * s, y + 30 * s], (230, 180, 100), 4)

PREV, PHASE = {}, {}
def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    on = PRE < t < PRE + VL[i]
    tk = {k: mouth(on and sp == k, t) for k in "GPBCTKNO"}
    if sc == "end": return fade(i, t, end_card(st))
    first = SC_START[i] < 0.05
    yard = sc in ("tree", "pole")
    im = (BG_YARD if yard else BG_CLASS).copy(); d = ImageDraw.Draw(im)
    zoom, zc = 1.0, (960, 540)
    who = {"G": 380, "P": 680, "B": 960, "C": 1200, "T": 1720}
    ex = {k: "happy" for k in who}; arms = {k: ("down", "down") for k in who}; look = {k: (0, 0) for k in who}
    hat = sc in ("detective", "clue", "suspect", "coin", "lesson", "think", "idea", "trap", "crow", "tree", "pole", "solved", "end1") or (sc == "detective")
    medal_state = "hidden"; crow_draw = None
    if sc == "title":
        for k in who: arms[k] = ("down", "wave")
    elif sc == "morning":
        arms["T"] = ("up", "down"); medal_state = "hand"
        if sp == "K": ex.update({k: "surprised" for k in "GPBC"})
        if sp == "G": ex["G"] = "smug"; arms["G"] = ("chin", "down")
        if sp == "T" and i == segs_of("morning")[2]: ex["T"] = "angry" if t < 1.5 else "smug"; ex["G"] = "worried"
        if sp == "P": arms["P"] = ("down", "gesture")
        if i == segs_of("morning")[-1]:
            if t > DUR[i] * 0.55: medal_state = "desk"; arms["T"] = ("down", "point")
            else: arms["T"] = ("hold", "down")
        if first: zoom, zc = 1.0 + 0.4 * ease(st / 3.0), (1500, 520)
    elif sc == "leave":
        medal_state = "desk"
        who["T"] = lerp(1720, 2250, ease(st / 3.0))
        li = segs_of("leave")
        bx = who["B"]
        if i in li[1:4]:
            ex["B"] = "laugh" if sp == "B" else "happy"; arms["B"] = ("down", "hold")
            if sp == "C": ex["C"] = "worried"; arms["C"] = ("hip", "gesture")
            if sp == "G": arms["G"] = ("down", "up") if t < 1.0 else ("down", "point"); ex["G"] = "smug"
        if i == li[4]:
            ex.update({"G": "laugh", "B": "laugh", "P": "laugh", "C": "happy"}); arms["B"] = ("down", "hold")
            # crow lands on sill near end
            if t > DUR[i] - 1.6:
                a = ease((t - (DUR[i] - 1.6)) / 1.4)
                crow_draw = dict(x=lerp(2050, SILL[0] + 60, a), y=lerp(80, SILL[1] - 6, a), flap=a < 1, face=-1)
        if i == li[5]:
            ex.update({"G": "laugh", "B": "laugh", "P": "laugh"}); arms["B"] = ("down", "hold")
            zoom, zc = 1.8, (1450, 560)
            if t < 0.9: crow_draw = dict(x=SILL[0] + 60, y=SILL[1] - 6, face=-1, look=math.sin(t * 6))
            elif t < 1.5:
                a = ease((t - 0.9) / 0.6); crow_draw = dict(x=lerp(SILL[0] + 60, MEDAL_DESK[0] + 70, a), y=lerp(SILL[1] - 6, DESK_TOP, a) - math.sin(a * math.pi) * 60, face=-1, flap=True)
            elif t < 1.9: crow_draw = dict(x=MEDAL_DESK[0] + 70, y=DESK_TOP, face=-1, item="medal" if t > 1.7 else None); medal_state = "desk" if t <= 1.7 else "hidden"
            else:
                a = ease((t - 1.9) / 1.6); medal_state = "hidden"
                crow_draw = dict(x=lerp(MEDAL_DESK[0] + 70, 2100, a), y=lerp(DESK_TOP, -60, a), face=1, flap=True, item="medal")
            if t > 1.7: medal_state = "hidden"
    elif sc == "gone":
        who["T"] = lerp(2250, 1720, ease(st / 2.0)) if first else 1720
        ex["T"] = "surprised" if i == segs_of("gone")[1] else ("sad" if sp == "P" else "worried")
        arms["T"] = ("hip", "point") if sp == "T" else ("down", "down")
        if sp == "K": ex.update({k: "surprised" for k in "GPBC"})
        if sp == "P": ex["P"] = "sad"; zoom, zc = 1.3, (900, 520)
        if i == segs_of("gone")[1]: zoom, zc = 1.6, (1550, 560)
    elif sc == "detective":
        di = segs_of("detective")
        if i == di[0]: ex["G"] = "smug"; arms["G"] = ("hip", "up"); zoom, zc = 1.0 + 0.5 * ease(t / 1.5), (420, 500)
        if sp == "B": ex["B"] = "laugh"; arms["B"] = ("hip", "point"); ex["G"] = "angry"
        if i == di[2]: ex["G"] = "smug"; arms["G"] = ("down", "gesture")
        if sp == "C": who["C"] = lerp(1200, 560, ease(t / 1.4)); who["P"] = 800; arms["C"] = ("down", "hold") if t < 1.4 else ("down", "point")
        ex["T"] = "sad"
    elif sc == "clue":
        who["G"] = lerp(380, 1150, ease(st / 2.5)) if first else 1150
        who["C"] = 1000 if not first else lerp(560, 1000, ease(st / 2.5)); who["P"] = 760; who["B"] = 520
        arms["G"] = ("down", "hold"); ex["T"] = "worried"; who["T"] = 1810
        if i == segs_of("clue")[1]: zoom, zc = 2.0, (1480, 680)
        if sp == "P": ex["P"] = "surprised"
        if i == segs_of("clue")[3]: ex["G"] = "smug"
        if sp == "C": arms["C"] = ("down", "point"); zoom, zc = 1.5, (1350, 520)
        if i == segs_of("clue")[5]: ex["G"] = "surprised"; arms["G"] = ("down", "point")
    elif sc == "suspect":
        who.update({"G": 760, "B": 1010, "C": 470, "P": 250, "T": 1720})
        ex["B"] = "worried"
        if sp == "G": arms["G"] = ("down", "point"); ex["G"] = "angry" if i == segs_of("suspect")[3] else "smug"
        if i == segs_of("suspect")[0]: zoom, zc = 1.0 + 0.8 * ease(t / 2.5), (1010, 640)
        if sp == "B": arms["B"] = ("hold", "hold"); ex["B"] = "worried"
        if sp == "K": ex.update({"C": "surprised", "P": "surprised", "T": "surprised"})
    elif sc == "coin":
        who.update({"G": 760, "B": 1010, "C": 470, "P": 250, "T": 1720})
        ci = segs_of("coin")
        if i == ci[0]: arms["B"] = ("down", "up"); ex["B"] = "angry"; ex["G"] = "surprised"
        if i == ci[1]: ex["G"] = "smug"; arms["G"] = ("down", "hold"); zoom, zc = 1.5, (880, 520)
        if i == ci[2]: ex["B"] = "angry"; arms["B"] = ("hip", "point"); ex["G"] = "laugh"; arms["G"] = ("down", "down")
        if sp == "K": ex.update({k: "laugh" for k in "GPCT"}); ex["B"] = "sad"
    elif sc == "lesson":
        who.update({"G": 760, "B": 1010, "C": 470, "P": 250, "T": 1500})
        arms["T"] = ("down", "gesture") if sp == "T" else ("down", "down")
        ex["G"] = "sad"; arms["G"] = ("hold", "hold")
        if sp == "G": arms["G"] = ("chin", "down")
        zoom, zc = 1.3, (1100, 540)
    elif sc == "think":
        who.update({"G": 760, "B": 1010, "C": 470, "P": 250, "T": 1500})
        arms["C"] = ("chin", "down"); ex["C"] = "worried"
        if sp == "P": ex["P"] = "surprised"; arms["P"] = ("down", "gesture")
        if sp == "G": ex["G"] = "surprised"; arms["G"] = ("down", "up")
    elif sc == "idea":
        who.update({"G": 760, "B": 1010, "C": 470, "P": 250, "T": 1500})
        ex["C"] = "smug"; arms["C"] = ("down", "up")
        if sp == "K": ex.update({k: "surprised" for k in "GPBT"})
        if sp == "G": ex["G"] = "smug"; arms["G"] = ("hip", "up")
    elif sc == "trap":
        who.update({"G": 300, "P": 520, "B": 730, "C": 930, "T": 2250})
        ti = segs_of("trap")
        if i == ti[0]:
            who["G"] = lerp(760, 1380, ease(st / 2.5)) if st < 4.5 else lerp(1380, 300, ease((st - 4.5) / 2.5)); arms["G"] = ("down", "up") if 2.5 < st < 4.5 else ("down", "down")
            who.update({"P": 250, "B": 1010, "C": 470}) if False else None
        if i == ti[1]: arms["G"] = ("down", "up")
        if i == ti[2]: ex["B"] = "worried"; arms["B"] = ("chin", "down")
        if i == ti[3]: ex["P"] = "angry"; arms["P"] = ("down", "point"); ex["B"] = "worried"; arms["B"] = ("chin", "chin")
    elif sc == "crow":
        who.update({"G": 300, "P": 520, "B": 730, "C": 930, "T": 2250})
        cs = segs_of("crow"); tg = SC_START[cs[1]] + DUR[cs[1]] * 0.7
        for k in "GPBC": look[k] = (0.8, -0.5)
        if st < 1.3:
            a = ease(st / 1.3); crow_draw = dict(x=lerp(2050, SILL[0] + 20, a), y=lerp(100, SILL[1] - 6, a), flap=a < 1, face=-1)
        elif st < tg: crow_draw = dict(x=SILL[0] + 20, y=SILL[1] - 6, face=-1 if int(st * 1.2) % 2 == 0 else 1, look=math.sin(st * 5), item="foil" if st > tg - 0.6 else None)
        else:
            a = ease((st - tg) / 1.6); crow_draw = dict(x=lerp(SILL[0] + 20, 2100, a), y=lerp(SILL[1] - 6, -80, a), face=1, flap=True, item="foil")
        if i in cs[:2]: zoom, zc = 1.35, (1150, 520)
        if sp == "K": ex.update({k: "laugh" for k in "GPBC"}); arms["G"] = ("up", "up")
        if sp == "C": arms["C"] = ("down", "point"); ex["C"] = "surprised"
        if sp == "T":
            who["T"] = lerp(2250, 1600, ease(t / 1.8)); arms["T"] = ("down", "point") if t > 1.8 else ("down", "down")
    elif sc == "tree":
        who.update({"G": 520, "P": 760, "B": 980, "C": 300, "T": 1750})
        tr = segs_of("tree")
        if first:
            k_ = ease(st / 3.5)
            for k, x0 in [("C", -200), ("G", -400), ("P", -600), ("B", -800)]: who[k] = lerp(x0, who[k], k_)
            who["T"] = lerp(-1000, 1750, ease(st / 4.5)) if st < 4.5 else 1750
        for k in "GPBCT": look[k] = (-0.3, -0.9)
        if sp == "P": arms["P"] = ("down", "point"); ex["P"] = "surprised"
        if i == tr[2]: zoom, zc = 2.2, (NEST[0], NEST[1] + 60); ex["G"] = "surprised"
        if sp == "B": ex["B"] = "smug"; arms["B"] = ("up", "up")
        if sp == "T": arms["T"] = ("down", "point"); ex["T"] = "angry" if t < 1.6 else "happy"; ex["B"] = "worried"; look["T"] = (-0.7, 0)
        crow_draw = dict(x=1520, y=335, face=-1, look=math.sin(st * 3))
    elif sc == "pole":
        who.update({"G": 520, "P": 760, "B": 980, "C": 300, "T": 1730})
        po = segs_of("pole")
        for k in "GPBC": look[k] = (0.3, -0.9)
        arms["T"] = ("up", "up") if i == po[0] else ("down", "down")
        crow_draw = dict(x=1520, y=335, face=-1, flap=(i == po[1]))
        if i == po[1]: crow_draw["y"] = 300 + math.sin(t * 8) * 20; ex.update({k: "surprised" for k in "GPBC"})
        if i == po[2]:
            who["G"] = lerp(520, 1150, ease(t / 1.8)); arms["G"] = ("down", "up") if t > 1.8 else ("down", "down"); ex["G"] = "happy"
            if t > DUR[i] * 0.7:
                a = ease((t - DUR[i] * 0.7) / (DUR[i] * 0.3)); crow_draw = dict(x=lerp(1520, 1290, a), y=lerp(335, 760, a) - math.sin(a * math.pi) * 60, face=-1, flap=a < 1)
        if i == po[3]:
            who["G"] = 1150; ex["G"] = "laugh"; arms["C"] = ("down", "point")
            a = ease(t / 1.5); crow_draw = dict(x=lerp(1290, 1520, a), y=lerp(760, 335, a), face=-1, flap=a < 1, item="roti")
    elif sc == "solved":
        who["T"] = 1550; medal_state = "chest"
        arms["T"] = ("down", "gesture") if sp == "T" else ("down", "down")
        if sp == "K": arms.update({k: ("down", "up") for k in "GPBC"})
        if sp == "B": ex["B"] = "laugh"; arms["B"] = ("hip", "point"); ex["G"] = "worried"
        for k in "GPBC": ex[k] = ex[k] if ex[k] != "happy" else "happy"
    elif sc == "end1":
        who.update({"T": 1690, "P": 300, "B": 560, "C": 800, "G": 1060}); medal_state = "chest"
        if sp == "G": ex["G"] = "smug"; arms["G"] = ("down", "gesture")
        if sp == "T": ex["T"] = "laugh"; who["G"] = lerp(1060, 1320, ease(t / 1.5)); arms["T"] = ("down", "hold")
        if sp == "K": who["G"] = 1320; ex.update({k: "laugh" for k in who}); arms["G"] = ("down", "up")
    if sp in who:
        for k in who:
            if k != sp and look[k] == (0, 0): look[k] = (0.6 if who[sp] > who[k] else -0.6, 0)
    # props drawn behind characters
    if not yard:
        if medal_state == "desk": medal(d, *MEDAL_DESK, 0.75, st)
        if sc in ("detective", "clue") or (sc == "leave" and i == segs_of("leave")[-1] and t > 1.5) or sc == "gone": feather(d, 1520, DESK_TOP - 12, 1.5)
        if sc == "clue" and i >= segs_of("clue")[4]:
            for k in range(4): d.ellipse([1300 + k * 40, SILL[1] - 8, 1312 + k * 40, SILL[1]], fill=(110, 90, 70))
        if sc == "trap" and (i != segs_of("trap")[0] or st > 3.0): _ell(d, [SILL[0] - 16, SILL[1] - 30, SILL[0] + 16, SILL[1] - 2], (220, 225, 235), 3); star(d, SILL[0] + 6, SILL[1] - 22, 8) if (st * 2) % 1 < 0.5 else None
        if sc == "crow" and crow_draw and crow_draw.get("item") is None: _ell(d, [SILL[0] - 16, SILL[1] - 30, SILL[0] + 16, SILL[1] - 2], (220, 225, 235), 3)
    else:
        po = segs_of("pole")
        nest(d, *NEST, items=not (sc == "pole"), t=st)
        if sc == "pole":
            fall = [(1100, -0.0), (1180, 0.4), (1250, 0.8), (1320, 1.2)]
            for k, (gx, dt) in enumerate(fall):
                if i == po[0]:
                    a = max(0, min(1, (t - 1.5 - dt) / 0.7)); x_ = lerp(NEST[0] - 40 + k * 30, gx, a); y_ = lerp(NEST[1] - 30, 990, a * a)
                else: x_, y_ = gx, 990
                if k == 0: medal(d, x_, y_, 0.6, st)
                elif k == 1: d.rounded_rectangle([x_ - 20, y_ - 8, x_ + 20, y_ + 8], 6, fill=(240, 90, 160), outline=INK, width=3)
                elif k == 2: d.line([(x_ - 30, y_ + 6), (x_ + 20, y_ - 6)], fill=(200, 205, 215), width=7); d.ellipse([x_ + 14, y_ - 16, x_ + 36, y_ + 2], fill=(200, 205, 215), outline=INK, width=2)
                else: d.rounded_rectangle([x_ - 14, y_ - 8, x_ + 14, y_ + 8], 5, fill=(240, 200, 60), outline=INK, width=2)
    # characters with walking
    infos = {}
    for k in sorted(who, key=lambda k: who[k]):
        x = who[k]; key = (i, k); wp = None
        if key in PREV and abs(x - PREV[key][0]) > 0.6 and abs(t - PREV[key][1]) < 0.1:
            PHASE[k] = PHASE.get(k, 0.0) + abs(x - PREV[key][0]) / (190 * CH[k].s); wp = PHASE[k]
        PREV[key] = (x, t)
        if x < -250 or x > 2150: continue
        lb = abs(math.sin(st * 9 + ord(k))) * 14 if ex[k] == "laugh" else 0
        kt = tk["K"] * 0.8 if sp == "K" and k != "T" else 0
        infos[k] = draw(d, CH[k], x, FL - lb, ex[k], talk=max(tk.get(k, 0), kt), blink=blink(st, ord(k)), look=look[k], arms=arms[k], t=st, walk=wp)
    gi = infos.get("G"); ti = infos.get("T")
    if gi and hat: det_hat(d, gi)
    # props in hands / effects
    if medal_state == "hand" and ti: medal(d, ti["hand_l"][0], ti["hand_l"][1] - 10, 0.9, st)
    if medal_state == "chest" and ti: medal(d, ti["head"][0] - 10, ti["head"][1] + 230, 0.7, st)
    if sc == "title":
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
        a = ease(st / 0.6); od.rounded_rectangle([330, 50, 1590, 270], 60, fill=(255, 255, 255, int(235 * a)), outline=(255, 200, 60, int(255 * a)), width=10)
        im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
        if a > 0.5: pop_text(d, 960, 75, "गोलू जासूस और गायब मेडल!", 112, fill=(40, 90, 200), stroke="white", sw=10)
    if sc == "morning" and sp == "K" and ti:
        for k in range(5):
            a = st * 2 + k * 1.3; star(d, ti["hand_l"][0] + math.cos(a) * 80, ti["hand_l"][1] - 10 + math.sin(a) * 60, 14, (255, 230, 90))
    if sc == "leave" and "B" in infos and segs_of("leave")[1] <= i: bat(d, infos["B"]["hand_r"])
    if sc == "leave" and i in segs_of("leave")[3:5] and gi:
        a = (t % 1.2) / 1.2; bx, by = lerp(gi["hand_r"][0], infos["B"]["hand_r"][0] - 20, a), lerp(gi["hand_r"][1], 900, a) - math.sin(a * math.pi) * 200
        _ell(d, [bx - 16, by - 16, bx + 16, by + 16], (220, 50, 50), 3)
    if sc == "leave" and i == segs_of("leave")[4]: pop_text(d, 600, 140, "चौका! छक्का!", 96, fill=(255, 220, 60), stroke=INK)
    if sc == "leave" and sp == "O" and on: pop_text(d, 1250, 330, "काँव! काँव!", 90, fill="white", stroke=INK)
    if sc == "gone" and i == segs_of("gone")[1]: pop_text(d, 1400, 250, "मेडल गायब!", 100, fill=(240, 60, 60), stroke="white")
    if sc == "gone" and i == segs_of("gone")[0] and ti: pop_text(d, 960, 150, "10 मिनट बाद...", 90, fill="white", stroke=(70, 40, 140))
    if sc in ("detective", "clue") and gi:
        if sc == "clue" or (sc == "detective" and i >= segs_of("detective")[3] and t > 1.4): magnifier(d, gi["hand_r"][0] - 10, gi["hand_r"][1] + 10, 0.9)
        if sc == "detective" and i == segs_of("detective")[0] and t > 0.8: tag(d, 640, 120, "गोलू जासूस 🔍".replace(" 🔍", ""), 80, bg=(130, 90, 50))
    if sc == "detective" and i == segs_of("detective")[3] and "C" in infos and t < 1.4: magnifier(d, infos["C"]["hand_r"][0] - 10, infos["C"]["hand_r"][1] + 10, 0.7)
    if sc == "clue" and i == segs_of("clue")[1]: tag(d, 1480, 470, "सुराग 1: काला पंख", 40, bg=(40, 40, 50))
    if sc == "clue" and i == segs_of("clue")[3] and gi:
        think_bubble(d, 1250, 90, 360, 230, (gi["head"][0] + 80, gi["top"] - 10))
        d.chord([1340, 130, 1520, 260], 180, 360, fill=(30, 30, 40)); d.rectangle([1320, 190, 1540, 210], fill=(30, 30, 40)); feather(d, 1500, 150, 0.8)
    if sc == "clue" and i == segs_of("clue")[5]: tag(d, 1300, 140, "सुराग 2: खुली खिड़की", 50, bg=(40, 40, 50))
    if sc == "suspect" and "B" in infos:
        bi = infos["B"]; px, py = bi["head"][0] + 50, bi["head"][1] + 300
        if (st * 3) % 1 < 0.6: star(d, px, py, 26, (255, 230, 90))
        coin(d, px, py + 6, 0.5)
        if i == segs_of("suspect")[3]: pop_text(d, 1000, 120, "चोर पकड़ा गया?!", 96, fill=(240, 60, 60), stroke="white")
    if sc == "coin":
        ci = segs_of("coin")
        if i == ci[0] and "B" in infos: coin(d, *infos["B"]["hand_r"], 1.2); tag(d, 1200, 140, "चॉकलेट का सिक्का!", 64, bg=(120, 70, 30))
        if i == ci[1] and gi:
            if t < DUR[i] * 0.6: coin(d, gi["hand_r"][0], gi["hand_r"][1], 1.0)
            else: pop_text(d, gi["head"][0] + 140, gi["top"] - 60, "गप!", 100, fill=(255, 220, 60), stroke=INK)
        if i == ci[2] and gi:
            for k in range(3): d.ellipse([gi["head"][0] - 30 + k * 30, gi["head"][1] + 80, gi["head"][0] - 20 + k * 30, gi["head"][1] + 90], fill=(120, 70, 30))
            pop_text(d, 1150, 140, "सबूत खा गया!", 96, fill=(255, 220, 60), stroke=INK)
        if sp == "K":
            for k, (x, y) in enumerate([(700, 200), (1100, 240), (1450, 190)]):
                if t > 0.2 + k * 0.3: pop_text(d, x, y - 10 * math.sin(t * 8 + k), "हा हा!", 80, fill=(255, 220, 60), stroke=INK)
    if sc == "lesson" and i == segs_of("lesson")[0]: tag(d, 1000, 120, "पहले सबूत, फिर इल्ज़ाम!", 60, bg=(30, 120, 80))
    if sc == "think" and "C" in infos:
        ci_ = infos["C"]; think_bubble(d, 980, 90, 640, 230, (ci_["head"][0] + 60, ci_["top"] - 10))
        th = segs_of("think"); n = 1 + (i >= th[3]) + (i >= th[4])
        if n >= 1: d.rounded_rectangle([1060, 170, 1160, 200], 8, fill=(240, 90, 160), outline=INK, width=4)
        if n >= 2: d.line([(1240, 220), (1340, 150)], fill=(200, 205, 215), width=10); d.ellipse([1320, 120, 1370, 165], fill=(200, 205, 215), outline=INK, width=3)
        if n >= 3: medal(d, 1500, 200, 0.9, st)
        if i == th[4]: pop_text(d, 1300, 340, "सब चमकीली!", 64, fill=(255, 220, 60), stroke=INK)
    if sc == "idea" and "C" in infos:
        ci_ = infos["C"]
        if i == segs_of("idea")[0]: bulb(d, ci_["head"][0], ci_["top"] - 80)
        if i in segs_of("idea")[1:3]:
            think_bubble(d, 900, 80, 520, 260, (ci_["head"][0] + 60, ci_["top"] - 10)); crow(d, 1160, 300, 1.3, -1, st, item="medal")
        if i == segs_of("idea")[2]: tag(d, 1160, 380, "कौए चमकती चीज़ें ले जाते हैं!", 44, bg=(40, 40, 50))
        if i == segs_of("idea")[3] and gi: pop_text(d, gi["head"][0] + 200, gi["top"] - 140, "प्लान!", 100, fill=(255, 220, 60), stroke=INK)
    if sc in ("trap", "crow"):
        # benches in front: kids hide behind them
        for x0 in (140, 620):
            d.rounded_rectangle([x0, 800, x0 + 440, 850], 10, fill=(160, 105, 60), outline=INK, width=5)
            d.rectangle([x0 + 10, 850, x0 + 430, 1080], fill=(185, 125, 75), outline=INK, width=5)
        if sc == "trap" and i == segs_of("trap")[0] and gi and st < 3.0: _ell(d, [gi["hand_r"][0] - 16, gi["hand_r"][1] - 16, gi["hand_r"][0] + 16, gi["hand_r"][1] + 16], (220, 225, 235), 3)
        if sc == "trap" and i == segs_of("trap")[1]: pop_text(d, 600, 140, "श्श्श!", 110, fill="white", stroke=INK)
        if sc == "trap" and i == segs_of("trap")[2] and "B" in infos: pop_text(d, infos["B"]["head"][0] + 150, infos["B"]["top"] - 60, "आ... आ...", 70, fill="white", stroke=INK)
        if sc == "crow" and sp == "O" and on: pop_text(d, 1350, 300, "काँव! काँव!", 90, fill="white", stroke=INK)
        if sc == "crow" and sp == "K": pop_text(d, 960, 120, "चोर पकड़ा गया!", 110, fill=(255, 220, 60), stroke=INK)
    if sc == "tree" and i == segs_of("tree")[2]: tag(d, NEST[0], NEST[1] + 70, "मिल गया!", 34, bg=(30, 120, 80))
    if sc == "tree" and sp == "T": tag(d, 960, 110, "पेड़ पर चढ़ना खतरनाक!", 64, bg=(200, 50, 60))
    if sc == "pole" and ti:
        po = segs_of("pole")
        if i == po[0]:
            hx, hy = ti["hand_r"]; d.line([(hx - 60, hy + 260), (NEST[0] + 40, NEST[1] + 10)], fill=INK, width=20); d.line([(hx - 60, hy + 260), (NEST[0] + 40, NEST[1] + 10)], fill=(170, 125, 70), width=12)
        if i == po[2] and gi and t < DUR[i] * 0.8: roti(d, gi["hand_r"][0], gi["hand_r"][1] - 20, 0.9)
        if sp == "O" and on: pop_text(d, 800, 120, "काँव! काँव! काँव!", 80, fill="white", stroke=INK)
        if i == po[3]:
            for k in range(3):
                a = (st * 1.0 + k / 3) % 1; hx_ = 1540 + (k - 1) * 50; hy_ = 260 - a * 150
                d.polygon([(hx_, hy_ + 20), (hx_ - 22, hy_ - 4), (hx_ - 12, hy_ - 18), (hx_, hy_ - 8), (hx_ + 12, hy_ - 18), (hx_ + 22, hy_ - 4)], fill=(240, 80, 110))
    if sc == "solved" and i == segs_of("solved")[1]: pop_text(d, 960, 90, "सबूत देखो • सोचो • फिर बोलो", 84, fill="white", stroke=(240, 80, 110))
    if sc == "end1":
        if sp != "G" and gi:
            hx, hy = gi["hand_r"]; samosa(d, hx, hy - 20, 0.9)
        if sp == "G" and gi: think_bubble(d, 1150, 60, 300, 200, (gi["head"][0] + 60, gi["top"] - 10)); samosa(d, 1300, 160, 1.6)
        if sp == "K":
            for k, (x, y) in enumerate([(700, 200), (1100, 240), (1450, 190)]):
                if t > 0.2 + k * 0.3: pop_text(d, x, y - 10 * math.sin(t * 8 + k), "हा हा!", 80, fill=(255, 220, 60), stroke=INK)
    if crow_draw:
        c = dict(crow_draw); x, y = c.pop("x"), c.pop("y"); crow(d, x, y, 1.0, t=st, **c)
    if sc == "detective" and i == segs_of("detective")[1]: subscribe_banner(im, t)
    im = camera(im, zc[0], zc[1], zoom, W, H)
    return fade(i, t, im)

def end_card(st):
    im = end_bg(); d = ImageDraw.Draw(im)
    for ch, x, k in [(G, 260, 1), (P, 520, 2), (B, 1420, 3), (C, 1680, 4)]:
        info = draw(d, ch, x, 1060, "happy", blink=blink(st, k), arms=("down", "wave"), t=st)
        if ch is G: det_hat(d, info)
    pop_text(d, 960, 70, "गोलू जासूस का केस पसंद आया?", 92, fill=(40, 90, 200), stroke=(255, 255, 255), sw=10)
    clicked = st > 6.0; pulse = 1 + 0.05 * math.sin(st * 6); bw, bh = 560 * pulse, 140 * pulse
    d.rounded_rectangle([960 - bw / 2, 300, 960 + bw / 2, 300 + bh], 70, fill=(130, 130, 130) if clicked else (230, 30, 40))
    bell(d, 960 - bw / 2 + 90, 300 + bh / 2 - 6, 1.2, ang=math.sin(st * 14) if clicked else 0)
    d.text((960 - bw / 2 + 150, 300 + bh * 0.12), "सब्सक्राइब्ड" if clicked else "सब्सक्राइब", font=hfont(76 * pulse), fill="white")
    d.rounded_rectangle([660, 490, 940, 600], 55, fill=(40, 120, 230)); thumbs(d, 725, 532, 0.9); d.text((785, 498), "लाइक", font=hfont(56), fill="white")
    d.rounded_rectangle([980, 490, 1220, 600], 55, fill=(40, 170, 90)); d.text((1030, 498), "शेयर", font=hfont(56), fill="white")
    if 4.5 < st < 6.2:
        hx = lerp(1300, 1000, ease((st - 4.5) / 1.0)); hy = lerp(700, 380, ease((st - 4.5) / 1.0))
        d.ellipse([hx - 26, hy - 26, hx + 26, hy + 26], fill="white", outline=INK, width=5)
    crow(d, 960, 860, 1.4, -1, st, item="medal")
    tag(d, 960, 900, "हर शनिवार गोलू का नया कारनामा", 50, bg=(240, 80, 110))
    return im

def fade(i, t, im):
    sc = SEG[i][0]
    fi = min(1, t / 0.3) if (i == 0 or SEG[i - 1][0] != sc) and sc in ("title", "gone", "tree", "solved", "end") else 1
    fo = min(1, (DUR[i] - t) / 0.3) if (i == len(SEG) - 1 or SEG[i + 1][0] != sc) and sc in ("leave", "crow", "pole", "end") else 1
    f = min(fi, fo)
    return Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, f)) if f < 1 else im

def rend(i): return render_seg(frame, i, DUR[i], D, W, H)

def thumbnail():
    im = BG_CLASS.copy(); d = ImageDraw.Draw(im)
    gi = draw(d, G, 520, 1180, "surprised", look=(0.7, -0.3), arms=("down", "hold"), t=0.4)
    det_hat(d, gi); magnifier(d, gi["hand_r"][0] - 10, gi["hand_r"][1] + 10, 1.4)
    crow(d, 1500, 830, 2.4, -1, 0.2, item="medal")
    pop_text(d, 1250, 60, "गोलू जासूस!", 170, fill=(255, 220, 60), stroke=INK, sw=14)
    tag(d, 1300, 300, "मेडल किसने चुराया?", 80, bg=(220, 40, 50))
    im.resize((1280, 720), Image.LANCZOS).save(f"{D}/thumb.jpg", quality=92)

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        idx = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else list(range(len(SEG)))
        tiles = [frame(i, DUR[i] * float(sys.argv[3]) if len(sys.argv) > 3 else DUR[i] * 0.6).resize((480, 270)) for i in idx]
        sh = Image.new("RGB", (1920, 270 * ((len(tiles) + 3) // 4)))
        for k, tl in enumerate(tiles):
            sh.paste(tl, ((k % 4) * 480, (k // 4) * 270)); ImageDraw.Draw(sh).text(((k % 4) * 480 + 6, (k // 4) * 270 + 4), str(idx[k]), fill="red")
        sh.save(f"{D}/sheet.png")
    elif sys.argv[1] == "thumb": thumbnail()
    elif sys.argv[1] == "render":
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(2) as ex: list(ex.map(rend, sorted(range(len(SEG)), key=lambda k: -DUR[k])))
        build_audio(SEG, D, PRE, DUR, f"{D}/mix.wav", mvol=0.06)
        concat(D, len(SEG), f"{D}/mix.wav", f"{D}/body.mp4")
        print(round(sum(DUR), 1))
