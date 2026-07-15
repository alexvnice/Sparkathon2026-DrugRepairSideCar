# Drug Repair Sidecar — Sparkathon 2026

ASR post-processing pipeline that corrects drug name transcription errors.
Demo site compares before/after transcriptions across four fix strategies.
Hosted on **Cloudflare Workers + Assets**, gated behind HTTP Basic Auth so only judges can access the live URL.

## Fix strategies

| Type | Description |
|---|---|
| **Text Post-process** | Dictionary lookup / phonetic edit-distance on raw transcript |
| **Term Boost** | Re-run decoder with hotword boost on drug name candidates |
| **Re-decode** | Isolate erroneous segment, redecode with larger/targeted model |
| **Prompt / History** | Inject conversation history or drug-name context into decoder prompt |

## Repo structure

```
├── src/
│   └── index.js        # Cloudflare Worker — Basic Auth gate; passes through to ASSETS
├── site/               # Static frontend served via ASSETS binding
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── data/
│   │   └── demos.json  # Transcript pairs, WER numbers, audio paths
│   └── audio/          # WAV files go here (not committed)
├── wrangler.jsonc       # Worker config — name, assets dir, ASSETS binding
└── README.md
```

## How it works

`src/index.js` is a Cloudflare Worker that runs before every request (`run_worker_first: true`).
It checks for a valid HTTP Basic Auth header matching the `JUDGE_USERNAME` / `JUDGE_PASSWORD` secrets.
On success it proxies to the static `site/` assets via the `ASSETS` binding; otherwise it returns 401.

## Secrets required

Two Cloudflare Worker secrets must be set before the Worker will serve anything:

```bash
wrangler secret put JUDGE_USERNAME
wrangler secret put JUDGE_PASSWORD
```

## Running locally

```bash
npx wrangler dev
```

The Worker runs locally at `http://localhost:8787`. Secrets are read from `.dev.vars` if present:

```
# .dev.vars  (do not commit)
JUDGE_USERNAME=judge
JUDGE_PASSWORD=changeme
```

Alternatively, serve just the static site without auth:

```bash
npx serve site
# or
python -m http.server 8080 --directory site
```

## Deploying to Cloudflare Workers

```bash
wrangler deploy
```

Worker name: `sparkathon2026-drug-repair-side-car` (set in `wrangler.jsonc`).
Secrets must already exist in the Cloudflare dashboard or be set via `wrangler secret put` before deploy.

## Adding real audio

Drop WAV files into `site/audio/` matching the paths in `data/demos.json`, e.g.:

```
site/audio/case001.wav
site/audio/case002.wav
...
```

Update `data/demos.json` with real transcripts and WER numbers before the judging session.

