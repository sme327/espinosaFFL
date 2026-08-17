import type { Metadata } from "next";
import { ClubhouseLink as Link } from "@/components/clubhouse-link";
import { FOUNDED, MANAGER_ORDER, getChampions, seasonNoteFor } from "@/lib/league";

export const metadata: Metadata = { title: "Trophy Room" };

export default function ChampionsPage() {
  const champions = getChampions();
  const reigning = champions[champions.length - 1];
  const byMargin = [...champions].sort((a, b) => a.margin - b.margin);
  const closest = byMargin[0];
  const biggest = byMargin[byMargin.length - 1];
  const everWon = new Set(champions.map((champ) => champ.championManager?.id));
  const chasers = MANAGER_ORDER.filter((manager) => !everWon.has(manager.id));

  return <main className="page-wrap inner-page">
    <header className="page-intro">
      <p className="eyebrow">🏆 The Clubhouse</p>
      <h1>Trophy Room</h1>
      <p>Every champion. Every season. Every memory.</p>
    </header>

    {reigning && <section className="hq-section">
      <div className="section-heading"><h2>Reigning Champion</h2><span>The last one standing</span></div>
      <div className="hq-champ-card">
        <span className="hq-champ-trophy" aria-hidden="true">🏆</span>
        <p className="eyebrow">{reigning.season} Champion</p>
        <span className="hq-champ-emoji" aria-hidden="true">{reigning.championManager?.emoji}</span>
        <h3 className="hq-champ-name" style={{ color: reigning.championManager?.color }}>{reigning.championManager?.name}</h3>
        <p className="hq-champ-team">&ldquo;{reigning.championTeam}&rdquo;</p>
        <p className="hq-champ-score">Defeated {reigning.runnerUpManager?.name} · {reigning.championScore}–{reigning.runnerUpScore}</p>
        {seasonNoteFor(reigning.season) && <p className="hq-champ-tagline">{seasonNoteFor(reigning.season)?.tagline}</p>}
      </div>
    </section>}

    <section className="hq-section">
      <div className="section-heading"><h2>All Champions</h2><span>League founded {FOUNDED}</span></div>
      <div className="hq-champions-row">
        {champions.map((champ) => <article className="hq-mini-champ-card" key={champ.season} style={{ borderTopColor: champ.championManager?.color }}>
          <p className="hq-mini-champ-season" style={{ color: champ.championManager?.color }}>{champ.season}</p>
          <span className="hq-mini-champ-emoji" aria-hidden="true">{champ.championManager?.emoji}</span>
          <p className="hq-mini-champ-name" style={{ color: champ.championManager?.color }}>{champ.championManager?.name}</p>
          <p className="hq-mini-champ-team">{champ.championTeam}</p>
          <hr />
          <p className="hq-mini-champ-score">🏆 {champ.championScore}–{champ.runnerUpScore}</p>
          <p className="hq-mini-champ-margin">def. {champ.runnerUpManager?.name} (margin: {champ.margin} pts)</p>
        </article>)}
      </div>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Season Stories</h2><span>What made each season unforgettable</span></div>
      <div className="hq-season-stories">
        {[...champions].reverse().map((champ) => {
          const note = seasonNoteFor(champ.season);
          return <article className="hq-season-story" key={champ.season} style={{ borderTopColor: champ.championManager?.color }}>
            <div className="hq-season-story-head">
              <span className="hq-season-story-year" style={{ color: champ.championManager?.color }}>{champ.season}</span>
              <div><h3>{champ.championManager?.name} wins</h3>{note && <p className="hq-season-story-tagline">{note.tagline}</p>}</div>
            </div>
            {note && <ul className="hq-highlights">{note.highlights.map((highlight, index) => <li className="hq-highlight" key={index}>⚡ {highlight}</li>)}</ul>}
          </article>;
        })}
      </div>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>By the Numbers</h2><span>Championship records</span></div>
      <div className="hq-stat-row">
        {closest && <article className="hq-stat-card"><span aria-hidden="true">😰</span><h3>Closest Championship</h3><p className="hq-stat-card-value">{closest.margin} pts</p><p className="hq-stat-card-sub">{closest.championManager?.name}, {closest.season}</p></article>}
        {biggest && <article className="hq-stat-card"><span aria-hidden="true">💥</span><h3>Biggest Margin</h3><p className="hq-stat-card-value">{biggest.margin} pts</p><p className="hq-stat-card-sub">{biggest.championManager?.name}, {biggest.season}</p></article>}
        <article className="hq-stat-card"><span aria-hidden="true">🎯</span><h3>Still Waiting</h3>
          {chasers.length ? <><p className="hq-stat-card-value">{chasers.map((manager, index) => <span key={manager.id} style={{ color: manager.color }}>{index > 0 ? " · " : ""}{manager.name}</span>)}</p><p className="hq-stat-card-sub">Still chasing that first ring 👀</p></> : <p className="hq-stat-card-value" style={{ color: "var(--elliot)" }}>Everyone&rsquo;s won one!</p>}
        </article>
      </div>
    </section>

    <p className="hq-page-footer">Espinosa FFL · Trophy Room</p>
    <p className="sr-only"><Link href="/">Back to Clubhouse</Link></p>
  </main>;
}
