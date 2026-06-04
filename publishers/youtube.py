"""
Publisher YouTube Shorts via YouTube Data API v3.
Richiede: progetto Google Cloud con YouTube Data API attiva, OAuth (client id/secret)
e un refresh_token del canale Zampotta.
"""
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_URI = "https://oauth2.googleapis.com/token"


def _service():
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri=TOKEN_URI,
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def publish(video_path: str, title: str, description: str, tags=None) -> dict:
    yt = _service()
    # i Short si riconoscono da formato verticale + hashtag #Shorts nel titolo/descrizione
    body = {
        "snippet": {
            "title": (title[:95] + " #Shorts"),
            "description": description + "\n\n#Shorts #cani #gatti #zampotta",
            "tags": tags or ["cani", "gatti", "animali", "zampotta"],
            "categoryId": "15",  # Pets & Animals
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }
    media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        _status, resp = req.next_chunk()
    return {"channel": "youtube", "status": "published", "id": resp.get("id")}
