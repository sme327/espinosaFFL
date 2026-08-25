#!/usr/bin/env python3
"""Normalize a static 2026 Yahoo player export for the family Draft Room."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
# This repo lives at "<Fantasy Football Leagues>/Espinosa FFL Clubhouse/Clubhouse/";
# the serious draft app's player export is two levels up, in the IWNH league folder.
LEAGUES_DIR = ROOT.parents[1]
DEFAULT_SOURCE = LEAGUES_DIR / "Insert Witty Name Here" / "draft-room-2026" / "data" / "imports" / "yahoo-players-2026.json"
DEFAULT_OUTPUT = ROOT / "data" / "draft" / "players-2026.json"
POSITIONS = {"QB", "RB", "WR", "TE", "K", "DEF"}
MAX_PRESEASON_RANK = 350


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--max-rank", type=int, default=MAX_PRESEASON_RANK)
    return parser.parse_args()


def main() -> None:
    args = arguments()
    source = Path(args.source).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    raw_bytes = source.read_bytes()
    raw = json.loads(raw_bytes)
    if raw.get("season") != 2026 or not isinstance(raw.get("players"), list):
        raise ValueError("Expected a 2026 Yahoo player export")

    players = []
    seen_ids: set[int] = set()
    for row in raw["players"]:
        player_id = row.get("yahoo_player_id")
        rank = row.get("preseason_rank")
        position = row.get("position")
        if not isinstance(player_id, int) or player_id in seen_ids:
            continue
        if position not in POSITIONS or not isinstance(rank, int) or rank > args.max_rank:
            continue
        name = str(row.get("name", "")).strip()
        nfl_team = str(row.get("nfl_team", "")).strip().upper()
        if not name or not nfl_team:
            continue
        seen_ids.add(player_id)
        players.append({
            "id": f"yahoo:2026:{player_id}",
            "source": "yahoo-static-export",
            "sourceId": str(player_id),
            "name": name,
            "position": position,
            "nflTeam": nfl_team,
            "byeWeek": row.get("bye_week") if isinstance(row.get("bye_week"), int) else None,
            "overallRank": rank,
            "sourceUrl": row.get("source_url"),
            "imageUrl": None,
        })

    players.sort(key=lambda player: (player["overallRank"], player["name"]))
    if len(players) < 100:
        raise ValueError(f"Player pool is unexpectedly small: {len(players)}")

    payload = {
        "season": 2026,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceGeneratedAt": raw.get("generated_at"),
        "sourceSha256": hashlib.sha256(raw_bytes).hexdigest(),
        "maxPreseasonRank": args.max_rank,
        "playerCount": len(players),
        "players": players,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(players)} family draft players to {output}")


if __name__ == "__main__":
    main()
