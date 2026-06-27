"""Rivalry Arena — all head-to-head matchups."""
from __future__ import annotations
import streamlit as st

from utils.data import (
    MANAGER_COLORS, MANAGER_EMOJI, RIVALRY_PAIRS,
    get_all_rivalries,
)
from utils.styles import inject_css, render_nav, render_page_header, section_header

st.set_page_config(
    page_title="Rivalry Arena · Espinosa FFL",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
render_nav("rivalries")
render_page_header(
    "🥊 THE CLUBHOUSE",
    "Rivalry Arena",
    "Every matchup. Every grudge. Every bragging right.",
)

all_rivalries = get_all_rivalries()

# ── RIVALRY CARDS ─────────────────────────────────────────────────────────

# Arrange in 2 columns of 3
left_rivals  = all_rivalries[:3]
right_rivals = all_rivalries[3:]

col_left, col_right = st.columns(2, gap="medium")


def _biggest_win_text(entry: dict | None, manager: str) -> str:
    if not entry:
        return "No wins yet"
    return (
        f"{entry['score_a']:.1f} – {entry['score_b']:.1f} "
        f"(Wk {entry['week']}, {entry['season']})"
    )


def _biggest_loss_text(entry: dict | None) -> str:
    if not entry:
        return "No losses yet"
    return (
        f"{entry['score_b']:.1f} – {entry['score_a']:.1f} "
        f"(Wk {entry['week']}, {entry['season']})"
    )


def rivalry_card_html(rv: dict) -> str:
    ra, rb   = rv["manager_a"],   rv["manager_b"]
    ca, cb   = rv["color_a"],     rv["color_b"]
    la, lb   = rv["light_a"],     rv["light_b"]
    ea, eb   = rv["emoji_a"],     rv["emoji_b"]
    rsa, rsb = rv["rs_a_wins"],   rv["rs_b_wins"]
    poa, pob = rv["po_a_wins"],   rv["po_b_wins"]
    ta,  tb  = rv["total_a_wins"], rv["total_b_wins"]

    # Who leads all-time?
    if ta > tb:
        leader_color = ca
        leader_txt   = f"{ra} leads ({ta}–{tb})"
    elif tb > ta:
        leader_color = cb
        leader_txt   = f"{rb} leads ({tb}–{ta})"
    else:
        leader_color = "#AAA"
        leader_txt   = f"Tied all-time ({ta}–{tb})"

    # Streak
    streak_txt = ""
    if rv["streak_holder"] and rv["streak_count"]:
        sc      = rv["streak_count"]
        sh      = rv["streak_holder"]
        sh_color = ca if sh == ra else cb
        streak_txt = (
            f'<div style="font-family:Nunito,sans-serif;font-size:0.78rem;'
            f'color:{sh_color};font-weight:800;text-align:center;margin:0.3rem 0;">'
            f"🔥 {sh} on a {sc}-game streak"
            f"</div>"
        )

    # Closest game
    closest_txt = ""
    cg = rv["closest_game"]
    if cg:
        margin = abs(cg["score_a"] - cg["score_b"])
        closest_txt = f"{max(cg['score_a'], cg['score_b']):.1f} – {min(cg['score_a'], cg['score_b']):.1f} (margin: {margin:.1f} pts, Wk {cg['week']}, {cg['season']})"

    # Playoff meetings
    po_meetings_html = ""
    if rv["po_meetings"]:
        po_lines = []
        for pm in rv["po_meetings"]:
            rnd_label = {
                "semifinal": "Semifinal",
                "final":     "Championship",
                "3rd_place": "3rd Place",
            }.get(pm["round"], pm["round"].title())
            wc    = ca if pm["winner"] == ra else cb
            po_lines.append(
                f'<div style="font-family:Nunito,sans-serif;font-size:0.75rem;color:#555;'
                f'padding:0.2rem 0;border-bottom:1px solid #F0EDE8;">'
                f'{pm["season"]} {rnd_label}: '
                f'<span style="color:{wc};font-weight:800;">{pm["winner"]}</span> wins '
                f'{pm["score_a"]:.1f} – {pm["score_b"]:.1f}'
                f"</div>"
            )
        po_meetings_html = (
            f'<div style="margin-top:0.5rem;">'
            f'<div style="font-family:Nunito,sans-serif;font-size:0.65rem;font-weight:800;'
            f'text-transform:uppercase;letter-spacing:1.5px;color:#AAA;margin-bottom:0.3rem;">'
            f'Playoff Meetings</div>'
            + "".join(po_lines)
            + "</div>"
        )

    # Biggest wins
    big_a = rv["biggest_a_win"]
    big_b = rv["biggest_b_win"]

    big_a_txt = (
        f"{big_a['score_a']:.1f} – {big_a['score_b']:.1f} (Wk {big_a['week']}, {big_a['season']})"
        if big_a else "—"
    )
    big_b_txt = (
        f"{big_b['score_b']:.1f} – {big_b['score_a']:.1f} (Wk {big_b['week']}, {big_b['season']})"
        if big_b else "—"
    )

    return f"""<div style="background:#FFFDF8;border-radius:18px;padding:1.3rem 1.2rem;
                    box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:1rem;
                    border-top:5px solid {ca};">

        <!-- Matchup header -->
        <div style="display:flex;align-items:center;justify-content:space-between;gap:0.5rem;">
            <!-- Manager A -->
            <div style="flex:1;text-align:center;">
                <div style="width:52px;height:52px;border-radius:50%;background:{ca};
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.6rem;margin:0 auto 0.3rem;">{ea}</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;
                            color:{ca};line-height:1.1;">{ra}</div>
            </div>
            <!-- Score -->
            <div style="text-align:center;flex-shrink:0;padding:0 0.3rem;">
                <div style="font-family:'Fredoka One',cursive;font-size:2rem;color:#333;">
                    {ta} – {tb}
                </div>
                <div style="font-family:'Nunito',sans-serif;font-size:0.62rem;font-weight:800;
                            text-transform:uppercase;letter-spacing:1.5px;color:#CCC;">
                    All Time
                </div>
            </div>
            <!-- Manager B -->
            <div style="flex:1;text-align:center;">
                <div style="width:52px;height:52px;border-radius:50%;background:{cb};
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.6rem;margin:0 auto 0.3rem;">{eb}</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.4rem;
                            color:{cb};line-height:1.1;">{rb}</div>
            </div>
        </div>

        <!-- Streak -->
        {streak_txt}

        <!-- Splits -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.65rem;">
            <div style="background:#F6F1E7;border-radius:10px;padding:0.5rem;text-align:center;">
                <div style="font-family:'Nunito',sans-serif;font-size:0.6rem;font-weight:800;
                            text-transform:uppercase;letter-spacing:1px;color:#AAA;">Reg. Season</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.2rem;color:#333;
                            margin-top:0.1rem;">{rsa} – {rsb}</div>
            </div>
            <div style="background:#F6F1E7;border-radius:10px;padding:0.5rem;text-align:center;">
                <div style="font-family:'Nunito',sans-serif;font-size:0.6rem;font-weight:800;
                            text-transform:uppercase;letter-spacing:1px;color:#AAA;">Playoffs</div>
                <div style="font-family:'Fredoka One',cursive;font-size:1.2rem;color:#333;
                            margin-top:0.1rem;">{poa} – {pob}</div>
            </div>
        </div>

        <!-- Playoff meetings -->
        {po_meetings_html}

        <!-- Biggest wins -->
        <div style="margin-top:0.6rem;border-top:1px solid #EEE8E0;padding-top:0.55rem;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;">
                <div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.6rem;font-weight:800;
                                text-transform:uppercase;letter-spacing:1px;color:{ca};">
                        {ra}'s Best Win
                    </div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.73rem;color:#555;">
                        {big_a_txt}
                    </div>
                </div>
                <div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.6rem;font-weight:800;
                                text-transform:uppercase;letter-spacing:1px;color:{cb};">
                        {rb}'s Best Win
                    </div>
                    <div style="font-family:'Nunito',sans-serif;font-size:0.73rem;color:#555;">
                        {big_b_txt}
                    </div>
                </div>
            </div>
        </div>

        <!-- Closest game -->
        {"<div style='margin-top:0.5rem;font-family:Nunito,sans-serif;font-size:0.73rem;color:#AAA;'>" + "⚖️ Closest: " + closest_txt + "</div>" if closest_txt else ""}
    </div>"""


with col_left:
    section_header("Rivalries", "Left bracket")
    for rv in left_rivals:
        st.markdown(rivalry_card_html(rv), unsafe_allow_html=True)

with col_right:
    section_header("", "Right bracket")
    for rv in right_rivals:
        st.markdown(rivalry_card_html(rv), unsafe_allow_html=True)

# ── PLAYOFF RIVALRY SUMMARY ───────────────────────────────────────────────

st.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)
section_header("Playoff Encounters", "When it really mattered")

# Collect all playoff meetings across all rivalries
all_po: list[dict] = []
for rv in all_rivalries:
    for pm in rv["po_meetings"]:
        all_po.append({
            "season": pm["season"],
            "round":  pm["round"],
            "manager_a": rv["manager_a"],
            "manager_b": rv["manager_b"],
            "score_a":   pm["score_a"],
            "score_b":   pm["score_b"],
            "winner":    pm["winner"],
        })

all_po.sort(key=lambda x: (x["season"], x["round"]))

if all_po:
    po_rows = []
    rnd_labels = {
        "semifinal": "Semifinal",
        "final":     "🏆 Championship",
        "3rd_place": "3rd Place",
    }
    for pm in all_po:
        ra       = pm["manager_a"]
        rb       = pm["manager_b"]
        winner   = pm["winner"]
        ca       = MANAGER_COLORS.get(ra, "#333")
        cb       = MANAGER_COLORS.get(rb, "#333")
        wc       = ca if winner == ra else cb
        rnd_lbl  = rnd_labels.get(pm["round"], pm["round"])
        score_a  = pm["score_a"]
        score_b  = pm["score_b"]
        margin   = abs(score_a - score_b)
        # Present from winner's perspective
        if winner == ra:
            score_str = f"{score_a:.1f} – {score_b:.1f}"
        else:
            score_str = f"{score_b:.1f} – {score_a:.1f}"
        po_rows.append([
            (str(pm["season"]), "bold center"),
            (rnd_lbl, ""),
            (f'<span style="color:{ca};font-weight:800;">{ra}</span> vs '
             f'<span style="color:{cb};font-weight:800;">{rb}</span>', ""),
            (f'<span style="color:{wc};font-weight:800;">{winner}</span>', "center"),
            (score_str, "center"),
            (f'{margin:.1f}', "muted center"),
        ])

    from utils.styles import html_table
    st.markdown(
        html_table(
            ["Season", "Round", "Matchup", "Winner", "Score", "Margin"],
            po_rows,
        ),
        unsafe_allow_html=True,
    )

st.markdown(
    """<div style="padding:2.5rem 0 1.5rem;text-align:center;">
        <div style="font-family:'Nunito',sans-serif;font-size:0.72rem;color:#BBB;
                    font-weight:700;letter-spacing:2px;text-transform:uppercase;">
            Espinosa FFL &bull; Rivalry Arena
        </div>
    </div>""",
    unsafe_allow_html=True,
)
