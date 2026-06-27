"""Home — Espinosa FFL Clubhouse."""
from __future__ import annotations
import datetime
import random
from pathlib import Path

import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_LIGHT_COLORS, MANAGER_EMOJI, MANAGER_ORDER,
    TEAM_TO_MANAGER, CLUBHOUSE_QUOTES, RECENT_EVENTS,
    CHAMPIONSHIP_TAGLINES,
    get_champions, get_all_time_standings, get_rivalry_stats, RIVALRY_PAIRS,
    LEAGUE_NAME, CURRENT_SEASON,
)
from utils.styles import (
    inject_css, render_nav, manager_avatar_html, section_header, html_table,
)

st.set_page_config(
    page_title="Espinosa FFL Clubhouse",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("home")

# ── HERO ─────────────────────────────────────────────────────────────────────
HERO_PATH = Path(__file__).parent / "assets" / "hero.png"
if HERO_PATH.exists():
    st.image(str(HERO_PATH), use_container_width=True)
else:
    st.markdown(
        """<div class="hq-hero">
            <div class="hq-hero-title">Espinosa Fantasy Football Clubhouse</div>
            <div class="hq-hero-taglines">
                One League.&nbsp;&nbsp;One Family.&nbsp;&nbsp;Countless Memories.
            </div>
            <div class="hq-hero-sub">
                Champions &bull; Rivalries &bull; Traditions &bull; Draft Day
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown(
    """<div style="text-align:center;padding:0.5rem 0 1.4rem;">
        <div style="font-family:'Nunito',sans-serif;font-weight:700;font-size:0.78rem;
                    color:#AAA;letter-spacing:2px;text-transform:uppercase;">
            Est. 2023 &bull; 4 Managers &bull; 3 Champions &bull; 1 Family
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ── ROW 1: Champion | Leaderboard | Rivalry ───────────────────────────────

champions    = get_champions()
at_standings = get_all_time_standings()

# Daily rotating rivalry spotlight
day_idx     = datetime.date.today().toordinal()
rival_pair  = RIVALRY_PAIRS[day_idx % len(RIVALRY_PAIRS)]
rivalry     = get_rivalry_stats(*rival_pair)

col_champ, col_lb, col_rival = st.columns(3, gap="medium")

# ── Champion Card ────────────────────────────────────────────────────────────
with col_champ:
    latest       = champions.iloc[-1]
    champ_mgr    = latest["champion_manager"]
    champ_color  = MANAGER_COLORS.get(champ_mgr, "#0A5EA8")
    champ_light  = MANAGER_LIGHT_COLORS.get(champ_mgr, "#E3EDF8")
    champ_emoji  = MANAGER_EMOJI.get(champ_mgr, "🏈")
    tagline      = CHAMPIONSHIP_TAGLINES.get(int(latest["season"]), "")

    st.markdown(
        f"""<div class="hq-card" style="border-top-color:{champ_color};">
            <div class="hq-section-label">🏆 Current Champion</div>
            <div style="text-align:center;padding:0.75rem 0 0.5rem;">
                <div style="font-size:3.5rem;">🏆</div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.68rem;font-weight:800;
                            text-transform:uppercase;letter-spacing:3px;color:#AAA;margin-top:0.3rem;">
                    {int(latest['season'])} Champion
                </div>
                <div class="hq-big-name" style="color:{champ_color};">{champ_mgr}</div>
                <div class="hq-team-name">{latest['champion_team']}</div>
                <div class="hq-score-line">
                    {latest['champion_score']:.1f} – {latest['runner_up_score']:.1f}
                    &nbsp;over&nbsp; {latest['runner_up_manager']}
                </div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.78rem;color:#888;
                            font-style:italic;margin-top:0.5rem;line-height:1.4;">
                    "{tagline}"
                </div>
            </div>
            <div style="text-align:center;">
                <a href="/champions" class="hq-btn" style="background:{champ_color};" target="_self">
                    View Trophy Room →
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

# ── All-Time Leaderboard ─────────────────────────────────────────────────────
with col_lb:
    rank_classes = ["gold", "silver", "bronze", ""]
    rows_html = ""
    for i, (_, row) in enumerate(at_standings.iterrows()):
        mgr        = row["manager"]
        color      = MANAGER_COLORS.get(mgr, "#0A5EA8")
        emoji      = MANAGER_EMOJI.get(mgr, "🏈")
        rank_cls   = rank_classes[i] if i < len(rank_classes) else ""
        champ_ct   = int(row["championships"])
        trophy_str = "🏆" * champ_ct if champ_ct else ""
        rows_html += f"""
        <div class="hq-lb-row">
            <div class="hq-lb-rank {rank_cls}">{i+1}</div>
            <div class="hq-lb-avatar" style="background:{color};">{emoji}</div>
            <div class="hq-lb-info">
                <div class="hq-lb-name">{mgr}</div>
                <div class="hq-lb-record">{row['wins']}–{row['losses']} &nbsp;·&nbsp;
                    {row['win_pct']:.0%} win rate</div>
            </div>
            <div class="hq-lb-trophy">{trophy_str}</div>
        </div>"""

    st.markdown(
        f"""<div class="hq-card" style="border-top-color:#D6A319;">
            <div class="hq-section-label">📊 All-Time Leaderboard</div>
            <div style="margin-top:0.5rem;">{rows_html}</div>
            <div style="text-align:center;margin-top:0.8rem;">
                <a href="/manager_profiles" class="hq-btn" target="_self">
                    View Locker Room →
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

# ── Rivalry Spotlight ────────────────────────────────────────────────────────
with col_rival:
    ra, rb      = rivalry["manager_a"], rivalry["manager_b"]
    ca, cb      = rivalry["color_a"],   rivalry["color_b"]
    ea, eb      = rivalry["emoji_a"],   rivalry["emoji_b"]
    total_a     = rivalry["total_a_wins"]
    total_b     = rivalry["total_b_wins"]
    rs_a        = rivalry["rs_a_wins"]
    rs_b        = rivalry["rs_b_wins"]
    po_a        = rivalry["po_a_wins"]
    po_b        = rivalry["po_b_wins"]
    streak      = rivalry["streak_holder"]
    streak_ct   = rivalry["streak_count"]
    streak_txt  = f"🔥 {streak} on a {streak_ct}-game streak" if streak and streak_ct else ""

    st.markdown(
        f"""<div class="hq-card" style="border-top-color:#E86AA6;">
            <div class="hq-section-label">🔥 Rivalry Spotlight</div>
            <div class="hq-rivalry-vs" style="margin:0.8rem 0 0.4rem;">
                <div style="flex:1;text-align:center;">
                    <div style="font-size:1.8rem;">{ea}</div>
                    <div class="hq-rivalry-manager" style="color:{ca};">{ra}</div>
                </div>
                <div style="flex-shrink:0;text-align:center;padding:0 0.3rem;">
                    <div class="hq-rivalry-score">{total_a}–{total_b}</div>
                    <div class="hq-rivalry-divider">All Time</div>
                </div>
                <div style="flex:1;text-align:center;">
                    <div style="font-size:1.8rem;">{eb}</div>
                    <div class="hq-rivalry-manager" style="color:{cb};">{rb}</div>
                </div>
            </div>
            <div style="font-family:'Nunito',sans-serif;font-size:0.75rem;color:#999;
                        text-align:center;margin-bottom:0.3rem;">
                Reg. season: {rs_a}–{rs_b} &nbsp;·&nbsp; Playoffs: {po_a}–{po_b}
            </div>
            {"<div style='font-family:Nunito,sans-serif;font-size:0.78rem;color:#555;text-align:center;font-weight:700;margin-top:0.2rem;'>" + streak_txt + "</div>" if streak_txt else ""}
            <div style="text-align:center;margin-top:0.75rem;">
                <a href="/rivalries" class="hq-btn" target="_self">
                    View Rivalry Arena →
                </a>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)

# ── ROW 2: Recent Events | Clubhouse Quote ────────────────────────────────

col_events, col_quote = st.columns([3, 2], gap="medium")

with col_events:
    section_header("What's Happening", "Latest from the Clubhouse")
    items_html = "".join(
        f'<div class="hq-feed-item"><span class="hq-feed-icon">{icon}</span><span>{text}</span></div>'
        for icon, text in RECENT_EVENTS
    )
    st.markdown(
        f"""<div class="hq-card" style="border-top-color:#1F5E3B;">
            {items_html}
        </div>""",
        unsafe_allow_html=True,
    )

with col_quote:
    section_header("Clubhouse Quote", "Words to live by")
    quote_idx = day_idx % len(CLUBHOUSE_QUOTES)
    quote     = CLUBHOUSE_QUOTES[quote_idx]
    st.markdown(
        f"""<div class="hq-quote-card">
            <div style="font-size:2.2rem;margin-bottom:0.6rem;">💬</div>
            <div class="hq-quote-text">"{quote}"</div>
            <div class="hq-quote-attr">— The Espinosa FFL Clubhouse</div>
        </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-top:1.25rem'></div>", unsafe_allow_html=True)

# ── ROW 3: Season History Strip ───────────────────────────────────────────

section_header("Champion History", "Every season. Every winner.")

champ_cols = st.columns(len(champions), gap="medium")
for i, (_, row) in enumerate(champions.iterrows()):
    mgr     = row["champion_manager"]
    color   = MANAGER_COLORS.get(mgr, "#0A5EA8")
    emoji   = MANAGER_EMOJI.get(mgr, "🏈")
    with champ_cols[i]:
        st.markdown(
            f"""<div class="hq-mini-champ" style="border-top-color:{color};">
                <div class="hq-mini-champ-year">{int(row['season'])}</div>
                <div style="font-size:1.8rem;margin:0.3rem 0 0.2rem;">{emoji}</div>
                <div class="hq-mini-champ-name" style="color:{color};">{mgr}</div>
                <div class="hq-mini-champ-team">{row['champion_team']}</div>
                <div class="hq-mini-champ-score">
                    {row['champion_score']:.1f} – {row['runner_up_score']:.1f}
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<div style='padding:3rem 0 1.5rem;text-align:center;'>", unsafe_allow_html=True)
st.markdown(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
        <div style="font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;
                    font-weight:700;letter-spacing:2px;text-transform:uppercase;">
            Espinosa Fantasy Football Clubhouse &bull; Est. 2023
        </div>
    </div>""",
    unsafe_allow_html=True,
)
