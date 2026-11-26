"""Generate Pixar-style 3D clips with fal.ai for every job in fal_jobs/*.json.
Job format:
{"style": "Pixar-style 3D animation, soft lighting, vibrant colors, cute expressive Indian kids",
 "aspect_ratio": "9:16",
 "video_model": "fal-ai/kling-video/v2.6/pro/image-to-video",
 "image_model": "fal-ai/flux/dev",
 "clips": [{"id": "01", "image_prompt": "...", "motion_prompt": "...", "duration": "5"}]}
Writes fal_out/<job>/<id>.png and <id>.mp4 plus fal_out/log.txt. Clips already made are skipped.
"""
import json, os, pathlib, time, urllib.request, urllib.error

KEY = os.environ.get("FAL_KEY", "").strip()
out_root = pathlib.Path("fal_out"); out_root.mkdir(exist_ok=True)
LOG = open(out_root / "log.txt", "a")
def log(*a):
    print(*a); print(*a, file=LOG); LOG.flush()

def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                               headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"},
                               method="POST" if body is not None else "GET")
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read())

def run(model, args, wait=900):
    sub = req(f"https://queue.fal.run/{model}", args)
    status_url, resp_url = sub["status_url"], sub["response_url"]
    t0 = time.time()
    while time.time() - t0 < wait:
        st = req(status_url)
        if st.get("status") == "COMPLETED":
            return req(resp_url)
        time.sleep(6)
    raise TimeoutError(model)

def download(url, dest):
    with urllib.request.urlopen(url, timeout=300) as r: dest.write_bytes(r.read())

if not KEY:
    log("ERROR: FAL_KEY secret is missing"); raise SystemExit(0)

for job in sorted(pathlib.Path("fal_jobs").glob("*.json")):
    spec = json.loads(job.read_text()); out = out_root / job.stem; out.mkdir(parents=True, exist_ok=True)
    style = spec.get("style", "")
    for c in spec["clips"]:
        mp4 = out / f'{c["id"]}.mp4'
        if mp4.exists(): continue
        try:
            png = out / f'{c["id"]}.png'
            if not png.exists():
                img = run(spec.get("image_model", "fal-ai/flux/dev"), {"prompt": f'{c["image_prompt"]}. {style}',
                          "image_size": "portrait_16_9" if spec.get("aspect_ratio", "9:16") == "9:16" else "landscape_16_9"})
                download(img["images"][0]["url"], png)
            # upload the still as a data URL so the video model can use it
            import base64
            data_url = "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode()
            vid = run(spec.get("video_model", "fal-ai/kling-video/v2.6/pro/image-to-video"),
                      {"prompt": f'{c["motion_prompt"]}. {style}', "image_url": data_url, "duration": c.get("duration", "5")})
            download(vid["video"]["url"], mp4)
            log("made", mp4)
        except urllib.error.HTTPError as e:
            log("ERROR", job.stem, c["id"], f"HTTP {e.code}: {e.read()[:400]!r}")
        except Exception as e:
            log("ERROR", job.stem, c["id"], repr(e))
