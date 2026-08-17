"use client";

import { useCallback, useEffect, useRef, useState } from "react";

export type FamilyDraftState = {
  draft: { id: string; season: number; status: string; orderType: string; rounds: number; rosterSlots: string[]; currentOverall: number; version: number };
  actor: { id: string; displayName: string; isCommissioner: boolean } | null;
  teams: { id: string; managerId: string; teamName: string; draftPosition: number }[];
  slots: { id: string; overall: number; round: number; pickInRound: number; teamId: string; rosterSlot: string }[];
  picks: { id: string; slotId: string; teamId: string; playerId: string; playerName: string; position: string; nflTeam: string | null; overallRank: number | null; imageUrl: string | null }[];
};

export function useFamilyDraftState(draftId: string, refreshMs = 2500) {
  const [state, setState] = useState<FamilyDraftState | null>(null);
  const [connection, setConnection] = useState<"connecting" | "ready" | "reconnecting">("connecting");
  const [error, setError] = useState<string | null>(null);
  const activeRequest = useRef<AbortController | null>(null);

  const refresh = useCallback(async () => {
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    try {
      const response = await fetch(`/api/draft/${encodeURIComponent(draftId)}/state`, { cache: "no-store", signal: controller.signal });
      const result = await response.json() as FamilyDraftState & { error?: string };
      if (!response.ok) throw new Error(result.error || "The draft board could not be refreshed.");
      setState(result);
      setConnection("ready");
      setError(null);
    } catch (cause) {
      if (controller.signal.aborted) return;
      setConnection("reconnecting");
      setError(cause instanceof Error ? cause.message : "The draft board could not be refreshed.");
    }
  }, [draftId]);

  useEffect(() => {
    const initial = window.setTimeout(() => { void refresh(); }, 0);
    const interval = window.setInterval(() => { if (!document.hidden) void refresh(); }, refreshMs);
    const refreshOnReturn = () => { if (!document.hidden) void refresh(); };
    window.addEventListener("focus", refreshOnReturn);
    document.addEventListener("visibilitychange", refreshOnReturn);
    return () => {
      window.clearInterval(interval);
      window.clearTimeout(initial);
      window.removeEventListener("focus", refreshOnReturn);
      document.removeEventListener("visibilitychange", refreshOnReturn);
      activeRequest.current?.abort();
    };
  }, [refresh, refreshMs]);

  return { state, connection, error, refresh };
}
