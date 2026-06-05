# CLAUDE.md

## lightthebe.am

Sacramento Kings fan page — Light the Beam. Single-page tracker showing whether the beam is lit (Kings won their last home game). Live game probability via ESPN, season recap with beam calendar, automated offseason mode with countdown to opening night. Easter eggs include 5-click logo demo mode and a chargeable beam button on the About page. Deployed to Cloudflare Pages.

## Deploy

```bash
wrangler pages deploy . --project-name=lightthebeam
```

(Auth: needs `wrangler login` or `CLOUDFLARE_API_TOKEN` env var.)

## Architecture notes

- Single `index.html` file — all CSS and JS inline.
- All data fetched client-side from ESPN's public API at view time. No backend, no database, no scheduled jobs.
- Phase detection (`inseason` / `offseason` / `preseason`) is API-driven, not date-driven — see `getData()`.
- Past-season navigation is the same component; `currentSeason` global decides what gets fetched.
- AdSense scaffolding is in place but ads currently require approval before they will serve.
