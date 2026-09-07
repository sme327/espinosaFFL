#!/usr/bin/env python3
"""Create (or update) one week of family matchups for the prediction board.

The commissioner mirrors the real Yahoo pairings each week:

    python3 scripts/seed_weekly_matchups.py --pairs shawn:jennifer,daphne:elliot \
        --featured shawn:jennifer --apply

Defaults: the current Tuesday-to-Tuesday week, and every matchup locks at
noon Chicago time on that week's Sunday. A matchup with an earlier game
(Thursday night, etc.) can lock sooner:

    --lock daphne:elliot=2026-09-10T19:15:00-05:00

Re-running the same week updates lock times and the featured matchup;
saved predictions are never touched.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CYCLE = json.loads((ROOT / "data" / "config" / "weekly-cycle.json").read_text(encoding="utf-8"))
MANAGERS_CSV = ROOT / "data" / "config" / "managers.csv"
DATABASE = "espinosa-ffl-clubhouse"
CHICAGO = timezone(timedelta(hours=-5))  # CDT; close enough for family lock times
FINAL_FAMILY_WEEK = 17


def sql_text(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def season_start(season: int) -> datetime:
    start = CYCLE.get("seasonStartTuesdays", {}).get(str(season))
    if not start:
        raise SystemExit(f"No seasonStartTuesdays entry for {season} in weekly-cycle.json")
    return datetime.fromisoformat(f"{start}T00:00:00").replace(tzinfo=CHICAGO)


def current_week(season: int) -> int:
    week = (datetime.now(CHICAGO) - season_start(season)).days // 7 + 1
    return min(max(week, 1), FINAL_FAMILY_WEEK)


def parse_pair(raw: str, managers: set[str]) -> tuple[str, str]:
    parts = [part.strip() for part in raw.split(":")]
    if len(parts) != 2 or parts[0] == parts[1] or any(part not in managers for part in parts):
        raise SystemExit(f"Bad pair '{raw}': expected two different manager IDs from {sorted(managers)}")
    return parts[0], parts[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--season", type=int, default=None)
    parser.add_argument("--week", type=int, default=None)
    parser.add_argument("--pairs", required=True, help="Comma-separated manager pairs, e.g. shawn:jennifer,daphne:elliot")
    parser.add_argument("--featured", default=None, help="The Game of the Week pair, e.g. shawn:jennifer")
    parser.add_argument("--lock", action="append", default=[], metavar="PAIR=ISO", help="Per-matchup lock override, e.g. daphne:elliot=2026-09-10T19:15:00-05:00")
    parser.add_argument("--apply", action="store_true", help="Run the SQL against the remote D1 database via wrangler")
    args = parser.parse_args()

    season = args.season or max(int(year) for year in CYCLE.get("seasonStartTuesdays", {"0": None}) if CYCLE["seasonStartTuesdays"][year])
    week = args.week or current_week(season)
    if not 1 <= week <= FINAL_FAMILY_WEEK:
        raise SystemExit(f"Week must be 1-{FINAL_FAMILY_WEEK}")

    managers = {row["id"] for row in csv.DictReader(MANAGERS_CSV.open(encoding="utf-8"))}
    pairs = [parse_pair(raw, managers) for raw in args.pairs.split(",") if raw.strip()]
    if not pairs:
        raise SystemExit("At least one pair is required")
    used = [manager for pair in pairs for manager in pair]
    if len(set(used)) != len(used):
        raise SystemExit("A manager can only appear in one matchup per week")

    featured = parse_pair(args.featured, managers) if args.featured else None
    if featured and featured not in pairs and (featured[1], featured[0]) not in pairs:
        raise SystemExit("--featured must be one of the --pairs")

    default_lock = (season_start(season) + timedelta(weeks=week - 1, days=5, hours=12)).isoformat()
    locks: dict[frozenset[str], str] = {}
    for override in args.lock:
        raw_pair, _, iso = override.partition("=")
        pair = parse_pair(raw_pair, managers)
        datetime.fromisoformat(iso)  # validate
        locks[frozenset(pair)] = iso

    statements = []
    for a, b in pairs:
        lock_at = locks.get(frozenset((a, b)), default_lock)
        is_featured = 1 if featured and frozenset(featured) == frozenset((a, b)) else 0
        statements.append(
            "INSERT INTO weekly_matchups (id, season, week, manager_a_id, manager_b_id, locks_at, featured) "
            f"VALUES ({sql_text(f'wk-{season}-{week}-{a}-{b}')}, {season}, {week}, {sql_text(a)}, {sql_text(b)}, {sql_text(lock_at)}, {is_featured}) "
            "ON CONFLICT(season, week, manager_a_id, manager_b_id) DO UPDATE SET "
            "locks_at = excluded.locks_at, featured = excluded.featured, updated_at = CURRENT_TIMESTAMP;"
        )
        print(f"Week {week}: {a} vs {b}" + (" ⚔️ Game of the Week" if is_featured else "") + f" · locks {lock_at}")

    output = ROOT / "data" / "weekly" / f"seed-{season}-week-{week}.sql"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(statements) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")

    if args.apply:
        subprocess.run(["npx", "wrangler", "d1", "execute", DATABASE, "--remote", "--file", str(output)], check=True, cwd=ROOT)
        print("Applied to the live clubhouse. ✅")
    else:
        print(f"Apply with:\n  npx wrangler d1 execute {DATABASE} --remote --file {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
