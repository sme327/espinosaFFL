# 2026 Family Draft Player Data

## Source

The Draft Room uses a static Yahoo player export already maintained by the serious Draft App. This is a draft-day player catalog, not the postponed live Yahoo clubhouse integration.

The family importer reads:

`../../insert witty name here/Draft App/data/imports/yahoo-players-2026.json`

It writes a smaller normalized pool to `data/draft/players-2026.json`.

## Included fields

- Stable Yahoo-derived player ID
- Player name
- Position
- NFL team abbreviation
- Bye week when available
- 2026 preseason rank
- Yahoo source page
- Optional image URL

Roster status and statistics from the serious league are intentionally excluded because they do not belong to the family league.

## Pool boundary

The default family pool includes ranked QB, RB, WR, TE, K, and DEF entries through preseason rank 350. This is much larger than a four- or five-team, seven-round draft while avoiding hundreds of irrelevant unranked rows.

## Refresh process

1. Refresh and verify the serious Draft App's Yahoo export.
2. Run `python3 scripts/build_family_player_pool.py` in the family clubhouse.
3. Review the reported player count and source checksum change.
4. Run the clubhouse tests.
5. Freeze the final pool shortly before the family draft.

The importer refuses the wrong season, duplicate IDs, a very small pool, invalid positions, blank names, and blank NFL teams.

## Pictures and team identity

Player headshots and NFL team logos are downloaded once by `scripts/fetch_player_images.py` (or `npm run draft:images`) into `public/players/<season>/` and `public/nfl/`, so draft day never depends on an outside CDN. The script matches pool players to Sleeper's free public player dump by Yahoo ID, then by suffix-stripped name plus team or position, and stamps `imageUrl` onto the pool JSON; `build_family_player_pool.py` re-stamps from the downloaded files, so rebuilding the pool never loses pictures. DEF entries use their team logo as the picture.

Player images remain optional. The player card always has a large position-colored fallback with the player's initials, and the NFL badge shows a readable abbreviation beside the logo. Missing imagery can therefore never hide a player or prevent a pick.
