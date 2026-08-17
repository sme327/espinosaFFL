import { env } from "cloudflare:workers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { currentDraftActor } from "@/lib/server/draft-auth";

export async function GET(_request: Request, context: { params: Promise<{ draftId: string }> }) {
  const { draftId } = await context.params;
  const db = requireDraftDb(env);
  const draft = await db.prepare(
    "SELECT id, season, status, order_type AS orderType, rounds, roster_slots_json AS rosterSlotsJson, current_overall AS currentOverall, version FROM draft_seasons WHERE id = ?",
  ).bind(draftId).first<{ id: string; season: number; status: string; orderType: string; rounds: number; rosterSlotsJson: string; currentOverall: number; version: number }>();
  if (!draft) return NextResponse.json({ error: "Draft not found." }, { status: 404 });

  const [actor, teams, slots, picks] = await Promise.all([
    currentDraftActor(),
    db.prepare(
      "SELECT id, manager_id AS managerId, team_name AS teamName, draft_position AS draftPosition FROM draft_teams WHERE draft_id = ? AND active = 1 ORDER BY draft_position",
    ).bind(draftId).all<{ id: string; managerId: string; teamName: string; draftPosition: number }>(),
    db.prepare(
      "SELECT id, overall, round, pick_in_round AS pickInRound, team_id AS teamId, roster_slot AS rosterSlot FROM draft_slots WHERE draft_id = ? ORDER BY overall",
    ).bind(draftId).all<{ id: string; overall: number; round: number; pickInRound: number; teamId: string; rosterSlot: string }>(),
    db.prepare(
      `SELECT p.id, p.slot_id AS slotId, p.team_id AS teamId, p.actor_manager_id AS actorManagerId, p.selection_type AS selectionType,
              p.created_at AS createdAt, pl.id AS playerId, pl.name AS playerName, pl.position, pl.nfl_team AS nflTeam,
              pl.overall_rank AS overallRank, pl.image_url AS imageUrl
         FROM draft_picks_live p JOIN draft_players pl ON pl.id = p.player_id
        WHERE p.draft_id = ? AND p.reversed_at IS NULL ORDER BY p.created_at`,
    ).bind(draftId).all<{ id: string; slotId: string; teamId: string; actorManagerId: string; selectionType: string; createdAt: string; playerId: string; playerName: string; position: string; nflTeam: string | null; overallRank: number | null; imageUrl: string | null }>(),
  ]);

  const response = NextResponse.json({
    draft: { ...draft, rosterSlots: JSON.parse(draft.rosterSlotsJson) as string[], rosterSlotsJson: undefined },
    actor,
    teams: teams.results,
    slots: slots.results,
    picks: picks.results,
  });
  response.headers.set("Cache-Control", "no-store");
  return response;
}
