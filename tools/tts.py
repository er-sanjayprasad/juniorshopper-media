"""Generate voice audio for every job in jobs/*.json using ElevenLabs.
Job format: {"lines": [{"id": "00", "voice_id": "...", "text": "...", "stability": 0.4}], "model": "eleven_multilingual_v2"}
Audio is written to audio/<job>/<id>.mp3. Lines that already have audio are skipped.
"""
import json, os, pathlib, sys, urllib.request

KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("ELEVENLABS_API_KEY secret is missing")

def call(url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

# keep an up-to-date list of voices available on the account
voices = json.loads(call("https://api.elevenlabs.io/v1/voices"))
pathlib.Path("audio").mkdir(exist_ok=True)
with open("audio/voices.json", "w") as f:
    json.dump([{"voice_id": v["voice_id"], "name": v["name"], "labels": v.get("labels", {})} for v in voices.get("voices", [])], f, ensure_ascii=False, indent=1)

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
        dest.write_bytes(call(f'https://api.elevenlabs.io/v1/text-to-speech/{line["voice_id"]}?output_format=mp3_44100_128', body))
        print("made", dest)
