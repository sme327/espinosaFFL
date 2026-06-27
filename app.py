"""Home — Espinosa FFL Clubhouse."""
from __future__ import annotations
import datetime
from pathlib import Path

import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_EMOJI,
    RECENT_EVENTS, CHAMPIONSHIP_TAGLINES,
    get_champions, get_rivalry_stats, RIVALRY_PAIRS,
)
from utils.styles import inject_css, render_nav, md_html

st.set_page_config(
    page_title="Espinosa FFL Clubhouse",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("home")

# ── pre-load data ──────────────────────────────────────────────────────────
champions   = get_champions()
day_idx     = datetime.date.today().toordinal()
rival_pair  = RIVALRY_PAIRS[day_idx % len(RIVALRY_PAIRS)]
rivalry     = get_rivalry_stats(*rival_pair)
latest      = champions.iloc[-1]
champ_mgr   = latest["champion_manager"]
champ_color = MANAGER_COLORS.get(champ_mgr, "#0A5EA8")
champ_emoji = MANAGER_EMOJI.get(champ_mgr, "🏈")
tagline     = CHAMPIONSHIP_TAGLINES.get(int(latest["season"]), "")

# ══════════════════════════════════════════════════════════════════════════
# 1. CLUBHOUSE HERO
# ══════════════════════════════════════════════════════════════════════════
HERO_PATH = Path(__file__).parent / "assets" / "hero.png"
if HERO_PATH.exists():
    st.image(str(HERO_PATH), use_container_width=True)
else:
    md_html(
        """<div style="background:linear-gradient(160deg,#0A5EA8 0%,#1472C8 45%,#1F5E3B 100%);border-radius:24px;padding:4rem 2rem;text-align:center;position:relative;overflow:hidden;margin-bottom:0.25rem;">
<div style="position:absolute;top:0;left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:center;gap:4rem;opacity:0.10;pointer-events:none;">
<span style="font-size:7rem;">🏟️</span><span style="font-size:9rem;">🏈</span><span style="font-size:7rem;">🏆</span>
</div>
<div style="position:relative;z-index:1;">
<div style="font-size:5.5rem;margin-bottom:0.6rem;filter:drop-shadow(0 6px 16px rgba(0,0,0,0.3));">🏟️</div>
<div style="font-family:'Fredoka One',cursive;font-size:2.6rem;color:white;line-height:1.2;text-shadow:0 2px 12px rgba(0,0,0,0.2);">Welcome to the Clubhouse</div>
<div style="font-family:'Nunito',sans-serif;font-size:1rem;color:rgba(255,255,255,0.78);margin-top:0.6rem;font-weight:700;">Where Espinosa FFL history lives forever</div>
</div>
</div>"""
    )

md_html(
    """<div style="text-align:center;padding:1rem 0 0.25rem;">
<div style="font-family:'Fredoka One',cursive;font-size:2.3rem;color:#0A5EA8;line-height:1.15;">Espinosa Fantasy Football Clubhouse</div>
<div style="font-family:'Nunito',sans-serif;font-weight:700;font-size:0.95rem;color:#999;margin-top:0.35rem;letter-spacing:0.5px;">One League &nbsp;&bull;&nbsp; One Family &nbsp;&bull;&nbsp; Countless Memories</div>
</div>"""
)

# ══════════════════════════════════════════════════════════════════════════
# 2. CURRENT CHAMPION
# ══════════════════════════════════════════════════════════════════════════
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🏆</span></div>')

_, champ_col, _ = st.columns([0.5, 9, 0.5])
with champ_col:
    btn_style = (
        f"display:inline-block;font-family:'Nunito',sans-serif;font-weight:800;"
        f"font-size:0.85rem;color:white;background:{champ_color};padding:10px 28px;"
        f"border-radius:24px;text-decoration:none;box-shadow:0 4px 16px rgba(0,0,0,0.15);"
    )
    md_html(
        f"""<div class="hq-champ-featured" style="border-color:{champ_color};">
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

# ══════════════════════════════════════════════════════════════════════════
# 3. EXPLORE THE CLUBHOUSE
# ══════════════════════════════════════════════════════════════════════════
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🚪</span></div>')

md_html(
    """<div style="text-align:center;margin-bottom:1.5rem;">
<div style="font-family:'Fredoka One',cursive;font-size:2.1rem;color:#333;">Explore the Clubhouse</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.88rem;color:#BBB;font-weight:700;margin-top:0.3rem;letter-spacing:0.5px;">Pick a room and step inside</div>
</div>"""
)

ROOMS = [
    {
        "icon": "🏆", "title": "Trophy Room",
        "desc": "Every champion. Every title. Every memory.",
        "href": "/champions", "color": "#D6A319", "soon": False,
        "room_class": "hq-room-trophy",
        "illo_bg": "linear-gradient(160deg,#FFF8E0 0%,#FFE050 100%)",
        "illo_main": "🏆", "illo_l": "🥇", "illo_r": "🥈",
    },
    {
        "icon": "📖", "title": "Season Scrapbook",
        "desc": "Relive the standings, playoffs, and draft day moments.",
        "href": "/season_archive", "color": "#0A5EA8", "soon": False,
        "room_class": "hq-room-scrapbook",
        "illo_bg": "linear-gradient(160deg,#EEF5FF 0%,#90C4FF 100%)",
        "illo_main": "📖", "illo_l": "🏈", "illo_r": "⭐",
    },
    {
        "icon": "👥", "title": "Locker Room",
        "desc": "Manager profiles, career records, and personal bests.",
        "href": "/manager_profiles", "color": "#1F5E3B", "soon": False,
        "room_class": "hq-room-locker",
        "illo_bg": "linear-gradient(160deg,#EEF7EF 0%,#80CC80 100%)",
        "illo_main": "👕", "illo_l": "🪖", "illo_r": "🏅",
    },
    {
        "icon": "🥊", "title": "Rivalry Arena",
        "desc": "Every grudge. Every bragging right. Head-to-head history.",
        "href": "/rivalries", "color": "#E86AA6", "soon": False,
        "room_class": "hq-room-rivalry",
        "illo_bg": "linear-gradient(160deg,#FEF0F8 0%,#F080C0 100%)",
        "illo_main": "⚔️", "illo_l": "🥊", "illo_r": "🔥",
    },
    {
        "icon": "🎯", "title": "Achievement Wall",
        "desc": "Badges, stickers, and collectible achievements. Coming soon!",
        "href": "#", "color": "#9966CC", "soon": True,
        "room_class": "hq-room-achievement",
        "illo_bg": "linear-gradient(160deg,#F0EEF8 0%,#C8B8E8 100%)",
        "illo_main": "🎯", "illo_l": "🏅", "illo_r": "⭐",
    },
    {
        "icon": "📋", "title": "Draft Room",
        "desc": "Snake draft history, first-round picks, and draft day chaos. Coming soon!",
        "href": "#", "color": "#7B5EA7", "soon": True,
        "room_class": "hq-room-draft",
        "illo_bg": "linear-gradient(160deg,#F5F0FF 0%,#B8A0E0 100%)",
        "illo_main": "📋", "illo_l": "🍕", "illo_r": "✏️",
    },
]


def _room_card(room: dict) -> str:
    soon     = room["soon"]
    soon_cls = " coming-soon" if soon else ""
    href     = room["href"]
    target   = ' target="_self"' if not soon else ""
    title_c  = "#999" if soon else "#222"
    enter    = (
        f'<div class="hq-enter-btn" style="background:{room["color"]};">Enter →</div>'
        if not soon else
        '<div style="font-size:0.68rem;color:#CCC;font-family:Nunito,sans-serif;'
        'font-weight:800;text-transform:uppercase;letter-spacing:1.5px;margin-top:auto;">Coming Soon</div>'
    )
    return (
        f'<div><a href="{href}"{target} class="hq-explore-card {room["room_class"]}{soon_cls}">'
        f'<div class="hq-room-illo" style="background:{room["illo_bg"]};">'
        f'<span class="hq-illo-side">{room["illo_l"]}</span>'
        f'<span class="hq-illo-main">{room["illo_main"]}</span>'
        f'<span class="hq-illo-side">{room["illo_r"]}</span>'
        f'</div>'
        f'<div class="hq-explore-card-body">'
        f'<div class="hq-explore-room-title" style="color:{title_c};">{room["title"]}</div>'
        f'<div class="hq-explore-room-desc">{room["desc"]}</div>'
        f'{enter}'
        f'</div>'
        f'</a></div>'
    )


cols_row1 = st.columns(3, gap="medium")
for col, room in zip(cols_row1, ROOMS[:3]):
    with col:
        md_html(_room_card(room))

cols_row2 = st.columns(3, gap="medium")
for col, room in zip(cols_row2, ROOMS[3:]):
    with col:
        md_html(_room_card(room))

# ══════════════════════════════════════════════════════════════════════════
# 4. CLUBHOUSE ACTIVITY — bulletin + rivalry spotlight
# ══════════════════════════════════════════════════════════════════════════
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">📍</span></div>')

col_bull, col_rival = st.columns(2, gap="medium")

# ── What's Happening (3 most recent events) ───────────────────────────────
with col_bull:
    items_html = "".join(
        f'<div class="hq-bulletin-item"><span class="hq-bulletin-pin">{icon}</span><span>{text}</span></div>'
        for icon, text in RECENT_EVENTS[:3]
    )
    md_html(
        f"""<div class="hq-bulletin">
<div class="hq-bulletin-header">📌 &nbsp; What's Happening</div>
{items_html}
</div>"""
    )

# ── Rivalry Spotlight — big helmets, big score ────────────────────────────
with col_rival:
    ra, rb    = rivalry["manager_a"], rivalry["manager_b"]
    ca, cb    = rivalry["color_a"],   rivalry["color_b"]
    ea, eb    = rivalry["emoji_a"],   rivalry["emoji_b"]
    ta, tb    = rivalry["total_a_wins"], rivalry["total_b_wins"]
    streak    = rivalry["streak_holder"]
    streak_ct = rivalry["streak_count"]

    streak_html = ""
    if streak and streak_ct:
        sc = ca if streak == ra else cb
        streak_html = (
            f'<div style="font-family:Nunito,sans-serif;font-size:0.8rem;color:{sc};'
            f'font-weight:800;text-align:center;margin-bottom:0.6rem;">'
            f'🔥 {streak} on a {streak_ct}-game streak</div>'
        )

    btn_s = (
        "display:block;text-align:center;padding:0.75rem 1.5rem;margin-top:0.9rem;"
        "background:#0A5EA8;color:white;border-radius:24px;"
        "font-family:'Nunito',sans-serif;font-weight:900;font-size:0.9rem;"
        "text-decoration:none;box-shadow:0 4px 14px rgba(10,94,168,0.28);"
    )
    md_html(
        f"""<div style="background:#FFFDF8;border-radius:18px;padding:1.4rem 1.3rem;box-shadow:0 4px 20px rgba(0,0,0,0.07);border-top:5px solid {ca};height:100%;">
<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.9rem;">
<span style="font-size:1.3rem;">⚔️</span>
<div>
<div style="font-family:'Fredoka One',cursive;font-size:1.1rem;color:#333;">Rivalry Spotlight</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#AAA;font-weight:700;">Today's featured matchup</div>
</div>
</div>
<div style="display:flex;align-items:center;justify-content:center;gap:1rem;margin:0 0 0.6rem;">
<div style="text-align:center;">
<div style="width:72px;height:72px;border-radius:50%;background:{ca};display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 0.3rem;box-shadow:0 4px 16px rgba(0,0,0,0.12);">{ea}</div>
<div style="font-family:'Fredoka One',cursive;font-size:1rem;color:{ca};">{ra}</div>
</div>
<div style="text-align:center;padding:0 0.5rem;">
<div style="font-family:'Fredoka One',cursive;font-size:3rem;color:#333;line-height:1;">{ta}–{tb}</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.55rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:#CCC;">All Time</div>
</div>
<div style="text-align:center;">
<div style="width:72px;height:72px;border-radius:50%;background:{cb};display:flex;align-items:center;justify-content:center;font-size:2.2rem;margin:0 auto 0.3rem;box-shadow:0 4px 16px rgba(0,0,0,0.12);">{eb}</div>
<div style="font-family:'Fredoka One',cursive;font-size:1rem;color:{cb};">{rb}</div>
</div>
</div>
{streak_html}
<div><a href="/rivalries" target="_self" style="{btn_s}">See Rivalry Arena →</a></div>
</div>"""
    )

# ══════════════════════════════════════════════════════════════════════════
# 5. CHAMPION SHELF — museum exhibit
# ══════════════════════════════════════════════════════════════════════════
md_html('<div class="hq-chalk-divider"><span class="hq-chalk-divider-icon">🏅</span></div>')

trophy_icons = {"Shawn": "🏆", "Jennifer": "⭐", "Daphne": "✨", "Elliot": "🩷"}

shelf_items = ""
for _, row in champions.iterrows():
    mgr   = row["champion_manager"]
    color = MANAGER_COLORS.get(mgr, "#0A5EA8")
    icon  = trophy_icons.get(mgr, "🏆")
    shelf_items += (
        f'<div class="hq-trophy-item">'
        f'<span class="hq-trophy-item-icon">{icon}</span>'
        f'<div class="hq-trophy-item-year">{int(row["season"])}</div>'
        f'<div class="hq-trophy-item-name" style="color:{color};">{mgr}</div>'
        f'<div class="hq-trophy-item-team">{row["champion_team"]}</div>'
        f'</div>\n'
    )

shelf_items += (
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
<div class="hq-shelf-sub">Every trophy. Every season. The museum never forgets.</div>
<div class="hq-shelf-rail">
{shelf_items}
</div>
<div class="hq-shelf-plank"></div>
</div>"""
)

# ══════════════════════════════════════════════════════════════════════════
# 6. FOOTER
# ══════════════════════════════════════════════════════════════════════════
md_html(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
<div style="font-size:1.8rem;margin-bottom:0.5rem;">🏈</div>
<div style="font-family:'Fredoka One',cursive;font-size:1.15rem;color:#0A5EA8;margin-bottom:0.3rem;">Espinosa Fantasy Football Clubhouse</div>
<div style="font-family:'Nunito',sans-serif;font-size:0.7rem;color:#CCC;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Est. 2023 &bull; Family is the whole league</div>
</div>"""
)
