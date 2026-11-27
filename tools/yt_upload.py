#!/usr/bin/env python3
"""Upload videos to YouTube with the user's own Google Cloud project.

Each job is uploads/<name>.json:
{
  "channel": "juniorshopper" | "utoon" | "bizarrebrain",
  "file": "daily/2026-11-27/video.mp4",          # path in this repo
  "thumbnail": "daily/2026-11-27/thumb.jpg",     # optional
  "title": "...", "description": "...", "tags": ["..."],
  "categoryId": "27",                            # 27 Education, 1 Film & Animation, 24 Entertainment
  "madeForKids": false,
  "privacy": "private" | "public" | "unlisted",
  "publishAt": "2026-11-27T19:00:00+05:30",      # optional, needs privacy private
  "language": "hi"
}
Results go to uploads/done/<name>.json (video id and channel) and errors to uploads/log.txt.
Jobs that already have a result are skipped.
"""
import json, os, sys, time, pathlib, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
UP = ROOT / "uploads"
DONE = UP / "done"
LOG = UP / "log.txt"
TOKENS = {
    "juniorshopper": "YT_TOKEN_JUNIORSHOPPER",
    "utoon": "YT_TOKEN_UTOON",
    "bizarrebrain": "YT_TOKEN_BIZARREBRAIN",
}


def log(msg):
    line = time.strftime("%Y-%m-%d %H:%M:%S ") + msg
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def access_token(channel):
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ[TOKENS[channel]],
        "grant_type": "refresh_token",
    }).encode()
    r = urllib.request.urlopen("https://oauth2.googleapis.com/token", data, timeout=60)
    return json.load(r)["access_token"]


def req(url, token, data=None, headers=None, method=None):
    h = {"Authorization": "Bearer " + token}
    h.update(headers or {})
    return urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h, method=method), timeout=600)


def upload(job, name):
    ch = job["channel"]
    tok = access_token(ch)
    status = {"privacyStatus": job.get("privacy", "private"),
              "selfDeclaredMadeForKids": bool(job.get("madeForKids", False)),
              "containsSyntheticMedia": False}
    if job.get("publishAt"):
        status["privacyStatus"] = "private"
        status["publishAt"] = job["publishAt"]
    meta = {
        "snippet": {
            "title": job["title"][:100],
            "description": job.get("description", "")[:5000],
            "tags": job.get("tags", []),
            "categoryId": str(job.get("categoryId", "27")),
            "defaultLanguage": job.get("language", "hi"),
            "defaultAudioLanguage": job.get("language", "hi"),
        },
        "status": status,
    }
    path = ROOT / job["file"]
    size = path.stat().st_size
    r = req("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
            tok, json.dumps(meta).encode(),
            {"Content-Type": "application/json; charset=UTF-8",
             "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)}, "POST")
    loc = r.headers["Location"]
    with open(path, "rb") as f:
        r = req(loc, tok, f.read(), {"Content-Type": "video/mp4"}, "PUT")
    res = json.load(r)
    vid = res["id"]
    out = {"id": vid, "url": "https://youtu.be/" + vid,
           "channelId": res["snippet"].get("channelId"),
           "channelTitle": res["snippet"].get("channelTitle"),
           "privacy": res["status"].get("privacyStatus"),
           "uploadStatus": res["status"].get("uploadStatus")}
    if job.get("thumbnail"):
        try:
            tp = ROOT / job["thumbnail"]
            ct = "image/png" if tp.suffix.lower() == ".png" else "image/jpeg"
            req("https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=" + vid,
                tok, tp.read_bytes(), {"Content-Type": ct}, "POST")
            out["thumbnail"] = "set"
        except urllib.error.HTTPError as e:
            out["thumbnail"] = "failed: " + e.read().decode()[:300]
    return out


def main():
    DONE.mkdir(parents=True, exist_ok=True)
    for jf in sorted(UP.glob("*.json")):
        name = jf.stem
        dest = DONE / jf.name
        if dest.exists():
            continue
        try:
            job = json.loads(jf.read_text(encoding="utf-8"))
            out = upload(job, name)
            dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
            log(f"OK {name}: {out['url']} on '{out['channelTitle']}' ({out['privacy']}) thumb={out.get('thumbnail','-')}")
        except urllib.error.HTTPError as e:
            log(f"ERROR {name}: HTTP {e.code} {e.read().decode()[:500]}")
        except Exception as e:
            log(f"ERROR {name}: {type(e).__name__} {e}")


if __name__ == "__main__":
    main()
