# Espinosa Family Draft Room Specification

## Product boundary

The Draft Room serves one family of exactly five people. A season may activate four or five teams. It is intentionally small, picture-led, and easier than the serious twelve-team Draft App while retaining its reliability patterns.

Yahoo remains the official league system after the draft. The Draft Room only needs a clear final results section; it does not need an automated Yahoo transfer workflow.

## Reused reliability patterns

- One authoritative shared draft state
- Snake schedule generated from season configuration
- Tap-your-name manager sessions (trusted household — the family explicitly declined PINs)
- Only the current manager or commissioner can submit a pick
- Idempotent, concurrency-guarded pick saving
- Commissioner proxy pick and latest-pick correction
- Simple automatic refresh and device-reload recovery
- Append-only pick and correction history
- One durable state snapshot after each confirmed pick
- Shared Room View and personal Pick View

## Intentionally omitted complexity

- PINs, passwords, and login security of any kind (four people in one house)
- More than five teams
- Keepers and keeper costs
- Traded draft picks
- Private tier queues
- Manager prediction models
- In-draft grades or pick analysis (a playful post-draft family report card was added at the family's request after the 2026 draft — celebration, not statistics)
- Automated Yahoo roster entry
- Dense twelve-team board layouts
- Draft timers, countdowns, pause, and resume controls
- Elaborate external backup workflows

## Season configuration

Every draft season must explicitly define:

- Season
- Active manager IDs, containing four or five of the five permanent family IDs
- Draft position for every active manager
- Number of rounds
- Ordered roster slots
- Snake or linear order
- Draft status
- Commissioner manager ID

Roster sizes may grow in later seasons as the children get older. No current implementation may infer rounds from a permanent seven-round assumption.

Wyatt remains a full clubhouse member while inactive. Activating him adds his manager ID and draft position to that season's configuration; it does not create a sixth family slot.

## Draft experiences

Interface mode is presentation guidance, not an age label and not a permission boundary.

### Picture-assisted

- Adult-curated shortlist of two to four valid players
- Very large player pictures and NFL logos
- Tap to hear the name
- Large two-step confirmation
- Quiet commissioner assistance available

### Guided

- Pictures remain primary
- Position icons and short roster-needs prompts
- Favorites tray
- Three understandable recommendations
- Spoken names and minimal reading

### Strategy

- Search, rankings, position filters, bye weeks, roster needs, and favorites
- Simple value and balance explanations
- Same safe confirmation and turn rules as every other mode

## Shared Room View

- Current manager photo, team logo, and team color
- Visual snake path that works for four or five columns
- Latest pick and next manager
- Every developing roster
- Draft progress
- Large pick celebration
- No private favorites or recommendations

## Personal Pick View

- Available players with photos and reliable fallbacks
- Position and NFL-team filters
- Manager-specific presentation mode
- Favorites and roster needs
- Selection preview and explicit confirmation
- Clear waiting, current-picker, saving, and reconnected states

## Results

- Full board by round
- Results grouped by team
- Final rosters with player picture, name, position, NFL team, and overall pick
- Printable layout
- Simple copy or download
- Commissioner correction when the recorded result must be aligned with Yahoo

## Status

The 2026 family draft ran to completion on this system on 2026-09-07: 28 of 28 picks in snake order (Elliot, Shawn, Jennifer, Daphne), every pick made by its own manager, zero proxy picks or corrections needed.

## Release gates

- Complete four-team rehearsal on real family devices
- Reserved five-team configuration rehearsal
- Simultaneous-pick and duplicate-request tests
- Reconnect and stale-screen tests
- Commissioner correction and device-reload rehearsal
- Touch, keyboard, and reduced-motion review
