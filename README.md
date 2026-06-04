# 🐾 Zampotta Autopilot

Macchina di **pubblicazione automatica** dei contenuti social per il brand **Zampotta** (cani & gatti).
Usa solo le **API ufficiali** (niente bot, niente rischio ban) ed è ospitata **gratis** su GitHub.

## Cosa fa
1. **Genera** un video verticale + didascalia per il giorno (motion-graphic con ffmpeg, o usa video pronti nella cartella `media/`).
2. **Pubblica** in automatico su:
   - ✅ **Instagram** (Reels) — via Meta Graph API
   - ✅ **YouTube** (Shorts) — via YouTube Data API
   - ⚠️ **TikTok** — via Content Posting API, ma come **bozza privata** finché l'app non è approvata da TikTok
3. **Registra** ogni pubblicazione in `posts_log.json` e mostra i risultati nella **dashboard** (`dashboard/index.html`).
4. Gira da solo ogni giorno con **GitHub Actions** (scheduler gratuito nel cloud) — il tuo PC può restare spento.

## Architettura
```
GitHub repo ──► GitHub Actions (cron giornaliero, gratis)
                     │
                     ├─ content/generate_video.py   → crea il video del giorno
                     ├─ publishers/instagram.py      → Reel via Graph API
                     ├─ publishers/youtube.py        → Short via Data API
                     ├─ publishers/tiktok.py         → bozza via Content Posting API
                     └─ main.py                       → orchestra + scrive posts_log.json
                     
dashboard/index.html  ──►  legge posts_log.json e mostra report (GitHub Pages / Render, gratis)
```

## Come parte (sintesi — dettagli in SETUP.md)
1. Tu crei gli accessi API una volta sola (Meta, Google/YouTube, TikTok) — ti guido clic per clic.
2. Metti i token come **GitHub Secrets** (così restano segreti, non finiscono nel codice).
3. Attivi GitHub Pages per la dashboard.
4. Da lì gira da solo: 1 post al giorno, report aggiornati.

## Costi
- GitHub + GitHub Actions + GitHub Pages: **0 €**
- API Meta / YouTube / TikTok: **0 €**
- (Opzionale) dashboard su Render: **0 €** (piano free)
- (Opzionale) video AI realistici: a crediti, solo se vuoi

## File principali
- `main.py` — orchestratore
- `content/generate_video.py` — generatore video
- `content/captions.json` — piano editoriale (didascalie + testi)
- `publishers/` — moduli per ogni piattaforma
- `.github/workflows/publish.yml` — scheduler giornaliero
- `dashboard/index.html` — pannello report
- `posts_log.json` — storico pubblicazioni
- `SETUP.md` — guida passo-passo agli accessi

> ⚠️ **Onestà tecnica:** Instagram e YouTube pubblicano sul *tuo* account in modalità sviluppatore senza review. **TikTok pubblico** richiede l'**audit dell'app da parte di TikTok** (processo a parte): finché non è approvata, i post TikTok restano **bozze private** da pubblicare a mano. I token Meta vanno rinnovati ~ogni 60 giorni (incluso uno script di refresh).
