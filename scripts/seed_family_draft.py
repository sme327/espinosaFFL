#!/usr/bin/env python3
"""Generate the D1 seed SQL for a family draft season.

Reads data/config/draft-seasons.json, data/config/managers.csv, and the
player pool, then writes one SQL file to run with wrangler:

    python3 scripts/seed_family_draft.py --order shawn,jennifer,daphne,elliot
    npx wrangler d1 execute espinosa-ffl-clubhouse --remote --file data/draft/seed-2026.sql

The SQL is safe to re-run: managers and players are upserted (so image or
rank refreshes flow through), while the season, teams, and slots use
INSERT OR IGNORE so re-seeding can never reset a draft that is underway.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "config" / "draft-seasons.json"
MANAGERS_CSV = ROOT / "data" / "config" / "managers.csv"
# No PINs in this house: the column is required by the schema, not by the family.
TRUSTED_HOUSEHOLD_PIN_HASH = "trusted-household"


def sql_text(value: object) -> str:
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season", type=int, default=None, help="Defaults to the latest configured season")
    parser.add_argument("--order", default=None, help="Comma-separated manager IDs in draft-position order; defaults to the season's draftOrder in draft-seasons.json")
    parser.add_argument("--status", choices=["ready", "live"], default="ready")
    parser.add_argument("--output", default=None)
    parser.add_argument("--reset", action="store_true",
                        help="First remove the season, teams, and slots so a new draft order can apply. Refuses to run once any pick exists.")
    return parser.parse_args()


def main() -> None:
    args = arguments()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    drafts = config["drafts"]
    season = args.season or max(draft["season"] for draft in drafts)
    draft = next((d for d in drafts if d["season"] == season), None)
    if not draft:
        raise SystemExit(f"No draft configured for season {season}")

    order = [manager_id.strip() for manager_id in args.order.split(",") if manager_id.strip()] if args.order else list(draft.get("draftOrder", []))
    if not order:
        raise SystemExit("No draft order: pass --order or set draftOrder in draft-seasons.json")
    active = draft["activeManagerIds"]
    if sorted(order) != sorted(active):
        raise SystemExit(f"--order must contain exactly the active managers {active}, got {order}")
    if draft["rounds"] != len(draft["rosterSlots"]):
        raise SystemExit("Draft rounds must match the season's roster slots")

    managers = {row["id"]: row for row in csv.DictReader(MANAGERS_CSV.open(encoding="utf-8"))}
    for manager_id in active + draft["reservedManagerIds"]:
        if manager_id not in managers:
            raise SystemExit(f"Manager {manager_id} is missing from managers.csv")

    pool = json.loads((ROOT / "data" / "draft" / f"players-{season}.json").read_text(encoding="utf-8"))
    if pool["season"] != season or pool["playerCount"] < 100:
        raise SystemExit("Player pool looks wrong; rebuild it first")

    draft_id = f"family-{season}"
    statements: list[str] = ["PRAGMA defer_foreign_keys = on;"]

    if args.reset:
        # A recorded pick means the family draft has really happened; never erase it.
        guard = f"EXISTS (SELECT 1 FROM draft_picks_live WHERE draft_id = {sql_text(draft_id)})"
        # Trips the family_size CHECK constraint, aborting the whole batch, if picks exist.
        statements.append(
            "INSERT INTO draft_seasons (id, season, family_size, status, order_type, rounds, roster_slots_json, commissioner_manager_id) "
            f"SELECT 'reset-refused-picks-exist', -1, 0, 'planning', 'snake', 1, '[]', {sql_text(draft['commissionerManagerId'])} WHERE {guard};"
        )
        for table in ("draft_transitions", "draft_snapshots", "draft_events", "draft_slots", "draft_teams", "draft_seasons"):
            column = "id" if table == "draft_seasons" else "draft_id"
            statements.append(f"DELETE FROM {table} WHERE {column} = {sql_text(draft_id)} AND NOT {guard};")

    for manager_id, row in managers.items():
        is_active = manager_id in active
        statements.append(
            "INSERT INTO draft_managers (id, display_name, pin_hash, is_commissioner, active) "
            f"VALUES ({sql_text(manager_id)}, {sql_text(row['display_name'])}, {sql_text(TRUSTED_HOUSEHOLD_PIN_HASH)}, "
            f"{1 if manager_id == draft['commissionerManagerId'] else 0}, {1 if is_active else 0}) "
            "ON CONFLICT(id) DO UPDATE SET display_name = excluded.display_name, "
            "is_commissioner = excluded.is_commissioner, active = excluded.active, updated_at = CURRENT_TIMESTAMP;"
        )

    statements.append(
        "INSERT OR IGNORE INTO draft_seasons (id, season, family_size, status, order_type, rounds, roster_slots_json, commissioner_manager_id) "
        f"VALUES ({sql_text(draft_id)}, {season}, {config['familySize']}, {sql_text(args.status)}, {sql_text(draft['orderType'])}, "
        f"{draft['rounds']}, {sql_text(json.dumps(draft['rosterSlots']))}, {sql_text(draft['commissionerManagerId'])});"
    )

    team_ids = {}
    for position, manager_id in enumerate(order, start=1):
        team_id = f"team-{season}-{manager_id}"
        team_ids[manager_id] = team_id
        team_name = managers[manager_id]["team_name"] or managers[manager_id]["display_name"]
        statements.append(
            "INSERT OR IGNORE INTO draft_teams (id, draft_id, manager_id, team_name, draft_position, active) "
            f"VALUES ({sql_text(team_id)}, {sql_text(draft_id)}, {sql_text(manager_id)}, {sql_text(team_name)}, {position}, 1);"
        )

    overall = 0
    for round_number in range(1, draft["rounds"] + 1):
        round_order = list(reversed(order)) if draft["orderType"] == "snake" and round_number % 2 == 0 else order
        for pick_in_round, manager_id in enumerate(round_order, start=1):
            overall += 1
            statements.append(
                "INSERT OR IGNORE INTO draft_slots (id, draft_id, overall, round, pick_in_round, team_id, roster_slot) "
                f"VALUES ({sql_text(f'slot-{season}-{overall}')}, {sql_text(draft_id)}, {overall}, {round_number}, "
                f"{pick_in_round}, {sql_text(team_ids[manager_id])}, {sql_text(draft['rosterSlots'][round_number - 1])});"
            )

    for player in pool["players"]:
        statements.append(
            "INSERT INTO draft_players (id, season, source, source_id, name, position, nfl_team, bye_week, overall_rank, image_url) "
            f"VALUES ({sql_text(player['id'])}, {season}, {sql_text(player['source'])}, {sql_text(player['sourceId'])}, "
            f"{sql_text(player['name'])}, {sql_text(player['position'])}, {sql_text(player['nflTeam'])}, "
            f"{sql_text(player['byeWeek'])}, {sql_text(player['overallRank'])}, {sql_text(player['imageUrl'])}) "
            "ON CONFLICT(id) DO UPDATE SET name = excluded.name, position = excluded.position, nfl_team = excluded.nfl_team, "
            "bye_week = excluded.bye_week, overall_rank = excluded.overall_rank, image_url = excluded.image_url, updated_at = CURRENT_TIMESTAMP;"
        )

    output = Path(args.output) if args.output else ROOT / "data" / "draft" / f"seed-{season}.sql"
    output.write_text("\n".join(statements) + "\n", encoding="utf-8")
    print(f"Wrote {len(statements)} statements to {output}")
    print(f"Draft order: {', '.join(order)}  (snake)" if draft["orderType"] == "snake" else f"Draft order: {', '.join(order)}")
    print("Apply with:")
    print(f"  npx wrangler d1 execute espinosa-ffl-clubhouse --remote --file {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
