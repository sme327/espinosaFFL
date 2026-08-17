import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ClubhouseLink as Link } from "@/components/clubhouse-link";
import { draftPicks, getChampions, getSeasonPlayoffs, getSeasonStandings, managerForTeam, seasonList, seasonNoteFor } from "@/lib/league";

export function generateMetadata({ params }: { params: Promise<{ year: string }> }): Promise<Metadata> {
  return params.then(({ year }) => ({ title: `${year} Season` }));
}

type BracketGameData = { seed1: number; team1: string; score1: number; seed2: number; team2: string; score2: number } | undefined;

function BracketGame({ game }: { game: BracketGameData }) {
  if (!game) return null;
  const team1Wins = game.score1 > game.score2;
  return <div className="hq-bracket-game">
    <div className={`hq-bracket-team ${team1Wins ? "hq-bracket-winner" : "hq-bracket-loser"}`}><span>#{game.seed1} {managerForTeam(game.team1)?.name}</span><b>{game.score1}</b></div>
    <div className={`hq-bracket-team ${!team1Wins ? "hq-bracket-winner" : "hq-bracket-loser"}`}><span>#{game.seed2} {managerForTeam(game.team2)?.name}</span><b>{game.score2}</b></div>
  </div>;
}

export default async function SeasonPage({ params }: { params: Promise<{ year: string }> }) {
  const { year: yearParam } = await params;
  const year = Number(yearParam);
  const seasons = seasonList();
  if (!Number.isInteger(year) || !seasons.includes(year)) notFound();

  const champion = getChampions().find((champ) => champ.season === year);
  const note = seasonNoteFor(year);
  const standings = getSeasonStandings(year);
  const playoffs = getSeasonPlayoffs(year);
  const semifinals = playoffs.filter((game) => game.gameType === "semifinal");
  const final = playoffs.find((game) => game.gameType === "final");
  const thirdPlace = playoffs.find((game) => game.gameType === "3rd_place");
  const rankEmoji = ["🥇", "🥈", "🥉", "4️⃣"];

  const picksThisSeason = draftPicks.filter((pick) => pick.season === year).sort((a, b) => a.overallPick - b.overallPick);
  const rounds = [...new Set(picksThisSeason.map((pick) => pick.round))].filter((round) => round <= 5).sort((a, b) => a - b);

  return <main className="page-wrap inner-page">
    <header className="page-intro">
      <p className="eyebrow">📖 The Clubhouse</p>
      <h1>Season Scrapbook</h1>
      <p>Every week. Every win. Every memory.</p>
    </header>

    <nav className="hq-season-picker" aria-label="Choose a season">
      {[...seasons].reverse().map((season) => <Link key={season} href={`/seasons/${season}`} aria-current={season === year ? "page" : undefined} className={season === year ? "active" : ""}>{season}</Link>)}
    </nav>

    {champion && <div className="hq-season-header">
      <span aria-hidden="true">{champion.championManager?.emoji}</span>
      <div>
        <p className="eyebrow">{champion.season} Champion</p>
        <h2 style={{ color: champion.championManager?.color }}>{champion.championManager?.name}</h2>
        <p className="hq-season-header-line">{champion.championTeam} · {champion.championScore}–{champion.runnerUpScore} def. {champion.runnerUpManager?.name}</p>
        {note && <p className="hq-season-header-tagline">{note.tagline}</p>}
      </div>
    </div>}

    <div className="hq-season-body">
      <div className="surface hq-season-standings">
        <div className="section-heading"><h2>Regular Season Standings</h2><span>Weeks 1 – 15</span></div>
        <table className="hq-table hq-table-flush">
          <thead><tr><th></th><th>Manager</th><th>Team</th><th>Record</th><th className="right">PF</th><th className="right">PA</th></tr></thead>
          <tbody>{standings.map((row) => <tr key={row.teamName}>
            <td>{rankEmoji[row.rank - 1] ?? row.rank}</td>
            <td className="bold" style={{ color: row.manager?.color }}>{row.manager?.name}</td>
            <td className="muted">{row.teamName}</td>
            <td className="bold">{row.wins}–{row.losses}</td>
            <td className="right">{row.pf}</td>
            <td className="right muted">{row.pa}</td>
          </tr>)}</tbody>
        </table>
        {note && note.highlights.length > 0 && <div className="hq-season-highlights">
          <p className="hq-rivalry-block-title">Season Highlights</p>
          <ul className="hq-highlights">{note.highlights.map((highlight, index) => <li className="hq-highlight" key={index}>⚡ {highlight}</li>)}</ul>
        </div>}
      </div>

      <div className="surface hq-season-bracket">
        <div className="section-heading"><h2>Playoff Bracket</h2><span>The road to the championship</span></div>
        <div className="hq-bracket-round"><p className="hq-bracket-round-title">Semifinals — Week 16</p>{semifinals.map((game, index) => <BracketGame game={game} key={index} />)}</div>
        <div className="hq-bracket-round"><p className="hq-bracket-round-title">🏆 Championship — Week 17</p><BracketGame game={final} /></div>
        <div className="hq-bracket-round"><p className="hq-bracket-round-title">3rd Place — Week 17</p><BracketGame game={thirdPlace} /></div>
      </div>
    </div>

    {rounds.length > 0 && <section className="hq-section">
      <div className="section-heading"><h2>Draft Day</h2><span>{year} Draft — First {rounds.length} Rounds</span></div>
      <div className="hq-draft-grid">
        {rounds.map((round) => <div className="hq-draft-round" key={round}>
          <p className="hq-draft-round-title">Round {round}</p>
          {picksThisSeason.filter((pick) => pick.round === round).map((pick) => {
            const manager = managerForTeam(pick.teamName);
            return <div className="hq-pick-card" key={pick.overallPick} style={{ borderLeftColor: manager?.color }}>
              <span className="hq-pick-number" style={{ color: manager?.color }}>{pick.overallPick}</span>
              <div><p className="hq-pick-player">{pick.playerName}</p><p className="hq-pick-manager">{manager?.name}</p></div>
            </div>;
          })}
        </div>)}
      </div>
    </section>}

    <p className="hq-page-footer">Espinosa FFL · Season Scrapbook</p>
  </main>;
}
