import type { Metadata } from "next";
import { ClubhouseLink } from "@/components/clubhouse-link";
import { ManagerIdentity } from "@/components/manager-identity";
import { PlayerIdentity, type DraftPlayerIdentity } from "@/components/player-identity";
import { TeamLogo } from "@/components/team-logo";
import { RoomHero } from "@/components/room-hero";
import playerPool from "@/data/draft/players-2026.json";
import { familyDraftForSeason } from "@/lib/family-draft";
import { managerById } from "@/lib/league";

export const metadata: Metadata = { title: "Draft Room" };

const POSITION_LABELS = { QB: "Quarterbacks", RB: "Running Backs", WR: "Wide Receivers", TE: "Tight Ends", K: "Kickers", DEF: "Defenses" } as const;
const STATUS_LABELS = {
  planning: "Getting ready for draft day",
  ready: "Draft day is set",
  live: "Draft day is live!",
  complete: "The 2026 draft is in the books",
  closed: "Season underway",
} as const;
type DraftRoomPlayer = DraftPlayerIdentity & { id: string; overallRank: number; byeWeek: number };

export default function DraftRoomPage() {
  const draft = familyDraftForSeason(2026);
  if (!draft) throw new Error("The 2026 family draft has not been configured.");
  const drafted = draft.status === "complete" || draft.status === "closed";
  const activeManagers = draft.activeManagerIds.map(managerById).filter((manager) => manager !== undefined);
  const reservedManagers = draft.reservedManagerIds.map(managerById).filter((manager) => manager !== undefined);
  const featured = playerPool.players.slice(0, 12) as DraftRoomPlayer[];

  return <main className="page-wrap inner-page draft-room-page">
    <RoomHero room="draft" label="Espinosa Family Draft" title="2026 Draft Room" status={STATUS_LABELS[draft.status]}>Big pictures, simple choices, and one shared board for the whole family.</RoomHero>

    <section className="hq-section draft-door-row">
      <ClubhouseLink href="/draft/pick" className="draft-door">
        <span aria-hidden="true">🪑</span>
        <strong>My Draft Seat</strong>
        <small>{drafted ? "Relive your own picks from draft day." : "Everyone opens this on their own device to browse players and make picks."}</small>
      </ClubhouseLink>
      <ClubhouseLink href="/draft/room" className="draft-door">
        <span aria-hidden="true">📺</span>
        <strong>The Big Board</strong>
        <small>{drafted ? "The full 2026 results — every round, every roster, printable." : "Put this one on the TV — the shared board the whole family watches."}</small>
      </ClubhouseLink>
    </section>

    <section className="hq-section">
      <div className="section-heading"><h2>Who&rsquo;s Drafting?</h2><span>4 teams this season · Wyatt&rsquo;s seat is saved</span></div>
      <div className="draft-family-row">
        {activeManagers.map((manager) => <article className="draft-manager-seat" key={manager.id} style={{ borderColor: manager.color }}>
          <ManagerIdentity manager={manager} size="large" showName showTeam />
          <TeamLogo manager={manager} size="medium" />
          <span>{drafted ? "Roster in the books" : "Ready to draft"}</span>
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
        <p>{drafted
          ? "A snake draft, everyone on their own device — and every single pick was made by its own manager."
          : "We’ll use a snake draft. Everyone picks on their own device, and Dad can help make any pick when needed."}</p>
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
      <p className="draft-pool-note">{playerPool.playerCount} ranked players are loaded with photos and NFL team logos; anyone missing a picture gets a clear, colorful fallback.</p>
    </section>
  </main>;
}
