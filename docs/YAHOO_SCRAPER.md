# Yahoo Scraper

## Source

Espinosa FFL still runs its actual league on Yahoo — draft, scoring, and the season itself all happen there. The Clubhouse's historical archive (Trophy Room, Locker Room, Rivalry Arena, Season Scrapbook) is built from that Yahoo data, not from anything decided in the Clubhouse's own Draft Room.

`scripts/fetch_yahoo_data.py` scrapes it (Playwright + BeautifulSoup, headless Chrome) and writes straight into `data/source/`. This script — and the Yahoo relationship it represents — is the one thing carried over from the retired Streamlit version of this project; everything else was rebuilt from scratch.

## Usage

```bash
pip install -r scripts/requirements.txt
playwright install chromium

python3 scripts/fetch_yahoo_data.py                  # all years in YEARS
python3 scripts/fetch_yahoo_data.py --year 2025       # single year
python3 scripts/fetch_yahoo_data.py --section draft   # one section only, any year
python3 scripts/normalize_league.py                   # regenerate app/data/league.json
```

Login is interactive on first run and saved to `.yahoo_cookies.json` (gitignored, never commit). If a saved session already exists for the "A New Dynasty" league under the same Yahoo account, it's reused automatically so you don't have to log in twice.

Yahoo rate-limits after roughly 40 rapid page loads — the scraper waits 3.5s between requests and auto-pauses 5 minutes on a "Request denied" response.

## New season checklist

Once a season wraps on Yahoo:

1. Add its year to `YEARS` and its `(game_code, league_id)` pair to `LEAGUE_IDS` in `scripts/fetch_yahoo_data.py`.
2. Run the scraper for that year.
3. Run `python3 scripts/normalize_league.py`.
4. Update `data/config/season-notes.csv` and `data/config/recent-events.csv` with that season's tagline, highlights, and any new bulletin items — these are hand-written, not derived from Yahoo.
5. `npm run build && npx wrangler deploy -c dist/server/wrangler.json`.

## What it writes, and what's actually used

The scraper mirrors its original (Streamlit-era) behavior and writes every section Yahoo exposes: `season_standings.csv`, `draft_picks.csv`, `weekly_matchups.csv`, `playoff_games.csv`, `season_managers.csv`, `season_trades.csv`, `league_settings.csv`. `scripts/normalize_league.py` only reads `draft_picks.csv`, `weekly_matchups.csv`, `playoff_games.csv`, and `league_settings.csv` — standings are computed live from matchups (Yahoo's own standings export has a known column-shift bug), and manager/trade data isn't part of the Clubhouse's story pages. The extra files are harmless to have on disk; `season_managers.csv` specifically is gitignored because it contains real email addresses.
