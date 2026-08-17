import { randomUUID } from "node:crypto";
import { env } from "cloudflare:workers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { currentDraftActor } from "@/lib/server/draft-auth";

type PickBody = { playerId?: string; slotId?: string; draftVersion?: number; idempotencyKey?: string; overrideReason?: string };

export async function POST(request: Request, context: { params: Promise<{ draftId: string }> }) {
  const actor = await currentDraftActor();
  if (!actor) return NextResponse.json({ error: "Enter your manager PIN before making a pick." }, { status: 401 });
  const { draftId } = await context.params;
  const body = await request.json().catch(() => null) as PickBody | null;
  if (!body || typeof body.playerId !== "string" || typeof body.slotId !== "string" || typeof body.idempotencyKey !== "string" || !Number.isInteger(body.draftVersion) || body.idempotencyKey.length > 160) {
    return NextResponse.json({ error: "The confirmed pick is incomplete." }, { status: 400 });
  }

  const db = requireDraftDb(env);
  const draft = await db.prepare("SELECT status, current_overall AS currentOverall, version FROM draft_seasons WHERE id = ?")
    .bind(draftId).first<{ status: string; currentOverall: number; version: number }>();
  if (!draft || draft.status !== "live") return NextResponse.json({ error: "The draft is not live." }, { status: 409 });
  if (draft.version !== body.draftVersion) return NextResponse.json({ error: "The board changed. Refresh and confirm again.", currentVersion: draft.version }, { status: 409 });

  const slot = await db.prepare(
    `SELECT s.id, s.overall, s.team_id AS teamId, t.manager_id AS managerId
       FROM draft_slots s JOIN draft_teams t ON t.id = s.team_id
      WHERE s.id = ? AND s.draft_id = ? AND t.active = 1`,
  ).bind(body.slotId, draftId).first<{ id: string; overall: number; teamId: string; managerId: string }>();
  if (!slot || slot.overall !== draft.currentOverall) return NextResponse.json({ error: "That is no longer the active pick." }, { status: 409 });

  const isProxy = actor.isCommissioner && actor.id !== slot.managerId;
  if (actor.id !== slot.managerId && !actor.isCommissioner) return NextResponse.json({ error: "Only the current manager can make this pick." }, { status: 403 });
  if (isProxy && !body.overrideReason?.trim()) return NextResponse.json({ error: "Commissioner proxy picks require a reason." }, { status: 400 });

  const player = await db.prepare("SELECT id, name, position, nfl_team AS nflTeam, overall_rank AS overallRank FROM draft_players WHERE id = ?")
    .bind(body.playerId).first<{ id: string; name: string; position: string; nflTeam: string | null; overallRank: number | null }>();
  if (!player) return NextResponse.json({ error: "Player not found." }, { status: 404 });

  const existing = await db.prepare("SELECT id, slot_id AS slotId, player_id AS playerId FROM draft_picks_live WHERE draft_id = ? AND reversed_at IS NULL ORDER BY created_at")
    .bind(draftId).all<{ id: string; slotId: string; playerId: string }>();
  const next = await db.prepare(
    `SELECT s.overall FROM draft_slots s LEFT JOIN draft_picks_live p ON p.slot_id = s.id AND p.reversed_at IS NULL
      WHERE s.draft_id = ? AND s.overall > ? AND p.id IS NULL ORDER BY s.overall LIMIT 1`,
  ).bind(draftId, slot.overall).first<{ overall: number }>();

  const pickId = randomUUID();
  const eventId = randomUUID();
  const snapshotId = randomUUID();
  const transitionId = randomUUID();
  const nextVersion = draft.version + 1;
  const nextOverall = next?.overall ?? slot.overall + 1;
  const nextStatus = next ? "live" : "complete";
  const payload = { pickId, slotId: slot.id, overall: slot.overall, teamId: slot.teamId, player, selectionType: isProxy ? "commissioner_proxy" : "manager", overrideReason: body.overrideReason?.trim() || null };
  const snapshot = { draftId, version: nextVersion, currentOverall: nextOverall, status: nextStatus, picks: [...existing.results, { id: pickId, slotId: slot.id, playerId: player.id }], lastEvent: payload };

  try {
    await db.batch([
      db.prepare("INSERT INTO draft_transitions (id, draft_id, from_version, to_version, idempotency_key) VALUES (?, ?, ?, ?, ?)").bind(transitionId, draftId, draft.version, nextVersion, body.idempotencyKey),
      db.prepare("INSERT INTO draft_picks_live (id, draft_id, slot_id, player_id, team_id, actor_manager_id, idempotency_key, selection_type, override_reason) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)").bind(pickId, draftId, slot.id, player.id, slot.teamId, actor.id, body.idempotencyKey, isProxy ? "commissioner_proxy" : "manager", body.overrideReason?.trim() || null),
      db.prepare("INSERT INTO draft_events (id, draft_id, sequence, event_type, actor_manager_id, idempotency_key, payload_json) VALUES (?, ?, ?, 'pick.confirmed', ?, ?, ?)").bind(eventId, draftId, nextVersion, actor.id, body.idempotencyKey, JSON.stringify(payload)),
      db.prepare("INSERT INTO draft_snapshots (id, draft_id, event_sequence, state_json) VALUES (?, ?, ?, ?)").bind(snapshotId, draftId, nextVersion, JSON.stringify(snapshot)),
      db.prepare("UPDATE draft_seasons SET current_overall = ?, version = ?, status = ?, updated_at = CURRENT_TIMESTAMP, completed_at = CASE WHEN ? = 'complete' THEN CURRENT_TIMESTAMP ELSE completed_at END WHERE id = ? AND version = ?").bind(nextOverall, nextVersion, nextStatus, nextStatus, draftId, draft.version),
    ]);
  } catch {
    const replay = await db.prepare("SELECT id, slot_id AS slotId, player_id AS playerId FROM draft_picks_live WHERE draft_id = ? AND idempotency_key = ?")
      .bind(draftId, body.idempotencyKey).first<{ id: string; slotId: string; playerId: string }>();
    if (replay) return NextResponse.json({ ok: true, replayed: true, pick: replay });
    return NextResponse.json({ error: "The board changed before this pick could be saved. Refresh and confirm again." }, { status: 409 });
  }

  return NextResponse.json({ ok: true, pick: payload, draft: { version: nextVersion, currentOverall: nextOverall, status: nextStatus } }, { status: 201 });
}
