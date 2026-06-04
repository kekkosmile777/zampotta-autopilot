"""
Genera un video verticale 1080x1920 (~12s) brand Zampotta con ffmpeg.
Richiede: ffmpeg installato, font DejaVuSans-Bold, l'icona del brand (assets/icona.png).
Usa SOLO testo ASCII (niente emoji/apostrofi) per evitare problemi di rendering.
"""
import os
import subprocess
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON = os.path.join(ROOT, "assets", "icona.png")
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

CREAM = "0xFFF7F0"
TEAL = "0x2BB6A3"
TEAL_DARK = "0x1E8576"
CORAL = "0xFF7A59"
INK = "0x2D2A32"


def _font():
    for f in FONT_CANDIDATES:
        if os.path.exists(f):
            return f
    raise RuntimeError("Nessun font trovato. Installa DejaVu o indica un font valido.")


def _esc(text: str) -> str:
    # drawtext escaping: niente apostrofi, niente due punti non escapati
    return text.replace(":", "\\:").replace("'", "")


def generate(post: dict, out_path: str, accent: str = CORAL) -> str:
    """post = {hook, sub, cta}; crea out_path .mp4 e lo restituisce."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg non installato")
    font = _font()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    payoff = "Tutto per la sua felicita"
    hook = _esc(post.get("hook", ""))
    sub = _esc(post.get("sub", ""))
    cta = _esc(post.get("cta", ""))

    silent = out_path.replace(".mp4", "_silent.mp4")
    pad = out_path.replace(".mp4", "_pad.m4a")

    vf = (
        f"[1:v]scale=520:-1,format=rgba,fade=in:st=0:d=0.8:alpha=1[ic];"
        f"[0:v]drawbox=x=0:y=0:w=1080:h=18:color={accent}@1:t=fill,"
        f"drawbox=x=0:y=1902:w=1080:h=18:color={accent}@1:t=fill[bg];"
        f"[bg][ic]overlay=x=(W-w)/2:y=330[v1];"
        f"[v1]drawtext=fontfile={font}:text='{hook}':fontcolor={INK}:fontsize=72:x=(w-text_w)/2:y=1000:enable='gte(t,0.8)',"
        f"drawtext=fontfile={font}:text='{sub}':fontcolor={TEAL_DARK}:fontsize=50:x=(w-text_w)/2:y=1110:enable='gte(t,1.5)',"
        f"drawtext=fontfile={font}:text='ZAMPOTTA':fontcolor={TEAL}:fontsize=112:x=(w-text_w)/2:y=1330:enable='gte(t,3.2)',"
        f"drawtext=fontfile={font}:text='{payoff}':fontcolor={CORAL}:fontsize=44:x=(w-text_w)/2:y=1480:enable='gte(t,4.2)',"
        f"drawtext=fontfile={font}:text='{cta}':fontcolor={INK}:fontsize=48:x=(w-text_w)/2:y=1680:enable='gte(t,6.8)',"
        f"fade=in:st=0:d=0.6,fade=out:st=11.3:d=0.7[vout]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={CREAM}:s=1080x1920:d=12:r=30",
        "-loop", "1", "-i", ICON,
        "-filter_complex", vf,
        "-map", "[vout]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-t", "12",
        silent,
    ], check=True)

    # base audio soffice (accordo La maggiore) a basso volume
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "sine=frequency=220:duration=12",
        "-f", "lavfi", "-i", "sine=frequency=277.18:duration=12",
        "-f", "lavfi", "-i", "sine=frequency=329.63:duration=12",
        "-filter_complex",
        "[0][1][2]amix=inputs=3:duration=longest,tremolo=f=5:d=0.4,lowpass=f=1600,volume=0.10,"
        "afade=in:st=0:d=1.2,afade=out:st=10.5:d=1.5[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", "128k", pad,
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", silent, "-i", pad,
        "-c:v", "copy", "-c:a", "aac", "-shortest", out_path,
    ], check=True)

    for f in (silent, pad):
        try:
            os.remove(f)
        except OSError:
            pass
    return out_path
