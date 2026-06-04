"""
Publisher Instagram Reels via Meta Graph API.
Richiede: account Instagram BUSINESS collegato a una Pagina Facebook, app Meta,
token a lunga durata. Il video deve essere raggiungibile a un URL PUBBLICO (video_url).
"""
import os
import time
import requests

GRAPH = "https://graph.facebook.com/v21.0"


def publish(video_url: str, caption: str) -> dict:
    ig_user_id = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]

    # 1) Crea il container del Reel
    r = requests.post(
        f"{GRAPH}/{ig_user_id}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": token,
        },
        timeout=60,
    )
    r.raise_for_status()
    creation_id = r.json()["id"]

    # 2) Attendi che il media sia pronto (FINISHED)
    for _ in range(30):  # max ~5 minuti
        s = requests.get(
            f"{GRAPH}/{creation_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=30,
        ).json()
        code = s.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise RuntimeError(f"Instagram media in ERROR: {s}")
        time.sleep(10)
    else:
        raise TimeoutError("Instagram: il media non e' diventato FINISHED in tempo")

    # 3) Pubblica
    p = requests.post(
        f"{GRAPH}/{ig_user_id}/media_publish",
        data={"creation_id": creation_id, "access_token": token},
        timeout=60,
    )
    p.raise_for_status()
    media_id = p.json().get("id")
    return {"channel": "instagram", "status": "published", "id": media_id}
