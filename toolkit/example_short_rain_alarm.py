import os, sys, subprocess, wave, math, random
sys.path.insert(0, "/home/claude/utoon"); sys.path.insert(0, "/home/claude/jshort")
import draw
from draw import Kid, draw_kid, hfont, pop_text, tag, lerp, ease, mix, OUT
from PIL import Image, ImageDraw, ImageFilter
from script import SEG

W, H, FPS = 1080, 1920, 30
D = "/home/claude/jshort"
def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()
PRE, POST = 0.2, 0.35
VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
EXTRA = {"grab": 0.5, "cta": 1.2}
DUR = []
for i, (sc, sp, _) in enumerate(SEG):
    last = i == len(SEG) - 1 or SEG[i + 1][0] != sc
    DUR.append(PRE + VL[i] + POST + (EXTRA.get(sc, 0) if last else 0))
SC_START, acc = [], {}
for i, (sc, _, _) in enumerate(SEG):
    SC_START.append(acc.get(sc, 0.0)); acc[sc] = acc.get(sc, 0.0) + DUR[i]
SC_LEN = acc
FLOOR = 1620
C = Kid((150, 90, 220), hair="tuft", s=1.4)
MOM = Kid((236, 80, 120), dress=True, hair="bun", s=1.7, adult=True)
CLOTHES = [((240, 90, 90), "shirt"), ((90, 160, 230), "pant"), ((250, 200, 70), "frock"), ((120, 196, 120), "shirt"), ((200, 120, 220), "towel")]

def terrace(dark=0.0):
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    top, bot = mix((120, 200, 255), (70, 80, 100), dark), mix((210, 240, 255), (130, 140, 155), dark)
    for y in range(1200): d.line([(0, y), (W, y)], fill=mix(top, bot, y / 1200))
    # city skyline
    rnd = random.Random(3)
    x = 0
    while x < W:
        w = rnd.randint(90, 170); h = rnd.randint(150, 420)
        d.rectangle([x, 1150 - h, x + w, 1150], fill=mix((190, 200, 220), (90, 95, 110), dark))
        for wy in range(1150 - h + 20, 1140, 50):
            for wx in range(x + 15, x + w - 20, 40): d.rectangle([wx, wy, wx + 18, wy + 26], fill=mix((240, 245, 255), (120, 125, 140), dark))
        x += w + 10
    # terrace floor
    d.rectangle([0, 1150, W, H], fill=mix((220, 200, 175), (150, 135, 120), dark))
    for k in range(-4, 12):
        d.line([(540 + (k * 130 - 540) * 0.5, 1260), (540 + (k * 130 - 540) * 1.8, H)], fill=mix((200, 180, 155), (130, 118, 105), dark), width=3)
    # parapet wall
    d.rectangle([0, 1150, W, 1260], fill=mix((240, 225, 200), (160, 150, 135), dark)); d.rectangle([0, 1140, W, 1160], fill=mix((210, 190, 165), (140, 128, 115), dark))
    # water tank
    d.rounded_rectangle([800, 820, 1020, 1150], 30, fill=mix((40, 40, 45), (25, 25, 30), dark)); d.rectangle([790, 820, 1030, 850], fill=mix((60, 60, 65), (30, 30, 35), dark))
    # poles + line
    for px in (90, 760):
        d.rectangle([px - 10, 560, px + 10, 1500], fill=(120, 120, 130))
    d.line([(90, 580), (760, 600)], fill=(80, 80, 90), width=5)
    # plants
    for px in (120, 330):
        d.polygon([(px - 50, 1500), (px + 50, 1500), (px + 40, 1420), (px - 40, 1420)], fill=(200, 110, 70))
        for a in range(-3, 4): d.line([(px, 1420), (px + a * 25, 1330 - abs(a) * 10)], fill=mix((70, 150, 80), (50, 100, 60), dark), width=12)
    return im
BG_SUN = terrace(0.0); BG_DARK = terrace(1.0)

def cloth(d, x, y, col, kind, swing):
    if kind == "shirt":
        d.polygon([(x - 50, y), (x + 50, y), (x + 75, y + 40), (x + 50, y + 55), (x + 45, y + 150), (x - 45, y + 150), (x - 50, y + 55), (x - 75, y + 40)], fill=col)
    elif kind == "pant":
        d.polygon([(x - 40, y), (x + 40, y), (x + 45, y + 170), (x + 8, y + 170), (x, y + 50), (x - 8, y + 170), (x - 45, y + 170)], fill=col)
    elif kind == "frock":
        d.polygon([(x - 30, y), (x + 30, y), (x + 70, y + 150), (x - 70, y + 150)], fill=col)
    else:
        d.rectangle([x - 45, y, x + 45, y + 140], fill=col); d.line([(x - 45, y + 110), (x + 45, y + 110)], fill="white", width=6)
    d.rectangle([x - 6, y - 14, x + 6, y + 8], fill=(240, 220, 120))

def clothes_line(d, n_left, swing):
    for k, (col, kind) in enumerate(CLOTHES):
        if k >= n_left: continue
        x = 170 + k * 130; y = 584 + k * 4
        cloth(d, x + math.sin(swing + k) * 4, y, col, kind, swing)

def rain_alarm(d, x, y, s=1.0, flashing=False, t=0.0):
    d.rounded_rectangle([x - 90 * s, y - 60 * s, x + 90 * s, y], int(10 * s), fill=(30, 120, 70), outline=(20, 70, 40), width=4)
    for k in range(5): d.line([(x - 80 * s, y - 50 * s + k * 9 * s), (x - 10 * s, y - 50 * s + k * 9 * s)], fill=(230, 190, 80), width=max(2, int(4 * s)))
    d.ellipse([x + 10 * s, y - 52 * s, x + 50 * s, y - 12 * s], fill=(30, 30, 30))
    d.rectangle([x + 58 * s, y - 52 * s, x + 82 * s, y - 10 * s], fill=(220, 60, 50))
    on = flashing and (t * 4) % 1 < 0.55
    d.ellipse([x + 60 * s, y - 80 * s, x + 80 * s, y - 60 * s], fill=(255, 60, 60) if on else (120, 40, 40))
    if on:
        for r in (40, 60):
            d.arc([x + 30 * s - r, y - 32 * s - r, x + 30 * s + r, y - 32 * s + r], -60, 60, fill=(255, 80, 80), width=5)

def raindrops(d, t, n=140):
    rnd = random.Random(5)
    for _ in range(n):
        x0 = rnd.randint(0, W); sp = rnd.uniform(1400, 2000); y = (rnd.randint(0, H) + t * sp) % H
        d.line([(x0 - y * 0.05, y), (x0 - y * 0.05 - 8, y + 40)], fill=(200, 220, 255), width=4)

def cloud(d, x, y, s, col):
    for dx, dy, r in [(0, 0, 90), (100, 20, 70), (-100, 22, 70), (50, -50, 75), (-50, -40, 65)]:
        d.ellipse([x + dx * s - r * s, y + dy * s - r * s, x + dx * s + r * s, y + dy * s + r * s], fill=col)

def blink(t, s=0): return ((t + s) % 3.3) < 0.13
def mouth(on, t): return on and math.sin(t * 22) > -0.2

def frame(i, t):
    sc, sp, _ = SEG[i]; st = SC_START[i] + t; su = st / SC_LEN[sc]
    speaking = PRE < t < PRE + VL[i]
    tc, tm = mouth(speaking and sp == "C", t), mouth(speaking and sp == "T", t)
    dark = {"sunny": 0.0, "clouds": ease(su), "beep": 1.0, "grab": 1.0, "rain": 1.0, "proud": 1.0, "cta": 0.0}[sc]
    im = Image.blend(BG_SUN, BG_DARK, dark) if 0 < dark < 1 else (BG_DARK if dark else BG_SUN).copy()
    d = ImageDraw.Draw(im)
    if sc in ("clouds", "beep", "grab", "rain", "proud"):
        k = ease(su) if sc == "clouds" else 1.0
        for j, (cx, cy) in enumerate([(200, 180), (620, 120), (980, 230), (420, 330)]):
            cloud(d, lerp(-300 if j % 2 == 0 else W + 300, cx, k), cy, 1.1, (90, 95, 110))
    nleft = 5
    if sc == "grab": nleft = 5 - int(min(5, st / 0.6))
    if sc in ("rain", "proud"): nleft = 0
    clothes_line(d, nleft, st * 2)
    rain_alarm(d, 600, 1150, 1.2, flashing=sc in ("beep", "grab"), t=st)
    if sc == "sunny":
        d.ellipse([820, 90, 990, 260], fill=(255, 225, 80))
        pop_text(d, 540, 300, "मम्मी बाज़ार गईं...", 92, fill=(255, 255, 255), stroke=(70, 40, 140))
        draw_kid(d, MOM, lerp(620, 1300, ease((st - 1.0) / 2.5)), FLOOR, "happy", blink=blink(st), walk=st * 1.3, arms=("down", "wave"))
    elif sc == "clouds":
        pop_text(d, 540, 420, "उफ़!", 160, fill=(255, 220, 60), stroke=(40, 30, 80))
    elif sc == "beep":
        if (st * 4) % 1 < 0.55: pop_text(d, 600, 860, "बीप! बीप!", 120, fill=(255, 80, 80), stroke="white")
        cx = lerp(-200, 420, ease((st - 1.2) / 1.2)) if st > 1.2 else -300
        draw_kid(d, C, cx, FLOOR, "wow", talk=tc, blink=blink(st, 1), walk=st * 1.8 if st < 2.4 else 0, arms=("down", "point") if st > 2.4 else "down", look=1)
    elif sc == "grab":
        draw_kid(d, C, 300 + (5 - nleft) * 90, FLOOR, "happy", blink=blink(st, 1), arms="up", walk=st * 2)
        # pile in hands
        hx, hy = 300 + (5 - nleft) * 90, FLOOR - 1.4 * 470
        for k in range(5 - nleft):
            d.rounded_rectangle([hx - 80, hy - 30 - k * 26, hx + 80, hy - k * 26], 10, fill=CLOTHES[k][0])
        pop_text(d, 540, 300, "फटाफट!", 130, fill=(255, 220, 60), stroke=(40, 30, 80))
    elif sc in ("rain", "proud"):
        raindrops(d, st)
        mi = draw_kid(d, MOM, 760, FLOOR, "wow" if sc == "rain" else "happy", talk=tm, blink=blink(st, 3), arms=("down", "up"), look=-1)
        hx, hy = mi["hand_r"]
        d.chord([hx - 230, hy - 200, hx + 230, hy + 60], 180, 360, fill=(240, 80, 110)); d.line([(hx, hy), (hx, hy - 70)], fill=(40, 40, 40), width=8)
        ci = draw_kid(d, C, 330, FLOOR, "happy", talk=tc, blink=blink(st, 1), arms=("down", "up") if sc == "proud" else "hold", look=1)
        if sc == "proud":
            ax, ay = ci["hand_r"]; rain_alarm(d, ax + 10, ay + 10, 1.0, flashing=False)
            if su > 0.35: tag(d, 540, 300, "रेन अलार्म STEM किट", 64, bg=(30, 120, 70))
            if su > 0.55: pop_text(d, 540, 420, "खुद बनाया!", 120, fill=(255, 220, 60), stroke=(40, 30, 80))
        else:
            for k in range(5): d.rounded_rectangle([250, FLOOR - 640 - k * 26, 410, FLOOR - 610 - k * 26], 10, fill=CLOTHES[k][0])
    elif sc == "cta":
        im = Image.new("RGB", (W, H), (250, 236, 90)); d = ImageDraw.Draw(im)
        d.ellipse([-200, -200, 400, 400], fill=(240, 80, 110)); d.ellipse([700, 1500, 1300, 2100], fill=(40, 140, 240))
        f = hfont(150); a_ = "Junior"; b_ = "Shopper"; wa, wb = d.textlength(a_, font=f), d.textlength(b_, font=f)
        x0 = (W - wa - wb) / 2
        d.text((x0, 260), a_, font=f, fill=(240, 80, 60), stroke_width=10, stroke_fill="white"); d.text((x0 + wa, 260), b_, font=f, fill=(40, 120, 230), stroke_width=10, stroke_fill="white")
        pop_text(d, 540, 520, "मज़ेदार साइंस किट", 90, fill=(70, 40, 140), stroke="white", sw=8)
        rain_alarm(d, 540, 900, 2.2)
        draw_kid(d, C, 240, 1450, "happy", blink=blink(st, 1), arms=("down", "wave"), walk=st)
        d.rounded_rectangle([140, 1520, 940, 1660], 70, fill=(240, 80, 110)); pop_text(d, 540, 1535, "juniorshopper.com", 80, fill="white", stroke=(240, 80, 110), sw=0)
        pop_text(d, 540, 1700, "फ्री डिलीवरी • पूरे भारत में", 64, fill=(30, 120, 70), stroke="white", sw=6)
    fi = min(1, t / 0.25) if i == 0 else 1
    fo = min(1, (DUR[i] - t) / 0.3) if i == len(SEG) - 1 else 1
    if min(fi, fo) < 1: im = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), im, max(0, min(fi, fo)))
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
        tiles = [frame(i, DUR[i] * 0.7).resize((270, 480)) for i in range(len(SEG))]
        sh = Image.new("RGB", (270 * len(tiles), 480))
        for k, tl in enumerate(tiles): sh.paste(tl, (k * 270, 0))
        sh.save(f"{D}/sheet.png")
    else:
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor() as ex: list(ex.map(render, range(len(SEG))))
        print(round(sum(DUR), 1))
