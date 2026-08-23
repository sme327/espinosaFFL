import { ClubhouseLink as Link } from "@/components/clubhouse-link";
import { TeamLogo } from "@/components/team-logo";
import { CLUBHOUSE_FAMILY, FOUNDED, getChampions, getRivalryStats, rivalrySpotlightPair, seasonList, seasonNoteFor } from "@/lib/league";

const ROOMS = [
  { key: "draft", icon: "draft", title: "Draft Room", href: "/draft", desc: "Build your team under the draft-night lights." },
  { key: "locker", icon: "locker", title: "Locker Room", href: "/managers", desc: "Meet all five managers and their teams." },
  { key: "trophy", icon: "trophy", title: "Trophy Room", href: "/champions", desc: "Every champion and every title." },
  { key: "rivalry", icon: "rivalry", title: "Rivalry Arena", href: "/rivalries", desc: "Head-to-head history and bragging rights." },
  { key: "scrapbook", icon: "scrapbook", title: "Season Scrapbook", href: "/seasons", desc: "Standings, playoffs, and family memories." },
  { key: "weekly", icon: "weekly", title: "Weekly Fun", href: "/weekly", desc: "Make picks and celebrate game week." },
  { key: "achievement", icon: "achievements", title: "Ring of Honor", href: "/achievements", desc: "See what everyone has earned." },
] as const;

export default function Overview() {
  const champions = getChampions();
  const reigning = champions[champions.length - 1];
  const note = reigning ? seasonNoteFor(reigning.season) : undefined;
  const seasons = seasonList();

  const [spotA, spotB] = rivalrySpotlightPair();
  const spotlight = getRivalryStats(spotA, spotB);

  return <main className="stadium-home"><h1 className="sr-only">Espinosa FFL Clubhouse</h1>
    <section className="stadium-gate">
      <div className="page-wrap stadium-gate-inner">
        <div className="stadium-gate-copy">
          <p className="stadium-kicker">Our house · Our teams · Our season</p>
          <h2>Welcome to the Clubhouse</h2>
          <p>Five managers. One family. The season starts here.</p>
          <Link href="/draft" className="stadium-primary">Enter the Draft Room</Link>
        </div>
        <div className="stadium-scoreboard" aria-label="Next clubhouse event: Draft Night">
          <span>Next Event</span><strong>Draft Night</strong><small>5 teams · no clock</small>
        </div>
      </div>
    </section>

    <div className="page-wrap stadium-home-content">
      <section className="stadium-family" aria-labelledby="family-lineup-title">
        <div className="stadium-section-heading"><p>Home Team</p><h2 id="family-lineup-title">The Starting Five</h2></div>
        <div className="stadium-family-lineup">
          {CLUBHOUSE_FAMILY.map((manager) => <div className="stadium-family-member" key={manager.id} style={{ "--manager-color": manager.color } as React.CSSProperties}>
            <TeamLogo manager={manager} size="large" />
            <strong>{manager.name}</strong>
            <span>{manager.teamName ?? "Future Manager"}</span>
          </div>)}
        </div>
      </section>

      <section className="stadium-concourse" aria-labelledby="concourse-title">
        <div className="stadium-section-heading"><p>Main Concourse</p><h2 id="concourse-title">Choose Your Room</h2></div>
        <div className="stadium-room-list">
          {ROOMS.map((room) => <Link key={room.key} href={room.href} className={`stadium-room-sign stadium-room-${room.key}`}>
            <span className="stadium-room-code"><img src={`/stadium/icons/${room.icon}.svg`} alt="" /></span>
            <span><strong>{room.title}</strong><small>{room.desc}</small></span>
            <b aria-hidden="true">→</b>
          </Link>)}
        </div>
      </section>

      {reigning && <>
        <section className="stadium-champion">
          <div className="stadium-champion-banner"><span>{reigning.season} League Champion</span></div>
          {reigning.championManager && <TeamLogo manager={reigning.championManager} size="large" />}
          <div className="stadium-champion-copy"><h2>{reigning.championManager?.name}</h2><p>{reigning.championTeam}</p>{note && <blockquote>{note.tagline}</blockquote>}</div>
          <div className="stadium-final-score"><span>Final</span><strong>{reigning.championScore.toFixed(1)} <i>–</i> {reigning.runnerUpScore.toFixed(1)}</strong><small>vs. {reigning.runnerUpManager?.name}</small></div>
          <Link href="/champions" className="stadium-secondary">Enter the Trophy Room</Link>
        </section>
      </>}

      <section className="stadium-rivalry">
          <div className="stadium-section-heading"><p>Primetime</p><h2>Rivalry Spotlight</h2></div>
          <div className="hq-rivalry-head">
            <div className="hq-rivalry-side"><TeamLogo manager={spotA} size="medium" /><p>{spotA.name}</p></div>
            <div className="hq-rivalry-score"><strong>{spotlight.totalAWins}–{spotlight.totalBWins}</strong><span>ALL TIME</span></div>
            <div className="hq-rivalry-side"><TeamLogo manager={spotB} size="medium" /><p>{spotB.name}</p></div>
          </div>
          {spotlight.streakHolder && spotlight.streakCount > 1 && <p className="hq-rivalry-streak">{spotlight.streakHolder.name} owns a {spotlight.streakCount}-game streak</p>}
          <Link href="/rivalries" className="stadium-secondary">See Every Rivalry</Link>
      </section>

      <section className="stadium-banners">
        <div className="stadium-section-heading"><p>Ring of Honor</p><h2>Championship Banners</h2></div>
        <div className="hq-shelf-rail">
          {champions.map((champ) => <div className="hq-shelf-item" key={champ.season}>
            {champ.championManager && <TeamLogo manager={champ.championManager} size="medium" />}
            <p className="hq-shelf-year">{champ.season}</p>
            <p className="hq-shelf-name" style={{ color: champ.championManager?.color }}>{champ.championManager?.name}</p>
            <p className="hq-shelf-team">{champ.championTeam}</p>
          </div>)}
          <div className="hq-shelf-item hq-shelf-item-soon">
            <span className="stadium-banner-open" aria-hidden="true">?</span>
            <p className="hq-shelf-year">{Math.max(...seasons) + 1}</p>
            <p className="hq-shelf-name">???</p>
            <p className="hq-shelf-team">Who will it be?</p>
          </div>
        </div>
      </section>

    </div>

    <footer className="hq-footer">
      <p className="hq-footer-name">Espinosa Fantasy Football Clubhouse</p>
      <p className="hq-footer-tag">Est. {FOUNDED} • Family is the whole league</p>
    </footer>
  </main>;
}
