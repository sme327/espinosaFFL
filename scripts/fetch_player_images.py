#!/usr/bin/env python3
"""Download player headshots and NFL team logos for the family Draft Room.

Matches the family player pool against Sleeper's public NFL player dump
(free, no API key), downloads each matched player's headshot into
public/players/<season>/ and every NFL team logo into public/nfl/, then
stamps imageUrl on data/draft/players-2026.json. DEF entries use their
team logo as the picture. Unmatched players keep imageUrl null and fall
back to the initials card, so a missing photo can never hide a player.
"""

from __future__ import annotations

import argparse
import json
import re
import ssl
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:  # macOS framework Python ships without root certificates
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POOL = ROOT / "data" / "draft" / "players-2026.json"
DEFAULT_SLEEPER_CACHE = ROOT / "data" / "source" / "sleeper-players-nfl.json"
SLEEPER_PLAYERS_URL = "https://api.sleeper.app/v1/players/nfl"
HEADSHOT_URL = "https://sleepercdn.com/content/nfl/players/{sleeper_id}.jpg"
TEAM_LOGO_URL = "https://sleepercdn.com/images/team_logos/nfl/{team}.png"
FANTASY_POSITIONS = {"QB", "RB", "WR", "TE", "K"}
NAME_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}
MIN_IMAGE_BYTES = 2000


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pool", default=str(DEFAULT_POOL))
    parser.add_argument("--sleeper-cache", default=str(DEFAULT_SLEEPER_CACHE))
    parser.add_argument("--refresh", action="store_true", help="Re-download the Sleeper player dump")
    return parser.parse_args()


def normalized_name(name: str) -> str:
    tokens = re.sub(r"[^a-z\s]", "", name.lower()).split()
    return "".join(token for token in tokens if token not in NAME_SUFFIXES)


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "espinosa-ffl-clubhouse family draft"})
    with urllib.request.urlopen(request, timeout=60, context=SSL_CONTEXT) as response:
        return response.read()


def load_sleeper_players(cache: Path, refresh: bool) -> dict:
    if refresh or not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(fetch_bytes(SLEEPER_PLAYERS_URL))
        print(f"Downloaded Sleeper player dump to {cache}")
    return json.loads(cache.read_text(encoding="utf-8"))


def build_matcher(sleeper: dict):
    """Return a function mapping a pool player to a Sleeper ID, or None."""
    by_yahoo: dict[str, str] = {}
    by_name_team: dict[tuple[str, str], list[str]] = {}
    by_name_position: dict[tuple[str, str], list[str]] = {}
    by_name_team_any: dict[tuple[str, str], list[str]] = {}
    for sleeper_id, row in sleeper.items():
        yahoo_id = row.get("yahoo_id")
        if yahoo_id is not None:
            by_yahoo.setdefault(str(yahoo_id), sleeper_id)
        name = normalized_name(row.get("full_name") or "")
        team = row.get("team")
        if not name or not team:
            continue
        by_name_team_any.setdefault((name, team), []).append(sleeper_id)
        if row.get("position") in FANTASY_POSITIONS:
            by_name_team.setdefault((name, team), []).append(sleeper_id)
            by_name_position.setdefault((name, row["position"]), []).append(sleeper_id)

    def match(player: dict) -> str | None:
        direct = by_yahoo.get(player["sourceId"])
        if direct:
            return direct
        name = normalized_name(player["name"])
        for candidates in (
            by_name_team.get((name, player["nflTeam"])),
            by_name_position.get((name, player["position"])),
            by_name_team_any.get((name, player["nflTeam"])),
        ):
            if candidates and len(candidates) == 1:
                return candidates[0]
        return None

    return match


# Sleeper serves PNGs behind .jpg URLs, so trust magic bytes, not the URL.
IMAGE_FORMATS = ((b"\xff\xd8", "jpg"), (b"\x89PNG", "png"), (b"RIFF", "webp"))


def existing_image(directory: Path, stem: str) -> Path | None:
    for _, extension in IMAGE_FORMATS:
        candidate = directory / f"{stem}.{extension}"
        if candidate.exists():
            return candidate
    return None


def download_image(url: str, directory: Path, stem: str) -> Path | None:
    already = existing_image(directory, stem)
    if already:
        return already
    try:
        payload = fetch_bytes(url)
    except OSError as error:
        print(f"  failed {url}: {error}")
        return None
    extension = next((ext for magic, ext in IMAGE_FORMATS if payload.startswith(magic)), None)
    if len(payload) < MIN_IMAGE_BYTES or not extension:
        print(f"  rejected {url}: not a usable image ({len(payload)} bytes)")
        return None
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / f"{stem}.{extension}"
    destination.write_bytes(payload)
    time.sleep(0.1)  # be polite to the free CDN
    return destination


def main() -> None:
    args = arguments()
    pool_path = Path(args.pool).expanduser().resolve()
    payload = json.loads(pool_path.read_text(encoding="utf-8"))
    season = payload["season"]
    players = payload["players"]
    match = build_matcher(load_sleeper_players(Path(args.sleeper_cache).expanduser().resolve(), args.refresh))

    headshot_dir = ROOT / "public" / "players" / str(season)
    logo_dir = ROOT / "public" / "nfl"

    teams = sorted({player["nflTeam"] for player in players})
    logo_count = sum(
        download_image(TEAM_LOGO_URL.format(team=team.lower()), logo_dir, team) is not None
        for team in teams
    )

    downloaded = 0
    unmatched: list[str] = []
    for player in players:
        if player["position"] == "DEF":
            logo = existing_image(logo_dir, player["nflTeam"])
            player["imageUrl"] = f"/nfl/{logo.name}" if logo else None
            continue
        sleeper_id = match(player)
        headshot = existing_image(headshot_dir, player["sourceId"])
        if not headshot and sleeper_id:
            headshot = download_image(HEADSHOT_URL.format(sleeper_id=sleeper_id), headshot_dir, player["sourceId"])
            if headshot:
                downloaded += 1
        if headshot:
            player["imageUrl"] = f"/players/{season}/{headshot.name}"
        else:
            player["imageUrl"] = None
            unmatched.append(f"#{player['overallRank']} {player['name']} ({player['position']} {player['nflTeam']})")

    payload["imagesUpdatedAt"] = datetime.now(timezone.utc).isoformat()
    pool_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    headshot_players = len([p for p in players if p["position"] != "DEF"])
    print(f"Team logos ready: {logo_count}/{len(teams)}")
    print(f"Player headshots ready: {downloaded}/{headshot_players}")
    if unmatched:
        print(f"No photo (initials fallback will show) for {len(unmatched)}:")
        for line in unmatched:
            print(f"  {line}")


if __name__ == "__main__":
    main()
