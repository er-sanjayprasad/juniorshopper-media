"""Generate voice audio for every job in jobs/*.json using ElevenLabs.
Job format: {"lines": [{"id": "00", "voice_id": "...", "text": "...", "stability": 0.4}], "model": "eleven_multilingual_v2"}
Audio is written to audio/<job>/<id>.mp3. Lines that already have audio are skipped.
"""
import json, os, pathlib, sys, urllib.request

import traceback, urllib.error
KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
pathlib.Path("audio").mkdir(exist_ok=True)
LOG = open("audio/log.txt", "w")
def log(*a):
    print(*a); print(*a, file=LOG); LOG.flush()
if not KEY:
    log("ERROR: ELEVENLABS_API_KEY secret is missing or empty"); sys.exit(0)

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def err(e):
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code}: {e.read()[:400]!r}"
    return repr(e)

try:
    voices = json.loads(call("https://api.elevenlabs.io/v1/voices"))
    with open("audio/voices.json", "w") as f:
        json.dump([{"voice_id": v["voice_id"], "name": v["name"], "labels": v.get("labels", {})} for v in voices.get("voices", [])], f, ensure_ascii=False, indent=1)
    log("voices listed:", len(voices.get("voices", [])))
except Exception as e:
    log("WARN voices list failed:", err(e))

for job in sorted(pathlib.Path("jobs").glob("*.json")):
    spec = json.loads(job.read_text())
    out = pathlib.Path("audio") / job.stem
    out.mkdir(parents=True, exist_ok=True)
    for line in spec["lines"]:
        dest = out / f'{line["id"]}.mp3'
        if dest.exists():
            continue
        body = {"text": line["text"], "model_id": spec.get("model", "eleven_multilingual_v2"),
                "voice_settings": {"stability": line.get("stability", 0.45), "similarity_boost": 0.8, "style": line.get("style", 0.3)}}
        try:
            dest.write_bytes(call(f'https://api.elevenlabs.io/v1/text-to-speech/{line["voice_id"]}?output_format=mp3_44100_128', body))
            log("made", dest)
        except Exception as e:
            log("ERROR", job.stem, line["id"], err(e))
