# ⚙️ Setup Zampotta Autopilot (una volta sola)

Questi sono gli unici passaggi che richiedono **te** (accessi/identità). Ti guido clic per clic.
Tutto il resto (codice, video, pubblicazione) lo fa la macchina.

---

## 1. Repository su GitHub (gratis)
1. Crea un account su github.com (puoi usare zampottashop@gmail.com).
2. Crea un repository **privato** chiamato `zampotta-autopilot`.
3. Carica i file di questa cartella (o lo faccio io con il tuo accesso).

## 2. Instagram (Meta Graph API)
> Serve un account Instagram **Business/Creator** collegato a una **Pagina Facebook**.
1. Converti @zampotta in **Account aziendale** (app IG → Impostazioni → tipo di account).
2. Crea una **Pagina Facebook** "Zampotta" e collegala all'account IG.
3. Vai su **developers.facebook.com** → crea un'app tipo "Business".
4. Aggiungi il prodotto **Instagram Graph API**. Genera un **token a lunga durata** con i permessi
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `pages_read_engagement`.
5. Recupera l'**IG_USER_ID** (ID dell'account Instagram business).
6. Annota: `IG_USER_ID`, `IG_ACCESS_TOKEN`, `META_APP_ID`, `META_APP_SECRET`.

## 3. YouTube (Data API v3)
1. Vai su **console.cloud.google.com** → crea un progetto "Zampotta".
2. Abilita **YouTube Data API v3**.
3. Crea credenziali **OAuth 2.0** (tipo Desktop). Ottieni `YT_CLIENT_ID` e `YT_CLIENT_SECRET`.
4. Genera un **refresh token** col canale YouTube di Zampotta (scope `youtube.upload`).
   (Ti fornisco uno scriptino guidato per ottenerlo.)
5. Annota: `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.

## 4. TikTok (opzionale, limitato)
1. **developers.tiktok.com** → crea un'app, prodotto **Content Posting API**, scope `video.publish`.
2. Ottieni un access token utente → `TIKTOK_ACCESS_TOKEN`.
3. ⚠️ Finché l'app non è **approvata** da TikTok, i post escono come **bozza privata**.
   Per il pubblico serve richiedere l'audit (processo separato). Conviene partire con IG + YouTube.

## 5. Inserisci i token come GitHub Secrets
Nel repo → **Settings → Secrets and variables → Actions → New repository secret**.
Aggiungi (i nomi devono essere ESATTI):
```
ENABLED_CHANNELS = instagram,youtube
PUBLIC_MEDIA_BASE = https://raw.githubusercontent.com/<tuo-utente>/zampotta-autopilot/main/media
IG_USER_ID, IG_ACCESS_TOKEN, META_APP_ID, META_APP_SECRET
YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
TIKTOK_ACCESS_TOKEN   (solo se usi TikTok)
```

## 6. Dashboard (gratis)
- Opzione A: **GitHub Pages** → Settings → Pages → Source: branch `main`, cartella `/dashboard`.
- Opzione B: **Render** (static site) collegato al repo, cartella `dashboard`.
La dashboard mostra i post pubblicati e gli errori, leggendo `posts_log.json`.

## 7. Avvio
- Vai su **Actions** nel repo → workflow "Zampotta Autopilot" → **Run workflow** (prova manuale).
- Se va a buon fine, parte da solo ogni giorno alle 12:00 UTC (~13/14 in Italia).

## Manutenzione
- Il **token Meta** scade ogni ~60 giorni: incluso uno script di refresh (`tools/refresh_meta_token.py` — te lo aggiungo quando attiviamo IG).
- Per cambiare orario: modifica il `cron` in `.github/workflows/publish.yml`.
- Per aggiungere/modificare i contenuti: `content/captions.json`.

---

> 🤖 Quando vuoi, dimmi "partiamo col setup" e ti accompagno passo passo (Meta, Google, GitHub), esattamente come abbiamo fatto con Gmail. Tu fai i clic di autenticazione, io configuro tutto il resto.
