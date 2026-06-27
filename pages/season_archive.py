"""Season Scrapbook — per-season deep dive."""
from __future__ import annotations
import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_EMOJI, TEAM_TO_MANAGER,
    SEASON_NOTES, CHAMPIONSHIP_TAGLINES,
    get_season_standings, get_champions, get_season_playoffs,
    load_all, CURRENT_SEASON, FOUNDED,
)
from utils.styles import (
    inject_css, render_nav, render_page_header,
    section_header, html_table,
)

st.set_page_config(
    page_title="Season Scrapbook · Espinosa FFL",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("season_archive")
render_page_header(
    "📖 THE CLUBHOUSE",
    "Season Scrapbook",
    "Every week. Every win. Every memory.",
)

# Season selector
seasons = list(range(FOUNDED, CURRENT_SEASON + 1))
season  = st.selectbox(
    "Choose a season",
    options=seasons[::-1],
    format_func=lambda s: f"{s} Season",
)

st.markdown("<div style='margin-top:0.75rem'></div>", unsafe_allow_html=True)

# Load data for selected season
standings = get_season_standings(season)
champions = get_champions()
playoffs  = get_season_playoffs(season)
notes     = SEASON_NOTES.get(season, {})

season_champ = champions[champions["season"] == season]
champ_row    = season_champ.iloc[0] if not season_champ.empty else None

# ── SEASON HEADER ─────────────────────────────────────────────────────────

if champ_row is not None:
    mgr    = champ_row["champion_manager"]
    color  = MANAGER_COLORS.get(mgr, "#0A5EA8")
    emoji  = MANAGER_EMOJI.get(mgr, "🏈")
    tagline = notes.get("tagline", CHAMPIONSHIP_TAGLINES.get(season, ""))

    st.markdown(
        f"""<div style="background:#FFFDF8;border-radius:20px;padding:1.5rem 1.8rem;
                    box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:5px solid {color};
                    display:flex;align-items:center;gap:1.2rem;margin-bottom:1.25rem;
                    flex-wrap:wrap;">
            <div style="font-size:3rem;">{emoji}</div>
            <div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.68rem;font-weight:800;
                            text-transform:uppercase;letter-spacing:3px;color:#AAA;">
                    {season} Champion
                </div>
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;
                            color:{color};line-height:1.1;">
                    {mgr}
                </div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.85rem;
                            color:#666;font-style:italic;">
                    {champ_row['champion_team']} &nbsp;·&nbsp;
                    {champ_row['champion_score']:.1f} – {champ_row['runner_up_score']:.1f}
                    def. {champ_row['runner_up_manager']}
                </div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.8rem;
                            color:#AAA;font-style:italic;margin-top:0.2rem;">
                    "{tagline}"
                </div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

# ── MAIN CONTENT: Standings | Playoffs ───────────────────────────────────

col_stand, col_play = st.columns([3, 2], gap="medium")

# ── Regular Season Standings ─────────────────────────────────────────────
with col_stand:
    section_header("Regular Season Standings", "Weeks 1 – 15")

    if not standings.empty:
        rank_emojis = ["🥇", "🥈", "🥉", "4️⃣"]
        table_rows  = []
        for _, row in standings.iterrows():
            mgr    = row["manager"]
            color  = MANAGER_COLORS.get(mgr, "#0A5EA8")
            rank_e = rank_emojis[int(row["rank"]) - 1] if row["rank"] <= 4 else str(row["rank"])
            table_rows.append([
                rank_e,
                (f'<span style="font-weight:800;color:{color};">{mgr}</span>', ""),
                (row["team_name"], "muted"),
                (f'{row["wins"]}–{row["losses"]}', "bold"),
                (f'{row["pf"]:.1f}', "right"),
                (f'{row["pa"]:.1f}', "muted right"),
            ])

        st.markdown(
            html_table(
                ["", "Manager", "Team", "Record", "PF", "PA"],
                table_rows,
            ),
            unsafe_allow_html=True,
        )

        # Season highlights
        if notes.get("highlights"):
            st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
            section_header("Season Highlights")
            for h in notes["highlights"]:
                st.markdown(
                    f'<div class="hq-highlight">⚡ {h}</div>',
                    unsafe_allow_html=True,
                )

# ── Playoff Bracket ──────────────────────────────────────────────────────
with col_play:
    section_header("Playoff Bracket", "The road to the championship")

    if not playoffs.empty:
        def game_html(game_row) -> str:
            t1, s1 = game_row["team_1"],  float(game_row["score_1"])
            t2, s2 = game_row["team_2"],  float(game_row["score_2"])
            mgr1   = TEAM_TO_MANAGER.get(t1, t1)
            mgr2   = TEAM_TO_MANAGER.get(t2, t2)
            seed1  = int(game_row["seed_1"])
            seed2  = int(game_row["seed_2"])
            c1     = MANAGER_COLORS.get(mgr1, "#333")
            c2     = MANAGER_COLORS.get(mgr2, "#333")
            w1     = "winner" if s1 > s2 else "loser"
            w2     = "winner" if s2 > s1 else "loser"
            return f"""<div class="hq-bracket-game">
                <div class="hq-bracket-team {w1}">
                    <span style="color:{'inherit' if w1 == 'loser' else c1};">
                        #{seed1} {mgr1}
                    </span>
                    <span class="hq-bracket-score">{s1:.1f}</span>
                </div>
                <div class="hq-bracket-team {w2}">
                    <span style="color:{'inherit' if w2 == 'loser' else c2};">
                        #{seed2} {mgr2}
                    </span>
                    <span class="hq-bracket-score">{s2:.1f}</span>
                </div>
            </div>"""

        # Semis
        semis = playoffs[playoffs["game_type"] == "semifinal"]
        if not semis.empty:
            st.markdown(
                '<div class="hq-bracket-round">Semifinals — Week 16</div>',
                unsafe_allow_html=True,
            )
            for _, g in semis.iterrows():
                st.markdown(game_html(g), unsafe_allow_html=True)

        # Championship
        final = playoffs[playoffs["game_type"] == "final"]
        if not final.empty:
            st.markdown(
                '<div class="hq-bracket-round">🏆 Championship — Week 17</div>',
                unsafe_allow_html=True,
            )
            st.markdown(game_html(final.iloc[0]), unsafe_allow_html=True)

        # 3rd place
        third = playoffs[playoffs["game_type"] == "3rd_place"]
        if not third.empty:
            st.markdown(
                '<div class="hq-bracket-round">3rd Place — Week 17</div>',
                unsafe_allow_html=True,
            )
            st.markdown(game_html(third.iloc[0]), unsafe_allow_html=True)

# ── DRAFT PICKS ───────────────────────────────────────────────────────────

st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)
section_header("Draft Day", f"{season} Draft — First 5 Rounds")

data  = load_all()
draft = data.get("draft", None)

if draft is not None and not draft.empty:
    season_draft = draft[
        (draft["season"] == season) & (draft["player_name"] != "--empty--")
    ].sort_values("overall_pick")

    # Organize by round
    rounds = season_draft["round"].unique()
    n_cols = min(len(rounds), 5)
    cols   = st.columns(n_cols, gap="small")

    for i, rnd in enumerate(sorted(rounds)[:n_cols]):
        rnd_picks = season_draft[season_draft["round"] == rnd]
        with cols[i]:
            st.markdown(
                f'<div style="font-family:Nunito,sans-serif;font-size:0.65rem;font-weight:800;'
                f'text-transform:uppercase;letter-spacing:2px;color:#AAA;margin-bottom:0.4rem;">'
                f'Round {int(rnd)}</div>',
                unsafe_allow_html=True,
            )
            for _, pick in rnd_picks.iterrows():
                team   = pick["team_name"]
                mgr    = TEAM_TO_MANAGER.get(team, team)
                color  = MANAGER_COLORS.get(mgr, "#0A5EA8")
                player = pick["player_name"]
                ovr    = int(pick["overall_pick"])
                st.markdown(
                    f"""<div class="hq-pick-card" style="border-left-color:{color};">
                        <div class="hq-pick-num" style="color:{color};">{ovr}</div>
                        <div>
                            <div class="hq-pick-player">{player}</div>
                            <div class="hq-pick-team">{mgr}</div>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

st.markdown(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
        <div style="font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;
                    font-weight:700;letter-spacing:2px;text-transform:uppercase;">
            Espinosa FFL &bull; Season Scrapbook
        </div>
    </div>""",
    unsafe_allow_html=True,
)
