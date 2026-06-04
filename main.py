"""
Zampotta Autopilot — orchestratore.

Uso:
  python main.py generate   # crea il video del giorno in media/ e scrive today.json
  python main.py publish    # pubblica il video sui canali attivi e aggiorna posts_log.json

Il flusso e' separato cosi' GitHub Actions puo' committare/pushare il video PRIMA
di pubblicarlo (Instagram/TikTok hanno bisogno di un URL pubblico = la raw URL del repo).
"""
import os
import sys
import json
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA_DIR = os.path.join(ROOT, "media")
TODAY_FILE = os.path.join(ROOT, "today.json")
LOG_FILE = os.path.join(ROOT, "posts_log.json")
CAPTIONS = os.path.join(ROOT, "content", "captions.json")

ACCENTS = ["0xFF7A59", "0x2BB6A3"]


def _load_json(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def pick_post():
    data = _load_json(CAPTIONS, {"posts": []})
    posts = data["posts"]
    idx = datetime.date.today().timetuple().tm_yday % len(posts)
    post = posts[idx]
    post["_hashtags"] = post.get("hashtags", data.get("default_hashtags", []))
    post["_idx"] = idx
    return post


def cmd_generate():
    from content.generate_video import generate
    post = pick_post()
    date = datetime.date.today().isoformat()
    os.makedirs(MEDIA_DIR, exist_ok=True)
    out = os.path.join(MEDIA_DIR, f"{date}.mp4")
    accent = ACCENTS[post["_idx"] % len(ACCENTS)]
    generate(post, out, accent=accent)
    today = {
        "date": date,
        "file": f"{date}.mp4",
        "caption": post["caption"] + "\n" + " ".join(post["_hashtags"]),
        "title": f"{post['hook']} {post['sub']}",
    }
    with open(TODAY_FILE, "w", encoding="utf-8") as f:
        json.dump(today, f, ensure_ascii=False, indent=2)
    print(f"[generate] creato {out}")


def cmd_publish():
    today = _load_json(TODAY_FILE, None)
    if not today:
        print("[publish] nessun today.json, esegui prima 'generate'")
        sys.exit(1)

    channels = [c.strip() for c in os.environ.get("ENABLED_CHANNELS", "").split(",") if c.strip()]
    media_base = os.environ.get("PUBLIC_MEDIA_BASE", "").rstrip("/")
    public_url = f"{media_base}/{today['file']}"
    local_path = os.path.join(MEDIA_DIR, today["file"])
    results = []

    if "instagram" in channels:
        try:
            from publishers import instagram
            results.append(instagram.publish(public_url, today["caption"]))
        except Exception as e:  # noqa: BLE001
            results.append({"channel": "instagram", "status": "error", "error": str(e)})

    if "youtube" in channels:
        try:
            from publishers import youtube
            results.append(youtube.publish(local_path, today["title"], today["caption"]))
        except Exception as e:  # noqa: BLE001
            results.append({"channel": "youtube", "status": "error", "error": str(e)})

    if "tiktok" in channels:
        try:
            from publishers import tiktok
            results.append(tiktok.publish(public_url, today["caption"], public=False))
        except Exception as e:  # noqa: BLE001
            results.append({"channel": "tiktok", "status": "error", "error": str(e)})

    log = _load_json(LOG_FILE, [])
    log.insert(0, {
        "date": today["date"],
        "file": today["file"],
        "title": today["title"],
        "results": results,
    })
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    for r in results:
        print(f"[publish] {r.get('channel')}: {r.get('status')} {r.get('error', r.get('id',''))}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "generate"
    {"generate": cmd_generate, "publish": cmd_publish}.get(cmd, cmd_generate)()
