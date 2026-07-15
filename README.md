# Drug Repair Sidecar — Sparkathon 2026

ASR post-processing pipeline that corrects drug name transcription errors.
Demo site compares before/after transcriptions across four fix strategies.

## Fix strategies

| Type | Description |
|---|---|
| **Text Post-process** | Dictionary lookup / phonetic edit-distance on raw transcript |
| **Term Boost** | Re-run decoder with hotword boost on drug name candidates |
| **Re-decode** | Isolate erroneous segment, redecode with larger/targeted model |
| **Prompt / History** | Inject conversation history or drug-name context into decoder prompt |

## Repo structure

```
├── site/               # Everything Cloudflare Pages serves (output dir = site)
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── data/
│   │   └── demos.json
│   └── audio/          # WAV files go here
├── .gitignore
└── README.md
```

## Running locally

Open `index.html` via a local server (needed for `fetch('data/demos.json')`):

```bash
npx serve .
# or
python -m http.server 8080
```

## Deploying to Cloudflare Pages

1. Push this repo to GitHub.
2. Go to **Cloudflare Dashboard → Pages → Create a project → Connect to Git**.
3. Settings:
   - **Production branch:** `main`
   - **Build command:** `exit 0`
   - **Build output directory:** `site`
4. Click **Save and Deploy**. You'll get a `*.pages.dev` URL.

## Adding real audio

Drop WAV files into `site/audio/` matching the paths in `data/demos.json`, e.g.:

```
site/audio/case001.wav
site/audio/case002.wav
...
```

Update `data/demos.json` with real transcripts and WER numbers before the judging session.

