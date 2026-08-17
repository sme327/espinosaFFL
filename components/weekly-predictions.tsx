"use client";

import { useEffect, useState } from "react";
import type { Manager } from "@/lib/league";

type Matchup = { id: string; managerAId: string; managerBId: string; locksAt: string; featured: number };
type Prediction = { matchupId: string; participantManagerId: string; predictedManagerId: string; confidence: string };
type WeeklyData = { season: number; week: number; matchups: Matchup[]; predictions: Prediction[] };
const faces = [{ id: "unsure", icon: "🤔", label: "Could go either way" }, { id: "confident", icon: "🙂", label: "I think they win" }, { id: "super", icon: "🤩", label: "Super confident" }] as const;

export function WeeklyPredictions({ season, week, family }: { season: number; week: number; family: Manager[] }) {
  const [data, setData] = useState<WeeklyData | null>(null);
  const [participant, setParticipant] = useState(family[0]?.id ?? "");
  const [message, setMessage] = useState("");
  const [openedAt] = useState(() => Date.now());

  async function refresh() {
    const response = await fetch(`/api/weekly/${season}/${week}/predictions`, { cache: "no-store" });
    if (response.ok) setData(await response.json() as WeeklyData);
  }
  useEffect(() => {
    let active = true;
    fetch(`/api/weekly/${season}/${week}/predictions`, { cache: "no-store" })
      .then((response) => response.ok ? response.json() as Promise<WeeklyData> : null)
      .then((result) => { if (active && result) setData(result); });
    return () => { active = false; };
  }, [season, week]);

  async function choose(matchup: Matchup, winner: string, confidence: string) {
    setMessage("Saving…");
    const response = await fetch(`/api/weekly/${season}/${week}/predictions`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ matchupId: matchup.id, participantManagerId: participant, predictedManagerId: winner, confidence }) });
    const result = await response.json() as { error?: string };
    setMessage(response.ok ? "Pick saved! 🏈" : result.error ?? "That pick could not be saved.");
    if (response.ok) await refresh();
  }

  const manager = (id: string) => family.find((candidate) => candidate.id === id);
  const face = (person: Manager) => person.photoPath
    ? <img className="weekly-manager-photo" src={person.photoPath} alt="" />
    : person.teamLogoPath
      ? <img className="weekly-manager-logo" src={person.teamLogoPath} alt="" />
      : <span>{person.emoji}</span>;
  if (!data) return <div className="weekly-empty">Loading the family schedule…</div>;
  if (!data.matchups.length) return <div className="weekly-empty"><span>🗓️</span><h2>The prediction board is ready</h2><p>Week {week} matchups will appear here when the 2026 family schedule is added.</p><div className="weekly-face-preview">{faces.map((face) => <span key={face.id}>{face.icon}<small>{face.label}</small></span>)}</div></div>;

  return <div>
    <div className="weekly-who"><strong>Who is making picks?</strong>{family.map((person) => <button type="button" className={participant === person.id ? "active" : ""} onClick={() => setParticipant(person.id)} key={person.id} style={{ "--pick-color": person.color } as React.CSSProperties}>{face(person)}{person.name}</button>)}</div>
    <div className="weekly-matchups">{data.matchups.map((matchup) => {
      const a = manager(matchup.managerAId); const b = manager(matchup.managerBId);
      const saved = data.predictions.find((prediction) => prediction.matchupId === matchup.id && prediction.participantManagerId === participant);
      const locked = openedAt >= Date.parse(matchup.locksAt);
      return <article className="weekly-matchup" key={matchup.id}>
        {matchup.featured ? <span className="weekly-featured">⚔️ Game of the Week</span> : null}
        <h3>Who will win?</h3><div className="weekly-manager-choice">
          {[a, b].map((person) => person && <button key={person.id} type="button" disabled={locked} className={saved?.predictedManagerId === person.id ? "selected" : ""} onClick={() => void choose(matchup, person.id, saved?.confidence ?? "confident")} style={{ "--pick-color": person.color, "--pick-light": person.lightColor } as React.CSSProperties}>{face(person)}<strong>{person.name}</strong><small>{person.teamName}</small></button>)}
        </div><div className="weekly-confidence" aria-label="How confident are you?">{faces.map((face) => <button type="button" disabled={locked || !saved} className={saved?.confidence === face.id ? "selected" : ""} key={face.id} onClick={() => saved && void choose(matchup, saved.predictedManagerId, face.id)} aria-label={face.label}>{face.icon}<small>{face.label}</small></button>)}</div>
        {locked ? <p className="weekly-locked">🔒 This matchup has started.</p> : null}
      </article>;
    })}</div><p className="weekly-save-message" aria-live="polite">{message}</p>
  </div>;
}
