"""Indian 2D kids-cartoon style rig: skin-tone faces, black hair, big outlined eyes, school uniforms."""
import math
from PIL import Image, ImageDraw, ImageFilter

INK = (25, 20, 25)
SKIN = (246, 205, 160); SKIN_SH = (228, 180, 136)
def L(a, b, t): return a + (b - a) * t

class Char:
    def __init__(self, gender="boy", shirt=(176, 120, 205), bottom=(40, 42, 60), hair="spiky", s=1.0, skin=SKIN, ribbon=(255, 255, 255), glasses=False, wide=1.0, adult=False, hc=(22, 22, 26), tie=True):
        self.hc = hc; self.tie = tie
        self.gender, self.shirt, self.bottom, self.hair, self.s, self.skin, self.ribbon, self.glasses, self.wide, self.adult = gender, shirt, bottom, hair, s, skin, ribbon, glasses, wide, adult

def _poly(d, pts, fill, w=5):
    d.polygon(pts, fill=fill); d.line(pts + [pts[0]], fill=INK, width=w, joint="curve")

def _ell(d, box, fill, w=5): d.ellipse(box, fill=fill, outline=INK, width=w)

def draw(d, c, x, y, expr="happy", talk=0.0, blink=False, look=(0, 0), arms=("down", "down"), t=0.0, brow=0, walk=None, prop=None):
    """x,y = feet centre. talk: 0..1 mouth openness. expr: happy, sad, angry, surprised, worried, laugh, smug"""
    s = c.s; w = max(3, int(5 * s))
    walking = walk is not None
    ph = (walk or 0.0) * math.pi * 2
    bob = abs(math.sin(ph)) * 12 * s if walking else 0.0
    breath = math.sin(t * 2.3 + x * 0.01) * 3 * s
    yb = y - bob
    feet = y; hip = yb - 230 * s; neck = yb - 400 * s + breath * 0.5
    nod = abs(math.sin(t * 7)) * 5 * s if talk > 0.05 else 0.0
    head_c = (x + (math.sin(t * 3) * 3 * s if talk > 0.05 else 0), yb - 500 * s + breath + nod); HR = 118 * s
    if talk > 0.05 and tuple(arms) == ("down", "down"):
        arms = ("down", "gesture")
    # legs: thigh + shin with knee, sock and shoe; swing when walking
    for side in ((-1, 1) if not c.adult else ()):
        hp = (x + side * 32 * s, hip + 10 * s)
        if walking:
            phase = ph + (0 if side > 0 else math.pi)
            a = math.sin(phase) * 0.18
            lift = max(0.0, math.sin(phase)) * 42 * s
        else:
            a, lift = 0.0, 0.0
        Lt = (y - 22 * s) - hp[1]
        ank = (hp[0] + Lt * math.sin(a) * 0.9 + side * 4 * s, y - 22 * s - lift)
        knee = ((hp[0] + ank[0]) / 2 + side * lift * 0.35, (hp[1] + ank[1]) / 2 - lift * 0.15)
        lw_ = int(32 * s)
        d.line([hp, knee, ank], fill=INK, width=lw_ + 2 * w, joint="curve"); d.line([hp, knee, ank], fill=c.skin, width=lw_, joint="curve")
        # sock
        dx, dy = ank[0] - knee[0], ank[1] - knee[1]; ln = max(1, math.hypot(dx, dy))
        sk = (ank[0] - dx / ln * 50 * s, ank[1] - dy / ln * 50 * s)
        d.line([sk, ank], fill=INK, width=lw_ + 2 * w + 2); d.line([sk, ank], fill=(250, 250, 250), width=lw_ + 2)
        # shoe
        fx = ank[0] + 12 * s
        _ell(d, [fx - 34 * s, ank[1] - 16 * s, fx + 34 * s, ank[1] + 24 * s], (20, 20, 22), w)
    # bottom: shorts or skirt
    if c.adult:
        sw_ = math.sin(ph) * 14 * s if walking else 0
        _poly(d, [(x - 70 * s, hip - 60 * s), (x + 70 * s, hip - 60 * s), (x + 110 * s + sw_, feet - 10 * s), (x - 110 * s + sw_, feet - 10 * s)], c.bottom, w)
        for k in range(-3, 4): d.line([(x + k * 14 * s, hip - 40 * s), (x + k * 30 * s, feet - 14 * s)], fill=INK, width=max(2, w - 3))
        d.line([(x - 110 * s, feet - 40 * s), (x + 110 * s, feet - 40 * s)], fill=(250, 200, 60), width=int(14 * s))
    elif c.gender == "girl":
        _poly(d, [(x - 70 * s, hip - 50 * s), (x + 70 * s, hip - 50 * s), (x + 100 * s, hip + 40 * s), (x - 100 * s, hip + 40 * s)], c.bottom, w)
        for k in range(-2, 3): d.line([(x + k * 26 * s, hip - 40 * s), (x + k * 36 * s, hip + 36 * s)], fill=INK, width=max(2, w - 2))
    else:
        _poly(d, [(x - 72 * s, hip - 50 * s), (x + 72 * s, hip - 50 * s), (x + 76 * s, hip + 20 * s), (x + 4 * s, hip + 20 * s), (x, hip - 10 * s), (x - 4 * s, hip + 20 * s), (x - 76 * s, hip + 20 * s)], c.bottom, w)
    # belt
    if not c.adult and c.tie: d.rectangle([x - 72 * s, hip - 62 * s, x + 72 * s, hip - 44 * s], fill=(25, 25, 28), outline=INK, width=w)
    if not c.adult and c.tie: d.rectangle([x - 14 * s, hip - 64 * s, x + 14 * s, hip - 42 * s], outline=(200, 200, 210), width=max(2, w - 1))
    # torso / shirt
    wd = c.wide
    if wd > 1.05:
        _ell(d, [x - 92 * s * wd, neck - 10 * s, x + 92 * s * wd, hip - 30 * s], c.shirt, w)
    else:
        _poly(d, [(x - 62 * s, neck), (x + 62 * s, neck), (x + 76 * s, hip - 56 * s), (x - 76 * s, hip - 56 * s)], c.shirt, w)
    if c.gender == "boy":
        d.rectangle([x + 22 * s, neck + 40 * s, x + 52 * s, neck + 70 * s], outline=INK, width=max(2, w - 2))  # pocket
    # arms
    def arm(side, pose):
        sh = (x + side * 66 * s, neck + 18 * s)
        swing = (math.sin(ph + (math.pi if side > 0 else 0)) * 50 * s) if walking else math.sin(t * 2.3 + side) * 3 * s
        poses = {"down": (sh[0] + side * 24 * s + swing, sh[1] + 190 * s),
                 "gesture": (sh[0] + side * 95 * s, sh[1] + 70 * s + math.sin(t * 5) * 22 * s), "point": (sh[0] + side * 170 * s, sh[1] + 20 * s - 60 * s),
                 "up": (sh[0] + side * 60 * s, sh[1] - 170 * s), "hip": (sh[0] + side * 20 * s, sh[1] + 150 * s),
                 "wave": (sh[0] + side * 90 * s, sh[1] - 150 * s + math.sin(t * 12) * 20 * s), "chin": (x + side * 40 * s, head_c[1] + HR * 0.9),
                 "hold": (x + side * 40 * s, sh[1] + 110 * s), "shrug": (sh[0] + side * 110 * s, sh[1] - 40 * s)}
        hand = poses.get(pose, poses["down"])
        el = (L(sh[0], hand[0], 0.5) + side * 20 * s, L(sh[1], hand[1], 0.5) + (10 * s if pose not in ("up", "wave") else 0))
        # sleeve
        sl = (L(sh[0], el[0], 0.55), L(sh[1], el[1], 0.55))
        d.line([sh, sl], fill=INK, width=int(46 * s) + 2 * w); d.line([sh, sl], fill=c.shirt, width=int(46 * s))
        d.line([sl, el, hand], fill=INK, width=int(28 * s) + 2 * w, joint="curve"); d.line([sl, el, hand], fill=c.skin, width=int(28 * s), joint="curve")
        _ell(d, [hand[0] - 22 * s, hand[1] - 22 * s, hand[0] + 22 * s, hand[1] + 22 * s], c.skin, w)
        if pose == "point":
            d.line([hand, (hand[0] + side * 38 * s, hand[1] - 8 * s)], fill=INK, width=int(14 * s) + 2 * w); d.line([hand, (hand[0] + side * 38 * s, hand[1] - 8 * s)], fill=c.skin, width=int(14 * s))
        return hand
    hl = arm(-1, arms[0]); hr = arm(1, arms[1])
    # collar + tie
    if c.adult:
        _poly(d, [(x - 62 * s, neck), (x + 20 * s, neck), (x + 76 * s, hip - 56 * s), (x + 20 * s, hip - 56 * s)], c.bottom, w)  # pallu
    if not c.adult:
      _poly(d, [(x - 50 * s, neck - 6 * s), (x, neck + 34 * s), (x - 14 * s, neck + 50 * s), (x - 62 * s, neck + 16 * s)], c.shirt, w)
      _poly(d, [(x + 50 * s, neck - 6 * s), (x, neck + 34 * s), (x + 14 * s, neck + 50 * s), (x + 62 * s, neck + 16 * s)], c.shirt, w)
      if c.tie: _poly(d, [(x - 12 * s, neck + 32 * s), (x + 12 * s, neck + 32 * s), (x + 18 * s, neck + 150 * s), (x, neck + 172 * s), (x - 18 * s, neck + 150 * s)], (40, 40, 60), w)
    # neck
    d.rectangle([x - 22 * s, neck - 40 * s, x + 22 * s, neck + 6 * s], fill=c.skin, outline=INK, width=w)
    hx, hy = head_c
    # hair back (ponytail)
    if c.hair == "ponytail":
        _poly(d, [(hx - HR * 0.9, hy - HR * 0.3), (hx - HR * 1.65, hy + HR * 0.1), (hx - HR * 1.8, hy + HR * 0.9), (hx - HR * 1.4, hy + HR * 0.6), (hx - HR * 1.05, hy + HR * 0.4)], (20, 20, 24), w)
    # ears
    for side in (-1, 1):
        _ell(d, [hx + side * HR * 0.92 - 22 * s, hy - 10 * s, hx + side * HR * 0.92 + 22 * s, hy + 46 * s], c.skin, w)
    # face
    _ell(d, [hx - HR * 0.95, hy - HR, hx + HR * 0.95, hy + HR * 1.02], c.skin, w)
    # hair front
    if c.hair == "spiky":
        pts = [(hx - HR * 1.0, hy + HR * 0.05), (hx - HR * 1.08, hy - HR * 0.6), (hx - HR * 0.75, hy - HR * 1.08), (hx - HR * 0.2, hy - HR * 1.22),
               (hx + HR * 0.45, hy - HR * 1.18), (hx + HR * 1.25, hy - HR * 1.05), (hx + HR * 0.95, hy - HR * 0.75), (hx + HR * 1.05, hy - HR * 0.3),
               (hx + HR * 0.82, hy - HR * 0.42), (hx + HR * 0.45, hy - HR * 0.55), (hx + HR * 0.55, hy - HR * 0.78), (hx + HR * 0.1, hy - HR * 0.55),
               (hx - HR * 0.35, hy - HR * 0.62), (hx - HR * 0.25, hy - HR * 0.82), (hx - HR * 0.72, hy - HR * 0.45), (hx - HR * 0.82, hy - HR * 0.05)]
        _poly(d, pts, c.hc, w)
    elif c.hair == "ponytail":
        pts = [(hx - HR * 0.98, hy + HR * 0.15), (hx - HR * 1.0, hy - HR * 0.55), (hx - HR * 0.5, hy - HR * 1.05), (hx + HR * 0.3, hy - HR * 1.08),
               (hx + HR * 0.9, hy - HR * 0.75), (hx + HR * 1.0, hy - HR * 0.2), (hx + HR * 0.75, hy - HR * 0.45), (hx + HR * 0.2, hy - HR * 0.6),
               (hx - HR * 0.4, hy - HR * 0.45), (hx - HR * 0.78, hy - HR * 0.1)]
        _poly(d, pts, c.hc, w)
        _ell(d, [hx - HR * 1.1, hy - HR * 0.95, hx - HR * 0.6, hy - HR * 0.6], c.ribbon, w)
        _ell(d, [hx - HR * 0.8, hy - HR * 1.12, hx - HR * 0.35, hy - HR * 0.78], c.ribbon, w)
    elif c.hair == "bun":
        _ell(d, [hx - HR * 0.45, hy - HR * 1.45, hx + HR * 0.45, hy - HR * 0.75], c.hc, w)
        pts = [(hx - HR * 0.98, hy + HR * 0.2), (hx - HR * 0.95, hy - HR * 0.6), (hx - HR * 0.3, hy - HR * 1.05), (hx + HR * 0.3, hy - HR * 1.05), (hx + HR * 0.95, hy - HR * 0.6),
               (hx + HR * 0.98, hy + HR * 0.2), (hx + HR * 0.75, hy - HR * 0.35), (hx, hy - HR * 0.62), (hx - HR * 0.75, hy - HR * 0.35)]
        _poly(d, pts, c.hc, w)
        d.ellipse([hx - 9 * s, hy - HR * 0.42, hx + 9 * s, hy - HR * 0.24], fill=(210, 40, 60))
    elif c.hair == "neat":
        pts = [(hx - HR * 0.98, hy), (hx - HR * 0.95, hy - HR * 0.7), (hx - HR * 0.4, hy - HR * 1.1), (hx + HR * 0.5, hy - HR * 1.08), (hx + HR * 0.98, hy - HR * 0.6),
               (hx + HR * 0.96, hy - HR * 0.1), (hx + HR * 0.6, hy - HR * 0.5), (hx - HR * 0.3, hy - HR * 0.55), (hx - HR * 0.8, hy - HR * 0.2)]
        _poly(d, pts, c.hc, w)
    # eyes
    lx, ly = look
    ey = hy - HR * 0.02; ex = HR * 0.38
    for side in (-1, 1):
        cx = hx + side * ex
        ew, eh = HR * 0.27, HR * (0.34 if expr != "surprised" else 0.4)
        if blink or expr == "laugh":
            d.arc([cx - ew, ey - eh * 0.6, cx + ew, ey + eh * 0.6], 200 if expr != "laugh" else 200, 340, fill=INK, width=w + 1)
        else:
            _ell(d, [cx - ew, ey - eh, cx + ew, ey + eh], (255, 255, 255), w)
            pr = HR * (0.13 if expr != "surprised" else 0.09)
            px, py = cx + lx * ew * 0.45 + (side * -2 * s), ey + ly * eh * 0.4 + (eh * 0.2 if expr == "sad" else 0)
            d.ellipse([px - pr, py - pr * 1.2, px + pr, py + pr * 1.2], fill=INK)
            d.ellipse([px - pr * 0.25 + pr * 0.35, py - pr * 0.9, px + pr * 0.35 + pr * 0.35, py - pr * 0.3], fill="white")
            if expr == "smug": d.chord([cx - ew - 3, ey - eh - 3, cx + ew + 3, ey + eh * 0.3], 180, 360, fill=c.skin, outline=INK, width=w)
        # brows
        by = ey - eh - HR * 0.12 - brow * HR * 0.05
        a = {"angry": 0.16, "sad": -0.14, "worried": -0.15, "surprised": -0.02}.get(expr, 0.0)
        inner_x, outer_x = cx - side * ew, cx + side * ew
        d.line([(outer_x, by - a * HR * 0.3 - (HR * 0.06 if expr == "surprised" else 0)), (inner_x, by + a * HR - (HR * 0.06 if expr == "surprised" else 0))], fill=INK, width=int(w * 1.8))
        if c.glasses: d.ellipse([cx - ew * 1.35, ey - eh * 1.15, cx + ew * 1.35, ey + eh * 1.15], outline=INK, width=w)
    # nose
    d.arc([hx - 10 * s, hy + HR * 0.18, hx + 10 * s, hy + HR * 0.36], 300, 90, fill=INK, width=max(2, w - 1))
    # cheeks
    if c.gender == "girl" or expr in ("laugh", "happy"):
        for side in (-1, 1):
            blush = Image.new("RGBA", (1, 1))
            d.ellipse([hx + side * HR * 0.6 - 22 * s, hy + HR * 0.3 - 12 * s, hx + side * HR * 0.6 + 22 * s, hy + HR * 0.3 + 12 * s], fill=(245, 170, 160))
    # mouth
    my = hy + HR * 0.58; mw = HR * 0.28
    if talk > 0.05 or expr in ("surprised", "laugh"):
        o = max(talk, 0.6 if expr == "surprised" else (0.8 if expr == "laugh" else 0)) * HR * 0.24
        if expr == "laugh":
            d.chord([hx - mw * 1.2, my - o * 0.6, hx + mw * 1.2, my + o * 1.4], 0, 180, fill=(170, 30, 40), outline=INK, width=w)
        else:
            _ell(d, [hx - mw * (0.9 if expr != "surprised" else 0.5), my - o * 0.5, hx + mw * (0.9 if expr != "surprised" else 0.5), my + o], (170, 30, 40), w)
            d.chord([hx - mw * 0.5, my - o * 0.45, hx + mw * 0.5, my + o * 0.2], 180, 360, fill="white")
    elif expr in ("happy", "smug"):
        d.arc([hx - mw, my - HR * 0.2, hx + mw, my + HR * 0.12], 25, 155, fill=INK, width=w + 1)
    elif expr in ("sad", "worried"):
        d.arc([hx - mw * 0.8, my, hx + mw * 0.8, my + HR * 0.24], 205, 335, fill=INK, width=w + 1)
    elif expr == "angry":
        d.line([(hx - mw * 0.7, my + 6 * s), (hx + mw * 0.7, my + 6 * s)], fill=INK, width=w + 1)
    return {"head": head_c, "R": HR, "hand_l": hl, "hand_r": hr, "top": hy - HR * 1.2}

def bus_bg(W=1920, H=1080):
    im = Image.new("RGB", (W, H), (245, 170, 30)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(L(250, 230, y / H)), int(L(178, 150, y / H)), int(L(40, 20, y / H))))
    for wx in range(-100, W, 520):
        d.rounded_rectangle([wx, 40, wx + 440, 360], 20, fill=(40, 50, 70), outline=INK, width=6)
        d.rectangle([wx + 18, 58, wx + 422, 342], fill=(150, 205, 235))
        d.rectangle([wx + 18, 250, wx + 422, 342], fill=(110, 170, 90))
        d.line([(wx + 220, 58), (wx + 220, 342)], fill=(40, 50, 70), width=10)
    for k in range(0, W, 520):
        d.line([(k + 470, 360), (k + 470, H)], fill=(200, 130, 20), width=6)
        for ry in range(420, H, 90): d.ellipse([k + 455, ry, k + 485, ry + 20], fill=(220, 150, 40), outline=(180, 110, 20), width=3)
    d.rectangle([0, 900, W, H], fill=(70, 70, 80))
    return im
