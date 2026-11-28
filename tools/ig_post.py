#!/usr/bin/env python3
"""Post today's Junior Shopper Reel to Instagram with the Instagram Graph API (graph.facebook.com).

Reads daily/<today IST>/instagram.json: {"video": "daily/.../short.mp4", "caption": "..."}
Writes daily/<today>/instagram_done.json after a successful post (so it never posts twice).

Secrets (GitHub > Settings > Secrets > Actions):
  IG_ACCESS_TOKEN  required. Best: a Facebook PAGE access token that "never expires".
  IG_USER_ID       optional. Instagram business account id; found automatically if empty.
  IG_APP_ID, IG_APP_SECRET  optional, used only by --check to show token type/expiry.

  python3 tools/ig_post.py          post today's Reel (if not posted yet)
  python3 tools/ig_post.py --check  check the token and print the Instagram account (no posting)
"""
import json, os, sys, time, datetime, pathlib, urllib.request, urllib.parse, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://graph.facebook.com/v26.0"
RAW = "https://raw.githubusercontent.com/er-sanjayprasad/juniorshopper-media/main/"
TOKEN = os.environ.get("IG_ACCESS_TOKEN", "").strip()


def call(path, params=None, post=False):
    params = dict(params or {})
    params["access_token"] = TOKEN
    data = urllib.parse.urlencode(params)
    url = f"{API}/{path}"
    try:
        if post:
            r = urllib.request.urlopen(url, data.encode(), timeout=120)
        else:
            r = urllib.request.urlopen(url + "?" + data, timeout=120)
        return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{path}: HTTP {e.code} {e.read().decode()[:400]}")


def ig_user_id():
    uid = os.environ.get("IG_USER_ID", "").strip()
    if uid:
        return uid
    try:
        me = call("me", {"fields": "id,name,instagram_business_account"})
        if me.get("instagram_business_account"):      # Page token
            return me["instagram_business_account"]["id"]
    except RuntimeError as e:
        if "nonexisting field" not in str(e):         # a User token has no such field; anything else is real
            raise
    pages = call("me/accounts", {"fields": "name,instagram_business_account"})  # User token
    for p in pages.get("data", []):
        if p.get("instagram_business_account"):
            return p["instagram_business_account"]["id"]
    raise RuntimeError("No Instagram business account found for this token")


def check():
    uid = ig_user_id()
    acct = call(uid, {"fields": "username,followers_count,media_count"})
    print("Instagram account:", acct)
    app_id, secret = os.environ.get("IG_APP_ID", ""), os.environ.get("IG_APP_SECRET", "")
    if app_id and secret:
        q = urllib.parse.urlencode({"input_token": TOKEN, "access_token": f"{app_id}|{secret}"})
        d = json.load(urllib.request.urlopen(f"{API}/debug_token?{q}", timeout=60))["data"]
        exp = d.get("expires_at", 0)
        print("Token type:", d.get("type"), "| valid:", d.get("is_valid"),
              "| expires:", "NEVER" if not exp else datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).isoformat())


def post():
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)
    day = ROOT / "daily" / today.strftime("%Y-%m-%d")
    job, done = day / "instagram.json", day / "instagram_done.json"
    if not job.exists():
        print("No instagram.json for today; nothing to post."); return
    if done.exists():
        print("Already posted today."); return
    j = json.loads(job.read_text(encoding="utf-8"))
    uid = ig_user_id()
    c = call(f"{uid}/media", {"media_type": "REELS", "video_url": RAW + j["video"],
                             "caption": j.get("caption", ""), "share_to_feed": "true"}, post=True)
    cid = c["id"]
    for _ in range(60):                                # wait up to ~10 min for Instagram to process
        st = call(cid, {"fields": "status_code,status"})
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            raise RuntimeError(f"Instagram processing error: {st}")
        time.sleep(10)
    else:
        raise RuntimeError("Instagram did not finish processing the video in 10 minutes")
    pub = call(f"{uid}/media_publish", {"creation_id": cid}, post=True)
    done.write_text(json.dumps({"media_id": pub["id"], "posted_at": today.isoformat(timespec="minutes") + "+05:30"},
                               indent=1), encoding="utf-8")
    print("Posted Reel, media id", pub["id"])


if __name__ == "__main__":
    if not TOKEN:
        print("IG_ACCESS_TOKEN secret is not set; skipping."); sys.exit(0)
    check() if "--check" in sys.argv else post()
