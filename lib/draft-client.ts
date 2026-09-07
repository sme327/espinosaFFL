"use client";

import { managerById, type Manager } from "@/lib/league";
import type { FamilyDraftState } from "@/lib/use-family-draft-state";

export type DraftTeamView = FamilyDraftState["teams"][number] & { manager: Manager | undefined };
export type DraftSlotView = FamilyDraftState["slots"][number];
export type DraftPickView = FamilyDraftState["picks"][number];

export type DraftView = {
  teams: DraftTeamView[];
  teamById: Map<string, DraftTeamView>;
  slotsByRound: DraftSlotView[][];
  slotById: Map<string, DraftSlotView>;
  pickBySlotId: Map<string, DraftPickView>;
  pickedPlayerIds: Set<string>;
  currentSlot: DraftSlotView | null;
  currentTeam: DraftTeamView | null;
  latestPick: DraftPickView | null;
  totalSlots: number;
};

export function deriveDraftView(state: FamilyDraftState): DraftView {
  const teams = [...state.teams]
    .sort((a, b) => a.draftPosition - b.draftPosition)
    .map((team) => ({ ...team, manager: managerById(team.managerId) }));
  const teamById = new Map(teams.map((team) => [team.id, team]));
  const slots = [...state.slots].sort((a, b) => a.overall - b.overall);
  const slotsByRound: DraftSlotView[][] = [];
  for (const slot of slots) (slotsByRound[slot.round - 1] ??= []).push(slot);
  const pickBySlotId = new Map(state.picks.map((pick) => [pick.slotId, pick]));
  const currentSlot = state.draft.status === "live"
    ? slots.find((slot) => slot.overall === state.draft.currentOverall) ?? null
    : null;
  return {
    teams,
    teamById,
    slotsByRound,
    slotById: new Map(slots.map((slot) => [slot.id, slot])),
    pickBySlotId,
    pickedPlayerIds: new Set(state.picks.map((pick) => pick.playerId)),
    currentSlot,
    currentTeam: currentSlot ? teamById.get(currentSlot.teamId) ?? null : null,
    latestPick: state.picks.length ? state.picks[state.picks.length - 1] : null,
    totalSlots: slots.length,
  };
}

async function draftRequest(url: string, init: RequestInit): Promise<{ ok: boolean; error?: string; currentVersion?: number }> {
  try {
    const response = await fetch(url, { headers: { "Content-Type": "application/json" }, ...init });
    const result = await response.json().catch(() => ({})) as { error?: string; currentVersion?: number };
    if (!response.ok) return { ok: false, error: result.error ?? "That didn't go through. Try again.", currentVersion: result.currentVersion };
    return { ok: true };
  } catch {
    return { ok: false, error: "The clubhouse couldn't be reached. Check the wifi and try again." };
  }
}

export function joinDraft(managerId: string) {
  return draftRequest("/api/draft/session", { method: "POST", body: JSON.stringify({ managerId }) });
}

export function leaveDraft() {
  return draftRequest("/api/draft/session", { method: "DELETE" });
}

export function submitPick(draftId: string, body: { playerId: string; slotId: string; draftVersion: number; idempotencyKey: string; overrideReason?: string }) {
  return draftRequest(`/api/draft/${encodeURIComponent(draftId)}/picks`, { method: "POST", body: JSON.stringify(body) });
}

export function submitControl(draftId: string, body: { action: "start" | "undo-latest"; draftVersion: number; idempotencyKey: string; reason?: string }) {
  return draftRequest(`/api/draft/${encodeURIComponent(draftId)}/control`, { method: "POST", body: JSON.stringify(body) });
}

const FAVORITES_PREFIX = "espinosa-draft-favorites";

export function loadFavorites(season: number, managerId: string): Set<string> {
  try {
    const raw = window.localStorage.getItem(`${FAVORITES_PREFIX}-${season}-${managerId}`);
    return new Set(raw ? JSON.parse(raw) as string[] : []);
  } catch {
    return new Set();
  }
}

export function saveFavorites(season: number, managerId: string, favorites: Set<string>): void {
  try {
    window.localStorage.setItem(`${FAVORITES_PREFIX}-${season}-${managerId}`, JSON.stringify([...favorites]));
  } catch {
    // Favorites are a convenience; losing them must never block a pick.
  }
}
