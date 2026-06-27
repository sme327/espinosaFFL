"""Locker Room — manager profiles and career stats."""
from __future__ import annotations
import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_LIGHT_COLORS, MANAGER_EMOJI, MANAGER_ORDER,
    MANAGER_TO_TEAM, RIVALRY_PAIRS,
    get_manager_career_stats, get_champions, get_rivalry_stats,
    get_all_time_standings,
)
from utils.styles import (
    inject_css, render_nav, render_page_header,
    section_header, manager_avatar_html, html_table, md_html,
)

st.set_page_config(
    page_title="Locker Room · Espinosa FFL",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("manager_profiles")
render_page_header(
    "👥 THE CLUBHOUSE",
    "Locker Room",
    "Every manager. Every season. Every rivalry.",
)

# ── MANAGER CARDS ─────────────────────────────────────────────────────────

section_header("Meet the Managers", "The Espinosa FFL roster")

cols = st.columns(len(MANAGER_ORDER), gap="medium")

all_stats = {m: get_manager_career_stats(m) for m in MANAGER_ORDER}
champions = get_champions()

for col, manager in zip(cols, MANAGER_ORDER):
    stats = all_stats[manager]
    color = MANAGER_COLORS.get(manager, "#0A5EA8")
    emoji = MANAGER_EMOJI.get(manager, "🏈")
    team  = MANAGER_TO_TEAM.get(manager, "")
    champ_ct   = stats.get("championship_count", 0)
    trophy_str = "🏆 " * champ_ct if champ_ct else "Still chasing..."
    champ_yrs  = stats.get("championships", [])
    runner_yrs = stats.get("runner_ups", [])
    wins       = stats.get("total_wins", 0)
    losses     = stats.get("total_losses", 0)
    ppg        = stats.get("avg_ppg", 0.0)
    win_pct    = stats.get("win_pct", 0.0)

    best_week  = stats.get("best_week")
    best_wk_txt = ""
    if best_week is not None:
        try:
            best_wk_txt = f"{float(best_week['team_score']):.1f} pts (Wk {int(best_week['week'])}, {int(best_week['season'])})"
        except Exception:
            pass

    champ_yr_txt   = ", ".join(str(y) for y in champ_yrs) if champ_yrs else "—"
    runner_yr_txt  = ", ".join(str(y) for y in runner_yrs) if runner_yrs else "—"

    runner_html = (
        f"<div style='margin-top:0.4rem;'><div style='font-family:Nunito,sans-serif;font-size:0.72rem;color:#AAA;font-weight:800;text-transform:uppercase;letter-spacing:1px;'>Runner-Up</div><div style='font-family:Nunito,sans-serif;font-size:0.82rem;color:#888;font-weight:700;margin-top:0.1rem;'>{runner_yr_txt}</div></div>"
        if runner_yrs else ""
    )
    bestweek_html = (
        f"<div style='margin-top:0.4rem;'><div style='font-family:Nunito,sans-serif;font-size:0.72rem;color:#AAA;font-weight:800;text-transform:uppercase;letter-spacing:1px;'>Best Single Week</div><div style='font-family:Nunito,sans-serif;font-size:0.78rem;color:#555;font-weight:700;margin-top:0.1rem;'>{best_wk_txt}</div></div>"
        if best_wk_txt else ""
    )
    with col:
        md_html(
            f'<div class="hq-profile-card" style="border-top-color:{color};">'
            f'<div class="hq-avatar" style="background:{color};width:76px;height:76px;font-size:2.3rem;margin:0 auto 0.7rem;border-radius:50%;display:flex;align-items:center;justify-content:center;">{emoji}</div>'
            f'<div class="hq-profile-name" style="color:{color};">{manager}</div>'
            f'<div class="hq-profile-team">"{team}"</div>'
            f'<div class="hq-stat-grid">'
            f'<div class="hq-stat-box"><div class="hq-stat-value" style="color:{color};">{wins}</div><div class="hq-stat-label">Career Wins</div></div>'
            f'<div class="hq-stat-box"><div class="hq-stat-value" style="color:{color};">{int(win_pct*100)}%</div><div class="hq-stat-label">Win Rate</div></div>'
            f'<div class="hq-stat-box"><div class="hq-stat-value" style="color:{color};">{champ_ct}</div><div class="hq-stat-label">Championships</div></div>'
            f'<div class="hq-stat-box"><div class="hq-stat-value" style="color:{color};">{ppg:.0f}</div><div class="hq-stat-label">Avg PPG</div></div>'
            f'</div>'
            f'<div style="margin-top:0.75rem;border-top:1px solid #EEE8E0;padding-top:0.6rem;">'
            f'<div style="font-family:\'Nunito\',sans-serif;font-size:0.72rem;color:#AAA;font-weight:800;text-transform:uppercase;letter-spacing:1px;">Titles</div>'
            f'<div style="font-family:\'Nunito\',sans-serif;font-size:0.82rem;color:#444;font-weight:700;margin-top:0.1rem;">{champ_yr_txt}</div>'
            f'</div>'
            f'{runner_html}'
            f'{bestweek_html}'
            f'</div>'
        )

# ── SEASON-BY-SEASON ──────────────────────────────────────────────────────

md_html("<div style='margin-top:1.5rem'></div>")
section_header("Year-by-Year Records", "Regular season (weeks 1–15) for each manager")

# Build a comparison table: seasons as columns, managers as rows
seasons_data: dict[str, dict] = {}
for manager in MANAGER_ORDER:
    stats = all_stats[manager]
    by_season = stats.get("seasons")
    if by_season is not None and not by_season.empty:
        for _, row in by_season.iterrows():
            s   = int(row["season"])
            key = manager
            if key not in seasons_data:
                seasons_data[key] = {}
            seasons_data[key][s] = f"{int(row['wins'])}–{int(row['losses'])}"

# Find all seasons
all_seasons = sorted(
    {s for mgr_data in seasons_data.values() for s in mgr_data.keys()}
)

table_rows = []
for manager in MANAGER_ORDER:
    color = MANAGER_COLORS.get(manager, "#0A5EA8")
    emoji = MANAGER_EMOJI.get(manager, "🏈")
    row   = [(f'<span style="color:{color};font-weight:800;">{emoji} {manager}</span>', "")]
    for s in all_seasons:
        val = seasons_data.get(manager, {}).get(s, "—")
        # Check if champion this season
        champ = champions[champions["season"] == s]["champion_manager"]
        if not champ.empty and champ.iloc[0] == manager:
            row.append((f"🏆 {val}", "bold gold"))
        else:
            row.append((val, "center"))
    table_rows.append(row)

headers = ["Manager"] + [str(s) for s in all_seasons]
md_html(html_table(headers, table_rows))

# ── HEAD-TO-HEAD MATRIX ───────────────────────────────────────────────────

md_html("<div style='margin-top:1.5rem'></div>")
section_header("Head-to-Head Matrix", "Regular season all-time records")

# Build the H2H matrix
h2h: dict[tuple[str, str], tuple[int, int]] = {}
for a, b in RIVALRY_PAIRS:
    rv = get_rivalry_stats(a, b)
    h2h[(a, b)] = (rv["rs_a_wins"], rv["rs_b_wins"])
    h2h[(b, a)] = (rv["rs_b_wins"], rv["rs_a_wins"])

# Render as table
h2h_headers = ["vs."] + MANAGER_ORDER
h2h_rows    = []
for mgr_a in MANAGER_ORDER:
    color = MANAGER_COLORS.get(mgr_a, "#0A5EA8")
    row   = [(f'<span style="color:{color};font-weight:800;">{mgr_a}</span>', "")]
    for mgr_b in MANAGER_ORDER:
        if mgr_a == mgr_b:
            row.append(("—", "muted center"))
        else:
            wins, losses = h2h.get((mgr_a, mgr_b), (0, 0))
            cls = "bold center green" if wins > losses else ("bold center" if wins == losses else "center muted")
            row.append((f"{wins}–{losses}", cls))
    h2h_rows.append(row)

md_html(html_table(h2h_headers, h2h_rows))

md_html("<div style=\"font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;margin-top:0.5rem;\">Regular season only (weeks 1–15). Playoff records tracked separately in Rivalry Arena.</div>")

# ── CAREER TOTALS TABLE ───────────────────────────────────────────────────

md_html("<div style='margin-top:1.5rem'></div>")
section_header("Career Totals", "All-time regular season stats")

at_df   = get_all_time_standings()
ct_rows = []
for _, row in at_df.iterrows():
    mgr   = row["manager"]
    color = MANAGER_COLORS.get(mgr, "#0A5EA8")
    emoji = MANAGER_EMOJI.get(mgr, "🏈")
    champ_ct = int(row["championships"])
    ct_rows.append([
        (f'<span style="color:{color};font-weight:800;">{emoji} {mgr}</span>', ""),
        (f'{row["wins"]}–{row["losses"]}', "bold"),
        (f'{row["win_pct"]:.0%}', "center"),
        (f'{row["pf"]:.1f}', "right"),
        ("🏆 " * champ_ct if champ_ct else "—", "center"),
    ])

md_html(html_table(["Manager", "Record", "Win %", "Total PF", "Titles"], ct_rows))

md_html("<div style=\"padding:2.5rem 0 1.5rem;text-align:center;\"><div style=\"font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;font-weight:700;letter-spacing:2px;text-transform:uppercase;\">Espinosa FFL &bull; Locker Room</div></div>")
