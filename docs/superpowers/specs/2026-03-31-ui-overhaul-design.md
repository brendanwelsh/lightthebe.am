# lightthebe.am UI Overhaul — Design Spec

**Date:** 2026-03-31
**Status:** Approved (user said "execute while I sleep")

## Overview

Major UX pass on the Sacramento Kings "Light the Beam" fan site. Improves game data presentation, hover interactions, beam effects, about page, easter eggs, and mobile experience.

## 1. All Games Card (GitHub Beam Tracker)

### Make it larger
- Increase card `flex-basis` from 340px to 420px
- Increase font sizes for game rows (opponent name, score, date)
- Increase logo size from 18px to 24px

### Rich hover tooltip
When hovering any completed game row, show an overlay with:
- Opponent logo (larger, ~40px)
- "The Kings played [Full Team Name] on [Full Date]"
- "Did they light the beam? YES/NO"
- Score: "SAC [score] - [OPP score]"
- Home/away indicator
- For wins: beam-on effect triggers (existing behavior, keep)
- For losses: no beam, "NO" displayed

This tooltip should appear as an inline expansion or overlay below the hovered row.

### Remove upcoming from All Games
- Filter out `STATUS_SCHEDULED` games from the All Games card
- They already appear in the Upcoming tile above
- As games complete, they naturally appear in the completed list

### Idle state for past seasons
- Default display: season beam count + record
- On hover of any game: temporarily show that game's details
- On mouse leave: return to season stats

## 2. Game Tiles Layout

### Score layout (mirrored balance)
For completed games:
```
[Away Logo] [Team Name] [Score]
              @
[Home Logo] [Team Name] [Score]
```

### Upcoming tile — full team names
Add a lookup table:
```js
var TEAM_NAMES = {
  ATL: 'Atlanta Hawks', BOS: 'Boston Celtics', BKN: 'Brooklyn Nets',
  CHA: 'Charlotte Hornets', CHI: 'Chicago Bulls', CLE: 'Cleveland Cavaliers',
  DAL: 'Dallas Mavericks', DEN: 'Denver Nuggets', DET: 'Detroit Pistons',
  GS: 'Golden State Warriors', HOU: 'Houston Rockets', IND: 'Indiana Pacers',
  LAC: 'LA Clippers', LAL: 'Los Angeles Lakers', MEM: 'Memphis Grizzlies',
  MIA: 'Miami Heat', MIL: 'Milwaukee Bucks', MIN: 'Minnesota Timberwolves',
  NO: 'New Orleans Pelicans', NY: 'New York Knicks', OKC: 'Oklahoma City Thunder',
  ORL: 'Orlando Magic', PHI: 'Philadelphia 76ers', PHX: 'Phoenix Suns',
  POR: 'Portland Trail Blazers', SAC: 'Sacramento Kings', SA: 'San Antonio Spurs',
  TOR: 'Toronto Raptors', UTAH: 'Utah Jazz', WSH: 'Washington Wizards'
};
```
Display full names in upcoming tile since there's room.

### Last Game — show date
Add date/time to last game tile for continuity with next game tile.

### Next Game — align spacing
Add empty score-sized slots where the score would be, so logos/team names align vertically with last game.

### Fix "TIMES" label
Remove the word "times" from beam count display. Replace with more descriptive text or just show the number prominently.

## 3. Beam Effect

### Fixed beam (no downward scroll)
Replace the `beamUp` animation (height: 0 to 100vh) with a simple opacity fade-in:
```css
@keyframes beamOn {
  0% { opacity: 0 }
  100% { opacity: 1 }
}
```
The beam is always full-height, just fades in. No directional animation.

### Beam count prominence
- Increase font size of beam count line
- Make it a styled element rather than plain text
- Position prominently below the YES/NO answer

## 4. About Page

### Enlarge classic Kings logo
- Increase from 100px to 180px width

### Text changes
- "Hoop Dreams" -> "Hoop Dreams, Baby"
- Add "FYBA Legend" somewhere prominent

### Light the Beam button
- Large purple button styled like a physical button (3D effect, shadow)
- On click: triggers beam-on effect (same as easter egg flash)
- Satisfying press animation (scale down, then up)
- Text: "LIGHT THE BEAM" in bold

## 5. Easter Eggs

### Remove 5-click logo flash
- Remove current `egg()` function behavior

### Grant Napier quotes (5-click logo)
Famous calls to embed as base64 audio:
- "If you don't like that, you don't like NBA basketball!"
- Since we can't actually download copyrighted audio, we'll use the Web Speech API to generate TTS versions of his famous quotes as a fun approximation, OR create a visual quote display with the text.

**Decision:** Use a visual quote popup (text overlay) with his famous quotes, styled dramatically. This avoids copyright issues and works everywhere. Quotes:
1. "If you don't like that, you don't like NBA basketball!"
2. "SLAM DUNK!"  
3. "He's on FIRE!"
4. "Light the beam, baby!"

### Bouncing basketballs
- On Kings win celebration (or triggered by about page button)
- Create N basketball emoji elements, animate with random trajectories
- Use CSS animations with random delays/positions
- Auto-cleanup after ~5 seconds

## 6. Scrolling & Mobile

### Better scroll experience
- Smooth scroll behavior on cards section
- Snap scrolling for horizontal card container on mobile
- Better touch targets for mobile (min 44px tap targets)

### Mobile responsive
- Game tiles stack vertically on mobile (existing, keep)
- Cards stack vertically on mobile
- Larger touch targets
- Beam button easily accessible on about page
- Ensure all hover interactions have tap equivalents on mobile

## 7. Implementation Notes

- All changes in single `index.html` file
- No external dependencies
- No build tools
- Vanilla JS/CSS only
- Keep ESPN API integration unchanged
- Maintain Cloudflare Pages compatibility
