"""Shared helpers: timing from voice files, audio assembly, procedural music, rendering pipeline."""
import os, sys, subprocess, wave, math, random
import numpy as np
sys.path.insert(0, "/home/claude/juniorshopper-media/toolkit")
from PIL import Image, ImageDraw

SR = 44100
PITCH = {"G": 1.15, "B": 1.15, "O": 0.85}

def mp3_to_wav(src, dst, sp):
    k = PITCH.get(sp, 1.0)
    af = f"asetrate={int(SR * k)},aresample={SR},atempo={max(0.5, 1 / k * 1.06):.3f}" if k != 1.0 else "anull"
    af += ",silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ac", "1", "-ar", str(SR), dst], check=True)

def wlen(p):
    with wave.open(p) as w: return w.getnframes() / w.getframerate()

def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a

def timing(SEG, D, PRE, POST, EXTRA):
    VL = [wlen(f"{D}/vo{i:02d}.wav") for i in range(len(SEG))]
    DUR = []
    for i, (sc, sp, _) in enumerate(SEG):
        last = i == len(SEG) - 1 or SEG[i + 1][0] != sc
        DUR.append(PRE + VL[i] + POST + (EXTRA.get(sc, 0) if last else 0))
    SC_START, acc = [], {}
    for i, (sc, _, _) in enumerate(SEG):
        SC_START.append(acc.get(sc, 0.0)); acc[sc] = acc.get(sc, 0.0) + DUR[i]
    return VL, DUR, SC_START, acc

def pluck(freq, dur, rnd):
    n = int(SR * dur); p = max(2, int(SR / freq))
    buf = rnd.uniform(-1, 1, p).astype(np.float32); out = np.zeros(n, np.float32)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out

def music(total, bpm=104, prog=None, seed=1, mood="happy"):
    """light ukulele-style arpeggio bed, looped from a 4-bar pattern"""
    rnd = np.random.default_rng(seed)
    beat = 60 / bpm
    if prog is None:
        prog = [(261.6, 329.6, 392.0), (196.0, 246.9, 293.7), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6)] if mood == "happy" else \
               [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7), (164.8, 207.7, 246.9)]
    bar = 4 * beat; L = int(SR * bar * len(prog)); pat = np.zeros(L + SR * 2, np.float32)
    cache = {}
    for b, ch in enumerate(prog):
        notes = [ch[0] / 2, ch[1], ch[2], ch[0] * 2, ch[2], ch[1], ch[0] * 2, ch[2]]
        for k, f in enumerate(notes):
            key = round(f, 1)
            if key not in cache: cache[key] = pluck(f, 1.2, rnd) * (np.exp(-np.linspace(0, 4, int(SR * 1.2)))).astype(np.float32)
            s = int(SR * (b * bar + k * beat / 2)); pat[s:s + len(cache[key])] += cache[key] * (0.7 if k else 1.0)
    pat = pat[:L]
    n = int(SR * total); reps = n // L + 1
    m = np.tile(pat, reps)[:n]
    m = m / (np.abs(m).max() + 1e-6)
    fade = int(SR * 1.5); m[-fade:] *= np.linspace(1, 0, fade); m[:int(SR * 0.5)] *= np.linspace(0, 1, int(SR * 0.5))
    return m

def beep(dur=0.18, f=1800):
    t = np.arange(int(SR * dur)) / SR
    return (np.sign(np.sin(2 * np.pi * f * t)) * 0.25 * np.minimum(1, (dur - t) * 40)).astype(np.float32)

def build_audio(SEG, D, PRE, DUR, out, mvol=0.07, extra_fx=(), music_mask=None, mood="happy", lead=0.0):
    total = lead + sum(DUR); n = int(SR * total) + SR
    mix = np.zeros(n, np.float32); start = lead
    for i in range(len(SEG)):
        a = read_wav(f"{D}/vo{i:02d}.wav"); s = int(SR * (start + PRE)); mix[s:s + len(a)] += a * 0.95
        start += DUR[i]
    for (t0, sig, vol) in extra_fx:
        s = int(SR * t0); mix[s:s + len(sig)] += sig[:max(0, n - s)] * vol
    m = music(total, mood=mood)
    if music_mask is not None: m = m * music_mask(np.arange(len(m)) / SR)
    mix[:len(m)] += m * mvol
    mix = np.clip(mix, -1, 1)[:int(SR * total)]
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    return total

def render_seg(frame, i, dur, D, W, H, FPS=30):
    n = int(round(dur * FPS)); tmp = f"{D}/seg{i:02d}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n): p.stdin.write(frame(i, k / FPS).tobytes())
    p.stdin.close(); assert p.wait() == 0
    os.rename(tmp, f"{D}/seg{i:02d}.mp4")
    return n

def concat(D, N, audio, out, FPS=30):
    with open(f"{D}/list.txt", "w") as f:
        for i in range(N): f.write(f"file 'seg{i:02d}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{D}/list.txt", "-c", "copy", f"{D}/video_noaudio.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{D}/video_noaudio.mp4", "-i", audio, "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-shortest", out], check=True)

def mouth(on, t): return (0.25 + 0.75 * abs(math.sin(t * 11))) if on else 0.0
def blink(t, k=0):
    p = (t + k * 0.9) % 3.4
    return p < 0.16 or (k % 3 == 0 and 0.32 < p < 0.46)

def camera(im, cx, cy, z, W, H):
    if z <= 1.001: return im
    w, h = W / z, H / z
    x0 = max(0, min(W - w, cx - w / 2)); y0 = max(0, min(H - h, cy - h / 2))
    return im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)
