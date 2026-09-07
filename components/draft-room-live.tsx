"use client";

import { useEffect, useRef, useState } from "react";
import { ManagerIdentity } from "@/components/manager-identity";
import { PlayerIdentity } from "@/components/player-identity";
import { TeamLogo } from "@/components/team-logo";
import { deriveDraftView, type DraftPickView, type DraftView } from "@/lib/draft-client";
import { useFamilyDraftState, type FamilyDraftState } from "@/lib/use-family-draft-state";

function pickAsIdentity(pick: DraftPickView) {
  return { name: pick.playerName, position: pick.position as "QB" | "RB" | "WR" | "TE" | "K" | "DEF", nflTeam: pick.nflTeam ?? "", imageUrl: pick.imageUrl };
}

function ConnectionNote({ connection, error }: { connection: string; error: string | null }) {
  if (connection !== "reconnecting") return null;
  return <p className="draft-live-connection" role="status">📶 Reconnecting to the clubhouse… {error}</p>;
}

function BigBoard({ state, view }: { state: FamilyDraftState; view: DraftView }) {
  return <section className="hq-section">
    <div className="section-heading"><h2>The Big Board</h2><span>{state.picks.length} of {view.totalSlots} picks in</span></div>
    <div className="draft-board-scroll">
      <table className="draft-board" style={{ "--board-columns": view.teams.length } as React.CSSProperties}>
        <thead>
          <tr>
            <th scope="col" className="draft-board-round-header"><span className="sr-only">Round</span></th>
            {view.teams.map((team) => <th scope="col" key={team.id} style={{ "--seat-color": team.manager?.color } as React.CSSProperties}>
              {team.manager && <TeamLogo manager={team.manager} size="small" />}
              <span>{team.teamName}</span>
            </th>)}
          </tr>
        </thead>
        <tbody>
          {view.slotsByRound.map((roundSlots, index) => {
            const byTeam = new Map(roundSlots.map((slot) => [slot.teamId, slot]));
            return <tr key={index}>
              <th scope="row" className="draft-board-round-header">R{index + 1}</th>
              {view.teams.map((team) => {
                const slot = byTeam.get(team.id);
                const pick = slot ? view.pickBySlotId.get(slot.id) : undefined;
                const isCurrent = slot != null && view.currentSlot?.id === slot.id;
                return <td key={team.id} className={isCurrent ? "draft-board-current" : pick ? "draft-board-filled" : "draft-board-open"}
                  style={{ "--seat-color": team.manager?.color } as React.CSSProperties}>
                  {pick
                    ? <PlayerIdentity player={pickAsIdentity(pick)} size="small" />
                    : isCurrent
                      ? <span className="draft-board-now">Picking now…</span>
                      : <span className="draft-board-slot-label">{slot?.rosterSlot ?? ""} · #{slot?.overall ?? ""}</span>}
                </td>;
              })}
            </tr>;
          })}
        </tbody>
      </table>
    </div>
  </section>;
}

function Rosters({ view, heading = "Every Team So Far" }: { view: DraftView; heading?: string }) {
  return <section className="hq-section">
    <div className="section-heading"><h2>{heading}</h2></div>
    <div className="draft-roster-grid">
      {view.teams.map((team) => {
        const teamSlots = view.slotsByRound.flat().filter((slot) => slot.teamId === team.id);
        return <article className="draft-roster-card" key={team.id} style={{ "--seat-color": team.manager?.color } as React.CSSProperties}>
          <header>
            {team.manager && <ManagerIdentity manager={team.manager} size="small" showName />}
            <strong>{team.teamName}</strong>
          </header>
          <ul>
            {teamSlots.map((slot) => {
              const pick = view.pickBySlotId.get(slot.id);
              return <li key={slot.id}>
                <b>{slot.rosterSlot}</b>
                {pick
                  ? <PlayerIdentity player={pickAsIdentity(pick)} size="small" />
                  : <span className="draft-roster-open">Round {slot.round} · pick #{slot.overall}</span>}
              </li>;
            })}
          </ul>
        </article>;
      })}
    </div>
  </section>;
}

function Results({ state, view }: { state: FamilyDraftState; view: DraftView }) {
  const [copied, setCopied] = useState(false);
  const copyResults = async () => {
    const lines = view.slotsByRound.flat().map((slot) => {
      const pick = view.pickBySlotId.get(slot.id);
      const team = view.teamById.get(slot.teamId);
      return `${slot.overall}. (R${slot.round}) ${team?.teamName ?? "?"} — ${pick ? `${pick.playerName} (${pick.position}, ${pick.nflTeam ?? ""})` : "—"}`;
    });
    try {
      await navigator.clipboard.writeText([`Espinosa Family Draft ${state.draft.season}`, ...lines].join("\n"));
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2500);
    } catch {
      // Clipboard can be unavailable; the printable board remains.
    }
  };
  return <section className="hq-section draft-results-actions">
    <div className="section-heading"><h2>🏆 That&rsquo;s a Wrap!</h2><span>Every pick is in the books</span></div>
    <p>The {state.draft.season} family draft is complete. Dad enters these rosters into Yahoo, and the results live here forever.</p>
    <div className="draft-results-buttons">
      <button type="button" onClick={copyResults}>{copied ? "✓ Copied!" : "Copy results"}</button>
      <button type="button" onClick={() => window.print()}>Print the board</button>
    </div>
  </section>;
}

export function DraftRoomLive({ draftId }: { draftId: string }) {
  const { state, connection, error } = useFamilyDraftState(draftId);
  const view = state ? deriveDraftView(state) : null;

  // Celebrate briefly whenever a new latest pick lands.
  const [celebrating, setCelebrating] = useState(false);
  const lastPickId = useRef<string | null>(null);
  const latestPickId = view?.latestPick?.id ?? null;
  useEffect(() => {
    const previous = lastPickId.current;
    lastPickId.current = latestPickId;
    if (latestPickId && previous && latestPickId !== previous) {
      setCelebrating(true);
      const celebration = window.setTimeout(() => setCelebrating(false), 4000);
      return () => window.clearTimeout(celebration);
    }
  }, [latestPickId]);

  if (!state || !view) {
    return <section className="hq-section draft-live-loading" aria-busy="true">
      <p>🏟️ Opening the draft room…</p>
      {error && <p className="draft-live-connection">{error} Retrying automatically.</p>}
    </section>;
  }

  const { draft } = state;
  const latestTeam = view.latestPick ? view.teamById.get(view.latestPick.teamId) : null;
  const latestSlot = view.latestPick ? view.slotById.get(view.latestPick.slotId) : null;

  return <div className="draft-live">
    <ConnectionNote connection={connection} error={error} />

    {draft.status === "ready" && <section className="hq-section draft-live-banner">
      <h2>🎬 Almost time!</h2>
      <p>The draft order is set. When everyone&rsquo;s couch-ready, Dad hits start on his device.</p>
    </section>}

    {draft.status === "live" && view.currentTeam?.manager && <section className={`hq-section draft-live-now${celebrating ? " draft-live-now-celebrating" : ""}`}
      style={{ "--seat-color": view.currentTeam.manager.color, "--seat-light": view.currentTeam.manager.lightColor } as React.CSSProperties}>
      <div className="draft-live-now-picker">
        <p className="eyebrow">On the clock — round {view.currentSlot?.round} · pick {view.currentSlot?.overall} of {view.totalSlots}</p>
        <div className="draft-live-now-identity">
          <ManagerIdentity manager={view.currentTeam.manager} size="large" showName showTeam />
          <TeamLogo manager={view.currentTeam.manager} size="large" />
        </div>
        <p className="draft-live-now-note">🛋️ No clock, no rushing.</p>
      </div>
      {view.latestPick && latestTeam && <aside className={`draft-live-latest${celebrating ? " draft-live-latest-pop" : ""}`}>
        <p className="eyebrow">Latest pick — #{latestSlot?.overall}</p>
        <PlayerIdentity player={pickAsIdentity(view.latestPick)} size="large" />
        <p>to <strong>{latestTeam.teamName}</strong> {latestTeam.manager?.emoji}</p>
      </aside>}
    </section>}

    {draft.status === "complete" && <Results state={state} view={view} />}

    <BigBoard state={state} view={view} />
    <Rosters view={view} heading={draft.status === "complete" ? "Final Rosters" : "Every Team So Far"} />
  </div>;
}
