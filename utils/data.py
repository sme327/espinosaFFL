"""Central data loading and derived metrics for Espinosa FFL."""
from __future__ import annotations
import pandas as pd
import streamlit as st
from pathlib import Path
from itertools import combinations

DATA_DIR = Path(__file__).parent.parent / "data"

LEAGUE_NAME     = "Espinosa FFL"
LEAGUE_SUBTITLE = "Family Fantasy Football"
FOUNDED         = 2023
CURRENT_SEASON  = 2025

# ── MANAGER IDENTITY ────────────────────────────────────────────────────────

# Yahoo manager key → display name
MANAGER_DISPLAY: dict[str, str] = {
    "shawnCommissioner": "Shawn",
    "Iosue":             "Jennifer",
    "Daphne":            "Daphne",
    "elliot":            "Elliot",
}

# Team name → manager display name (same team names every season in this league)
TEAM_TO_MANAGER: dict[str, str] = {
    "dad will win":    "Shawn",
    "Marvelous Mamma": "Jennifer",
    "Daphne's Magic":  "Daphne",
    "Pinkie pink 🏈":  "Elliot",
}

MANAGER_TO_TEAM: dict[str, str] = {v: k for k, v in TEAM_TO_MANAGER.items()}

# Each manager owns a color used throughout the app
MANAGER_COLORS: dict[str, str] = {
    "Shawn":    "#1F5E3B",  # Packers Green
    "Jennifer": "#002244",  # Seahawks Navy
    "Daphne":   "#0A5EA8",  # Seahawks Blue
    "Elliot":   "#E86AA6",  # Pink
    "Wyatt":    "#F28C28",  # Orange (future)
}

MANAGER_LIGHT_COLORS: dict[str, str] = {
    "Shawn":    "#E3F0E8",
    "Jennifer": "#E3E8F0",
    "Daphne":   "#E3EDF8",
    "Elliot":   "#FDE8F3",
    "Wyatt":    "#FEF0E3",
}

MANAGER_EMOJI: dict[str, str] = {
    "Shawn":    "🏈",
    "Jennifer": "⭐",
    "Daphne":   "✨",
    "Elliot":   "🩷",
    "Wyatt":    "🌟",
}

MANAGER_ORDER = ["Shawn", "Jennifer", "Daphne", "Elliot"]

# All head-to-head pairs
RIVALRY_PAIRS: list[tuple[str, str]] = list(combinations(MANAGER_ORDER, 2))

# ── NARRATIVE CONTENT ────────────────────────────────────────────────────────

SEASON_NOTES: dict[int, dict] = {
    2023: {
        "tagline":    "The inaugural season. Dad said he'd win. He was right.",
        "highlights": [
            "Shawn went 12–3, the best regular season record at the time.",
            "Daphne made it to the championship game as a first-year player.",
            "Jennifer upset Dad in Week 2 — a sign of things to come.",
        ],
    },
    2024: {
        "tagline":    "The ultimate comeback. Jennifer wins by 0.2 points.",
        "highlights": [
            "Jennifer finished 5–10 in the regular season (last place among playoff seeds) — then won it all.",
            "The championship margin: 0.2 points. The closest finish in league history.",
            "Shawn came within a whisper of back-to-back titles.",
        ],
    },
    2025: {
        "tagline":    "Daphne's year... until it wasn't. Elliot sweeps the playoffs.",
        "highlights": [
            "Daphne went 13–2 — the best regular season record in league history.",
            "Jennifer went 2–13 in the regular season and still reached the championship.",
            "Elliot entered the playoffs as the 3-seed and never looked back.",
        ],
    },
}

CHAMPIONSHIP_TAGLINES: dict[int, str] = {
    2023: "Dad said he'd win. He wasn't wrong.",
    2024: "Dead last in August. Champion in January.",
    2025: "The 3-seed who silenced everyone.",
}

CLUBHOUSE_QUOTES = [
    "Trash talk is our love language.",
    "No crying after fantasy losses.",
    "Draft first. Panic later.",
    "The trophy has found a new home every year.",
    "Daphne hasn't won yet. Keep watching.",
    "Jennifer wins quietly. Then wins loudly.",
    "Elliot plays it cool. And wins.",
    "Dad will win... eventually.",
    "Every week is a rivalry week.",
    "This is family. The standings are personal.",
    "Wyatt is scouting from the sidelines.",
    "The championship confetti has fallen.",
]

RECENT_EVENTS = [
    ("🏆", "Elliot wins the 2025 Championship (118.4 – 80.8 over Jennifer)"),
    ("😤", "Daphne goes 13–2 in the regular season — then loses to Jennifer in the playoffs"),
    ("⚡", "Jennifer goes 2–13 and still reaches the championship game"),
    ("📅", "2026 season coming soon — Wyatt is watching closely"),
]

# ── DATA LOADING ─────────────────────────────────────────────────────────────

@st.cache_data
def load_all() -> dict[str, pd.DataFrame]:
    files = {
        "standings":       "season_standings.csv",
        "draft":           "draft_picks.csv",
        "matchups":        "weekly_matchups.csv",
        "playoffs":        "playoff_games.csv",
        "season_managers": "season_managers.csv",
        "league_settings": "league_settings.csv",
    }
    result = {}
    for key, fname in files.items():
        path = DATA_DIR / fname
        if path.exists():
            result[key] = pd.read_csv(path)
    return result


def get_regular_season_matchups() -> pd.DataFrame:
    """Weeks 1–15 only (playoffs are weeks 16–17)."""
    data = load_all()
    m = data.get("matchups", pd.DataFrame())
    if m.empty:
        return pd.DataFrame()
    return m[m["week"] <= 15].copy()


# ── CHAMPIONS ────────────────────────────────────────────────────────────────

def get_champions() -> pd.DataFrame:
    """One row per season. Winner derived from scores (winner column is empty in CSV)."""
    data = load_all()
    playoffs = data.get("playoffs", pd.DataFrame())
    if playoffs.empty:
        return pd.DataFrame()
    finals = playoffs[playoffs["game_type"] == "final"].copy()
    rows = []
    for _, row in finals.iterrows():
        s1, s2 = float(row["score_1"]), float(row["score_2"])
        if s1 > s2:
            ct, cs, rt, rs = row["team_1"], s1, row["team_2"], s2
        else:
            ct, cs, rt, rs = row["team_2"], s2, row["team_1"], s1
        rows.append({
            "season":            int(row["season"]),
            "champion_team":     ct,
            "champion_manager":  TEAM_TO_MANAGER.get(ct, ct),
            "champion_score":    round(cs, 1),
            "runner_up_team":    rt,
            "runner_up_manager": TEAM_TO_MANAGER.get(rt, rt),
            "runner_up_score":   round(rs, 1),
            "margin":            round(abs(cs - rs), 2),
        })
    return pd.DataFrame(rows).sort_values("season").reset_index(drop=True)


# ── STANDINGS ────────────────────────────────────────────────────────────────

def get_season_standings(season: int) -> pd.DataFrame:
    """Regular season standings (weeks 1–15) computed from matchup data."""
    rs = get_regular_season_matchups()
    if rs.empty:
        return pd.DataFrame()
    s = rs[rs["season"] == season]
    records = []
    for team in s["team_name"].unique():
        tm = s[s["team_name"] == team]
        wins   = int((tm["result"] == "Win").sum())
        losses = int((tm["result"] == "Loss").sum())
        pf     = round(float(tm["team_score"].sum()), 1)
        pa     = round(float(tm["opponent_score"].sum()), 1)
        records.append({
            "team_name": team,
            "manager":   TEAM_TO_MANAGER.get(team, team),
            "wins":      wins,
            "losses":    losses,
            "pf":        pf,
            "pa":        pa,
            "win_pct":   round(wins / max(wins + losses, 1), 3),
        })
    df = (
        pd.DataFrame(records)
        .sort_values(["wins", "pf"], ascending=False)
        .reset_index(drop=True)
    )
    df.insert(0, "rank", range(1, len(df) + 1))
    return df


def get_all_time_standings() -> pd.DataFrame:
    """Career regular season records across all seasons."""
    rs = get_regular_season_matchups()
    if rs.empty:
        return pd.DataFrame()
    records = []
    for manager in MANAGER_ORDER:
        team = MANAGER_TO_TEAM.get(manager, "")
        tm   = rs[rs["team_name"] == team]
        wins   = int((tm["result"] == "Win").sum())
        losses = int((tm["result"] == "Loss").sum())
        pf     = round(float(tm["team_score"].sum()), 1)
        records.append({
            "manager":  manager,
            "team":     team,
            "wins":     wins,
            "losses":   losses,
            "pf":       pf,
            "win_pct":  round(wins / max(wins + losses, 1), 3),
        })
    champs = get_champions()
    champ_counts = champs.groupby("champion_manager").size().to_dict()
    df = pd.DataFrame(records)
    df["championships"] = df["manager"].map(lambda m: champ_counts.get(m, 0))
    return df.sort_values(["championships", "wins"], ascending=False).reset_index(drop=True)


# ── MANAGER CAREER ───────────────────────────────────────────────────────────

def get_manager_career_stats(manager: str) -> dict:
    team = MANAGER_TO_TEAM.get(manager, "")
    rs   = get_regular_season_matchups()
    if rs.empty or not team:
        return {}

    tm = rs[rs["team_name"] == team]
    total_wins   = int((tm["result"] == "Win").sum())
    total_losses = int((tm["result"] == "Loss").sum())
    total_pf     = round(float(tm["team_score"].sum()), 1)
    avg_ppg      = round(float(tm["team_score"].mean()), 2) if not tm.empty else 0.0

    by_season = (
        tm.groupby("season")
        .apply(lambda g: pd.Series({
            "wins":   int((g["result"] == "Win").sum()),
            "losses": int((g["result"] == "Loss").sum()),
            "pf":     round(float(g["team_score"].sum()), 1),
            "ppg":    round(float(g["team_score"].mean()), 1),
        }))
        .reset_index()
    )

    champs = get_champions()
    champ_seasons  = champs[champs["champion_manager"]  == manager]["season"].tolist()
    runner_seasons = champs[champs["runner_up_manager"] == manager]["season"].tolist()

    best_week = None
    if not tm.empty:
        idx = tm["team_score"].idxmax()
        best_week = tm.loc[idx]

    return {
        "manager":          manager,
        "team":             team,
        "total_wins":       total_wins,
        "total_losses":     total_losses,
        "win_pct":          round(total_wins / max(total_wins + total_losses, 1), 3),
        "total_pf":         total_pf,
        "avg_ppg":          avg_ppg,
        "seasons":          by_season,
        "championships":    champ_seasons,
        "runner_ups":       runner_seasons,
        "championship_count": len(champ_seasons),
        "best_week":        best_week,
    }


# ── RIVALRIES ────────────────────────────────────────────────────────────────

def get_rivalry_stats(manager_a: str, manager_b: str) -> dict:
    """Full head-to-head stats including regular season and playoff splits."""
    team_a = MANAGER_TO_TEAM.get(manager_a, "")
    team_b = MANAGER_TO_TEAM.get(manager_b, "")

    rs = get_regular_season_matchups()
    # Use only manager_a's perspective to avoid double-counting
    games = rs[(rs["team_name"] == team_a) & (rs["opponent"] == team_b)].copy()

    rs_a_wins = int((games["result"] == "Win").sum())
    rs_b_wins = int((games["result"] == "Loss").sum())

    # Playoff meetings
    data      = load_all()
    playoffs  = data.get("playoffs", pd.DataFrame())
    po_meetings: list[dict] = []
    po_a_wins = po_b_wins = 0

    if not playoffs.empty:
        for _, row in playoffs.iterrows():
            t1, t2 = str(row["team_1"]), str(row["team_2"])
            if not ({t1, t2} == {team_a, team_b}):
                continue
            s1, s2 = float(row["score_1"]), float(row["score_2"])
            winner_team = t1 if s1 > s2 else t2
            winner_mgr  = TEAM_TO_MANAGER.get(winner_team, winner_team)
            score_a = s1 if t1 == team_a else s2
            score_b = s2 if t1 == team_a else s1
            po_meetings.append({
                "season":  int(row["season"]),
                "round":   row["game_type"],
                "score_a": round(score_a, 1),
                "score_b": round(score_b, 1),
                "winner":  winner_mgr,
            })
            if winner_mgr == manager_a:
                po_a_wins += 1
            else:
                po_b_wins += 1

    # Biggest wins / closest game (regular season)
    biggest_a_win = biggest_b_win = closest_game = None
    if not games.empty:
        games = games.copy()
        games["margin"] = games["team_score"] - games["opponent_score"]

        a_wins = games[games["result"] == "Win"]
        if not a_wins.empty:
            r = a_wins.loc[a_wins["margin"].idxmax()]
            biggest_a_win = {
                "score_a": r["team_score"], "score_b": r["opponent_score"],
                "week": int(r["week"]), "season": int(r["season"]),
            }

        b_wins = games[games["result"] == "Loss"]
        if not b_wins.empty:
            r = b_wins.loc[b_wins["margin"].idxmin()]
            biggest_b_win = {
                "score_a": r["team_score"], "score_b": r["opponent_score"],
                "week": int(r["week"]), "season": int(r["season"]),
            }

        r = games.loc[games["margin"].abs().idxmin()]
        closest_game = {
            "score_a": r["team_score"], "score_b": r["opponent_score"],
            "week": int(r["week"]), "season": int(r["season"]),
        }

    # Current reg-season streak
    streak_holder = streak_count = None
    if not games.empty:
        sorted_games = games.sort_values(["season", "week"])
        last = sorted_games.iloc[-1]
        streak_holder = manager_a if last["result"] == "Win" else manager_b
        streak_count  = 0
        for _, g in sorted_games.iloc[::-1].iterrows():
            winner = manager_a if g["result"] == "Win" else manager_b
            if winner == streak_holder:
                streak_count += 1
            else:
                break

    return {
        "manager_a":     manager_a,
        "manager_b":     manager_b,
        "color_a":       MANAGER_COLORS.get(manager_a, "#0A5EA8"),
        "color_b":       MANAGER_COLORS.get(manager_b, "#E86AA6"),
        "light_a":       MANAGER_LIGHT_COLORS.get(manager_a, "#E3EDF8"),
        "light_b":       MANAGER_LIGHT_COLORS.get(manager_b, "#FDE8F3"),
        "emoji_a":       MANAGER_EMOJI.get(manager_a, "🏈"),
        "emoji_b":       MANAGER_EMOJI.get(manager_b, "🏈"),
        "rs_a_wins":     rs_a_wins,
        "rs_b_wins":     rs_b_wins,
        "po_a_wins":     po_a_wins,
        "po_b_wins":     po_b_wins,
        "total_a_wins":  rs_a_wins + po_a_wins,
        "total_b_wins":  rs_b_wins + po_b_wins,
        "po_meetings":   po_meetings,
        "biggest_a_win": biggest_a_win,
        "biggest_b_win": biggest_b_win,
        "closest_game":  closest_game,
        "streak_holder": streak_holder,
        "streak_count":  streak_count,
    }


def get_all_rivalries() -> list[dict]:
    return [get_rivalry_stats(a, b) for a, b in RIVALRY_PAIRS]


# ── PLAYOFFS ─────────────────────────────────────────────────────────────────

def get_season_playoffs(season: int) -> pd.DataFrame:
    """All playoff games for a season with derived winner column."""
    data = load_all()
    playoffs = data.get("playoffs", pd.DataFrame())
    if playoffs.empty:
        return pd.DataFrame()
    s = playoffs[playoffs["season"] == season].copy()
    s["winner_team"] = s.apply(
        lambda r: r["team_1"] if float(r["score_1"]) > float(r["score_2"]) else r["team_2"],
        axis=1,
    )
    s["winner_manager"] = s["winner_team"].map(TEAM_TO_MANAGER)
    s["loser_team"] = s.apply(
        lambda r: r["team_2"] if float(r["score_1"]) > float(r["score_2"]) else r["team_1"],
        axis=1,
    )
    s["score_1"] = s["score_1"].astype(float)
    s["score_2"] = s["score_2"].astype(float)
    return s.reset_index(drop=True)
