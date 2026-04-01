# lightthebe.am

Sacramento Kings fan page — live scores, beam tracker, season stats, and standings.

**Live:** [lightthebe.am](https://lightthebe.am)

## Stack

- Single-page static HTML/CSS/JS
- Live data from ESPN API (fetched client-side)
- Hosted on [Cloudflare Pages](https://pages.cloudflare.com)
- No build step

## Deploy

```bash
wrangler pages deploy . --project-name=lightthebeam
```

## Notes

- Season selector with history back to 2022-23
- Easter egg: tap the Kings logo 5x to light the beam
- `_headers` and `_redirects` are Cloudflare Pages config files
- Team logos loaded from ESPN CDN
