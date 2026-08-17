import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source"
CONFIG = ROOT / "data/config"
OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "app/data/league.json"

FOUNDED = 2023
CURRENT_SEASON = 2026
FAMILY_SIZE = 5


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def to_bool(value: str) -> bool:
    return value.strip().casefold() == "true"


managers = []
for row in read_csv(CONFIG / "managers.csv"):
    managers.append({
        "id": row["id"],
        "name": row["display_name"],
        "teamName": row["team_name"] or None,
        "color": row["color"],
        "lightColor": row["light_color"],
        "emoji": row["emoji"],
        "order": int(row["order"]),
        "active": to_bool(row["active"]),
        "clubhouseMember": True,
        "photoPath": row["photo_path"] or None,
        "teamLogoPath": row["team_logo_path"] or None,
        "soundPath": row["sound_path"] or None,
        "celebration": row["celebration"] or None,
        "interfaceMode": row["interface_mode"] or None,
    })

seasons = []
for row in read_csv(CONFIG / "season-notes.csv"):
    highlights = [row[key] for key in ("highlight_1", "highlight_2", "highlight_3") if row.get(key)]
    seasons.append({
        "season": int(row["season"]),
        "tagline": row["tagline"],
        "highlights": highlights,
    })

recent_events = []
for row in sorted(read_csv(CONFIG / "recent-events.csv"), key=lambda item: int(item["order"])):
    recent_events.append({"icon": row["icon"], "text": row["text"]})

matchups = []
for row in read_csv(SOURCE / "weekly_matchups.csv"):
    matchups.append({
        "season": int(row["season"]),
        "week": int(row["week"]),
        "teamName": row["team_name"],
        "opponent": row["opponent"],
        "result": row["result"],
        "teamScore": float(row["team_score"]),
        "opponentScore": float(row["opponent_score"]),
    })

playoffs = []
for row in read_csv(SOURCE / "playoff_games.csv"):
    playoffs.append({
        "season": int(row["season"]),
        "week": int(row["week"]),
        "round": int(row["round"]),
        "gameType": row["game_type"],
        "seed1": int(row["seed_1"]),
        "team1": row["team_1"],
        "score1": float(row["score_1"]),
        "seed2": int(row["seed_2"]),
        "team2": row["team_2"],
        "score2": float(row["score_2"]),
    })

draft_picks = []
for row in read_csv(SOURCE / "draft_picks.csv"):
    if row["player_name"] == "--empty--":
        continue
    draft_picks.append({
        "season": int(row["season"]),
        "round": int(row["round"]),
        "pickInRound": int(row["pick_in_round"]),
        "overallPick": int(row["overall_pick"]),
        "teamName": row["team_name"],
        "playerName": row["player_name"],
    })

league_settings = []
for row in read_csv(SOURCE / "league_settings.csv"):
    league_settings.append({
        "season": int(row["season"]),
        "numTeams": int(row["num_teams"]),
        "scoringType": row["scoring_type"],
        "draftType": row["draft_type"],
        "rosterSlots": row["roster_slots"],
        "divisions": row["divisions"],
        "waiverType": row["waiver_type"],
        "playoffTiebreaker": row["playoff_tiebreaker"],
    })


def validate() -> None:
    manager_ids = [manager["id"] for manager in managers]
    if len(manager_ids) != FAMILY_SIZE or len(set(manager_ids)) != FAMILY_SIZE:
        raise ValueError(f"Expected exactly {FAMILY_SIZE} unique Espinosa family members")

    active_managers = [manager for manager in managers if manager["active"]]
    if len(active_managers) not in (4, 5):
        raise ValueError("A season must support either four or five active family teams")

    known_teams = {manager["teamName"] for manager in managers if manager["teamName"]}
    for matchup in matchups:
        if matchup["teamName"] not in known_teams or matchup["opponent"] not in known_teams:
            raise ValueError(f"Unknown team in {matchup['season']} week {matchup['week']}")
        mirror = next((candidate for candidate in matchups if
            candidate["season"] == matchup["season"] and
            candidate["week"] == matchup["week"] and
            candidate["teamName"] == matchup["opponent"] and
            candidate["opponent"] == matchup["teamName"]), None)
        if not mirror:
            raise ValueError(f"Missing mirrored matchup in {matchup['season']} week {matchup['week']}")
        if mirror["teamScore"] != matchup["opponentScore"] or mirror["opponentScore"] != matchup["teamScore"]:
            raise ValueError(f"Mismatched mirrored score in {matchup['season']} week {matchup['week']}")

    for setting in league_settings:
        if setting["numTeams"] not in (4, 5):
            raise ValueError(f"Season {setting['season']} must have four or five teams")
        if not setting["rosterSlots"].strip():
            raise ValueError(f"Season {setting['season']} is missing its roster configuration")


validate()

payload = {
    "generatedFor": date.today().isoformat(),
    "leagueName": "Espinosa FFL",
    "leagueSubtitle": "Family Fantasy Football",
    "founded": FOUNDED,
    "currentSeason": CURRENT_SEASON,
    "familySize": FAMILY_SIZE,
    "managers": managers,
    "seasons": seasons,
    "recentEvents": recent_events,
    "matchups": matchups,
    "playoffs": playoffs,
    "draftPicks": draft_picks,
    "leagueSettings": league_settings,
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", encoding="utf-8") as output_file:
    json.dump(payload, output_file, ensure_ascii=False, indent=2)
    output_file.write("\n")

print(f"Wrote {OUTPUT} ({len(matchups)} matchups, {len(playoffs)} playoff games, {len(draft_picks)} draft picks)")
