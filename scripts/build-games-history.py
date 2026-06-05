#!/usr/bin/env python3
"""
Generates games-history.json — every Sacramento Kings game from 2001-02 through
the most-recently-completed season, with records-relevant fields extracted.

The current in-progress season is intentionally excluded so the file is stable
between deploys; the facts page fetches current-season data live from ESPN.

Run from the repo root: python3 scripts/build-games-history.py
"""
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

KID = "23"
# First lit October 29, 2022 vs Miami Heat (per ESPN/Wikipedia).
# The searchlight was installed Sept 16, 2022 ("916 Day") but didn't fire until the first home win.
# Any game on or after this date is beam-era; anything before is a pre-beam home win.
BEAM_START_DATE = "2022-10-29"
SCHED_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{kid}/schedule?season={yr}&seasontype={st}"
SUMMARY_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={gid}"


def current_season_year():
    now = datetime.utcnow()
    # ESPN convention: season year = ending year. NBA starts in Oct.
    return now.year + 1 if now.month >= 10 else now.year


def fetch_json(url, retries=3):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.loads(r.read())
        except Exception as e:
            if attempt == retries - 1:
                return None
            time.sleep(0.5 * (attempt + 1))


def parse_score(c):
    s = c.get("score")
    if s is None:
        return 0
    if isinstance(s, dict):
        try:
            return int(s.get("displayValue") or s.get("value") or 0)
        except (TypeError, ValueError):
            return 0
    try:
        return int(s)
    except (TypeError, ValueError):
        return 0


def extract_game(event, summary):
    comp = (event.get("competitions") or [{}])[0]
    competitors = comp.get("competitors") or []
    ks = next((c for c in competitors if str((c.get("team") or {}).get("id")) == KID), None)
    os_ = next((c for c in competitors if str((c.get("team") or {}).get("id")) != KID), None)
    if not ks or not os_:
        return None
    k_score = parse_score(ks)
    o_score = parse_score(os_)

    def team_stats(team_box):
        out = {}
        for s in (team_box or {}).get("statistics") or []:
            name = s.get("name")
            if name:
                out[name] = s.get("displayValue")
        return out

    teams_box = (summary.get("boxscore") or {}).get("teams") or []
    sac_box = next((t for t in teams_box if str((t.get("team") or {}).get("id")) == KID), None)
    opp_box = next((t for t in teams_box if str((t.get("team") or {}).get("id")) != KID), None)

    def linescores(c):
        out = []
        for ls in c.get("linescores") or []:
            v = ls.get("displayValue") or ls.get("value") or 0
            try:
                out.append(int(v))
            except (TypeError, ValueError):
                out.append(0)
        return out

    # Player-level data: who played for SAC in this game (with minutes > 0)
    players_box = (summary.get("boxscore") or {}).get("players") or []
    sac_players_box = next(
        (t for t in players_box if str((t.get("team") or {}).get("id")) == KID), None
    )
    sac_players = []
    if sac_players_box:
        sg = (sac_players_box.get("statistics") or [{}])[0]
        labels = sg.get("labels") or []
        try:
            min_idx = labels.index("MIN")
        except ValueError:
            min_idx = -1
        for a in sg.get("athletes") or []:
            if a.get("didNotPlay"):
                continue
            stats = a.get("stats") or []
            try:
                mins = int(stats[min_idx]) if min_idx >= 0 and len(stats) > min_idx else 0
            except (TypeError, ValueError):
                mins = 0
            if mins <= 0:
                continue
            ath = a.get("athlete") or {}
            sac_players.append({
                "id": str(ath.get("id") or ""),
                "name": ath.get("displayName") or ath.get("shortName") or "",
                "pos": (ath.get("position") or {}).get("abbreviation") or "",
                "min": mins,
            })

    # preBeam = the beam didn't exist yet. Pre-beam home wins are home wins, not beams.
    game_date = event.get("date") or ""
    is_pre_beam = game_date < BEAM_START_DATE

    return {
        "gameId": event.get("id"),
        "date": game_date,
        "home": ks.get("homeAway") == "home",
        "won": k_score > o_score,
        "kScore": k_score,
        "oScore": o_score,
        "opp": (os_.get("team") or {}).get("abbreviation") or "???",
        "preBeam": is_pre_beam,
        "sacStats": team_stats(sac_box),
        "oppStats": team_stats(opp_box),
        "sacLinescores": linescores(ks),
        "oppLinescores": linescores(os_),
        "sacPlayers": sac_players,
    }


def crunch_season(yr):
    """Returns list of game dicts for season ending in yr (e.g. 2026 = 2025-26)."""
    season_games = []
    # Regular season + postseason.
    events_by_id = {}
    for st in (2, 3):
        sched = fetch_json(SCHED_URL.format(kid=KID, yr=yr, st=st))
        if not sched:
            continue
        for ev in sched.get("events") or []:
            status_name = (
                ((ev.get("competitions") or [{}])[0].get("status") or {}).get("type") or {}
            ).get("name")
            if status_name == "STATUS_FINAL":
                events_by_id[ev.get("id")] = ev

    if not events_by_id:
        return []

    def fetch_one(gid_event):
        gid, ev = gid_event
        summary = fetch_json(SUMMARY_URL.format(gid=gid))
        if not summary:
            return None
        return extract_game(ev, summary)

    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(fetch_one, item): item for item in events_by_id.items()}
        for fut in as_completed(futures):
            r = fut.result()
            if r:
                season_games.append(r)

    season_games.sort(key=lambda g: g["date"])
    return season_games


def main():
    cur = current_season_year()
    # Build for everything older than the current in-progress season.
    end = cur - 1  # most-recently-completed season
    start = 2002  # 2001-02 ESPN season year
    print(f"Building history: seasons {start} -> {end} (current {cur} excluded)", file=sys.stderr)

    all_games = []
    for yr in range(start, end + 1):
        season_name = f"{yr-1}-{str(yr)[2:]}"
        sys.stderr.write(f"  {season_name}... ")
        sys.stderr.flush()
        games = crunch_season(yr)
        sys.stderr.write(f"{len(games)} games\n")
        all_games.extend(games)
        time.sleep(0.5)  # polite delay between seasons

    all_games.sort(key=lambda g: g["date"])
    out = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "seasonsIncluded": {"start": start, "end": end},
        "beamStartDate": BEAM_START_DATE,
        "games": all_games,
    }
    with open("games-history.json", "w") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"Wrote games-history.json — {len(all_games)} games", file=sys.stderr)


if __name__ == "__main__":
    main()
