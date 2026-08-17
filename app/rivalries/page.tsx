import type { Metadata } from "next";
import type { RivalryStats } from "@/lib/league";
import { getAllRivalries, playoffGames, managerForTeam } from "@/lib/league";

export const metadata: Metadata = { title: "Rivalry Arena" };

const ROUND_LABELS: Record<string, string> = { semifinal: "Semifinal", final: "Championship", "3rd_place": "3rd Place" };

function RivalryCard({ rivalry }: { rivalry: RivalryStats }) {
  const { managerA, managerB } = rivalry;
  return <article className="hq-rivalry-card" style={{ borderTopColor: managerA.color }}>
    <div className="hq-rivalry-head">
      <div className="hq-rivalry-side"><span className="hq-rivalry-avatar" style={{ background: managerA.color }}>{managerA.emoji}</span><p style={{ color: managerA.color }}>{managerA.name}</p></div>
      <div className="hq-rivalry-score"><strong>{rivalry.totalAWins}–{rivalry.totalBWins}</strong><span>ALL TIME</span></div>
      <div className="hq-rivalry-side"><span className="hq-rivalry-avatar" style={{ background: managerB.color }}>{managerB.emoji}</span><p style={{ color: managerB.color }}>{managerB.name}</p></div>
    </div>
    {rivalry.streakHolder && rivalry.streakCount > 1 && <p className="hq-rivalry-streak" style={{ color: rivalry.streakHolder.color }}>🔥 {rivalry.streakHolder.name} on a {rivalry.streakCount}-game streak</p>}
    <div className="hq-rivalry-mini-grid">
      <div className="hq-rivalry-mini-stat"><span>Reg. Season</span><b>{rivalry.rsAWins}–{rivalry.rsBWins}</b></div>
      <div className="hq-rivalry-mini-stat"><span>Playoffs</span><b>{rivalry.poAWins}–{rivalry.poBWins}</b></div>
    </div>
    {rivalry.poMeetings.length > 0 && <div className="hq-rivalry-block">
      <p className="hq-rivalry-block-title">Playoff Meetings</p>
      {rivalry.poMeetings.map((meeting, index) => <p className="hq-rivalry-line" key={index}>{meeting.season} {ROUND_LABELS[meeting.round] ?? meeting.round}: <b style={{ color: meeting.winner?.color }}>{meeting.winner?.name}</b> wins {meeting.winnerScore}–{meeting.loserScore}</p>)}
    </div>}
    <div className="hq-rivalry-block">
      <p className="hq-rivalry-block-title">Biggest Wins</p>
      <div className="hq-rivalry-mini-grid">
        <div className="hq-rivalry-mini-stat"><span style={{ color: managerA.color }}>{managerA.name}</span><b>{rivalry.biggestAWin ? `${rivalry.biggestAWin.scoreA}–${rivalry.biggestAWin.scoreB} (Wk ${rivalry.biggestAWin.week}, ${rivalry.biggestAWin.season})` : "—"}</b></div>
        <div className="hq-rivalry-mini-stat"><span style={{ color: managerB.color }}>{managerB.name}</span><b>{rivalry.biggestBWin ? `${rivalry.biggestBWin.scoreA}–${rivalry.biggestBWin.scoreB} (Wk ${rivalry.biggestBWin.week}, ${rivalry.biggestBWin.season})` : "—"}</b></div>
      </div>
    </div>
    {rivalry.closestGame && <p className="hq-rivalry-closest">⚖️ Closest: {rivalry.closestGame.scoreA}–{rivalry.closestGame.scoreB} (Wk {rivalry.closestGame.week}, {rivalry.closestGame.season})</p>}
  </article>;
}

export default function RivalriesPage() {
  const rivalries = getAllRivalries();
  const left = rivalries.slice(0, 3);
  const right = rivalries.slice(3, 6);

  const encounters = playoffGames
    .map((game) => {
      const winnerTeam = game.score1 > game.score2 ? game.team1 : game.team2;
      const loserScore = game.score1 > game.score2 ? game.score2 : game.score1;
      const winnerScore = game.score1 > game.score2 ? game.score1 : game.score2;
      return { ...game, winnerManager: managerForTeam(winnerTeam), team1Manager: managerForTeam(game.team1), team2Manager: managerForTeam(game.team2), winnerScore, loserScore };
    })
    .sort((a, b) => a.season - b.season || a.round - b.round);

  return <main className="page-wrap inner-page">
    <header className="page-intro">
      <p className="eyebrow">🥊 The Clubhouse</p>
      <h1>Rivalry Arena</h1>
      <p>Every matchup. Every grudge. Every bragging right.</p>
    </header>

    <section className="hq-section">
      <div className="hq-rivalry-columns">
        <div><div className="section-heading"><h2>Rivalries</h2><span>Left bracket</span></div>{left.map((rivalry) => <RivalryCard rivalry={rivalry} key={`${rivalry.managerA.id}-${rivalry.managerB.id}`} />)}</div>
        <div><div className="section-heading"><h2>&nbsp;</h2><span>Right bracket</span></div>{right.map((rivalry) => <RivalryCard rivalry={rivalry} key={`${rivalry.managerA.id}-${rivalry.managerB.id}`} />)}</div>
      </div>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Playoff Encounters</h2><span>When it really mattered</span></div>
      <div className="hq-table-wrap"><table className="hq-table">
        <thead><tr><th>Season</th><th>Round</th><th>Matchup</th><th>Winner</th><th>Score</th><th>Margin</th></tr></thead>
        <tbody>{encounters.map((game, index) => <tr key={index}>
          <td>{game.season}</td>
          <td>{game.gameType === "final" ? "🏆 Championship" : ROUND_LABELS[game.gameType] ?? game.gameType}</td>
          <td><span style={{ color: game.team1Manager?.color }}>{game.team1Manager?.name}</span> vs <span style={{ color: game.team2Manager?.color }}>{game.team2Manager?.name}</span></td>
          <td className="bold" style={{ color: game.winnerManager?.color }}>{game.winnerManager?.name}</td>
          <td>{game.winnerScore} – {game.loserScore}</td>
          <td className="muted">{Math.round((game.winnerScore - game.loserScore) * 10) / 10}</td>
        </tr>)}</tbody>
      </table></div>
    </section>

    <p className="hq-page-footer">Espinosa FFL · Rivalry Arena</p>
  </main>;
}
