"""Home — Espinosa FFL Clubhouse."""
from __future__ import annotations
import datetime
from pathlib import Path

import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_EMOJI,
    CLUBHOUSE_QUOTES, RECENT_EVENTS, CHAMPIONSHIP_TAGLINES,
    get_champions, get_all_time_standings, get_rivalry_stats, RIVALRY_PAIRS,
)
from utils.styles import inject_css, render_nav, section_header, md_html

st.set_page_config(
    page_title="Espinosa FFL Clubhouse",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("home")

# ── pre-load data ──────────────────────────────────────────────────────────
champions    = get_champions()
at_standings = get_all_time_standings()
day_idx      = datetime.date.today().toordinal()
rival_pair   = RIVALRY_PAIRS[day_idx % len(RIVALRY_PAIRS)]
rivalry      = get_rivalry_stats(*rival_pair)
latest       = champions.iloc[-1]
champ_mgr    = latest["champion_manager"]
champ_color  = MANAGER_COLORS.get(champ_mgr, "#0A5EA8")
champ_emoji  = MANAGER_EMOJI.get(champ_mgr, "🏈")
tagline      = CHAMPIONSHIP_TAGLINES.get(int(latest["season"]), "")

# ── HERO ───────────────────────────────────────────────────────────────────
HERO_PATH = Path(__file__).parent / "assets" / "hero.png"
if HERO_PATH.exists():
    st.image(str(HERO_PATH), use_container_width=True)
    md_html(
        """<div style="text-align:center;padding:1rem 0 0.25rem;">
<div style="font-family:'Fredoka One',cursive;font-size:2.5rem;color:#0A5EA8;line-height:1.1;">Espinosa Fantasy Football Clubhouse</div>
<div style="font-family:'Nunito',sans-serif;font-weight:700;font-size:1rem;color:#666;margin-top:0.35rem;">One League &nbsp;&bull;&nbsp; One Family &nbsp;&bull;&nbsp; Countless Memories</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;font-weight:700;margin-top:0.2rem;letter-spacing:2px;text-transform:uppercase;">Champions &bull; Rivalries &bull; Traditions &bull; Draft Day</div>
</div>"""
    )
else:
    md_html(
        """<div class="hq-hero-text">
<span class="hq-hero-emoji">🏟️</span>
<div class="hq-hero-title-text">Espinosa Fantasy Football Clubhouse</div>
<div class="hq-hero-tagline-text">One League &nbsp;&bull;&nbsp; One Family &nbsp;&bull;&nbsp; Countless Memories</div>
<div class="hq-hero-sub-text">Champions &bull; Rivalries &bull; Traditions &bull; Draft Day</div>
</div>"""
    )

# ═══════════════════════════════════════════════════════════════════════════
# FEATURED CHAMPION — the star of the page
# ═══════════════════════════════════════════════════════════════════════════
_, champ_col, _ = st.columns([1, 8, 1])
with champ_col:
    btn_style = (
        f"display:inline-block;font-family:'Nunito',sans-serif;font-weight:800;"
        f"font-size:0.82rem;color:white;background:{champ_color};padding:9px 22px;"
        f"border-radius:22px;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,0.15);"
        f"transition:all 0.18s;"
    )
    md_html(
        f"""<div class="hq-champ-featured" style="border-color:{champ_color};box-shadow:0 12px 56px rgba(214,163,25,0.16),0 4px 24px rgba(0,0,0,0.07);">
<div class="hq-confetti-tl">🎊 🎉 🎊</div>
<div class="hq-confetti-tr">🎊 🎉 🎊</div>
<span class="hq-champ-featured-trophy">🏆</span>
<div class="hq-champ-featured-label">✦ &nbsp; {int(latest['season'])} League Champion &nbsp; ✦</div>
<div class="hq-champ-featured-name" style="color:{champ_color};">{champ_emoji} {champ_mgr}</div>
<div class="hq-champ-featured-team">{latest['champion_team']}</div>
<div class="hq-champ-featured-score">{latest['champion_score']:.1f} – {latest['runner_up_score']:.1f} &nbsp;&bull;&nbsp; defeated {latest['runner_up_manager']}</div>
<div class="hq-champ-featured-tagline">"{tagline}"</div>
<div style="text-align:center;margin-top:1.25rem;"><a href="/champions" target="_self" style="{btn_style}">View the Trophy Room →</a></div>
</div>"""
    )

# ═══════════════════════════════════════════════════════════════════════════
# LEADERBOARD + RIVALRY  (equal columns, smaller than champion)
# ═══════════════════════════════════════════════════════════════════════════
col_lb, col_rival = st.columns(2, gap="medium")

# ── All-Time Leaderboard ───────────────────────────────────────────────────
with col_lb:
    rank_medals = ["🥇", "🥈", "🥉", "🏅"]
    rows_html = ""
    for i, (_, row) in enumerate(at_standings.iterrows()):
        mgr      = row["manager"]
        color    = MANAGER_COLORS.get(mgr, "#0A5EA8")
        emoji    = MANAGER_EMOJI.get(mgr, "🏈")
        medal    = rank_medals[i] if i < len(rank_medals) else str(i + 1)
        champ_ct = int(row["championships"])
        trophy   = "🏆 " * champ_ct if champ_ct else ""
        av_style = f"background:{color};width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;"
        rows_html += (
            f'<div class="hq-lb-row">'
            f'<div style="font-size:1.35rem;min-width:1.8rem;text-align:center;">{medal}</div>'
            f'<div class="hq-lb-avatar" style="{av_style}">{emoji}</div>'
            f'<div class="hq-lb-info" style="flex:1;min-width:0;">'
            f'<div class="hq-lb-name" style="font-family:\'Nunito\',sans-serif;font-weight:800;font-size:0.9rem;color:#222;">{mgr}</div>'
            f'<div class="hq-lb-record" style="font-family:\'Nunito\',sans-serif;font-size:0.7rem;color:#AAA;">{row["wins"]}–{row["losses"]} &nbsp;·&nbsp; {row["win_pct"]:.0%}</div>'
            f'</div>'
            f'<div style="font-size:0.95rem;flex-shrink:0;">{trophy}</div>'
            f'</div>\n'
        )

    lb_wrap = "background:#FFFDF8;border-radius:18px;padding:1.4rem 1.3rem;box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:5px solid #D6A319;height:100%;"
    lnk_style = "font-family:'Nunito',sans-serif;font-weight:800;font-size:0.76rem;color:#0A5EA8;text-decoration:none;border-bottom:2px solid #D9D7CF;padding-bottom:1px;"
    md_html(
        f"""<div class="hq-lb-gold" style="{lb_wrap}">
<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
<span style="font-size:1.5rem;">🏟️</span>
<div>
<div style="font-family:'Fredoka One',cursive;font-size:1.1rem;color:#333;">All-Time Standings</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#AAA;font-weight:700;">Regular season wins</div>
</div>
</div>
{rows_html}
<div style="text-align:center;margin-top:0.9rem;"><a href="/manager_profiles" target="_self" style="{lnk_style}">Open Locker Room →</a></div>
</div>"""
    )

# ── Rivalry Spotlight ──────────────────────────────────────────────────────
with col_rival:
    ra, rb     = rivalry["manager_a"], rivalry["manager_b"]
    ca, cb     = rivalry["color_a"],   rivalry["color_b"]
    la, lb_col = rivalry["light_a"],   rivalry["light_b"]
    ea, eb     = rivalry["emoji_a"],   rivalry["emoji_b"]
    ta, tb     = rivalry["total_a_wins"], rivalry["total_b_wins"]
    rs_a, rs_b = rivalry["rs_a_wins"],   rivalry["rs_b_wins"]
    po_a, po_b = rivalry["po_a_wins"],   rivalry["po_b_wins"]
    streak     = rivalry["streak_holder"]
    streak_ct  = rivalry["streak_count"]

    streak_html = ""
    if streak and streak_ct:
        sc = rivalry["color_a"] if streak == ra else rivalry["color_b"]
        streak_html = f'<div style="font-family:Nunito,sans-serif;font-size:0.78rem;color:{sc};font-weight:800;text-align:center;margin-top:0.3rem;">🔥 {streak} on a {streak_ct}-game streak</div>'

    rv_wrap = f"background:#FFFDF8;border-radius:18px;padding:1.4rem 1.3rem;box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:5px solid {ca};height:100%;position:relative;overflow:hidden;"
    av_a = f"width:48px;height:48px;border-radius:50%;background:{ca};display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 0.25rem;"
    av_b = f"width:48px;height:48px;border-radius:50%;background:{cb};display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 0.25rem;"
    rv_lnk = "font-family:'Nunito',sans-serif;font-weight:800;font-size:0.76rem;color:#0A5EA8;text-decoration:none;border-bottom:2px solid #D9D7CF;padding-bottom:1px;"
    split_a = f"position:absolute;top:0;left:0;bottom:0;width:50%;background:{la};opacity:0.18;border-radius:18px 0 0 18px;"
    split_b = f"position:absolute;top:0;right:0;bottom:0;width:50%;background:{lb_col};opacity:0.18;border-radius:0 18px 18px 0;"
    cell_s  = "background:rgba(255,255,255,0.7);border-radius:8px;padding:0.4rem;text-align:center;"
    lbl_s   = "font-family:'Nunito',sans-serif;font-size:0.57rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:#AAA;"
    val_s   = "font-family:'Fredoka One',cursive;font-size:1.1rem;color:#333;"

    md_html(
        f"""<div style="{rv_wrap}">
<div style="{split_a}"></div>
<div style="{split_b}"></div>
<div style="position:relative;">
<div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.8rem;">
<span style="font-size:1.3rem;">⚔️</span>
<div>
<div style="font-family:'Fredoka One',cursive;font-size:1.1rem;color:#333;">Rivalry Spotlight</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#AAA;font-weight:700;">Today's featured matchup</div>
</div>
</div>
<div style="display:flex;align-items:center;justify-content:space-between;gap:0.3rem;margin-bottom:0.3rem;">
<div style="flex:1;text-align:center;"><div style="{av_a}">{ea}</div><div style="font-family:'Fredoka One',cursive;font-size:1.3rem;color:{ca};line-height:1.1;">{ra}</div></div>
<div style="text-align:center;flex-shrink:0;padding:0 0.5rem;"><div style="font-family:'Fredoka One',cursive;font-size:2.2rem;color:#333;">{ta}–{tb}</div><div style="font-family:'Nunito',sans-serif;font-size:0.58rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#CCC;">All Time</div></div>
<div style="flex:1;text-align:center;"><div style="{av_b}">{eb}</div><div style="font-family:'Fredoka One',cursive;font-size:1.3rem;color:{cb};line-height:1.1;">{rb}</div></div>
</div>
{streak_html}
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;margin-top:0.6rem;">
<div style="{cell_s}"><div style="{lbl_s}">Reg. Season</div><div style="{val_s}">{rs_a}–{rs_b}</div></div>
<div style="{cell_s}"><div style="{lbl_s}">Playoffs</div><div style="{val_s}">{po_a}–{po_b}</div></div>
</div>
<div style="text-align:center;margin-top:0.85rem;"><a href="/rivalries" target="_self" style="{rv_lnk}">View Rivalry Arena →</a></div>
</div>
</div>"""
    )

# ── DIVIDER ────────────────────────────────────────────────────────────────
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🏈</span></div>')

# ═══════════════════════════════════════════════════════════════════════════
# BULLETIN BOARD + CHALKBOARD
# ═══════════════════════════════════════════════════════════════════════════
col_bull, col_chalk = st.columns([3, 2], gap="medium")

with col_bull:
    items_html = "".join(
        f'<div class="hq-bulletin-item"><span class="hq-bulletin-pin">{icon}</span><span>{text}</span></div>'
        for icon, text in RECENT_EVENTS
    )
    md_html(
        f"""<div class="hq-bulletin">
<div class="hq-bulletin-header">📌 &nbsp; What's Happening</div>
{items_html}
</div>"""
    )

with col_chalk:
    quote = CLUBHOUSE_QUOTES[day_idx % len(CLUBHOUSE_QUOTES)]
    md_html(
        f"""<div class="hq-chalkboard">
<div class="hq-chalkboard-icon">💬</div>
<div class="hq-chalkboard-text">"{quote}"</div>
<div class="hq-chalkboard-line"></div>
<div class="hq-chalkboard-attr">— The Espinosa FFL Clubhouse</div>
</div>"""
    )

# ── DIVIDER ────────────────────────────────────────────────────────────────
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🏈</span></div>')

# ═══════════════════════════════════════════════════════════════════════════
# TROPHY SHELF
# ═══════════════════════════════════════════════════════════════════════════
trophy_icons = {"Shawn": "🏆", "Jennifer": "⭐", "Daphne": "✨", "Elliot": "🩷"}

items_html = ""
for _, row in champions.iterrows():
    mgr   = row["champion_manager"]
    color = MANAGER_COLORS.get(mgr, "#0A5EA8")
    icon  = trophy_icons.get(mgr, "🏆")
    items_html += (
        f'<div class="hq-trophy-item">'
        f'<span class="hq-trophy-item-icon">{icon}</span>'
        f'<div class="hq-trophy-item-year">{int(row["season"])}</div>'
        f'<div class="hq-trophy-item-name" style="color:{color};">{mgr}</div>'
        f'<div class="hq-trophy-item-team">{row["champion_team"]}</div>'
        f'</div>\n'
    )

items_html += (
    '<div class="hq-trophy-item coming-soon">'
    '<span class="hq-trophy-item-icon">🏆</span>'
    '<div class="hq-trophy-item-year">2026</div>'
    '<div class="hq-trophy-item-name">???</div>'
    '<div class="hq-trophy-item-team">Who will it be?</div>'
    '</div>'
)

md_html(
    f"""<div class="hq-trophy-shelf-wrap">
<div class="hq-shelf-label">🏆 Champion Shelf</div>
<div class="hq-shelf-sub">Every trophy. Every season.</div>
<div class="hq-shelf-rail">
{items_html}
</div>
<div class="hq-shelf-plank"></div>
</div>"""
)

# ── DIVIDER ────────────────────────────────────────────────────────────────
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🏈</span></div>')

# ═══════════════════════════════════════════════════════════════════════════
# EXPLORE THE CLUBHOUSE
# ═══════════════════════════════════════════════════════════════════════════
md_html(
    """<div class="hq-explore-header">
<div class="hq-explore-title-text">Explore the Clubhouse</div>
<div class="hq-explore-sub">Pick a room and step inside</div>
</div>"""
)

ROOMS = [
    {"icon": "🏆", "title": "Trophy Room",      "desc": "Every champion. Every season. Every memory.",        "href": "/champions",        "color": "#D6A319", "soon": False, "room_class": "hq-room-trophy"},
    {"icon": "📖", "title": "Season Scrapbook", "desc": "Relive the standings, playoffs, and drafts.",        "href": "/season_archive",   "color": "#0A5EA8", "soon": False, "room_class": "hq-room-scrapbook"},
    {"icon": "👥", "title": "Locker Room",       "desc": "Manager profiles, career stats, and rivalries.",    "href": "/manager_profiles", "color": "#1F5E3B", "soon": False, "room_class": "hq-room-locker"},
    {"icon": "🥊", "title": "Rivalry Arena",     "desc": "Every grudge. Every bragging right.",               "href": "/rivalries",        "color": "#E86AA6", "soon": False, "room_class": "hq-room-rivalry"},
    {"icon": "🎯", "title": "Achievement Wall",  "desc": "Badges, stickers, and unlockables. Coming soon.",  "href": "#",                 "color": "#AAA",    "soon": True,  "room_class": "hq-room-achievement"},
]

explore_cols = st.columns(5, gap="medium")
for col, room in zip(explore_cols, ROOMS):
    with col:
        soon_cls = " coming-soon" if room["soon"] else ""
        href     = room["href"]
        target   = ' target="_self"' if not room["soon"] else ""
        arrow    = f'<div class="hq-explore-arrow" style="color:{room["color"]};">→</div>' if not room["soon"] else '<div style="font-size:0.62rem;color:#CCC;font-family:Nunito,sans-serif;font-weight:800;text-transform:uppercase;letter-spacing:1px;margin-top:0.4rem;">Coming Soon</div>'
        title_c  = "#AAA" if room["soon"] else "#222"
        # Wrap <a> in <div> so the block-level <div> triggers CommonMark HTML block mode
        md_html(
            f'<div><a href="{href}"{target} class="hq-explore-card {room["room_class"]}{soon_cls}">'
            f'<span class="hq-explore-icon">{room["icon"]}</span>'
            f'<div class="hq-explore-room-title" style="color:{title_c};">{room["title"]}</div>'
            f'<div class="hq-explore-room-desc">{room["desc"]}</div>'
            f'{arrow}'
            f'</a></div>'
        )

md_html(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
<div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#CCC;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Espinosa Fantasy Football Clubhouse &bull; Est. 2023 &bull; All Rights Reserved to the Family</div>
</div>"""
)
