"""
Publisher TikTok via Content Posting API (PULL_FROM_URL).
ATTENZIONE: finche' l'app TikTok non e' APPROVATA dall'audit, la privacy consentita
e' SELF_ONLY (bozza privata, visibile solo a te). Per il pubblico serve l'app approvata.
Richiede: app TikTok for Developers, token utente con scope video.publish.
Il video deve essere a un URL PUBBLICO verificato (dominio whitelisted nell'app TikTok).
"""
import os
import requests

BASE = "https://open.tiktokapis.com/v2"


def publish(video_url: str, caption: str, public: bool = False) -> dict:
    token = os.environ["TIKTOK_ACCESS_TOKEN"]
    privacy = "PUBLIC_TO_EVERYONE" if public else "SELF_ONLY"
    r = requests.post(
        f"{BASE}/post/publish/video/init/",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        json={
            "post_info": {
                "title": caption[:150],
                "privacy_level": privacy,
                "disable_comment": False,
                "disable_duet": False,
                "disable_stitch": False,
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url,
            },
        },
        timeout=60,
    )
    r.raise_for_status()
    data = r.json().get("data", {})
    return {
        "channel": "tiktok",
        "status": "draft" if not public else "published",
        "id": data.get("publish_id"),
        "note": "bozza privata (app non ancora approvata)" if not public else "",
    }
