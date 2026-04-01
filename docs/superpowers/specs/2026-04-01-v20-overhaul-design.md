# lightthebe.am v20 — Complete UX Overhaul Design Spec

**Date:** 2026-04-01
**Status:** Approved

## 1. Layout Consistency — Universal Game Bar Format

Every game display across the entire site uses this format:

```
[Away Logo] ABR  score  ·  score  ABR [Home Logo]
```

- Logos always on outside edges
- Abbreviations inside the logos
- Scores center-separated by `·`
- Next Game: same layout with blank/`---` where scores go so icons align vertically
- All Games list rows: logo to the RIGHT of team abbreviation

Applied to: Live bar, Last Game bar, Next Game bar, hover preview bar, All Games rows.

## 2. GitHub Beam Tracker (Dot Calendar)

- Same width as game bars (~700px max-width)
- More vertical spacing above, separating from beam count
- Larger dots (14-16px on mobile)
- **Connected to All Games**: hovering a dot highlights the corresponding All Games row, and vice versa. Both use CSS class `.gm-active` for highlight.

## 3. Unified Hover Behavior (Desktop)

When hovering ANY game (dot or All Games row):

1. Hero text changes to: "[Team Full Name] on [Full Date]"
2. Below: "Was the beam lit? **YES**" or "**NO**"
3. Beam turns on for wins, off for losses
4. No floating tooltip or score box — hero text + beam state only
5. On mouse leave: returns to idle (season beam count for current, storytelling text for past)

Past seasons have IDENTICAL behavior to current season.

## 4. Mobile Interaction — Tap-to-Preview

- **First tap** on game row/dot: Shows game detail in hero (does NOT navigate to ESPN)
- **Second tap on same game**: Navigates to ESPN
- **Tap elsewhere**: Clears preview, returns to idle
- Selected game gets subtle highlight border
- Dots increase to 14-16px on mobile for tap targets

Implementation: `data-selected` attribute on tapped element. If already selected, follow the link. Otherwise, preventDefault and show preview.

## 5. About Page — Beam Button Hold-to-Charge

### Hold Mechanic
- Press and hold LIGHT THE BEAM button
- 0-3s: Beam starts dim, button glows subtly
- 3-7s: Beam intensifies, slight screen vibration
- 7-10s: Strong glow, screen shaking
- 10s: EXPLOSION

### Explosion Effect
- Canvas-based particle system: purple/gold sparks, embers, fragments fly outward from center
- Screen shake peaks then settles
- White flash overlay
- Cowbell sound plays
- Everything settles after ~3 seconds
- Colors: Kings purple (#5b2d8e, #9b4dca) and gold (#FDB927)

### Normal tap (no hold)
- Quick beam flash (existing behavior, no basketballs)

## 6. About Page — Content Restructure

### Layout order:
1. Kings classic logo (180px, clickable — 5 clicks = demo mode)
2. **"LIGHT THE BEAM"** title
3. Beam button (hold-to-charge)
4. **"About This Site"** heading
   - "All data pulled from ESPN's public API. Scores update every 30 seconds during live games. Season archives go back to 2022-23 when the beam tradition began."
   - Brief beam tradition explanation
5. **"About the Author"** heading
   - "Built by @BrendanWelsh, FYBA Legend, known as BulldogsRock25 on AIM."
   - "Born and raised in Sacramento. Grew up playing youth basketball, played on the court at Arco Arena. Sat in the nosebleeds watching Webber, Peja, Vlade, Doug Christie, and the greatest team to never win a championship."
   - "Skipped school in 4th grade to get Carl's Jr Kings bobbleheads. Recently got $15 tickets to a game and $16 hot dogs."
6. **Kings Links**: Kings Store, @SacramentoKings, NBA.com/kings
7. **Disclaimer**: "Not affiliated with the Sacramento Kings. Made by a fan, for fans."
8. **Sign-off**: "Hoop Dreams, Baby." (last line, styled as a mic-drop)

## 7. Easter Eggs & Demo Mode

- **5-click Kings logo**: Toggles live game demo mode
- **Red "DEMO" stamp** overlaid on the live game bar (rotated, semi-transparent, unmistakable)
- **Cowbell sound** (royalty-free, base64-embedded) plays on demo activation
- Remove all previous easter egg behavior (no TTS, no visual quotes, no bouncing basketballs on win load)

## 8. Season Navigation

- Current season pill: **"Current"** instead of "2025-26"
- Past season idle state: Storytelling — "In the 2024-25 season, the Kings lit the beam **40** times" with prominent styled number
- Past seasons show the same All Games card (scrollable), same GitHub dots, same hover behavior

## 9. Visual Polish

- **Live game clock**: Larger font for quarter/time display
- **Beam count**: More prominent, less faded
- **All Games rows**: Remove left win/loss color bar. Just rows with hover behavior.
- **Beam laser**: Positioned below footer
- **No redundant text**: Single source of truth for beam count, record, etc.
- **Font audit**: Slightly increase base sizes for readability

## 10. Cowbell Audio

Embed a short royalty-free cowbell sound as base64 data URI. Plays on:
- Demo mode activation (5-click logo)
- Beam button explosion (10s hold)

## Technical Notes

- Single `index.html` file, no build tools
- All vanilla JS/CSS
- ESPN API integration unchanged
- Canvas API for explosion particles
- `touchstart`/`touchend` for hold detection on mobile
- Base64 audio for cowbell (no external files)
