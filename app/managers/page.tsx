import type { Metadata } from "next";
import { ManagerIdentity } from "@/components/manager-identity";
import { CLUBHOUSE_FAMILY, MANAGER_ORDER, getAllTimeStandings, getChampions, getManagerCareerStats, getRivalryStats, getSeasonStandings, seasonList } from "@/lib/league";

export const metadata: Metadata = { title: "Locker Room" };

export default function ManagersPage() {
  const seasons = seasonList();
  const champions = getChampions();
  const allTime = getAllTimeStandings();
  const careers = MANAGER_ORDER.map((manager) => getManagerCareerStats(manager.id)).filter((stats) => stats !== null);
  const futureManagers = CLUBHOUSE_FAMILY.filter((manager) => !manager.active);

  return <main className="page-wrap inner-page">
    <header className="page-intro">
      <p className="eyebrow">👥 The Clubhouse</p>
      <h1>Locker Room</h1>
      <p>Every manager. Every season. Every rivalry.</p>
    </header>

    <section className="hq-section">
      <div className="section-heading"><h2>Meet the Managers</h2><span>The Espinosa FFL roster</span></div>
      <div className="hq-managers-row">
        {careers.map((career) => <article className="hq-profile-card" key={career.manager.id} style={{ borderTopColor: career.manager.color }}>
          <ManagerIdentity manager={career.manager} size="large" />
          <h3 className="hq-profile-name" style={{ color: career.manager.color }}>{career.manager.name}</h3>
          <p className="hq-profile-team">&ldquo;{career.team}&rdquo;</p>
          <div className="hq-stat-grid">
            <div className="hq-stat-box"><b style={{ color: career.manager.color }}>{career.totalWins}-{career.totalLosses}</b><span>Career Record</span></div>
            <div className="hq-stat-box"><b style={{ color: career.manager.color }}>{(career.winPct * 100).toFixed(0)}%</b><span>Win Rate</span></div>
            <div className="hq-stat-box"><b style={{ color: career.manager.color }}>{career.championshipCount}</b><span>Championships</span></div>
            <div className="hq-stat-box"><b style={{ color: career.manager.color }}>{career.avgPpg}</b><span>Avg PPG</span></div>
          </div>
          <p className="hq-profile-line"><span>Titles</span> {career.championships.length ? career.championships.join(", ") : "—"}</p>
          {career.runnerUps.length > 0 && <p className="hq-profile-line"><span>Runner-Up</span> {career.runnerUps.join(", ")}</p>}
          {career.bestWeek && <p className="hq-profile-line"><span>Best Single Week</span> {career.bestWeek.teamScore} pts (Wk {career.bestWeek.week}, {career.bestWeek.season})</p>}
        </article>)}
        {futureManagers.map((manager) => <article className="hq-profile-card hq-profile-card-future" key={manager.id} style={{ borderTopColor: manager.color }}>
          <ManagerIdentity manager={manager} size="large" />
          <p className="hq-future-badge">Future Manager</p>
          <h3 className="hq-profile-name" style={{ color: manager.color }}>{manager.name}</h3>
          <p className="hq-profile-team">Clubhouse roster spot reserved</p>
          <p className="hq-future-copy">Part of the family clubhouse now. League records begin when Wyatt joins the draft.</p>
        </article>)}
      </div>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Year-by-Year Records</h2><span>Regular season (weeks 1–15) for each manager</span></div>
      <div className="hq-table-wrap"><table className="hq-table">
        <thead><tr><th>Manager</th>{seasons.map((season) => <th key={season}>{season}</th>)}</tr></thead>
        <tbody>{MANAGER_ORDER.map((manager) => <tr key={manager.id}>
          <td className="bold" style={{ color: manager.color }}>{manager.emoji} {manager.name}</td>
          {seasons.map((season) => {
            const standing = getSeasonStandings(season).find((row) => row.manager?.id === manager.id);
            const isChamp = champions.find((champ) => champ.season === season)?.championManager?.id === manager.id;
            if (!standing) return <td key={season} className="muted">—</td>;
            return <td key={season} className={isChamp ? "bold gold" : ""}>{isChamp ? "🏆 " : ""}{standing.wins}–{standing.losses}</td>;
          })}
        </tr>)}</tbody>
      </table></div>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Head-to-Head Matrix</h2><span>Regular season all-time records</span></div>
      <div className="hq-table-wrap"><table className="hq-table">
        <thead><tr><th>vs.</th>{MANAGER_ORDER.map((manager) => <th key={manager.id}>{manager.name}</th>)}</tr></thead>
        <tbody>{MANAGER_ORDER.map((rowManager) => <tr key={rowManager.id}>
          <td className="bold" style={{ color: rowManager.color }}>{rowManager.name}</td>
          {MANAGER_ORDER.map((colManager) => {
            if (rowManager.id === colManager.id) return <td key={colManager.id} className="muted center">—</td>;
            const { rsAWins, rsBWins } = getRivalryStats(rowManager, colManager);
            const winning = rsAWins > rsBWins;
            const tied = rsAWins === rsBWins;
            return <td key={colManager.id} className={`center ${winning ? "bold green" : tied ? "bold" : "muted"}`}>{rsAWins}–{rsBWins}</td>;
          })}
        </tr>)}</tbody>
      </table></div>
      <p className="hq-table-caption">Regular season only (weeks 1–15). Playoff records tracked separately in Rivalry Arena.</p>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Career Totals</h2><span>All-time regular season stats</span></div>
      <div className="hq-table-wrap"><table className="hq-table">
        <thead><tr><th>Manager</th><th>Record</th><th className="center">Win %</th><th className="right">Total PF</th><th>Titles</th></tr></thead>
        <tbody>{allTime.map((row) => <tr key={row.manager.id}>
          <td className="bold" style={{ color: row.manager.color }}>{row.manager.emoji} {row.manager.name}</td>
          <td className="bold">{row.wins}–{row.losses}</td>
          <td className="center">{(row.winPct * 100).toFixed(1)}%</td>
          <td className="right">{row.pf}</td>
          <td>{row.championships > 0 ? "🏆".repeat(row.championships) : "—"}</td>
        </tr>)}</tbody>
      </table></div>
    </section>

    <p className="hq-page-footer">Espinosa FFL · Locker Room</p>
  </main>;
}
