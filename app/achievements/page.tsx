import type { Metadata } from "next";
import { ManagerIdentity } from "@/components/manager-identity";
import { TeamLogo } from "@/components/team-logo";
import { RoomHero } from "@/components/room-hero";
import { achievementCategories, achievements, historicalAchievementsFor } from "@/lib/achievements";
import { CLUBHOUSE_FAMILY } from "@/lib/league";
import { liveAwardsByManager, mergeWallAchievements } from "@/lib/server/achievement-awards";

export const metadata: Metadata = { title: "Achievement Wall" };

export default async function AchievementsPage() {
  const liveAwards = await liveAwardsByManager();
  return <main className="page-wrap inner-page achievement-page">
    <RoomHero room="achievements" label="The Family Hall of Fame" title="Achievement Wall">Winning is one way to shine. Showing up, helping, cheering, and making memories count too.</RoomHero>

    <section className="achievement-key" aria-label="Achievement categories">
      {achievementCategories.map((category) => <div key={category.id}><strong>{category.label}</strong><span>{category.description}</span></div>)}
    </section>

    <section className="achievement-lockers">
      {CLUBHOUSE_FAMILY.map((manager) => {
        const earned = mergeWallAchievements(historicalAchievementsFor(manager), liveAwards.get(manager.id) ?? []);
        const earnedIds = new Set(earned.map((award) => award.id));
        const nextUp = achievements.filter((achievement) => !earnedIds.has(achievement.id)).slice(0, 4);
        return <article className="achievement-locker" key={manager.id} style={{ "--locker-color": manager.color } as React.CSSProperties}>
          <header className="achievement-locker-head">
            <ManagerIdentity manager={manager} size="large" showName showTeam futureLabel={!manager.active} />
            <TeamLogo manager={manager} size="large" />
          </header>
          <div className="achievement-locker-label"><span>{earned.reduce((total, award) => total + award.count, 0)}</span> earned</div>
          <div className="achievement-earned">
            <h2>On the Wall</h2>
            {earned.length ? earned.map((award) => <div className="achievement-badge earned" key={award.id}>
              <span className="achievement-badge-icon" aria-hidden="true">{award.icon}</span>
              <div><strong>{award.name}</strong><p>{award.notes.length ? `“${award.notes[award.notes.length - 1]}”` : award.description}</p><small>{award.count > 1 ? `${award.count} times · ` : ""}{award.seasons.join(" · ")}</small></div>
            </div>) : <p className="achievement-empty">{manager.active ? "A fresh wall, ready for the next great moment." : "Wyatt’s space is ready before his first official season."}</p>}
          </div>
          <div className="achievement-next">
            <h2>Still to Unlock</h2>
            <div>{nextUp.map((award) => <span className="achievement-badge locked" key={award.id} title={award.description}><b aria-hidden="true">{award.icon}</b><small>{award.name}</small></span>)}</div>
          </div>
        </article>;
      })}
    </section>
    <p className="hq-page-footer">Espinosa FFL · Achievement Wall</p>
  </main>;
}
