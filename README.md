# Paytm Kaasu

An AI cash-flow partner for kirana shops, built for the Paytm Buildathon (Chennai, Track 1: Merchant Growth AI).

Kaasu (காசு, Tamil for money) runs on the Paytm Soundbox and the Paytm for Business app. It sees a festival cash gap weeks ahead and closes it with the shop's own savings first, then udhaar collected on payday, then a loan only for the gap. Money moves only with the UPI PIN.

## Run it

Requires Node 24. No install is needed for the core demo.

```
node server.mjs
```

Then open:

- App: http://localhost:3000
- Pitch deck (10 slides): http://localhost:3000/deck/
- Motion films: http://localhost:3000/film2/?play and http://localhost:3000/film/?play

AI features read keys from a local `.env` file, which is never committed:

```
LLM_API_KEY=your-gemini-key
SARVAM_API_KEY=your-sarvam-key   # optional fallback
```

Without keys, or with `OFFLINE=1`, the app runs offline with the same numbers.

## What's here

| Path | What it is |
|---|---|
| `server.mjs` | Node server: AI brief, Q&A, voice and bill reading, with a guardrail that rejects any number the cash engine didn't compute |
| `public/sim.js` | The cash engine: plain, explainable maths, no AI |
| `public/app.js`, `public/index.html` | The app: 3D Soundbox and phone, all journeys |
| `public/deck/` | The 10-slide pitch deck |
| `public/film/`, `public/film2/` | The motion films, rendered to `video/` |
| `video/` | Rendered films and music |
| `tools/` | End-to-end tests (Playwright), asset capture, and deck, film and music generators |
| `Kaasu-Pitch-Story.md` | The pitch story and script |

All merchant data is simulated. No real money, customers or lenders are involved.

## Test

```
PYTHONIOENCODING=utf-8 python tools/shots.py
```

This walks every journey in Chrome and prints any errors.

## After the Buildathon

Rotate the Gemini and Sarvam API keys. They were shared in a chat while building.
