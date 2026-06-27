"""Trophy Room — all champions."""
from __future__ import annotations
import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_LIGHT_COLORS, MANAGER_EMOJI,
    CHAMPIONSHIP_TAGLINES, SEASON_NOTES,
    get_champions,
)
from utils.styles import inject_css, render_nav, render_page_header, section_header

st.set_page_config(
    page_title="Trophy Room · Espinosa FFL",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("champions")
render_page_header(
    "🏆 THE CLUBHOUSE",
    "Trophy Room",
    "Every champion. Every season. Every memory.",
)

champions = get_champions()

# ── REIGNING CHAMPION ─────────────────────────────────────────────────────

section_header("Reigning Champion", "The last one standing")

latest    = champions.iloc[-1]
mgr       = latest["champion_manager"]
color     = MANAGER_COLORS.get(mgr, "#0A5EA8")
emoji     = MANAGER_EMOJI.get(mgr, "🏈")
tagline   = CHAMPIONSHIP_TAGLINES.get(int(latest["season"]), "")

st.markdown(
    f"""<div class="hq-champ-card" style="max-width:560px;margin:0 auto 2rem;">
        <span class="hq-champ-trophy">🏆</span>
        <div class="hq-champ-season">{int(latest['season'])} Champion</div>
        <div style="font-size:3.5rem;margin:0.4rem 0 0.1rem;">{emoji}</div>
        <div class="hq-champ-name" style="color:{color};">{mgr}</div>
        <div class="hq-champ-team">{latest['champion_team']}</div>
        <div class="hq-champ-score">
            Defeated {latest['runner_up_manager']} &nbsp;·&nbsp;
            {latest['champion_score']:.1f} – {latest['runner_up_score']:.1f}
        </div>
        <div class="hq-champ-tagline">"{tagline}"</div>
    </div>""",
    unsafe_allow_html=True,
)

# ── ALL CHAMPIONS ─────────────────────────────────────────────────────────

section_header("All Champions", f"League founded {int(champions.iloc[0]['season'])}")

champ_cols = st.columns(len(champions), gap="medium")
for col, (_, row) in zip(champ_cols, champions.iterrows()):
    mgr    = row["champion_manager"]
    color  = MANAGER_COLORS.get(mgr, "#0A5EA8")
    light  = MANAGER_LIGHT_COLORS.get(mgr, "#E3EDF8")
    emoji  = MANAGER_EMOJI.get(mgr, "🏈")
    season = int(row["season"])
    notes  = SEASON_NOTES.get(season, {})

    with col:
        st.markdown(
            f"""<div class="hq-card" style="border-top-color:{color};">
                <div style="text-align:center;padding:0.5rem 0;">
                    <div style="font-family:'Fredoka One',cursive;font-size:1.6rem;
                                color:{color};">{season}</div>
                    <div style="font-size:2.2rem;margin:0.3rem 0;">{emoji}</div>
                    <div style="font-family:'Fredoka One',cursive;font-size:1.7rem;
                                color:{color};line-height:1.1;">{mgr}</div>
                    <div class="hq-team-name">{row['champion_team']}</div>
                    <div style="margin:0.6rem 0;border-top:1px solid #EEE8E0;"></div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.78rem;
                                font-weight:700;color:#555;">
                        🏆 {row['champion_score']:.1f} – {row['runner_up_score']:.1f}
                    </div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#999;">
                        def. {row['runner_up_manager']}
                        &nbsp;(margin: {row['margin']:.1f} pts)
                    </div>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ── SEASON STORIES ────────────────────────────────────────────────────────

section_header("Season Stories", "What made each season unforgettable")

for _, row in champions.sort_values("season", ascending=False).iterrows():
    season  = int(row["season"])
    mgr     = row["champion_manager"]
    color   = MANAGER_COLORS.get(mgr, "#0A5EA8")
    notes   = SEASON_NOTES.get(season, {})
    tagline = notes.get("tagline", "")
    highs   = notes.get("highlights", [])

    highlights_html = "".join(
        f'<div class="hq-highlight">⚡ {h}</div>' for h in highs
    )

    st.markdown(
        f"""<div class="hq-card" style="border-top-color:{color};margin-bottom:1rem;">
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.75rem;">
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;
                            color:{color};">{season}</div>
                <div>
                    <div style="font-family:'Fredoka One',cursive;font-size:1.3rem;
                                color:{color};">{mgr} wins</div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.8rem;
                                color:#888;font-style:italic;">"{tagline}"</div>
                </div>
            </div>
            {highlights_html}
        </div>""",
        unsafe_allow_html=True,
    )

# ── CHAMPIONSHIP STATS ───────────────────────────────────────────────────

st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
section_header("By the Numbers", "Championship records")

col_a, col_b, col_c = st.columns(3, gap="medium")

# Closest finish
closest = champions.sort_values("margin").iloc[0]
closest_mgr   = closest["champion_manager"]
closest_color = MANAGER_COLORS.get(closest_mgr, "#0A5EA8")

# Biggest blowout
blowout       = champions.sort_values("margin", ascending=False).iloc[0]
blowout_mgr   = blowout["champion_manager"]
blowout_color = MANAGER_COLORS.get(blowout_mgr, "#0A5EA8")

with col_a:
    st.markdown(
        f"""<div class="hq-card" style="border-top-color:{closest_color};text-align:center;">
            <div style="font-size:2rem;">😰</div>
            <div class="hq-section-label" style="margin-top:0.3rem;">Closest Championship</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;
                        color:{closest_color};margin:0.2rem 0;">
                {closest['margin']:.1f} pts
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.82rem;color:#555;font-weight:700;">
                {int(closest['season'])} — {closest['champion_manager']} def. {closest['runner_up_manager']}
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.75rem;color:#AAA;">
                {closest['champion_score']:.1f} – {closest['runner_up_score']:.1f}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

with col_b:
    st.markdown(
        f"""<div class="hq-card" style="border-top-color:{blowout_color};text-align:center;">
            <div style="font-size:2rem;">💥</div>
            <div class="hq-section-label" style="margin-top:0.3rem;">Biggest Margin</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;
                        color:{blowout_color};margin:0.2rem 0;">
                {blowout['margin']:.1f} pts
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.82rem;color:#555;font-weight:700;">
                {int(blowout['season'])} — {blowout['champion_manager']} def. {blowout['runner_up_manager']}
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.75rem;color:#AAA;">
                {blowout['champion_score']:.1f} – {blowout['runner_up_score']:.1f}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

with col_c:
    # Who is still waiting for their first title?
    champ_managers = set(champions["champion_manager"].tolist())
    from utils.data import MANAGER_ORDER
    waiting = [m for m in MANAGER_ORDER if m not in champ_managers]
    waiting_color = "#E86AA6" if not waiting else MANAGER_COLORS.get(waiting[0], "#888")
    waiting_text  = waiting[0] if waiting else "Everyone's won one!"
    waiting_sub   = "Still chasing that first ring 👀" if waiting else "Championship parity!"

    st.markdown(
        f"""<div class="hq-card" style="border-top-color:{waiting_color};text-align:center;">
            <div style="font-size:2rem;">🎯</div>
            <div class="hq-section-label" style="margin-top:0.3rem;">Still Waiting</div>
            <div style="font-family:'Fredoka One',cursive;font-size:2rem;
                        color:{waiting_color};margin:0.2rem 0;">
                {waiting_text}
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.82rem;color:#888;
                        font-style:italic;">
                {waiting_sub}
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
        <div style="font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;
                    font-weight:700;letter-spacing:2px;text-transform:uppercase;">
            Espinosa FFL &bull; Trophy Room
        </div>
    </div>""",
    unsafe_allow_html=True,
)
