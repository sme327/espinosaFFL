"use client";

import { useMemo, useRef, useState } from "react";
import { ManagerIdentity } from "@/components/manager-identity";
import { PlayerIdentity, type DraftPlayerIdentity } from "@/components/player-identity";
import playerPool from "@/data/draft/players-2026.json";
import { deriveDraftView, joinDraft, leaveDraft, loadFavorites, saveFavorites, submitControl, submitPick } from "@/lib/draft-client";
import { useFamilyDraftState } from "@/lib/use-family-draft-state";

type PoolPlayer = DraftPlayerIdentity & { id: string; overallRank: number; byeWeek: number | null };
type PositionFilter = "ALL" | "FAV" | PoolPlayer["position"];

const POSITION_FILTERS: { key: PositionFilter; label: string }[] = [
  { key: "ALL", label: "Everyone" },
  { key: "FAV", label: "⭐ Favorites" },
  { key: "QB", label: "QB" },
  { key: "RB", label: "RB" },
  { key: "WR", label: "WR" },
  { key: "TE", label: "TE" },
  { key: "K", label: "K" },
  { key: "DEF", label: "DEF" },
];

const ALL_PLAYERS = playerPool.players as PoolPlayer[];
const NO_FAVORITES: Set<string> = new Set();

export function DraftPickLive({ draftId }: { draftId: string }) {
  const { state, connection, error, refresh } = useFamilyDraftState(draftId);
  const view = state ? deriveDraftView(state) : null;

  const [positionFilter, setPositionFilter] = useState<PositionFilter>("ALL");
  const [teamFilter, setTeamFilter] = useState("ALL");
  const [search, setSearch] = useState("");
  const [favoritesFor, setFavoritesFor] = useState<{ managerId: string; favorites: Set<string> } | null>(null);
  const [confirming, setConfirming] = useState<PoolPlayer | null>(null);
  const [overrideReason, setOverrideReason] = useState("");
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const idempotencyKey = useRef<string>("");

  const actor = state?.actor ?? null;
  const season = state?.draft.season ?? playerPool.season;

  // Derived-from-props state: reload favorites when a different person takes the device.
  if (actor && favoritesFor?.managerId !== actor.id) {
    setFavoritesFor({ managerId: actor.id, favorites: loadFavorites(season, actor.id) });
  }
  const favorites = favoritesFor?.favorites ?? NO_FAVORITES;

  const availablePlayers = useMemo(() => {
    if (!view) return [];
    const query = search.trim().toLowerCase();
    return ALL_PLAYERS.filter((player) => !view.pickedPlayerIds.has(player.id))
      .filter((player) => positionFilter === "ALL" || (positionFilter === "FAV" ? favorites.has(player.id) : player.position === positionFilter))
      .filter((player) => teamFilter === "ALL" || player.nflTeam === teamFilter)
      .filter((player) => !query || player.name.toLowerCase().includes(query));
  }, [view, positionFilter, teamFilter, search, favorites]);

  if (!state || !view) {
    return <section className="hq-section draft-live-loading" aria-busy="true">
      <p>🏈 Getting your draft seat ready…</p>
      {error && <p className="draft-live-connection">{error} Retrying automatically.</p>}
    </section>;
  }

  const { draft } = state;

  // ── Who are you? ──
  if (!actor) {
    return <section className="hq-section draft-whoami">
      <div className="section-heading"><h2>Who&rsquo;s holding this device?</h2><span>Tap your name — no passwords in this house</span></div>
      <div className="draft-whoami-grid">
        {view.teams.map((team) => team.manager && <button type="button" key={team.id} className="draft-whoami-tile"
          style={{ "--seat-color": team.manager.color, "--seat-light": team.manager.lightColor } as React.CSSProperties}
          onClick={async () => {
            const result = await joinDraft(team.managerId);
            if (!result.ok) setNotice(result.error ?? null);
            await refresh();
          }}>
          <ManagerIdentity manager={team.manager} size="large" showName showTeam />
        </button>)}
      </div>
      {notice && <p className="draft-live-connection" role="alert">{notice}</p>}
    </section>;
  }

  const myTeam = view.teams.find((team) => team.managerId === actor.id) ?? null;
  const isMyTurn = draft.status === "live" && view.currentTeam?.managerId === actor.id;
  const isProxyPick = draft.status === "live" && actor.isCommissioner && !isMyTurn;
  const canPickNow = draft.status === "live" && (isMyTurn || actor.isCommissioner);
  const myNextSlot = myTeam && view.currentSlot
    ? view.slotsByRound.flat().find((slot) => slot.teamId === myTeam.id && slot.overall >= view.currentSlot!.overall)
    : null;
  const picksUntilMyTurn = myNextSlot && view.currentSlot ? myNextSlot.overall - view.currentSlot.overall : null;

  const toggleFavorite = (playerId: string) => {
    const next = new Set(favorites);
    if (next.has(playerId)) next.delete(playerId); else next.add(playerId);
    setFavoritesFor({ managerId: actor.id, favorites: next });
    saveFavorites(season, actor.id, next);
  };

  const openConfirm = (player: PoolPlayer) => {
    idempotencyKey.current = crypto.randomUUID();
    setOverrideReason("");
    setNotice(null);
    setConfirming(player);
  };

  const confirmPick = async () => {
    if (!confirming || !view.currentSlot || saving) return;
    setSaving(true);
    const result = await submitPick(draftId, {
      playerId: confirming.id,
      slotId: view.currentSlot.id,
      draftVersion: draft.version,
      idempotencyKey: idempotencyKey.current,
      overrideReason: isProxyPick ? overrideReason.trim() : undefined,
    });
    setSaving(false);
    if (result.ok) {
      setConfirming(null);
      setNotice(null);
    } else {
      setNotice(result.error ?? null);
      if (result.currentVersion !== undefined) setConfirming(null);
    }
    await refresh();
  };

  const startDraft = async () => {
    const result = await submitControl(draftId, { action: "start", draftVersion: draft.version, idempotencyKey: crypto.randomUUID() });
    setNotice(result.ok ? null : result.error ?? null);
    await refresh();
  };

  const undoLatest = async () => {
    const reason = window.prompt("Undo the latest pick — what needs fixing?");
    if (!reason?.trim()) return;
    const result = await submitControl(draftId, { action: "undo-latest", draftVersion: draft.version, idempotencyKey: crypto.randomUUID(), reason: reason.trim() });
    setNotice(result.ok ? null : result.error ?? null);
    await refresh();
  };

  return <div className="draft-live draft-pick-page" style={myTeam?.manager ? { "--seat-color": myTeam.manager.color, "--seat-light": myTeam.manager.lightColor } as React.CSSProperties : undefined}>
    {connection === "reconnecting" && <p className="draft-live-connection" role="status">📶 Reconnecting to the clubhouse… your picks are safe.</p>}

    <section className="hq-section draft-me-bar">
      {myTeam?.manager
        ? <ManagerIdentity manager={myTeam.manager} size="medium" showName showTeam />
        : <strong>{actor.displayName}</strong>}
      {actor.isCommissioner && <span className="draft-me-commissioner">Commissioner</span>}
      <button type="button" className="draft-ghost-button" onClick={async () => { await leaveDraft(); await refresh(); }}>Switch person</button>
    </section>

    {notice && <p className="draft-live-connection" role="alert">{notice}</p>}

    {draft.status === "ready" && <section className="hq-section draft-live-banner">
      <h2>🎬 Almost draft time!</h2>
      <p>Get comfy. {actor.isCommissioner ? "When everyone's ready, start the draft." : "Dad will start the draft when everyone's ready."}</p>
      {actor.isCommissioner && <button type="button" className="draft-primary-button" onClick={startDraft}>🏈 Start the family draft</button>}
    </section>}

    {draft.status === "complete" && <section className="hq-section draft-live-banner">
      <h2>🏆 The draft is done!</h2>
      <p>Head to the big board to see every roster, or relive your picks below.</p>
    </section>}

    {draft.status === "live" && <section className={`hq-section draft-turn-banner${isMyTurn ? " draft-turn-mine" : ""}`}>
      {isMyTurn
        ? <><h2>🎉 {actor.displayName}, you&rsquo;re on the clock!</h2><p>Round {view.currentSlot?.round} · pick #{view.currentSlot?.overall}. Take your time and pick your player below.</p></>
        : <><h2>{view.currentTeam?.manager?.emoji} {view.currentTeam?.manager?.name ?? "Someone"} is picking…</h2>
          <p>{picksUntilMyTurn != null && picksUntilMyTurn > 0 && myTeam ? `You're up in ${picksUntilMyTurn} pick${picksUntilMyTurn === 1 ? "" : "s"}. ` : ""}Browse and star favorites while you wait.</p></>}
      {actor.isCommissioner && state.picks.length > 0 && <button type="button" className="draft-ghost-button" onClick={undoLatest}>↩︎ Undo latest pick</button>}
    </section>}

    {myTeam && <section className="hq-section draft-my-roster">
      <div className="section-heading"><h2>My Team</h2><span>{state.picks.filter((pick) => pick.teamId === myTeam.id).length} of {draft.rounds} spots filled</span></div>
      <ul>
        {view.slotsByRound.flat().filter((slot) => slot.teamId === myTeam.id).map((slot) => {
          const pick = view.pickBySlotId.get(slot.id);
          return <li key={slot.id}>
            <b>{slot.rosterSlot}</b>
            {pick ? <PlayerIdentity player={{ name: pick.playerName, position: pick.position as PoolPlayer["position"], nflTeam: pick.nflTeam ?? "", imageUrl: pick.imageUrl }} size="small" />
              : <span className="draft-roster-open">Open — round {slot.round}</span>}
          </li>;
        })}
      </ul>
    </section>}

    <section className="hq-section">
      <div className="section-heading"><h2>Available Players</h2><span>{availablePlayers.length} to choose from</span></div>
      <div className="draft-filter-bar" role="group" aria-label="Player filters">
        {POSITION_FILTERS.map((filter) => <button type="button" key={filter.key}
          className={`draft-filter-chip${positionFilter === filter.key ? " draft-filter-active" : ""}`}
          onClick={() => setPositionFilter(filter.key)}>{filter.label}</button>)}
        <select aria-label="NFL team" value={teamFilter} onChange={(event) => setTeamFilter(event.target.value)}>
          <option value="ALL">All NFL teams</option>
          {[...new Set(ALL_PLAYERS.map((player) => player.nflTeam))].sort().map((team) => <option key={team} value={team}>{team}</option>)}
        </select>
        <input type="search" placeholder="Search names…" aria-label="Search players" value={search} onChange={(event) => setSearch(event.target.value)} />
      </div>

      <div className="draft-pick-grid">
        {availablePlayers.slice(0, 60).map((player) => <article className="draft-pick-card" key={player.id}>
          <span className="draft-player-rank">#{player.overallRank}</span>
          <button type="button" className={`draft-fav-star${favorites.has(player.id) ? " draft-fav-on" : ""}`}
            aria-label={favorites.has(player.id) ? `Remove ${player.name} from favorites` : `Add ${player.name} to favorites`}
            onClick={() => toggleFavorite(player.id)}>★</button>
          <PlayerIdentity player={player} size="large" />
          <small>{player.byeWeek ? `Bye week ${player.byeWeek}` : " "}</small>
          <button type="button" className="draft-primary-button" disabled={!canPickNow}
            onClick={() => openConfirm(player)}>
            {isMyTurn ? "Draft!" : isProxyPick ? `Pick for ${view.currentTeam?.manager?.name ?? "them"}` : "Wait for your turn"}
          </button>
        </article>)}
      </div>
      {availablePlayers.length > 60 && <p className="draft-pool-note">Showing the top 60 — use search or the filters to find anyone else.</p>}
    </section>

    {confirming && <div className="draft-confirm-backdrop" role="dialog" aria-modal="true" aria-label={`Confirm pick ${confirming.name}`}>
      <div className="draft-confirm-card">
        <p className="eyebrow">Round {view.currentSlot?.round} · pick #{view.currentSlot?.overall} · {view.currentTeam?.teamName}</p>
        <PlayerIdentity player={confirming} size="large" />
        {isProxyPick && <label className="draft-confirm-reason">Why is Dad making this pick?
          <input type="text" value={overrideReason} onChange={(event) => setOverrideReason(event.target.value)} placeholder="e.g. helping Elliot from the couch" />
        </label>}
        <div className="draft-confirm-buttons">
          <button type="button" className="draft-ghost-button" onClick={() => setConfirming(null)} disabled={saving}>Not yet</button>
          <button type="button" className="draft-primary-button" onClick={confirmPick} disabled={saving || (isProxyPick && !overrideReason.trim())}>
            {saving ? "Saving…" : `✅ Draft ${confirming.name}!`}
          </button>
        </div>
      </div>
    </div>}
  </div>;
}
