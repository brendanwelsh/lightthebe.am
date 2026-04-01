<p align="center">
  <img src="https://img.shields.io/badge/status-live-brightgreen" alt="Live">
  <img src="https://img.shields.io/badge/hosting-Cloudflare%20Pages-F38020" alt="Cloudflare Pages">
  <img src="https://img.shields.io/badge/build-zero--config-blue" alt="Zero Config">
  <img src="https://img.shields.io/badge/data-ESPN%20API-red" alt="ESPN API">
  <img src="https://img.shields.io/badge/team-Sacramento%20Kings-5b2d8e" alt="Sacramento Kings">
</p>

<h1 align="center">Light the Beam</h1>
<p align="center"><strong>Is the Beam Lit?</strong></p>
<p align="center">
  <a href="https://lightthebe.am">lightthebe.am</a>
</p>

<p align="center">
  <img src="preview.png" alt="Light the Beam Preview" width="700">
</p>

---

## About

A Sacramento Kings fan dashboard that answers one question: **did the Kings win tonight?** After every Kings victory, Golden 1 Center lights a purple beam into the Sacramento sky. This site tracks that tradition with live scores, a beam calendar, full season stats, NBA standings, and multiple easter eggs.

All game data is fetched live from the ESPN API on every page load — no backend, no database, no stale data. The entire site is a single HTML file.

## Features

- **Live Beam Status** — Giant YES/NO answer that updates automatically from ESPN. When the beam is lit, the entire page gets a purple beam effect (CSS gradient shooting upward from the bottom).

- **Beam Calendar** — Monthly dot grid showing every game of the season. Purple dots = wins (beam lit), dim dots = losses. Hover any dot to see the game details and the answer changes to reflect that game.

- **Season Selector** — Tabs for 2025-26, 2024-25, 2023-24, and 2022-23 seasons. Each loads the full season's data from ESPN.

- **Last Game / Next Game** — Score display for the most recent game and upcoming opponent with tip-off time and ticket link.

- **Upcoming Schedule** — Next 5 games with opponents, dates, and ticket links to the Kings website.

- **NBA Standings** — Full league standings with rank, team logo, record, and win percentage.

- **All Games Log** — Complete game-by-game results for the season with scores, opponents, and W/L indicators.

- **Season Stats Dashboard** — Record (home/away), current streak, best/worst streaks, games left, beams lit, PPG, opponent PPG, point differential, season points, and team rankings (out of 30) for every major stat category.

- **Beam Animation** — When the Kings have won, the page triggers a purple beam effect: a vertical gradient shoots up from the bottom with a glow pulse, plus a brief flash overlay.

- **Easter Egg** — Tap the Kings logo 5 times to manually light the beam with the full animation sequence.

- **Hover-to-Beam on Calendar** — Hovering over a win dot in the beam calendar lights the beam and shows that game's context. Hovering a loss dot shows the result without the beam.

- **About Page** — Toggle-able about section with Kings photos (Bibby, beam ceremonies) and social links.

- **Responsive** — Desktop shows a 3-column stats layout; mobile stacks everything vertically.

## Data Flow

```
Page Load
  |
  v
ESPN Scoreboard API (current season)
  |
  v
Parse: wins, losses, scores, opponents, dates
  |
  v
Render: beam status, calendar, standings, stats
  |
  (no backend — everything is client-side fetch + DOM manipulation)
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Vanilla HTML/CSS/JS — 822 lines |
| Data | ESPN Scoreboard API (client-side fetch, no API key needed) |
| Logos | ESPN CDN (`a.espncdn.com/i/teamlogos/nba/500/`) |
| Fonts | System font stack (-apple-system) |
| Animations | CSS keyframes (beam, flash, fade) |
| Hosting | Cloudflare Pages |

## Assets

| File | Purpose |
|------|---------|
| `bibby.png` | Mike Bibby photo (about page) |
| `bibby-full.png` | Full Bibby photo |
| `beam-house.png` | Golden 1 Center beam photo |
| `beam-tv.png` | Beam on broadcast |
| `kings-classic.png` | Classic Kings logo |
| `kings-logo.png` | Current Kings logo |
| `_headers` | Cloudflare Pages headers config |
| `_redirects` | Cloudflare Pages redirects config |

## Project Structure

```
lightthebe.am/
  index.html          # Entire site — HTML, CSS, JS, ESPN data fetching
  bibby.png           # About page photo
  bibby-full.png      # About page photo
  beam-house.png      # Beam ceremony photo
  beam-tv.png         # Broadcast beam photo
  kings-classic.png   # Retro Kings logo
  kings-logo.png      # Current logo
  _headers            # Cloudflare headers
  _redirects          # Cloudflare redirects
  CHANGES.md          # Version history
  preview.png         # Screenshot for this README
  CLAUDE.md           # AI assistant context
  README.md           # You are here
```

## Deploy

```bash
wrangler pages deploy . --project-name=lightthebeam
```

## License

Private project. All rights reserved. Not affiliated with the Sacramento Kings, NBA, or ESPN.
