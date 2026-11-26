import os, sys, subprocess, wave, math, random
sys.path.insert(0, "/home/claude/utoon"); sys.path.insert(0, "/home/claude/bb2")
from draw import hfont, ease, lerp, thumbs, bell
from PIL import Image, ImageDraw, ImageFilter, ImageChops
from script import SEG

W, H, FPS = 1920, 1080, 30
D = "/home/claude/bb2"
def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
PRE, POST = 0.3, 0.6
VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
DUR = [PRE + v + POST + (1.0 if SEG[i][0] in ("title", "outro") else 0) + (2.0 if SEG[i][0] == "outro" else 0) for i, v in enumerate(VL)]

ACC = (255, 196, 60); CY = (90, 210, 255); RED = (255, 90, 90); WH = (240, 244, 250)

def space_bg(seed=1):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    for y in range(H): d.line([(0, y), (W, y)], fill=(int(lerp(8, 18, y / H)), int(lerp(12, 22, y / H)), int(lerp(32, 52, y / H))))
    rnd = random.Random(seed)
    for _ in range(320):
        x, y = rnd.randint(0, W), rnd.randint(0, H); r = rnd.choice([1, 1, 1, 2, 2, 3]); b = rnd.randint(140, 255)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(b, b, min(255, b + 20)))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([1200, -300, 2300, 600], fill=(70, 40, 140, 70)); gd.ellipse([-400, 600, 700, 1500], fill=(20, 90, 140, 60))
    g = g.filter(ImageFilter.GaussianBlur(120)); im.paste(g, (0, 0), g)
    return im
BG = space_bg()

# continents: lists of (lon, lat) polygons, very simplified
CONT = [
 [(-165, 65), (-140, 70), (-95, 72), (-60, 60), (-55, 50), (-80, 30), (-97, 18), (-85, 10), (-105, 22), (-125, 40), (-150, 58)],   # N America
 [(-80, 10), (-60, 8), (-35, -7), (-40, -22), (-55, -35), (-70, -55), (-75, -40), (-80, -5)],                                     # S America
 [(-10, 36), (10, 37), (32, 31), (43, 12), (51, 11), (40, -15), (32, -28), (18, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],      # Africa
 [(-10, 37), (-9, 44), (0, 50), (10, 55), (25, 70), (60, 70), (100, 77), (140, 72), (170, 66), (142, 50), (125, 40), (120, 23), (105, 10), (100, 20), (88, 22), (80, 8), (73, 20), (60, 25), (50, 30), (35, 36), (26, 40), (12, 44)],  # Eurasia
 [(114, -22), (130, -12), (142, -11), (153, -25), (147, -38), (135, -35), (115, -34)],                                               # Australia
 [(-180, -72), (-60, -64), (0, -70), (90, -66), (180, -72), (180, -90), (-180, -90)],                                               # Antarctica
]

def earth(size, rot=0.0, light=None, water_shift=0.0, glow=True):
    """render an earth sprite (RGBA). rot = degrees of longitude offset; light = angle of sun in degrees (None = flat light)"""
    S = size; im = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    R = S / 2 - 6
    d.ellipse([6, 6, S - 6, S - 6], fill=(30, 110, 200))
    def proj(lon, lat):
        lon = (lon + rot + 180) % 360 - 180
        lo, la = math.radians(lon), math.radians(lat)
        if math.cos(lo) * math.cos(la) < -0.02: return None
        return (S / 2 + R * math.cos(la) * math.sin(lo), S / 2 - R * math.sin(la))
    land = (90, 170, 80)
    for poly in CONT:
        dense = []
        for a, b in zip(poly, poly[1:] + poly[:1]):
            for k in range(6): dense.append((lerp(a[0], b[0], k / 6), lerp(a[1], b[1], k / 6)))
        pts = [proj(*p) for p in dense]
        vis = [p for p in pts if p]
        if len(vis) > 2: d.polygon(vis, fill=land if poly is not CONT[5] else (235, 240, 245))
    if water_shift > 0:  # oceans move to poles: show equatorial land belt, polar water caps
        band = int(R * 0.55 * water_shift)
        d.rectangle([0, S / 2 - band, S, S / 2 + band], fill=(160, 140, 90))
        cap = int(R * 0.45 * water_shift)
        d.rectangle([0, 0, S, 6 + cap], fill=(25, 95, 190)); d.rectangle([0, S - 6 - cap, S, S], fill=(25, 95, 190))
    mask = Image.new("L", (S, S), 0); ImageDraw.Draw(mask).ellipse([6, 6, S - 6, S - 6], fill=255)
    # shading
    sh = Image.new("L", (S, S), 0); sd = ImageDraw.Draw(sh)
    if light is not None:
        # night side: half disc darkened, soft edge
        ang = math.radians(light)
        cx, cy = S / 2 - math.cos(ang) * R * 1.0, S / 2
        sd.ellipse([cx - R * 1.15, cy - R * 1.3, cx + R * 1.15, cy + R * 1.3], fill=185)
        sh = sh.filter(ImageFilter.GaussianBlur(S / 25))
    else:
        sd.ellipse([S * 0.35, S * 0.3, S * 1.25, S * 1.2], fill=110); sh = sh.filter(ImageFilter.GaussianBlur(S / 8))
    dark = Image.new("RGBA", (S, S), (0, 0, 20, 255)); im = Image.composite(dark, im, ImageChops.multiply(sh, mask)) if True else im
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0)); out.paste(im, (0, 0), mask)
    if glow:
        g = Image.new("RGBA", (S + 80, S + 80), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([30, 30, S + 50, S + 50], outline=(120, 200, 255, 160), width=14); g = g.filter(ImageFilter.GaussianBlur(14))
        g.paste(out, (40, 40), out); return g
    return out

def text_c(d, y, s, sz, fill=WH, stroke=(10, 14, 30), sw=6, x=W / 2):
    f = hfont(sz); w = d.textlength(s, font=f); d.text((x - w / 2, y), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)

def big_number(d, x, y, val, unit, sz=150, col=ACC):
    f = hfont(sz); s = f"{int(val):,}"; w = d.textlength(s, font=f)
    d.text((x - w / 2, y), s, font=f, fill=col, stroke_width=6, stroke_fill=(10, 14, 30))
    text_c(d, y + sz * 1.05, unit, int(sz * 0.36), x=x)

def subtitle(im, text, t, vl):
    """burn in subtitle chunk for current time"""
    if t < PRE or t > PRE + vl + 0.2: return
    words = text.split(); f = hfont(46, 600)
    d = ImageDraw.Draw(im)
    chunks, cur = [], []
    for w in words:
        cur.append(w)
        if d.textlength(" ".join(cur), font=f) > 1300 or w.endswith(("।", "?", "!", ",")) and len(cur) > 3:
            chunks.append(" ".join(cur)); cur = []
    if cur: chunks.append(" ".join(cur))
    tot = sum(len(c) for c in chunks); p = (t - PRE) / vl * tot; acc = 0; cs = chunks[-1]
    for c in chunks:
        acc += len(c)
        if p <= acc: cs = c; break
    w = d.textlength(cs, font=f)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([W / 2 - w / 2 - 30, 960, W / 2 + w / 2 + 30, 1040], 20, fill=(0, 0, 0, 160))
    im.paste(ov, (0, 0), ov); d = ImageDraw.Draw(im)
    d.text((W / 2 - w / 2, 966), cs, font=f, fill=(255, 255, 255))

def icon_house(d, x, y, s, rot=0):
    d.rectangle([x - 30 * s, y - 40 * s, x + 30 * s, y], fill=(230, 200, 160)); d.polygon([(x - 40 * s, y - 40 * s), (x, y - 75 * s), (x + 40 * s, y - 40 * s)], fill=(200, 80, 60))
def icon_tree(d, x, y, s):
    d.rectangle([x - 6 * s, y - 40 * s, x + 6 * s, y], fill=(120, 80, 40)); d.ellipse([x - 30 * s, y - 90 * s, x + 30 * s, y - 30 * s], fill=(70, 160, 80))
def icon_car(d, x, y, s):
    d.rounded_rectangle([x - 45 * s, y - 30 * s, x + 45 * s, y - 8 * s], int(8 * s), fill=(80, 150, 230)); d.rounded_rectangle([x - 25 * s, y - 48 * s, x + 20 * s, y - 28 * s], int(6 * s), fill=(80, 150, 230))
    for wx in (-25, 25): d.ellipse([x + wx * s - 10 * s, y - 18 * s, x + wx * s + 10 * s, y + 2 * s], fill=(30, 30, 30))
def icon_person(d, x, y, s):
    d.ellipse([x - 10 * s, y - 70 * s, x + 10 * s, y - 50 * s], fill=WH); d.line([(x, y - 50 * s), (x, y - 20 * s)], fill=WH, width=int(6 * s))
    d.line([(x, y - 20 * s), (x - 12 * s, y)], fill=WH, width=int(6 * s)); d.line([(x, y - 20 * s), (x + 12 * s, y)], fill=WH, width=int(6 * s)); d.line([(x - 16 * s, y - 42 * s), (x + 16 * s, y - 42 * s)], fill=WH, width=int(6 * s))
def plane(d, x, y, s):
    d.polygon([(x - 60 * s, y), (x + 60 * s, y - 6 * s), (x + 70 * s, y), (x + 60 * s, y + 6 * s)], fill=WH)
    d.polygon([(x, y - 2 * s), (x - 20 * s, y - 45 * s), (x - 5 * s, y - 45 * s), (x + 20 * s, y)], fill=WH); d.polygon([(x - 50 * s, y), (x - 62 * s, y - 25 * s), (x - 52 * s, y - 25 * s), (x - 40 * s, y)], fill=WH)

def sun(d, x, y, r, t):
    for k in range(12):
        a = k * math.pi / 6 + t * 0.3
        d.line([(x + math.cos(a) * r * 1.2, y + math.sin(a) * r * 1.2), (x + math.cos(a) * r * 1.5, y + math.sin(a) * r * 1.5)], fill=(255, 210, 80), width=8)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 210, 80))

EARTH_CACHE = {}
def earth_c(size, rot, light=None, ws=0.0):
    key = (size, int(rot) % 360, light, round(ws, 2))
    if key not in EARTH_CACHE:
        if len(EARTH_CACHE) > 400: EARTH_CACHE.clear()
        EARTH_CACHE[key] = earth(size, rot, light, ws)
    return EARTH_CACHE[key]

def paste_c(im, spr, cx, cy): im.paste(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)), spr)

def blackhole(im, cx, cy, r, t, disk=True, tilt=0.32):
    d = ImageDraw.Draw(im)
    if disk:
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        for k in range(14):
            rr = r * (1.4 + k * 0.17); a = int(200 - k * 12)
            col = (255, int(140 + k * 6), int(40 + k * 4), max(30, a))
            gd.ellipse([cx - rr * 1.9, cy - rr * tilt * 1.9, cx + rr * 1.9, cy + rr * tilt * 1.9], outline=col, width=int(r * 0.12))
        g = g.filter(ImageFilter.GaussianBlur(r * 0.08)); im.paste(g, (0, 0), g)
        # lensed back ring over the top
        g2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g2d = ImageDraw.Draw(g2)
        g2d.ellipse([cx - r * 1.35, cy - r * 1.35, cx + r * 1.35, cy + r * 1.35], outline=(255, 200, 90, 200), width=int(r * 0.18))
        g2 = g2.filter(ImageFilter.GaussianBlur(r * 0.06)); im.paste(g2, (0, 0), g2)
        d = ImageDraw.Draw(im)
        for k in range(40):
            ang = k * 0.9 + t * (1.5 + (k % 5) * 0.3); rr = r * (1.6 + (k % 7) * 0.25)
            px, py = cx + math.cos(ang) * rr * 1.9, cy + math.sin(ang) * rr * tilt * 1.9
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 230, 160))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0))
    if disk:  # front part of disk crossing the shadow
        d.chord([cx - r * 2.6, cy - r * tilt * 1.2, cx + r * 2.6, cy + r * tilt * 1.6], 0, 180, fill=None, outline=(255, 170, 60), width=int(r * 0.14))
    return d

def astronaut(im, cx, cy, s=1.0, stretch=1.0, rot=0.0):
    w, h = int(160 * s), int(260 * s)
    spr = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(spr)
    ox, oy = w, h
    d.rounded_rectangle([ox - 45 * s, oy - 40 * s, ox + 45 * s, oy + 70 * s], int(20 * s), fill=(235, 238, 245), outline=(120, 130, 150), width=4)
    d.rectangle([ox - 30 * s, oy - 20 * s, ox + 30 * s, oy + 15 * s], fill=(200, 205, 215))
    for sx in (-1, 1):
        d.line([(ox + sx * 45 * s, oy - 20 * s), (ox + sx * 85 * s, oy + 20 * s)], fill=(235, 238, 245), width=int(26 * s))
        d.line([(ox + sx * 22 * s, oy + 65 * s), (ox + sx * 30 * s, oy + 130 * s)], fill=(235, 238, 245), width=int(28 * s))
    d.ellipse([ox - 50 * s, oy - 130 * s, ox + 50 * s, oy - 30 * s], fill=(235, 238, 245), outline=(120, 130, 150), width=4)
    d.ellipse([ox - 34 * s, oy - 110 * s, ox + 34 * s, oy - 55 * s], fill=(40, 70, 120)); d.ellipse([ox - 20 * s, oy - 102 * s, ox - 4 * s, oy - 86 * s], fill=(160, 200, 255))
    if stretch != 1.0: spr = spr.resize((max(1, int(spr.width / math.sqrt(stretch))), int(spr.height * stretch)), Image.BICUBIC)
    if rot: spr = spr.rotate(rot, expand=True, resample=Image.BICUBIC)
    im.paste(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)), spr)

def clock(d, x, y, r, ang, col=WH):
    d.ellipse([x - r, y - r, x + r, y + r], outline=col, width=6)
    d.line([(x, y), (x + math.sin(ang) * r * 0.8, y - math.cos(ang) * r * 0.8)], fill=col, width=6)
    d.line([(x, y), (x + math.sin(ang / 12) * r * 0.5, y - math.cos(ang / 12) * r * 0.5)], fill=col, width=8)

def frame(i, t):
    sc, txt = SEG[i]; dur = DUR[i]; u = t / dur
    im = BG.copy(); d = ImageDraw.Draw(im)
    if sc == "title":
        d = blackhole(im, 1380, 540, 170, t)
        text_c(d, 300, "ब्लैक होल में", 120, fill=WH, x=560)
        text_c(d, 450, "गिर जाएँ तो?", int(110 * (0.7 + 0.3 * ease(t / 0.8))), fill=ACC, x=560)
        text_c(d, 760, "BIZARRE BRAIN", 52, fill=CY, sw=3, x=560)
    elif sc == "hook":
        d = blackhole(im, 1250, 540, 150, t)
        astronaut(im, lerp(300, 800, ease(t / dur)), 520 + math.sin(t) * 20, 1.0, rot=t * 20)
        d = ImageDraw.Draw(im); text_c(d, 60, "जहाँ से रोशनी भी नहीं निकलती", 74, fill=ACC)
    elif sc == "what":
        p = ease((t - 2.0) / (dur - 4))
        r = lerp(320, 0, p)
        if r > 8:
            g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
            gd.ellipse([960 - r * 1.3, 540 - r * 1.3, 960 + r * 1.3, 540 + r * 1.3], fill=(255, 120, 60, 120)); g = g.filter(ImageFilter.GaussianBlur(40)); im.paste(g, (0, 0), g)
            d = ImageDraw.Draw(im); d.ellipse([960 - r, 540 - r, 960 + r, 540 + r], fill=(255, int(lerp(140, 230, p)), int(lerp(70, 200, p))))
        if p > 0.85: d = blackhole(im, 960, 540, 110 * ease((p - 0.85) / 0.15) + 1, t)
        text_c(d, 60, "विशाल तारा → ब्लैक होल", 76, fill=ACC)
    elif sc == "horizon":
        d = blackhole(im, 960, 540, 170, t, disk=False)
        for k in range(16):
            dash_a = k * math.pi / 8 + t * 0.2
            d.arc([960 - 260, 540 - 260, 960 + 260, 540 + 260], math.degrees(dash_a), math.degrees(dash_a) + 12, fill=CY, width=6)
        for k in range(6):
            ph = (t * 0.5 + k / 6) % 1; y0 = 260 + k * 110
            pts = [(lerp(100, 960, q * ph), y0 + (540 - y0) * (q * ph) ** 3) for q in [j / 20 for j in range(21)]]
            d.line(pts, fill=(255, 240, 150), width=4)
        text_c(d, 60, "इवेंट होराइज़न", 84, fill=CY); text_c(d, 860, "यहाँ से कुछ भी वापस नहीं आता", 58)
    elif sc == "disk":
        d = blackhole(im, 960, 560, 150, t * 2)
        text_c(d, 60, "चमकती गैस की डिस्क", 80, fill=ACC)
    elif sc == "photo":
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse([760, 340, 1160, 740], outline=(255, 150, 50, 255), width=70); g = g.filter(ImageFilter.GaussianBlur(28)); im.paste(g, (0, 0), g)
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.arc([780, 360, 1140, 720], 60, 200, fill=(255, 220, 120, 255), width=40); g = g.filter(ImageFilter.GaussianBlur(16)); im.paste(g, (0, 0), g)
        d = ImageDraw.Draw(im); text_c(d, 60, "पहली तस्वीर • 2019", 84, fill=ACC); text_c(d, 820, "M87 आकाशगंगा का ब्लैक होल (चित्रण)", 54)
    elif sc in ("fall", "spaghetti"):
        d = blackhole(im, 1420, 540, 150, t)
        if sc == "fall":
            astronaut(im, lerp(250, 850, ease(t / dur)), 540, 1.0, rot=-90)
            for k in range(4): d.line([(980 + k * 40, 540), (1040 + k * 40, 540)], fill=CY, width=6)
        else:
            st = 1.0 + 2.2 * ease((t - 1.0) / (dur - 2))
            astronaut(im, 900, 540, 0.9, stretch=st, rot=-90)
            text_c(d, 60, "स्पैगेटीफ़िकेशन 🍜".replace(" 🍜", ""), 84, fill=ACC)
            d.line([(560, 860), (1240, 860)], fill=RED, width=6); d.polygon([(1240, 840), (1280, 860), (1240, 880)], fill=RED)
            text_c(d, 890, "ज़्यादा खिंचाव", 50, fill=RED, x=1180)
    elif sc == "bigsmall":
        d = blackhole(im, 520, 560, 70, t); d = blackhole(im, 1380, 560, 220, t * 0.6)
        text_c(d, 200, "छोटा ब्लैक होल", 60, fill=RED, x=520); text_c(d, 120, "विशाल ब्लैक होल", 60, fill=(110, 230, 120), x=1380)
        text_c(d, 860, "तुरंत खिंचाव", 52, fill=RED, x=520); text_c(d, 900, "होराइज़न पर कम खिंचाव", 52, fill=(110, 230, 120), x=1380)
    elif sc == "time":
        d = blackhole(im, 1400, 540, 150, t, disk=False)
        astronaut(im, 1150, 540, 0.6, rot=-90)
        d = ImageDraw.Draw(im)
        clock(d, 1150, 330, 70, t * (6.0 * max(0.05, 1 - u)), RED)
        clock(d, 360, 330, 70, t * 6.0, CY)
        astronaut(im, 360, 600, 0.7)
        d = ImageDraw.Draw(im); text_c(d, 840, "दोस्त की घड़ी", 50, fill=CY, x=360); text_c(d, 200, "धीमा समय", 50, fill=RED, x=1150)
        text_c(d, 60, "गुरुत्वाकर्षण = धीमा समय", 80, fill=ACC)
    elif sc == "inside":
        d = blackhole(im, 960, 560, 230, t * 0.5, disk=False)
        q = 1 + 0.08 * math.sin(t * 4); text_c(d, 430, "?", int(220 * q), fill=ACC)
        if u > 0.55: text_c(d, 850, "सिंगुलैरिटी?", 80, fill=CY)
    elif sc == "nearest":
        cx, cy = 900, 540
        for k in range(900):
            a = k * 0.05; rr = 6 + a * 18
            for arm in (0, math.pi):
                x = cx + math.cos(a + arm + t * 0.05) * rr; y = cy + math.sin(a + arm + t * 0.05) * rr * 0.45
                if 0 < x < W and 0 < y < H: d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(190, 190, 255))
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(0, 0, 0), outline=(255, 180, 80), width=4)
        sx, sy = cx + 360, cy + 70; d.ellipse([sx - 12, sy - 12, sx + 12, sy + 12], fill=(255, 220, 80))
        d.line([(cx + 20, cy + 6), (sx - 16, sy - 4)], fill=CY, width=3)
        text_c(d, 80, "आकाशगंगा का केंद्र: सैजिटेरियस A*", 66, fill=ACC)
        text_c(d, cy + 110, "हम", 44, fill=(255, 220, 80), x=sx); text_c(d, 840, "≈ 26,000 प्रकाश वर्ष दूर", 64, fill=CY)
    elif sc == "sun":
        sun(d, 960, 520, 160, t)
        if u > 0.4:
            text_c(d, 80, "सूरज ब्लैक होल नहीं बनेगा", 80, fill=(110, 230, 120))
    elif sc == "outro":
        d = blackhole(im, 960, 380, 130, t)
        text_c(d, 640, "अगला सवाल क्या हो? कमेंट करें", 64, fill=WH)
        clicked = t > dur - 3.5; pulse = 1 + 0.05 * math.sin(t * 6)
        bw, bh = 560 * pulse, 130 * pulse
        d.rounded_rectangle([960 - bw / 2, 760, 960 + bw / 2, 760 + bh], 65, fill=(130, 130, 130) if clicked else (230, 30, 40))
        bell(d, 960 - bw / 2 + 85, 760 + bh / 2 - 6, 1.1, ang=math.sin(t * 14) if clicked else 0)
        d.text((960 - bw / 2 + 145, 760 + bh * 0.1), "सब्सक्राइब्ड" if clicked else "सब्सक्राइब", font=hfont(72 * pulse), fill="white")
    subtitle(im, txt, t, VL[i])
    d = ImageDraw.Draw(im); d.text((40, 30), "BIZARRE BRAIN", font=hfont(34), fill=(150, 170, 210))
    f = min(1, t / 0.3, (dur - t) / 0.3)
    if f < 1: im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, f))
    return im

def render(i):
    n = int(round(DUR[i] * FPS)); tmp = f"{D}/seg{i:02d}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frame(i, k / FPS).tobytes())
    p.stdin.close(); assert p.wait() == 0
    os.rename(tmp, f"{D}/seg{i:02d}.mp4")

if __name__ == "__main__":
    if sys.argv[1] == "preview":
        tiles = [frame(i, DUR[i] * 0.7).resize((480, 270)) for i in range(len(SEG))]
        sh = Image.new("RGB", (1920, 270 * ((len(tiles) + 3) // 4)))
        for k, tl in enumerate(tiles): sh.paste(tl, ((k % 4) * 480, (k // 4) * 270))
        sh.save(f"{D}/sheet.png")
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor() as ex: list(ex.map(render, range(len(SEG))))
        print(round(sum(DUR), 1))
