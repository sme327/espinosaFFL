import { ClubhouseLink as Link } from "@/components/clubhouse-link";
import { TeamLogo } from "@/components/team-logo";
import { FOUNDED, getChampions, getRivalryStats, recentEvents, rivalrySpotlightPair, seasonList, seasonNoteFor } from "@/lib/league";

const ROOMS = [
  { key: "trophy", icon: ["🥇", "🏆", "🥈"], title: "Trophy Room", href: "/champions", desc: "Every champion. Every title. Every memory.", color: "var(--room-trophy)", gradient: "linear-gradient(160deg,#FFF8E0 0%,#FFE050 100%)" },
  { key: "scrapbook", icon: ["📷", "📖", "🎉"], title: "Season Scrapbook", href: "/seasons", desc: "Relive the standings, playoffs, and draft day moments.", color: "var(--room-scrapbook)", gradient: "linear-gradient(160deg,#EEF5FF 0%,#90C4FF 100%)" },
  { key: "locker", icon: ["🎽", "👥", "🧦"], title: "Locker Room", href: "/managers", desc: "Manager profiles, career records, and personal bests.", color: "var(--room-locker)", gradient: "linear-gradient(160deg,#EEF7EF 0%,#80CC80 100%)" },
  { key: "rivalry", icon: ["😤", "🥊", "😈"], title: "Rivalry Arena", href: "/rivalries", desc: "Every grudge. Every bragging right. Head-to-head history.", color: "var(--room-rivalry)", gradient: "linear-gradient(160deg,#FEF0F8 0%,#F080C0 100%)" },
  { key: "weekly", icon: ["🏈", "🔮", "⭐"], title: "Weekly Fun", href: "/weekly", desc: "Make family picks, choose an MVP, and celebrate the week.", color: "var(--action-green)", gradient: "linear-gradient(160deg,#B9C6CA 0%,#91B39A 100%)" },
  { key: "achievement", icon: ["🎖️", "🎯", "🏅"], title: "Achievement Wall", href: null, desc: "Badges, stickers, and collectible achievements. Coming soon!", color: "var(--room-achievement)", gradient: "linear-gradient(160deg,#F0EEF8 0%,#C8B8E8 100%)" },
  { key: "draft", icon: ["📝", "📋", "🎲"], title: "Draft Room", href: "/draft", desc: "Meet the draft class and get ready to build your 2026 team.", color: "var(--room-draft)", gradient: "linear-gradient(160deg,#F5F0FF 0%,#B8A0E0 100%)" },
] as const;

export default function Overview() {
  const champions = getChampions();
  const reigning = champions[champions.length - 1];
  const note = reigning ? seasonNoteFor(reigning.season) : undefined;
  const seasons = seasonList();

  const [spotA, spotB] = rivalrySpotlightPair();
  const spotlight = getRivalryStats(spotA, spotB);

  return <main><h1 className="sr-only">Espinosa FFL Clubhouse</h1>
    <div className="page-wrap inner-page">

      <section className="hq-hero">
        <span className="hq-hero-deco hq-hero-deco-1" aria-hidden="true">🏟️</span>
        <span className="hq-hero-deco hq-hero-deco-2" aria-hidden="true">🏈</span>
        <span className="hq-hero-deco hq-hero-deco-3" aria-hidden="true">🏆</span>
        <span className="hq-hero-emoji" aria-hidden="true">🏟️</span>
        <h2 className="hq-hero-title">Welcome to the Clubhouse</h2>
        <p className="hq-hero-sub">Where Espinosa FFL history lives forever</p>
      </section>
      <p className="hq-brand-title">Espinosa Fantasy Football Clubhouse</p>
      <p className="hq-brand-sub">One League • One Family • Countless Memories</p>

      {reigning && <>
        <div className="hq-divider"><span aria-hidden="true">🏆</span></div>
        <section className="hq-champ-featured">
          <span className="hq-confetti hq-confetti-left" aria-hidden="true">🎊 🎉 🎊</span>
          <span className="hq-confetti hq-confetti-right" aria-hidden="true">🎊 🎉 🎊</span>
          <span className="hq-champ-trophy" aria-hidden="true">🏆</span>
          <p className="eyebrow">✦ {reigning.season} League Champion ✦</p>
          {reigning.championManager && <TeamLogo manager={reigning.championManager} size="large" />}
          <h2 className="hq-champ-name" style={{ color: reigning.championManager?.color }}>{reigning.championManager?.name}</h2>
          <p className="hq-champ-team">&ldquo;{reigning.championTeam}&rdquo;</p>
          <p className="hq-champ-score">{reigning.championScore.toFixed(1)} – {reigning.runnerUpScore.toFixed(1)} • defeated {reigning.runnerUpManager?.name}</p>
          {note && <p className="hq-champ-tagline">{note.tagline}</p>}
          <Link href="/champions" className="hq-champ-cta" style={{ background: reigning.championManager?.color }}>View the Trophy Room →</Link>
        </section>
      </>}

      <div className="hq-divider"><span aria-hidden="true">🚪</span></div>
      <section>
        <div className="hq-explore-head"><h2>Explore the Clubhouse</h2><p>Pick a room and step inside</p></div>
        <div className="hq-explore-grid">
          {ROOMS.map((room) => {
            const card = <>
              <div className="hq-explore-banner" style={{ background: room.gradient }}>
                <span>{room.icon[0]}</span><span className="hq-explore-banner-main">{room.icon[1]}</span><span>{room.icon[2]}</span>
              </div>
              <div className="hq-explore-body">
                <h3>{room.title}</h3>
                <p>{room.desc}</p>
                {room.href ? <span className="hq-explore-cta" style={{ background: room.color }}>Enter →</span> : <span className="hq-explore-soon">Coming Soon</span>}
              </div>
            </>;
            return room.href
              ? <Link key={room.key} href={room.href} className="hq-explore-card">{card}</Link>
              : <div key={room.key} className="hq-explore-card hq-explore-card-soon" aria-disabled="true">{card}</div>;
          })}
        </div>
      </section>

      <div className="hq-divider"><span aria-hidden="true">📍</span></div>
      <section className="hq-activity-grid">
        <div className="hq-bulletin">
          <h3>📌 What&rsquo;s Happening</h3>
          {recentEvents.slice(0, 3).map((event, index) => <div className="hq-bulletin-item" key={index}><span>{event.icon}</span><span>{event.text}</span></div>)}
        </div>
        <div className="hq-spotlight" style={{ borderTopColor: spotA.color }}>
          <h3>⚔️ Rivalry Spotlight</h3>
          <p className="hq-spotlight-sub">Today&rsquo;s featured matchup</p>
          <div className="hq-rivalry-head">
            <div className="hq-rivalry-side"><span className="hq-rivalry-avatar" style={{ background: spotA.color, width: 72, height: 72, fontSize: "1.8rem" }}>{spotA.emoji}</span><p style={{ color: spotA.color }}>{spotA.name}</p></div>
            <div className="hq-rivalry-score"><strong>{spotlight.totalAWins}–{spotlight.totalBWins}</strong><span>ALL TIME</span></div>
            <div className="hq-rivalry-side"><span className="hq-rivalry-avatar" style={{ background: spotB.color, width: 72, height: 72, fontSize: "1.8rem" }}>{spotB.emoji}</span><p style={{ color: spotB.color }}>{spotB.name}</p></div>
          </div>
          {spotlight.streakHolder && spotlight.streakCount > 1 && <p className="hq-rivalry-streak" style={{ color: spotlight.streakHolder.color }}>🔥 {spotlight.streakHolder.name} on a {spotlight.streakCount}-game streak</p>}
          <Link href="/rivalries" className="hq-spotlight-cta">See Rivalry Arena →</Link>
        </div>
      </section>

      <div className="hq-divider"><span aria-hidden="true">🏅</span></div>
      <section className="hq-shelf-wrap">
        <h3>🏆 Champion Shelf</h3>
        <p className="hq-shelf-sub">Every trophy. Every season. The museum never forgets.</p>
        <div className="hq-shelf-rail">
          {champions.map((champ) => <div className="hq-shelf-item" key={champ.season}>
            {champ.championManager && <TeamLogo manager={champ.championManager} size="medium" />}
            <p className="hq-shelf-year">{champ.season}</p>
            <p className="hq-shelf-name" style={{ color: champ.championManager?.color }}>{champ.championManager?.name}</p>
            <p className="hq-shelf-team">{champ.championTeam}</p>
          </div>)}
          <div className="hq-shelf-item hq-shelf-item-soon">
            <span className="hq-shelf-icon">🏆</span>
            <p className="hq-shelf-year">{Math.max(...seasons) + 1}</p>
            <p className="hq-shelf-name">???</p>
            <p className="hq-shelf-team">Who will it be?</p>
          </div>
        </div>
        <div className="hq-shelf-plank" aria-hidden="true" />
      </section>

    </div>

    <footer className="hq-footer">
      <p className="hq-footer-emoji">🏈</p>
      <p className="hq-footer-name">Espinosa Fantasy Football Clubhouse</p>
      <p className="hq-footer-tag">Est. {FOUNDED} • Family is the whole league</p>
    </footer>
  </main>;
}
