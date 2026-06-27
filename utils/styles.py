"""CSS injection and reusable HTML components — Playbook HQ design."""
from __future__ import annotations
import base64 as _b64
import streamlit as st
from utils.data import MANAGER_COLORS, MANAGER_LIGHT_COLORS, MANAGER_EMOJI

# ── Playbook background texture (X's and O's at ~10% fill opacity) ──────────
_BG_SVG = (
    b"<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'>"
    b"<text x='8' y='50' font-size='28' fill='#4A6741' fill-opacity='0.11'"
    b" font-family='Georgia,serif' font-weight='bold'>X</text>"
    b"<circle cx='92' cy='90' r='16' fill='none' stroke='#4A6741'"
    b" stroke-opacity='0.08' stroke-width='2.5'/>"
    b"</svg>"
)
_BG_URI = "data:image/svg+xml;base64," + _b64.b64encode(_BG_SVG).decode()
_BG_CSS = (
    ".stApp,.main{"
    f"background-image:url('{_BG_URI}') !important;"
    "background-repeat:repeat !important;"
    "}"
)

_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Fredoka+One&family=Nunito:wght@400;600;700;800;900&display=swap"
)

_CSS = """
/* ── BASE ─────────────────────────────────────────────────────── */
.stApp, .main { background: #F6F1E7 !important; }
#MainMenu  { visibility: hidden; }
footer     { visibility: hidden; }
header     { visibility: hidden; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.main .block-container {
    padding-top: 88px !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
    max-width: 1300px;
}

div[data-testid="stMarkdownContainer"] p {
    font-family: 'Nunito', sans-serif;
    color: #333;
}

/* ── NAV ──────────────────────────────────────────────────────── */
.hq-nav {
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 9999;
    background: #FFFDF8;
    border-bottom: 2px solid #D9D7CF;
    display: flex;
    align-items: center;
    padding: 0 2rem;
    height: 66px;
    gap: 0.45rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    overflow-x: auto;
    flex-wrap: nowrap;
}

.hq-nav-brand {
    font-family: 'Fredoka One', cursive;
    font-size: 1.2rem;
    color: #0A5EA8;
    text-decoration: none !important;
    margin-right: 0.6rem;
    white-space: nowrap;
    flex-shrink: 0;
}

.hq-tab {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.76rem;
    color: #555 !important;
    text-decoration: none !important;
    padding: 5px 12px;
    border-radius: 20px;
    border: 2px solid #D9D7CF;
    background: #FFFDF8;
    white-space: nowrap;
    transition: all 0.18s ease;
    display: inline-block;
    flex-shrink: 0;
}

.hq-tab:hover {
    background: #0A5EA8 !important;
    color: white !important;
    border-color: #0A5EA8;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(10,94,168,0.25);
}

.hq-tab.active {
    background: #0A5EA8 !important;
    color: white !important;
    border-color: #0A5EA8;
    box-shadow: 0 4px 12px rgba(10,94,168,0.2);
}

.hq-tab-soon {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.72rem;
    color: #BBB !important;
    padding: 5px 12px;
    border-radius: 20px;
    border: 2px dashed #D9D7CF;
    background: transparent;
    white-space: nowrap;
    flex-shrink: 0;
}

/* ── HERO (CSS fallback) ──────────────────────────────────────── */
.hq-hero {
    width: 100%;
    border-radius: 22px;
    background: linear-gradient(135deg, #0A5EA8 0%, #1F5E3B 60%, #D6A319 100%);
    min-height: 240px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    margin-bottom: 1.25rem;
}

.hq-hero-title {
    font-family: 'Fredoka One', cursive;
    font-size: 2.8rem;
    color: white;
    line-height: 1.1;
    text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    margin: 0;
}

.hq-hero-taglines {
    font-family: 'Nunito', sans-serif;
    font-size: 1.05rem;
    color: rgba(255,255,255,0.9);
    font-weight: 700;
    margin-top: 0.65rem;
}

.hq-hero-sub {
    font-family: 'Nunito', sans-serif;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.68);
    font-weight: 700;
    margin-top: 0.4rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* Hero image override */
.stImage img {
    border-radius: 22px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
    margin-bottom: 0.25rem;
}

/* ── CARDS ────────────────────────────────────────────────────── */
.hq-card {
    background: #FFFDF8;
    border-radius: 20px;
    padding: 1.5rem 1.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-top: 5px solid #0A5EA8;
    height: 100%;
    box-sizing: border-box;
}

.hq-card-title {
    font-family: 'Fredoka One', cursive;
    font-size: 1.05rem;
    color: #333;
    margin: 0 0 0.2rem;
}

.hq-card-icon { font-size: 2rem; margin-bottom: 0.4rem; display: block; }

.hq-big-name {
    font-family: 'Fredoka One', cursive;
    font-size: 2rem;
    line-height: 1.1;
    margin: 0.2rem 0 0.05rem;
}

.hq-team-name {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: #777;
    margin: 0.1rem 0;
    font-style: italic;
}

.hq-score-line {
    font-family: 'Nunito', sans-serif;
    font-size: 0.8rem;
    color: #999;
    margin-top: 0.2rem;
}

.hq-section-label {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.64rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #999;
    margin-bottom: 0.1rem;
}

/* ── BUTTONS ──────────────────────────────────────────────────── */
.hq-btn {
    display: inline-block;
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.78rem;
    color: white !important;
    background: #0A5EA8;
    padding: 7px 16px;
    border-radius: 20px;
    text-decoration: none !important;
    margin-top: 0.9rem;
    transition: all 0.18s;
    letter-spacing: 0.3px;
}

.hq-btn:hover {
    opacity: 0.85;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(10,94,168,0.3);
}

/* ── PAGE HEADER ──────────────────────────────────────────────── */
.hq-page-header {
    padding: 1.2rem 0 1rem;
    border-bottom: 3px solid #D9D7CF;
    margin-bottom: 1.5rem;
}

.hq-page-room {
    font-family: 'Nunito', sans-serif;
    font-size: 0.68rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #AAA;
    margin-bottom: 0.2rem;
}

.hq-page-title {
    font-family: 'Fredoka One', cursive;
    font-size: 2.8rem;
    color: #0A5EA8;
    margin: 0;
    line-height: 1.05;
}

.hq-page-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 0.88rem;
    color: #777;
    font-weight: 600;
    margin-top: 0.25rem;
}

/* ── SECTION HEADER ───────────────────────────────────────────── */
.hq-section-title {
    font-family: 'Fredoka One', cursive;
    font-size: 1.55rem;
    color: #222;
    margin: 0 0 0.1rem;
}

.hq-section-sub {
    font-family: 'Nunito', sans-serif;
    font-size: 0.82rem;
    color: #888;
    font-weight: 600;
}

/* ── LEADERBOARD ──────────────────────────────────────────────── */
.hq-lb-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid #EEE8E0;
}

.hq-lb-row:last-child { border-bottom: none; }

.hq-lb-rank {
    font-family: 'Fredoka One', cursive;
    font-size: 1.2rem;
    color: #CCC;
    min-width: 1.4rem;
    text-align: center;
    flex-shrink: 0;
}

.hq-lb-rank.gold   { color: #D6A319; }
.hq-lb-rank.silver { color: #9E9E9E; }
.hq-lb-rank.bronze { color: #C87941; }

.hq-lb-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}

.hq-lb-info { flex: 1; min-width: 0; }

.hq-lb-name {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.9rem;
    color: #222;
}

.hq-lb-record {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    color: #999;
}

.hq-lb-trophy { font-size: 0.9rem; flex-shrink: 0; }

/* ── CHAMPION CARD ────────────────────────────────────────────── */
.hq-champ-card {
    background: #FFFDF8;
    border-radius: 24px;
    padding: 2.2rem 1.8rem;
    text-align: center;
    box-shadow: 0 8px 40px rgba(0,0,0,0.1);
    border: 3px solid #D6A319;
    position: relative;
    overflow: hidden;
}

.hq-champ-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 6px;
    background: linear-gradient(to right, #D6A319, #F5C842, #D6A319);
}

.hq-champ-trophy  { font-size: 4.5rem; display: block; margin-bottom: 0.4rem; }
.hq-champ-season  {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #999;
}

.hq-champ-name {
    font-family: 'Fredoka One', cursive;
    font-size: 2.8rem;
    line-height: 1.05;
    margin: 0.3rem 0 0.1rem;
}

.hq-champ-team {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #666;
    font-style: italic;
}

.hq-champ-score {
    font-family: 'Nunito', sans-serif;
    font-size: 0.82rem;
    color: #999;
    margin-top: 0.35rem;
}

.hq-champ-tagline {
    font-family: 'Nunito', sans-serif;
    font-style: italic;
    font-size: 0.88rem;
    color: #888;
    margin-top: 0.65rem;
    line-height: 1.45;
    padding: 0 0.5rem;
}

/* Small champion card (archive/list views) */
.hq-mini-champ {
    background: #FFFDF8;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
    box-shadow: 0 3px 14px rgba(0,0,0,0.07);
    border-top: 4px solid #D6A319;
}

.hq-mini-champ-year {
    font-family: 'Fredoka One', cursive;
    font-size: 1.4rem;
    color: #D6A319;
    line-height: 1;
}

.hq-mini-champ-name {
    font-family: 'Fredoka One', cursive;
    font-size: 1.2rem;
    margin: 0.25rem 0 0.1rem;
}

.hq-mini-champ-team {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.72rem;
    color: #888;
    font-style: italic;
}

.hq-mini-champ-score {
    font-family: 'Nunito', sans-serif;
    font-size: 0.7rem;
    color: #AAA;
    margin-top: 0.15rem;
}

/* ── RIVALRY CARD ─────────────────────────────────────────────── */
.hq-rivalry-card {
    background: #FFFDF8;
    border-radius: 18px;
    padding: 1.3rem 1.2rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    border-top: 5px solid #E86AA6;
    margin-bottom: 0.75rem;
}

.hq-rivalry-vs {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.4rem;
    margin: 0.6rem 0;
}

.hq-rivalry-manager {
    font-family: 'Fredoka One', cursive;
    font-size: 1.5rem;
    text-align: center;
    flex: 1;
    line-height: 1.1;
}

.hq-rivalry-score {
    font-family: 'Fredoka One', cursive;
    font-size: 1.9rem;
    color: #333;
    text-align: center;
    flex-shrink: 0;
}

.hq-rivalry-divider {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    font-weight: 800;
    color: #CCC;
    text-transform: uppercase;
    text-align: center;
}

/* ── BADGES ───────────────────────────────────────────────────── */
.hq-badge {
    display: inline-flex;
    align-items: center;
    gap: 3px;
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.68rem;
    padding: 2px 8px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}

.hq-badge-gold   { background: #FEF5DC; color: #B8860B; border: 1px solid #D6A319; }
.hq-badge-green  { background: #E3F0E8; color: #1F5E3B; border: 1px solid #1F5E3B; }
.hq-badge-blue   { background: #E3EDF8; color: #0A5EA8; border: 1px solid #0A5EA8; }
.hq-badge-pink   { background: #FDE8F3; color: #C94B87; border: 1px solid #E86AA6; }
.hq-badge-navy   { background: #E3E8F0; color: #002244; border: 1px solid #002244; }

/* ── FEED ─────────────────────────────────────────────────────── */
.hq-feed-item {
    display: flex;
    align-items: flex-start;
    gap: 0.7rem;
    padding: 0.55rem 0;
    border-bottom: 1px solid #EEE8E0;
    font-family: 'Nunito', sans-serif;
    font-size: 0.84rem;
    color: #444;
    line-height: 1.4;
}

.hq-feed-item:last-child { border-bottom: none; }
.hq-feed-icon { font-size: 1.05rem; flex-shrink: 0; margin-top: 1px; }

/* ── TABLE ────────────────────────────────────────────────────── */
.hq-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Nunito', sans-serif;
    font-size: 0.88rem;
}

.hq-table th {
    font-weight: 800;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #AAA;
    padding: 0.5rem 0.75rem;
    border-bottom: 2px solid #EEE8E0;
    text-align: left;
}

.hq-table td {
    padding: 0.58rem 0.75rem;
    color: #333;
    border-bottom: 1px solid #F2EDE6;
}

.hq-table tr:last-child td { border-bottom: none; }
.hq-table tr:hover td { background: rgba(10,94,168,0.025); }
.hq-table .bold   { font-weight: 800; }
.hq-table .muted  { color: #AAA; }
.hq-table .center { text-align: center; }
.hq-table .right  { text-align: right; }
.hq-table .gold   { color: #D6A319; font-weight: 800; }
.hq-table .green  { color: #1F5E3B; font-weight: 800; }

/* ── MANAGER PROFILE CARD ─────────────────────────────────────── */
.hq-profile-card {
    background: #FFFDF8;
    border-radius: 20px;
    padding: 1.8rem 1.4rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-top: 5px solid #0A5EA8;
    height: 100%;
}

.hq-avatar {
    width: 76px; height: 76px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.3rem;
    margin: 0 auto 0.7rem;
    border: 3px solid rgba(255,255,255,0.5);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.hq-profile-name {
    font-family: 'Fredoka One', cursive;
    font-size: 1.9rem;
    line-height: 1.05;
    margin: 0.1rem 0 0;
}

.hq-profile-team {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 0.8rem;
    color: #888;
    font-style: italic;
    margin-bottom: 0.75rem;
}

.hq-stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
    margin-top: 0.7rem;
}

.hq-stat-box {
    background: #F6F1E7;
    border-radius: 12px;
    padding: 0.55rem 0.4rem;
    text-align: center;
}

.hq-stat-value {
    font-family: 'Fredoka One', cursive;
    font-size: 1.55rem;
    line-height: 1;
}

.hq-stat-label {
    font-family: 'Nunito', sans-serif;
    font-size: 0.58rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #AAA;
    margin-top: 0.15rem;
}

/* ── PLAYOFF BRACKET ──────────────────────────────────────────── */
.hq-bracket-round {
    font-family: 'Nunito', sans-serif;
    font-size: 0.65rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #AAA;
    margin-bottom: 0.4rem;
    margin-top: 0.75rem;
}

.hq-bracket-game {
    background: #FFFDF8;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 0.65rem;
}

.hq-bracket-team {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.55rem 0.85rem;
    font-family: 'Nunito', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    border-bottom: 1px solid #F2EDE6;
}

.hq-bracket-team:last-child { border-bottom: none; }
.hq-bracket-team.winner { background: #F0FAF3; }
.hq-bracket-team.loser  { color: #BBB; }

.hq-bracket-score {
    font-family: 'Fredoka One', cursive;
    font-size: 1.05rem;
}

.hq-bracket-team.winner .hq-bracket-score { color: #1F5E3B; }
.hq-bracket-team.loser  .hq-bracket-score { color: #CCC; }

/* ── DRAFT PICK ───────────────────────────────────────────────── */
.hq-pick-card {
    background: #FFFDF8;
    border-radius: 12px;
    padding: 0.7rem 0.9rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border-left: 4px solid #D6A319;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 0.65rem;
}

.hq-pick-num {
    font-family: 'Fredoka One', cursive;
    font-size: 1rem;
    color: #D6A319;
    min-width: 1.6rem;
    text-align: center;
}

.hq-pick-player {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.88rem;
    color: #222;
}

.hq-pick-team {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    color: #888;
}

/* ── QUOTE CARD ───────────────────────────────────────────────── */
.hq-quote-card {
    background: linear-gradient(135deg, #0A5EA8 0%, #1F5E3B 100%);
    border-radius: 20px;
    padding: 1.8rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(10,94,168,0.2);
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.hq-quote-text {
    font-family: 'Fredoka One', cursive;
    font-size: 1.4rem;
    color: white;
    line-height: 1.3;
    margin-bottom: 0.4rem;
}

.hq-quote-attr {
    font-family: 'Nunito', sans-serif;
    font-size: 0.7rem;
    color: rgba(255,255,255,0.6);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── HIGHLIGHT BOX ────────────────────────────────────────────── */
.hq-highlight {
    background: #FFFDF8;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    border-left: 5px solid #D6A319;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 0.5rem;
    font-family: 'Nunito', sans-serif;
    font-size: 0.85rem;
    color: #444;
    line-height: 1.4;
}

/* ── SELECTBOX ────────────────────────────────────────────────── */
.stSelectbox > label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    color: #666 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

div[data-baseweb="select"] {
    background: #FFFDF8 !important;
    border-radius: 12px !important;
}

/* ── RESPONSIVE ───────────────────────────────────────────────── */
@media (max-width: 768px) {
    .main .block-container {
        padding-top: 72px !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .hq-nav { padding: 0 1rem; height: 54px; }
    .hq-hero-title { font-size: 1.9rem; }
    .hq-page-title { font-size: 2.1rem; }
    .hq-champ-name { font-size: 2rem; }
}

/* ═══════════════════════════════════════════════════════════════
   PHASE 2 — Playbook HQ Experience Layer
   ═══════════════════════════════════════════════════════════════ */

/* ── NAV SIGN STYLE (override pill → sign) ─────────────────────── */
.hq-tab {
    padding: 7px 15px !important;
    border-radius: 10px !important;
    font-size: 0.8rem !important;
    box-shadow: 0 2px 0 rgba(0,0,0,0.07);
}
.hq-tab:hover {
    box-shadow: 0 4px 0 rgba(10,94,168,0.3) !important;
    transform: translateY(-2px) !important;
}
.hq-tab.active {
    box-shadow: 0 3px 0 rgba(10,94,168,0.25) !important;
}
.hq-tab-soon {
    border-radius: 10px !important;
    padding: 7px 14px !important;
    font-size: 0.78rem !important;
}

/* ── HERO ─────────────────────────────────────────────────────── */
/* Image hero: rounded + shadow applied to stImage */
.hq-hero-img-wrap img,
.stImage > img {
    border-radius: 22px !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.14) !important;
}

/* Text-only hero (no image) */
.hq-hero-text {
    text-align: center;
    padding: 3.5rem 2rem 2rem;
}

.hq-hero-emoji { font-size: 4rem; display: block; margin-bottom: 0.75rem; }

.hq-hero-title-text {
    font-family: 'Fredoka One', cursive;
    font-size: 3.2rem;
    color: #0A5EA8;
    line-height: 1.1;
    margin: 0;
}

.hq-hero-tagline-text {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #666;
    margin-top: 0.5rem;
}

.hq-hero-sub-text {
    font-family: 'Nunito', sans-serif;
    font-size: 0.75rem;
    color: #AAA;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.3rem;
}

/* ── FEATURED CHAMPION (home page star card) ────────────────────── */
.hq-champ-featured {
    background: #FFFDF8;
    border-radius: 26px;
    padding: 2.75rem 2.5rem 2.25rem;
    text-align: center;
    box-shadow: 0 12px 56px rgba(214,163,25,0.18), 0 4px 24px rgba(0,0,0,0.07);
    border: 2px solid #D6A319;
    position: relative;
    overflow: hidden;
    max-width: 720px;
    margin: 0 auto;
}

.hq-champ-featured::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 7px;
    background: linear-gradient(90deg, #D6A319 0%, #F5C842 45%, #D6A319 100%);
}

/* Confetti corner decorations */
.hq-confetti-tl {
    position: absolute;
    top: 0.9rem; left: 1.1rem;
    font-size: 1.3rem;
    opacity: 0.22;
    user-select: none;
    pointer-events: none;
    line-height: 1;
}

.hq-confetti-tr {
    position: absolute;
    top: 0.9rem; right: 1.1rem;
    font-size: 1.3rem;
    opacity: 0.22;
    user-select: none;
    pointer-events: none;
    line-height: 1;
}

.hq-champ-featured-trophy { font-size: 6.5rem; display: block; margin-bottom: 0.3rem; }

.hq-champ-featured-label {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 3.5px;
    color: #D6A319;
    margin-bottom: 0.1rem;
}

.hq-champ-featured-name {
    font-family: 'Fredoka One', cursive;
    font-size: 4rem;
    line-height: 1.05;
    margin: 0.2rem 0 0.1rem;
}

.hq-champ-featured-team {
    font-family: 'Nunito', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #777;
    font-style: italic;
}

.hq-champ-featured-score {
    font-family: 'Nunito', sans-serif;
    font-size: 0.85rem;
    color: #AAA;
    margin-top: 0.3rem;
}

.hq-champ-featured-tagline {
    font-family: 'Nunito', sans-serif;
    font-style: italic;
    font-size: 0.9rem;
    color: #888;
    margin: 0.85rem auto 0;
    max-width: 440px;
    line-height: 1.45;
}

/* ── CHALKBOARD QUOTE ─────────────────────────────────────────── */
.hq-chalkboard {
    background: #2B4A2B;
    border-radius: 18px;
    padding: 2rem 1.75rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.18), inset 0 0 50px rgba(0,0,0,0.15);
    border: 4px solid #3D6B3D;
    height: 100%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
}

/* Chalk texture lines */
.hq-chalkboard::before {
    content: '';
    position: absolute;
    inset: 12px;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    pointer-events: none;
}

.hq-chalkboard-icon { font-size: 1.8rem; margin-bottom: 0.6rem; opacity: 0.85; }

.hq-chalkboard-text {
    font-family: 'Fredoka One', cursive;
    font-size: 1.35rem;
    color: rgba(255,255,255,0.92);
    line-height: 1.35;
}

.hq-chalkboard-line {
    width: 60px;
    height: 2px;
    background: rgba(255,255,255,0.2);
    margin: 0.65rem auto 0.5rem;
    border-radius: 1px;
}

.hq-chalkboard-attr {
    font-family: 'Nunito', sans-serif;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.38);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ── BULLETIN BOARD (What's Happening) ─────────────────────────── */
.hq-bulletin {
    background: #FBF4E3;
    border-radius: 18px;
    padding: 1.4rem 1.4rem 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07), 0 0 0 2px #E8D9B5;
    height: 100%;
    box-sizing: border-box;
}

.hq-bulletin-header {
    font-family: 'Fredoka One', cursive;
    font-size: 1.05rem;
    color: #7A5C1E;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.hq-bulletin-item {
    background: white;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: flex-start;
    gap: 0.55rem;
    font-family: 'Nunito', sans-serif;
    font-size: 0.83rem;
    font-weight: 600;
    color: #444;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 0 0 1px rgba(0,0,0,0.03);
    line-height: 1.35;
}

.hq-bulletin-item:last-child { margin-bottom: 0; }
.hq-bulletin-pin { font-size: 0.9rem; flex-shrink: 0; margin-top: 1px; }

/* ── FOOTBALL DIVIDER ─────────────────────────────────────────── */
.hq-divider-football {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 1.5rem 0;
    color: #D9D7CF;
    font-size: 1.1rem;
    user-select: none;
}

.hq-divider-football::before,
.hq-divider-football::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #E5E0D8;
}

/* ── TROPHY SHELF ─────────────────────────────────────────────── */
.hq-trophy-shelf-wrap {
    background: #FFFDF8;
    border-radius: 20px;
    padding: 1.75rem 1.5rem 0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    overflow: hidden;
}

.hq-shelf-label {
    font-family: 'Fredoka One', cursive;
    font-size: 1.4rem;
    color: #333;
    margin-bottom: 0.1rem;
}

.hq-shelf-sub {
    font-family: 'Nunito', sans-serif;
    font-size: 0.8rem;
    color: #AAA;
    font-weight: 600;
    margin-bottom: 1.25rem;
}

.hq-shelf-rail {
    display: flex;
    justify-content: center;
    gap: 0;
    flex-wrap: nowrap;
}

.hq-trophy-item {
    flex: 1;
    text-align: center;
    padding: 0.5rem 0.5rem 1.25rem;
    transition: transform 0.2s;
}

.hq-trophy-item:hover { transform: translateY(-4px); }

.hq-trophy-item-icon { font-size: 3.5rem; display: block; line-height: 1; }

.hq-trophy-item-year {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #CCC;
    margin-top: 0.5rem;
}

.hq-trophy-item-name {
    font-family: 'Fredoka One', cursive;
    font-size: 1.25rem;
    line-height: 1.1;
    margin-top: 0.2rem;
}

.hq-trophy-item-team {
    font-family: 'Nunito', sans-serif;
    font-size: 0.68rem;
    color: #AAA;
    font-style: italic;
    margin-top: 0.1rem;
}

.hq-trophy-item.coming-soon .hq-trophy-item-icon { filter: grayscale(1) opacity(0.25); }
.hq-trophy-item.coming-soon .hq-trophy-item-name { color: #CCC; }

/* The shelf plank */
.hq-shelf-plank {
    height: 10px;
    background: linear-gradient(180deg, #C8A870 0%, #B08A52 60%, #96703C 100%);
    border-radius: 0 0 4px 4px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.18);
    margin: 0 -1.5rem;
}

/* ── EXPLORE SECTION ──────────────────────────────────────────── */
.hq-explore-header {
    text-align: center;
    padding: 1rem 0 1.4rem;
}

.hq-explore-title-text {
    font-family: 'Fredoka One', cursive;
    font-size: 2rem;
    color: #333;
}

.hq-explore-sub {
    font-family: 'Nunito', sans-serif;
    font-size: 0.85rem;
    color: #888;
    font-weight: 600;
    margin-top: 0.2rem;
}

.hq-explore-card {
    background: #FFFDF8;
    border-radius: 20px;
    padding: 2rem 1.25rem 1.75rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    text-decoration: none !important;
    display: block;
    transition: all 0.2s ease;
    border: 2px solid transparent;
    height: 100%;
    box-sizing: border-box;
}

.hq-explore-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 36px rgba(0,0,0,0.11);
    border-color: #D9D7CF;
}

.hq-explore-icon { font-size: 3.2rem; display: block; margin-bottom: 0.6rem; }

.hq-explore-room-title {
    font-family: 'Fredoka One', cursive;
    font-size: 1.2rem;
    color: #222;
    margin-bottom: 0.25rem;
}

.hq-explore-room-desc {
    font-family: 'Nunito', sans-serif;
    font-size: 0.75rem;
    color: #999;
    font-weight: 600;
    line-height: 1.4;
}

.hq-explore-arrow {
    font-family: 'Nunito', sans-serif;
    font-weight: 800;
    font-size: 0.8rem;
    margin-top: 0.75rem;
    display: block;
}

.hq-explore-card.coming-soon {
    opacity: 0.45;
    cursor: default;
}

.hq-explore-card.coming-soon:hover {
    transform: none;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
    border-color: transparent;
}

/* ── MOBILE RESPONSIVE (phase 2 additions) ──────────────────────── */
@media (max-width: 768px) {
    .hq-champ-featured-name { font-size: 2.8rem; }
    .hq-champ-featured-trophy { font-size: 5rem; }
    .hq-shelf-rail { flex-wrap: wrap; }
    .hq-trophy-item { min-width: 120px; }
}
"""

# ── PHASE 3 — Atmosphere, Polish & Premium Feel ─────────────────────────────
_CSS += """

/* ── BLOCK CONTAINER — reduce top padding ──────────────────────────────────── */
.main .block-container { padding-top: 80px !important; }

/* ── NAV — hand-painted wooden clubhouse signs ─────────────────────────────── */
.hq-nav {
    background: linear-gradient(180deg, #FFFAF0 0%, #F2E8D0 100%) !important;
    border-bottom: 3px solid #C8A870 !important;
    box-shadow: 0 3px 20px rgba(0,0,0,0.09), inset 0 -1px 0 rgba(200,168,112,0.4) !important;
}
.hq-tab {
    background: linear-gradient(180deg, #FFFDF5 0%, #EFE4C8 100%) !important;
    border-color: #C8A870 !important;
    border-radius: 7px !important;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06), 0 2px 0 rgba(155,115,50,0.45) !important;
    color: #5A4428 !important;
    font-weight: 900 !important;
    font-size: 0.78rem !important;
    padding: 7px 14px !important;
    letter-spacing: 0.2px;
}
.hq-tab:hover {
    background: linear-gradient(180deg, #1472C8 0%, #0A5EA8 100%) !important;
    color: white !important;
    border-color: #074899 !important;
    box-shadow: 0 4px 0 rgba(4,48,110,0.4), 0 7px 20px rgba(10,94,168,0.28) !important;
    transform: translateY(-2px) !important;
}
.hq-tab.active {
    background: linear-gradient(180deg, #1472C8 0%, #0A5EA8 100%) !important;
    color: white !important;
    border-color: #074899 !important;
    box-shadow: 0 3px 0 rgba(4,48,110,0.35), 0 5px 16px rgba(10,94,168,0.25) !important;
}
.hq-tab-soon {
    border-radius: 7px !important;
    border-color: #D9D0BC !important;
    color: #B8A890 !important;
    font-size: 0.75rem !important;
    padding: 7px 13px !important;
}

/* ── CHAMPION CARD — trophy room centerpiece ───────────────────────────────── */
.hq-champ-featured {
    background: linear-gradient(160deg, #FFFEF9 0%, #FFFBF0 60%, #FFF8E4 100%) !important;
    box-shadow: 0 20px 72px rgba(214,163,25,0.22), 0 8px 32px rgba(0,0,0,0.06),
                inset 0 1px 0 rgba(255,255,255,0.95) !important;
}
.hq-champ-featured::before {
    height: 9px !important;
    background: linear-gradient(90deg, #A07010 0%, #D6A319 22%, #F5C842 50%,
                #D6A319 78%, #A07010 100%) !important;
}
.hq-champ-featured-trophy {
    font-size: 7rem !important;
    text-shadow: 0 0 28px rgba(214,163,25,0.55), 0 0 56px rgba(214,163,25,0.22) !important;
}
.hq-champ-featured-name  { font-size: 4.2rem !important; }

/* ── CHALK-LINE SECTION DIVIDER ─────────────────────────────────────────────── */
.hq-chalk-divider {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.75rem 0;
    user-select: none;
}
.hq-chalk-divider::before,
.hq-chalk-divider::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, #C8A870 35%, #C8A870 65%, transparent 100%);
    opacity: 0.4;
    border-radius: 1px;
}
.hq-chalk-divider-icon {
    font-size: 1rem;
    opacity: 0.65;
    filter: drop-shadow(0 1px 3px rgba(0,0,0,0.15));
}

/* ── LEADERBOARD — warm gold top ────────────────────────────────────────────── */
.hq-lb-gold { background: linear-gradient(160deg,#FFFBEC 0%,#FFF8E0 100%) !important; }

/* ── TROPHY SHELF ───────────────────────────────────────────────────────────── */
.hq-trophy-shelf-wrap {
    background: linear-gradient(180deg, #FFFDF8 0%, #FFF8EC 100%) !important;
    border-top: 5px solid #C8A870 !important;
}
.hq-trophy-item-icon { filter: drop-shadow(0 2px 8px rgba(214,163,25,0.28)); }

/* ── EXPLORE CARDS — room entrances ─────────────────────────────────────────── */
.hq-explore-card {
    min-height: 185px !important;
    border-top-width: 4px !important;
    border-top-style: solid !important;
    border-top-color: #D9D7CF !important;
    border-radius: 20px !important;
    transition: all 0.22s ease !important;
}
.hq-explore-card:hover {
    transform: translateY(-7px) !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.12) !important;
}
.hq-explore-icon       { font-size: 3.6rem !important; }
.hq-explore-room-title { font-size: 1.05rem !important; font-weight: 900 !important; }

/* Per-room backgrounds and accent colours */
.hq-room-trophy      { background: linear-gradient(160deg,#FFFBEC 0%,#FFF3C4 100%); border-top-color: #D6A319 !important; }
.hq-room-scrapbook   { background: linear-gradient(160deg,#EEF5FF 0%,#DAEAFF 100%); border-top-color: #0A5EA8 !important; }
.hq-room-locker      { background: linear-gradient(160deg,#EEF7EF 0%,#D4EDD4 100%); border-top-color: #1F5E3B !important; }
.hq-room-rivalry     { background: linear-gradient(160deg,#FEF0F8 0%,#FAD5EE 100%); border-top-color: #E86AA6 !important; }
.hq-room-achievement { background: #F4F2EF; border-top-color: #BBB !important; }

/* ── MOBILE ─────────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
    .hq-champ-featured-trophy { font-size: 5.5rem !important; }
    .hq-champ-featured-name   { font-size: 3rem !important; }
    .hq-explore-card          { min-height: 150px !important; }
}
"""

# ── PHASE 4 — Exploration Homepage ───────────────────────────────────────────
_CSS += """

/* Explore cards: full-width illustration banner, flex column */
.hq-explore-card {
    padding: 0 !important;
    min-height: 300px !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}
.hq-explore-card-body {
    padding: 1rem 1.2rem 1.2rem;
    display: flex;
    flex-direction: column;
    flex: 1;
    align-items: center;
    text-align: center;
    gap: 0.4rem;
}
/* Phase 3 room backgrounds move into .hq-room-illo; card body stays cream */
.hq-room-trophy, .hq-room-scrapbook, .hq-room-locker,
.hq-room-rivalry, .hq-room-achievement, .hq-room-draft {
    background: #FFFDF8 !important;
}

/* Illustration banner */
.hq-room-illo {
    height: 148px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    flex-shrink: 0;
}
.hq-illo-main {
    font-size: 4.5rem;
    line-height: 1;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.18));
}
.hq-illo-side { font-size: 1.8rem; opacity: 0.7; }

/* Enter button */
.hq-enter-btn {
    margin-top: auto;
    padding: 0.5rem 1.3rem;
    border-radius: 20px;
    font-family: 'Nunito', sans-serif;
    font-weight: 900;
    font-size: 0.82rem;
    color: white;
    display: inline-block;
    box-shadow: 0 3px 10px rgba(0,0,0,0.12);
    transition: all 0.15s;
}

/* Draft Room */
.hq-room-draft { border-top-color: #7B5EA7 !important; }

@media (max-width: 768px) {
    .hq-room-illo    { height: 110px; }
    .hq-illo-main    { font-size: 3.2rem; }
    .hq-illo-side    { font-size: 1.4rem; }
    .hq-explore-card { min-height: 220px !important; }
}
"""


def _fix_html(html: str) -> str:
    """Make HTML safe for st.markdown's CommonMark parser.

    st.markdown uses CommonMark, which has two rules that break complex HTML:
    1. An opening tag must be complete (end with >) on its FIRST line to trigger
       HTML block mode — multi-line style="" attributes break this.
    2. A blank line anywhere inside an HTML block terminates it — subsequent tags
       are then Markdown-escaped and shown as raw text.

    This function collapses newlines inside tags and removes blank lines.
    """
    import re
    # Remove HTML comments (they can confuse the block parser)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    # Collapse newlines that appear inside an opening/closing tag
    result: list[str] = []
    in_tag = False
    for ch in html:
        if ch == "<" and not in_tag:
            in_tag = True
            result.append(ch)
        elif ch == ">" and in_tag:
            in_tag = False
            result.append(ch)
        elif in_tag and ch == "\n":
            result.append(" ")   # newline inside tag → space
        else:
            result.append(ch)
    html = "".join(result)
    # Remove blank lines (they terminate HTML block mode)
    html = re.sub(r"\n[ \t]*\n", "\n", html)
    return html


def md_html(html: str) -> None:
    """Render HTML via st.markdown after fixing CommonMark HTML block issues."""
    st.markdown(_fix_html(html), unsafe_allow_html=True)


def inject_css() -> None:
    full_css = _CSS + _BG_CSS
    css = full_css.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    st.html(
        f"""<script>
(function() {{
    if (document.getElementById('hq-css')) return;
    var l = document.createElement('link');
    l.rel  = 'stylesheet';
    l.href = '{_FONTS_URL}';
    document.head.appendChild(l);
    var s = document.createElement('style');
    s.id = 'hq-css';
    s.textContent = `{css}`;
    document.head.appendChild(s);
}})();
</script>""",
        unsafe_allow_javascript=True,
    )


def render_nav(active: str = "home") -> None:
    pages = [
        ("home",             "/",                "🏠 Clubhouse"),
        ("champions",        "/champions",        "🏆 Trophy Room"),
        ("season_archive",   "/season_archive",   "📖 Scrapbook"),
        ("manager_profiles", "/manager_profiles", "👥 Locker Room"),
        ("rivalries",        "/rivalries",        "🥊 Rivalry Arena"),
    ]
    coming_soon = ["🎯 Achievements", "🗂️ Draft Room"]

    links = "".join(
        f'<a href="{href}" class="hq-tab{" active" if active == key else ""}"'
        f' target="_self">{label}</a>'
        for key, href, label in pages
    )
    soon_html = "".join(
        f'<span class="hq-tab-soon">{label}</span>' for label in coming_soon
    )

    st.markdown(
        f"""<div class="hq-nav">
            <a href="/" class="hq-nav-brand" target="_self">🏈 Espinosa FFL</a>
            {links}
            {soon_html}
        </div>""",
        unsafe_allow_html=True,
    )


def render_page_header(room: str, title: str, subtitle: str) -> None:
    st.markdown(
        f"""<div class="hq-page-header">
            <div class="hq-page-room">{room}</div>
            <div class="hq-page-title">{title}</div>
            <div class="hq-page-subtitle">{subtitle}</div>
        </div>""",
        unsafe_allow_html=True,
    )


def manager_avatar_html(manager: str, size: int = 56) -> str:
    color = MANAGER_COLORS.get(manager, "#0A5EA8")
    emoji = MANAGER_EMOJI.get(manager, "🏈")
    return (
        f'<div class="hq-avatar" '
        f'style="width:{size}px;height:{size}px;background:{color};font-size:{size // 2}px;">'
        f"{emoji}</div>"
    )


def html_table(headers: list, rows: list) -> str:
    th = "".join(f"<th>{h}</th>" for h in headers)
    tbody = "".join(
        "<tr>"
        + "".join(
            f'<td class="{v[1]}">{v[0]}</td>' if isinstance(v, tuple) else f"<td>{v}</td>"
            for v in row
        )
        + "</tr>"
        for row in rows
    )
    return (
        f"<table class='hq-table'>"
        f"<thead><tr>{th}</tr></thead>"
        f"<tbody>{tbody}</tbody>"
        f"</table>"
    )


def section_header(title: str, subtitle: str = "") -> None:
    sub = (
        f'<div class="hq-section-sub">{subtitle}</div>' if subtitle else ""
    )
    st.markdown(
        f'<div class="hq-section-title">{title}</div>{sub}',
        unsafe_allow_html=True,
    )
    st.markdown("<div style='margin-bottom:0.75rem'></div>", unsafe_allow_html=True)
