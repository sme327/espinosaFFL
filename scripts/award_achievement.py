#!/usr/bin/env python3
"""Commissioner tool: grant (or revoke) an achievement badge on the wall.

    python3 scripts/award_achievement.py --achievement helping_hand --manager daphne \
        --note "Helped Elliot set his week 1 lineup" --apply

    python3 scripts/award_achievement.py --achievement helping_hand --manager daphne \
        --revoke --apply

Duplicate protection follows the fairness rules: one-time badges use the
season as their award key; repeatable badges default to today's date so
the same badge can be earned again another day (--key overrides).
Revoking marks the award revoked instead of deleting its history.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATABASE = "espinosa-ffl-clubhouse"


def sql_text(value: object) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--achievement", required=True)
    parser.add_argument("--manager", required=True)
    parser.add_argument("--season", type=int, default=None, help="Defaults to the current league season")
    parser.add_argument("--note", default=None, help="Short family story behind the award")
    parser.add_argument("--key", default=None, help="Award key for duplicate protection (see docstring for defaults)")
    parser.add_argument("--awarded-by", default="shawn")
    parser.add_argument("--revoke", action="store_true", help="Revoke this badge (matched by achievement, manager, and key) instead of granting it")
    parser.add_argument("--apply", action="store_true", help="Run the SQL against the remote D1 database via wrangler")
    args = parser.parse_args()

    config = json.loads((ROOT / "data" / "config" / "achievements.json").read_text(encoding="utf-8"))
    badge = next((item for item in config["achievements"] if item["id"] == args.achievement), None)
    if not badge:
        raise SystemExit(f"Unknown achievement '{args.achievement}'. Choose from: " + ", ".join(sorted(item["id"] for item in config["achievements"])))

    managers = {row["id"] for row in csv.DictReader((ROOT / "data" / "config" / "managers.csv").open(encoding="utf-8"))}
    if args.manager not in managers or args.awarded_by not in managers:
        raise SystemExit(f"Managers must be one of {sorted(managers)}")

    league = json.loads((ROOT / "app" / "data" / "league.json").read_text(encoding="utf-8"))
    season = args.season or league["currentSeason"]
    now = datetime.now(timezone.utc)
    award_key = args.key or (now.date().isoformat() if badge.get("repeatable") else str(season))

    if args.revoke:
        statement = (
            "UPDATE achievement_awards SET revoked_at = CURRENT_TIMESTAMP "
            f"WHERE achievement_id = {sql_text(args.achievement)} AND manager_id = {sql_text(args.manager)} "
            f"AND award_key = {sql_text(award_key)} AND revoked_at IS NULL;"
        )
        print(f"Revoking {badge['icon']} {badge['name']} from {args.manager} (key {award_key})")
    else:
        statement = (
            "INSERT OR IGNORE INTO achievement_awards (id, achievement_id, manager_id, season, award_key, awarded_by_manager_id, awarded_at, note) "
            f"VALUES ({sql_text(str(uuid.uuid4()))}, {sql_text(args.achievement)}, {sql_text(args.manager)}, {season}, "
            f"{sql_text(award_key)}, {sql_text(args.awarded_by)}, {sql_text(now.isoformat())}, {sql_text(args.note)});"
        )
        print(f"Awarding {badge['icon']} {badge['name']} to {args.manager} for {season} (key {award_key})")
        if badge["awardMethod"] == "automatic":
            print("Note: this badge is normally earned automatically; awarding by hand is a historical backfill.")

    if args.apply:
        subprocess.run(["npx", "wrangler", "d1", "execute", DATABASE, "--remote", "--command", statement], check=True, cwd=ROOT)
        print("The wall is updated. ✅")
    else:
        print("SQL:\n  " + statement)
        print("Re-run with --apply to update the live clubhouse.")


if __name__ == "__main__":
    main()
