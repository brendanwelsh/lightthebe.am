# CLAUDE.md

## lightthebe.am

Sacramento Kings fan page — Light the Beam. Tracker showing whether the beam is lit (Kings won their last game, home or road). Live game probability via ESPN, season recap with beam calendar, automated offseason mode with a hero countdown that cycles through upcoming dates (offseason milestones / preseason game dates). Easter eggs: 5-click classic-logo demo mode on `/about` (deep-links home as `/?demo=1`), and a hold-to-charge beam button on `/beam`. Deployed to Cloudflare Pages.

## Deploy

```bash
wrangler pages deploy . --project-name=lightthebeam
```

(Auth: needs `wrangler login` or `CLOUDFLARE_API_TOKEN` env var.)

## Architecture notes

- Multi-page static site, each page self-contained (inline CSS + JS): `index.html` (tracker), `players`/`player`, `totals`, `stats`, `game`, plus `beam.html` ("About the Beam" — beam facts/specs) and `about.html` (the maker bio + PayPal tip). Clean URLs (`/beam`, `/about`, …) are served by Cloudflare Pages; `scripts/preview_server.py` mimics that routing for local preview.
- Every page shares the same top nav (`.page-nav`): Home · Roster · Totals · Stats · Beam · About. Keep them in sync when editing.
- All data fetched client-side from ESPN's public API at view time. No backend, no database, no scheduled jobs.
- Phase detection (`inseason` / `offseason` / `preseason`) is API-driven, not date-driven — see `getData()`.
- Past-season navigation is the same component; `currentSeason` global decides what gets fetched.
- AdSense scaffolding is in place but ads currently require approval before they will serve.
