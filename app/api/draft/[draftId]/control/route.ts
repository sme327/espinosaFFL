import { randomUUID } from "node:crypto";
import { env } from "cloudflare:workers";
import { NextResponse } from "next/server";
import { requireDraftDb } from "@/db";
import { currentDraftActor } from "@/lib/server/draft-auth";

type CorrectionBody = { action?: "undo-latest"; draftVersion?: number; idempotencyKey?: string; reason?: string };

export async function POST(request: Request, context: { params: Promise<{ draftId: string }> }) {
  const actor = await currentDraftActor();
  if (!actor) return NextResponse.json({ error: "Enter your commissioner PIN first." }, { status: 401 });
  if (!actor.isCommissioner) return NextResponse.json({ error: "Only the commissioner can correct a pick." }, { status: 403 });

  const { draftId } = await context.params;
  const body = await request.json().catch(() => null) as CorrectionBody | null;
  if (!body || body.action !== "undo-latest" || !Number.isInteger(body.draftVersion) || typeof body.idempotencyKey !== "string" || body.idempotencyKey.length > 160 || typeof body.reason !== "string" || !body.reason.trim()) {
    return NextResponse.json({ error: "Choose undo latest and briefly explain the correction." }, { status: 400 });
  }

  const db = requireDraftDb(env);
  const draft = await db.prepare("SELECT status, version FROM draft_seasons WHERE id = ?")
    .bind(draftId).first<{ status: string; version: number }>();
  if (!draft || !["live", "complete"].includes(draft.status)) return NextResponse.json({ error: "This draft cannot be corrected right now." }, { status: 409 });
  if (draft.version !== body.draftVersion) return NextResponse.json({ error: "The board changed. Reload before correcting a pick.", currentVersion: draft.version }, { status: 409 });

  const latest = await db.prepare(
    `SELECT p.id, p.slot_id AS slotId, p.player_id AS playerId, s.overall
       FROM draft_picks_live p JOIN draft_slots s ON s.id = p.slot_id
      WHERE p.draft_id = ? AND p.reversed_at IS NULL ORDER BY s.overall DESC LIMIT 1`,
  ).bind(draftId).first<{ id: string; slotId: string; playerId: string; overall: number }>();
  if (!latest) return NextResponse.json({ error: "There is no pick to undo." }, { status: 409 });

  const remaining = await db.prepare("SELECT id, slot_id AS slotId, player_id AS playerId FROM draft_picks_live WHERE draft_id = ? AND reversed_at IS NULL AND id != ? ORDER BY created_at")
    .bind(draftId, latest.id).all<{ id: string; slotId: string; playerId: string }>();
  const nextVersion = draft.version + 1;
  const eventId = randomUUID();
  const snapshotId = randomUUID();
  const transitionId = randomUUID();
  const payload = { pickId: latest.id, slotId: latest.slotId, playerId: latest.playerId, overall: latest.overall, reason: body.reason.trim() };
  const snapshot = { draftId, version: nextVersion, currentOverall: latest.overall, status: "live", picks: remaining.results, lastEvent: { type: "pick.undone", ...payload } };

  try {
    await db.batch([
      db.prepare("INSERT INTO draft_transitions (id, draft_id, from_version, to_version, idempotency_key) VALUES (?, ?, ?, ?, ?)").bind(transitionId, draftId, draft.version, nextVersion, body.idempotencyKey),
      db.prepare("UPDATE draft_picks_live SET reversed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND reversed_at IS NULL").bind(latest.id),
      db.prepare("INSERT INTO draft_events (id, draft_id, sequence, event_type, actor_manager_id, idempotency_key, payload_json) VALUES (?, ?, ?, 'pick.undone', ?, ?, ?)").bind(eventId, draftId, nextVersion, actor.id, body.idempotencyKey, JSON.stringify(payload)),
      db.prepare("INSERT INTO draft_snapshots (id, draft_id, event_sequence, state_json) VALUES (?, ?, ?, ?)").bind(snapshotId, draftId, nextVersion, JSON.stringify(snapshot)),
      db.prepare("UPDATE draft_seasons SET current_overall = ?, version = ?, status = 'live', completed_at = NULL, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND version = ?").bind(latest.overall, nextVersion, draftId, draft.version),
    ]);
  } catch {
    const replay = await db.prepare("SELECT id FROM draft_events WHERE draft_id = ? AND idempotency_key = ? AND event_type = 'pick.undone'")
      .bind(draftId, body.idempotencyKey).first<{ id: string }>();
    if (replay) return NextResponse.json({ ok: true, replayed: true });
    return NextResponse.json({ error: "The board changed before the correction could be saved. Reload and try again." }, { status: 409 });
  }

  return NextResponse.json({ ok: true, undone: payload, draft: { version: nextVersion, currentOverall: latest.overall, status: "live" } });
}
