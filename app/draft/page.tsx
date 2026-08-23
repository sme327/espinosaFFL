import type { Metadata } from "next";
import { ManagerIdentity } from "@/components/manager-identity";
import { PlayerIdentity, type DraftPlayerIdentity } from "@/components/player-identity";
import { TeamLogo } from "@/components/team-logo";
import { RoomHero } from "@/components/room-hero";
import playerPool from "@/data/draft/players-2026.json";
import { familyDraftForSeason } from "@/lib/family-draft";
import { managerById } from "@/lib/league";

export const metadata: Metadata = { title: "Draft Room" };

const POSITION_LABELS = { QB: "Quarterbacks", RB: "Running Backs", WR: "Wide Receivers", TE: "Tight Ends", K: "Kickers", DEF: "Defenses" } as const;
type DraftRoomPlayer = DraftPlayerIdentity & { id: string; overallRank: number; byeWeek: number };

export default function DraftRoomPage() {
  const draft = familyDraftForSeason(2026);
  if (!draft) throw new Error("The 2026 family draft has not been configured.");
  const activeManagers = draft.activeManagerIds.map(managerById).filter((manager) => manager !== undefined);
  const reservedManagers = draft.reservedManagerIds.map(managerById).filter((manager) => manager !== undefined);
  const featured = playerPool.players.slice(0, 12) as DraftRoomPlayer[];

  return <main className="page-wrap inner-page draft-room-page">
    <RoomHero room="draft" label="Espinosa Family Draft" title="2026 Draft Room" status="Getting ready for draft day">Big pictures, simple choices, and one shared board for the whole family.</RoomHero>

    <section className="hq-section">
      <div className="section-heading"><h2>Who&rsquo;s Drafting?</h2><span>4 teams this season · Wyatt&rsquo;s seat is saved</span></div>
      <div className="draft-family-row">
        {activeManagers.map((manager) => <article className="draft-manager-seat" key={manager.id} style={{ borderColor: manager.color }}>
          <ManagerIdentity manager={manager} size="large" showName showTeam />
          <TeamLogo manager={manager} size="medium" />
          <span>Ready to draft</span>
        </article>)}
        {reservedManagers.map((manager) => <article className="draft-manager-seat draft-manager-seat-future" key={manager.id}>
          <ManagerIdentity manager={manager} size="large" showName futureLabel />
          <TeamLogo manager={manager} size="medium" />
          <span>Seat saved for a future season</span>
        </article>)}
      </div>
    </section>

    <section className="hq-section draft-plan-card">
      <div>
        <p className="eyebrow">The simple plan</p>
        <h2>{draft.rounds} picks for each team</h2>
        <p>We&rsquo;ll use a snake draft. Everyone picks on their own device, and Dad can help make any pick when needed.</p>
      </div>
      <div className="draft-roster-chips" aria-label="Roster spots">
        {draft.rosterSlots.map((slot, index) => <span key={`${slot}-${index}`}>{index + 1}<b>{slot}</b></span>)}
      </div>
      <p className="draft-no-clock">🛋️ No clock. No rushing. We&rsquo;re all sitting together.</p>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Players to Know</h2><span>Top of the 2026 preseason list</span></div>
      <div className="draft-player-grid">
        {featured.map((player) => <article className="draft-player-card" key={player.id}>
          <span className="draft-player-rank">#{player.overallRank}</span>
          <PlayerIdentity player={player} size="large" />
          <small>{POSITION_LABELS[player.position]} · Bye {player.byeWeek}</small>
        </article>)}
      </div>
      <p className="draft-pool-note">349 ranked players are loaded. Player photos and official team art are the next visual layer; every player already has a clear, colorful fallback.</p>
    </section>
  </main>;
}
