#!/usr/bin/env python3
"""Load the achievement badge catalog from achievements.json into D1.

Idempotent: definitions are upserted by ID, so edits to names, icons, or
descriptions flow through on re-run. Awards are never touched.

    python3 scripts/seed_achievements.py --apply
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATABASE = "espinosa-ffl-clubhouse"


def sql_text(value: object) -> str:
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Run the SQL against the remote D1 database via wrangler")
    args = parser.parse_args()

    config = json.loads((ROOT / "data" / "config" / "achievements.json").read_text(encoding="utf-8"))
    statements = []
    for order, badge in enumerate(config["achievements"], start=1):
        statements.append(
            "INSERT INTO achievement_definitions (id, name, description, icon, category, award_method, repeatable, rule_key, active, sort_order) "
            f"VALUES ({sql_text(badge['id'])}, {sql_text(badge['name'])}, {sql_text(badge['description'])}, {sql_text(badge['icon'])}, "
            f"{sql_text(badge['category'])}, {sql_text(badge['awardMethod'])}, {1 if badge.get('repeatable') else 0}, {sql_text(badge.get('ruleKey'))}, 1, {order}) "
            "ON CONFLICT(id) DO UPDATE SET name = excluded.name, description = excluded.description, icon = excluded.icon, "
            "category = excluded.category, award_method = excluded.award_method, repeatable = excluded.repeatable, "
            "rule_key = excluded.rule_key, active = excluded.active, sort_order = excluded.sort_order, updated_at = CURRENT_TIMESTAMP;"
        )

    output = ROOT / "data" / "config" / "seed-achievements.sql"
    output.write_text("\n".join(statements) + "\n", encoding="utf-8")
    print(f"Wrote {len(statements)} badge definitions to {output.relative_to(ROOT)}")

    if args.apply:
        subprocess.run(["npx", "wrangler", "d1", "execute", DATABASE, "--remote", "--file", str(output)], check=True, cwd=ROOT)
        print("Applied to the live clubhouse. ✅")
    else:
        print(f"Apply with:\n  npx wrangler d1 execute {DATABASE} --remote --file {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
