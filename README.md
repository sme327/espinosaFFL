# Espinosa FFL Clubhouse

The family's "Real Stadium" at **[espinosaFFL.sme327.com](https://espinosaFFL.sme327.com)** — a light, picture-first layer of family fun *around* our Yahoo league, never a second fantasy platform. Five family slots: Shawn (commissioner), Jennifer, Daphne, Elliot, and Wyatt (future manager, seat reserved).

Next.js (via [vinext](https://www.npmjs.com/package/vinext)) on Cloudflare Workers, with D1 (`espinosa-ffl-clubhouse`) for live state. The design contracts live in [`docs/`](docs/) — start with `REAL_STADIUM_CONCEPT.md`.

## The rooms

| Route | Room |
| --- | --- |
| `/` | Clubhouse entrance, reigning champion, trophy shelf |
| `/champions` | Trophy Room — every title since 2023 |
| `/seasons` | Scrapbook — standings, brackets, draft-day history per season |
| `/managers` | Locker Room — career stats for the whole family |
| `/rivalries` | Rivalry Arena — all six head-to-heads |
| `/weekly` | Tuesday-to-Tuesday Family Picks (predictions with confidence faces) |
| `/achievements` | Achievement Wall — computed history + commissioner-awarded badges |
| `/draft` | Family Draft Room (`/draft/pick` per-device seat, `/draft/room` shared big board) |

The 2026 family draft was completed on this system on **2026-09-07** — 28 picks, snake order Elliot → Shawn → Jennifer → Daphne, every pick made by its own manager. The full board lives at `/draft/room`.

## Commissioner playbook

Identity is tap-your-name — no PINs, by family decision. Turn order and corrections are still enforced server-side.

```bash
# Each week: mirror the real Yahoo pairings onto the prediction board
npm run weekly:matchups -- --pairs shawn:jennifer,daphne:elliot --featured shawn:jennifer --apply
#   (per-matchup early lock: --lock daphne:elliot=2026-09-10T19:15:00-05:00)

# Award a badge on the Achievement Wall (add --revoke to take one back)
npm run wall:award -- --achievement helping_hand --manager daphne --note "The story" --apply

# Next season's draft: set draftOrder/rosterSlots in data/config/draft-seasons.json, then
python3 scripts/seed_family_draft.py --reset   # refuses once real picks exist
npx wrangler d1 execute espinosa-ffl-clubhouse --remote --file data/draft/seed-2026.sql
```

## Data pipelines

- `npm run data:build` — normalize the scraped Yahoo league history (`scripts/normalize_league.py`).
- `npm run draft:players` — build the family player pool from the serious Draft App's Yahoo export (see `docs/PLAYER_DATA.md`).
- `npm run draft:images` — download player headshots + NFL logos into `public/` (Sleeper's public dump, matched by Yahoo ID) so draft day never depends on an outside CDN.
- `npm run wall:seed` — load the badge catalog from `data/config/achievements.json` into D1.
- `scripts/fetch_yahoo_data.py` — the Yahoo scraper feeding `data/source/` (see `docs/YAHOO_SCRAPER.md`).

## Develop, test, deploy

```bash
npm run dev        # local dev on a miniflare D1 (.wrangler/state/) — seed it with the same SQL files
npm test           # typecheck + build + node --test (renders real pages)
npm run build && npx wrangler deploy --config dist/server/wrangler.json
```

The D1 schema lives in `db/schema.ts` with mirror migrations in `drizzle/`; all seed SQL is idempotent and never touches recorded picks, predictions, or awards.
